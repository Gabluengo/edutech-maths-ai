import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

# 1. Configuración de la página y carga de secretos
load_dotenv()
st.set_page_config(page_title="AI Edexcel Math Tutor", layout="wide")

# 2. Conexión a Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# 3. Funciones de Datos

def get_curriculums():
    return supabase.table("curriculums").select("*").execute().data

def get_units(curr_id):
    return supabase.table("units").select("*").eq("curriculum_id", curr_id).execute().data

def get_topics(unit_id):
    return supabase.table("topics").select("*").eq("unit_id", unit_id).order("order_index").execute().data

def get_sub_topics(topic_id):
    return supabase.table("sub_topics").select("*").eq("topic_id", topic_id).order("order_index").execute().data

# 4. Interfaz de Usuario (Sidebar)
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

# 4. Cuerpo Principal
# VISTA A: Si hay un subtema seleccionado -> MODO CLASE
if st.session_state.get('selected_sub_topic'):
    sub = st.session_state.selected_sub_topic
    
    if st.button("⬅ Volver al Syllabus"):
        st.session_state.selected_sub_topic = None
        st.rerun()

    st.title(f"Clase: {sub['name']}")
    
    with st.expander("🎯 Objetivos de aprendizaje"):
        st.write(sub['content_guidelines'])
    
    # Aquí irá el Agente IA
    st.chat_message("assistant").write(f"Hola. Vamos a trabajar en **{sub['name']}**. Basado en el syllabus de Edexcel, ¿quieres que repasemos la teoría o prefieres que te proponga un ejercicio de desarrollo?")
    st.chat_input("Escribe tu duda o sube una imagen del ejercicio...")

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

# Lógica para mostrar contenido dinámico
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