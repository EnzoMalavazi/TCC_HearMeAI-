import openai
##https://qwenlm.github.io/blog/qwen2.5-max/

openai.api_key = "API KEY"

chat = [{"role": "system", "content": "Você é um assistente útil."}]

while True:
    user_msg = input("Você: ")
    if user_msg.lower() == "quit":
        break

    # Adiciona a mensagem do usuário ao histórico
    chat.append({"role": "user", "content": user_msg})

    # Chamada correta para a API OpenAI com a nova versão
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat
    )

    assistant_response = response.choices[0].message.content
    print("ChatGPT:", assistant_response.strip())

    # Adiciona a resposta do assistente ao histórico
    chat.append({"role": "assistant", "content": assistant_response.strip()})
