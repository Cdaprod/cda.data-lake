import requests
from pydantic import BaseModel, validator

# Define a base class for Language Models
class LanguageModel(BaseModel):
    model_name: str
    
    class Config:
        arbitrary_types_allowed = True

    def generate(self, prompt: str):
        raise NotImplementedError("This method should be implemented by subclasses.")

# Define the class for GPT-4
class GPT4Model(LanguageModel):
    api_key: str
    api_url: str = "https://api.openai.com/v1/engines/davinci-codex/completions"

    @validator('model_name')
    def validate_model_name(cls, v):
        if v not in ['davinci', 'curie', 'babbage', 'ada']:
            raise ValueError("GPT-4 model name must be one of 'davinci', 'curie', 'babbage', 'ada'.")
        return v

    def generate(self, prompt: str, max_tokens: int = 150, temperature: float = 0.7):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()  # Will raise an exception for HTTP error codes
        return response.json()

# Define the class for Llama models
class LlamaModel(LanguageModel):
    # If you have a local SDK or API for the Llama model, you can implement it here
    def generate(self, prompt: str):
        # Here you would implement the interaction with your local Llama model
        # For this example, let's assume there's a function called `llama_generate` which does this
        response = llama_generate(prompt, self.model_name)
        return response

# Example usage of the GPT-4 model
gpt4 = GPT4Model(model_name='davinci', api_key='your-gpt4-api-key')
gpt4_response = gpt4.generate("What is the capital of France?")
print(gpt4_response)

# Example usage of the Llama model
llama = LlamaModel(model_name='your-llama-model-name')
llama_response = llama.generate("Please summarize the following text...")
print(llama_response)