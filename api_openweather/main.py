from fastapi import FastAPI
import requests
import pandas
import matplotlib.pyplot as plt

app = FastAPI()

API_KEY = 'Use_sua_chave'  # Substitua pela sua chave
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

@app.get("/fwi/{location}")
def get_fwi(location: str):
    # Faz a chamada à API do OpenWeatherMap para obter dados climáticos ao vivo
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        return {"error": "Não foi possível obter dados para a localização fornecida."}

    data = response.json()

    # Verifica se os dados foram retornados corretamente
    if 'main' not in data or 'wind' not in data:
        return {"error": "Dados climáticos não disponíveis."}

    # Extração de dados climáticos
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    precipitation = data.get('rain', {}).get('1h', 0)  # Precipitação na última 1h

    # Cálculo do FWI
    fwi = calculate_fwi(temp, humidity, wind_speed, precipitation)
    fire_risk = assess_fire_risk(fwi)

    return {
        'location': location,
        'temperature': temp,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'precipitation': precipitation,
        'FWI': fwi,
        'fire_risk': fire_risk
    }
