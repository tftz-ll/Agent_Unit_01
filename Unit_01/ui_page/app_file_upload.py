"""
基于Streamlit完成WEB网页上传服务

好处：简单的几行代码就可以完成快速的网页开发

每当 web 页面内容发生变化，本页代码重新执行
问题：1、状态丢失怎么解决？
        streamlit自带了session_state消息存放
     2、想要删除知识库 知识怎么办？
"""
import sys
from pathlib import Path

# 获取项目根目录（Unit_01 的父目录）
project_root = Path(__file__).parent.parent.parent  # app.py -> ui_page -> Unit_01 -> Agent_Unit_01
sys.path.insert(0, str(project_root))
import streamlit as st
import time
import os
from Unit_01.utils.file_hanlder import listdir_with_allowed_type, delete_file_data
from Unit_01.utils.path_tool import get_abs_path
from Unit_01.utils.logger_handler import logger
from Unit_01.rag.vector_store import VectorStoreService
from Unit_01.utils.config_handler import chroma_conf
# 创建大标题
st.title("知识库更新服务")

# 添加文件 file_uploader
uploader_files = st.file_uploader(
    label="请上传文件",
    type=["txt", "pdf"],
    accept_multiple_files=True,  # 仅接受单个文件的上传
)

# 创建知识库对象
session = st.session_state

if "vector_store" not in session:
    # 获取向量存储对象，使用vectory_store中写好的方法进行文件存储
    session["vector_store"] = VectorStoreService()
# """
# 正在进行文件上传页面制作
# 思路：
#     将文件保存到本地路径，再通过路径给pdfloader/textloader分割
#     通过文件名生成id，一同存入向量库中
#     生成文件已加载的页面，通过点击可以删除文件{通过id chroma.delete方法} // 似乎可以用.collection来访问chroma原生方法
# """

if uploader_files is not None:
    for uploader_file in uploader_files:
        file_name = uploader_file.name
        file_type = uploader_file.type
        file_size = uploader_file.size / 1024  # 转换为KB单位

        # .subheader 二级标题
        st.subheader(f"文件名：{file_name}")
        # .write 网页中显示正常大小的文本
        st.write(f"格式：{file_type}| 大小：{round(file_size, 2)} KB")

        # getvalue() 获取字节数据
        byte_data = uploader_file.getvalue()

        # 从文件夹中获取文件名初步判断，如果文件名相同则不加载文件，
        # 相同加载文件 再判断 如果md5值确认重复，文件夹中进行文件删除操作，否则正常进行向量加载操作
        file_name_pool = [Path(path).name for path in listdir_with_allowed_type(get_abs_path(chroma_conf["data_path"]),
                                                                                tuple(chroma_conf["allow_knowledge_file_type"]))]
        if file_name not in file_name_pool:
            # 文件写入列表部分
            with st.spinner("文件正在写入本地..."):
                # 转圈动画
                try:
                    # 将获取到的文件数据写入文件列表 /data
                    with open(get_abs_path(f"data/{file_name}"), "wb") as f:
                        f.write(byte_data)
                        res = "完成"
                        logger.info(f"[app_file_upload 文件上传页面] {file_name} 写入本地成功")
                except Exception as e:
                    logger.error(f"[app_file_upload 文件上传页面] 将文件{file_name} 写入本地时失败，因为：\n{e}")
                    res = "失败"
                time.sleep(0.3)

                st.write(f"[{file_name}] 写入列表 {res}")

            # 文件载入向量库部分
            if res == "完成":
                with st.spinner("文件正在载入知识库中"):
                    # 转圈动画
                    try:
                        # 调用类VectorStoreService 的方法读取文件列表，加载文件数据
                        res = session["vector_store"].load_document(get_abs_path(f"data\\{file_name}"))
                        logger.info(f"[app_file_upload 文件上传页面] {res}")
                    except Exception as e:
                        logger.error(f"[app_file_upload 文件上传页面] 将文件{file_name} 写入本地时失败，因为：\n{e}")
                        res = "失败"
                    st.write(f"[{file_name}] {res}")

            if res.endswith("跳过") or res.endswith("失败"):
                # 文件加载失败时，我们需要将文件从文件夹子中删除，避免文件堆积
                res = delete_file_data(get_abs_path(f"data/{file_name}"))
                st.write(f"文件{file_name} 由于加载失败，进行删除操作 | {res}")

        if file_name in file_name_pool:
            st.error(f"当前文件名重复，请确认是否上传了相同文件，或者请将文件从文件加载列表中移除！")

with st.expander("展开以删除文件"):
    # 删除文件部分
    path = listdir_with_allowed_type(get_abs_path(chroma_conf["data_path"]),
                                     tuple(chroma_conf["allow_knowledge_file_type"]))
    for file_path in path:
        file_name = Path(file_path).name
        # 将读取到的文件名称依次取出，写入expander内
        # 给每个文件创造三个空间分别存放名称、删除按钮、勾选框，勾选框选中的同时点击删除件才判定为确认删除此文件
        left, middle, right = st.columns(3, vertical_alignment="bottom")
        left.text(f"文件名: [{file_name}]")
        # 这里将文件名作为按钮键，这意味着文件名一定不能重复
        button1 = middle.button("Click me to delete", use_container_width=True, key=f"{file_name}_button")
        button2 = right.checkbox("Check me to ensure", key=f"{file_name}_checkbox")

        if button1 and button2:
            # 这边应当调用删除方法
            with st.spinner(f"删除文件[{file_name}]中..."):
                res = delete_file_data(file_path)
                st.write(res)
                time.sleep(0.2)
                print(file_path)
                res = session["vector_store"].delete_document(file_path)
                st.write(res)
                time.sleep(0.2)
                # res = session["vector_store"].load_document()
                # st.write(res)
                # time.sleep(0.2)
                ####################
                # test
                # retriever = session["vector_store"].get_retriever()
                #
                # res = retriever.invoke("有故障怎么办")
                # for i in res:
                #     st.write(i.page_content, i.metadata)
                #     st.write("+" * 80)
                ####################

            st.rerun()





