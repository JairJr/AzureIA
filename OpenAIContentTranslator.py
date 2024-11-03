#Install dependecies 'pip install requests beautifulsoup4 openai langchain-openai'

import requests
from bs4 import BeautifulSoup
from langchain_openai.chat_models.azure import AzureChatOpenAI

def extract_text_from_url(url):
    response = requests.get(url)
    #print(response.status_code)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch URL: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    text = soup.get_text(separator=' ')
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

extract_text_from_url('https://dev.to/rohan_sharma/how-did-a-dumbo-become-an-open-source-contributor-333c')

client = AzureChatOpenAI(
    azure_endpoint = 'https://oai-lab1.openai.azure.com/',
    api_key = "YOUR_API_KEY",
  #you can check correct one on the destiny URI on https://ai.azure.com/ selecting your deployment
    api_version = '2024-08-01-preview',
  #here i used gpt-35-turbo but you can use another one
    deployment_name = 'gpt-35-turbo',
    max_retries=0
)

def translate_article(text, lang):
  messages = [
      ("system", "você atua como tradutor de textos"),
      ("user", f"traduza o {text} para o idioma {lang} e responda em markdown")
  ]
  response = client.invoke(messages)
  print(response)
  return response.content

url = 'https://dev.to/rohan_sharma/how-did-a-dumbo-become-an-open-source-contributor-333c'
text = extract_text_from_url(url)
translate_article(text, 'portugues')
  
#translate_article('You are heavy coder and was never a dumbo for sure ', 'portugues')
