import asyncio
from Unit_01.utils.logger_handler import logger
lock = asyncio.Lock()
token_cnt = {
    "total_token_cnt": {
        'input_tokens': 0,
        'output_tokens': 0,
        'total_tokens': 0,
    },
    "current_token_cnt": {
        'input_tokens': 0,
        'output_tokens': 0,
        'total_tokens': 0,
    },
        # 'input_token_details': {'cache_read': 0},
        # 'output_token_details': {'reasoning': 0}
}


def clear_token_cnt():
    token_cnt['current_token_cnt']["input_tokens"] = 0
    token_cnt['current_token_cnt']["output_tokens"] = 0
    token_cnt['current_token_cnt']["total_tokens"] = 0


async def a_token_for_count(token_usage: dict):
    """
    异步token计算代码，传入一个如下结构的字典
    dict = {
        'input_tokens': ...,
        'output_tokens': ...,
        'total_tokens': ...,
    }
    该方法进行解耦计算
    """
    try:
        async with lock:
            token_cnt['total_token_cnt']["input_tokens"] += token_usage["input_tokens"]
            token_cnt['total_token_cnt']["output_tokens"] += token_usage["output_tokens"]
            token_cnt['total_token_cnt']["total_tokens"] += token_usage["total_tokens"]
            token_cnt['current_token_cnt']["input_tokens"] += token_usage["input_tokens"]
            token_cnt['current_token_cnt']["output_tokens"] += token_usage["output_tokens"]
            token_cnt['current_token_cnt']["total_tokens"] += token_usage["total_tokens"]
    except Exception as e:
        logger.error(f"[hub] token计算失败，因为：\n{e}")


def s_token_for_count(token_usage: dict):
    """
    同步token计算代码，传入一个如下结构的字典
    dict = {
        'input_tokens': ...,
        'output_tokens': ...,
        'total_tokens': ...,
    }
    该方法进行解耦计算
    """
    try:
        token_cnt['total_token_cnt']["input_tokens"] += token_usage["input_tokens"]
        token_cnt['total_token_cnt']["output_tokens"] += token_usage["output_tokens"]
        token_cnt['total_token_cnt']["total_tokens"] += token_usage["total_tokens"]
        token_cnt['current_token_cnt']["input_tokens"] += token_usage["input_tokens"]
        token_cnt['current_token_cnt']["output_tokens"] += token_usage["output_tokens"]
        token_cnt['current_token_cnt']["total_tokens"] += token_usage["total_tokens"]
    except Exception as e:
        logger.error(f"[hub] token计算失败，因为：\n{e}")

