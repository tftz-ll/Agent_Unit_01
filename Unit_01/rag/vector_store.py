"""
实现向量库的存储和文本分割
"""
import os.path
from langchain_chroma import Chroma
from Unit_01.utils.config_handler import chroma_conf
from Unit_01.utils.path_tool import get_abs_path
from Unit_01.model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from Unit_01.utils.file_hanlder import (txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex)
from Unit_01.utils.logger_handler import logger
from langchain_core.documents import Document


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embedding_model,
            persist_directory=chroma_conf["persist_directory"]
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

    def load_document(self):
        """
        从数据文件夹内读取文件，转为向量存入向量库
        计算文件的md5进行去重
        :return:
        """

        def check_md5_hex(md5: str):
            """
            处理过返回True，否则False
            :param md5:
            :return:
            """
            md5_save_path = get_abs_path(chroma_conf["md5_hex_store"])
            if not os.path.exists(md5_save_path):
                open(md5_save_path, "w", encoding="utf-8").close()
                return False
            # 我觉得有点怪

            with open(md5_save_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5:
                        return True  # 处理过

                return False  # 没处理过

        def save_md5_hex(md5: str):
            md5_save_path = get_abs_path(chroma_conf["md5_hex_store"])
            with open(md5_save_path, "a", encoding="utf-8") as f:
                f.write(md5 + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        allowed_file_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"])
        )

        for path in allowed_file_path:
            # 获取文件的MD5
            md5_path = get_file_md5_hex(path)
            if check_md5_hex(md5_path):
                logger.info(f"[vector_store 加载知识库] {path}内容已经存在知识库内， 跳过")
                continue

            try:
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[vector_store 加载知识库] {path}内没有有效文本，跳过")
                    continue

                split_documents = self.split.split_documents(documents)

                if not split_documents:
                    logger.warning(f"[vector_store 加载知识库] {path}分片后没有有效内容，跳过")
                self.vector_store.add_documents(split_documents)
                save_md5_hex(md5_path)
                logger.info(f"[vector_store 加载知识库] {path}内容加载成功")
            except Exception as e:
                # exc_info  为True时，记录详细的信息堆栈，如果为 False 仅记录报错信息本身
                logger.error(f"[加载知识库] 加载失败{str(e)}", exc_info=True)


"""
改进点：
    1. 去重判断的那几个函数塞同一个函数里很臃肿，新建一个类进行分离
    2. 假如以后要加入多模态的信息处理，图片信息的存储方式是否要实现以下？
    3. 去重判断使用redis更快，资源占用更少
"""

if __name__ == "__main__":
    vs = VectorStoreService()

    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")
    for i in res:
        print(i.page_content)
        print("+"*80)





















"""
改进：
    1. 数据库替换文件读取
    2. 检查是否有数据库，有则用，否则logger警告，自动切换为文件读取模板运行
"""