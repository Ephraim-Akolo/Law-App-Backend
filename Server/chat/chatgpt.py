import openai
import os

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('.env', override=True)

client = openai.OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model, messages=messages)
    # print(response)
    return response.choices[0].message.content



if __name__ == "__main__":
    print(get_completion("what is known as a theory?"))