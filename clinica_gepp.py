import streamlit as st
import random
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="GEPP - Simulador SAC Entrega",
    page_icon="🚛",
    layout="centered"
)

# --- ESTILOS GEPP BRANDING ---
st.markdown("""
    <style>
    :root {
        --pepsi-blue: #004B93;
        --pepsi-red: #C9002B;
    }
    .stApp { background-color: #f8f9fa; }
    .gepp-header {
        background: linear-gradient(135deg, #004B93 0%, #002d5a 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 8px solid #C9002B;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        padding: 1.2rem;
        background-color: white;
        color: #333;
        font-weight: 600;
        border: 2px solid #dee2e6;
        text-align: left;
        white-space: normal;
        height: auto;
        line-height: 1.4;
    }
    .stButton>button:hover {
        border-color: #004B93;
        background-color: #f0f7ff;
    }
    .report-card {
        background-color: white;
        padding: 40px;
        border: 1px solid #ccc;
        color: #333;
        font-family: 'Arial', sans-serif;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .signature-box {
        margin-top: 30px;
        text-align: center;
        border-top: 1px solid #333;
        display: inline-block;
        padding-top: 10px;
        width: 380px;
    }
    .scenario-text {
        background-color: #eef2f7;
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid var(--pepsi-blue);
        margin-bottom: 20px;
        font-size: 1.2rem;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DATOS ROBUSTECIDO ---
BANCO_DATOS = [
    # TEMA: PRÓXIMOS A CADUCAR (Escenario ajustado)
    {
        "cat": "Calidad",
        "titulo": "Producto Próximo a Caducar",
        "situacion": "Llegas al punto de venta y el cliente reclama que tiene producto por vencer. Tú no traes los cambios de mercado en tu liquidación de hoy.",
        "excelente": "'Entiendo su preocupación, jefa. Aunque no traigo los cambios programados, déjeme revisar exactamente qué producto es el que está por vencer; si lo traigo en el camión, se lo cambio ahorita mismo para que siempre tenga producto fresco.'",
        "regular": "'Déjeme anotarlo para decirle al preventista que le cargue el cambio la próxima semana. Ahorita no puedo hacer nada porque no traigo los folios de mercado.'",
        "mala": "'Yo no traigo cambios hoy porque no venían en mi hoja. Ese es tema del vendedor, yo solo vengo a entregar lo que me cargaron.'",
        "fb": "La proactividad de revisar y cambiar el producto con el inventario del camión evita rechazos y garantiza frescura."
    },
    # TEMA: JARRITOS / SABORES
    {
        "cat": "Jarritos",
        "situacion": "El cliente reclama: 'Yo pedí puro de Mandarina y me traes de Tamarindo y Ponche. No los quiero.'",
        "excelente": "'Una disculpa por el error en los sabores, jefe. Déjeme ver si traigo Mandarina extra en la unidad para ajustarlo. Si no, ¿le parece si le dejo estos sabores y les damos prioridad en el enfriador para que roten rápido?'",
        "regular": "'Es lo que capturó el sistema, jefe. Tómelo así por esta vez y a la otra le pido al preventista que tenga más cuidado con sus sabores.'",
        "mala": "'Es lo que hay en existencia. Si no los quiere los regreso, pero se va a quedar sin la promoción de Jarritos.'",
        "fb": "Negociar el inventario disponible o buscar soluciones en el camión demuestra actitud de servicio."
    },
    # TEMA: RETRASO DE HORARIO
    {
        "cat": "Horario",
        "situacion": "Llegas 2 horas tarde del horario preferido: 'A esta hora ya no recibo, ya estoy cerrando caja y me voy.'",
        "excelente": "'Le pido una disculpa sincera por el retraso, tuvimos una demora en la carga. ¿Me permite bajarle solo lo más vendido en 3 minutos para que no pierda venta mañana? Yo le ayudo a acomodarlo de volada.'",
        "regular": "'Es que la ruta estuvo muy pesada hoy, jefe. Déjeme bajarle aunque sea lo poquito para que no me regañen en el Cedis.'",
        "mala": "'Apenas voy llegando, si quiere el producto recíbame ahorita o nos vemos la otra semana. Yo también ya me quiero ir.'",
        "fb": "La humildad y la oferta de ayuda rápida desactivan la molestia por el retraso."
    },
    # TEMA: VISITA OMITIDA
    {
        "cat": "Visita Omitida",
        "situacion": "Cliente furioso: 'La semana pasada no vinieron y perdí mucha venta. ¡Ya no quiero nada de GEPP!'",
        "excelente": "'Le ofrezco una disculpa de parte de la empresa, jefe. Tuvimos un problema con la unidad. Estoy aquí para recuperar su confianza; déjeme surtirle lo más urgente y yo mismo le acomodo el refri para que se vea impecable.'",
        "regular": "'Es que faltó el chofer de esta ruta, jefe. Pero hoy ya estoy yo aquí, no se enoje y recíbame el pedido.'",
        "mala": "'Yo apenas cubro esta ruta hoy, no sé por qué no vinieron. Si va a querer el refresco dígame de una vez.'",
        "fb": "Validar la molestia del cliente (Pararrayos) es el primer paso para recuperar una cuenta perdida."
    },
    # TEMA: GATORADE
    {
        "cat": "Gatorade",
        "situacion": "Cliente rechaza: 'Aquí no vendo Gatorade, pura gente grande viene y no hacen deporte.'",
        "excelente": "'Jefe, Gatorade no es solo para deportistas; con este calor es la mejor hidratación para los trabajadores que pasan por aquí. ¿Le dejo unas cuantas para que vea cómo se venden solo por el calor?'",
        "regular": "'Pruébelo jefe, de todos modos tarda en caducar. Le dejo unos cuantos para ver si salen.'",
        "mala": "'Por eso no crece su negocio, porque no quiere meter productos nuevos que sí dejan margen.'",
        "fb": "Vender el beneficio de la hidratación diaria es más efectivo que vender el deporte."
    }
]

# --- LÓGICA DE NAVEGACIÓN ---
def reset_quiz():
    # Selecciona 4 escenarios aleatorios para que sea dinámico
    mezcla = random.sample(BANCO_DATOS, 4)
    quiz_list = []
    for esc in mezcla:
        ops = [
            {"tipo": "E", "txt": esc["excelente"], "fb": esc["fb"]},
            {"tipo": "R", "txt": esc["regular"], "fb": esc["fb"]},
            {"tipo": "M", "txt": esc["mala"], "fb": esc["fb"]}
        ]
        random.shuffle(ops)
        quiz_list.append({
            "cat": esc["cat"],
            "t": esc["situacion"],
            "o": ops
        })
    st.session_state.quiz = quiz_list
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.paso = 'QUIZ'
    st.session_state.respondido = False

if 'paso' not in st.session_state:
    st.session_state.paso = 'INICIO'

# --- INTERFAZ ---
st.markdown('<div class="gepp-header"><h1>GEPP: RUTA DE EXCELENCIA</h1><p>Certificación SAC Entrega Embotellado</p></div>', unsafe_allow_html=True)

if st.session_state.paso == 'INICIO':
    st.subheader("📋 Registro del Colaborador")
    st.session_state.nombre = st.text_input("Nombre Completo:", placeholder="Ej. Juan Pérez")
    st.session_state.ruta = st.text_input("Número de Ruta / Cedis:", placeholder="Ej. R-102")
    
    if st.button("COMENZAR EVALUACIÓN"):
        if st.session_state.nombre and st.session_state.ruta:
            reset_quiz()
            st.rerun()
        else:
            st.warning("Es obligatorio ingresar nombre y ruta para generar la ficha de evidencia.")

elif st.session_state.paso == 'QUIZ':
    curr = st.session_state.quiz[st.session_state.idx]
    st.caption(f"Situación {st.session_state.idx + 1} de 4 | Categoría: {curr['cat']}")
    
    st.markdown(f'<div class="scenario-text">"{curr["t"]}"</div>', unsafe_allow_html=True)

    if not st.session_state.respondido:
        st.write("**Selecciona la respuesta que aplicarías:**")
        for i, op in enumerate(curr["o"]):
            if st.button(op["txt"], key=f"btn_{i}"):
                val = 2 if op["tipo"] == "E" else 1 if op["tipo"] == "R" else 0
                st.session_state.score += val
                st.session_state.history.append({"t": curr["t"], "r": op["tipo"]})
                st.session_state.last_type = op["tipo"]
                st.session_state.last_fb = op["fb"]
                st.session_state.respondido = True
                st.rerun()
    else:
        if st.session_state.last_type == "E":
            st.success(f"**EXCELENTE.** {st.session_state.last_fb}")
        elif st.session_state.last_type == "R":
            st.warning(f"**REGULAR.** {st.session_state.last_fb}")
        else:
            st.error(f"**MALA DECISIÓN.** {st.session_state.last_fb}")
        
        if st.button("Siguiente Situación ➡️"):
            if st.session_state.idx < len(st.session_state.quiz) - 1:
                st.session_state.idx += 1
                st.session_state.respondido = False
                st.rerun()
            else:
                st.session_state.paso = 'REPORTE'
                st.rerun()

elif st.session_state.paso == 'REPORTE':
    st.balloons()
    st.header("🏁 Evaluación Finalizada")
    
    max_pts = 8 # 4 escenarios * 2 pts
    score = st.session_state.score
    cat_final = "LEYENDA GEPP" if score >= 7 else "PROFESIONAL" if score >= 5 else "EN FORMACIÓN"
    
    st.success(f"Puntaje Obtenido: {score} de {max_pts}")
    
    # HTML del Reporte
    st.markdown(f"""
    <div class="report-card">
        <h2 style="text-align:center; color:#004B93; margin-top:0;">FICHA DE EVIDENCIA SAC</h2>
        <p style="text-align:right;"><strong>FECHA:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>
        <p><strong>COLABORADOR:</strong> {st.session_state.nombre.upper()}</p>
        <p><strong>RUTA / UNIDAD:</strong> {st.session_state.ruta}</p>
        <hr>
        <h3 style="margin-bottom:5px;">DESEMPEÑO:</h3>
        <p style="font-size:24px;"><strong>CALIFICACIÓN:</strong> {score} / {max_pts}</p>
        <p style="font-size:20px;"><strong>NIVEL:</strong> <span style="color:#C9002B; font-weight:bold;">{cat_final}</span></p>
        <hr>
        <h4>RESUMEN DE COMPETENCIAS:</h4>
        <ul style="font-size: 13px;">
    """, unsafe_allow_html=True)
    
    for h in st.session_state.history:
        label = "Excelente" if h['r'] == "E" else "Regular" if h['r'] == "R" else "Mala"
        st.write(f"- {h['t'][:65]}...: **{label}**")
        
    st.markdown(f"""
        </ul>
        <br><br>
        <div style="text-align:center;">
            <p style="font-size: 11px; font-style: italic;">Certificado generado para validación de entrenamiento SAC</p>
            <br>
            <div class="signature-box">
                <br>
                <strong>MARCELO HERNÁNDEZ MONTALVO</strong><br>
                Jefe SAC Entrega Embotellado
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Toma una captura de pantalla para tu comprobante oficial.")
    
    if st.button("Reiniciar Clínica (Nuevos Escenarios)"):
        st.session_state.paso = 'INICIO'
        st.rerun()

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Pepsi_logo_2014.svg/1200px-Pepsi_logo_2014.svg.png", width=100)
    st.title("Centro SAC GEPP")
    st.divider()
    st.write(f"Evaluando a: **{st.session_state.get('nombre', 'Pendiente')}**")
    st.info("Esta sesión consta de 4 escenarios aleatorios.")
