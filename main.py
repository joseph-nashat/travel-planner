#python -m venv env
#env\scripts\activate
#pip install langchain langchain-chroma langchain-core langchain-openai langchain-text-splitters langsmith python-dotenv
import streamlit as st
import src.chatbot as cb
from langchain_core.messages import HumanMessage,AIMessage

st.title("🦜🔗 Quickstart App")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        
# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            gpt_messages = []
            for message in st.session_state.messages[-10:]:
                if message['role'] == 'assistant':
                    gpt_messages.append(AIMessage(content=message['content']))
                else:
                    gpt_messages.append(HumanMessage(content=message['content']))
            print (gpt_messages)    
            # response = cb.callChatBotV2(f"{st.session_state.messages[-10:]}" ) 
            response = cb.callChatBotV3(gpt_messages )             
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)        