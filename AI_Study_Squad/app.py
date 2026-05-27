from groq import Groq
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def ask_agent(name, instruction, user_query):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": user_query}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def save_log(user_query, responses):
    logs = []
    if os.path.exists("study_logs.json"):
        with open("study_logs.json", "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    logs.append({"query": user_query, "responses": responses})
    with open("study_logs.json", "w") as f:
        json.dump(logs, f, indent=4)

if __name__ == "__main__":
    print("🎓 AI Study Squad is Active.")
    while True:
        user_input = input("\nEnter a topic (or 'exit'): ")
        if user_input.lower() == "exit":
            break
        result = ask_agent("Nerd", "You are The Nerd. Be technical.", user_input)
        print(result)
