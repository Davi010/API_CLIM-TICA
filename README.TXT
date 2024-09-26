docker build -t my-openweather-app .

docker run -p 8000:8000 my-openweather-app

#comandos parensentação
# Criar um DataFrame a partir dos dados coletados
    df = pd.DataFrame([weather_data])
    
    # Exibir o DataFrame
    print(df)