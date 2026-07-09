"""
En este archivo se encuentra la lógica principal del proyecto

Aqui se encuentran: estructuras de datos, funciones de análsis de síntomas y validanciones. 
El archivo app.py (Flask) importa estas funciones para mostrar los resultados en la web.

Este módulo también puede ejecutarse solo desde la consola para probar
que las funciones funcionan, usando el bloque if __name__ == "__main__"
"""

# Importamos una librería estándar: datetime nos sirve para trabajar
# con las fechas de cada registro de síntomas
from datetime import datetime
from dotenv import load_dotenv
load_dotenv() #Lee el archivo .env y carga sus variables al entorno

# ---------------------------------------------------------------------
# ESTRUCTURAS DE DATOS (diccionarios y listas)
# ---------------------------------------------------------------------
# Usamos un diccionario para guardar a los pacientes organizados por su
# ID (la clave). Cada paciente es a su vez un diccionario con sus datos.
# El historial médico es una lista de texto, y los registros de glucosa
# son una lista de diccionarios (fecha + valor).

pacientes_db = {
    1: {
        "nombre": "Luis Fernando Carrasco",
        "edad": 60, 
        "es_cronico": True, #booleano: padecimiento crónico (sí)
        # Lista con el historial médico de fondo del paceinte.
        "historial_medico": [
            "Infarto hace 3 años",
            "Hipertensión arterial (HTA)",
            "Diabetes",
            "Intolerante al gluten",
            "Alérgico a mariscos"
        ],
        # Registros de glucosa de los últimos 5 días (en mg/dL).
        # Esta es la métrica principal que analizamos para la demo.

        "registros_glucosa": [
            {"fecha": "2026-06-24", "valor": 145},
            {"fecha": "2026-06-25", "valor": 152},
            {"fecha": "2026-06-26", "valor": 148},
            {"fecha": "2026-06-27", "valor": 160},
            {"fecha": "2026-06-28", "valor": 155},
            {"fecha": "2026-06-29", "valor": 158},
            {"fecha": "2026-06-30", "valor": 162},
            {"fecha": "2026-07-01", "valor": 150},
            {"fecha": "2026-07-02", "valor": 145},
            {"fecha": "2026-07-03", "valor": 148},
            {"fecha": "2026-07-04", "valor": 152},
            {"fecha": "2026-07-05", "valor": 156},
            {"fecha": "2026-07-06", "valor": 160},
            {"fecha": "2026-07-07", "valor": 165},
        ],
        
        "presion_arterial": [
            {"fecha": "2026-06-24", "sistolica": 138, "diastolica": 86},
            {"fecha": "2026-06-25", "sistolica": 142, "diastolica": 88},
            {"fecha": "2026-06-26", "sistolica": 140, "diastolica": 87},
            {"fecha": "2026-06-27", "sistolica": 148, "diastolica": 91},
            {"fecha": "2026-06-28", "sistolica": 145, "diastolica": 90},
            {"fecha": "2026-06-29", "sistolica": 150, "diastolica": 92},
            {"fecha": "2026-06-30", "sistolica": 154, "diastolica": 95},
            {"fecha": "2026-07-01", "sistolica": 147, "diastolica": 91},
            {"fecha": "2026-07-02", "sistolica": 142, "diastolica": 88},
            {"fecha": "2026-07-03", "sistolica": 136, "diastolica": 85},
            {"fecha": "2026-07-04", "sistolica": 130, "diastolica": 83},
            {"fecha": "2026-07-05", "sistolica": 126, "diastolica": 81},
            {"fecha": "2026-07-06", "sistolica": 122, "diastolica": 79},
            {"fecha": "2026-07-07", "sistolica": 118, "diastolica": 77},
        ],

        "oxigenacion": [
            {"fecha": "2026-06-24", "valor": 97},
            {"fecha": "2026-06-25", "valor": 96},
            {"fecha": "2026-06-26", "valor": 96},
            {"fecha": "2026-06-27", "valor": 95},
            {"fecha": "2026-06-28", "valor": 95},
            {"fecha": "2026-06-29", "valor": 94},
            {"fecha": "2026-06-30", "valor": 93},
            {"fecha": "2026-07-01", "valor": 94},
            {"fecha": "2026-07-02", "valor": 95},
            {"fecha": "2026-07-03", "valor": 96},
            {"fecha": "2026-07-04", "valor": 96},
            {"fecha": "2026-07-05", "valor": 97},
            {"fecha": "2026-07-06", "valor": 97},
            {"fecha": "2026-07-07", "valor": 98},
        ],

        "chequeos_previos": [
            "Electrocardiograma - 15 marzo 2026 - Normal",
            "Análisis de sangre - 02 mayo 2026 - Glucosa elevada",
        ],

        # Otros síntomas que el paciente reporta (contexto extra)
        "otros_sintomas": ["Fatiga leve", "Mareos ocasionales"]

    }
}

