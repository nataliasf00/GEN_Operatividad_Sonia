# 📌 Operatividad Sonia (Crones para indicador)

[![Estado del Proyecto](https://img.shields.io/badge/status-terminado-ogreen.svg)]()
[![Licencia](https://img.shields.io/badge/licencia-MIT-blue.svg)]()

## 🚀 Descripción  

**Operatividad Sonia (Crones para indicador)** son una serie de scripts alojados en el Servidor de Power BI que realizan las consultas sobre operatividad de cámaras, alarmas y grabación de video.

### 🎯 Propósito  
Consultar la API de Ceiba II, extrayendo la información de operatividad de cámaras, alarmas y grabación de video para posteriormente alojarla en la base de datos.

## 📌 Funcionalidades  

### 📥 **1TransmisionDVR**  
- ✅ **Consultar la Key de CeibaII**
  - url = 'http://192.168.90.68:12056/api/v1/basic/key?username=' + username + '&password=' + password
  - requests = GET
  - username = 'admin'
  - password = 'admin'

- ✅ **Obtener la lista de dispositivos**
  - url = 'http://192.168.90.68:12056/api/v1/basic/devices?key=' + key
  - requests = GET
  - parameters = key
 
- ✅ **Obtener la lista de dispositivos en línea**
  - url = 'http://192.168.90.68:12056/api/v1/basic/state/now'
  - requests = POST
  - parameters = key, terid

- ✅ **Consultar el último reporte de GPS**
  - url = 'http://192.168.90.68:12056/api/v1/basic/gps/last'
  - requests = POST
  - parameters = key, terid

- ✅ **Agregar columna con la fecha y hora actuales**

- ✅ **Autenticarse en APPBordo para obtener la key**
  - url = 'https://adbordo.valliu.co:8443/api/login/user'
  - requests = POST
  - parameters = username, password **usar un usuario y contraseña activo de Bitacora**
 
- ✅ **Consultar el estado y ubicación de los vehículos en APPBordo**
  - url = 'https://adbordo.valliu.co:8443/api/status/vehicle?x-api-key=32947e4e1104f267aa4c97f04e81a50fb57cbcdc'
  - requests = GET
  - parameters = x-api-key

- ✅ **Guardar la información en la base de datos**

#### 📥 **Descripción de columnas** 

| 📦 Columna         | 🔍 Descripción |
|--------------------|----------------|
| numero_unidad      | número interno del bus                |
| terid              | serial del AD Plus               |
| sim                | número de la simcard               |
| channelcount       | cantidad de canales                |
| cname              | nombre de los canales               |
| Transmision DVR    | estado del DVR (Online o Offline)               |
| fecha_consulta     | fecha en la que se consulto el estado               |
| fecha              | fecha actual               |
| numero_consulta    | numero de consulta en el día               |
| gpstime            | hora del GPS               |
| altitude           | altitud               |
| direction          | dirección |
| gpslat             | latitud |
| gpslng             | longitud |
| velocidad          | velocidad |
| time_server        | hora del servidor |
| ubicacion_actual   | ubicación del vehiculo en Bitácora |
| estado             | estado del vehiculo según Bitácora |

### 📥 **2DetalleAlarmas**
- ✅ **Almacenar el dataframe con la interpretación de las alarmas**
  - data_alarmas
    
- ✅ **Consultar ultima fecha de alarmas guardadas en la base de datos de camaras**
  - Se suma un segundo de más a la última fecha de alarmas guardadas para realizar la consulta futura
 
- ✅ **Consultar la Key de CeibaII**
  - url = 'http://192.168.90.68:12056/api/v1/basic/key?username=' + username + '&password=' + password
  - requests = GET
  - username = 'admin'
  - password = 'admin'

- ✅ **Obtener la lista de dispositivos**
  - url = 'http://192.168.90.68:12056/api/v1/basic/devices?key=' + key
  - requests = GET
  - parameters = key
 
- ✅ **Consultar las alarmas registradas en los dispositivos**
  - url = 'http://192.168.90.68:12056/api/v1/basic/alarm/detail'
  - requests = POST
  - parameters = key, terid, type, starttime, endtime

- ✅ **Guardar la información en la base de datos**

#### 📥 **Descripción de columnas** 

| 📦 Columna             | 🔍 Descripción |
|------------------------|----------------|
| terid                  | serial del AD Plus              |
| gpstime                |hora del GPS               |
| altitude               | altitud               |
| direction              | dirección |
| gpslat                 | latitud |
| gpslng                 | longitud |         
| speed                  | velocidad               |
| recordspeed            |                |
| state                  | estado de la alarma               |
| time                   | fecha y hora de ocurrencia de la alarma               |
| type                   | tipo de alarma               |
| content                | contenido de la alarma               |
| cmdtype                | canal               |
| alarmid                | ID de la alarma               |
| fecha_consulta         | fecha de consulta del cron               |
| Center description     | Nombre de la alarma               |
| English description    | Nombre de la alarma               |
| numero_unidad          | número interno del bus               |

### 📥 **3GrabacionVideo**  
- ✅ **Consultar la Key de CeibaII**
  - url = 'http://192.168.90.68:12056/api/v1/basic/key?username=' + username + '&password=' + password
  - requests = GET
  - username = 'admin'
  - password = 'admin'
 
- ✅ **Consultar en la base de datos de camaras las unidades a las que se les consulto la grabación de video en la fecha actual**

- ✅ **Obtener la lista de dispositivos**
  - url = 'http://192.168.90.68:12056/api/v1/basic/devices?key=' + key
  - requests = GET
  - parameters = key
  
- ✅ **Obtener la lista de dispositivos en línea**
  - url = 'http://192.168.90.68:12056/api/v1/basic/state/now'
  - requests = POST
  - parameters = key, terid
 
- ✅ **Quitar de la lista de dispositivos los que ya fueron consultados**

- ✅ **Consultar el calendario de grabación de video de los dispositivos (fechas en las que se tiene grabación)**
  - url = 'http://192.168.90.68:12056/api/v1/basic/record/calendar?key=' + key + '&terid=' + terid + '&starttime=' + starttime + '&st=1'
  - requests = GET
  - parameters = key, terid, starttime
  - **Se realiza la consulta para verificar los ultimos 6 meses**
 
 - ✅ **Consultar la cantidad de horas de grabación por dia en los dispositivos**
  - url = 'http://192.168.90.68:12056/api/v1/basic/record/filelist?key=' + key + '&terid=' + terid + '&starttime=' + starttime + '&endtime=' + endtime + '&chl=' + chl + '&st=' + st 
  - requests = GET
  - parameters = key, terid, starttime, endtime, chl, st
  - **st = '1'**   

  - ✅ **Guardar la información en la base de datos**

#### 📥 **Descripción de columnas** 

| 📦 Columna             | 🔍 Descripción |
|------------------------|----------------|
| terid                  | serial del AD Plus              |
| numero_unidad          | número interno del bus               |
| chn                    | número del canal               |
| fecha_inicial          | fecha inicial de grabación en el dispositivo             |
| fecha_final            | fecha final de grabación en el dispositivo                 |
| cantidad_dias          | cantidad de días de grabación guardados en el dispositivo |
| horas_grabacion        | cantidad de horas de grabación guardados en el dispositivo |
| fecha_consulta         | fecha en la que se realizo la consulta|         

## 📌 Requisitos  

Para ejecutar el proyecto, asegúrate de tener **Python 3.8 o superior** instalado y las siguientes librerías:  

### 📦 **Librerías necesarias**  

| 📦 Librería                | 🔍 Descripción |
|---------------------------|----------------|
| `pandas` (`pd`)           | Manipulación y análisis de datos, especialmente para trabajar con **Excel**, **CSV**, etc. |
| `json`                    | Manejo de datos en formato **JSON**. *(Incluida en Python, no requiere instalación)* |
| `numpy` (`np`)            | Cálculo numérico y trabajo con arreglos multidimensionales. |
| `requests`                | Realizar peticiones HTTP de forma sencilla. Ideal para APIs. |
| `pyodbc`                  | Conexión con bases de datos mediante **ODBC** (SQL Server, Access, etc.). |
| `datetime`, `timedelta`, `relativedelta`   | Manejo de fechas y tiempos en Python. *(Incluida en Python, no requiere instalación)* |
| `sqlalchemy`              | Toolkit para trabajar con bases de datos SQL de forma **ORM o SQL pura**. |
| `mysql.connector`         | Conexión directa a bases de datos **MySQL** desde Python. |

```
# 📖 Ejecucion de los crones
Los scripts se ejecutan a partir de una tarea en el programador de tareas de Windows en el servidor de Power BI

## ❓Frencuencias
1️⃣ TransmisionDVR
🕒**Frecuencia cada 3 horas** = 12:00am, 3:00am,, 6:00am, 9:00am, 12:00pm, 3:00pm, 6:00pm, 9:00pm

2️⃣ DetalleAlarmas
🕒**Frecuencia cada 3 horas** = 2:50am, 5:50am, 8:50am, 11:50am, 2:50pm, 5:50pm, 8:50pm, 11:50pm

3️⃣ GrabacionVideo
🕒** Frecuencia aproximadamente cada 3 horas** = 5:00am, 7:00am, 8:00am, 10:00am, 11:00am, 2:00pm, 4:00pm, 5:00pm, 7:00pm

# Contacto y Soporte 
Para dudas o soporte técnico, contactar a la profesional de Mejoramiento Continuo de Sistema Alimentador Oriental.
