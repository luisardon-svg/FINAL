#pages/2_Doctor.py
#Panel del doctor

import streamlit as st
import logica
import altair as alt

st.set_page_config(page_title = "Doctor", page_icon = "🩺")

paciente = logica.pacientes_db[1]

st.title(" 👩‍⚕️ ¡Bienvenida Dra. Sofía Mendoza García!")
# ============================================
# INFORMACIÓN DE LA DOCTORA
# Se muestra justo debajo del título del panel
# ============================================
st.markdown("""
<div style="
    background-color: rgba(255, 255, 255, 0.05);
    border-left: 4px solid #4da3ff;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 24px;
    font-size: 15px;
    color: #fafafa;
">
    <div style="font-size: 16px; font-weight: 600; color: #4da3ff; margin-bottom: 8px;">
        📋 Datos básicos
    </div>
    <div style="line-height: 1.9;">
        ├─ <strong>Especialidades:</strong> Medicina Interna + Endocrinología<br>
        ├─ <strong>Cédula:</strong> 45-123456<br>
        ├─ <strong>Hospital/Clínica:</strong> Centro Médico "La Paz"<br>
        ├─ <strong>Experiencia:</strong> 15 años<br>
        └─ <strong>Teléfono:</strong> +502 7777-1234
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

#Datos básicos del paciente
st.title(" 🩺 Paciente:")
st.header(paciente["nombre"])
st.write(f"**Edad:** {paciente['edad']} años")

#Historial medico: recorremos la lista con un ciclo for
st.subheader("Historial médico")
for condicion in paciente["historial_medico"]:
    st.write("- " + condicion)

st.divider()

#SECCION ": Metricas de glucosa
# lista de registro de paciente 
#LEEMOS la misma memoria de la pag del paciente
#los registros nuevos también estarán actualizados
#si paciente aun no ha abierto su pag, iniciamos con registros originales
if "registros_memoria" not in st.session_state:
    st.session_state.registros_memoria = list(paciente["registros_glucosa"])
registros = st.session_state.registros_memoria

#Los tres calculos vienen de funciones de logica.py
promedio = logica.calcular_promedio_glucosa(registros)
maxima = logica.encontrar_glucosa_maxima(registros)
tendencia = logica.detectar_tendencia(registros)



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
#Semaforo de estado general
estado = logica.calcular_estado_semaforo(promedio, tendencia, alerta)

st.subheader("Estado general del paciente")

if estado == "alerta":
    st.error("🔴 ALERTA — requiere atención inmediata")
elif estado == "atencion":
    st.warning("🟡 ATENCIÓN — vigilar de cerca")
else: 
    st.success("🟢 ESTABLE — dentro de lo esperado")



# --- Capa opcional: análisis generado por IA (Gemini) ---
if st.button("🤖 Generar análisis con IA (opcional)"):
    with st.spinner("Consultando a Gemini..."):
        analisis_ia = logica.generar_recomendacion_ia(
            paciente=paciente,
            promedio_glucosa=promedio,
            tendencia_glucosa=tendencia,
            estado_semaforo=estado
        )
    # Guardamos el resultado en session_state para que no se pierda al re-renderizar
    st.session_state.analisis_ia = analisis_ia

# Si ya se generó un análisis con IA, lo mostramos
if "analisis_ia" in st.session_state:
    st.markdown("**🤖 Análisis generado por IA (para revisión del doctor):**")
    st.write(st.session_state.analisis_ia)

st.divider() 

#resumen clinico
# generar_resumen_clinico (logica.py) arma el texto con f-strings,
# reutilizando promedio, tendencia, alerta y semaforo.
st.subheader("Resumen clínico")

resumen = logica.generar_resumen_clinico(paciente, registros)
st.text(resumen)

# Métricas de glucosa
st.subheader("Métricas de glucosa")

racha = logica.calcular_racha_dias_alerta(registros)

# Cuadrícula 2x2 en vez de 1 fila de 4 — cada métrica tiene más espacio
# horizontal, evitando que los valores se corten con "..."

col1, col2 = st.columns(2)
col1.metric("Promedio", f"{promedio} mg/dL")
col2.metric("Maxima", f"{maxima} mg/dL")

col3, col4 = st.columns(2)
col3.metric("Tendencia", tendencia)
col4.metric("Racha en alerta", f"{racha} días")

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

if "ALERTA" in alerta:
    st.error(f"**{alerta}**")
else: 
    st.success(f"{alerta}")
    


#SECCION: Presion arterial
#LEEMOS LA MEMORIA COMPARTIDA (O DE PACIENTE_DB COMO RESPALDO).
if "presion_memoria" not in st.session_state: 
    st.session_state.presion_memoria = list(paciente["presion_arterial"])
registros_presion = st.session_state.presion_memoria

promedio_presion = logica.calcular_promedio_presion(registros_presion)
maxima_presion = logica.encontrar_presion_maxima(registros_presion)
tendencia_presion = logica.detectar_tendencia_presion(registros_presion)
alerta_presion = logica.generar_alerta_presion(registros_presion)

st.subheader("Presión arterial")

racha_presion = logica.calcular_racha_dias_alerta_presion(registros_presion)

col1, col2 = st.columns(2)
col1.metric("Promedio", f"{promedio_presion['sistolica']}/{promedio_presion['diastolica']} mmHg")
col2.metric("Máxima", f"{maxima_presion['sistolica']}/{maxima_presion['diastolica']} mmHg")

col3, col4 = st.columns(2)
col3.metric("Tendencia", tendencia_presion)
col4.metric("Racha en alerta", f"{racha_presion} días")

#Alerta de presión (mismo patrón que la glucosa)
if "ALERTA" in alerta_presion: 
    st.error(f"**{alerta_presion}**")
else:
    st.success(alerta_presion)

# Gráfica de evolución de la sistólica, con línea roja en el límite (140)
datos_presion = []
for r in registros_presion:
    datos_presion.append({"Fecha": r["fecha"], "sistolica": r["sistolica"]})

grafica_presion = alt.Chart(alt.Data(values=datos_presion)).mark_line(point=True).encode(
    x=alt.X("Fecha:N", title="Fecha"),
    y=alt.Y("sistolica:Q", title="Sistólica (mmHg)", scale=alt.Scale(domain=[100, 170]))
).properties(height=300)

limite_presion = alt.Chart(
    alt.Data(values=[{"sistolica": logica.PRESION_SISTOLICA_LIMITE}])
).mark_rule(color="red", strokeDash=[6, 4]).encode(y="sistolica:Q")

st.altair_chart(grafica_presion + limite_presion, use_container_width=True)

#SECCION: Oxigenación (sp=2)
# Leemos de la memoria compartida (o del pacientes_db como respaldo). 
if "oxigenacion_memoria" not in st.session_state:
    st.session_state.oxigenacion_memoria = list(paciente["oxigenacion"])
registros_oxi = st.session_state.oxigenacion_memoria

#Cálculos con las funciones de logica.py
promedio_oxi = logica.calcular_promedio_glucosa(registros_oxi) #calcula "valor"
minima_oxi = logica.encontrar_oxigenacion_minima(registros_oxi)
tendencia_oxi = logica.detectar_tendencia(registros_oxi)
alerta_oxi = logica.generar_alerta_oxigenacion(registros_oxi)

st. subheader("Oxigenacion (SpO2)")

racha_oxi = logica.calcular_racha_dias_alerta_oxigenacion(registros_oxi)

col1, col2 = st.columns(2)
col1.metric("Promedio", f"{promedio_oxi} %")
col2.metric("Mínimo", f"{minima_oxi} %")

col3, col4 = st.columns(2)
col3.metric("Tendencia", tendencia_oxi)
col4.metric("Racha en alerta", f"{racha_oxi} días")

#Alerta de oxigenación (mismo patrón que glucosa y presión)
if "ALERTA" in alerta_oxi:
    st.error(f"**{alerta_oxi}**")
else:
    st.success(alerta_oxi)

#Gráfica de evolución, con línea naranja en el límite (92 - threshhold bajo)
datos_oxi = []
for r in registros_oxi: 
    datos_oxi.append({"Fecha": r["fecha"], "spo2": r["valor"]})

grafica_oxi = alt.Chart(alt.Data(values=datos_oxi)).mark_line(point=True, color="#f59e0b").encode(
    x=alt.X("Fecha:N", title="Fecha"),
    y=alt.Y("spo2:Q", title="SpO2 (%)", scale=alt.Scale(domain=[85, 100]))
).properties(height=300)

limite_oxi = alt.Chart(
    alt.Data(values=[{"spo2": logica.OXIGENACION_LIMITE_BAJA}])
).mark_rule(color="orange", strokeDash=[6, 4]).encode(y="spo2:Q")

st.altair_chart(grafica_oxi + limite_oxi, use_container_width=True)

st.divider()

st.divider()

# =========================================================================
# SECCIÓN: Síntomas reportados por el paciente
# =========================================================================
# Leemos la misma memoria compartida que usa el Panel Paciente.
# Si el paciente aún no ha abierto su panel, iniciamos con lo que ya
# existe en pacientes_db (chequeos previos guardados como "otros_sintomas").
if "sintomas_memoria" not in st.session_state:
    st.session_state.sintomas_memoria = []
    for sintoma_previo in paciente["otros_sintomas"]:
        st.session_state.sintomas_memoria.append({
            "fecha": "Previo",
            "sintomas": [sintoma_previo]
        })

st.subheader("Síntomas reportados por el paciente")

if len(st.session_state.sintomas_memoria) == 0:
    st.info("El paciente no ha reportado síntomas.")
else:
    # Mostramos el más reciente destacado, y el resto en una tabla desplegable.
    ultimo_registro = st.session_state.sintomas_memoria[-1]
    st.warning(
        f"**Último reporte ({ultimo_registro['fecha']}):** "
        f"{', '.join(ultimo_registro['sintomas'])}"
    )

    with st.expander("Ver historial completo de síntomas"):
        sintomas_para_mostrar = []
        for registro in st.session_state.sintomas_memoria:
            sintomas_para_mostrar.append({
                "fecha": registro["fecha"],
                "síntomas reportados": ", ".join(registro["sintomas"])
            })
        st.table(sintomas_para_mostrar)


# =========================================================================
# SECCIÓN: Análisis sugerido (tarjeta con botones Aprobar / Editar / Rechazar)
# =========================================================================
# El sistema SUGIERE (generar_recomendacion_sugerida), el doctor APRUEBA.
# Este es el corazón ético del proyecto: nunca se automatiza la receta.
st.subheader("Análisis sugerido")

# Inicializamos el estado de la recomendación una sola vez.
if "recomendacion_doctor" not in st.session_state:
    st.session_state.recomendacion_doctor = None
if "editando_recomendacion" not in st.session_state:
    st.session_state.editando_recomendacion = False

# El sistema genera la sugerencia a partir del estado del semáforo.
recomendacion_sugerida = logica.generar_recomendacion_sugerida(
    estado_semaforo=estado,
    promedio_glucosa=promedio,
    tendencia_glucosa=tendencia
)




# ORDEN DE PRIORIDAD DE LOS ESTADOS (importante):
# 1º edición  →  2º ya hay decisión guardada  →  3º primera vez (sin decisión)
# El modo edición va primero porque, al activarlo, recomendacion_doctor
# puede seguir siendo None y no queremos caer en la rama de "primera vez".

if st.session_state.editando_recomendacion:
    # --- Modo edición: el doctor modifica el texto antes de aprobar ---
    st.warning("📝 Editando recomendación")

    # Si ya había un texto guardado, partimos de él; si no, del sugerido.
    if st.session_state.recomendacion_doctor is not None:
        texto_base = st.session_state.recomendacion_doctor["texto"]
    else:
        texto_base = recomendacion_sugerida["texto"]

    texto_editado = st.text_area("Modifica la recomendación:", value=texto_base, height=120)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Guardar cambios"):
            st.session_state.recomendacion_doctor = {
                "texto": texto_editado,
                "estado": "pendiente",
                "editado_por_doctor": True,
                "fecha": recomendacion_sugerida["fecha"]
            }
            st.session_state.editando_recomendacion = False
            st.success("Cambios guardados. Ahora puedes aprobar la recomendación editada.")
            st.rerun()
    with col2:
        if st.button("❌ Cancelar edición"):
            st.session_state.editando_recomendacion = False
            st.rerun()

elif st.session_state.recomendacion_doctor is not None:
    # --- Ya hay una decisión guardada: mostramos su estado ---
    rec = st.session_state.recomendacion_doctor

    if rec["estado"] == "aprobada":
        st.success(f"✅ **Aprobada:** {rec['texto']}")
        if rec["editado_por_doctor"]:
            st.caption("✏️ Esta recomendación fue editada por el doctor.")
        if st.button("↩️ Reconsiderar"):
            st.session_state.recomendacion_doctor = None
            st.rerun()

    elif rec["estado"] == "rechazada":
        st.error(f"❌ **Rechazada:** {rec['texto']}")
        if st.button("↩️ Reconsiderar"):
            st.session_state.recomendacion_doctor = None
            st.rerun()

    elif rec["estado"] == "pendiente":
        st.warning(f"⏳ **Pendiente de aprobación:** {rec['texto']}")
        if rec["editado_por_doctor"]:
            st.caption("✏️ Texto editado por el doctor, listo para aprobar.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Aprobar"):
                st.session_state.recomendacion_doctor["estado"] = "aprobada"
                st.success("Recomendación aprobada y enviada al paciente.")
                st.rerun()
        with col2:
            if st.button("❌ Rechazar"):
                st.session_state.recomendacion_doctor["estado"] = "rechazada"
                st.info("Recomendación rechazada.")
                st.rerun()

else:
    # --- Primera vez: no hay decisión todavía. Mostramos la sugerencia + 3 botones ---
    st.info(f"💡 **Sugerencia del sistema:** {recomendacion_sugerida['texto']}")

   

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Aprobar sugerencia"):
            st.session_state.recomendacion_doctor = {
                "texto": recomendacion_sugerida["texto"],
                "estado": "aprobada",
                "editado_por_doctor": False,
                "fecha": recomendacion_sugerida["fecha"]
            }
            st.success("Sugerencia aprobada y enviada al paciente.")
            st.rerun()
    with col2:
        if st.button("✏️ Editar antes de aprobar"):
            st.session_state.editando_recomendacion = True
            st.rerun()
    with col3:
        if st.button("❌ Rechazar sugerencia"):
            st.session_state.recomendacion_doctor = {
                "texto": recomendacion_sugerida["texto"],
                "estado": "rechazada",
                "editado_por_doctor": False,
                "fecha": recomendacion_sugerida["fecha"]
            }
            st.info("Sugerencia rechazada.")
            st.rerun()