# Rango de referencia para la glucosa en ayunas (valores orientativos).
# Por encima de este límite consideramos que la glucosa es elevada
GLUCOSA_LIMITE_ALTA = 130

# ---------------------------------------------------------------------
# FUNCIÓN 1: calcular el promedio de glucosa
# ---------------------------------------------------------------------

def calcular_promedio_glucosa(registros):
    """
    Recibe una lista de registros (diccionarios) y devuelve el promedio
    de los valores de glucosa.
 
    Demuestra: parámetros, return, condicional (if), ciclo for, listas.
    """
    # Condicional: si la lista está vacía, evitamos dividir entre cero.
    if len(registros) == 0:
        return 0
    
    suma = 0
    # Ciclo for: recorremos cada registro y sumamos su valor de glucosa
    for registro in registros:
        suma = suma + registro["valor"]

    promedio = suma / len(registros)
    return round(promedio, 2)

# ---------------------------------------------------------------------
# FUNCIÓN 2: encontrar el valor de glucosa más alto registrado
# ---------------------------------------------------------------------
def encontrar_glucosa_maxima(registros):
    """
    Recibe la lista de registros y devuelve el valor de glucosa más alto.
 
    Demuestra: parámetros, return, ciclo while, condicional, listas.
    """
    if len(registros) == 0:
        return 0
 
    maxima = registros[0]["valor"]   #Empieza en el primer valor 
    indice = 1
    # Ciclo while: recorremos la lista hasta llegar al final.
    while indice < len(registros):
        if registros[indice]["valor"] > maxima:
            maxima = registros[indice]["valor"]
        indice = indice + 1
 
    return maxima


# ---------------------------------------------------------------------
# FUNCIÓN 3: detectar la tendencia (¿sube, baja o se mantiene?)
# ---------------------------------------------------------------------
def detectar_tendencia(registros):
    """
    Compara el primer y el último registro para decir si la glucosa
    va subiendo, bajando o se mantiene estable.
 
    Demuestra: parámetros, return, condicionales if/elif/else, listas.
    """
    # Necesitamos al menos dos registros para comparar.
    if len(registros) < 2:
        return "No hay suficientes datos para una tendencia"
 
    primero = registros[0]["valor"]
    ultimo = registros[-1]["valor"]  #Es -1 para tomar el último valor de la lista, ya que es una lista cerrada.
 
    # Condicional con if / elif / else: la decisión "de verdad".
    if ultimo > primero:
        return "Subiendo"
    elif ultimo < primero:
        return "Bajando"
    else:
        return "Estable"
    
# ---------------------------------------------------------------------
# FUNCIÓN 4: generar una alerta si la glucosa promedio está elevada
# ---------------------------------------------------------------------

def generar_alerta(registros):
    """
    Revisa el promedio de glucosa de los registros MÁS RECIENTES (los
    últimos 5) y devuelve un mensaje de alerta si supera el límite.
    Usar solo los últimos registros refleja mejor el estado actual del
    paciente que promediar todo el historial completo.

    Demuestra: parámetros, return, condicional, slicing de listas,
    y uso de otra función.
    """
    registros_recientes = registros[-5:] #Slicing de listas    # El [-5] acorta la lista a los últimos 5 datos

    promedio_reciente = calcular_promedio_glucosa(registros_recientes)

    # Condicional: comparamos el promedio contra el límite
    if promedio_reciente > GLUCOSA_LIMITE_ALTA:
        return "ALERTA: glucosa promedio elevada. Revisar tratamiento."
    else:
        return "Glucosa promedio dentro de rango."
    
