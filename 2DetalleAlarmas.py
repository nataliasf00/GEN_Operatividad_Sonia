#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import pandas as pd
import json
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Diccionario de las alarmas

data_alarmas = {
    'type': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 20, 29, 36, 47, 58, 59, 60, 61, 62, 63, 64, 74, 160, 161, 162, 163, 164, 165, 166, 169, 172, 173, 174, 175, 176, 392],
    'Center description': [
        'Video loss alarm', 'Motion detection alarm', 'Camera-covering alarm', 'Abnormal storage alarm',
        'IO 1', 'IO 2', 'IO 3', 'IO 4', 'IO 5', 'IO 6', 'IO 7', 'IO 8', 'Emergency alarm', 
        'High-speed alarm', 'Low voltage alarm', 'Accelerometer alarm', 'Geo-fencing alarm', 
        'Illegal shutdown', 'Temperature alarm', 'Distance alarm', 
        'Alarm for abnormal temperature changes', 'Driver Fatigue', 'No driver', 
        'Phone Detection', 'Smoking Detection', 'Driver Distraction', 'Lane departure', 
        'Forward Collision Warning', 'Abnormal boot alarm', 'Speeding Alarm', 
        'Impeding violation', 'Following Distance Monitoring', 'Pedestrian Collision Warning', 
        'Yawning Detection', 'Left blind spot detection', 'Right blind spot detection', 
        'Seat Belt Detection', 'Rolling Stop Alarm', 'Left BSD warning', 'Left BSD alarm', 
        'Right BSD warning', 'Right BSD alarm', 'Forward blind area'
    ],
    'English description': [
        'Video loss alarm', 'Motion detection alarm', 'Camera-covering alarm', 'Abnormal storage alarm',
        'IO 1', 'IO 2', 'IO 3', 'IO 4', 'IO 5', 'IO 6', 'IO 7', 'IO 8', 'Emergency alarm', 
        'High-speed alarm', 'Low voltage alarm', 'Accelerometer alarm', 'Geo-fencing alarm', 
        'Illegal shutdown', 'Temperature alarm', 'Distance alarm', 
        'Alarm for abnormal temperature changes', 'Driver Fatigue', 'No driver', 
        'Phone Detection', 'Smoking Detection', 'Driver Distraction', 'Lane departure', 
        'Forward Collision Warning', 'Abnormal boot alarm', 'Speeding Alarm', 
        'Impeding violation', 'Following Distance Monitoring', 'Pedestrian Collision Warning', 
        'Yawning Detection', 'Left blind spot detection', 'Right blind spot detection', 
        'Seat Belt Detection', 'Rolling Stop Alarm', 'Left BSD warning', 'Left BSD alarm', 
        'Right BSD warning', 'Right BSD alarm', 'Forward blind area'
    ]
}

# Crear el DataFrame
df_alarmas = pd.DataFrame(data_alarmas)


# Crea el motor de SQLAlchemy
# Asegúrate de reemplazar 'dialecto', 'usuario', 'contraseña', 'host', 'puerto' y 'nombre_bd' con tus datos reales
engine = create_engine('mysql+pymysql://saocomct_camaras:1t&F)DQG6BLq@190.90.160.5/saocomct_camaras')

# Realiza la consulta
df_bd = pd.read_sql("SELECT gpstime FROM detalle_alarmas ORDER BY gpstime DESC LIMIT 1", con=engine)


fecha_original = df_bd.loc[0, 'gpstime']

# Formatear la fecha en el formato deseado

# Agregar un segundo
fecha_inicio_dia = fecha_original + timedelta(seconds=1)
fecha_inicio_dia = fecha_inicio_dia.strftime('%Y-%m-%d %H:%M:%S')

fechas_inicio_dia = []
fechas_inicio_dia.append(fecha_inicio_dia)

print(fecha_inicio_dia)

fecha_actual = datetime.now()
fecha_fin_dia = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')

fechas_fin_dia = []
fechas_fin_dia.append(fecha_fin_dia)

print(fecha_fin_dia)

# Sacar el Key para acceder a la API
username = 'admin'
password = 'admin'

