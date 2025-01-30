import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def mostrar_analisis(data_tiempo):
    '''
    Esta función toma datos de tiempo en formato JSON, extrae los valores de temperatura, 
    humedad, presión y descripción, simula datos para un periodo de 11 días (5 días anteriores, el actual y 5 días siguientes) 
    y muestra gráficos de estos valores usando matplotlib.
    '''
    try:
    # Usar los datos pasados como argumento    
        data = data_tiempo  
    except (FileNotFoundError, json.JSONDecodeError):
        print("No se pudo cargar el archivo de datos del clima.")
        return

    # Obtener los datos actuales de temperatura, humedad y presión
    temperatura_actual = data['list'][0]['main']['temp']
    humedad_actual = data['list'][0]['main']['humidity']
    presion_actual = data['list'][0]['main']['pressure']
    
    # Simulación de datos para los últimos 5 días, el actual y los próximos 5 días
    temperatura = [temperatura_actual + np.random.uniform(-3, 3) for _ in range(5)] + [temperatura_actual] + [temperatura_actual + np.random.uniform(-3, 3) for _ in range(5)]
    humedad = [humedad_actual + np.random.uniform(-10, 10) for _ in range(5)] + [humedad_actual] + [humedad_actual + np.random.uniform(-10, 10) for _ in range(5)]
    presion = [presion_actual + np.random.uniform(-5, 5) for _ in range(5)] + [presion_actual] + [presion_actual + np.random.uniform(-5, 5) for _ in range(5)]

    # Crear un DataFrame con los datos simulados
    dates = pd.date_range(end=pd.Timestamp('today'), periods=11)
    df = pd.DataFrame({
        'Fecha': dates,
        'Temperatura (°C)': temperatura,
        'Humedad (%)': humedad,
        'Presión (hPa)': presion})

    # Establecer la columna 'Fecha' como índice
    df.set_index('Fecha', inplace=True)

    # Graficar los datos
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Gráfico de Temperatura
    df['Temperatura (°C)'].plot(ax=axs[0], color='red', marker='o', linestyle='-')
    axs[0].set_title('Temperatura (°C) durante 11 días')
    axs[0].set_xlabel('Fecha')
    axs[0].set_ylabel('Temperatura (°C)')
    axs[0].grid(True)

    # Gráfico de Humedad
    df['Humedad (%)'].plot(ax=axs[1], color='blue', marker='o', linestyle='-')
    axs[1].set_title('Humedad (%) durante 11 días')
    axs[1].set_xlabel('Fecha')
    axs[1].set_ylabel('Humedad (%)')
    axs[1].grid(True)

    # Gráfico de Presión
    df['Presión (hPa)'].plot(ax=axs[2], color='green', marker='o', linestyle='-')
    axs[2].set_title('Presión (hPa) durante 11 días')
    axs[2].set_xlabel('Fecha')
    axs[2].set_ylabel('Presión (hPa)')
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()
