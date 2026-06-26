# 🩺 SaludSeguimiento

> Plataforma web que conecta a pacientes y doctores para dar seguimiento remoto a la salud, relacionando los síntomas actuales con el historial del paciente — **sin necesidad de una cita física**.

Proyecto Final de *Fundamentos de la Programación*.

---

## 📖 ¿De qué trata?

**NOMBRE POR DEFINIR** es una plataforma web donde:

- 🧑‍🦱 **Los pacientes** llevan una bitácora de su salud: registran síntomas, su intensidad y cómo evolucionan sus padecimientos (crónicos o nuevos).
- 🩺 **Los doctores** dan seguimiento remoto: revisan el historial del paciente, relacionan los síntomas actuales con registros pasados y ajustan el tratamiento a distancia.

La idea es facilitar el seguimiento continuo de cualquier padecimiento, de forma interactiva para ambas partes, sin que el paciente tenga que acudir presencialmente para cada revisión de rutina.

---

## 💡 El principio que nos guía

> **El sistema sugiere. El doctor aprueba y ajusta.**

La plataforma **nunca** automatiza una receta médica por su cuenta. Lo que hace es organizar la información y *sugerir*, pero siempre hay un profesional de la salud que revisa, aprueba y decide. Así mantenemos a un humano responsable en el centro de cada decisión, lo que resuelve la parte ética y legal del problema.

---

## ✨ Funcionalidades del prototipo

| Pantalla | Para quién | Qué permite hacer |
|---|---|---|
| 🔐 **Login** | Ambos | Ingresar con cuentas de ejemplo (paciente / doctor) |
| 📋 **Panel del paciente** | Paciente | Registrar síntomas y ver su propio historial |
| 👨‍⚕️ **Panel del doctor** | Doctor | Revisar al paciente y dejar una recomendación |
| 📈 **Historial** | Ambos | Ver la evolución de los síntomas en una gráfica |

---

## 🎯 La historia de la demo

> **Juan** es un paciente diabético. Registra sus niveles de glucosa día a día desde su panel.
> La plataforma muestra la **evolución** de esos valores en una gráfica.
> Su **doctora** detecta una alerta en la tendencia y **ajusta el tratamiento a distancia**, sin necesidad de una cita presencial.

Esta historia es el recorrido central que el prototipo demuestra de principio a fin.

---

## 🛠️ Tecnologías

- **[Python](https://www.python.org/)** — lenguaje principal
- **[Flask](https://flask.palletsprojects.com/)** — framework web
- **[SQLite](https://www.sqlite.org/)** — base de datos ligera con datos de ejemplo
- **[Bootstrap](https://getbootstrap.com/)** — diseño e interfaz
- **[Chart.js](https://www.chartjs.org/)** — gráficas de evolución

---

## 🚀 Cómo ejecutar el proyecto

Sigue estos pasos para correr la aplicación en tu computadora:

```bash
# 1. Clona el repositorio
git clone <URL-del-repositorio>

# 2. Entra a la carpeta del proyecto
cd <nombre-del-proyecto>

# 3. Crea un entorno virtual
python -m venv venv

# 4. Actívalo (Windows)
venv\Scripts\activate

# En Mac/Linux sería:
# source venv/bin/activate

# 5. Instala las dependencias
pip install -r requirements.txt

# 6. Ejecuta la aplicación
python app.py
```

Luego abre tu navegador en **http://127.0.0.1:5000** 🎉

> 💡 **Nota:** si trabajas dentro de una carpeta de OneDrive, conviene pausar la sincronización mientras creas el entorno virtual, para evitar que el proceso se interrumpa.

---

## 👥 Equipo

Proyecto desarrollado en pareja:

- **Luis Roberto Ardón** — Backend, rutas de Flask y datos de ejemplo
- **Mariana Duarte** — Diseño de pantallas (Bootstrap), gráfica y pitch

---

## ⚠️ Alcance del proyecto

Este es un **prototipo de demostración** con fines académicos, no una aplicación médica lista para producción. No cuenta con seguridad real ni debe usarse para decisiones médicas verdaderas. Su propósito es **demostrar el concepto** y acompañar un pitch de negocio.

---

<p align="center">
  Hecho con 💙 para el curso de Fundamentos de la Programación
</p>