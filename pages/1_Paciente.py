#pages/1_Paciente.py
#Panel de paciente (esqueleto)

import streamlit as st
import logica
import altair as alt
import pandas as pd
from datetime import date, datetime

st.set_page_config(page_title = "Paciente", page_icon = "👤")

# -----------------------------------------------------------------------
# ESTILOS (tarjetas oscuras, badge de semáforo, banner de alerta)
# Colores fijos a mano para que se vea igual sin depender del theme.
# -----------------------------------------------------------------------

st.markdown("""
<style>
.card {
    background-color: #262626;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 12px;
}
.metric-label { font-size: 13px; color: #a3a3a3; margin-bottom: 4px; }
.metric-value { font-size: 24px; font-weight: 600; }
.badge-semaforo {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 13px; font-weight: 500; padding: 6px 14px; border-radius: 999px;
}
.badge-amarillo { background-color: rgba(234,179,8,0.15); color: #eab308; }
.badge-verde    { background-color: rgba(34,197,94,0.15); color: #22c55e; }
.alerta-banner {
    background-color: rgba(153,27,27,0.55); border-radius: 10px;
    padding: 14px 18px; color: #fecaca; font-size: 14px; margin-bottom: 20px;
}
.avatar-circle {
    width: 44px; height: 44px; border-radius: 50%;
    background-color: rgba(59,130,246,0.2); color: #60a5fa;
    display: flex; align-items: center; justify-content: center;
    font-weight: 600; font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- Obtenemos los datos del paciente Luis Fernando (ID 1) ---
paciente = logica.pacientes_db[1]    #Accedemos al diccionario y sacamos al paciente con clave [1]

# --- Memoria: igual que antes, inicializamos una sola vez ---
if "registros_memoria" not in st.session_state:
    st.session_state.registros_memoria = list(paciente["registros_glucosa"])

if "presion_memoria" not in st.session_state:
    st.session_state.presion_memoria = list(paciente["presion_arterial"])

if "oxigenacion_memoria" not in st.session_state:
    st.session_state.oxigenacion_memoria = list(paciente["oxigenacion"])

registros = st.session_state.registros_memoria
registros_presion = st.session_state.presion_memoria
registros_oxigenacion = st.session_state.oxigenacion_memoria

# -----------------------------------------------------------------------
# CÁLCULOS reales con logica.py (nada se recalcula aquí)
# -----------------------------------------------------------------------

promedio = logica.calcular_promedio_glucosa(registros)
maximo = logica.encontrar_glucosa_maxima(registros)
tendencia = logica.detectar_tendencia(registros)
alerta = logica.generar_alerta(registros)
hay_alerta = alerta.startswith("ALERTA")

estado_semaforo = "amarillo" if hay_alerta else "verde"
clase_badge = "badge-amarillo" if hay_alerta else "badge-verde"


# Pequeño helper para mostrar fechas como "24 jun" en vez de "2026-06-24".
# Usamos un diccionario en vez de librerías de localización, para que
# sea fácil de explicar en vivo con lo que hemos visto en el curso.
MESES = {"01": "ene", "02": "feb", "03": "mar", "04": "abr", "05": "may", "06": "jun",
         "07": "jul", "08": "ago", "09": "sep", "10": "oct", "11": "nov", "12": "dic"}

def formatear_fecha_corta(fecha_iso):
    partes = fecha_iso.split("-") #["2026", "06", "24"]
    return f"{partes[2]} {MESES[partes[1]]}"

fecha_inicio = formatear_fecha_corta(registros[0]["fecha"])
fecha_fin = formatear_fecha_corta(registros[1]["fecha"])

# Inciales para el avatar: primera letra del primer y último nombre
partes_nombre = paciente["nombre"].split()
iniciales = (partes_nombre[0][0] + partes_nombre[-1][0]).upper()

# últimos valores de presión y oxigenación (ya existen en pacientes_db)
ultima_presion = paciente["presion_arterial"][-1]
ultima_oxigenacion = paciente["oxigenacion"][-1]
glucosa_actual = registros[-1]["valor"]

# -----------------------------------------------------------------------
# ENCABEZADO
# -----------------------------------------------------------------------
col_izq, col_der = st.columns([3, 1])
with col_izq:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px;">
        <div class="avatar-circle">{iniciales}</div>
        <div>
            <p style="font-weight:600; font-size:17px; margin:0;">Hola, {partes_nombre[0]} {partes_nombre[1] if len(partes_nombre) > 1 else ''}</p>
            <p style="font-size:13px; color:#a3a3a3; margin:0;">Seguimiento del {fecha_inicio} – {fecha_fin}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_der:
    st.markdown(f"""
    <div style="text-align:right;">
        <span class="badge-semaforo {clase_badge}">Semáforo: {estado_semaforo}</span>
    </div>
    """, unsafe_allow_html=True)
 
st.write("")

 
# -----------------------------------------------------------------------
# BANNER DE ALERTA — usa el mensaje real de generar_alerta, sin inventar texto
# -----------------------------------------------------------------------
if hay_alerta:
    st.markdown(f"""
    <div class="alerta-banner">
        🔔 {alerta}
    </div>
    """, unsafe_allow_html=True)
 

# -----------------------------------------------------------------------
# TARJETAS DE MÉTRICAS (glucosa actual, última presión, última oxigenación)
# -----------------------------------------------------------------------

c1, c2, c3 = st.columns(3)
with c1:
    color_glucosa = "#eab308" if hay_alerta else "#e5e5e5"
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Glucosa</div>
        <div class="metric-value" style="color:{color_glucosa};">{glucosa_actual} <span style="font-size:13px; color:#a3a3a3;">mg/dL</span></div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Presión</div>
        <div class="metric-value">{ultima_presion["sistolica"]}/{ultima_presion["diastolica"]}</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Oxigenación</div>
        <div class="metric-value">{ultima_oxigenacion["valor"]} <span style="font-size:13px; color:#a3a3a3;">%</span></div>
    </div>
    """, unsafe_allow_html=True)

