# Inicio.py
#Pagina principal de la aplicación
# Streamlit usa archivo como pag. de inicio; el resto estaran en pages/ y aparecerán en barra lateral
import streamlit as st #Importamos libreria de stremlit
st.set_page_config(page_title="Vital Health Monitor", page_icon="⚕️", layout="centered")

#ENCABEZADO
st.title("Health Monitor ⚕️")
st.write("Plataforma de seguimiento remoto de la salud")

st.divider()

st.subheader("¿Cómo funciona?")
col1, col2, col3 = st.columns(3)

with col1: 
    with st.container(border=True):
        st.markdown("### Paciente")
        st.write("Registra su glucosa y otros datos día a día.")

with col2: 
    with st.container(border=True):
        st.markdown("### Sistema")
        st.write("Analiza los datos y detecta señales de alerta")

with col3:
    with st.container(border=True):
        st.markdown("### Doctor")
        st.write("Revisa la alerta, sugiere y aprueba el tratamiento")
    
st.divider()

#Reencuadre etico
st.info(
    "⚕️ **El sistema sugiere, pero la decisión final siempre es del doctor.** "
    "Nunca se automatiza la receta médica."
)
st.caption("Usa el menú de la izquierda para entrar al panel del paciente o del doctor.")
