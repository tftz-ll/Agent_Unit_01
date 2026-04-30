from langchain.agents.middleware import wrap_tool_call, AgentState, dynamic_prompt, ModelRequest, before_model
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langgraph.runtime import Runtime
from typing import Callable
from Unit_01.utils.logger_handler import logger
from Unit_01.utils.prompt_loader import load_system_prompt, load_report_prompt
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
        raise e
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



"""
改进点：
    1. 以后或许可以通过修饰器监控的方法将获取token消耗
    2. 通过监控用户剩余token量对模型进行切换（降智操作）
    3. 检测到非法信息后强行终止对话（对不起，用户，请换一个话题再聊吧~）
    4. 【以身问路，尸体前行】
"""