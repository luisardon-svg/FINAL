# Inicio.py
#Pagina principal de la aplicación
# Streamlit usa archivo como pag. de inicio; el resto estaran en pages/ y aparecerán en barra lateral
import streamlit as st #Importamos libreria de stremlit
import logica #modulo con logica de porgra
st.set_page_config(page_title="Vital Health Monitor", page_icon="⚕️")

st.title("Health Monitor ⚕️")
st.write("Plataforma de seguimiento de salud, usa el menu de la izquierda para ingresar con base al tipo de usuario que seas.")

#prueba de conexion con logica.py
#traemos al paciente empleado en el caso
paciente = logica.pacientes_db[1]
registros = paciente ["registros_glucosa"]

#El promedio es calculado por una funcion creada dentro de logica.py
promedio = logica.calcular_promedio_glucosa(registros)

st.divider()
st.subheader("Conexion con la logica ✓")
st.write(f"Paciente: **{paciente['nombre']}**")
st.write(f"Promeido de glucosa: **{promedio:.2f} mg/dL**")

         


