from utils.download import download_model
from utils.hardware import check, check_ram


check()
from utils.model import Model
import yaml
from colorama import Fore, Style
import os
from threading import Thread
from typing import Iterator
import gradio as gr
import torch


models = {
    'Qwen-1.5-0.5-Chat': 'https://huggingface.co/Qwen/Qwen1.5-0.5B-Chat-GGUF/resolve/main/qwen1_5-0_5b-chat-q4_0.gguf',
    'LLaMA-7B-Chat-Uncensored': 'https://huggingface.co/TheBloke/llama2_7b_chat_uncensored-GGUF/resolve/main/llama2_7b_chat_uncensored.Q2_K.gguf',
    'Mistral-Instruct-v0.1': 'https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q2_K.gguf',
}

try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except yaml.YAMLError as e:
    print(f"Invalid YAML format: {e}")
    exit(1)

for model in config['models']:
    if model['state']:
        download_model(models[model['name']], f'models/{model["name"]}.gguf')

ram = check_ram()
if check_ram() <= 4:
    print(Fore.YELLOW + f"WARNING: You have {ram}GB(s) of RAM. This may cause issues with the models.")
    print("Consider upgrading your RAM or using a smaller model." + Style.RESET_ALL)

model = Model('models/LLaMA-7B-Chat-Uncensored.gguf')

MAX_MAX_NEW_TOKENS = 2048
DEFAULT_MAX_NEW_TOKENS = 1024
MAX_INPUT_TOKEN_LENGTH = int(os.getenv("MAX_INPUT_TOKEN_LENGTH", "4096"))

def generate(
     message: str,
     chat_history: 'list[tuple[str, str]]',
     system_prompt: str,
     max_new_tokens: int = 1024,
     temperature: float = 0.6,
     top_p: float = 0.9,
     top_k: int = 50,
     repetition_penalty: float = 1.2,
) -> Iterator[str]:
    conversation = []
    print('ashbiashdi')
    if system_prompt:
        conversation.append({"role": "system", "content": system_prompt})
    for user, assistant in chat_history:
        conversation.extend([{"role": "user", "content": user}, {"role": "assistant", "content": assistant}])
    conversation.append({"role": "user", "content": message})

    streamer = model.stream(conversation)

    outputs = []
    for text in streamer:
        outputs.append(text)
        yield "".join(outputs)


chat_interface = gr.ChatInterface(
    fn=generate,
    stop_btn=None,
    examples=[
        ["Hello there! How are you doing?"],
        ["Can you explain briefly to me what is the Python programming language?"],
        ["Explain the plot of Cinderella in a sentence."],
        ["What is the meaning of life?"],
        ["What is the best programming language?"],
    ],
)

with gr.Blocks() as demo:
    chat_interface.render()

if __name__ == "__main__":
    demo.launch(share=True)
