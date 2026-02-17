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
        padding: 1rem;
        background-color: white;
        color: #333;
        font-weight: 600;
        border: 2px solid #dee2e6;
        text-align: left;
        white-space: normal;
        height: auto;
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
        width: 350px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DATOS ROBUSTECIDO (10 ESCENARIOS) ---
BANCO_DATOS = [
    {
        "id": "GRB",
        "titulo": "Taquerías (Producto GRB)",
        "situacion": "El cliente dice: 'Ya no me bajes vidrio (GRB), me quita mucho espacio y las cajas estorban.'",
        "excelente": "✅ 'Entiendo el espacio, jefe. Pero el vidrio es lo que más busca el cliente en taquerías por el sabor. ¿Qué le parece si acomodamos las cajas vacías bajo la barra para que no estorben?'",
        "regular": "🟡 'Bueno jefe, le dejo solo PET entonces, pero sepa que el vidrio le da mejor imagen a su negocio.'",
        "mala": "❌ 'Si no quiere vidrio no le puedo respetar el precio de promoción. Usted sabe si quiere perder dinero.'",
        "fb": "El GRB es clave en taquerías. Siempre busca soluciones de espacio antes de ceder al PET."
    },
    {
        "id": "ENVASE",
        "titulo": "Envase No Operativo",
        "situacion": "El cliente entrega envase sucio o de competencia: 'Llévatelo, total es refresco igual.'",
        "excelente": "✅ 'Jefe, para que planta me acepte el envase y yo pueda surtirle calidad, necesito que sean de nuestra marca y estén limpios. Ayúdeme a separarlos y yo le ayudo con los nuevos.'",
        "regular": "🟡 'Hoy se los paso jefe, pero la próxima si vienen sucios no se los puedo recibir porque me regañan.'",
        "mala": "❌ 'Eso no me sirve. Si no tiene envase bueno no hay producto. Yo no vengo a perder el tiempo.'",
        "fb": "Educar al cliente sobre el envase asegura una operación fluida y sin rechazos en planta."
    },
    {
        "id": "DOBLE_VUELTA",
        "titulo": "Cliente Cerrado (Doble Vuelta)",
        "situacion": "Llegas y el cliente está ocupado: 'Ahorita no puedo, joven. Déme una vuelta y regrese después.'",
        "excelente": "✅ 'Entiendo que está ocupado. ¿Me permite bajar solo lo más urgente en 5 minutos o prefiere que pase al final de mi ruta antes de irme al Cedis?'",
        "regular": "🟡 'Está bien, le doy la vuelta pero si ya voy tarde no prometo regresar porque la ruta está pesada.'",
        "mala": "❌ 'Yo ya no vuelvo a pasar. O recibe ahorita o se queda sin refresco hasta la próxima visita.'",
        "fb": "Ser flexible sin comprometer la ruta muestra profesionalismo y empatía."
    },
    {
        "id": "INVENTARIO",
        "titulo": "Tienda en Inventario",
        "situacion": "Encargado contando: 'No recibo nada hoy, estamos en inventario y se me descuadra todo.'",
        "excelente": "✅ 'Lo entiendo, jefa. ¿Qué le parece si bajo el producto y yo mismo le ayudo a contarlo para que lo anote de una vez en su lista actual?'",
        "regular": "🟡 'Deme oportunidad jefa, me tardo poquito. Nada más anote estas cajas al final de su lista.'",
        "mala": "❌ 'A mí el sistema me obliga a entregar hoy. Si no recibe, me va a afectar mi bono de efectividad.'",
        "fb": "El Servicio 360 implica ayudar al cliente en sus procesos, no ser una carga adicional."
    },
    {
        "id": "TICKET",
        "titulo": "Sin Ticket No Reciben",
        "situacion": "El cliente exige: 'Si no traes el ticket impreso o nota de preventa, no te recibo nada.'",
        "excelente": "✅ 'Tiene razón jefe, el orden es primero. Déjeme generar la nota digital en mi equipo o llamar al preventista para que se la envíe por WhatsApp ahorita mismo.'",
        "regular": "🟡 'Déjeme ver qué puedo hacer, es que la impresora falló. ¿Me firma un papelito y luego le traigo el bueno?'",
        "mala": "❌ 'Ya sabe cómo trabajamos, no se ponga así por un papel. Mañana se lo traigo sin falta.'",
        "fb": "Respeta los procesos administrativos del cliente; el ticket es su control de dinero."
    },
    {
        "id": "GATORADE",
        "titulo": "Venta de Gatorade",
        "situacion": "Cliente rechaza: 'Aquí no vendo Gatorade, pura gente grande viene y no hacen deporte.'",
        "excelente": "✅ 'Jefe, Gatorade no es solo para atletas; con este calor es la mejor forma de hidratarse para cualquier trabajador. ¿Le dejo 6 botellas para que vea cómo vuelan?'",
        "regular": "🟡 'Pruébelo jefe, de todos modos no caduca rápido. Le dejo una cajita para ver si sale.'",
        "mala": "❌ 'Por eso no crece su negocio, porque no quiere meter productos nuevos.'",
        "fb": "Vende beneficios (hidratación) en lugar de solo el concepto deportivo."
    },
    {
        "id": "EPURA",
        "titulo": "Epura Garrafón",
        "situacion": "Cliente dice: 'No me deje agua hoy, todavía tengo medio garrafón.'",
        "excelente": "✅ 'Entiendo, jefa. Pero para que no ande cargando después de la tienda, ¿le dejo uno de reserva de una vez? Así descansa el fin de semana.'",
        "regular": "🟡 'Acuérdese que luego se acaba y yo no paso hasta el otro miércoles por aquí.'",
        "mala": "❌ 'Como quiera. Luego no ande pidiendo de urgencia porque no voy a tener.'",
        "fb": "La conveniencia (no cargar peso) es el mejor argumento de venta para Epura."
    },
    {
        "id": "FANTASMA",
        "titulo": "Pedido No Reconocido",
        "situacion": "El cliente jura que no pidió nada de lo que traes en el camión.",
        "excelente": "✅ 'Una disculpa jefe, pudo haber un error de captura. ¿Me permite checar qué le falta en su refri? Solo le dejo lo necesario para que no pierda venta.'",
        "regular": "🟡 'Déjeme hablar con el vendedor para ver qué pasó, pero pues ya traigo la carga aquí lista.'",
        "mala": "❌ 'Usted lo pidió y yo lo traigo. Si no recibe lo voy a tener que reportar con el supervisor.'",
        "fb": "Usa la frase pararrayos para bajar la tensión y negocia sobre el inventario real."
    },
    {
        "id": "DINERO",
        "titulo": "Sin Efectivo",
        "situacion": "Cliente dice: 'No tengo dinero, joven. La venta ha estado muy floja.'",
        "excelente": "✅ 'Entiendo jefe. Pero viene el calor fuerte. ¿Le dejo solo 2 cajitas de Pepsi 600ml y Agua Epura? Son las que más rotan y le darán flujo de lana rápido.'",
        "regular": "🟡 'Hágale un esfuerzo jefe, yo tengo que cumplir mi meta. No me deje abajo hoy.'",
        "mala": "❌ 'Bueno patrón, si no hay lana no hay refresco. Nos vemos la próxima semana.'",
        "fb": "Ofrece el 'Mínimo Indispensable' para que el cliente no pierda ventas de alta rotación."
    },
    {
        "id": "CERRADO",
        "titulo": "Servicio 360 (Rechazo)",
        "situacion": "Rechazo total: 'Hoy no ocupo nada, ya surtí con la competencia.'",
        "excelente": "✅ 'No hay problema, jefa. Déjeme nada más frentear su refri para que luzca bien y se le venda rápido lo que tiene. ¡Nos vemos el jueves!'",
        "regular": "🟡 'Entendido. Voy a aprovechar para limpiar los exhibidores de afuera rápido. ¡Ventas exitosas!'",
        "mala": "❌ 'De haber sabido ni me paro. Me hizo perder el tiempo bajando cajas.'",
        "fb": "El merchandising (limpiar/acomodar) es servicio que garantiza ventas futuras."
    }
]

