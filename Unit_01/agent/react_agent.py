"""
这里是agent主体部分
"""
from langchain.agents import create_agent
from Unit_01.model.factory import chat_model
from Unit_01.utils.prompt_loader import load_system_prompt
from Unit_01.agent.tools.agent_tools import (rag_summarize, get_weather, get_user_location, get_current_month,
                                             get_user_id, fetch_external_data, fill_context_for_report)
from Unit_01.agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize, get_weather, get_user_location, get_current_month,
                   get_user_id, fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

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
                                pass
                                yield "reasoning", summary["text"]
                                # 当前还没有思考窗口，先不输出思考内容
                        if chunk["type"] == "text":
                            yield "text", chunk["text"]

# @wrap_model_call
# def log_calling_model(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]):
#     print(request)
#     print(handler)
#     print("模型调用")
#     return handler(request)
if __name__ == "__main__":
    agent = ReactAgent()
    res = agent.execute_stream(query="请根据我的所在地情况，看看如何保养机器人，并生成一份报告")

    # 一个非常奇怪的现象，迭代器中的值typing，可以进行判断，但是不能输出出去，否则会提前结束程序
    for typing, chunk in res:
        # print(typing)
        # print(chunk, end='', flush=True)
        if typing == "reasoning":
            print("   ", end='', flush=True)
            print(chunk, end='', flush=True)
        elif typing == "text":
            print(" :", end='', flush=True)
            print(chunk, end='', flush=True)
"""
改进点：
    1. 这里流式输出其实是假流式，真正的流式参数应该是messages（具体改进方案看另一个项目中的实验）
    2. 加入显示输出思考链
    3. 补全长记忆模式
"""