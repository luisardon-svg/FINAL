# Inicio.py
#Pagina principal de la aplicación
# Streamlit usa archivo como pag. de inicio; el resto estaran en pages/ y aparecerán en barra lateral
import streamlit as st #Importamos libreria de stremlit
import logica
st.set_page_config(page_title="Vital Health Monitor", page_icon="⚕️", layout="centered")

#ENCABEZADO
st.title("Health Monitor ⚕️")
st.write("Plataforma de seguimiento remoto de la salud")

st.divider()

#CASO DE DEMOSTRACIÓN
st.subheader("Caso de demostración")
paciente_demo = logica.pacientes_db[1]
col1, col2 = st.columns(2)

with col1: 
    with st.container(border=True):
        st.markdown("### Paciente")
        st.write(f"**{paciente_demo['nombre']}**")
        st.write(f"Edad: {paciente_demo['edad']} años")
        st.write(f"Condiciones: Diabético e hipertenso en seguimiento remoto")

with col2: 
    with st.container(border=True):
        st.markdown("### Sistema")
        #Leer datos en vivo
        registros = paciente_demo["registros_glucosa"]
        promedio = logica.calcular_promedio_glucosa(registros)
        alerta = logica.generar_alerta(registros)


    if "ALERTA" in alerta: 
        st.error("🔴 **ALERTA activa** — niveles de glucosa elevados")
    else: 
        st.success("✅ Dentro de rango")

st.write(f"Promedio glucosa: **{promedio} mg/dL**")
    
st.divider()
# --- FLUJO EN 3 ETAPAS ---
st.subheader("¿Cómo funciona?")
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 🧑 Paciente")
        st.write("Registra su glucosa y otros datos día a día.")

with col2:
    with st.container(border=True):
        st.markdown("### ⚙️ Sistema")
        st.write("Analiza los datos en tiempo real y detecta señales de alerta basándose en límites clínicos establecidos (glucosa > 130 mg/dL, presión > 140 mmHg, oxigenación < 92%).")

with col3:
    with st.container(border=True):
        st.markdown("### 👩‍⚕️ Doctor")
        st.write("Revisa la alerta, sugiere y aprueba el tratamiento.")

#METRICAS RESUMEN
st.subheader("Estado actual del sistema")
col1, col2, col3 = st.columns(3)

col1.metric("Pacientes monitoreados", "1")
col2.write("**Métricas rastreadas**\nGlucosa, Presión, Oxigenación)")

if "ALERTA" in alerta: 
    col3. metric("Estado", "🔴 Activa")
else: 
    col3. metric("Estado", "✅ Estable")

st.divider()

#Reencuadre etico
st.info(
    "⚕️ **El sistema sugiere, pero la decisión final siempre es del doctor.** "
    "Nunca se automatiza la receta médica."
)
st.caption("Usa el menú de la izquierda para entrar al panel del paciente o del doctor.")
