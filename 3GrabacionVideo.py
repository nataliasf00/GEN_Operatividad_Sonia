#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
import json
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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


# Crea el motor de SQLAlchemy
# Asegúrate de reemplazar 'dialecto', 'usuario', 'contraseña', 'host', 'puerto' y 'nombre_bd' con tus datos reales
engine = create_engine('mysql+pymysql://saocomct_camaras:1t&F)DQG6BLq@190.90.160.5/saocomct_camaras')

try:
    # Realiza la consulta
    df_bd = pd.read_sql("SELECT terid FROM grabacion_video WHERE DATE(fecha_consulta) = CURDATE()", con=engine)
    df_bd = df_bd.drop_duplicates()
    terid_consultados = df_bd['terid'].tolist()
except:
    terid_consultados = []

print(terid_consultados)


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

df2_2['numero_unidad'] = df2_2['carlicence'].str[:6]

df2_2['cantidad_canales'] = df2_2["cname"].str.count(",") + 1
# Str de los canales
df2_2["str_chn"] = df2_2["cantidad_canales"].apply(lambda x: ",".join(map(str, range(1, x + 1))))

df_canales = df2_2[['terid', 'str_chn', 'numero_unidad', 'cname']]

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

df_status = pd.merge(df_status, df_canales, on='terid', how='left')

df_status = df_status[~df_status['terid'].isin(terid_consultados)]
df_status = df_status.reset_index(drop=True)

# Obtenemos la fecha actual
hoy = datetime.today()

# Lista vacía para almacenar los primeros días de los últimos 6 meses
primer_dia_meses = []

# Iteramos para los últimos 6 meses
for i in range(6):
    # Restamos exactamente i meses y fijamos el día como 1
    primer_dia_mes = (hoy - relativedelta(months=i)).replace(day=1)
    primer_dia_meses.append(primer_dia_mes)

# Ordenamos las fechas de más antiguo a más reciente
primer_dia_meses = sorted(primer_dia_meses)

df_dias_grabacion = pd.DataFrame()

for i in range(len(df_status)):
    terid = df_status.loc[i, 'terid']
    # Mostramos las fechas en formato de texto
    for fecha in primer_dia_meses:
        starttime = fecha.strftime("%Y-%m-%d")
        if __name__ == '__main__':
            url8_1 = 'http://192.168.90.68:12056/api/v1/basic/record/calendar?key=' + key + '&terid=' + terid + '&starttime=' + starttime + '&st=1'
            response8_1 = requests.get(url8_1) 
            
            if response8_1.status_code == 200:
                content8_1 = response8_1.content
                
        dic8_1 = json.loads(content8_1.decode('utf-8'))        
        # Extraer los datos del diccionario
        data8_1 = dic8_1['data']
        
        # Crear el DataFrame
        df8_1 = pd.DataFrame(data8_1)
        df8_1['terid'] = terid
        df_dias_grabacion = pd.concat([df_dias_grabacion, df8_1], ignore_index=True)
    
# Consultar la cantidad de horas de grabación por día

st = '1'

df_horas_grabacion = pd.DataFrame()


for i in range(len(df_dias_grabacion)):
    starttime = df_dias_grabacion.loc[i, 'date'] + ' 00:00:00'
    endtime = df_dias_grabacion.loc[i, 'date'] + ' 23:59:59'
    terid = df_dias_grabacion.loc[i, 'terid']
    chl = df_status.loc[df_status['terid'] == terid, 'str_chn'].values[0]
    
    if __name__ == '__main__':
        #url8_2_2 = 'http://192.168.90.68:12056/api/v1/basic/record/filelist?key=zT908g2j9nhKs59b4mtGh5k2haZh2YDTaEn27jMamS0%3D&terid=00D2029ACC&starttime=2024-11-06 00:00:00&endtime=2024-11-06 23:59:59&chl=1,2,3,4&st=1'
        url8_2 = 'http://192.168.90.68:12056/api/v1/basic/record/filelist?key=' + key + '&terid=' + terid + '&starttime=' + starttime + '&endtime=' + endtime + '&chl=' + chl + '&st=' + st 
        response8_2 = requests.get(url8_2) 
    
        if response8_2.status_code == 200:
            content8_2 = response8_2.content

    dic8_2 = json.loads(content8_2.decode('utf-8'))        
    # Extraer los datos del diccionario
    data8_2 = dic8_2['data']
    
    # Crear el DataFrame
    df8_2 = pd.DataFrame(data8_2)
    df8_2['terid'] = terid
    df8_2['fecha_grabacion'] = df_dias_grabacion.loc[i, 'date']
    df_horas_grabacion = pd.concat([df_horas_grabacion, df8_2], ignore_index=True)

df_horas_grabacion['starttime'] = pd.to_datetime(df_horas_grabacion['starttime'])
df_horas_grabacion['endtime'] = pd.to_datetime(df_horas_grabacion['endtime'])

# Calcular la duración en horas y agregarla como una nueva columna
df_horas_grabacion['duration_hours'] = (df_horas_grabacion['endtime'] - df_horas_grabacion['starttime']).dt.total_seconds() / 3600

df_grabacion = df_horas_grabacion.groupby(["terid", "chn", "fecha_grabacion"], as_index=False)["duration_hours"].sum()
df_grabacion = pd.merge(df_grabacion, df_status[['terid', 'numero_unidad', 'cname']], on='terid', how='left')

df_grabacion = df_grabacion.groupby(['terid', 'numero_unidad', 'chn']).agg(
    fecha_inicial=('fecha_grabacion', 'min'),
    fecha_final=('fecha_grabacion', 'max'),
    cantidad_dias=('fecha_grabacion', 'count'),
    horas_grabacion=('duration_hours', 'sum')
).reset_index()

from datetime import datetime, timedelta

fecha_actual = datetime.now()
df_grabacion['fecha_consulta'] = fecha_actual

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

df_grabacion.to_sql('grabacion_video', con=motor, if_exists='append', index=False)

