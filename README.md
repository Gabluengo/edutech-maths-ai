# 🎓 Edutech AI: Pearson Edexcel A-Level Math Tutor

Un prototipo de plataforma educativa nativa en IA diseñada para guiar a estudiantes a través del syllabus de **Pearson Edexcel International A-Level Mathematics**.

## 🚀 Estado del Proyecto: Semana 1 (Cimientos)
Actualmente, la plataforma cuenta con una arquitectura de datos jerárquica y una interfaz funcional para la navegación de contenidos.

### ✅ Logros Alcanzados
- **Estructura de Datos Pro:** Implementación en Supabase (PostgreSQL) con jerarquía de 4 niveles: *Curriculum > Units > Topics > Sub-topics*.
- **Navegación Dinámica:** Frontend en Streamlit que filtra contenidos en tiempo real desde la base de datos.
- **Modo Clase:** Interfaz dedicada para la interacción alumno-tutor por cada subtema.
- **Seguridad:** Gestión de credenciales mediante variables de entorno (`.env`) y control de versiones con Git.
- **Gobernanza:** Inclusión de `content_guidelines` en la base de datos para restringir y guiar el comportamiento de la IA.
- **Integración de LLM (Groq Cloud):** Implementación de Llama-3.3-70b-versatile como motor de tutoría.
- **System Prompt Dinámico:** Creación de una arquitectura que inyecta `content_guidelines` de Supabase en el contexto de la IA según el subtema seleccionado.
- **Gestión de Memoria:** Implementación de historial de conversación en `st.session_state` para mantener el hilo pedagógico.
- **Renderizado Matemático:** Soporte para fórmulas en formato LaTeX integrado en el chat.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.11
- **Web Framework:** Streamlit
- **Base de Datos:** Supabase (PostgreSQL)
- **Entorno:** Miniconda
- **IA (Próximamente):** Integración con LLMs vía LangChain / Groq.

## 📋 Requisitos Previos
- Entorno Conda activo.
- Archivo `.env` con `SUPABASE_URL` y `SUPABASE_KEY`.

---
*Este proyecto es parte de un plan de desarrollo de 12 semanas para crear un tutor de IA ético y pedagógicamente alineado.*
