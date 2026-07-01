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

# ---------------------------------------------------------------------
# ESTRUCTURAS DE DATOS (diccionarios y listas)
# ---------------------------------------------------------------------
# Usamos un diccionario para guardar a los pacientes organizados por su
# ID (la clave). Cada paciente es a su vez un diccionario con sus datos.
# El historial médico es una lista de texto, y los registros de glucosa
# son una lista de diccionarios (fecha + valor).

pacientes_db = {
    1: {
        "nombre": "Luis Fernado Carrasco",
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
        ],
        # Otros síntomas que el paciente reporta (contexto extra)
        "otros_sintomas": ["Fatiga leve", "Mareos ocasionales"]

    }
}

# Rango de referencia para la glucosa en ayunas (valores orientativos).
# Por encima de este límite consideramos que la glucosa
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
 
    maxima = registros[0]["valor"]
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
    ultimo = registros[-1]["valor"]
 
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
    Revisa el promedio de glucosa y devuelve un mensaje de alerta para
    el doctor si supera el límite considerado normal.
 
    Demuestra: parámetros, return, condicional, uso de otra función,
    y una constante. Esta es la lógica que la doctora ve en su panel.
    """
    
    promedio = calcular_promedio_glucosa(registros)

    # Condicional: comparamos el promedio contra el límite
    if promedio > GLUCOSA_LIMITE_ALTA:
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