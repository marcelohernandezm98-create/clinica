import streamlit as st
# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
   page_title="GEPP - Simulador de Ruta",
   page_icon="🚛",
   layout="centered"
)
# --- ESTILOS PERSONALIZADOS (BRANDING GEPP/PEPSI) ---
st.markdown("""
<style>
   :root {
       --pepsi-blue: #004B93;
       --pepsi-red: #C9002B;
   }
   .stApp { background-color: #f8f9fa; }
   .gepp-header {
       background: linear-gradient(90deg, #004B93 0%, #002d5a 100%);
       padding: 2rem;
       border-radius: 15px;
       color: white;
       text-align: center;
       margin-bottom: 2rem;
       border-bottom: 6px solid #C9002B;
   }
   .stButton>button {
       width: 100%;
       border-radius: 12px;
       padding: 1rem;
       font-weight: bold;
   }
   .correct-card {
       background-color: #d4edda;
       padding: 20px;
       border-radius: 10px;
       border-left: 8px solid #28a745;
       color: #155724;
   }
   .wrong-card {
       background-color: #f8d7da;
       padding: 20px;
       border-radius: 10px;
       border-left: 8px solid #C9002B;
       color: #721c24;
   }
</style>
   """, unsafe_allow_html=True)
# --- INICIALIZACIÓN DE ESTADO ---
if 'paso' not in st.session_state:
   st.session_state.paso = 'INICIO'
if 'puntaje' not in st.session_state:
   st.session_state.puntaje = 0
if 'escenario_actual' not in st.session_state:
   st.session_state.escenario_actual = 0
# --- ESCENARIOS ---
ESCENARIOS = [
   {
       "titulo": "Escenario 1: El Pedido No Reconocido",
       "situacion": "El cliente dice: '¡Yo no pedí estas 10 cajas! No las quiero.'",
       "opciones": [
           {"texto": "⚠️ 'Pues aquí dice que sí. Reclame a la oficina.'", "es_correcta": False, "feedback": "¡ERROR! Culpar al sistema daña la relación."},
           {"texto": "✅ 'Entiendo el malentendido, jefe. ¿Qué le parece si dejamos solo lo básico?'", "es_correcta": True, "feedback": "¡EXCELENTE! Usaste empatía y negociación."}
       ]
   }
]
# --- LÓGICA ---
def procesar_respuesta(es_correcta, feedback):
   if es_correcta:
       st.session_state.puntaje += 1
   st.session_state.feedback_actual = feedback
   st.session_state.es_correcta_actual = es_correcta
   st.session_state.paso = 'FEEDBACK'
# --- INTERFAZ ---
st.markdown('<div class="gepp-header"><h1>GEPP: RUTA DE EXCELENCIA</h1></div>', unsafe_allow_html=True)
if st.session_state.paso == 'INICIO':
   st.subheader("🚀 Bienvenido al Desafío")
   if st.button("COMENZAR ENTRENAMIENTO"):
       st.session_state.paso = 'SIMULADOR'
       st.rerun()
elif st.session_state.paso == 'SIMULADOR':
   esc = ESCENARIOS[st.session_state.escenario_actual]
   st.info(f"🗨️ **SITUACIÓN:** {esc['situacion']}")
   for opcion in esc["opciones"]:
       if st.button(opcion["texto"]):
           procesar_respuesta(opcion["es_correcta"], opcion["feedback"])
           st.rerun()
elif st.session_state.paso == 'FEEDBACK':
   if st.session_state.es_correcta_actual:
       st.success(st.session_state.feedback_actual)
   else:
       st.error(st.session_state.feedback_actual)
   if st.button("REINICIAR"):
       st.session_state.paso = 'INICIO'
       st.rerun()
