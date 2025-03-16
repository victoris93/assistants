from llama_index.llms.ollama import Ollama
import subprocess

def load_model(model):
    try:
        llm = Ollama(model=model)
    except Exception as e:
        subprocess.run(["ollama", "pull", model])    
        llm = Ollama(model=model)
    
    return llm