# ---------------------------------------------------------------------
# FUNCIÓN 5: validar un valor de glucosa escrito por el usuario
# ---------------------------------------------------------------------

def validar_glucosa(valor_texto):
    """
    Revisa lo que el usuario escribió al registrar una glucosa nueva.
    Devuelve un diccionario con dos claves:
    - "valido": True or False
    - "mensaje": explicación de por qué es válido o no
    
    Demuestra: parámetros , return, condicionales if/elif/else,
    validación de la entrada del usuario, y manejo de un caso de error.
    """

    # Límites de lo que consideramos una glucosa humana realista (mg/dL)
    GLUCOSA_MINIMA = 20
    GLUCOSA_MAXIMA = 600

    # 1) Que no esté vacío. strip() quita espacios en blanco a los lados;
    # si al quitarlos no queda nada, el usuario no escribió un valor real.

    if valor_texto is None or valor_texto.strip() == "":
        return {"valido": False, "mensaje": "El valor no puede estar vacío."}
    
    # 2) Que sea un número. Intentamos convertir el texto a número decimal.
    # Si no puede (por ejemplo escribió "abc"), Python lanza un error
    # que atrapamos con try/except y devolvemos un mensaje claro.

    try:
        valor = float(valor_texto)
    except ValueError:
        return {"valido": False, "mensaje": "El valor debe ser un número."}
    
    # 3) Que esté dentro del rango razonable (20 a 600 mg/dL).
    if valor < GLUCOSA_MINIMA:
        return {"valido": False, "mensaje": "El valor es demasiado bajo (mínimo 20)."}
    elif valor > GLUCOSA_MAXIMA:
        return {"valido": False, "mensaje": "El valor es demasiado alto (máximo 600)."}
    else:
        # Si pasó las tres pruebas, es un valor válido.
        return {"valido": True, "mensaje": "Valor de glucosa válido."}
    

# ---------------------------------------------------------------------
# FUNCIÓN 6: validación de presión arterial
# ---------------------------------------------------------------------

def validar_presion_arterial(sistolica, diastolica):
    """
    Revisa una lectura de presión arterial.
    Devuelve un diccionario con "valido" (bool) y "mensaje" (str).
    """
    try:                                  #Conversión segura a un número entero con try / except (la presión solo acepta números enteros)
        sistolica = int(sistolica)  
        diastolica = int(diastolica)
    except (ValueError, TypeError):         #Se conoce como "defensive programming" #Si el usuario mete algún dato erróneo que no sea un número, el sistema no truena
        return {"valido": False, "mensaje": "La presión arterial debe ser un número entero."}
    
    if sistolica <= diastolica:
        return {"valido": False, "mensaje": "La sistólica debe ser mayor que la diastólica."}
    
    if not (70 <= sistolica <= 200):
        return {"valido": False, "mensaje": "La sistólica debe estar entre 70 y 200 mmHg."}
    
    if not (40 <= diastolica <= 130):
        return {"valido": False, "mensaje": "La diastólica debe estar entre 40 y 130 mmHg."}
    
    return {"valido": True, "mensaje": "Presión arterial válida."}

# ---------------------------------------------------------------------
# FUNCIÓN 7: validación de oxigenación
# ---------------------------------------------------------------------

def validar_oxigenacion(spo2):
    """
    Revisa un valor de saturación de oxígeno (SpO2).
    Devuelve un diccionario con "valido" (bool) y "mensaje" (str).
    """

    try:
        spo2 = int(spo2)
    except (ValueError, TypeError):
        return {"valido": False, "mensaje": "La oxigenación debe ser un número entero."}


    if not (70 <= spo2 <= 100):
        return {"valido": False, "mensaje": "La oxigenación debe estar entre 70 y 100%."}

    return {"valido": True, "mensaje": "Oxigenación válida."}

