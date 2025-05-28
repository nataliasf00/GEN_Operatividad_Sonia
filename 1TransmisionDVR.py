#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importación de librerias

import requests
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from datetime import datetime, timedelta

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

# Obtener la lista de dispositivos
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

# Extraer el número de la unidad y dejar las columnas que son de interés
df_dispositivos = df2_2.copy()

df_dispositivos['numero_unidad'] = df_dispositivos['carlicence'].str[:6]

df_dispositivos = df_dispositivos[['numero_unidad', 'terid', 'sim', 'channelcount', 'cname']]

# Sacar la lista de los seriales de los dipositivos
main_terid = df2_2['terid'].tolist()


# Sacar la lista de dispositivos que están en línea
if __name__ == '__main__':
    url5_2 = 'http://192.168.90.68:12056/api/v1/basic/state/now'
    rq5_2 =  {
"key": key,
"terid": main_terid,
}
    response5_2 = requests.post(url5_2, json=rq5_2)
    
    if response5_2.status_code == 200:
        content5_2 = response5_2.content

dic5_2 = json.loads(content5_2.decode('utf-8'))

# Extraer los datos del diccionario
data5_2 = dic5_2['data']

# Crear el DataFrame
df5_2 = pd.DataFrame(data5_2)

# Mostrar el DataFrame resultante
df_status = df5_2.copy()

df_status['Transmision DVR'] = "Online"


df_dispositivos = pd.merge(df_dispositivos, df_status, on='terid', how='left')
df_dispositivos.fillna('Offline', inplace=True)

# Crea el motor de SQLAlchemy
# Asegúrate de reemplazar 'dialecto', 'usuario', 'contraseña', 'host', 'puerto' y 'nombre_bd' con tus datos reales
engine = create_engine('mysql+pymysql://saocomct_camaras:1t&F)DQG6BLq@190.90.160.5/saocomct_camaras')

try:
    # Realiza la consulta
    df_bd = pd.read_sql("SELECT numero_consulta FROM operatividad_camaras WHERE DATE(fecha) = CURDATE() ORDER BY numero_consulta DESC LIMIT 1", con=engine)
    numero_consulta = df_bd.loc[0, 'numero_consulta'] + 1

except:
    numero_consulta = 1

df_dispositivos['numero_consulta'] = numero_consulta

if __name__ == '__main__':
    url3_3 = 'http://192.168.90.68:12056/api/v1/basic/gps/last'
    rq3_3 = {
"key": key,
"terid": main_terid
}
    response3_3 = requests.post(url3_3, json=rq3_3)
    
    if response3_3.status_code == 200:
        content3_3 = response3_3.content

dic3_3 = json.loads(content3_3.decode('utf-8'))

# Extraer los datos del diccionario
data3_3 = dic3_3['data']

# Crear el DataFrame
df3_3 = pd.DataFrame(data3_3)

fecha_actual = datetime.now()

# Agregar la columna con la fecha y hora actuales a todas las filas
df3_3['fecha_consulta'] = fecha_actual
df3_3['fecha'] = df3_3['fecha_consulta'].dt.date
# Mostrar el DataFrame resultante

df_ult_gps = df3_3.copy()
df_ult_gps = df_ult_gps.rename(columns={'speed': 'velocidad', 'recordspeed': 'vel_tacografo', 'time': 'time_server'})
df_ult_gps


df_dispositivos = pd.merge(df_dispositivos, df_ult_gps[['terid', 'fecha_consulta', 'fecha', 'gpstime', 'altitude', 'direction', 'gpslat', 'gpslng', 'velocidad', 'time_server']], on='terid', how='left')
df_dispositivos = df_dispositivos[['numero_unidad', 'terid', 'sim', 'channelcount', 'cname', 'Transmision DVR', 'fecha_consulta', 'fecha', 'numero_consulta', 'gpstime', 'altitude', 'direction', 'gpslat', 'gpslng', 'velocidad', 'time_server']]
df_dispositivos

# API de Appbordo
url1 = "https://adbordo.valliu.co:8443/api/login/user"
req1 = {
    "username": "NSANCHEZ",  # Reemplaza con tu usuario
    "password": "1234"  # Reemplaza con tu contraseña
}
headers1 = {
    "Content-Type": "application/json"
}

# Realizar la solicitud POST
try:
    response1 = requests.post(url1, json=req1, headers=headers1)
    response1.raise_for_status()  
    content1 = response1.content
    dic1 = json.loads(content1.decode('utf-8'))
    key = dic1['key']
    print(key)
except requests.exceptions.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")

# Estado de los vehículos

url2 = "https://adbordo.valliu.co:8443/api/status/vehicle?x-api-key=32947e4e1104f267aa4c97f04e81a50fb57cbcdc"
headers2 = {
    "x-api-key": key
}

# Realizar la solicitud GET
try:
    response2 = requests.get(url2, headers=headers2)
    response2.raise_for_status() 
    content2 = response2.content
    dic2 = json.loads(content2.decode('utf-8'))
except requests.exceptions.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")

dic2 = json.loads(content2.decode('utf-8'))

# Extraer los datos del diccionario
data2 = dic2

# Crear el DataFrame
df2 = pd.DataFrame(data2)

df3 = df2.copy()

df3['numero_unidad'] = 'BUS' + df3['movil']
df3 = df3.drop(columns=['fecha_hora_suceso', 'movil'])
df3['ubicacion_actual'] =  df3['ubicacion_actual'].str.upper()
df3['estado'] =  df3['estado'].str.upper()
df3.rename(columns={'estado': 'observacion'}, inplace=True)

df3['estado'] = df3['observacion'].apply(lambda x: 
    'OPERATIVO' if isinstance(x, str) and 'OPERATIVO' in x else 
    'VARADO' if isinstance(x, str) and 'VARADO' in x else 
    'MANTENIMIENTO' if isinstance(x, str) and 'MANTENIMIENTO' in x else 
    'DESCONOCIDO'
)


df_dispositivos = pd.merge(df_dispositivos, df3[['numero_unidad', 'ubicacion_actual', 'estado']], on='numero_unidad', how='left')

# Guardar la información en la base de datos
from sqlalchemy import create_engine

usuario = 'saocomct_camaras'
contraseña = '1t&F)DQG6BLq'
host = '190.90.160.5'
puerto = '3306'
base_de_datos = 'saocomct_camaras'


# Crea la cadena de conexión
cadena_conexion = f'mysql+mysqlconnector://{usuario}:{contraseña}@{host}:{puerto}/{base_de_datos}'

# Crea el motor de conexión
motor = create_engine(cadena_conexion)

df_dispositivos.to_sql('operatividad_camaras', con=motor, if_exists='append', index=False)

