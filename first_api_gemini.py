import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
#Matheus-Saggiorato 05/2024

api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-pro")

response_name = model.generate_content('escreva o nome de um cientista famoso na física de partículas ou cosmologia, tente ser aleatória')
candidate_name = response_name.candidates[0]
content_name = candidate_name.content
part_name = content_name.parts[0]
nome_cientista = part_name.text

prompt_dica = f'escreva a principal contribuição na física de partículas ou cosmologia de {nome_cientista}, sem citar o seu nome ou nome da teoria'

response_name = model.generate_content(prompt_dica)
candidate_name = response_name.candidates[0]
content_name = candidate_name.content
part_name = content_name.parts[0]
dica = part_name.text
print(dica)


def response_check(user_response, nome_cientista):
    if user_response.lower() in nome_cientista.lower():
        print(f'Acertou, o nome é {nome_cientista}')
    else:
        print(f'Não foi dessa vez, a resposta é {nome_cientista}')

user_input = input('Quem é o cientista? ')
response_check(user_input, nome_cientista)