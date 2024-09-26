import requests
import pandas as pd
import matplotlib.pyplot as plt

API_KEY = '442a1ac939e50a654bbd2770df6d28d4'  # Substitua pela sua chave
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Função para calcular o FWI (simplificado)
def calculate_fwi(temp, humidity, wind_speed, precipitation):
    FFMC = 101 - (humidity / 10)
    DMC = 0.5 * (temp - 5)
    DC = 2 * (temp - 5)
    ISI = (FFMC * wind_speed) / 100
    BUI = DMC + DC
    FWI = ISI * (BUI / 50)
    return FWI

# Função para determinar o risco de queimadas
def assess_fire_risk(fwi):
    if fwi < 5:
        return "Baixo risco"
    elif 5 <= fwi < 15:
        return "Risco moderado"
    else:
        return "Alto risco"

# Função para coletar dados climáticos
def get_weather_data(location):
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        print("Erro ao obter dados para a localização fornecida.")
        return None

    return response.json()

# Processar dados
location = 'Amazonas'  # Altere a localização conforme necessário
data = get_weather_data(location)

if data:
    # Extração de dados climáticos
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    precipitation = data.get('rain', {}).get('1h', 0)  # Precipitação na última 1h

    # Cálculo do FWI
    fwi = calculate_fwi(temp, humidity, wind_speed, precipitation)
    fire_risk = assess_fire_risk(fwi)

    # Criar dataframe com todos os dados
    df = pd.DataFrame({
        'Parâmetros': ['Temperatura', 'Umidade', 'Velocidade do Vento', 'Precipitação', 'FWI'],
        'Valores': [temp, humidity, wind_speed, precipitation, fwi]
    })

    # Definir cores diferentes para cada barra
    colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#FF4500']  # Cores para cada barra

    # Plotar gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df['Parâmetros'], df['Valores'], color=colors)

    # Adicionar números ao lado das barras
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',  # Adiciona o valor com duas casas decimais
                    xy=(bar.get_x() + bar.get_width() / 2, height),  # Posição do texto
                    xytext=(0, 3),  # Deslocamento do texto em relação à barra
                    textcoords='offset points',
                    ha='center', va='bottom')

    ax.set_ylabel('Valores', fontsize=12)
    ax.set_xlabel('Parâmetros', fontsize=12)
    
    # Adicionar informação sobre o risco de fogo no título
    ax.set_title(f'Dados Climáticos em {location}\nRisco de Fogo: {fire_risk}', fontsize=14)
    
    plt.xticks(fontsize=12)  # Aumentar tamanho dos rótulos do eixo X
    plt.yticks(fontsize=12)  # Aumentar tamanho dos rótulos do eixo Y

    plt.tight_layout()  # Ajustar layout para evitar sobreposição
    plt.show()
