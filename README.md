# 🩺 Vital Health Monitor

> Plataforma web donde los pacientes llevan una bitácora de su salud y el doctor da seguimiento remoto, relacionando los datos actuales con su historial — **sin necesidad de una cita presencial**.

Proyecto Final de *Fundamentos de la Programación*.

---

## 📖 ¿De qué trata?

- 🧑 **Los pacientes** registran su glucosa, presión arterial y oxigenación día a día.
- 🩺 **Los doctores** revisan las métricas, la alerta y la tendencia, y dejan una recomendación.

## 💡 El principio que nos guía

> **El sistema sugiere. El doctor aprueba y ajusta.**

La plataforma **nunca** automatiza una receta. Organiza la información y *sugiere*, pero siempre un profesional revisa, aprueba y decide. Así mantenemos a un humano responsable en cada decisión (resuelve la parte ética y legal).

---

## 🎯 La historia de la demo

> **Luis Fernando Carrasco**, paciente diabético, registra su glucosa día a día.
> La plataforma muestra la **evolución** en una gráfica con Altair.
> Su **doctora** detecta la **alerta** (los últimos días superan el límite de 130 mg/dL) y **ajusta el tratamiento a distancia**.

---

## 🛠️ Tecnologías

- **Python** — lenguaje principal
- **Streamlit** — framework web (interfaz en puro Python)
- **Altair** — gráficas de evolución
- Datos de ejemplo en un diccionario dentro de `logica.py`

---

## 🚀 Cómo ejecutar el proyecto

```bash
# 1. Clona el repositorio
git clone <URL-del-repositorio>
cd FINAL

# 2. Crea y activa un entorno virtual (Mac/Linux)
python3 -m venv venv
source venv/bin/activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Ejecuta la aplicación
streamlit run Inicio.py
```

Se abre solo en el navegador (normalmente `http://localhost:8501`) 🎉

---

## 📂 Estructura

- `Inicio.py` — portada de la app
- `pages/1_Paciente.py` — panel del paciente
- `pages/2_Doctor.py` — panel del doctor
- `logica.py` — toda la lógica (funciones de análisis y validación); corre sola por consola con `python logica.py`

---

## 👥 Equipo

- **Luis Roberto Ardón** — panel del paciente
- **Mariana Duarte** — panel del doctor

*(Ambos entienden y trabajan todo el código.)*

---

## ⚠️ Alcance

Prototipo académico de demostración. No es una aplicación médica real ni debe usarse para decisiones médicas verdaderas.