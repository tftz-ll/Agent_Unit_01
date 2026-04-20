import json
import os
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
# import config_data
from Unit_01.utils.logger_handler import logger
from Unit_01.utils.path_tool import get_abs_path
from Unit_01.utils.config_handler import memory_conf


class FileChatMessageHistory(BaseChatMessageHistory):
    """
        langchain对记忆模块进行了高度封装，
        整个类的实现都是为了一个名为 get_session_history(session_id, user_id/亦或者是存储路径)这个函数服务的
        这个函数会把BaseChatMessageHistory返回回去，
        通过调用子类【这里是ChatHistoryMemory】的方法实现对消息的存储
        因此实际上这个类的作用就是 （以下摘抄自官方文档）
        【
        messages (属性): 当你将该对象传递给 RunnableWithMessageHistory 或类似组件时，框架会在每次交互开始时访问此属性以获取上下文。
        add_messages (方法): 仅在处理完一次模型调用并将新的 HumanMessage/AIMessage 写入历史时，才会由框架触发。
        clear (方法): 此方法永远不会自动执行。它必须由你的业务代码显式调用（例如，当用户点击“清除对话”按钮或开始一个新会话时）。
        】
        便于个人理解的
        messages 从存储中获取对话消息
        add_messages 接受当前窗口的所有对话，存储到储存中
        clear 清空当前对话信息 （这个方法langchain不会主动调用）
    """
    storage_path: str
    session_id: str

    def __init__(self, session_id, storage_path):
        """
        根据传入的值创建一个存放json格式历史消息的文件
        """
        self.storage_path = storage_path
        self.session_id = session_id

        self.file_path = os.path.join(self.storage_path, self.session_id)

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    @property
    def messages(self) -> list[BaseMessage]:
        """
        框架会访问这个属性以直接获取上下文的所有信息
        因此这个方法要实现的是将所有信息返回回去
        """
        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """
        这个函数会接受一个信息列表，列表中装的是每一次对话传来的新消息（而不是全部）
        我们需要使用这个函数去将传来的新消息添加记忆存储文件中
        文件读写：
            由于我们无法做到将信息一条条的加到整个json文件的末尾【with open的方式无法做到】
            因此我们先将整个历史对话获取到 【通过 list(self.messages) 访问属性并转为列表的方法】
            然后将新消息 添加到列表末尾
            再对整个记忆文件进行覆写的形式完成记忆存储
        """
        all_messages = list(self.messages)  # 从文件中获取历史消息
        all_messages.extend(messages)  # 将新消息 添加到列表末尾

        series_messages = [message_to_dict(message) for message in all_messages]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(series_messages, f)  # 再对整个记忆文件进行覆写的形式完成记忆存储

    def clear(self) -> None:
        """"
        清空当前对话消息，langchain框架不会主动调用
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)


def get_session_id(session_id):
    logger.info("[get_session_id 记忆模块] 运行")
    return FileChatMessageHistory(session_id, get_abs_path(memory_conf["file_store_path"]))