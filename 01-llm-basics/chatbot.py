import ollama

messages = [
    {"role": "system", "content": "You are a helpful assistant. Keep answers short."}
]

print("Chatbot ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    messages.append({"role": "user", "content": user_input})

    stream = ollama.chat(model="llama3.2", messages=messages, stream=True)

    print("Bot: ", end="")
    reply = ""
    for chunk in stream:
        piece = chunk["message"]["content"]
        print(piece, end="", flush=True)
        reply += piece
    print("\n")

    messages.append({"role": "assistant", "content": reply})