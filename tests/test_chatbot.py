import re
import allure
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.chatbot_page import ChatbotPage

# ---------------------- TMB ----------------------
@allure.feature("Chatbot TMB")
@allure.story("Validación de mensaje final")
@allure.title("Prueba Chatbot TMB")
def test_chatbot_TMB(page: Page):
    home = HomePage(page)
    chatbot = ChatbotPage(page)

    with allure.step("Abrir página principal TMB"):
        home.open_tmb()
        allure.attach(page.screenshot(), name="pantalla_inicial", attachment_type=allure.attachment_type.PNG)

    with allure.step("Aceptar cookies y abrir chatbot"):
        home.accept_cookies_tmb()
        page.wait_for_timeout(500)
        home.open_chatbot_tmb()
        allure.attach(page.screenshot(), name="chatbot_abierto", attachment_type=allure.attachment_type.PNG)

    with allure.step("Enviar mensaje 'hola'"):
        chatbot.enviar_mensaje_tmb("hola")
        allure.attach(page.screenshot(), name="mensaje_hola", attachment_type=allure.attachment_type.PNG)

    with allure.step("Seleccionar Información del transporte"):
        chatbot.seleccionar_informacion_transporte()
        allure.attach(page.screenshot(), name="info_transporte", attachment_type=allure.attachment_type.PNG)

    with allure.step("Enviar mensaje 'gracias'"):
        page.wait_for_timeout(2000)
        chatbot.enviar_mensaje_tmb("gracias")
        allure.attach(page.screenshot(), name="mensaje_gracias", attachment_type=allure.attachment_type.PNG)

    with allure.step("Validar mensaje final"):
        mensaje_objetivo = "¡Muchas gracias a ti!"
        assert chatbot.validar_mensaje_final_tmb(mensaje_objetivo), f"No se encontró el mensaje: '{mensaje_objetivo}'"
        allure.attach(page.screenshot(), name="mensaje_final", attachment_type=allure.attachment_type.PNG)


#----- Avianca -----
@allure.feature("Chatbot Avianca")
@allure.story("Validación de flujo completo")
@allure.title("Prueba Chatbot Avianca")
def test_chatbot_Avianca(page: Page):
    chatbot = ChatbotPage(page, avianca=True) 
    home = HomePage(page)
    chatbot = ChatbotPage(page, avianca=True)

    with allure.step("Abrir página Avianca"):
        home.open_avianca()
        allure.attach(page.screenshot(), name="pantalla_inicial", attachment_type=allure.attachment_type.PNG)

    with allure.step("Aceptar cookies"):
        home.accept_cookies_avianca()
        allure.attach(page.screenshot(), name="cookies_aceptadas", attachment_type=allure.attachment_type.PNG)
        page.wait_for_timeout(500)

    with allure.step("Abrir chat"):
        page.wait_for_timeout(500)
        home.open_fixed_button()
        page.locator("#termsCheckbox").check()
        home.accept_terms_and_start_chat()
        allure.attach(page.screenshot(), name="chat_iniciado", attachment_type=allure.attachment_type.PNG)

    with allure.step("Enviar mensaje 'hola'"):
        chatbot.enviar_mensaje_avianca("hola")
        allure.attach(page.screenshot(), name="mensaje_hola", attachment_type=allure.attachment_type.PNG)

    with allure.step("Validar mensaje de bienvenida y continuar"):
        assert chatbot.validar_mensaje_avianca("¡Hola! 𝗦𝗼𝘆 𝗩𝗶𝗮𝗻𝗰𝗮"), "No apareció el mensaje de bienvenida"
        chatbot.click_boton_avianca("Continuar sin LifeMiles")
        assert chatbot.validar_mensaje_avianca("Por favor dime cuál es tu"), "No apareció la solicitud de correo"
        allure.attach(page.screenshot(), name="mensaje_bienvenida", attachment_type=allure.attachment_type.PNG)

    with allure.step("Enviar correo"):
        chatbot.enviar_mensaje_avianca("h.leonardo321@gmail.com")
        allure.attach(page.screenshot(), name="correo_enviado", attachment_type=allure.attachment_type.PNG)

    with allure.step("Tengo una consulta LifeMiles"):
        chatbot.click_boton_avianca("Tengo una consulta LifeMiles")
        assert chatbot.validar_mensaje_avianca("LifeMiles es un programa de lealtad"), "No apareció LifeMiles es un programa de lealtad"
        allure.attach(page.screenshot(), name="consulta_lifemiles", attachment_type=allure.attachment_type.PNG)

    with allure.step("Volver al menú principal"):
        chatbot.click_boton_avianca("Volver al menú principal")
        allure.attach(page.screenshot(), name="menu_principal", attachment_type=allure.attachment_type.PNG)

    with allure.step("Validar mensaje final '¡Gracias por preferirnos!'"):
        assert chatbot.validar_mensaje_avianca("¡Gracias por preferirnos!"), "No apareció el mensaje final"
        allure.attach(page.screenshot(), name="mensaje_final", attachment_type=allure.attachment_type.PNG)

