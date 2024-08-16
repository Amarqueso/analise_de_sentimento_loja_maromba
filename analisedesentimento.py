import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from collections import Counter

# Baixar o stemmer e recursos do nltk
nltk.download('rslp')
nltk.download('stopwords')
nltk.download('punkt')

# Scraping da página
url = 'https://www.lojamaromba.com/novo-black-mamba-90-caps-com-dmaa-innovative-labs/?utm_source=organic&utm_content=%7C%7Cnemu_ZOL3iGCGZn'
cabecalhos = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0'}

pagina = requests.get(url, headers=cabecalhos)
sopa = BeautifulSoup(pagina.text, 'html.parser')
conteudo_avaliacao = sopa.find(class_='ratings-content')
avaliacoes_formatadas = []

for p in conteudo_avaliacao.find_all('p'):
    if 'info' not in p.get('class', []):
        avaliacoes_formatadas.append(p.get_text())

# Dicionário de sentimentos com radicais
dicionario_sentimentos = {
    "positivo": ["bom", "ótim", "excelent", "feliz", "curt", "gost", "potent", "impression", "rápid", "parabém", "recom", "melhor", "incr", "aprov"],
    "negativo": ["ruim", "péssim", "horrivel", "trist", "pi", "negativ", "fraq", "desej", "baix"]
}

# Lista de modificadores que podem alterar o sentido
modificadores = ["muito", "demais", "não", "pouco"]

# Inicializando o stemmer e stopwords
stemmer = RSLPStemmer()
stopwords_pt = set(stopwords.words('portuguese'))

def analisar_sentimentos(avaliacoes_formatadas):
    todas_as_palavras = []
    palavras_classificadas = {"positivo": [], "negativo": []}  # Removido "neutro"
    
    for avaliacao in avaliacoes_formatadas:
        tokens = word_tokenize(avaliacao, language='portuguese')
        tokens_filtrados = [palavra for palavra in tokens if palavra.lower() not in stopwords_pt and palavra.isalpha()]
        
        # Analisando cada palavra e o contexto ao redor dela
        for i, palavra in enumerate(tokens_filtrados):
            sentimento = None
            radical = stemmer.stem(palavra.lower())
            
            # Verificando se há modificadores antes da palavra
            if i > 0 and tokens_filtrados[i-1].lower() in modificadores:
                modificador = tokens_filtrados[i-1].lower()
            else:
                modificador = None
            
            # Checando se a palavra é positiva ou negativa
            if any(radical.startswith(p) for p in dicionario_sentimentos["positivo"]):
                sentimento = "positivo"
                if modificador == "não" or modificador == "pouco":
                    sentimento = "negativo"
                elif modificador == "muito" or modificador == "demais":
                    sentimento = "positivo"
            elif any(radical.startswith(n) for n in dicionario_sentimentos["negativo"]):
                sentimento = "negativo"
                if modificador == "não" or modificador == "pouco":
                    sentimento = "positivo"
                elif modificador == "muito" or modificador == "demais":
                    sentimento = "negativo"

            # Adiciona a palavra na categoria apropriada
            if sentimento:
                palavras_classificadas[sentimento].append(palavra)
                todas_as_palavras.append(palavra)
    
    return todas_as_palavras, palavras_classificadas

# Analisar sentimentos e palavras
todas_as_palavras, palavras_classificadas = analisar_sentimentos(avaliacoes_formatadas)

# Função para colorir as palavras conforme o sentimento
def cor_palavra(palavra, **kwargs):
    if palavra in palavras_classificadas['positivo']:
        return 'green'
    elif palavra in palavras_classificadas['negativo']:
        return 'red'

# Filtrando apenas palavras positivas e negativas
palavras_filtradas = palavras_classificadas['positivo'] + palavras_classificadas['negativo']
texto_unido = ' '.join(palavras_filtradas)

# Gerando a nuvem de palavras
nuvem_palavras = WordCloud(width=800, height=400, background_color='white', color_func=cor_palavra).generate(texto_unido)

# Exibindo a nuvem de palavras
plt.figure(figsize=(10, 5))
plt.imshow(nuvem_palavras, interpolation='bilinear')
plt.axis('off')
plt.show()

# Exibindo as palavras mais usadas
contagem_palavras = Counter(palavras_filtradas)
print("Palavras mais usadas:")
print(contagem_palavras.most_common(10))
