"""
这个文件用于统一整个项目的绝对路径
"""
import os


def get_project_root():
    """
    获取工程所在的根目录
    """
    # 获取当前文件绝对路径
    current_file = os.path.abspath(__file__)
    # 所在文件夹绝对路径
    current_dir = os.path.dirname(current_file)
    # 当前项目根目录(Unit_01)
    project_rot = os.path.dirname(current_dir)

    return project_rot


def get_abs_path(relative_path: str):
    """
    传入一个相对路径，获取绝对路径
    :param relative_path:
    :return:
    """
    return os.path.join(get_project_root(), relative_path)


if __name__ == "__main__":
    print(get_abs_path("config_data"))


"""
可改进点：
    get_project_root 不觉得这样一层层跳级有点草率吗...
"""

