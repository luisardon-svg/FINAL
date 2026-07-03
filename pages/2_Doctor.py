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