# Mostramos el historial médico recorriendo la lista con un ciclo for

st.subheader("Historial médico")
for condicion in paciente["historial_medico"]:
    st.write("-", condicion)

# --- SECCIÓN 2: Resumen de glucosa (cifras clave) ---
st.subheader("Resumen de glucosa")

# Sacamos la lista de registros de glucosa del paciente
registros = paciente["registros_glucosa"]

# Usamos la memoria como fuente de datos
registros = st.session_state.registros_memoria  # Reasignamos "registros" para que se almacene en memoria

# Usamos NUESTRAS funciones de logica.py para calcular cada dato
promedio = logica.calcular_promedio_glucosa(registros)
maximo = logica.encontrar_glucosa_maxima(registros)
tendencia = logica.detectar_tendencia(registros)

# st.columns crea columnas para poner las métricas lado a lado
col1, col2, col3 = st.columns(3)

col1.metric("Promedio", f"{round(promedio, 2)} mg/dL")
col2.metric("Máximo", f"{maximo} mg/dL")
col3.metric("Tendencia", tendencia)


# --- SECCIÓN 3: Gráfica de evolución ---

st.subheader("Evolución de la glucosa")

# Armamos una lista de diccionarios (fecha + valor) recorriendo los
# registros con un for. Altair necesita los datos en este formato

datos_grafica = []
for registro in registros:
    datos_grafica.append({
        "Fecha": registro["fecha"],
        "Glucosa": registro["valor"]
    })

# Construimos la gráfica de línea con Altair.
grafica = alt.Chart(alt.Data(values=datos_grafica)).mark_line(point=True).encode(
    x = alt.X("Fecha:N", title="Fecha"),
    y = alt.Y("Glucosa:Q", title="Glucosa (mg/dL)",
              scale=alt.Scale(domain=[100,180]))
).properties(height=300)

# Linea roja horizontal en el límite de alerta (130)
linea_limite = (
    alt.Chart(pd.DataFrame({"limite": [130]}))
    .mark_rule(color="red", strokeDash=[4, 4])
    .encode(y="limite:Q")
)

# Combinar ambas capas 
grafica_final = grafica + linea_limite

st.altair_chart(grafica_final, use_container_width=True)

# --- SECCIÓN 4: Registrar nueva glucosa (con validación) ---
st.subheader("Registrar nueva glucosa")


# Campo de texto para que el usuario escriba el valor
valor_nuevo = st.text_input("Valor de glucosa (mg/dL)")

