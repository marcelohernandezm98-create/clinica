import streamlit as st
import random
from datetime import datetime
from fpdf import FPDF
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="GEPP - Certificación SAC",
    page_icon="🚛",
    layout="centered"
)

# --- FUNCIÓN PARA GENERAR PDF ---
def generar_pdf(nombre, ruta, puntaje, categoria, historial):
    pdf = FPDF()
    pdf.add_page()
    
    # Borde decorativo
    pdf.rect(5, 5, 200, 287)
    
    # Encabezado
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(0, 75, 147) # Azul Pepsi
    pdf.cell(0, 20, 'GEPP - CERTIFICADO DE CAPACITACION', 0, 1, 'C')
    
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(201, 0, 43) # Rojo Pepsi
    pdf.cell(0, 10, 'SISTEMA DE ATENCION AL CLIENTE (SAC)', 0, 1, 'C')
    
    pdf.ln(10)
    
    # Cuerpo del certificado
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, f"Por medio de la presente, se certifica que el colaborador:", align='C')
    
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 15, nombre.upper(), 0, 1, 'C')
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Perteneciente a la ruta/unidad: {ruta}", 0, 1, 'C')
    
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Ha completado satisfactoriamente la clinica de entrenamiento dinamico, obteniendo un desempeno de nivel:", align='C')
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 15, f"CATEGORIA: {categoria}", 0, 1, 'C')
    
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 10, f"Puntuacion final: {puntaje} de 8 puntos posibles.", 0, 1, 'C')
    
    pdf.ln(15)
    
    # Detalle de competencias
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 10, "RESUMEN DE COMPETENCIAS EVALUADAS:", 0, 1, 'L')
    pdf.set_font('Arial', '', 9)
    for h in historial:
        res = "Excelente" if h['r'] == "E" else "Regular" if h['r'] == "R" else "Mala"
        pdf.cell(0, 7, f"- {h['t'][:80]}... : {res}", 0, 1, 'L')
    
    # Firma
    pdf.ln(20)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "_______________________________________", 0, 1, 'C')
    pdf.cell(0, 7, "MARCELO HERNANDEZ MONTALVO", 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, "Jefe SAC Entrega Embotellado", 0, 1, 'C')
    
    pdf.set_y(-30)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, f"Fecha de emision: {datetime.now().strftime('%d/%m/%Y')}", 0, 0, 'C')
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .gepp-header {
        background: linear-gradient(135deg, #004B93 0%, #002d5a 100%);
        padding: 2rem; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 2rem; border-bottom: 8px solid #C9002B;
    }
    .stButton>button { width: 100%; border-radius: 12px; padding: 1rem; font-weight: 600; text-align: left; }
    .scenario-text { background-color: #eef2f7; padding: 25px; border-radius: 12px; border-left: 6px solid #004B93; margin-bottom: 20px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DATOS (24 ESCENARIOS) ---
BANCO_DATOS = [
    {"cat": "Calidad", "titulo": "Producto Proximo a Caducar", "situacion": "El cliente reclama producto por vencer y no traes ordenes de cambio.", "E": "'Entiendo. Dejeme revisar que es; si lo traigo en el camion se lo cambio ahorita mismo para que tenga producto fresco.'", "R": "'Anote lo que es y le digo al preventista que le mande el cambio la otra semana.'", "M": "'Eso es descuido suyo por no rotar. Yo solo entrego lo que me cargaron.'", "fb": "La proactividad evita mermas y asegura frescura."},
    {"cat": "Surtido", "titulo": "Jarritos Sabores", "situacion": "El cliente pidio Mandarina y traes Tamarindo: 'No me los bajes.'", "E": "'Disculpe. Dejeme ver si traigo Mandarina extra en la unidad. Si no, ¿podemos acomodar estos en un lugar mas visible?'", "R": "'Es lo que capturaron en sistema. Tomelo asi y a la otra le pido al preventista mas cuidado.'", "M": "'Es lo que hay. Si no los quiere los regreso y se queda sin promocion.'", "fb": "Negociar el stock disponible salva la venta."},
    {"cat": "Servicio", "titulo": "Retraso Horario", "situacion": "Llegas 2 horas tarde: 'Ya no recibo, ya estoy cerrando caja.'", "E": "'Una disculpa, tuvimos retraso en carga. ¿Me permite bajar lo mas vendido en 3 minutos? Yo le ayudo a acomodar.'", "R": "'Hubo mucho trafico, jefe. Dejeme bajarle poquito para que no me regañen.'", "M": "'Apenas voy llegando. Si quiere el producto recibame ahorita o nos vemos la otra semana.'", "fb": "La humildad y rapidez desactivan la molestia."},
    {"cat": "Servicio", "titulo": "Visita Omitida", "situacion": "Cliente furioso: 'La semana pasada no vinieron. ¡Ya no quiero nada!'", "E": "'Disculpe jefe, tuvimos una falla tecnica. Estoy aqui para recuperar su confianza surtiendole lo urgente hoy.'", "R": "'Falto el chofer anterior. Pero hoy ya estoy yo aqui, recibame el pedido.'", "M": "'Yo apenas cubro esta ruta hoy. Si va a querer el refresco digame de una vez.'", "fb": "El Pararrayos recupera cuentas perdidas."},
    {"cat": "Logistica", "titulo": "Espacio Taquerias", "situacion": "Taquero: 'Ya no quiero vidrio, las cajas estorban.'", "E": "'Entiendo. Pero el vidrio es lo que mas busca su cliente. ¿Y si acomodamos las vacias bajo la barra?'", "R": "'Le dejo PET entonces, pero sepa que el vidrio le da mejor imagen.'", "M": "'Si no quiere vidrio pierde el precio de promocion. Usted decide.'", "fb": "Proteger el GRB es clave en el canal de comida."},
    {"cat": "Ventas", "titulo": "Objeccion Gatorade", "situacion": "Cliente: 'Aqui no vendo Gatorade, no hacen deporte.'", "E": "'Jefe, con este calor es la mejor hidratacion para cualquier trabajador. ¿Le dejo 6 para que vea como vuelan?'", "R": "'Pruebelo jefe, tarda en caducar. Le dejo unos cuantos.'", "M": "'Por eso no crece su negocio, porque no quiere meter productos nuevos.'", "fb": "Vende hidratacion, no solo deporte."},
    {"cat": "Ventas", "titulo": "Epura Garrafon", "situacion": "Cliente: 'No me deje agua, tengo medio garrafon.'", "E": "'Jefa, para que no cargue despues, ¿le dejo uno de reserva? Asi descansa el fin de semana.'", "R": "'Acuérdese que luego se acaba y yo no paso hasta el otro miercoles.'", "M": "'Como quiera. Luego no ande pidiendo de urgencia.'", "fb": "Vende comodidad y ahorro de esfuerzo."},
    {"cat": "Operacion", "titulo": "Envase Sucio", "situacion": "Cliente entrega envase de competencia o muy sucio.", "E": "'Para que planta me lo acepte, necesito que sean de nuestra marca. Ayudeme a separarlos y yo le ayudo con los nuevos.'", "R": "'Hoy se los paso, pero la proxima no puedo recibirlos.'", "M": "'Eso no me sirve. Si no tiene envase Pepsi no hay producto.'", "fb": "Educar asegura operacion sin rechazos."},
    {"cat": "Operacion", "titulo": "Inventario", "situacion": "Encargado contando: 'No recibo nada hoy.'", "E": "'Entiendo. ¿Que le parece si bajo el producto y yo mismo le ayudo a contarlo para su lista?'", "R": "'Deme oportunidad jefa, me tardo poquito. Anotelo al final.'", "M": "'El sistema me obliga a entregar hoy. Me va a afectar mi bono.'", "fb": "Facilitar el trabajo es Servicio 360."},
    {"cat": "Ventas", "titulo": "Precio Competencia", "situacion": "Cliente: 'La competencia me da mas barato.'", "E": "'Entiendo. Pero con Pepsi tiene mayor rotacion y respaldo GEPP. ¿Revisamos sus promos vigentes?'", "R": "'Ellos venden menos, por eso dan mas barato.'", "M": "'Si quiere producto malo compre alla. Yo traigo la lider.'", "fb": "Vende valor y servicio, no solo precio."},
    {"cat": "Calidad", "titulo": "Envase Roto", "situacion": "Al bajar el pedido se rompe una botella.", "E": "'No se preocupe, fue mi error. Dejeme limpiar y le cambio la dañada por una nueva de mi reserva.'", "R": "'Paguela y yo prometo que la otra semana se la repongo.'", "M": "'Usted se atraveso. Ahora tiene que pagarla.'", "fb": "Responsabilidad y limpieza ganan respeto."},
    {"cat": "Ventas", "titulo": "Bodega Llena", "situacion": "Cliente: 'No tengo espacio, no me dejes nada.'", "E": "'Entiendo. ¿Me permite acomodarle lo que tiene? Si hacemos espacio, le dejo solo lo mas urgente.'", "R": "'Ni modo jefa, me llevo el pedido entonces.'", "M": "'Hagale un lugar, yo no puedo regresar producto al Cedis.'", "fb": "Acomodar es vender."},
    {"cat": "Logistica", "titulo": "Camion Estorbando", "situacion": "Transito se queja de que el camion estorba.", "E": "'Una disculpa. Deme 2 minutos para terminar y muevo la unidad de inmediato.'", "R": "'Estoy trabajando, esperese a que acabe.'", "M": "'Muevase por otro lado, yo tengo permiso de entrega.'", "fb": "La cortesia es imagen de marca."},
    {"cat": "Operacion", "titulo": "Billete Grande", "situacion": "El cliente paga con $500 y no traes cambio.", "E": "'No traigo cambio por seguridad. ¿Me ayuda a buscar uno chico o preguntamos al vecino mientras bajo?'", "R": "'Vaya a cambiarlo a la gasolinera porque yo no traigo morralla.'", "M": "'Si no tiene cambio no le dejo nada. Consiga o me retiro.'", "fb": "Busca soluciones compartidas."},
    {"cat": "Operacion", "titulo": "Pedido Fantasma", "situacion": "Cliente: 'Yo no pedi esto, el preventista se equivoco.'", "E": "'Lamento el error. ¿Que le falta en su refri? Le dejo eso para que no pierda venta y me llevo el resto.'", "R": "'Hable con el vendedor, yo traigo lo que dice mi liquidacion.'", "M": "'Usted lo pidio y ahora lo recibe. Yo no ando paseando refresco.'", "fb": "Negociar el stock salva la venta."},
    {"cat": "Servicio", "titulo": "Cliente al Telefono", "situacion": "El cliente te ignora por estar hablando por celular.", "E": "(Esperas con sonrisa, confirmas señas de entrega y esperas a que termine para cobrar amablemente).", "R": "(Interrumpes): 'Jefe, firme aqui que ya me tengo que ir.'", "M": "(Gritas para que te haga caso o avientas las cajas).", "fb": "El respeto define el nivel SAC."},
    {"cat": "Operacion", "titulo": "Credito Vencido", "situacion": "Sistema marca bloqueo y el cliente no quiere pagar saldo anterior.", "E": "'Jefe, el sistema no me deja bajar nuevo hasta liberar el saldo. ¿Pagamos el vencido y le dejo lo urgente?'", "R": "'Si no paga no hay refresco. Son reglas de la empresa.'", "M": "'Usted no pago y ahora se amolo. Cuando tenga dinero avise.'", "fb": "Negociar para habilitar es vision de negocio."},
    {"cat": "Servicio", "titulo": "Promocion Faltante", "situacion": "Cliente: 'El preventa me prometio un vaso y no lo traes.'", "E": "'Disculpe, no venia reportado. Dejeme anotar sus datos y reporte este folio para que en la proxima se le entregue.'", "R": "'Eso es con el preventista, yo no traigo regalos hoy.'", "M": "'Seguro le mintio para que pidiera mas.'", "fb": "Asumir la gestion da seguridad."},
    {"cat": "Calidad", "titulo": "Revision Preventiva", "situacion": "Notas producto que vence mañana en su refri.", "E": "'Jefe, note que estas Pepsi vencen pronto. ¿Si gusta se las cambio?'", "R": "'Tiene producto por vencer, jefa. Ahi se lo encargo.'", "M": "(No dices nada y dejas que el producto caduque).", "fb": "La prevencion es la base del SAC."},
    {"cat": "Servicio", "titulo": "Anaqueles Sucios", "situacion": "El area de entrega esta muy sucia.", "E": "'Jefe, voy a limpiar rapido este espacio para que su Pepsi luzca mejor. El orden atrae clientes.'", "R": "'Esta muy sucio aqui, jefa. A ver si para la otra ya tiene limpio.'", "M": "(Bajas el producto sobre la suciedad sin decir nada).", "fb": "Merchandising incluye limpieza."},
    {"cat": "Ventas", "titulo": "Lanzamientos", "situacion": "Llegas con sabor nuevo: 'Eso no se mueve aqui.'", "E": "'Entiendo. GEPP esta invirtiendo mucho en publicidad para esto. Pongamos 3 a la vista para que lo conozcan.'", "R": "'Tomelo por esta vez, si no se vende vemos que hacemos.'", "M": "'Viene obligatorio en su pedido. Lo tiene que recibir.'", "fb": "Promover innovacion ayuda al crecimiento."},
    {"cat": "Logistica", "titulo": "Doble Vuelta", "situacion": "Cliente ocupado: 'Dame una vuelta.'", "E": "'Entiendo. ¿Me permite bajar lo urgente en 5 minutos o paso al final de mi ruta?'", "R": "'Esta bien, le doy la vuelta pero si voy tarde no prometo regresar.'", "M": "'Yo ya no vuelvo a pasar. Reciba ahorita o nos vemos despues.'", "fb": "Flexibilidad con profesionalismo."},
    {"cat": "Operacion", "titulo": "Envase Dañado", "situacion": "Cliente tiene envase muy dañado: 'Cambiamelo.'", "E": "'Con gusto le ayudo a renovar su inventario. Solo dejenme separar los operativos le digo a mi supervisor para que en el cedis no me lo pasen a cobro.'", "R": "'Solo le voy a dejar lo que tiene, pero no le garantizo que los que deje esten mejores.'", "M": "'Yo no soy checador para revisar envases. Le voy a rechazar los garrafones.'", "fb": "Gestion de envase es gestion de activos."},
    {"cat": "Calidad", "titulo": "Envase Sucio Exterior", "situacion": "Cliente: 'El vidrio viene sucio por fuera.'", "E": "'Disculpe. Dejeme limpiarlos ahorita mismo y me aseguro que los proximos vengan impecables.'", "R": "'Es por el manejo en planta. Si quiere le cambio a lata pero es mas caro.'", "M": "'Asi vienen de bodega. Si va querer para no bajarla del camion.'", "fb": "Servicio 360 es cuidar el detalle."}
]

# --- LÓGICA DE NAVEGACIÓN ---
def reset_quiz():
    mezcla = random.sample(BANCO_DATOS, 4)
    quiz_list = []
    for esc in mezcla:
        ops = [{"tipo": "E", "txt": esc["E"], "fb": esc["fb"]}, {"tipo": "R", "txt": esc["R"], "fb": esc["fb"]}, {"tipo": "M", "txt": esc["M"], "fb": esc["fb"]}]
        random.shuffle(ops)
        quiz_list.append({"cat": esc["cat"], "t": esc["titulo"], "s": esc["situacion"], "o": ops})
    st.session_state.quiz = quiz_list
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.paso = 'QUIZ'
    st.session_state.respondido = False

if 'paso' not in st.session_state:
    st.session_state.paso = 'INICIO'

# --- INTERFAZ ---
st.markdown('<div class="gepp-header"><h1>GEPP: CERTIFICACION SAC</h1><p>Excelencia en Entrega Embotellado</p></div>', unsafe_allow_html=True)

if st.session_state.paso == 'INICIO':
    st.subheader("📋 Datos del Certificado")
    st.session_state.nombre = st.text_input("Nombre Completo:", placeholder="Juan Perez")
    st.session_state.ruta = st.text_input("Ruta / Cedis:", placeholder="R-102 / Belenes")
    
    if st.button("COMENZAR EXAMEN"):
        if st.session_state.nombre and st.session_state.ruta:
            reset_quiz()
            st.rerun()
        else:
            st.warning("Debes ingresar nombre y ruta para generar el certificado PDF.")

elif st.session_state.paso == 'QUIZ':
    curr = st.session_state.quiz[st.session_state.idx]
    st.caption(f"Pregunta {st.session_state.idx + 1} de 4")
    st.markdown(f'<div class="scenario-text">"{curr["s"]}"</div>', unsafe_allow_html=True)

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
        if st.session_state.last_type == "E": st.success(f"**EXCELENTE.** {st.session_state.last_fb}")
        elif st.session_state.last_type == "R": st.warning(f"**REGULAR.** {st.session_state.last_fb}")
        else: st.error(f"**MALA DECISION.** {st.session_state.last_fb}")
        
        if st.button("Siguiente ➡️"):
            if st.session_state.idx < 3:
                st.session_state.idx += 1
                st.session_state.respondido = False
                st.rerun()
            else:
                st.session_state.paso = 'FINAL'
                st.rerun()

elif st.session_state.paso == 'FINAL':
    st.balloons()
    score = st.session_state.score
    categoria = "LEYENDA GEPP" if score >= 7 else "PROFESIONAL" if score >= 5 else "EN FORMACION"
    
    st.header("🏁 Examen Finalizado")
    st.metric("Puntuacion", f"{score} / 8")
    st.subheader(f"Nivel Alcanzado: {categoria}")
    
    # Generar PDF
    pdf_bytes = generar_pdf(st.session_state.nombre, st.session_state.ruta, score, categoria, st.session_state.history)
    
    st.download_button(
        label="📥 DESCARGAR CERTIFICADO OFICIAL (PDF)",
        data=pdf_bytes,
        file_name=f"Certificado_GEPP_{st.session_state.nombre.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
    
    if st.button("Reiniciar"):
        st.session_state.paso = 'INICIO'
        st.rerun()
