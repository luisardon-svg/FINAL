# Inicio.py
#Pagina principal de la aplicación
# Streamlit usa archivo como pag. de inicio; el resto estaran en pages/ y aparecerán en barra lateral
import streamlit as st #Importamos libreria de stremlit
import logica
st.set_page_config(page_title="Vital Health Monitor", page_icon="⚕️", layout="centered")

#ENCABEZADO
st.title("Health Monitor ⚕️")
st.write("Plataforma de seguimiento remoto de la salud")

#Reencuadre etico
st.info(
    "⚕️ **El sistema sugiere, pero la decisión final siempre es del doctor.** "
    "Nunca se automatiza la receta médica."
)

st.caption("Usa el menú de la izquierda para entrar al panel del paciente o del doctor.")
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



st.divider()

# --- GLOSARIO DE TÉRMINOS MÉDICOS ---
st.subheader("📚 Glosario de términos médicos")

with st.expander("**Glucosa**"):
    st.write("""
    Azúcar en la sangre. Es la principal fuente de energía del cuerpo. 
    - **Rango normal:** 70–100 mg/dL en ayuno.
    - **En este proyecto:** límite de alerta = **130 mg/dL**. Valores superiores sugieren diabetes descontrolada.
    """)

with st.expander("**Presión arterial (PA)**"):
    st.write("""
    Fuerza con la que la sangre empuja contra las paredes de las arterias.
    Se mide en mmHg (milímetros de mercurio) y tiene dos valores: sistólica/diastólica.
    - **Rango normal:** 120/80 mmHg o menor.
    - **En este proyecto:** límite de alerta sistólica = **140 mmHg**. Valores superiores indican hipertensión.
    """)

with st.expander("**Sistólica (presión sistólica)**"):
    st.write("""
    Presión MÁXIMA cuando el corazón se contrae y bombea sangre.
    Es el primer número en la lectura de PA (ej. **140**/80).
    - **Normal:** < 120 mmHg.
    - **En este proyecto:** monitoreo continuo con alerta en 140 mmHg.
    """)

with st.expander("**Diastólica (presión diastólica)**"):
    st.write("""
    Presión MÍNIMA cuando el corazón se relaja entre latidos.
    Es el segundo número en la lectura de PA (ej. 140/**90**).
    - **Normal:** < 80 mmHg.
    - **En este proyecto:** se registra pero sin alerta independiente (el límite principal es sistólica > 140).
    """)

with st.expander("**Oxigenación / SpO₂ (saturación de oxígeno)**"):
    st.write("""
    Porcentaje de hemoglobina en la sangre que transporta oxígeno.
    Se mide en % y refleja cuánto oxígeno tienen los glóbulos rojos.
    - **Rango normal:** 95–100%.
    - **En este proyecto:** límite de alerta = **< 92%**. Valores inferiores sugieren hipoxia (falta de oxígeno).
    """)

with st.expander("**Tendencia**"):
    st.write("""
    Dirección general de los valores en el tiempo.
    - **Subiendo:** los valores aumentan en los últimos días → riesgo de empeorar.
    - **Bajando:** los valores disminuyen en los últimos días → mejora.
    - **Estable:** sin cambio significativo.
    """)

with st.expander("**Semáforo de estado**"):
    st.write("""
    Indicador visual del riesgo general del paciente basado en todas las métricas:
    - 🔴 **ALERTA:** alguna métrica está fuera de rango (requiere atención inmediata).
    - 🟡 **ATENCIÓN:** métrica en zona de riesgo o tendencia adversa (vigilar).
    - 🟢 **ESTABLE:** todas las métricas dentro de rango normal.
    """)

with st.expander("**Racha de alerta (días consecutivos)**"):
    st.write("""
    Número de días seguidos en los que una métrica ha estado fuera de rango.
    Calculado de forma recursiva, de atrás hacia adelante en el historial.
    - Racha = 14 días significa que TODOS los últimos 14 días el paciente estuvo en alerta.
    - Racha = 0 significa que hoy está normal (fuera de alerta).
    """)

st.caption("Usa el menú de la izquierda para entrar al panel del Paciente o del Doctor.")