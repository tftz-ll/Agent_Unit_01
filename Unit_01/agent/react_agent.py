"""
这里是agent主体部分
"""
import asyncio

from langchain.agents import create_agent
from Unit_01.model.factory import chat_model, chat_model_ollama
from Unit_01.utils.config_handler import load_model_data_config
from Unit_01.utils.prompt_loader import load_system_prompt
from Unit_01.agent.tools.agent_tools import (rag_summarize, get_weather, get_current_month, ground_web_search,
                                             web_search_for_report, async_extract_webpage, async_map_webpage,
                                             crawl_web_page)
from Unit_01.agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
from Unit_01.concern_hub.hub import a_token_for_count
from langsmith import traceable, get_current_run_tree


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize, get_weather, get_current_month, ground_web_search, web_search_for_report,
                   async_extract_webpage, async_map_webpage, crawl_web_page],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )
        # 创建一个字段，用于langsmith进行token计算，
        # self.token_usage_metadata =

    def execute_stream(self, query: str):
        """
        将得到的字符串以 迭代器 形式返回回去
        注意：为了判别返回内容为思考标签还是文本标签 改迭代器会返回两个值
        类型[typing] 和文本[content]
        :param query:
        :return: typing content
        """
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }
        # 这里的report设置了一个键值对，作为提示词切换的标记
        res = self.agent.stream(input_dict, stream_mode=["messages"], context={'report': False})
        for message in res:
            for j in message[-1]:
                if hasattr(j, "content"):  # 避开TollMessage类型a nd type(j).__name__ != "ToolMessage"
                    for chunk in getattr(j, "content"):
                        if type(chunk) is str:
                            continue
                            # 区分信息类型（推理还是文本输出）
                        if chunk["type"] == "reasoning":
                            for summary in chunk["summary"]:
                                # pass
                                yield "reasoning", summary["text"]
                                # 当前还没有思考窗口，先不输出思考内容
                        if chunk["type"] == "text":
                            yield "text", chunk["text"]

    # @traceable(
    #     run_type="chain",
    #     metadata={"ls_provider": "openai", "ls_model_name": load_model_data_config["chat_model_name"]}
    # ) 假如哪天我有了历史回溯查看agent运行情况的需求时再使用langsmith代理吧
    async def execute_astream(self, query: str):
        """
        效果和上面的函数一样，但这个方法是异步的
        类型[typing] 和文本[content]
        :param query:
        :return: typing content
        """


        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }
        # 这里的report设置了一个键值对，作为提示词切换的标记
        res = self.agent.astream(input_dict, stream_mode=["messages"], context={'report': False})
        async for message in res:
            for j in message:
                if isinstance(j, str):
                    continue

                content = j[0]
                metadata = j[-1]

                # 进行token字段提取, 被诈骗了，smith这小东西要花钱，我宁愿本地计算
                if hasattr(content, "usage_metadata"):
                    token_usage = getattr(content, "usage_metadata")
                    if token_usage is not None:
                        # print("\n当前token消耗: ", token_usage)
                        await a_token_for_count(token_usage)
                        # yield "token_usage", token_usage

                # if metadata["langgraph_node"] != "model":
                #     continue
                if hasattr(content, "content"):
                    for chunk in getattr(content, "content"):
                        if type(chunk) is str:
                            continue
                            # 区分信息类型（推理还是文本输出）
                        if chunk["type"] == "reasoning":
                            for summary in chunk["summary"]:
                                # print(summary["text"], end='', flush=True)
                                yield "reasoning", summary["text"]
                                # 当前还没有思考窗口，先不输出思考内容
                        if chunk["type"] == "text":
                            # print(chunk["text"], end='', flush=True)
                            yield "text", chunk["text"]


class ReactAgentOllama:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model_ollama,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize, get_weather, get_current_month, ground_web_search, web_search_for_report,
                   async_extract_webpage, async_map_webpage, crawl_web_page],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

    async def execute_astream(self, query: str):
        """
        效果和上面的函数一样，但这个方法是异步的
        类型[typing] 和文本[content]
        :param query:
        :return: typing content
        """
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }

        res = self.agent.astream(input_dict, stream_mode=["messages"], context={'report': False})

        async for messages in res:
            for j in messages:
                if isinstance(j, str):
                    continue

                content = j[0]
                metadata = j[-1]
                if type(content).__name__ == "ToolMessage":
                    continue
                additional_kwargs = getattr(content, "additional_kwargs")
                context = getattr(content, "content")
                reasoning = additional_kwargs.get("reasoning_content", "")
                if reasoning != "":
                    print(reasoning, end='', flush=True)
                else:
                    print(context, end='', flush=True)


if __name__ == "__main__":
    from Unit_01.concern_hub.hub import token_cnt
    agent = ReactAgent()
    res = asyncio.run(agent.execute_astream(query="请对中日关系最近局势进行一次研究"))
    print("本次token消耗为：", token_cnt)
    # async def astream(agent, query: str):
    #     async for typing, chunk in agent.execute_astream(query):
    #         # print(typing)
    #         # print(chunk, end='', flush=True)
    #         if typing == "reasoning":
    #             # print("   ", end='', flush=True)
    #             print(chunk, end='', flush=True)
    #         elif typing == "text":
    #             # print(" :", end='', flush=True)
    #             print(chunk, end='', flush=True)
    #
    # asyncio.run(astream(agent, "你的知识库中有什么内容"))
"""
改进点：
    1. 这里流式输出其实是假流式，真正的流式参数应该是messages（具体改进方案看另一个项目中的实验）
    2. 加入显示输出思考链
    3. 补全长记忆模式
"""