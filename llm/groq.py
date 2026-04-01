from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self):
        pass
    def get_model(self):
        return ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")