"""
目标：实现函数
get_file_md5_hex()
# 获取md5十六进制字符串
listdir_with_allowed_type()
# 返回文件夹内的文件列表(允许的文件后缀)
pdf_loader()
txt_loader()
"""
import hashlib
import os.path
from Unit_01.utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import (PyPDFLoader, TextLoader)


def get_file_md5_hex(file_path: str) -> str | None:
    """
    获取文件的md5十六进制字符串
    """
    # 文件导入，首先要判断路径是否正确，其次是该文件
    if not os.path.exists(file_path):
        logger.error(f"[md5计算] 文件{file_path}不存在")
        return
    if not os.path.isfile(file_path):
        # 怎么界定？比如说文件夹不是一个文件，快捷方式不是一个文件，这里是为了判断文件是否正规
        logger.error(f"[md5计算] 路径{file_path}不是文件")
        return

    md5_obj = hashlib.md5()

    chunk_size = 4096  # 4kb文件进行分片，避免加载爆内存
    try:
        with open(file_path, "rb") as f:  # 要对文件进行切片，就需要以二进制的形式进行读取
            while chunk := f.read(chunk_size):
                # 判断的同时声明变量
                """
                等价于
                while chunk:
                    chunk = f.read(chunk_size)
                这样写就得在前面声明变量，麻烦
                """
                md5_obj.update(chunk)
                md5_hex = md5_obj.hexdigest()
                return md5_hex
    except Exception as e:
        logger.error(f"计算文件{file_path}md5失败，{str(e)}")
        return


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    """
    返回文件夹内的文件列表（允许加载的文件）
    """
    files = []

    if not os.path.isdir(path):
        logger.error(f"[文件列表读取] {path}不是文件夹")

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return tuple(files)


def pdf_loader(file_path: str, passwd=None) -> list[Document]:
    """
    加载pdf格式的文件（只读文字内容）
    """
    return PyPDFLoader(file_path, passwd).load()


def txt_loader(file_path: str) -> list[Document]:
    """
    加载txt文本文件
    """
    return TextLoader(file_path, encoding="utf-8").load()


"""
可改进点：
    1. pdf和txt加载器中的load()全量加载如果遇到文件很大的情况可能会对内存造成压力
       考虑增加一个文件大小判断，在load和lazy_load()中切换
"""


