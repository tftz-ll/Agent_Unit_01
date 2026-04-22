"""
实现向量库的存储和文本分割
"""
import os.path
from langchain_chroma import Chroma
from Unit_01.utils.config_handler import chroma_conf
from Unit_01.utils.path_tool import get_abs_path
from Unit_01.model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from Unit_01.utils.file_hanlder import (listdir_with_allowed_type, get_file_md5_hex,
                                        check_md5_hex, get_file_documents, save_md5_hex)
from Unit_01.utils.logger_handler import logger
from langchain_core.documents import Document
from pathlib import Path


class VectorStoreService:
    """
    用于读取文件列表中的文件，
    并进行向量存储的类
        get_retriever 获得一个连接向量库的rag链
        load_document 读取文件夹列表，将未读入的文件进行写入操作
    """

    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embedding_model,
            persist_directory=get_abs_path(chroma_conf["persist_directory"])
        )
        self.split = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            length_function=len
        )

    def get_retriever(self):
        """
        获取向量匹配器
        :return:
        """
        return self.vector_store.as_retriever(
            search_retriever={"k": chroma_conf["k"]}
        )

    def load_document(self, path: str) -> str:
        """
        这个代码纯纯屎山，后面重构的时候需要重写
        传入一个文件地址，从文件列表读取文件
        转为向量存入向量库
        计算文件的md5进行去重
        :return: result: 代表文件载入向量库结果
        """
        # 获取完整的文件列表
        result = "None"
        allowed_file_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"])
        )

        if Path(path).suffix not in chroma_conf["allow_knowledge_file_type"]:
            logger.error(f"[vector_store 加载知识库] 文件{Path(path).name} 类型为 {Path(path).suffix} 不是允许的加载文件 {chroma_conf["allow_knowledge_file_type"]} 失败")
            return f"[vector_store 加载知识库] 文件{path} 不是允许的加载文件 {chroma_conf["allow_knowledge_file_type"]} 失败"

        # 去重操作部分
        logger.debug(f"当前加载文件 {path} !!!调试日志!!!")
        md5_path = get_file_md5_hex(path)
        if check_md5_hex(md5_path):
            logger.info(f"[vector_store 加载知识库] {path}内容已经存在知识库内，跳过")
            result = f"{path}内容已经存在知识库内，跳过"

        # 文档写入向量库部分
        try:
            documents: list[Document] = get_file_documents(path)

            if not documents:
                logger.warning(f"[vector_store 加载知识库] {path}内没有有效文本，跳过")

            split_documents = self.split.split_documents(documents)

            if not split_documents:
                logger.warning(f"[vector_store 加载知识库] {path}分片后没有有效内容，跳过")
            self.vector_store.add_documents(split_documents)
            logger.debug(f"{[i for i in split_documents]}")
            save_md5_hex(md5_path)
            logger.info(f"[vector_store 加载知识库] {path}内容加载 成功")
            result = f"{path}内容加载 成功"
        except Exception as e:
            # exc_info  为True时，记录详细的信息堆栈，如果为 False 仅记录报错信息本身
            logger.error(f"[加载知识库] 加载失败{str(e)}", exc_info=True)
            result = f"{path}内容加载 失败"
        return result

    def delete_document(self, file_path: str) -> str:
        """
        params:
            file_path: str 传入文件的绝对路径
        return: 返回向量知识库删除结果
        此函数根据chroma数据中的metadata source 进行数据删除（source默认为文件路径）
        """
        collection = self.vector_store._collection

        try:
            # 只有当删除的文件数量不为0时才判定删除成功
            res = collection.delete(where={'source': file_path})["deleted"]
        except Exception as e:
            logger.error(f"[delete_document 知识库删除操作] 文件{file_path}删除失败， 因为：\n{e}")
            return f"文件 [{Path(file_path).name}] 从知识库中删除 失败 "
        if res != 0:
            logger.info(f"[delete_document 知识库删除操作] 文件{file_path}删除成功 删除{res}条数据")
            return f"文件 [{Path(file_path).name}] 从知识库中删除 成功"
        else:
            return f"文件 [{Path(file_path).name}] 从知识库中删除 失败 "


if __name__ == "__main__":
    # vs = VectorStoreService().vector_store._collection
    #
    # vs.delete(where={'source': 'D:\\tool\\Agent_Unit_01\\Unit_01\\data\\08.列表&元组.pdf'})
    vs = VectorStoreService()
    # vs.load_document()
    retriever = vs.get_retriever()

    res = retriever.invoke("扫拖一体机")
    for i in res:
        print(i.page_content, i.metadata["source"])
        print("+"*80)
#





















"""
改进：
    1. 数据库替换文件读取
    2. 检查是否有数据库，有则用，否则logger警告，自动切换为文件读取模板运行
"""