# ---------------------------------------------------------------------
# FUNCIÓN 8: promedio de presión sistólica y diastólica
# ---------------------------------------------------------------------
def calcular_promedio_presion(registros):
    """
    Recibe la lista de registros de presión arterial y devuelve un
    diccionario con el promedio de la sistólica y de la diastólica.
 
    Demuestra: parámetros, return, ciclo for, condicional, listas, diccionarios.
    """
    if len(registros) == 0:
        return {"sistolica": 0, "diastolica": 0}
 
    suma_sistolica = 0
    suma_diastolica = 0
    for registro in registros:
        suma_sistolica = suma_sistolica + registro["sistolica"]
        suma_diastolica = suma_diastolica + registro["diastolica"]
 
    promedio_sistolica = suma_sistolica / len(registros)
    promedio_diastolica = suma_diastolica / len(registros)
 
    return {
        "sistolica": round(promedio_sistolica, 2),
        "diastolica": round(promedio_diastolica, 2),
    }
 
 
# ---------------------------------------------------------------------
# FUNCIÓN 9: registro con la sistólica más alta
# ---------------------------------------------------------------------
def encontrar_presion_maxima(registros):
    """
    Recorre los registros de presión y devuelve el registro completo
    (sistólica + diastólica) donde la sistólica fue más alta.
 
    Demuestra: parámetros, return, ciclo while, condicional, listas.
    """
    if len(registros) == 0:                          #Solo si el paciente no tiene registros
        return {"sistolica": 0, "diastolica": 0}
 
    maximo = registros[0]         #Asume que el primer registro es el máximo
    indice = 1                     #Prepara un índice para recorrer desde el segundo registro

    while indice < len(registros):                               #En cada vuelta compara la sistólica del registro actual contra la sistólica del "máximo" guardado hasta ahora
        if registros[indice]["sistolica"] > maximo["sistolica"]:   #Si el actual es mayor, maximo se actualiza para apuntar a ese registro completo
            maximo = registros[indice]
        indice = indice + 1                                       #Avanza en el contador
 
    return maximo
 
 
# ---------------------------------------------------------------------
# FUNCIÓN 10: tendencia de la presión sistólica
# ---------------------------------------------------------------------
def detectar_tendencia_presion(registros):
    """
    Compara la sistólica del primer y el último registro.
 
    Demuestra: parámetros, return, condicionales if/elif/else, listas.
    """
    if len(registros) < 2:
        return "No hay suficientes datos para una tendencia"
 
    primero = registros[0]["sistolica"]
    ultimo = registros[-1]["sistolica"]
 
    if ultimo > primero:
        return "Subiendo"
    elif ultimo < primero:
        return "Bajando"
    else:
        return "Estable"
 
 
# ---------------------------------------------------------------------
# FUNCIÓN 11: alerta de presión arterial elevada
# ---------------------------------------------------------------------
PRESION_SISTOLICA_LIMITE = 140
 
def generar_alerta_presion(registros):
    """
    Revisa el promedio de la sistólica de los últimos 5 registros
    y devuelve un mensaje de alerta si supera el límite.
 
    Demuestra: parámetros, return, condicional, slicing, uso de otra función.
    """
    registros_recientes = registros[-5:]
    promedio_reciente = calcular_promedio_presion(registros_recientes)
 
    if promedio_reciente["sistolica"] > PRESION_SISTOLICA_LIMITE:
        return "ALERTA: presión arterial elevada. Revisar tratamiento."
    else:
        return "Presión arterial dentro de rango."
 
 
