from langchain.agents.middleware import wrap_tool_call, AgentState, dynamic_prompt, ModelRequest, before_model
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langgraph.runtime import Runtime
from langchain_core.callbacks import BaseCallbackHandler
from typing import Callable
from Unit_01.utils.logger_handler import logger
from Unit_01.utils.prompt_loader import load_system_prompt, load_report_prompt
from langsmith import traceable
import asyncio

# requests 对请求函数的封装
# handler 对模型的调用

@wrap_tool_call
async def monitor_tool(
        requests: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command]
) -> ToolMessage | Command:
    """
    监控工具调用
    :return:
    """
    logger.info(f"[monitor_tool] 完成执行工具：{requests.tool_call['name']}")
    logger.info(f"[monitor_tool] 完成传入参数：{requests.tool_call['args']}")
    try:
        result = await handler(requests)  # 这个其实就是在调用工具
        logger.info(f"[monitor_tool] 工具{requests.tool_call['name']}调用成功")

        # # 骚操作来了，这里将会对工具调用进行监控，如果监控到返回值fill_context_for_report说明要切换报告模式了
        # if requests.tool_call['name'] == "fill_context_for_report":
        #     requests.runtime.context['report'] = True
    except Exception as e:
        logger.error(f"[monitor_tool] 工具{requests.tool_call['name']}调用失败 因为{str(e)}")
        # raise e
    return result




@dynamic_prompt  # 这个装饰器能够使每次agent生成提示词之前调用此函数
def report_prompt_switch(requests: ModelRequest):
    """
    通过之前注入的字典‘report’动态提供提示词
    将提示词返回给agent
    :return:
    """
    # is_report = requests.runtime.context.get('report', False)
    # if is_report:
    #     return load_report_prompt()
    # else:
    return load_system_prompt()


# AgentState 智能体的状态记录
# Runtime 记录了执行过程中的上下文信息


@before_model
def log_before_model(
        state: AgentState,
        runtime: Runtime
):
    """
    在模型执行前输出日志
    :return:
    """
    logger.info(f"[log_before_model] 即将调用模型，带有{len(state['messages'])}条消息")
    # logger.debug(f"[log_before_model] 即将调用模型，当前携带信息为：{state['messages']}")
    logger.debug(f"[log_before_model] {type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")
    return None



# async def my_async_generator(query_params: dict) -> Iterable:
#     async with httpx.AsyncClient() as http_client:
#         response = await http_client.get(
#             "https://api.example.com/data",
#             params=query_params,
#         )
#         for item in response.json():
#             yield item
#
#
# async def async_code():
#     async for item in my_async_generator({"param": "value"}):
#         print(item)




"""
qwen3.5-flash-2026-02-23
(AIMessageChunk(content=[], 
additional_kwargs={}, response_metadata={'created_at': 1778140064.0, 'model': 'qwen3.5-flash-2026-02-23', 'object': 'response', 'status': 'completed', 'model_provider': 'openai', 'model_name': 'qwen3.5-flash-2026-02-23'}, id='lc_run--019e0168-28b7-7d70-bf41-54b1746e8944', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 362, 'output_tokens': 123, 'total_tokens': 485, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 72}}, tool_call_chunks=[], chunk_position='last'), {'langgraph_step': 3, 'langgraph_node': 'model', 'langgraph_triggers': ('branch:to:model',), 'langgraph_path': ('__pregel_pull', 'model'), 'langgraph_checkpoint_ns': 'model:f73a9a0b-dcef-caa5-5b53-0726c59f8d05', 'checkpoint_ns': 'model:f73a9a0b-dcef-caa5-5b53-0726c59f8d05', 'ls_provider': 'openai', 'ls_model_name': 'qwen3.5-flash-2026-02-23', 'ls_model_type': 'chat', 'ls_temperature': None})


qwen3.5-plus
(AIMessageChunk(content=[{'type': 'text', 'text': '时小心路滑', 'index': 1}], additional_kwargs={}, response_metadata={'model_provider': 'openai'}, id='lc_run--019e0094-f846-7340-aeed-ef7fdaa49083', tool_calls=[], invalid_tool_calls=[], tool_call_chunks=[]), {'langgraph_step': 3, 'langgraph_node': 'model', 'langgraph_triggers': ('branch:to:model',), 'langgraph_path': ('__pregel_pull', 'model'), 'langgraph_checkpoint_ns': 'model:4f6472ed-9358-718d-99d2-02e1ff0d2123', 'checkpoint_ns': 'model:4f6472ed-9358-718d-99d2-02e1ff0d2123', 'ls_provider': 'openai', 'ls_model_name': 'qwen3.5-plus', 'ls_model_type': 'chat', 'ls_temperature': None})

改进点：
    1. 以后或许可以通过修饰器监控的方法将获取token消耗
    2. 通过监控用户剩余token量对模型进行切换（降智操作）
    3. 检测到非法信息后强行终止对话（对不起，用户，请换一个话题再聊吧~）
    4. 【以身问路，尸体前行】
"""