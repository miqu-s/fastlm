# check different hardware types and install the correct bindings!!111
import platform
import subprocess
import psutil


def check_ram():
    total_memory = psutil.virtual_memory().total
    total_memory_gb = total_memory / (1024 ** 3)
    return float(total_memory_gb)

def is_silicon_cpu():
    if platform.system() == 'Darwin':
        cmd = "/usr/sbin/sysctl -n machdep.cpu.brand_string"
        cpu_info = subprocess.check_output(cmd, shell=True).decode().strip()
        if 'Apple M' in cpu_info:
            install_bindings = subprocess.check_output('CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python', shell=True)
            print('Apple M1 CPU detected. Installing Metal llama-cpp-python bindings.')
            print(install_bindings)
            return True
        else:
            install_bindings = subprocess.check_output('CMAKE_ARGS="-DLLAMA_METAL=off -DLLAMA_CLBLAST=on" pip install llama-cpp-python', shell=True)
            print('Intel CPU detected. Installing OpenCL llama-cpp-python bindings.')
            print(install_bindings)
            return True


def check_gpu():
    try:
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE)
        if result.returncode == 0:
            check_cuda()
        else:
            install_bindings = subprocess.check_output('CMAKE_ARGS="-DLLAMA_CUDA=off -DLLAMA_CLBLAST=on" pip install llama-cpp-python', shell=True)
            print('No NVIDIA GPU detected. Installing OpenCL llama-cpp-python bindings.')
            print(install_bindings)
            return False

    except FileNotFoundError:
        return False

def check_cuda():
    try:
        result = subprocess.run(['nvcc', '--version'], stdout=subprocess.PIPE)
        if result.returncode == 0:
            install_bindings = subprocess.check_output('CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python', shell=True)
            print('NVIDIA GPU detected. Installing CUDA llama-cpp-python bindings.')
            print(install_bindings)
            return True
        else:
            print("CUDA is not installed. Please install CUDA.")
            return False
    except FileNotFoundError:
        print("CUDA is not installed. Please install CUDA.")
        return False
    
def check():
    if is_silicon_cpu():
        return
    else:
        check_gpu()
        return