# ---------------------------------------------------------------------
# FUNCIÓN 12: valor mínimo de oxigenación registrado
# ---------------------------------------------------------------------
def encontrar_oxigenacion_minima(registros):
    """
    Recorre los registros de oxigenación y devuelve el valor más bajo.
    A diferencia de la glucosa, aquí lo que importa es el mínimo, no
    el máximo: una oxigenación baja es la señal de alerta.
 
    Demuestra: parámetros, return, ciclo while, condicional, listas.
    """
    if len(registros) == 0:
        return 0
 
    minima = registros[0]["valor"]
    indice = 1
    while indice < len(registros):
        if registros[indice]["valor"] < minima:
            minima = registros[indice]["valor"]
        indice = indice + 1
 
    return minima
 
 
# ---------------------------------------------------------------------
# FUNCIÓN 13: alerta de oxigenación baja
# ---------------------------------------------------------------------
OXIGENACION_LIMITE_BAJA = 92
 
def generar_alerta_oxigenacion(registros):
    """
    Revisa el promedio de oxigenación de los últimos 5 registros y
    devuelve un mensaje de alerta si está por debajo del límite.
 
    Reutiliza calcular_promedio_glucosa porque los registros de
    oxigenación usan la misma llave "valor" que los de glucosa.
 
    Demuestra: parámetros, return, condicional, slicing, uso de otra función.
    """
    registros_recientes = registros[-5:]
    promedio_reciente = calcular_promedio_glucosa(registros_recientes)
 
    if promedio_reciente < OXIGENACION_LIMITE_BAJA:
        return "ALERTA: oxigenación baja. Revisar paciente."
    else:
        return "Oxigenación dentro de rango."


# ---------------------------------------------------------------------
# FUNCIÓN 14: calcular el estado tipo "semáforo" del paciente
# ---------------------------------------------------------------------
def calcular_estado_semaforo(promedio, tendencia, alerta):
    if "ALERTA" in alerta:
        return "alerta"
    elif tendencia == "Subiendo":
        return "atencion"
    else: 
        return "estable"
# ---------------------------------------------------------------------
# FUNCIÓN 15: generar un resumen clínico en texto (versión local)
# ---------------------------------------------------------------------
def generar_resumen_clinico(datos_paciente, registros):
    nombre = datos_paciente["nombre"]
    edad = datos_paciente["edad"]

    promedio = calcular_promedio_glucosa(registros)
    maxima =encontrar_glucosa_maxima(registros)
    tendencia = detectar_tendencia(registros)
    alerta = generar_alerta(registros)
    estado = calcular_estado_semaforo(promedio, tendencia, alerta)
    racha = calcular_racha_dias_alerta(registros)

    resumen = (
        f"Paciente: {nombre}, {edad} años.\n"
        f"Glucosa promedio: {promedio} mg/dL (máxima: {maxima} mg/dL).\n"
        f"Tendencia: {tendencia}. Estado general: {estado}.\n"
        f"Racha de días en alerta: {racha}.\n"
        f"Observación: {alerta}"
    )
    return resumen     

