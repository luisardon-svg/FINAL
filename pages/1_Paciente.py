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
