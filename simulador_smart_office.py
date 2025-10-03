import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configurações
start_date = datetime(2025, 9, 1, 0, 0, 0)  # data inicial simulada
end_date = start_date + timedelta(days=7)
interval = timedelta(minutes=15)

# Geração da linha do tempo
timestamps = []
current_time = start_date
while current_time < end_date:
    timestamps.append(current_time)
    current_time += interval

# Funções auxiliares
def simulate_temperature(timestamp):
    hour = timestamp.hour
    weekday = timestamp.weekday()  # 0=segunda, 6=domingo
    base_temp = 21 if hour < 6 else 24 if hour < 18 else 22
    # Meio da semana mais quente
    if weekday in [2, 3]:  # quarta/quinta
        base_temp += 1.5
    noise = np.random.normal(0, 0.5)
    return round(base_temp + noise, 1)

def simulate_luminosity(timestamp):
    hour = timestamp.hour
    if 6 <= hour <= 18:
        base_lux = np.random.randint(300, 600)  # horário comercial
    elif 19 <= hour <= 22:
        base_lux = np.random.randint(100, 300)  # iluminação reduzida
    else:
        base_lux = 0  # noite
    return base_lux

def simulate_occupancy(timestamp):
    hour = timestamp.hour
    weekday = timestamp.weekday()
    if weekday < 5 and 8 <= hour <= 17:  # dias úteis, horário comercial
        prob = 0.8 if hour not in [12, 13] else 0.4  # menos ocupação no almoço
        return 1 if np.random.rand() < prob else 0
    elif weekday == 5 and 9 <= hour <= 13:  # sábado, meio período
        return 1 if np.random.rand() < 0.3 else 0
    else:  # noite e domingo quase vazio
        return 1 if np.random.rand() < 0.05 else 0

# Construção do dataset
data = []
for ts in timestamps:
    data.append({"timestamp": ts, "sensor_id": "TEMP01", "valor": simulate_temperature(ts)})
    data.append({"timestamp": ts, "sensor_id": "LUX01", "valor": simulate_luminosity(ts)})
    data.append({"timestamp": ts, "sensor_id": "OCC01", "valor": simulate_occupancy(ts)})

# DataFrame final
df = pd.DataFrame(data)
df.to_csv("smart_office_data.csv", index=False)

print("Arquivo smart_office_data.csv gerado com sucesso!")
