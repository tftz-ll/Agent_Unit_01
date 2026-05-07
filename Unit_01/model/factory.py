from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_ollama import ChatOllama
from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from Unit_01.utils.config_handler import load_model_data_config
from langchain_ollama.chat_models import ChatOllama
from langchain_ollama.chat_models import ChatOllama, BaseChatModel


class BaseModelFactory(ABC):
    """
    抽象类定义的好处：
        直接锁定了创建模型的固定格式，统一了接口，方便协作扩展
    """
    @abstractmethod
    def generator(self) -> Embeddings | BaseChatOpenAI:
        """
        返回对象取决于模型父类
        """
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Embeddings | BaseChatOpenAI | BaseChatModel:
        return ChatOpenAI(
            model=load_model_data_config["chat_model_name"],
            base_url=load_model_data_config["base_url"],
            output_version=load_model_data_config['output_version']
        )


class EmbeddingModelFactory(BaseModelFactory):
    def generator(self) -> Embeddings | BaseChatOpenAI | BaseChatModel:
        return DashScopeEmbeddings(
            model=load_model_data_config["embedding_model_name"]
        )


class ChatModelFactoryLowPrice(BaseModelFactory):
    def generator(self) -> Embeddings | BaseChatOpenAI | BaseChatModel:
        return ChatOpenAI(
            model=load_model_data_config["chat_model_name_low_price"],
            extra_body={"enable_thinking": False},
            base_url=load_model_data_config["base_url"],
            output_version=load_model_data_config['output_version']
        )


class ChatModelFactoryOllama(BaseModelFactory):
    def generator(self) -> ChatOllama:
        return ChatOllama(
            model=load_model_data_config["chat_model_ollama"],
            reasoning=True,
            num_ctx=32768,  # 32K 安全，实测 6.96GB 峰值显存
            num_predict=2048,
        )


# 当场创建两个模型对象，后续只要导入这两个变量即可获得模型（但是这种方法不太适合需要多次创建的情景）
chat_model = ChatModelFactory().generator()
chat_model_low_price = ChatModelFactoryLowPrice().generator()
embedding_model = EmbeddingModelFactory().generator()
chat_model_ollama = ChatModelFactoryOllama().generator()
"""
改进点：
    开启思考模式
    接入Ollama本地模型（chat+embedding）
    做到能够切换本地模型与云端模型
"""