# ---------------------------------------------------------------------
# FUNCIÓN 16: generar la recomendación sugerida (para PR 5 - fase 7)
# ---------------------------------------------------------------------
def generar_recomendacion_sugerida(estado_semaforo, promedio_glucosa, tendencia_glucosa):
    """
    Genera una recomendación automática basada en el estado del semáforo.
    Devuelve el diccionario recomendacion_doctor con estado inicial
    "pendiente", listo para que el doctor lo apruebe, edite o rechace.
    """
    if estado_semaforo == "alerta":
        texto = (
            f"El paciente presenta niveles de glucosa elevados "
            f"(promedio {promedio_glucosa} mg/dL, tendencia {tendencia_glucosa}). "
            f"Se recomienda ajustar el tratamiento actual y agendar una consulta "
            f"de seguimiento en los próximos 3 días."
        )
    elif estado_semaforo == "atencion":
        texto = (
            f"El paciente muestra valores en zona de atención "
            f"(promedio {promedio_glucosa} mg/dL, tendencia {tendencia_glucosa}). "
            f"Se recomienda reforzar el monitoreo y revisar hábitos alimenticios."
        )
    else:
        texto = (
            f"El paciente se encuentra estable "
            f"(promedio {promedio_glucosa} mg/dL). "
            f"Se recomienda mantener el plan actual y continuar el monitoreo regular."
        )

    return {
        "texto": texto,
        "estado": "pendiente",
        "editado_por_doctor": False,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

# ---------------------------------------------------------------------
# FUNCIÓN 17: racha de días consecutivos en alerta (RECURSIVA)
# ---------------------------------------------------------------------

def calcular_racha_dias_alerta(registros, posicion=None):
    """
    Cuenta cuántos días consecutivos, empezando por el más reciente y
    yendo hacia atrás, el paciente registró glucosa por encima del
    límite (GLUCOSA_LIMITE_ALTA). En cuanto encuentra un día SIN alerta,
    la racha se corta ahí.

    Caso base: no quedan registros que revisar (posicion < 0), o el día
    actual NO está en alerta -> la racha termina, devolvemos 0.
    Caso recursivo: el día actual SÍ está en alerta -> devolvemos
    1 (por este día) + la racha de todos los días anteriores.

    Demuestra: recursión, parámetro con valor por defecto, condicional.
    """
    #Primera llamada: sin posición indicada, empezamos por el último registro (el más reciente)

    if posicion is None:
        posicion = len(registros) - 1
    
    #Caso base 1: ya no hay más días que revisar hacia atrás.
    if posicion < 0:
        return 0

    dia_en_alerta = registros[posicion]["valor"] > GLUCOSA_LIMITE_ALTA

    #Caso base 2: este día no está en alerta -> la racha se corta aquí.
    if not dia_en_alerta:
        return 0

    #Caso recursivo: cuento este día + lo que diga la racha del día anterior
    return 1 + calcular_racha_dias_alerta(registros, posicion - 1)


# ---------------------------------------------------------------------
# FUNCIÓN 18: racha de días consecutivos en alerta — presión arterial
# ---------------------------------------------------------------------

def calcular_racha_dias_alerta_presion(registros, posicion=None):
    """
    Misma lógica que calcular_racha_dias_alerta, pero para presión:
    cuenta días consecutivos (desde el más reciente) donde la sistólica
    superó PRESION_SISTOLICA_LIMITE.
    """
    if posicion is None:
        posicion = len(registros) - 1

    if posicion < 0:
        return 0

    dia_en_alerta = registros[posicion]["sistolica"] > PRESION_SISTOLICA_LIMITE

    if not dia_en_alerta:
        return 0

    return 1 + calcular_racha_dias_alerta_presion(registros, posicion - 1)

# ---------------------------------------------------------------------
# FUNCIÓN 19: racha de días consecutivos en alerta — oxigenación
# ---------------------------------------------------------------------

def calcular_racha_dias_alerta_oxigenacion(registros, posicion=None):
    """
    Misma lógica, pero invertida: aquí la alerta es cuando el valor está
    POR DEBAJO del límite (una oxigenación baja es la señal de riesgo,
    a diferencia de glucosa y presión donde el riesgo es un valor alto).
    """
    if posicion is None:
        posicion = len(registros) - 1

    if posicion < 0:
        return 0

    dia_en_alerta = registros[posicion]["valor"] < OXIGENACION_LIMITE_BAJA

    if not dia_en_alerta:
        return 0

    return 1 + calcular_racha_dias_alerta_oxigenacion(registros, posicion - 1)


# ---------------------------------------------------------------------
# FUNCIÓN 20: API GEMINI
# ---------------------------------------------------------------------

def generar_recomendacion_ia(paciente, promedio_glucosa, tendencia_glucosa, estado_semaforo):
    """
    Genera una recomendación usando la API de Gemini (capa OPCIONAL).
    El sistema SUGIERE; el doctor siempre revisa y aprueba.
    Si algo falla (sin internet, sin key, error de API), devuelve un
    mensaje de respaldo para que la app nunca se rompa en la demo.
    """
    import os
    from google import genai

    # La key se lee de la variable de entorno, nunca se escribe en el código.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ No se encontró la API key de Gemini. Usa la sugerencia del sistema."

    try:
        cliente = genai.Client(api_key=api_key)

        # Armamos el prompt con los datos reales del paciente.
        prompt = (
            f"Eres un asistente médico de apoyo. NO prescribes de forma definitiva; "
            f"solo sugieres para que un DOCTOR humano revise y apruebe.\n\n"
            f"Paciente: {paciente['nombre']}, {paciente['edad']} años.\n"
            f"Historial: {', '.join(paciente['historial_medico'])}.\n"
            f"Glucosa promedio: {promedio_glucosa} mg/dL. "
            f"Tendencia: {tendencia_glucosa}. Estado general: {estado_semaforo}.\n\n"
            f"Redacta una recomendación breve (máximo 3 frases) para que el doctor "
            f"la revise. Termina recordando que la decisión final es del médico."
        )

        respuesta = cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return respuesta.text

    except Exception as error:
        # Si la API falla por cualquier razón, la app no se cae.
        return f"⚠️ No se pudo generar el análisis con IA ({error}). Usa la sugerencia del sistema."

# ---------------------------------------------------------------------
# BLOQUE DE PRUEBA POR CONSOLA
# ---------------------------------------------------------------------
# Este bloque solo se ejecuta si corremos "python logica.py" directamente.
# Si app.py importa este archivo, este bloque NO se ejecuta.
# Sirve para demostrar que la lógica funciona sin necesidad de la web.
if __name__ == "__main__":
    print("=== Prueba de la lógica de SaludSeguimiento ===\n")
 
    # Tomamos los datos del paciente Luis Fernando (ID 1) del diccionario.
    paciente = pacientes_db[1]
    registros = paciente["registros_glucosa"]
 
    print("Paciente:", paciente["nombre"])
    print("Edad:", paciente["edad"])
    print()
 
    # Ciclo for para mostrar el historial médico (recorrer una lista).
    print("Historial médico:")
    for condicion in paciente["historial_medico"]:
        print("  -", condicion)
    print()
 
    print("Registros de glucosa (mg/dL):")
    for registro in registros:
        print("  ", registro["fecha"], "->", registro["valor"])
    print()
 
    promedio = calcular_promedio_glucosa(registros)
    print("Promedio de glucosa:", promedio, "mg/dL")
 
    maxima = encontrar_glucosa_maxima(registros)
    print("Glucosa máxima registrada:", maxima, "mg/dL")
 
    tendencia = detectar_tendencia(registros)
    print("Tendencia:", tendencia)
 
    alerta = generar_alerta(registros)
    print("Estado:", alerta)

    # --- Prueba de la validación de datos del usuario ---
    print()
    print("=== Prueba de validación de glucosa ===")
    valores_prueba = ["155", "", "abc", "10", "700"]
    
    # Ciclo for: recorremos varios valores de ejemplo y los validamos.
    for valor in valores_prueba:
        resultado = validar_glucosa(valor)
        print("Entrada:", repr(valor), "->", resultado["mensaje"])

 # --- Pruebas de validar_presion_arterial ---
    print("\n--- Pruebas: validar_presion_arterial ---")
    print(validar_presion_arterial(120, 80))     # (True, "")
    print(validar_presion_arterial(80, 120))     # (False, "sistólica debe ser mayor...")
    print(validar_presion_arterial(250, 90))     # (False, "sistólica fuera de rango")
    print(validar_presion_arterial(120, 20))     # (False, "diastólica fuera de rango")
    print(validar_presion_arterial("abc", 80))   # (False, "debe ser un número entero")

    # --- Pruebas de validar_oxigenacion ---
    print("\n--- Pruebas: validar_oxigenacion ---")
    print(validar_oxigenacion(96))    # (True, "")
    print(validar_oxigenacion(65))    # (False, "fuera de rango")
    print(validar_oxigenacion(101))   # (False, "fuera de rango")
    print(validar_oxigenacion("xyz")) # (False, "debe ser un número entero")
    estado = calcular_estado_semaforo(promedio, tendencia, alerta)
    print("Estado (semaforo):", estado)
    print("\n--- Resumen clínico ---")
    print(generar_resumen_clinico(paciente, registros))