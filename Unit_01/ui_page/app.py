import sys
from pathlib import Path
# 获取项目根目录（Unit_01 的父目录）
project_root = Path(__file__).parent.parent.parent  # app.py -> ui_page -> Unit_01 -> Agent_Unit_01
sys.path.insert(0, str(project_root))
import streamlit as st
import copy
from Unit_01.agent.react_agent import ReactAgent
from Unit_01.concern_hub.hub import token_cnt, clear_token_cnt
import asyncio


async def astream(agent, query: str,
                  reasoning_content,
                  text_content,
                  thinking_placeholder,
                  text_placeholder,
                  token_expression):
    # """
    # 这个方法是为了兼容异步实现的输出
    # """
    async for typing, chunk in agent.execute_astream(query):
        if typing == "reasoning":
            reasoning_content += chunk
            thinking_placeholder.markdown(reasoning_content)

        elif typing == "text":
            text_content += chunk
            text_placeholder.markdown(text_content)

    # 输出流程执行结束，将历史信息保存到st.session_state中，显示到页面上
    a = token_cnt['current_token_cnt']['input_tokens']
    b = token_cnt['current_token_cnt']['output_tokens']
    c = token_cnt['current_token_cnt']['total_tokens']
    token_expression.caption(
        f"输入token：{a} 输出tokens：{b} 总tokens：{c}"
    )

    st.session_state["messages"].append(
        {"role": "assistant",
         "content": text_content,
         "reasoning_content": reasoning_content,
         "tokens": {
             "input_tokens": copy.deepcopy(a),
             "output_tokens": copy.deepcopy(b),
             "total_tokens": copy.deepcopy(c),
         }
         })
    clear_token_cnt()


# 标题
st.title("『奇迹与你』agent试做版")

st.caption(
            f"当前总token消耗详情--"
            f"输入token：{token_cnt['total_token_cnt']['input_tokens']} "
            f"输出tokens：{token_cnt['total_token_cnt']['output_tokens']} "
            f"总tokens：{token_cnt['total_token_cnt']['total_tokens']}"
            )
st.divider()

if 'agent' not in st.session_state:
    st.session_state['agent'] = ReactAgent()

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

for messages in st.session_state["messages"]:
    # messages中三种情况
    # 角色为user 直接输出
    # 角色为AI 思考内容 输出
    # 角色为AI 文本内容 输出
    if messages["role"] == "user":
        st.chat_message(messages["role"]).write(messages["content"])

    if messages["role"] == "assistant":
        with st.chat_message("assistant"):
            with st.expander("Thinking..."):
                st.write(messages["reasoning_content"])
            st.write(messages["content"])
            st.caption(
                f"输入token：{messages['tokens']['input_tokens']} "
                f"输出tokens：{messages['tokens']['output_tokens']} "
                f"总tokens：{messages['tokens']['total_tokens']}"
            )

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    # 用户对话栏输出
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # ai窗口对话栏
    with st.chat_message("assistant"):
        # ai聊天窗口下的两个占位符 思考 和 文本
        with st.expander("Thinking..."):
            thinking_placeholder = st.empty()
        text_placeholder = st.empty()

        token_expression = st.empty()
    # 两个变量，分别存放思考信息和文本输出信息
    reasoning_content = ""
    text_content = ""

    # 获取模型响应文本迭代器
    asyncio.run(astream(
        agent=st.session_state['agent'],
        query=prompt,
        reasoning_content=reasoning_content,
        text_content=text_content,
        text_placeholder=text_placeholder,
        thinking_placeholder=thinking_placeholder,
        token_expression=token_expression
    ))
    st.rerun()



