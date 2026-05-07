"""
总结服务
    让 ai 对rag检索的内容进行总结
"""
from Unit_01.rag.vector_store import VectorStoreService
from Unit_01.utils.prompt_loader import load_rag_prompt
from Unit_01.model.factory import chat_model, chat_model_low_price
from langchain_core.prompts import PromptTemplate
import json


def print_prompt(prompt):
    """
    需要调试rag提示词时去掉注释即可
    :param prompt:
    :return:
    """
    # print("="*40, "这里在调试提示词", "="*40)
    # print(prompt.to_string())
    # print("+" * 40, "调试提示词结束", "+" * 40)
    return prompt


class RagSummarizeService(object):
    """
    进行向量检索结果总结
    """
    def __init__(self):
        # 获取向量检索器
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        # 获取提示词模板
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model_low_price
        self.chain = self._init_chain()

    def _init_chain(self):
        """
        生成一个链
        :return:
        """
        chain = self.prompt_template | print_prompt | self.model
        return chain

    def retriever_docs(self, query: str):
        """
        获取检索信息列表
        :param query:
        :return:
        """
        docs = self.retriever.invoke(query)
        return docs

    def get_context(self, query: str):
        """
        组装检索信息
        :param query:
        :return:
        """
        res = self.retriever_docs(query)

        context = "["
        cnt = 0
        for i in res:
            cnt += 1
            context += f"\n第{cnt}条参考资料：文本信息：{i.page_content} | 参考元数据{i.metadata}"
        context += "]"
        return context

    def rag_summarize(self, query):
        """
        获取rag总结结果
        :param query:
        :return:
        """
        context = self.get_context(query)
        res = self.chain.invoke(
            {
                "input": query,
                "context": context
            }
        )
        content = {
            "content": res.content[0]["text"],
            "token": {
                "input_tokens": res.usage_metadata["input_tokens"],
                "output_tokens": res.usage_metadata["output_tokens"],
                "total_tokens": res.usage_metadata["total_tokens"]
            }
        }
        return json.dumps(content, ensure_ascii=False)


if __name__ == "__main__":
    rag_summarize = RagSummarizeService().rag_summarize("哪些机器人适合打扫卫生")
    print(rag_summarize)
    print()
    pass

"""
改进点:
    1. 增强rag的检索，克服向量检索的缺点（如让ai生成关键词句进行检索，以得到更完整的资料）
"""
