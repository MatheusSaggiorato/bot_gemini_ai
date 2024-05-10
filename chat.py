import google.generativeai as genai
import os
import io
import pyperclip
import csv
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)

generation_config = {
    "candidate_count": 1,
    "temperature": 0.5,
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

text_without_summary = pyperclip.paste().strip()

resume_prompt = f'Summarize and prepare the entire content of the following text, with the concepts, learnings and teachings, so that another AI can use it optimally, in the form of a question -> answer, very summarized. {text_without_summary}'

print('Aguarde por favor, seus flashcards estão sendo gerados! Avisaremos quando estiver pronto')
prepared_text = chat.send_message(resume_prompt)

text_prompt = prepared_text.text

prompt = f'Create a list of questions and answers very summarized to Anki flashcards in "front, back" format, separated by commas in CSV format, focusing on the all concepts, questions and content extracted from this text {text_prompt}Example:(Question on front) How powerful is the product ( aⁿbᵐ)ᵏ?(Answer on back) = a^(nk)b^(mk)*Instructions:*-Separate each flashcard on a new line.-Provide clear, concise explanations, definitions, or elaborations on the back of the card. On the front there should always be a small clear question of what the user should remember, and on the back the answer.example"Em que ano foi ratificado o acordo de paz com a Alemanha?, em 1990"'

response = chat.send_message(prompt)

flashcards = response.text

linhas = flashcards.split('\n')

# Criar um objeto StringIO para armazenar o conteúdo CSV
conteudo_csv = io.StringIO()

# Criar um escritor CSV
escritor_csv = csv.writer(conteudo_csv)

# Escrever a linha de cabeçalho
escritor_csv.writerow(['Pergunta', 'Resposta'])

# Converter cada linha em uma lista e escrever no CSV
for linha in linhas:
  # Tentar dividir em pergunta e resposta (caso contrário, considerar tudo como pergunta)
  try:
    pergunta, resposta = linha.split(',', 1)  # Limitar a divisão em 1 vírgula
  except ValueError:
    pergunta = linha.strip()  # Se falhar, considera tudo como pergunta
    resposta = ''  # e resposta vazia

  # Remover espaços em branco no início e no final
  pergunta = pergunta.strip()
  resposta = resposta.strip()

  # Escrever a pergunta e a resposta no CSV
  escritor_csv.writerow([pergunta, resposta])

# Obter o conteúdo do CSV como string
conteudo_csv.seek(0)
texto_csv = conteudo_csv.read()

# Salvar o conteúdo CSV em um arquivo
with open('flashcards.csv', 'w', encoding='utf-8') as arquivo_csv:
  arquivo_csv.write(texto_csv)

print("Arquivo CSV salvo com sucesso em 'bot_gemini_ai/flashcards.csv'.")