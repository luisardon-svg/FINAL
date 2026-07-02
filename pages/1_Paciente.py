#pages/1_Paciente.py
#Panel de paciente (esqueleto)

import streamlit as st
import logica


st.set_page_config(page_title = "Paciente", page_icon = "👤")

# --- Obtenemos los datos del paciente Luis Fernando (ID 1) ---
paciente = logica.pacientes_db[1]    #Accedemos al diccionario y sacamos al paciente con clave [1]

# --- SECCIÓN 1: Encabezado / indentificación ---

st.title("Panel del Paciente")
st.header(paciente["nombre"])
st.write("Edad:", paciente["edad"], "años")

# Mostramos el historial médico recorriendo la lista con un ciclo for

st.subheader("Historial médico")
for condicion in paciente["historial_medico"]:
    st.write("-", condicion)

# --- SECCIÓN 2: Resumen de glucosa (cifras clave) ---
st.subheader("Resumen de glucosa")

# Sacamos la lista de registros de glucosa del paciente
registros = paciente["registros_glucosa"]

# Usamos NUESTRAS funciones de logica.py para calcular cada dato
promedio = logica.calcular_promedio_glucosa(registros)
maximo = logica.encontrar_glucosa_maxima(registros)
tendencia = logica.detectar_tendencia(registros)

# st.columns crea columnas para poner las métricas lado a lado
col1, col2, col3 = st.columns(3)

col1.metric("Promedio", f"{promedio} mg/dL")
col2.metric("Máximo", f"{maximo} mg/dL")
col3.metric("Tendencia", tendencia)