#Botón para registrar
if st.button("Registrar"):
    #Usamos NUESTRA función validar_glucosa de logica.py
    resultado = logica.validar_glucosa(valor_nuevo)

    if resultado["valido"]:
        #Si es válido, lo agregamos a la memoria con la fecha de hoy
        from datetime import date
        nuevo_registro = {"fecha": str(date.today()), "valor": round(float(valor_nuevo), 2)}
        st.session_state.registros_memoria.append(nuevo_registro)
        st.success(resultado["mensaje"])
        st.rerun() # vuelve a ejecutar todo para que la gráfica y métricas se actualicen
    else:
        #Si no es válido, mostramos el mensaje de error de la función
        st.error(resultado["mensaje"])


# =========================================================================
# PRESIÓN ARTERIAL — resumen + evolución (mismo patrón que glucosa)
# =========================================================================
st.subheader("Resumen de presión arterial")
 
promedio_presion = logica.calcular_promedio_presion(registros_presion)
maxima_presion = logica.encontrar_presion_maxima(registros_presion)
tendencia_presion = logica.detectar_tendencia_presion(registros_presion)
 
col1, col2, col3 = st.columns(3)
col1.metric("Promedio", f"{promedio_presion['sistolica']}/{promedio_presion['diastolica']} mmHg")
col2.metric("Máximo", f"{maxima_presion['sistolica']}/{maxima_presion['diastolica']} mmHg")
col3.metric("Tendencia", tendencia_presion)
 
st.subheader("Evolución de la presión arterial")
datos_grafica_presion = [{"Fecha": r["fecha"], "Sistólica": r["sistolica"]} for r in registros_presion]
 
grafica_presion = alt.Chart(alt.Data(values=datos_grafica_presion)).mark_line(point=True).encode(
    x=alt.X("Fecha:N", title="Fecha"),
    y=alt.Y("Sistólica:Q", title="Sistólica (mmHg)", scale=alt.Scale(domain=[100, 170]))
).properties(height=300)
 
linea_limite_presion = (
    alt.Chart(pd.DataFrame({"limite": [140]}))
    .mark_rule(color="red", strokeDash=[4, 4])
    .encode(y="limite:Q")
)
st.altair_chart(grafica_presion + linea_limite_presion, use_container_width=True)
 
# =========================================================================
# OXIGENACIÓN — resumen + evolución (mismo patrón, umbral hacia abajo)
# =========================================================================
st.subheader("Resumen de oxigenación")
 
promedio_oxi = logica.calcular_promedio_glucosa(registros_oxigenacion)  # reutilizada: promedia "valor"
minima_oxi = logica.encontrar_oxigenacion_minima(registros_oxigenacion)
tendencia_oxi = logica.detectar_tendencia(registros_oxigenacion)  # reutilizada: mismo formato de registro
 
col1, col2, col3 = st.columns(3)
col1.metric("Promedio", f"{promedio_oxi} %")
col2.metric("Mínimo", f"{minima_oxi} %")
col3.metric("Tendencia", tendencia_oxi)
 
st.subheader("Evolución de la oxigenación")
datos_grafica_oxi = [{"Fecha": r["fecha"], "Oxigenación": r["valor"]} for r in registros_oxigenacion]
 
grafica_oxi = alt.Chart(alt.Data(values=datos_grafica_oxi)).mark_line(point=True, color="#f59e0b").encode(
    x=alt.X("Fecha:N", title="Fecha"),
    y=alt.Y("Oxigenación:Q", title="SpO2 (%)", scale=alt.Scale(domain=[85, 100]))
).properties(height=300)
 
linea_limite_oxi = (
    alt.Chart(pd.DataFrame({"limite": [92]}))
    .mark_rule(color="orange", strokeDash=[4, 4])
    .encode(y="limite:Q")
)
st.altair_chart(grafica_oxi + linea_limite_oxi, use_container_width=True)







# --- SECCIÓN 5: Tabla de registros ---
st.subheader("Historial de registros")

# Creamos una versión "para mostrar" de los registros, con los valores
# formateados a exactamente 2 decimales como texto. 

#Recorremos la memoria con un for y armamos una lista nueva, sin 
# modificar los datos originales guardados en session_state.

registros_para_mostrar = []
for registro in st.session_state.registros_memoria:
    registros_para_mostrar.append({
        "fecha": registro["fecha"],
        "valor (mg/dL)": f"{registro["valor"]:.2f}"
    })

st.table(registros_para_mostrar)