from math import ceil
import requests
import pandas as pd
import os

class DadosRepositorios:

    def __init__(self, owner):
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.access_token = os.getenv("GITHUB_ACCESS_TOKEN")

        self.headers = {
            'Authorization': f'Bearer ' + self.access_token,
            'X-GitHub-Api-Version': '2022-11-28'
        }
    
    def lista_repositorios(self):
        repos_list = []

        for page_num in range(1, 20):
            try:
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    repos_list.extend(response.json())
                else:
                    print(f"Erro ao obter dados: {response.status_code}")
                    break
            except requests.exceptions.RequestException as e:
                print(f"Erro na requisição: {e}")
                break

        return repos_list
        
    def nomes_repos(self, repos_list):
        repo_names = []
        for page in repos_list:
            try:
                repo_names.append(page['name'])
            except KeyError:
                pass

        return repo_names
    
    def nomes_linguagens(self, repos_list):
        repo_languages = []
        for page in repos_list:
            try:
                repo_languages.append(page['language'])
            except KeyError:
                pass

        return repo_languages
    
    def cria_df_linguagens(self):
        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos(repositorios)
        linguagens = self.nomes_linguagens(repositorios)

        dados = pd.DataFrame()
        dados['repository_name'] = nomes
        dados['language'] = linguagens

        return dados
    
amazon_rep = DadosRepositorios('amzn')
ling_mais_usadas_amzn = amazon_rep.cria_df_linguagens()
#print(ling_mais_usadas_amzn)

netflix_rep = DadosRepositorios('netflix')
ling_mais_usadas_netflix = netflix_rep.cria_df_linguagens()

spotify_rep = DadosRepositorios('spotify')
ling_mais_usadas_spotify = spotify_rep.cria_df_linguagens()

apple_rep = DadosRepositorios('apple')
ling_mais_usadas_apple = apple_rep.cria_df_linguagens()

# Salvando os dados

ling_mais_usadas_amzn.to_csv('dados/linguagens_amazn.csv')
ling_mais_usadas_netflix.to_csv('dados/linguagens_netflix.csv')
ling_mais_usadas_spotify.to_csv('dados/linguagens_spotify.csv')
ling_mais_usadas_apple.to_csv('dados/linguagens_apple.csv')