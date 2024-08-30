import requests
import base64
import os

class ManipulaRepositorios:

    def __init__(self, username):
        self.username = username
        self.api_base_url = 'https://api.github.com'  # Corrigido para HTTPS
        self.access_token = os.getenv("GITHUB_ACCESS_TOKEN")
        self.headers = {
            'Authorization': "Bearer " + self.access_token,  # Corrigido para Authorization
            'X-GitHub-Api-Version': '2022-11-28'  # Corrigido o formato da data
        }
        
    def cria_repo(self, nome_repo):
        data = {
            "name": nome_repo,
            "description": "Dados dos repositórios de algumas empresas",  # Adicionada a vírgula
            "private": False
        }
        response = requests.post(f"{self.api_base_url}/user/repos",
                                 json=data, headers=self.headers)
        print(f'status_code criação do repositório: {response.status_code}')
    
    def add_arquivo(self, nome_repo, nome_arquivo, caminho_arquivo):

        # Codificando o arquivo
        with open(caminho_arquivo, "rb") as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content)

        # Realizando o upload
        url = f"{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{nome_arquivo}"
        data = {
            "message": "Adicionando um novo arquivo",
            "content": encoded_content.decode("utf-8")
        }

        response = requests.put(url, json=data, headers=self.headers)
        print(f'status_code upload do arquivo: {response.status_code}')

# Instanciando um objeto
novo_repo = ManipulaRepositorios('JeffAirData')

# Criando o repositório
nome_repo = 'linguagens-repositorios-empresas'
novo_repo.cria_repo(nome_repo)

# Adicionando arquivos salvos no repositório criado
novo_repo.add_arquivo(nome_repo, 'linguagens_amazn.csv', 'dados/linguagens_amazn.csv')
novo_repo.add_arquivo(nome_repo, 'linguagens_netflix.csv', 'dados/linguagens_netflix.csv')
novo_repo.add_arquivo(nome_repo, 'linguagens_spotify.csv', 'dados/linguagens_spotify.csv')
novo_repo.add_arquivo(nome_repo, 'linguagens_apple.csv', 'dados/linguagens_apple.csv')