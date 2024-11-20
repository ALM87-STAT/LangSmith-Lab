import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
API_URL = os.getenv("API_URL")
API_URL_FEEDBACK = os.getenv("API_URL_FEEDBACK")

# Valores por defecto
DEFAULT_CONTEXT = """
**1. Propósito del Proyecto**\n
StreamWorld es una plataforma digital de entretenimiento diseñada para ofrecer acceso ilimitado a una amplia gama de contenido audiovisual, incluyendo películas, series, documentales, y producciones exclusivas. El proyecto tiene como objetivo satisfacer la creciente demanda de contenido digital, brindando a los usuarios una experiencia personalizada y accesible en cualquier momento y lugar.

**2. Público Objetivo**\n
El proyecto está orientado a un público diverso, que incluye tanto a usuarios jóvenes como adultos, aficionados al entretenimiento en casa. StreamWorld se dirige a consumidores que valoran la accesibilidad, la calidad de imagen y sonido, y la disponibilidad de contenido variado y actualizado. Los segmentos de usuarios clave incluyen:
   - Adultos jóvenes (18-35 años) interesados en contenido original y tendencias culturales.
   - Familias que buscan una alternativa segura y variada para disfrutar en casa.
   - Amantes de géneros específicos (como ciencia ficción, acción, y drama) que desean explorar un catálogo completo.

**3. Características Principales**
   - **Biblioteca de Contenido Extensa**: Miles de títulos en diversos géneros, incluyendo producciones de cine clásico, populares, y lanzamientos recientes.
   - **Contenido Original y Exclusivo**: Producciones propias que diferencian la plataforma de la competencia, atrayendo y fidelizando a suscriptores.
   - **Recomendaciones Personalizadas**: Un sistema de IA avanzado que sugiere contenido en función del historial de visualización y preferencias del usuario.
   - **Multiplataforma**: Disponibilidad en diversos dispositivos (smartphones, tabletas, computadoras y televisores inteligentes).
   - **Interactividad y Socialización**: Funcionalidades como listas compartidas, reseñas de usuarios, y la posibilidad de ver contenido en grupo con amigos.
   - **Calidad de Imagen y Sonido**: Opciones de reproducción en HD, 4K y sonido Dolby para una experiencia cinematográfica en casa.
   - **Descargas para Modo Offline**: Posibilidad de descargar contenido para verlo sin conexión, especialmente útil para usuarios en áreas de baja conectividad.

**4. Objetivos de Negocio**
   - **Fidelización del Usuario**: Incrementar la retención y lealtad de usuarios mediante una experiencia de usuario de alta calidad y contenido exclusivo.
   - **Aumento de Ingresos**: Generar ingresos mediante suscripciones mensuales y anuales, con distintos niveles de precio según la calidad y funcionalidades.
   - **Expansión de Mercado**: Crecer en mercados emergentes y ofrecer contenido localizado para adaptarse a los intereses culturales de distintas regiones.
   - **Innovación Continua**: Invertir en nuevas tecnologías, como recomendaciones de IA y mejoras en la transmisión, para mantener la plataforma competitiva y atractiva.

**5. Análisis de Mercado y Competencia**\n
El mercado de plataformas de streaming es altamente competitivo, dominado por empresas como Netflix, Disney+, y HBO Max. La clave para diferenciar a StreamWorld será su enfoque en contenido original que refleje las tendencias y demandas locales, así como su sistema de recomendaciones hiper-personalizado, una interfaz intuitiva y un servicio de atención al cliente eficiente. Además, el proyecto buscará aprovechar alianzas estratégicas con productoras locales y festivales de cine para ofrecer contenido exclusivo y de alta calidad.
"""

DEFAULT_REQUIREMENTS = "Necesito una historia de usuario para el proceso de suscripción al servicio premium. Los usuarios deben poder elegir el plan de pago, proporcionar detalles de pago y confirmar su suscripción."

# --------- Streamlit ---------#

st.set_page_config(page_title="📝 Building Block AI")
st.title("📝 Building Block AI")

# Inicializar el estado de la sesión para la respuesta si no existe
if "generated_response" not in st.session_state:
    st.session_state.generated_response = None

# Inicializar el estado de la sesión para feedback
if "feedback_sent" not in st.session_state:
    st.session_state.feedback_sent = False

# --------- Sidebar ---------#

# Agregar campo de contexto en la barra lateral
st.sidebar.title("Contexto")
context = st.sidebar.text_area(
    "Ingrese el contexto del proyecto:",
    value=st.session_state.get("context", ""),
    key="context_input",
)

with st.sidebar:
    st.markdown("## Ejemplo de Contexto" + "\n" + DEFAULT_CONTEXT)

# --------- response ---------#


def generate_response(context, requirements):
    try:
        with st.spinner("Generando historia de usuario..."):
            response = requests.post(
                API_URL,
                json={
                    "input": {"contexto": context, "requisitos": requirements},
                    "config": {},
                    "kwargs": {},
                },
            )
            if response.status_code == 200:
                run_id = response.json()["metadata"]["run_id"]
                response = response.json()["output"].replace("\n", "  \n  ")
                st.session_state.generated_response = response
                st.session_state.feedback = {"run_id": str(run_id)}
            else:
                st.error("Error al comunicarse con la API")
    except Exception as e:
        st.error(f"Error: {str(e)}")


# --------- feedback ---------#


def send_feedback(feedback_id, score):
    try:
        feedback_response = requests.post(
            "http://localhost:8000/generate_story/feedback",
            json={
                "run_id": feedback_id,
                "key": "alpha v0.1",
                "score": score,
                "value": None,
                "comment": None,
            },
        )
        if feedback_response.status_code == 200:
            st.session_state.feedback_sent = True
            st.success("¡Gracias por tu feedback!")
        else:
            st.error("Error al enviar el feedback")
    except Exception as e:
        st.error(f"Error: {str(e)}")


# --------- Main ---------#

# Botón para limpiar la respuesta
if st.button("Nueva historia"):
    st.session_state.generated_response = None
    st.session_state.requirements_input = ""

# Formulario para ingresar los requisitos
with st.form("my_form"):
    requirements = st.text_area(
        "Ingrese los requisitos para generar la HU:",
        value=st.session_state.get("requirements", ""),
        placeholder=DEFAULT_REQUIREMENTS,
        key="requirements_input",
    )
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        submitted = st.form_submit_button("Generar")
    with col2:
        regenerate = st.form_submit_button("Generar de nuevo")
        st.session_state.feedback_sent = False
    if submitted or regenerate:
        generate_response(context, requirements)
    # Mostrar la respuesta generada si existe
    if st.session_state.generated_response:
        st.markdown(st.session_state.generated_response)

# Agregar botones de feedback si aún no se ha enviado
if not st.session_state.feedback_sent and st.session_state.generated_response:
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("👍 Útil"):
            send_feedback(st.session_state.feedback.get("run_id"), 1)
    with col2:
        if st.button("👎 No es útil"):
            send_feedback(st.session_state.feedback.get("run_id"), 0)
