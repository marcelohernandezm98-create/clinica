import streamlit as st
import time
import pandas as pd
import os
# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="GEPP - Simulador de Ruta", page_icon="🚛", layout="centered")
# --- BASE DE DATOS LOCAL ---
DB_FILE = "leaderboard_gepp_v3.csv"
def cargar_leaderboard():
   if os.path.exists(DB_FILE):
       return pd.read_csv(DB_FILE)
   else:
       return pd.DataFrame(columns=["Nombre", "Ruta", "Grupo", "Puntaje"])
def guardar_puntaje(nombre, ruta, grupo, puntaje):
   df = cargar_leaderboard()
   nuevo_registro = pd.DataFrame([[nombre, ruta, grupo, puntaje]], columns=["Nombre", "Ruta", "Grupo", "Puntaje"])
   df = pd.concat([df, nuevo_registro], ignore_index=True)
   df = df.sort_values(by="Puntaje", ascending=False)
   df.to_csv(DB_FILE, index=False)
# --- ESTILOS ---
st.markdown("""
<style>
   .stApp { background-color: #f8f9fa; }
   .gepp-header {
       background: linear-gradient(90deg, #004B93 0%, #002d5a 100%);
       padding: 1.5rem; border-radius: 15px; color: white; text-align: center;
       border-bottom: 6px solid #C9002B; margin-bottom: 20px;
   }
   .timer-box {
       font-size: 28px; font-weight: bold; text-align: center;
       padding: 10px; border-radius: 10px; border: 3px solid #004B93;
       background-color: white; margin-bottom: 15px;
   }
   .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; min-height: 4em; white-space: normal; }
</style>
   """, unsafe_allow_html=True)