if __name__ == '__main__':
    url1_1 = 'http://192.168.90.68:12056/api/v1/basic/key?username=' + username + '&password=' + password
    response1_1 = requests.get(url1_1)
    
    if response1_1.status_code == 200:
        content1_1 = response1_1.content

dic1_1 = json.loads(content1_1.decode('utf-8'))

# Extraer la key
key = dic1_1['data']['key']
print(key)


if __name__ == '__main__':
    url2_2 = 'http://192.168.90.68:12056/api/v1/basic/devices?key=' + key
    response2_2 = requests.get(url2_2)
    
    if response2_2.status_code == 200:
        content2_2 = response2_2.content

dic2_2 = json.loads(content2_2.decode('utf-8'))

# Extraer los datos del diccionario
data2_2 = dic2_2['data']

# Crear el DataFrame
df2_2 = pd.DataFrame(data2_2)

# Mostrar el DataFrame resultante
df2_2

# Sacar la lista de los seriales de los dipositivos
main_terid = df2_2['terid'].tolist()
print(main_terid)

df_dispositivos = df2_2.copy()

df_dispositivos['numero_unidad'] = df_dispositivos['carlicence'].str[:6]


df_detail_alarmas = pd.DataFrame()

for i in range(len(fechas_inicio_dia)):
    start_time = fechas_inicio_dia[i]
    end_time = fechas_fin_dia[i]
    
    if __name__ == '__main__':
        url4_2 = 'http://192.168.90.68:12056/api/v1/basic/alarm/detail'
        rq4_2 =  {"key": key, "terid": main_terid, "type": [], "starttime": start_time, "endtime": end_time}

        response4_2 = requests.post(url4_2, json=rq4_2)
        
        if response4_2.status_code == 200:
            content4_2 = response4_2.content

    # Creación del dataframe

    dic4_2 = json.loads(content4_2.decode('utf-8'))

    

    # Extraer los datos del diccionario
    data4_2 = dic4_2['data']

    # Crear el DataFrame
    df4_2 = pd.DataFrame(data4_2)
    df_detail_alarmas = pd.concat([df_detail_alarmas, df4_2], ignore_index=True)
    # Mostrar el DataFrame resultante

fecha_actual = datetime.now()
df_detail_alarmas['fecha_consulta'] = fecha_actual

# Agregar el nombre de las alarmas
df_detail_alarmas = pd.merge(df_detail_alarmas, df_alarmas, on='type', how='left')


df_detail_alarmas['terid'] = df_detail_alarmas['terid'].astype(str)
df_detail_alarmas['gpstime'] = pd.to_datetime(df_detail_alarmas['gpstime'])
df_detail_alarmas['gpslat'] = df_detail_alarmas['gpslat'].astype(float)
df_detail_alarmas['gpslng'] = df_detail_alarmas['gpslng'].astype(float)
df_detail_alarmas['time'] = pd.to_datetime(df_detail_alarmas['time'])
df_detail_alarmas['content'] = df_detail_alarmas['content'].astype(str)
df_detail_alarmas['alarmid'] = df_detail_alarmas['alarmid'].astype(str)
df_detail_alarmas['Center description'] = df_detail_alarmas['Center description'].astype(str)
df_detail_alarmas['English description'] = df_detail_alarmas['English description'].astype(str)

# Supongamos que deseas agregar la columna 'status' de df_status
df_detail_alarmas = pd.merge(df_detail_alarmas, df_dispositivos[['terid', 'numero_unidad']], on='terid', how='left')

usuario = 'saocomct_camaras'
contraseña = '1t&F)DQG6BLq'
host = '190.90.160.5'
puerto = '3306'
base_de_datos = 'saocomct_camaras'

# Crea la cadena de conexión
cadena_conexion = f'mysql+mysqlconnector://{usuario}:{contraseña}@{host}:{puerto}/{base_de_datos}'

# Crea el motor de conexión
motor = create_engine(cadena_conexion)

df_detail_alarmas.to_sql('detalle_alarmas', con=motor, if_exists='append', index=False)


# In[ ]:




