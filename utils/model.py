from llama_cpp import Llama
import json

class Model():
    def __init__(self, dir_path, chat_format="chatml"):
        self.llm = Llama(
            model_path=dir_path,
            chat_format=chat_format
        )

    def chat(self, messages):
        response = self.llm.create_chat_completion(messages=messages)
        text_content = response['choices'][0]['message']['content']
        return text_content
    
    def stream(self, messages):
        for i in self.llm.create_chat_completion(messages=messages, stream=True):
            i = i['choices'][0]['delta']
            if i == {'role': 'assistant'}:
                pass
            else:
                try:
                    yield i['content']
                except:
                    pass