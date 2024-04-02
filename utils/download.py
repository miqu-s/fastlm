import requests
from tqdm import tqdm
from colorama import Fore, Style
import os
import hashlib

hashes = {
    'Qwen-1.5-0.5-Chat.gguf': 'a1323198f4620fc4142ec7527d2853654e5a2843d1d8bc01ec0b08e09c9019da634ed7289f5d77c071bee92730fdb0a7e33e32be71c338fe572a9073fe950510',
    'LLaMA-7B-Chat-Uncensored.gguf': '21ae8df539f1a1160828aa57c43ea5751c8c735cd852f8ffa5356ff5d5636f0b0bc6d2d16a7ebb18b7400f89f071b5784c9d4e2b522232540ae8ca753acd114d',
    'Mistral-Instruct-v0.1.gguf': 'd05b8d92eaaf1b38bad75d7a3d37d160120dd1209826db73c7cf896c4704179d090ff7748da86fbf0ed3a8dcf95fc880b77bd83828878ef55112816e5e59a658'
}

def hash_file(file_path, algorithm='blake2b'):
    hash_algo = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def download_model(url, save_path):
    if os.path.exists(save_path):
        if hash_file(save_path) == hashes[save_path.split('/')[-1]]:
            print(Fore.GREEN + "Model already exists" + Style.RESET_ALL)
            return
        else:
            print(Fore.RED + "Model exists but hash does not match, redownloading." + Style.RESET_ALL)
            pass
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=Fore.BLUE + "Downloading" + Style.RESET_ALL)

    with open(save_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()

    if total_size != 0 and progress_bar.n != total_size:
        print(Fore.RED + "Download failed" + Style.RESET_ALL)
        os.remove(save_path)
    else:
        print(Fore.GREEN + "Download successful" + Style.RESET_ALL)
