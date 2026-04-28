from Unit_01.utils.config_handler import prompt_conf
from Unit_01.utils.path_tool import get_abs_path
from Unit_01.utils.logger_handler import logger


def load_system_prompt():
    try:
        system_prompt_path = get_abs_path(prompt_conf["main_prompt"])
    except Exception as e:
        logger.error(f"[load_system_prompt]错误 在yaml配置中没有找到main_prompt配置项")
        raise e

    try:
        return open(f"{system_prompt_path}", "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompt]解析主提示词错误 文件数据解析出错, {str(e)}")
        raise e


def load_rag_prompt():
    try:
        rag_summarize_prompt_path = get_abs_path(prompt_conf["rag_summarize_prompt_path"])
    except Exception as e:
        logger.error(f"[load_rag_prompt]错误 在yaml配置中没有找到rag_summarize_prompt_path配置项")
        raise e

    try:
        return open(f"{rag_summarize_prompt_path}", "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompt]解析rag总结提示词错误 文件数据解析出错, {str(e)}")
        raise e


def load_report_prompt():
    try:
        report_prompt_path = get_abs_path(prompt_conf["report_prompt_path"])
    except Exception as e:
        logger.error(f"[load_system_prompt]错误 在yaml配置中没有找到report_prompt_path配置项")
        raise e

    try:
        return open(f"{report_prompt_path}", "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompt]解析报告提示词错误 文件数据解析出错, {str(e)}")
        raise e


def load_web_search_prompt():
    try:
        web_search_summarize_prompt = get_abs_path(prompt_conf["web_search_summarize_prompt"])
    except Exception as e:
        logger.error(f"[load_system_prompt]错误 在yaml配置中没有找到web_search_summarize_prompt配置项")
        raise e

    try:
        return open(f"{web_search_summarize_prompt}", "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompt]解析报告提示词错误 文件数据解析出错, {str(e)}")
        raise e


if __name__ == "__main__":
    print(load_system_prompt())
    print(load_rag_prompt())
    print(load_report_prompt())
    print(load_web_search_prompt())








