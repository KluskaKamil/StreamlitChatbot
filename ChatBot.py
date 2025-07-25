import streamlit as st
from openai import OpenAI
import numpy as np

class ChatBot:
    def __init__(self, bot_title):
        st.title(bot_title)
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        if 'msgs' not in st.session_state:
            st.session_state.msgs = []
            
            
            
    def display_history(self):
        for msg in st.session_state.msgs:
            col_num = msg.get('col_num', 1)
            for col in st.columns(col_num):
                with col:   
                    with st.chat_message(msg['role']):
                        st.markdown(msg['content'])
                
            
    def create_columns_and_respond(self, col_number):
        pass
    
    
    def gpt_respond(self, model, col_sum=1):
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
            #st.session_state.msgs.append({"role": "assistant", "content": response, 'col_num':col_sum})
            return response
        
        
        
                
    def chat(self):
        self.display_history()
        models = np.array(['gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4.1'])
        model_selected = [st.sidebar.checkbox(model, value = True) for model in models]
        #model_selected = [st.sidebar.checkbox('gpt-4', value=True), st.sidebar.checkbox('gpt-3.5-turbo'), st.sidebar.checkbox('gpt-4.1')]
        
        
        prompt = st.chat_input('Yo!')
        
        if prompt:
            with st.chat_message('user'):
                st.markdown(prompt)
                st.session_state.msgs.append({'role': 'user', 'content': prompt})
            
                
            if col_sum:=sum(model_selected):
                columns = st.columns(col_sum)
                for col, model in zip(columns, models[model_selected]):
                    with col:
                        response = self.gpt_respond(model, col_sum)
                        
                st.session_state.msgs.append({"role": "assistant", "content": response, 'col_num':col_sum})
                
            else:
                self.gpt_respond('gpt-4')
                
            