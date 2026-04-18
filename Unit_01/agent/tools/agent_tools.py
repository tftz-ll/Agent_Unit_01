"""
当前文件中大量工具基本都是假的
"""
import os.path

from langchain_core.tools import tool
from Unit_01.rag.rag_service import RagSummarizeService
from Unit_01.utils.config_handler import agent_conf
from Unit_01.utils.path_tool import get_abs_path
from Unit_01.utils.logger_handler import logger
import random


user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
external_data = {}
month_arr = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]


@tool(description="当你想要查询一些知识库中的知识时，这个工具会很有用")
def rag_summarize(query: str) -> str:
    rag = RagSummarizeService()
    return rag.rag_summarize(query)


@tool(description="当你想要查询天气时，这个工具会很有用")
def get_weather(city: str) -> str:
    return f"城市{city}为晴天， 气温26摄制度， 降雨几率百分之60， 南方3级"


@tool(description="当年你想要知道用户所在城市时，这个工具也许能帮助你")
def get_user_location() -> str:
    return random.choice(["深圳", "火星第六基地", "月亮第三号空间观察站"])


@tool(description="当你想知道用户id时，这个工具也许能帮到你")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份")
def get_current_month() -> str:
    return random.choice(month_arr)


def generate_external_data():
    """
    Schema template
    {
        "user_id": {
            "month": {
                "特征": xxx,
                "效率": xxx
            }
            "month": {
                "特征": xxx,
                "效率": xxx
            }
        }
    }
    :return:
    """
    if not external_data :
        external_data_path = get_abs_path(agent_conf["external_data_path"])
        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部路径{external_data_path}不存在")
        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr = line.strip().split(",")
                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison
                }


@tool(description="当你想得知用户使用记录时，这个工具会很有用，获取不到时返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data 信息查询工具警告] 未能检索到用户：{user_id} 在 {month} 的使用记录数据")
        return ""


@tool(description="调用此工具将会切换为报告生模式")
def fill_context_for_report():
    """
    本质上是利用 tool_monitor 能够获取工具调用情况的特性来进行提示词模板切换
    :return:
    """
    return "fill_context_for_report"


# if __name__ == "__main__":
#     print(fetch_external_data("1002", "2025-01"))
#     print(external_data)
"""
改进点：
    1. 太明显了吧...
       目前这个agent的类型是一定要大改的，并且尝试接入一下web搜索，导航查询，代码编写等功能
    2. 用户记录现场读取这个资源消耗离大谱，如果真要实现相似功能的话，尝试数据库高效检索又或者cache携带（感觉这个还挺不靠谱的）
"""

