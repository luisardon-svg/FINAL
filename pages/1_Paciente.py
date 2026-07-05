#pages/1_Paciente.py
#Panel de paciente (esqueleto)

import streamlit as st
import logica
import altair as alt
import pandas as pd

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

# --- SECCIÓN 2: Resumen de glucosa (cifras clave) ---
st.subheader("Resumen de glucosa")

# Sacamos la lista de registros de glucosa del paciente
registros = paciente["registros_glucosa"]

# Inicializamos la memoria una sola vez con los registros originales.
# A partir de aquí, TODO (métricas, gráfica) lee de esta memoria.

if "registros_memoria" not in st.session_state:
    st.session_state.registros_memoria = list(registros)

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