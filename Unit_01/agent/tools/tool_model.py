from Unit_01.model.factory import chat_model_low_price
from Unit_01.utils.prompt_loader import load_web_search_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


class WebSearchSummarizeService(object):
    """
    创建一个类实例，获取用于网页搜索信息文本总结的类实例
    """
    def __init__(self):
        self.prompt = load_web_search_prompt()
        self.model = chat_model_low_price

    def get_chain(self):
        prompt = ChatPromptTemplate.from_template(self.prompt)
        chain = prompt | self.model
        return chain

    def summarize_service(self, text):
        return self.get_chain().invoke({"input": text})


web_search_summarize_model = WebSearchSummarizeService()

if __name__ == "__main__":
    model = WebSearchSummarizeService()
    res = model.summarize_service("""
    {'url': 'https://eu.36kr.com/zh/p/3780290045121801', 'title': 'DeepSeek V4终于发布，打破最强闭源垄断，明确携手华为芯片 - 36氪', 'raw_content': '# DeepSeek V4终于发布，打破最强闭源垄断，明确携手华为芯片\n\n刚刚，DeepSeek-V4来了！\n\n预览版正式上线并同步开源。\n\n一共两个版本：\n\nDeepSeek-V4-Pro：对标顶级闭源模型，1.6T，49B激活，上下文长度1M；\n\nDeepSeek-V4-Flash：更小更快的经济版，284B，13B激活，上下文长度1M。\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_a5d05e618061481884b69344f77c56f2@5888275_oswg73361oswg1080oswg254_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_a5d05e618061481884b69344f77c56f2@5888275_oswg73361oswg1080oswg254_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n官方原话是：**在Agent能力、世界知识和推理性能上均实现国内与开源领域的领先**。\n\n并且：\n\n目前DeepSeek-V4已经成为公司内部员工使用的Agentic Coding模型，据评测反馈使用体验优于Sonnet 4.5，交付质量接近Opus 4.6非思考模式。但仍与Opus 4.6思考模型存在一定差距。\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_d640bb9fffd74ac0a97c9f0a002447d5@5888275_oswg283707oswg1080oswg824_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_d640bb9fffd74ac0a97c9f0a002447d5@5888275_oswg283707oswg1080oswg824_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n目前官网和APP都上了，API服务也已同步更新。\n\n大家都关心的国产算力方面，划重点，**下半年支持华为算力**。\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_7345f5770a174500993e91b9e19be74c@5888275_oswg57844oswg1080oswg195_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_7345f5770a174500993e91b9e19be74c@5888275_oswg57844oswg1080oswg195_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n## **顶配和性价比之选，两个版本一起开**\n\n这次V4一口气发了两个版本。\n\n**V4-Pro**，性能比肩顶级闭源模型。\n\n官方给出的判断有三条：\n\nAgent能力大幅提高：在Agentic 能力Coding评测中，V4-Pro已达到当前开源模型最佳水平，并在其他Agent相关评测中同样表现优异。内部测评中，Agent Coding模式下，V4体验优于Sonnet 4.5，交付质量接近 Opus 4.6非思考模式，但仍与 Opus 4.6思考模式存在一定差距。\n\n丰富的世界知识：DeepSeek-V4-Pro在世界知识测评中，大幅领先其他开源模型，仅稍逊于顶尖闭源模型Gemini-Pro-3.1。\n\n世界顶级推理性能：在数学、STEM、竞赛型代码的测评中，DeepSeek-V4-Pro超越当前所有已公开评测的开源模型，取得了比肩世界顶级闭源模型的优异成绩。\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_c335d5b2ac95437b9f593902dd20900c@5888275_oswg425796oswg1080oswg798_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_c335d5b2ac95437b9f593902dd20900c@5888275_oswg425796oswg1080oswg798_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n**V4-Flash**，更小更快的经济版。推理能力接近Pro，世界知识储备稍逊一筹，但参数和激活更小，API更便宜。\n\n在Agent任务方面，DeepSeek-V4-Flash在简单任务上与DeepSeek-V4-Pro旗鼓相当，但在高难度任务上仍有差距。\n\n在洗车测试上，V4也是快速通过。\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_26e07282e5f44fe1b1295d6dfdb4491a@5888275_oswg562596oswg1080oswg1297_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_26e07282e5f44fe1b1295d6dfdb4491a@5888275_oswg562596oswg1080oswg1297_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n而在“绝望的父亲”这个经典的生物学场景当中，DeepSeek-V4并没有一轮get到红绿色盲这个关键点（根据遗传学规律，如果一名女性是红绿色盲，其生物学父亲必然也是）。\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_7d2017bc35b04507811c401513d7d726@5888275_oswg262929oswg1080oswg677_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_7d2017bc35b04507811c401513d7d726@5888275_oswg262929oswg1080oswg677_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n## **百万上下文实现标配**\n\n值得一提的是，**从今天开始，1M上下文是DeepSeek所有官方服务的标配。**\n\n一年前，1M上下文还是Gemini独家的王牌；其他所有闭源模型要么128K要么200K；开源这边几乎没人玩得起这个量级。\n\nDeepSeek直接把百万上下文从一个「高端功能」挪成了「水电煤」。\n\n而且开源。他们怎么做到的，发布稿里直接给了答案——\n\nV4开创了一种全新的注意力机制，在token维度进行压缩，结合DSA稀疏注意力一起用。相比传统方法，对计算和显存的需求大幅降低。\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_cceaea9f0e034869bca9252dea82daa5@5888275_oswg162525oswg1080oswg477_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_cceaea9f0e034869bca9252dea82daa5@5888275_oswg162525oswg1080oswg477_img_000?x-oss-process=image/format,jpg/interlace,1)\n\nDSA不是新词。半年前V3.2-Exp那次更新首次引入，当时外界关注度不高，因为跑分和V3.1-Terminus几乎一样，看起来像一次没什么料的中间版本。\n\n现在回头看，那是V4的地基。\n\n## **Agent能力专项优化**\n\nAgent这边，V4针对Claude Code、OpenClaw、OpenCode、CodeBuddy等主流Agent产品做了适配和优化，代码任务、文档生成任务都有提升。\n\n发布稿里还附了一张V4-Pro在某Agent框架下生成的PPT内页示例。\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_326e45e0f2404162921c938f032f72a5@5888275_oswg137144oswg1080oswg508_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_326e45e0f2404162921c938f032f72a5@5888275_oswg137144oswg1080oswg508_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n## **API价格**\n\nAPI这边，V4-Pro和V4-Flash同步上线,支持OpenAI ChatCompletions接口和Anthropic接口两套。\n\nbase\\_url 不变,model 参数改成 deepseek-v4-pro 或 deepseek-v4-flash 即可调用。\n\n两个版本最大上下文都是1M,都同时支持非思考模式和思考模式。思考模式下可以通过reasoning\\_effort 参数调强度,两档high和max。官方建议复杂 Agent 场景直接上max。\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_7117fb9e14d14ec5aa8cdfe4900d1197@5888275_oswg80811oswg1080oswg310_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n![](https://img.36krcdn.com/hsossms/20260424/v2_7117fb9e14d14ec5aa8cdfe4900d1197@5888275_oswg80811oswg1080oswg310_img_000?x-oss-process=image/format,jpg/interlace,1)\n\n这里有个重点——**下半年支持华为算力**。\n\n此外，旧模型名要下架。\n\ndeepseek-chat和deepseek-reasoner将在三个月后(2026年7月24日)停用，当前阶段内这两个名字分别指向V4-Flash的非思考和思考模式。\n\n对个人开发者影响不大，改一个model参数。对接了生产环境的公司，这三个月要去做迁移。\n\n## **One more thing**\n\n发布稿的结尾，DeepSeek 自己引了一句话。\n\n「不诱于誉，不恐于诽，率道而行，端然正己。」\n\n这是荀子《非十二子》里的一句。字面意思是，不被赞誉诱惑，不被诽谤吓到，按自己认定的道往前走，端正自己。\n\n放在今天这个场景里，有点意思。\n\n过去半年，关于V4什么时候发、是不是跳票、是不是已经被别家超越、是不是已经被 Claude 蒸馏数据搞定了之类的传言在中文和英文AI圈来来回 回跑了好几轮。年初甚至还有人信誓旦旦说V4会在春节前发，结果等到了四月底。\n\n他们没回应过一次。\n\n然后在某个周五的下午，把V4放出来，同步开源，同步上线官网和App，同步更新API，顺便把内部员工已经弃用Claude的事实写进发布稿。\n\n没有路线图，没有直播，没有访谈。\n\n率道而行这四个字，听着像是一句口号。但如果你把过去半年 V3.2 那次「没什么亮点」的 Exp 版本、DSA那套为V4铺了半年的稀疏注意力、1M 上下文从王牌变成标配的这条路径放在一起看。\n\nDeepSeek已经做到了。\n\nDeepSeek-V4模型开源链接：\n\n[1]https://huggingface.co/collections/deepseek-ai/deepseek-v4\n\n[2]https://modelscope.cn/collections/deepseek-ai/DeepSeek-V4\n\nDeepSeek-V4 技术报告：https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek\\_V4.pdf\n\n本文来自微信公众号[“量子位”](https://mp.weixin.qq.com/s/avXt0DgRa_Aye7bIOtdgxQ)，作者：量子位，36氪经授权发布。\n\n该文观点仅代表作者本人，36氪平台仅提供信息存储空间服务。\n\n36氪欧洲总站（eu.36kr.com）是关注海外的行业媒体，为企业跨境提供海外资讯及商业服务。\n\n© 2024 36kr.com. All rights reserved.', 'images': []}
], 'failed_results': [], 'response_time': 0.01, 'request_id': '385ac3ac-4382-4c34-b6e4-fcdc49d9e6f1', 'query': 'DeepSeek-V4的基本信息和特点'}, {'results': [
    """)
    content = res.content[0]
    usage_metadata = res.usage_metadata
    print(content["text"])
    print(type(usage_metadata['input_tokens']))
    print(usage_metadata["input_tokens"])
    print(usage_metadata["output_tokens"])
    print(usage_metadata["total_tokens"])
    print(usage_metadata)
    """
    usage_metadata={'input_tokens': 3658, 'output_tokens': 153, 'total_tokens': 3811, 
    content=[{'type': 'text', 'text': 'DeepSeek-V4 发布预览版并开源，含两版本：V4-Pro（1.6T 参数，49B 激活）对标顶级闭源模型，V4-Flash（284B 参数，13B 激活）为经济版。两者上下文长度均达 1M，采用全新注意力机制降低算力需求。V4-Pro 在 Agent 编码、世界知识及推理性能上领先开源界，体验优于 Sonnet 4.5，接近 Opus 4.6 非思考模式。官方宣布下半年支持华为算力，旧模型将于 2026 年 7 月 24 日停用，API 同步更新支持双接口。', 'annotations': [], 'id': 'msg_dae45f02-9bb9-4486-ac3c-3635f99d111e'}] additional_kwargs={} response_metadata={'id': 'resp_f3a9e610-eddc-965b-89bf-f57de64b3888', 'created_at': 1777359945.0, 'model': 'qwen3.5-plus-2026-02-15', 'object': 'response', 'status': 'completed', 'model_provider': 'openai', 'model_name': 'qwen3.5-plus-2026-02-15'} id='resp_f3a9e610-eddc-965b-89bf-f57de64b3888' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 3658, 'output_tokens': 153, 'total_tokens': 3811, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}

    """
    # for chunk in res:
    #     # """这里双层循环而不能直接索引是因为流式输出需要等待服务器将结果放进列表之中"""
    #     for content in chunk.content:
    #         res_type = content["type"]
    #
    #         if res_type == "reasoning":
    #             for i in content["summary"]:
    #                 print(i["text"], end="", flush=True)
    #
    #         if res_type == "text":
    #             print(content["text"], end='', flush=True)


