import sys
from pathlib import Path
# 获取项目根目录（Unit_01 的父目录）
project_root = Path(__file__).parent.parent.parent  # app.py -> ui_page -> Unit_01 -> Agent_Unit_01
sys.path.insert(0, str(project_root))
import streamlit as st
from Unit_01.agent.react_agent import ReactAgent
import asyncio


async def astream(agent, query: str,
                  reasoning_content,
                  text_content,
                  thinking_placeholder,
                  text_placeholder):
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

    st.session_state["messages"].append(
        {"role": "assistant", "content": text_content, "reasoning_content": reasoning_content})




# 标题
st.title("『奇迹与你』agent试做版")
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
        thinking_placeholder=thinking_placeholder
    ))


    # for typing, chunk in response:
    #     # """这里双层循环而不能直接索引是因为流式输出需要等待服务器将结果放进列表之中"""
    #     # 通过不断更新Markdown的方法做到流式输出的效果
    #     if typing == "reasoning":
    #         reasoning_content += chunk
    #         thinking_placeholder.markdown(reasoning_content)
    #
    #     elif typing == "text":
    #         text_content += chunk
    #         text_placeholder.markdown(text_content)
    #
    # st.session_state["messages"].append(
    #     {"role": "assistant", "content": text_content, "reasoning_content": reasoning_content})


