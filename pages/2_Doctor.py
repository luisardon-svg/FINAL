#pages/2_Doctor.py
#Panel del doctor

import streamlit as st
import logica
import altair as alt

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
#LEEMOS la misma memoria de la pag del paciente
#los registros nuevos también estarán actualizados
#si paciente aun no ha abierto su pag, iniciamos con registros originales
if "registros_mempria" not in st.session_state:
    st.session_state.registros_memoria = list(paciente["registros_glucosa"])
registros = st.session_state.registros_memoria

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

st.divider()

#SECCION #: Alerta
# generar_alerta (logica.py) decide el mensaje segun el promedio
alerta = logica.generar_alerta(registros)

st.subheader("Estado del paciente")
#si el mensaje contiene "ALERTA", lo mostramos en rojo (st.error)
# si no, en verde (st.success)
if "ALERTA" in alerta: 
    st.error(f"**{alerta}**")
else: 
    st.success(f"{alerta}")

st.divider()

#SECCION 4: Evolucion de glucosa
st.subheader("Evolucion de glucosa")

#Lista de datos (fecha + valor) recorriendo los registros con un for
#altair necesita los datos en ese formaato (igual que en la pagina del paciente). 
datos_grafica = []
for registro in registros: 
    datos_grafica.append({
        "Fecha": registro["fecha"],
        "Glucosa": registro["valor"]
        })

#Linea de evolucion (mismo estilo que la pagina del paciente)
grafica = alt.Chart(alt.Data(values=datos_grafica)).mark_line(point=True).encode(
    x=alt.X("Fecha:N", title="Fecha"),
y=alt.Y("Glucosa:Q", title="Glucosa (mg/dL)",
            scale=alt.Scale(domain=[100,180]))
).properties(height=300)

#linea roja del LIMITE (130), reusando la constante de logica.py
limite = alt.Chart(
    alt.Data(values=[{"Glucosa": logica.GLUCOSA_LIMITE_ALTA}])
).mark_rule(color="red", strokeDash=[6,4]).encode(
    y="Glucosa:Q"
)

#Superponemos capas
grafica_final = grafica + limite

st.altair_chart(grafica_final, use_container_width=True)
st.caption(f"La linea roja marca el limite de {logica.GLUCOSA_LIMITE_ALTA} mg/dL. Las lecturas por encima disparan la alerta.")