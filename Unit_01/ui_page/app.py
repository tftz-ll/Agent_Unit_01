import sys
from pathlib import Path

# 获取项目根目录（Unit_01 的父目录）
project_root = Path(__file__).parent.parent.parent  # app.py -> ui_page -> Unit_01 -> Agent_Unit_01
sys.path.insert(0, str(project_root))

import streamlit as st
from Unit_01.agent.react_agent import ReactAgent

# 标题
st.title("『奇迹与你』agent试做版")
st.divider()

if 'agent' not in st.session_state:
    st.session_state['agent'] = ReactAgent()

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state["messages"]:
    st.chat_message(message['role']).write(message['content'])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", 'content': prompt})

    with st.spinner("Thinking..."):
        res = st.session_state['agent'].execute_stream(prompt)

        response = st.chat_message("assistant").write_stream(res)
        print(response)
        st.session_state['messages'].append({'role': 'assistant', 'content': response})



# """
# 改进点：
#     尝试一下write_stream直接输出是什么效果
# """






