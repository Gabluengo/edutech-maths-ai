import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq # <--- Nueva importación
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 1. Configuración de la página y carga de secretos
load_dotenv()
st.set_page_config(page_title="AI Edexcel Math Tutor", layout="wide")

# 2. Conexión a Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# 3. Inicialización de la IA
llm = ChatGroq(
    temperature=0.2, # Baja temperatura para que sea preciso en matemáticas
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile" # Modelo potente para razonamiento
)

# 4. Funciones de Datos

def get_curriculums():
    return supabase.table("curriculums").select("*").execute().data

def get_units(curr_id):
    return supabase.table("units").select("*").eq("curriculum_id", curr_id).execute().data

def get_topics(unit_id):
    return supabase.table("topics").select("*").eq("unit_id", unit_id).order("order_index").execute().data

def get_sub_topics(topic_id):
    return supabase.table("sub_topics").select("*").eq("topic_id", topic_id).order("order_index").execute().data

def generate_system_prompt(sub_topic_name, guidelines):
    return f"""
    Eres un tutor experto en Matemáticas de Pearson Edexcel International A-Level.
    Tu objetivo es ayudar al estudiante a dominar el subtema: {sub_topic_name}.
    
    GUÍAS PEDAGÓGICAS ESPECÍFICAS (Síguelas estrictamente):
    {guidelines}
    
    INSTRUCCIONES DE COMPORTAMIENTO:
    1. Sé alentador pero riguroso con la notación matemática.
    2. Si el estudiante pide la respuesta, NO se la des directamente. Guíalo paso a paso con preguntas.
    3. Usa LaTeX para todas las fórmulas matemáticas (ej. $x^2 + 2x + 1$).
    4. Si el estudiante comete un error común mencionado en las guías, enfócate en corregir ese concepto.
    """

# 5. Interfaz de Usuario (Sidebar)
st.sidebar.title("📚 Edexcel Maths")
curriculums = get_curriculums()

if curriculums:
    curr_options = {f"{c['name']} - {c['level']}": c['id'] for c in curriculums}
    selected_curr_label = st.sidebar.selectbox("Curso:", list(curr_options.keys()))
    units = get_units(curr_options[selected_curr_label])
    
    if units:
        unit_options = {u['name']: u['id'] for u in units}
        selected_unit_label = st.sidebar.selectbox("Unidad:", list(unit_options.keys()))
        
        # Al cambiar de unidad, reseteamos el tema seleccionado
        if 'current_unit_id' not in st.session_state or st.session_state.current_unit_id != unit_options[selected_unit_label]:
            st.session_state.current_unit_id = unit_options[selected_unit_label]
            st.session_state.selected_sub_topic = None

# 6. Cuerpo Principal
# VISTA A: Si hay un subtema seleccionado -> MODO CLASE
if st.session_state.get('selected_sub_topic'):
    sub = st.session_state.selected_sub_topic
    
    if st.button("⬅ Volver al Syllabus"):
        st.session_state.selected_sub_topic = None
        st.session_state.messages = [] # Limpiar chat al salir
        st.rerun()

    st.title(f"Clase: {sub['name']}")
    
    # Inicializar historial de chat si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial de mensajes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input del usuario
    if prompt := st.chat_input("¿Qué parte de este tema quieres revisar?"):
        # 1. Guardar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Preparar el contexto para la IA
        # Incluimos el System Prompt + Historial + Nuevo mensaje
        system_content = generate_system_prompt(sub['name'], sub['content_guidelines'])
        
        messages_for_llm = [SystemMessage(content=system_content)]
        for m in st.session_state.messages:
            if m["role"] == "user":
                messages_for_llm.append(HumanMessage(content=m["content"]))
            else:
                messages_for_llm.append(AIMessage(content=m["content"]))

        # 3. Llamada a la IA
        with st.chat_message("assistant"):
            response = llm.invoke(messages_for_llm)
            full_response = response.content
            st.markdown(full_response)
        
        # 4. Guardar respuesta de la IA
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# VISTA B: Si hay una unidad seleccionada -> MOSTRAR TOPICS Y SUB_TOPICS
elif 'current_unit_id' in st.session_state:
    st.title(f"📖 {selected_unit_label}")
    
    # Herramientas rápidas
    cols = st.columns(3)
    cols[0].button("📝 Resumen Unidad")
    cols[1].button("🧪 Banco General")
    cols[2].button("📄 Past Papers")
    
    st.markdown("---")
    topics = get_topics(st.session_state.current_unit_id)
    
    for t in topics:
        st.subheader(f"{t['order_index']}. {t['name']}")
        sub_topics = get_sub_topics(t['id'])
        
        if sub_topics:
            for s in sub_topics:
                col_name, col_btn = st.columns([0.8, 0.2])
                col_name.write(f"  • {s['name']}")
                if col_btn.button("Entrar", key=s['id']):
                    st.session_state.selected_sub_topic = s
                    st.rerun()
        else:
            st.write("  *No hay subtemas cargados.*")

else:
    st.title("Bienvenido, Profesor")
    st.info("Seleccione un curso y unidad en el menú lateral para gestionar los contenidos.")

# 7. Lógica para mostrar contenido dinámico
if 'current_unit_id' in st.session_state:
    # Aquí es donde buscaremos los temas (topics) de esa unidad
    st.title(f"📖 {selected_unit_label}")
    
    # Próximo paso: Crear tabla de 'topics' y mostrarlos aquí
    st.write("Contenidos de la unidad:")
    
    # Simulación de botones de herramientas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📝 Ver Resumen")
    with col2:
        st.button("🧪 Banco de Ejercicios")
    with col3:
        st.button("📄 Past Papers")
        
    st.markdown("---")
    st.info("Haz clic en un subtema para iniciar la clase con la IA.")
else:
    st.title("Bienvenido, Profesor")
    st.write("Por favor, selecciona una unidad en el menú de la izquierda para comenzar.")