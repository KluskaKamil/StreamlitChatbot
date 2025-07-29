import streamlit as st
from openai import OpenAI
from openai import AzureOpenAI
import numpy as np


class ChatBot:
    def __init__(self, bot_title):
        st.title(bot_title)
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        if 'msgs' not in st.session_state:
            st.session_state.msgs = []
            
            
            
    def display_history(self):
        msgs = st.session_state.msgs
        i = 0
        while i < len(msgs):
            if msgs[i].get('col', False):
                col_group = []
                while i < len(msgs) and msgs[i].get('col', False):
                    col_group.append(msgs[i])
                    i += 1
                cols = st.columns(len(col_group))
                for col, msg in zip(cols, col_group):
                    with col:
                        with st.chat_message(msg['role']):
                            st.markdown(msg['content'])
            else:
                with st.chat_message(msgs[i]['role']):
                    st.markdown(msgs[i]['content'])
                i += 1
            
                
    
    
    def gpt_respond(self, model, col=False):
        with st.chat_message("assistant"):
            stream = self.client.chat.completions.create(
                model = model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.msgs
                ],
                stream=True
            )
            response = st.write_stream(stream)
        st.session_state.msgs.append({"role": "assistant", "content": response, 'col':col})
            
        
        
    def custom_model_respond(self, prompt, col=False):
        
        endpoint = st.secrets["BSF_ENDPOINT"]
        api_key = st.secrets["BSF_AZURE_API_KEY"]
        
        client = AzureOpenAI(
            api_version="2024-12-01-preview",
            azure_endpoint=endpoint,
            api_key=api_key,
        )
        
        
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_tokens=100,
            temperature=1.0,
            top_p=1.0,
            model='gpt-4o'
        )
            response = response.choices[0].message.content
            st.markdown(response)
        st.session_state.msgs.append({"role": "assistant", "content": response, 'col':col})
            
        
        
        
        
                
    def chat(self):
        self.display_history()
        models = np.array(['gpt-4o-mini', 'gpt-3.5-turbo', 'bluesoft'])
        model_selected = [st.sidebar.checkbox(model, value = True) for model in models]
        
        
        prompt = st.chat_input('Yo!')
        
        if prompt:
            with st.chat_message('user'):
                st.markdown(prompt)
                st.session_state.msgs.append({'role': 'user', 'content': prompt})
            
                
            if col_sum:=sum(model_selected):
                columns = st.columns(col_sum)
                for col, model in zip(columns, models[model_selected]):
                    if col_sum>1:
                        with col:
                            if model=='bluesoft':
                                self.custom_model_respond(prompt, True)
                                
                            else:
                                self.gpt_respond(model, True)
                    else:
                        if model=='bluesoft':
                            self.custom_model_respond(prompt, True)
                                
                        else:
                            self.gpt_respond(model, True)
                        
                                
            else:
                self.gpt_respond('gpt-4')
                
            