# --- ESCENARIOS ---
ESCENARIOS = [
   {
       "titulo": "Escenario 1: El Pedido No Reconocido",
       "situacion": "El cliente dice: '¡Yo no pedí estas 10 cajas! No las voy a recibir porque yo no las anoté.'",
       "opciones": [
           {"texto": "'Entiendo jefe, pudo ser un error de comunicación. ¿Qué le parece si dejamos solo lo básico para que no pierda venta este fin de semana?'", "puntos": 1.0, "feedback": "¡EXCELENTE! Usaste empatía y salvaste la venta con el mínimo indispensable."},
           {"texto": "'Bueno patrón, si no quiere las 10, déjeme ver si le puedo bajar nada más 5 para que no se quede sin producto.'", "puntos": 0.5, "feedback": "REGULAR. Intentaste negociar volumen, pero te faltó empatía para calmar la molestia del cliente."},
           {"texto": "'Pues aquí en mi liquidación dice que sí las pidió. Yo ya las bajé y no las voy a volver a subir.'", "puntos": 0.0, "feedback": "MALA. Confrontar al cliente destruye la relación y genera quejas en el CEDI."},
           {"texto": "'No se preocupe, me las llevo de regreso. Al rato le aviso a la oficina que usted no quiso el pedido.'", "puntos": 0.0, "feedback": "MALA. Te rendiste de inmediato. Un Agente GEPP siempre busca alternativas antes de retirar producto."}
       ]
   },
   {
       "titulo": "Escenario 2: La Objeción del Dinero",
       "situacion": "Llegas a la tienda y te dicen: 'No tengo dinero joven, la semana estuvo muy sola. Venga la próxima vuelta.'",
       "opciones": [
           {"texto": "'Lo entiendo jefe. Pero viene el calor fuerte. ¿Le dejo solo una cajita de Pepsi 600ml y Agua para que no se le vayan los clientes con la competencia?'", "puntos": 1.0, "feedback": "¡EXCELENTE! Aplicaste la Venta Sugestiva enfocada en el beneficio del cliente (el calor)."},
           {"texto": "'¿No tiene ni para un garrafón? Déjeme le dejo uno aunque sea para que no pierda la continuidad.'", "puntos": 0.5, "feedback": "REGULAR. El cliente no debe comprar por 'ayudarte', sino porque lo necesita."},
           {"texto": "'Está bien patrón, lo entiendo. Nos vemos la próxima semana. Suerte con su venta.'", "puntos": 0.0, "feedback": "MALA. Aceptaste el primer 'No'. Dejaste la puerta abierta para que la competencia llene ese espacio."},
           {"texto": "'Si no me paga hoy ya no voy a poder pasar el jueves porque me descuentan a mí el tiempo.'", "puntos": 0.0, "feedback": "MALA. Usar amenazas o problemas personales para presionar la venta es poco profesional."}
       ]
   },
   {
       "titulo": "Escenario 3: Anticipación con Epura",
       "situacion": "En un domicilio/tienda te dicen: 'Hoy no me deje agua, joven. Todavía tengo medio garrafón y no quiero gastar ahorita.'",
       "opciones": [
           {"texto": "'Tiene razón jefa. Pero acuérdese que yo paso hasta el martes. ¿Le dejo uno de reserva de una vez para que no ande cargando después?'", "puntos": 1.0, "feedback": "¡EXCELENTE! La anticipación ahorra esfuerzo al cliente y asegura tu venta del fin de semana."},
           {"texto": "'Ándele jefa, déjeme uno para que me ayude con mi cuota de hoy.'", "puntos": 0.5, "feedback": "REGULAR. El cliente no debe comprar por 'ayudarte', sino porque lo necesita."},
           {"texto": "'Sale, luego no me ande llamando de urgencia porque no voy a poder dar la vuelta extra.'", "puntos": 0.0, "feedback": "MALA. El servicio nunca debe usarse como castigo o amenaza."},
           {"texto": "'Está bien, me sigo con el vecino que él sí me pidió varios.'", "puntos": 0.0, "feedback": "MALA. Comparar a los clientes o ser sarcástico daña la imagen de marca GEPP."}
       ]
   },
   {
       "titulo": "Escenario 4: Problemas de Caducidad (Falla de Preventa)",
       "situacion": "El cliente está molesto: 'No te voy a recibir el pedido. Le dije al preventa que tengo 2 cajas por caducar y no me mandó el cambio. Hasta que no se las lleven, no quiero nada nuevo.'",
       "opciones": [
           {"texto": "'Le ofrezco una disculpa, jefe. Déjeme reportarlo ahorita mismo con el supervisor para que quede registro. Recíbame este producto nuevo para que no pierda venta y yo me comprometo personalmente a que el jueves sin falta se soluciona lo de sus cajas.'", "puntos": 1.0, "feedback": "¡EXCELENTE! Te hiciste responsable, diste una solución inmediata y aseguraste que el cliente se quedara con el producto nuevo."},
           {"texto": "'El preventa es el que se encarga de eso, a mí no me aparece el cambio en el sistema. Pero si gusta déjeme el pedido y yo le digo a él que pase a verla mañana.'", "puntos": 0.5, "feedback": "REGULAR. Aunque intentas dejar el pedido, le echaste la culpa al compañero y no diste una garantía real de solución."},
           {"texto": "'Si no me recibe el pedido me lo tengo que llevar todo y le voy a tener que cancelar su cuenta por hoy. Es problema de usted y del preventa.'", "puntos": 0.0, "feedback": "MALA. Fuiste grosero y confrontativo. Perdiste la venta y el cliente se quedó muy enojado con la marca."},
           {"texto": "'Está bien jefa, si no hay cambio no hay venta. Me llevo el pedido de regreso al CEDI.'", "puntos": 0.0, "feedback": "MALA. Te rendiste fácilmente. Un Agente GEPP debe negociar para que el producto nuevo entre a la tienda a pesar de los errores administrativos."}
       ]
   }
]
# --- LÓGICA DE ESTADOS ---
if 'paso' not in st.session_state: st.session_state.paso = 'INICIO'
if 'puntaje' not in st.session_state: st.session_state.puntaje = 0.0
if 'indice' not in st.session_state: st.session_state.indice = 0
def finalizar_pregunta(puntos, feedback):
   st.session_state.puntaje += puntos
   st.session_state.feedback = feedback
   st.session_state.puntos_obtenidos = puntos
   st.session_state.paso = 'FEEDBACK'
   st.rerun()
