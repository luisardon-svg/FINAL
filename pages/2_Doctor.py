#pages/2_Doctor.py
#Panel del doctor

import streamlit as st
import logica

st.set_page_config(page_title = "Doctor", page_icon = "🩺")

paciente = logica.pacientes_db[1]

st.title("Panel de doctor")
st.write("Seguimiento remoto del paciente")

st.divider()

#Datos básicos del paciente
st.header(paciente["nombre"])
st.write(f"**Edad:** {paciente['edad']} anios")

#Historial medico: recorremos la lista con un ciclo for
st.subheader("Historial medico")
for condicion in paciente["historial_medico"]:
    st.write("-" + condicion)

st.divider()

#SECCION ": Metricas de glucosa
# lista de registro de paciente 
registros = paciente ["registros_glucosa"]

#Los tres calculos vienen de funciones de logica.py
promedio = logica.calcular_promedio_glucosa(registros)
maxima = logica.encontrar_glucosa_maxima(registros)
tendencia = logica.detectar_tendencia(registros)

st.subheader("Metricas de glucosa")

#st.columns; crearemos 3
col1, col2, col3, = st.columns(3)
col1.metric("Promedio", f"{promedio} mg/dL")
col2.metric("Maxima", f"{maxima} mg/dL")
col3.metric("Tendencia", tendencia)
