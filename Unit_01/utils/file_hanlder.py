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
from pathlib import Path
from Unit_01.utils.config_handler import chroma_conf
from Unit_01.utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import (PyPDFLoader, TextLoader)
from Unit_01.utils.path_tool import get_abs_path


def get_file_md5_hex(file_path: str) -> str | None:
    """
    params:
        file_path: str 传入文件的绝对路径
    return -> str 返回 MD5+文件名 组成的字符串
    注意！为了方便后续的文件删除操作，返回的是MD5＋文件名 组成的字符串，而不是真正意义上的MD5
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
        return md5_hex + Path(file_path).name
    except Exception as e:
        logger.error(f"计算文件{file_path}md5失败，{str(e)}")
        return


def delete_file_data(file_path: str) -> str:
    """
    params:
        file_path: str 需要删除的文件的绝对路径

    注意！这个方法会将文件和其对应的md5值（如果有的话）一并删除
    """
    file = Path(file_path)
    file_name = file.name  # 获取文件名称用于MD5的删除判断
    # 对文件本身进行删除：

    if not file.exists():
        logger.error(f"[delete_file_data 文件删除操作] 文件数据删除失败 | 所给路径{file_path}不存在!")
        return "删除失败，该文件不存在于文件夹中"
    try:
        file.unlink()
    except Exception as e:
        logger.error(f"[delete_file_data 文件删除操作] 文件数据删除失败 | 因为: {str(e)}")
        return f"删除失败，因为{str(e)}"

    # 对MD5值进行删除
    try:
        f = open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8")
        md5_list = [i.strip() for i in f.readlines()]
        f.close()

        with open(get_abs_path(chroma_conf["md5_hex_store"]), "w+", encoding="utf-8") as f:
            for md5 in md5_list:
                if md5.endswith(file_name):
                    md5_list.remove(md5)
                    break
            f.writelines([i + "\n" for i in md5_list])
            logger.info(f"[delete_file_data 文件删除操作] MD5：{md5}删除成功")
    except Exception as e:
        logger.error(f"[delete_file_data 文件删除操作] 文件MD5删除失败 | 因为: {str(e)}")
        return f"MD5删除失败，因为{str(e)}"
    return "文件删除成功！"


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    """
    参数：
        path: str 文件夹名称
        allowed_types: tuple[str] 允许加载的文件类型
    返回：可加载文件的绝对路径
    # 新增功能
    """
    files = []
    files_name = []

    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type 文件列表读取] {path}不是文件夹")

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


def get_file_documents(read_path: str, file=None):
    if read_path.endswith("txt"):
        return txt_loader(read_path)

    if read_path.endswith("pdf"):
        return pdf_loader(read_path)

    return []


def file_load_to_list(byte_data, file_name: str):
    """
    params:
        byte_data 字节流数据
    """
    try:
        # 将获取到的文件数据写入文件列表 \data
        with open(get_abs_path(f"data\\{file_name}"), "wb") as f:
            f.write(byte_data)
            res = "完成"
            logger.info(f"[app_file_upload 文件上传页面] {file_name} 写入本地成功")
    except Exception as e:
        logger.error(f"[app_file_upload 文件上传页面] 将文件{file_name} 写入本地时失败，因为：\n{e}")
        res = "失败"

"""
可改进点：
    1. pdf和txt加载器中的load()全量加载如果遇到文件很大的情况可能会对内存造成压力
       考虑增加一个文件大小判断，在load和lazy_load()中切换
    删掉删掉，这样会导致返回迭代生成器，太乱了，一般没人传这么大的文件    吧？
"""


