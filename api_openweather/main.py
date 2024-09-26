import requests  # Biblioteca para fazer requisições HTTP
import pandas as pd  # Biblioteca para manipulação de dados
import matplotlib.pyplot as plt  # Biblioteca para visualização de dados

# Definindo constantes para a API
API_KEY = '442a1ac939e50a654bbd2770df6d28d4'  # Substitua pela sua chave da API
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'  # URL base da API

# Função para calcular o índice de risco de queimadas (FWI)
def calculate_fwi(temp, humidity, wind_speed, precipitation):
    # Cálculos baseados nas fórmulas do FWI
    FFMC = 101 - (humidity / 10)
    DMC = 0.5 * (temp - 5)
    DC = 2 * (temp - 5)
    ISI = (FFMC * wind_speed) / 100
    BUI = DMC + DC
    FWI = ISI * (BUI / 50)
    return FWI

# Função para determinar o nível de risco de queimadas baseado no FWI
def assess_fire_risk(fwi):
    if fwi < 5:
        return "Baixo risco"
    elif 5 <= fwi < 15:
        return "Risco moderado"
    else:
        return "Alto risco"

# Função para coletar dados climáticos da API
def get_weather_data(location):
    params = {
        'q': location,  # Localização para a qual os dados são solicitados
        'appid': API_KEY,  # Chave da API
        'units': 'metric'  # Unidades métricas para os dados
    }
    response = requests.get(BASE_URL, params=params)  # Faz a requisição

    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        print("Erro ao obter dados para a localização fornecida.")
        return None  # Retorna None em caso de erro

    return response.json()  # Retorna os dados em formato JSON

# Localização para consulta
location = 'Amazonas'  # Altere a localização conforme necessário
data = get_weather_data(location)  # Coleta os dados climáticos

if data:
    # Extração de dados climáticos
    temp = data['main']['temp']  # Temperatura
    humidity = data['main']['humidity']  # Umidade
    wind_speed = data['wind']['speed']  # Velocidade do vento
    precipitation = data.get('rain', {}).get('1h', 0)  # Precipitação na última 1h

    # Cálculo do FWI
    fwi = calculate_fwi(temp, humidity, wind_speed, precipitation)
    fire_risk = assess_fire_risk(fwi)  # Avaliação do risco de queimadas

    # Criar DataFrame com os dados coletados
    df = pd.DataFrame({
        'Parâmetros': ['Temperatura', 'Umidade', 'Velocidade do Vento', 'Precipitação', 'FWI'],
        'Valores': [temp, humidity, wind_speed, precipitation, fwi]
    })

    # Definir cores para cada barra do gráfico
    colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#FF4500']  # Cores das barras

    # Criar o gráfico de barras
    plt.figure(figsize=(10, 6))  # Define o tamanho do gráfico
    bars = plt.bar(df['Parâmetros'], df['Valores'], color=colors)  # Cria as barras

    # Adicionar valores ao topo de cada barra
    for bar in bars:
        height = bar.get_height()  # Altura da barra
        plt.annotate(f'{height:.2f}',  # Adiciona o valor na barra
                     xy=(bar.get_x() + bar.get_width() / 2, height),  # Posição do texto
                     xytext=(0, 3),  # Deslocamento do texto em relação à barra
                     textcoords='offset points',
                     ha='center', va='bottom')  # Alinhamento do texto

    # Configurações do gráfico
    plt.ylabel('Valores', fontsize=12)  # Rótulo do eixo Y
    plt.xlabel('Parâmetros', fontsize=12)  # Rótulo do eixo X
    plt.title(f'Dados Climáticos em {location}\nRisco de Fogo: {fire_risk}', fontsize=14)  # Título
    plt.xticks(fontsize=12)  # Tamanho dos rótulos do eixo X
    plt.yticks(fontsize=12)  # Tamanho dos rótulos do eixo Y
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição
    plt.show()  # Exibe o gráfico
