import re
from playwright.sync_api import Page, expect


class ChatbotPage:
    def __init__(self, page: Page, avianca: bool = False, ganaplay: bool = False, econocable: bool = False, mataro: bool = False):
        self.page = page
        self.avianca = avianca
        self.ganaplay = ganaplay
        self.econocable = econocable
        self.mataro = mataro

        if avianca:
            # Chatbot Avianca
            self.frame = page.locator("iframe[name='Ventana de mensajería']").content_frame

        elif ganaplay:
            # Chatbot GanaPlay
            self.frame = page.frame_locator("#cen_ifr_static")
        
        elif econocable:
            # Chatbot Econocable
            self.frame = page.locator("#bim-ifr").content_frame

        elif mataro:
            self.frame = page.frame_locator("iframe[src^='https://cwcentribot.centribal.com']")

        else:
            # Chatbot TMB
            self.textbox_comentario = page.get_by_role("textbox", name=re.compile("escribe tu comentario", re.I))
            self.boton_enviar_comentario = page.get_by_role("button", name=re.compile("enviar comentario", re.I))

    # --- TMB ---
    def enviar_mensaje_tmb(self, texto: str):
        expect(self.textbox_comentario).to_be_visible()
        self.textbox_comentario.click()
        self.textbox_comentario.fill(texto)
        expect(self.boton_enviar_comentario).to_be_visible()
        self.boton_enviar_comentario.click()

    def seleccionar_informacion_transporte(self):
        self.page.get_by_text("Información del transporte").click()
        self.page.wait_for_timeout(2000)
        expect(self.page.get_by_label("chat window").get_by_text("Metro", exact=True)).to_be_visible()
        self.page.get_by_label("chat window").get_by_text("Metro", exact=True).click()
        expect(self.page.get_by_label("chat window").get_by_text("Horarios", exact=True)).to_be_visible()
        self.page.get_by_label("chat window").get_by_text("Horarios", exact=True).click()

    def validar_mensaje_final_tmb(self, mensaje_objetivo: str, timeout: int = 5000) -> bool:
        locator = self.page.get_by_text(mensaje_objetivo)
        try:
            expect(locator).to_be_visible(timeout=timeout)
            return True
        except:
            return False

    # --- Avianca ---
    def enviar_mensaje_avianca(self, texto: str):
        textbox = self.frame.get_by_role("textbox", name="Escriba un mensaje")
        expect(textbox).to_be_visible()
        textbox.click()
        textbox.fill(texto)
        self.frame.get_by_role("button", name="Enviar mensaje").click()

    def click_boton_avianca(self, name: str):
        self.frame.get_by_role("button", name=name).click()

    def validar_mensaje_avianca(self, texto: str, timeout: int = 40000) -> bool:
        try:
            #self.frame.get_by_text(texto).wait_for(timeout=timeout)
            expect(self.frame.get_by_text(re.compile(texto))).to_be_visible(timeout=timeout)
            return True
        except:
            return False

    # --- GanaPlay ---
    def enviar_mensaje_ganaplay(self, texto: str):
        textbox = self.frame.get_by_role("textbox", name="Escribe aquí")
        
        expect(textbox).to_be_visible()
        textbox.click()
        textbox.fill(texto)
        textbox.press("Enter")


    def validar_mensaje_ganaplay(self, texto: str, timeout: int = 80000) -> bool:
        try:
            expect(self.frame.get_by_text(re.compile(texto, re.I))).to_be_visible(timeout=timeout)
            return True
        except:
            return False

# --- Econocable ---
    def abrir_chat_econocable(self):
        boton_ayuda = self.frame.get_by_role("button", name="¿Necesitas ayuda?")
        expect(boton_ayuda).to_be_visible(timeout=10000)
        boton_ayuda.click()
        expect(self.frame.get_by_role("img", name="Agent")).to_be_visible(timeout=10000)

    def enviar_mensaje_econocable(self, texto: str):
        textbox = self.frame.get_by_role("textbox", name="Escribe aquí")
        expect(textbox).to_be_visible(timeout=5000)
        textbox.click()
        textbox.fill(texto)
        textbox.press("Enter")

    def validar_mensaje_econocable(self, texto: str, timeout: int = 10000) -> bool:
        try:
            expect(self.frame.get_by_text(re.compile(texto, re.I))).to_be_visible(timeout=timeout)
            return True
        except:
            return False

# --- Mataró ---
    def abrir_chat_mataro(self):
        boton_ayuda = self.frame.get_by_role("button", name="Necessites ajuda?")
        expect(boton_ayuda).to_be_visible(timeout=10000)
        boton_ayuda.click()
        expect(self.frame.get_by_role("img", name="Agent").first).to_be_visible(timeout=10000)

    def aceptar_terminos_mataro(self):
        self.frame.get_by_role("button", name="Sí acepto.Castellano").click()

    def seleccionar_opcion_mataro(self, opcion: str):
        self.frame.get_by_role("button", name=opcion).click()

    def enviar_mensaje_mataro(self, texto: str):
        textbox = self.frame.get_by_role("textbox", name="Missatge")
        expect(textbox).to_be_visible()
        textbox.click()
        textbox.fill(texto)
        # El botón de enviar no tiene un selector claro, se usa el contenedor.
        self.frame.locator("form div").nth(2).click()

    def validar_mensaje_mataro(self, texto: str, timeout: int = 10000) -> bool:
        try:
            expect(self.frame.get_by_text(re.compile(texto, re.I))).to_be_visible(timeout=timeout)
            return True
        except:
            return False