# --- INTERFAZ ---
st.markdown('<div class="gepp-header"><h1>GEPP: DESAFÍO DE RUTA 2026 🚛</h1></div>', unsafe_allow_html=True)
if st.session_state.paso == 'INICIO':
   st.subheader("🚀 ¡Bienvenido al Entrenamiento de Agentes!")
   st.write("Analiza cada situación. Tu objetivo es mantener la venta y el servicio al cliente.")
   st.info("⏱️ Tienes **20 segundos** para responder a cada cliente.")
   if st.button("COMENZAR RUTA"):
       st.session_state.paso = 'JUEGO'
       st.rerun()
elif st.session_state.paso == 'JUEGO':
   actual = ESCENARIOS[st.session_state.indice]
   st.progress(st.session_state.indice / len(ESCENARIOS))
   placeholder_timer = st.empty()
   st.markdown(f"### {actual['titulo']}")
   st.warning(f"**SITUACIÓN:** {actual['situacion']}")
   for i, opcion in enumerate(actual['opciones']):
       if st.button(opcion['texto'], key=f"btn_{i}"):
           finalizar_pregunta(opcion['puntos'], opcion['feedback'])
   for t in range(20, -1, -1):
       color = "red" if t <= 5 else "#004B93"
       placeholder_timer.markdown(f"<div class='timer-box' style='color: {color};'>⏳ {t}s</div>", unsafe_allow_html=True)
       time.sleep(1)
       if t == 0:
           finalizar_pregunta(0.0, "⏱️ ¡TIEMPO AGOTADO! El cliente se desesperó y canceló el pedido.")
elif st.session_state.paso == 'FEEDBACK':
   if st.session_state.puntos_obtenidos == 1.0:
       st.success(f"### ⭐ Puntos: 1.0\n{st.session_state.feedback}")
   elif st.session_state.puntos_obtenidos == 0.5:
       st.warning(f"### ⚡ Puntos: 0.5\n{st.session_state.feedback}")
   else:
       st.error(f"### ❌ Puntos: 0.0\n{st.session_state.feedback}")
   if st.button("SIGUIENTE CLIENTE"):
       if st.session_state.indice < len(ESCENARIOS) - 1:
           st.session_state.indice += 1
           st.session_state.paso = 'JUEGO'
       else:
           st.session_state.paso = 'REGISTRO'
       st.rerun()
elif st.session_state.paso == 'REGISTRO':
   st.header("🏁 Fin de la Jornada")
   st.metric("Puntuación Total", f"{st.session_state.puntaje} / {len(ESCENARIOS)}")
   with st.form("registro"):
       nombre = st.text_input("Nombre del Agente:")
       ruta = st.text_input("Número de Ruta:")
       grupo = st.text_input("Grupo / CEDI:")
       if st.form_submit_button("GUARDAR RESULTADOS"):
           if nombre and ruta and grupo:
               guardar_puntaje(nombre, ruta, grupo, st.session_state.puntaje)
               st.session_state.paso = 'LEADERBOARD'
               st.rerun()
           else:
               st.error("Por favor completa los campos.")
elif st.session_state.paso == 'LEADERBOARD':
   st.header("🏆 Mejores Agentes de la Zona")
   df = cargar_leaderboard()
   st.dataframe(df.head(10), use_container_width=True)
   if st.button("REINICIAR ENTRENAMIENTO"):
       st.session_state.paso = 'INICIO'
       st.session_state.puntaje = 0.0
       st.session_state.indice = 0
       st.rerun()
