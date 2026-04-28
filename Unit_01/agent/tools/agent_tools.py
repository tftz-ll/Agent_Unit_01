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
from tavily import TavilyClient, AsyncTavilyClient
import asyncio
import time
from Unit_01.agent.tools.tool_model import web_search_summarize_model



@tool(description="当你想要查询一些知识库中的知识时，这个工具会很有用")
def rag_summarize(query: str) -> str:
    rag = RagSummarizeService()
    return rag.rag_summarize(query)


@tool(description="当你想要查询天气时，这个工具会很有用")
def get_weather(city: str) -> str:
    return f"城市{city}为晴天， 气温26摄制度， 降雨几率百分之60， 南方3级"


@tool(description="调用这个函数，你将能够获得当前日期时间")
def get_current_month() -> str:
    content_time = time.localtime(time.time())
    return f"当前时间为: \n{content_time[0]}年 {content_time[1]}月 {content_time[2]}日 {content_time[3]}时 {content_time[4]}分 {content_time[5]}秒"



@tool(description="""
这个工具为web搜索工具，他会根据你的问题在网页上搜索相关问题
使用方法
你可以传入的参数有四个：
    query 你要搜索的问题，只接收字符串;
    search_mark 搜索精确度，你只能填入数字 0 或 1，默认值为0，你一般不需要修改【当填入数字为0时为基础查询，均衡速度与质量；当填入数字为1时为高精度查询，专注于精确度，此时会返回chunk字段，里面包含的是根据匹配度对原文进行的提取】
    country 对特定国家进行搜索，默认为china，你一般不需要修改 只接受国家名称字符串小写形式，如：afghanistan, albania, algeria，除非用户指明他来自于其他国家，否则请不要更改
    max_results 最大搜索结果返回值，默认值为5，你只能填入1~20范围的数字，返回的信息数量会根据这个参数变化
返回值：
    一个字典，包含多个字段，需要额外说明的是score代表的是文本搜索结果匹配度
    """)
def ground_web_search(query: str, search_mark=0, country='china', max_results=5):
    tavily_client = TavilyClient()
    # 搜索部分
    if search_mark != 0 or search_mark != 1:
        search_depth = ['basic', 'advanced']
        response = tavily_client.search(
            query=query,
            search_depth=search_depth[search_mark],  # 默认0-basic的搜索精度
            timeout=20,
            country=country,
            max_results=max_results
            # include_raw_content=include_raw_content
        )
        # 将搜索到的内容返回
        return response
    else:
        return "请输入正确的搜索精度分数"


async def _web_extract(urls, query, chunks_per_source=3, client=None):
    try:
        response = await client.extract(urls=urls, query=query, chunks_per_source=chunks_per_source, extract_depth='advanced')
        response["query"] = query
    except Exception as e:
        logger.error(f"[_web_extract 异步提取函数错误] 因为：{e} (网页无法打开)")
        raise e
    return response

def log_and_return(x):
    """
    测试用函数
    """
    print(x)
    return x


# """这个函数是一个异步实现的网页搜寻函数"""
async def _web_search_for_report(queries: list[str]):
    try:
        client = AsyncTavilyClient()
        res_url = await asyncio.gather(*[client.search(q) for q in queries],
                                       return_exceptions=True)
        url_pool = []
        for i in res_url:
            if isinstance(i, Exception):
                continue
            query = i["query"]
            for result in i["results"][:3]:
                if result["score"] >= 0.77:
                    content = {'query': query, "url": result["url"]}
                    url_pool.append(content)
        logger.info("[_web_search_for_report] 异步网页搜索函数运行成功")
    except Exception as e:
        logger.error(f"[_web_search_for_report] 异步网页搜索函数search部分运行失败！ 因为{e}")
    try:
        res_extract = await asyncio.gather(*[_web_extract(client=client,
                                                          urls=url["url"],
                                                          query=url["query"]) for url in url_pool],
                                           return_exceptions=True)
        logger.info("[_web_search_for_report] 异步网页搜索函数运行成功")
    except Exception as e:
        logger.error(f"[_web_search_for_report] 异步网页搜索函数_web_extract部分运行失败！ 因为{e}")
    finally:
        await client.close()
    return [str(res) for res in res_extract if not isinstance(res, Exception)]


def web_search_for_report_summary(text: list[str]):
    """
    接收一段网页搜索文本：包含query-url-content
    通过总结模型（关闭思考模式的3.5flash版本）总结
    返回文本数据
    """

    web_search_summarize = web_search_summarize_model.summarize_service(text)
    return web_search_summarize


@tool(description="""这个函数用于获取报告用搜索数据
参数：queries 你需要传入一个列表，里面包含多个你需要调查的问题字符串
返回：一个json格式字符串，根据query， 搜索页面进行分类，使用前请务必进行一次数据整合
当使用web_search_for_report这个工具时，必须将要搜索的问题拆分成多个小问题，并包装成list[str]的形式传入（如：["query1", "query2", "query3"]），
这些小问题将会被这个工具分批次搜索，因此必须保证每一个小问题的语义完整，避免搜索到无关内容
""")
async def web_search_for_report(queries: list[str]) -> str:
    try:
        response = await asyncio.create_task(_web_search_for_report(queries))
        logger.info("[web_search_for_report] 网页搜索报告工具运行成功 ")
    except Exception as e:
        logger.error(f"[web_search_for_report] 网页搜索报告工具运行失败！ 因为{e}")

    cnt = 1
    text = ''
    cnt_for_token = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}

    summarize_contents = await web_search_for_report_summary(response)
    for summarize_content in summarize_contents:
        text += f"第{cnt}段文本["
        content = summarize_content.content[0]["text"]
        usage_metadata = summarize_content.usage_metadata

        cnt_for_token['input_tokens'] += usage_metadata["input_tokens"]
        cnt_for_token['output_tokens'] += usage_metadata["output_tokens"]
        cnt_for_token['total_tokens'] += usage_metadata["total_tokens"]
        text += str(content)
        text += "]\n"
        cnt += 1
    logger.info(f"[web_search_for_report] 本次工具使用Token消耗量为: {cnt_for_token}")
    return f"文本召回结果：\n{text} \n工具使用token消耗：{str(cnt_for_token)}"


if __name__ == "__main__":
    import time
    start = time.perf_counter()
    for _ in range(3):
        res = asyncio.run(web_search_for_report(['2024年生成式AI医疗模型幻觉真实案例', '2024-2025年医疗AI医生采纳度调查报告', '2024年生成式AI医疗应用监管合规挑战案例', '2024年医疗大模型临床试验结果发表研究']))
        print(res)
    times = time.perf_counter() - start
    print(f"三次运行平均耗时{times/3:.4f}s")
    # 217 point -》233 point
    # 记录：非异步请求模型情况下耗时 三次运行平均耗时45.8203s

    # 242 point -》263 point
    # 记录：异步请求模型情况下耗时 三次运行平均耗时16.3693s

"""
改进点：
    1. 太明显了吧...
       目前这个agent的类型是一定要大改的，并且尝试接入一下web搜索，导航查询，代码编写等功能
    2. 用户记录现场读取这个资源消耗离大谱，如果真要实现相似功能的话，尝试数据库高效检索又或者cache携带（感觉这个还挺不靠谱的）
下面放置的是一些随着版本更新迭代而删除的功能（将针对性agent转换为通用性agent）
"""
