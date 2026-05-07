"""
目标：
    文件配置 =》 读取 => 获得文件内容 进行分离
    通过yaml创建四个读取配置文件的函数
    分别管理(chroma、rag、prompt、agent)
"""
import yaml
from Unit_01.utils.path_tool import get_abs_path

def load_chroma_config(config_path: str = get_abs_path("config/chroma.yaml"), encoding: str = "utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        # 相较于.safe_load()虽然有一定的安全隐患，但用于项目内部配置文件的加载是合适的
        return yaml.full_load(f)


def load_model_data_config(config_path: str = get_abs_path("config/model_data.yaml"), encoding: str = "utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        # 相较于.safe_load()虽然有一定的安全隐患，但用于项目内部配置文件的加载是合适的
        return yaml.full_load(f)


def load_prompt_config(config_path: str = get_abs_path("config/prompt.yaml"), encoding: str = "utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        # 相较于.safe_load()虽然有一定的安全隐患，但用于项目内部配置文件的加载是合适的
        return yaml.full_load(f)


def load_agent_config(config_path: str = get_abs_path("config/agent.yaml"), encoding: str = "utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        # 相较于.safe_load()虽然有一定的安全隐患，但用于项目内部配置文件的加载是合适的
        return yaml.full_load(f)


# 这里直接创建四个对应的变量储存拿到的文件，避免了主文件中重复创建的资源浪费
load_model_data_config = load_model_data_config()
prompt_conf = load_prompt_config()
chroma_conf = load_chroma_config()
agent_conf = load_agent_config()

if __name__ == "__main__":
    # 测试文件是否成功拿到数据
    print(load_model_data_config)

"""
可改进点:
    暂无，目前似乎已经很完善了
"""






