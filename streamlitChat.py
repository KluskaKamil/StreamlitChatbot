import streamlit as st
from openai import OpenAI


st.title('Chat Bot')
user = 'user'
model = 'gpt-4'
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    
if 'messages' not in st.session_state:
    st.session_state.messages = []
            
if 'openai_model' not in st.session_state:
    st.session_state.openai_model = model
        
for message in st.session_state.messages:
    with st.chat_message(message.get('role', 'Unknown user')):
        st.markdown(message.get('content', 'No content to display'))


prompt= st.chat_input("What's up?")       
if prompt:
    with st.chat_message(user):
        st.markdown(prompt)
    st.session_state.messages.append({"role": user, "content": prompt})
        
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model = st.session_state.get('openai_model', 'Unknown model'),
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})