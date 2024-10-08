﻿# Análise de Sentimentos e Geração de Nuvem de Palavras


Neste projeto, realizei uma análise de sentimentos com base nas avaliações dos usuários sobre o termogênico Black Mamba, extraídas do site de suplementos Loja Maromba. Utilizando técnicas de web scraping e processamento de linguagem natural (NLP), coletei e analisei as avaliações para identificar sentimentos positivos e negativos.

Etapas do Projeto
1. Web Scraping
Utilizei a biblioteca requests para fazer a requisição HTTP na página do produto e BeautifulSoup para fazer o parsing do conteúdo HTML. Extraí as avaliações dos usuários localizadas na classe ratings-content, limpei e armazenei os dados para análise.

2. Análise de Sentimentos
Usei o RSLPStemmer do NLTK para reduzir as palavras aos seus radicais e desenvolvi um dicionário de sentimentos com radicais associados a sentimentos positivos e negativos. Considerando modificadores como "muito", "demais" e "não", ajustei a classificação das palavras.

3. Processamento de Texto
As avaliações foram tokenizadas e filtradas para remover stopwords. Comparei os radicais das palavras com o dicionário de sentimentos para classificá-las como positivas ou negativas.

4. Geração de Nuvem de Palavras
Incluí apenas palavras classificadas como positivas e negativas na nuvem de palavras. Usei a biblioteca WordCloud para visualizar essas palavras, destacando as positivas em verde e as negativas em vermelho, proporcionando uma visão rápida das palavras mais recorrentes.

5. Contagem de Palavras Mais Usadas
Além da nuvem de palavras, o código realiza a contagem das palavras mais frequentes nas avaliações, destacando os termos mais usados tanto entre os sentimentos positivos quanto negativos.

![Figure_1](https://github.com/user-attachments/assets/9fbc1740-bd91-4278-b32e-54590c6328d3)
