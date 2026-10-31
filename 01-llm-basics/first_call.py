import ollama

user_input = input("You: ")
response = ollama.chat
(model="llama3.2", messages=[{"role": "user", "content": user_input}])

print(response["message"]["content"])