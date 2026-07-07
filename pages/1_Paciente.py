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
.badge-rojo     { background-color: rgba(239,68,68,0.15); color: #ef4444; }
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

# Única fuente de verdad: la misma función que usa el Panel Doctor.
# Devuelve "alerta", "atencion" o "estable" — nunca colores sueltos.
estado_semaforo = logica.calcular_estado_semaforo(promedio, tendencia, alerta)
clase_badge = (
    "badge-rojo" if estado_semaforo == "alerta"
    else "badge-amarillo" if estado_semaforo == "atencion"
    else "badge-verde"
)

# Pequeño helper para mostrar fechas como "24 jun" en vez de "2026-06-24".
# Usamos un diccionario en vez de librerías de localización, para que
# sea fácil de explicar en vivo con lo que hemos visto en el curso.
MESES = {"01": "ene", "02": "feb", "03": "mar", "04": "abr", "05": "may", "06": "jun",
         "07": "jul", "08": "ago", "09": "sep", "10": "oct", "11": "nov", "12": "dic"}

def formatear_fecha_corta(fecha_iso):
    partes = fecha_iso.split("-") #["2026", "06", "24"]
    return f"{partes[2]} {MESES[partes[1]]}"

fecha_inicio = formatear_fecha_corta(registros[0]["fecha"])
fecha_fin = formatear_fecha_corta(registros[-1]["fecha"])

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

# promedio, maximo y tendencia ya fueron calculados arriba a partir
# de st.session_state.registros_memoria (no recalculamos nada aquí).

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

#Botón para registrar

with st.form("form_glucosa", clear_on_submit=True):
    valor_nuevo = st.text_input("Valor de glucosa (mg/dL)")
    enviado = st.form_submit_button("Registrar")

if enviado:
    resultado = logica.validar_glucosa(valor_nuevo)
    if resultado["valido"]:
        from datetime import date
        nuevo_registro = {"fecha": str(date.today()), "valor": round(float(valor_nuevo), 2)}
        st.session_state.registros_memoria.append(nuevo_registro)
        st.success(resultado["mensaje"])
        st.rerun()
    else:
        st.error(resultado["mensaje"])

# --- Historial de glucosa (desplegable, justo debajo del formulario) ---

with st.expander("Ver historial de registros de glucosa"):
    df_glucosa = pd.DataFrame(st.session_state.registros_memoria)
    df_editado = st.data_editor(
        df_glucosa,
        column_config={
            "fecha": "Fecha",
            "valor": st.column_config.NumberColumn("Valor (mg/dL)", format="%.2f")
        },
        num_rows="fixed",  # solo editar valores existentes, no borrar ni agregar filas
        use_container_width=True,
        key="editor_glucosa"
    )

if st.button("Guardar cambios de glucosa"):
    registros_validados = []
    hay_error = False
    for i, fila in df_editado.iterrows():
        resultado = logica.validar_glucosa(str(fila["valor"]))
        if resultado["valido"]:
            registros_validados.append({
                "fecha": str(fila["fecha"]),
                "valor": round(float(fila["valor"]), 2)
            })
        else:
            st.error(f"Fila {i + 1}: {resultado['mensaje']}")
            hay_error = True
    
    if not hay_error:
            st.session_state.registros_memoria = registros_validados
            st.success("Cambios guardados correctamente.")
            st.rerun()


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

# --- Registrar nueva presión arterial ---

st.subheader("Registrar presión arterial")

with st.form("form_presion", clear_on_submit=True):
    col_sis, col_dia = st.columns(2)
    sistolica_nueva = col_sis.text_input("Sistólica (mmHg)")
    diastolica_nueva = col_dia.text_input("Diastólica (mmHg)")
    enviado_presion = st.form_submit_button("Registrar presión")

if enviado_presion:
    resultado = logica.validar_presion_arterial(sistolica_nueva, diastolica_nueva)
    if resultado["valido"]:
        nuevo_registro = {
            "fecha": str(date.today()),
            "sistolica": int(sistolica_nueva),
            "diastolica": int(diastolica_nueva)
        }
        st.session_state.presion_memoria.append(nuevo_registro)
        st.success(resultado["mensaje"])
        st.rerun()
    else:
        st.error(resultado["mensaje"])

with st.expander("Ver historial de presión arterial"):
    presion_para_mostrar = []
    for registro in st.session_state.presion_memoria:
        presion_para_mostrar.append({
            "fecha": registro["fecha"],
            "sistólica (mmHg)": registro["sistolica"],
            "diastólica (mmHg)": registro["diastolica"]
        })
    st.table(presion_para_mostrar)

 
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


# --- Registrar nueva oxigenación --- 
st.subheader("Registrar oxigenación")

with st.form("form_oxigenacion", clear_on_submit=True):
    spo2_nuevo = st.text_input("Oxigenación (%)")
    enviado_oxi = st.form_submit_button("Registrar oxigenación")

if enviado_oxi:
    resultado = logica.validar_oxigenacion(spo2_nuevo)
    if resultado["valido"]:
        nuevo_registro = {
            "fecha": str(date.today()),
            "valor": int(spo2_nuevo)
        }
        st.session_state.oxigenacion_memoria.append(nuevo_registro)
        st.success(resultado["mensaje"])
        st.rerun()
    else:
        st.error(resultado["mensaje"])

with st.expander("Ver historial de oxigenación"):
    df_oxi = pd.DataFrame(st.session_state.oxigenacion_memoria)
    df_oxi_editado = st.data_editor(
        df_oxi,
        column_config={
            "fecha": "Fecha",
            "valor": st.column_config.NumberColumn("SpO2 (%)")
        },
        num_rows="fixed",
        use_container_width=True,
        key="editor_oxigenacion"
    )

    if st.button("Guardar cambios de oxigenación"):
        registros_validados = []
        hay_error = False
        for i, fila in df_oxi_editado.iterrows():
            resultado = logica.validar_oxigenacion(fila["valor"])
            if resultado["valido"]:
                registros_validados.append({
                    "fecha": str(fila["fecha"]),
                    "valor": int(fila["valor"])
                })
            else:
                st.error(f"Fila {i + 1}: {resultado['mensaje']}")
                hay_error = True

        if not hay_error:
            st.session_state.oxigenacion_memoria = registros_validados
            st.success("Cambios guardados correctamente.")
            st.rerun()

# =========================================================================
# SECCIÓN 5: Registro de síntomas (adaptativo según semáforo)
# =========================================================================
# El registro SIEMPRE está disponible — los síntomas pueden aparecer aunque
# las métricas estén bien (mareo por otra causa, etc.). Lo que cambia es
# el tono y la prominencia visual según el estado del paciente.
# Reutilizamos estado_semaforo que ya fue calculado arriba con logica.py.

# Inicializamos la memoria de síntomas una sola vez.
if "sintomas_memoria" not in st.session_state:
    st.session_state.sintomas_memoria = []
    for sintoma_previo in paciente["otros_sintomas"]:
        st.session_state.sintomas_memoria.append({
            "fecha": "Previo",
            "sintomas": [sintoma_previo]
        })

# Lista predefinida de síntomas comunes en diabetes/hipertensión.
SINTOMAS_COMUNES = [
    "Dolor de cabeza",
    "Mareo",
    "Fatiga",
    "Visión borrosa",
    "Sed excesiva",
    "Temblores",
    "Sudoración",
    "Palpitaciones",
    "Náuseas",
    "Hormigueo en manos o pies"
]

# Función interna para dibujar el formulario. La usamos en las tres ramas
# para no repetir el código del multiselect, texto libre y botón.

def formulario_sintomas():
    with st.form("form_sintomas", clear_on_submit=True):
        sintomas_seleccionados = st.multiselect(
            "Marque los síntomas que está experimentando",
            options=SINTOMAS_COMUNES
        )
        otro_sintoma = st.text_input("¿Otro síntoma no listado? (opcional)")
        enviado_sintomas = st.form_submit_button("Registrar síntomas")

    if enviado_sintomas:
        if not sintomas_seleccionados and otro_sintoma.strip() == "":
            st.error("Por favor seleccione al menos un síntoma o escriba uno.")
        else:
            sintomas_de_hoy = list(sintomas_seleccionados)
            if otro_sintoma.strip() != "":
                sintomas_de_hoy.append(otro_sintoma.strip())

            nuevo_registro = {
                "fecha": str(date.today()),
                "sintomas": sintomas_de_hoy
            }
            st.session_state.sintomas_memoria.append(nuevo_registro)
            st.success("Síntomas registrados. Su doctora podrá verlos en su próxima revisión.")
            st.rerun()

# --- Presentación adaptativa según el semáforo ---
if estado_semaforo == "alerta":
    # Estado rojo: prominente, con banner destacado.
    st.markdown("""
    <div class="alerta-banner">
        🔔 Nos gustaría saber cómo se siente. Por favor, marque los síntomas que esté experimentando.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    formulario_sintomas()
    st.markdown('</div>', unsafe_allow_html=True)

elif estado_semaforo == "atencion":
    # Estado amarillo: visible, tono neutral.
    st.subheader("¿Cómo se siente hoy?")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    formulario_sintomas()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Estado verde/estable: discreto, dentro de un expander desplegable.
    with st.expander("¿Quiere reportar cómo se siente hoy? (opcional)"):
        formulario_sintomas()

# --- Historial de síntomas reportados (siempre visible) ---
with st.expander("Ver historial de síntomas"):
    sintomas_para_mostrar = []
    for registro in st.session_state.sintomas_memoria:
        sintomas_para_mostrar.append({
            "Fecha": registro["fecha"],
            "Síntomas Reportados": ", ".join(registro["sintomas"])
        })
    st.table(sintomas_para_mostrar)
