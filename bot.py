import google.generativeai as genai
import pyperclip
import io
import csv
import os
from dotenv import load_dotenv
load_dotenv()

#carrega o api do gemini como variável de ambiente
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)

generation_config = {
    "candidate_count": 1,
    "temperature": 0.3,
}

safety_settings = {
    "HARASSMENT": "BLOCK_NONE",
    "HATE": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE",
}

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

chat = model.start_chat(history=[])

#pega o último conteúdo da área de transferência(que foi copiado)
text_prompt = pyperclip.paste().strip()

#Prompt para o gemini com o conteúdo da área de transferência
prompt = f'Taking as a basis all the concepts and teachings extracted from this text: {text_prompt}. Create a list of very summarized questions and answers to study on the Anki app flashcards in "front, back" format in CSV format separated by commas.Example:(front) How powerful is the product ( aⁿbᵐ)ᵏ?, = a^(nk)b^(mk) *Instructions:*-Don''t write de words "back" and "front". -Separate each flashcard on a new line.-Provide clear, concise explanations, definitions, or elaborations on the back of the card. On the front there should always be a small clear question of what the user should remember, and on the back the answer. Another example (Em que ano foi ratificado o acordo de paz com a Alemanha?, em 1990). Remember that the result must be based on the text provided at the beginning and in format [question, result], without brackets and symbols'

print('Aguarde por favor, seus flashcards estão sendo gerados! Avisaremos quando estiver pronto')

#pega a resposta do gemini e transforma nos flash cards
#ainda sem a formatação correta para usar no Anki
response = chat.send_message(prompt)
flashcards = response.text

#quebra em linhas
linhas = flashcards.split('\n')

#Cria um objeto StringIO para armazenar o conteúdo CSV
conteudo_csv = io.StringIO()

#Cria um escritor CSV
escritor_csv = csv.writer(conteudo_csv)

#Escreve a linha de cabeçalho
escritor_csv.writerow(['Pergunta', 'Resposta'])

#Converte cada linha em uma lista e escreve no CSV
for linha in linhas:
  #Tenta dividir em pergunta e resposta (caso contrário, considera tudo como pergunta)
  try:
    pergunta, resposta = linha.split(',', 1)  #Limitar a divisão em 1 vírgula
  except ValueError:
    pergunta = linha.strip()  #Se falhar, considera tudo como pergunta
    resposta = ''  #e resposta vazia

  #Remove espaços em branco no início e no final
  pergunta = pergunta.strip()
  resposta = resposta.strip()

  #Escreve a pergunta e a resposta no CSV
  escritor_csv.writerow([pergunta, resposta])

#Obtm o conteúdo do CSV como string
conteudo_csv.seek(0)
texto_csv = conteudo_csv.read()

#variáveis para gerar números diferente nos arquivos
nome_base = 'flashcards'
extensao = '.csv'
contador = 1

# Verifica se o arquivo com o nome atual existe
while os.path.exists(f'{nome_base}{contador}{extensao}'):
    contador += 1
nome_arquivo = f'{nome_base}{contador}{extensao}'

# Escreve o conteúdo no arquivo
with open(nome_arquivo, 'w', encoding='utf-8') as arquivo_csv:
    arquivo_csv.write(texto_csv)

print(f"Arquivo CSV salvo com sucesso em '{nome_arquivo}'.")