# ---------------------- GanaPlay ----------------------
@allure.feature("Chatbot GanaPlay")
@allure.story("Validación de flujo completo")
@allure.title("Prueba Chatbot GanaPlay")
def test_chatbot_Ganaplay(page: Page):
    home = HomePage(page)
    chatbot = ChatbotPage(page, ganaplay=True)

    with allure.step("Abrir página principal GanaPlay"):
        home.open_ganaplay()
        page.wait_for_timeout(4000)
        allure.attach(page.screenshot(), name="pantalla_inicial", attachment_type=allure.attachment_type.PNG)

    with allure.step("Abrir chat"):
        home.open_chat_ganaplay()
        page.wait_for_timeout(4000)
        allure.attach(page.screenshot(), name="chat_abierto", attachment_type=allure.attachment_type.PNG)

    with allure.step("Enviar saludo"):
        chatbot.enviar_mensaje_ganaplay("hola")
        allure.attach(page.screenshot(), name="mensajes_enviados_saludar", attachment_type=allure.attachment_type.PNG)
        page.wait_for_timeout(2000)
        chatbot.enviar_mensaje_ganaplay("heiner")
        allure.attach(page.screenshot(), name="mensajes_enviados_Nombre", attachment_type=allure.attachment_type.PNG)
        page.wait_for_timeout(5000)
        chatbot.enviar_mensaje_ganaplay("h.leonardo321@gmail.com")
        allure.attach(page.screenshot(), name="mensajes_enviados_Correo", attachment_type=allure.attachment_type.PNG)
        page.wait_for_timeout(5000)
        chatbot.enviar_mensaje_ganaplay("registrar")
        allure.attach(page.screenshot(), name="mensajes_enviados_registrar", attachment_type=allure.attachment_type.PNG)
        page.wait_for_timeout(5000)
        chatbot.enviar_mensaje_ganaplay("gracias")
        allure.attach(page.screenshot(), name="mensajes_enviados_gracias", attachment_type=allure.attachment_type.PNG)
        page.wait_for_timeout(2000)
        allure.attach(page.screenshot(), name="mensajes_enviados", attachment_type=allure.attachment_type.PNG)

    with allure.step("Validar mensaje final"):
        assert chatbot.validar_mensaje_ganaplay(r"¡Es un gusto atenderle!"), "No se encontró el mensaje esperado"
        allure.attach(page.screenshot(), name="mensaje_final", attachment_type=allure.attachment_type.PNG)

# ---------------------- Econocable ----------------------
@allure.feature("Chatbot Econocable")
@allure.story("Validación de flujo de conversación")
@allure.title("Prueba Chatbot Econocable")
def test_chatbot_Econocable(page: Page):
    home = HomePage(page)
    chatbot = ChatbotPage(page, econocable=True)

    with allure.step("Abrir página Econocable"):
        home.open_econocable()
        page.wait_for_timeout(500)
        allure.attach(page.screenshot(), name="pantalla_inicial", attachment_type=allure.attachment_type.PNG)

    with allure.step("Abrir el chat"):
        chatbot.abrir_chat_econocable()
        page.wait_for_timeout(500)
        allure.attach(page.screenshot(), name="chat_abierto", attachment_type=allure.attachment_type.PNG)

    with allure.step("Enviar mensajes de prueba"):
        chatbot.enviar_mensaje_econocable("hola")
        allure.attach(page.screenshot(), name="mensajes_saludo", attachment_type=allure.attachment_type.PNG)
        page.wait_for_timeout(2000)
        chatbot.enviar_mensaje_econocable("leo")
        page.wait_for_timeout(500)
        allure.attach(page.screenshot(), name="mensajes_enviados", attachment_type=allure.attachment_type.PNG)

    with allure.step("Validar mensaje '¿Es usted cliente'"):
        assert chatbot.validar_mensaje_econocable("¿Es usted cliente?"), "No se encontró el mensaje esperado"
        page.wait_for_timeout(500)
        allure.attach(page.screenshot(), name="mensaje_validado", attachment_type=allure.attachment_type.PNG)

# ---------------------- Mataró ----------------------
@allure.feature("Chatbot Mataró")
@allure.story("Validación de flujo de conversación")
@allure.title("Prueba Chatbot Mataró")
def test_chatbot_Mataro(page: Page):
    home = HomePage(page)
    chatbot = ChatbotPage(page, mataro=True)

    with allure.step("Abrir página Mataró"):
        home.open_mataro()
        allure.attach(page.screenshot(), name="pantalla_inicial", attachment_type=allure.attachment_type.PNG)

    with allure.step("Cerrar pop-up y aceptar cookies"):
        home.close_popup_mataro()
        home.accept_cookies_mataro()
        allure.attach(page.screenshot(), name="cookies_aceptadas", attachment_type=allure.attachment_type.PNG)

    with allure.step("Abrir el chat y aceptar términos"):
        chatbot.abrir_chat_mataro()
        page.wait_for_timeout(5000)
        chatbot.aceptar_terminos_mataro()
        allure.attach(page.screenshot(), name="chat_abierto_terminos_aceptados", attachment_type=allure.attachment_type.PNG)

    with allure.step("Seleccionar 'Calendario Fiscal'"):
        chatbot.seleccionar_opcion_mataro("Calendario Fiscal")
        link_locator = chatbot.frame.get_by_role("link", name="http://www.mataro.cat/short/6O")
        expect(link_locator, "No se encontró el enlace del calendario fiscal").to_be_visible()
        allure.attach(page.screenshot(), name="opcion_calendario_fiscal", attachment_type=allure.attachment_type.PNG)

    with allure.step("Enviar mensaje de agradecimiento"):
        chatbot.enviar_mensaje_mataro("gracias")
        page.wait_for_timeout(5000)
        allure.attach(page.screenshot(), name="mensaje_gracias", attachment_type=allure.attachment_type.PNG)

    with allure.step("Validar mensaje final"):
        mensaje_objetivo = "👍 Moltes gràcies per"
        assert chatbot.validar_mensaje_mataro(mensaje_objetivo), f"No se encontró el mensaje: '{mensaje_objetivo}'"
        allure.attach(page.screenshot(), name="mensaje_final_validacion", attachment_type=allure.attachment_type.PNG)