# --- LÓGICA DE NAVEGACIÓN ---
def reset_quiz():
    mezcla = random.sample(BANCO_DATOS, len(BANCO_DATOS))
    quiz_list = []
    for esc in mezcla:
        ops = [
            {"tipo": "E", "txt": esc["excelente"], "fb": esc["fb"]},
            {"tipo": "R", "txt": esc["regular"], "fb": esc["fb"]},
            {"tipo": "M", "txt": esc["mala"], "fb": esc["fb"]}
        ]
        random.shuffle(ops)
        quiz_list.append({
            "t": esc["titulo"],
            "s": esc["situacion"],
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
st.markdown('<div class="gepp-header"><h1>GEPP: RUTA DE EXCELENCIA</h1><p>Clínica SAC Entrega Embotellado</p></div>', unsafe_allow_html=True)

if st.session_state.paso == 'INICIO':
    st.subheader("📋 Registro de Entrenamiento")
    st.session_state.nombre = st.text_input("Nombre del Colaborador:", placeholder="Nombre Completo")
    st.session_state.ruta = st.text_input("Número de Ruta:", placeholder="Ej. R-102")
    
    if st.button("INICIAR SIMULACIÓN"):
        if st.session_state.nombre and st.session_state.ruta:
            reset_quiz()
            st.rerun()
        else:
            st.warning("Ingresa tus datos para generar la evidencia oficial al finalizar.")

elif st.session_state.paso == 'QUIZ':
    curr = st.session_state.quiz[st.session_state.idx]
    st.caption(f"Situación {st.session_state.idx + 1} de {len(st.session_state.quiz)}")
    
    st.info(f"🗨️ **ESCENARIO:** {curr['s']}")

    if not st.session_state.respondido:
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
        # Feedback visual
        if st.session_state.last_type == "E":
            st.success(f"⭐ **¡EXCELENTE!** {st.session_state.last_fb}")
        elif st.session_state.last_type == "R":
            st.warning(f"👌 **REGULAR.** {st.session_state.last_fb}")
        else:
            st.error(f"❌ **MALA DECISIÓN.** {st.session_state.last_fb}")
        
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
    st.header("🏁 Reporte de Evidencia Oficial")
    
    max_pts = len(st.session_state.quiz) * 2
    score = st.session_state.score
    cat = "LEYENDA GEPP" if score >= max_pts*0.9 else "PROFESIONAL" if score >= max_pts*0.6 else "EN FORMACIÓN"
    
    # El Documento
    st.markdown(f"""
    <div class="report-card">
        <h2 style="text-align:center; color:#004B93;">FICHA DE EVALUACIÓN SAC</h2>
        <p><strong>FECHA:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>
        <p><strong>COLABORADOR:</strong> {st.session_state.nombre.upper()}</p>
        <p><strong>RUTA:</strong> {st.session_state.ruta}</p>
        <hr>
        <h3>RESULTADOS:</h3>
        <p><strong>PUNTUACIÓN:</strong> {score} de {max_pts} puntos posibles.</p>
        <p><strong>CATEGORÍA:</strong> <span style="color:#C9002B; font-weight:bold;">{cat}</span></p>
        <hr>
        <p style="font-size:12px;">Esta clínica evalúa: Actitud positiva, gestión de rechazo, venta sugestiva y servicio 360 en el portafolio GEPP (Pepsi, Epura, Gatorade).</p>
        <br><br>
        <div style="text-align:center;">
            <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCABlAL8DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2N3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqGhc4lHxICG4hJOCV0hZFiRlE4Y3RReJGRSjpJSlUfVxeXZ1NWVgcMNCZGZ3R1d3R1d4XF1GVmRlW2hpamtsbW5eeXp6hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmqjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//2Q==" width="220"><br>
            <div class="signature-box">
                <strong>MARCELO HERNÁNDEZ MONTALVO</strong><br>
                Jefe SAC Entrega Embotellado
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("REINICIAR CLÍNICA (Contenido Nuevo)"):
        st.session_state.paso = 'INICIO'
        st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Pepsi_logo_2014.svg/1200px-Pepsi_logo_2014.svg.png", width=100)
    st.title("Guía SAC GEPP")
    st.markdown("""
    **¿Cómo calificar?**
    - **Excelente:** Resolvió el problema + Generó venta o valor.
    - **Regular:** Fue amable pero no intentó salvar la venta.
    - **Mala:** Fue grosero o se rindió sin argumentos.
    """)
    st.divider()
    st.info("💡 Consejo: Al finalizar, toma captura de la Ficha de Evaluación.")
