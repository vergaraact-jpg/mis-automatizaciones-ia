import streamlit as st
from google import genai
from google.genai import types

# Configuración de la página web
st.set_page_config(page_title="Asistente de Productividad IA", page_icon="⚡", layout="centered")

# Título de la Web
st.title("⚡ Tu Asistente de Productividad con IA")
st.write("Automatizaciones diarias para ahorrar tiempo y organizar tu día.")

# Barra lateral para ingresar la API Key
st.sidebar.header("🔑 Configuración")
api_key = st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password")
st.sidebar.markdown("---")
st.sidebar.info("Esta web procesa tus solicitudes usando IA en tiempo real.")

if not api_key:
    st.warning("👈 Por favor, introduce tu API Key de Gemini en la barra lateral para comenzar.")
    st.stop()

# Inicializar cliente de Gemini
client = genai.Client(api_key=api_key)

# Crear pestañas para las dos herramientas
tab1, tab2 = st.tabs(["📝 Lector Express (Resumidor)", "🎙️ Voz a Tarea / Evento"])

# --- PESTAÑA 1: RESUMIDOR ---
with tab1:
    st.header("Resumidor Express de Texto")
    st.write("Pega un texto largo, correo o información de un artículo para extraer lo más importante al instante.")
    
    texto_entrada = st.text_area("Pega tu texto aquí:", height=200, placeholder="Pega el contenido del artículo, correo o documento...")
    
    if st.button("🚀 Generar Resumen", type="primary"):
        if not texto_entrada.strip():
            st.error("Por favor, pega algún texto antes de continuar.")
        else:
            with st.spinner("Analizando contenido..."):
                prompt = f"""
                Analiza el siguiente texto y proporciona:
                1. 📌 **Idea Principal** (en 1 frase impactante).
                2. 🔑 **3 Puntos Clave** (en viñetas claras).
                3. 💡 **Conclusión o Acción sugerida**.

                Texto:
                {texto_entrada}
                """
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                st.success("¡Resumen completado!")
                st.markdown(response.text)

# --- PESTAÑA 2: VOZ A TAREA ---
with tab2:
    st.header("Organizador de Notas de Voz")
    st.write("Graba un audio diciendo lo que tienes que hacer (ej: *'Mañana a las 4pm reunión con Carlos'*).")
    
    audio_val = st.audio_input("🔴 Graba tu nota de voz:")
    
    if audio_val:
        if st.button("✨ Procesar Audio y Crear Tarea"):
            with st.spinner("Escuchando y estructurando la información..."):
                audio_bytes = audio_val.read()
                
                prompt_audio = """
                Escucha atentamente esta nota de voz y extrae la información en este formato estructurado y visual:
                
                📌 **Título de la Tarea/Evento:** [Nombre claro y corto]
                📅 **Fecha y Hora detectada:** [Si se menciona, si no pon 'No especificada']
                📝 **Detalles/Descripción:** [Resumen breve de la acción requerida]
                🏷️ **Categoría sugerida:** [Trabajo / Personal / Recordatorio / Urgente]
                """
                
                response_audio = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        prompt_audio,
                        types.Part.from_bytes(
                            data=audio_bytes,
                            mime_type=audio_val.type,
                        )
                    ]
                )
                st.success("¡Nota procesada correctamente!")
                st.markdown(response_audio.text)
