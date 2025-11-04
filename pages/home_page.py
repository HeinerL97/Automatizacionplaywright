import re
from playwright.sync_api import Page, expect

class HomePage:
    def __init__(self, page: Page):
        self.page = page

        # --- Avianca ---
        self.main_content_avianca = page.get_by_role("contentinfo", name="Site")
        self.accept_button = page.get_by_role("button", name="Aceptar")
        self.fixed_button = page.locator("#fixedButton")
        self.terms_checkbox = page.locator("#termsCheckbox")
        self.start_chat_button = page.get_by_role("button", name="Iniciar Chat")

        # --- TMB ---
        self.main_content_tmb = page.get_by_role("main", name="Contenido principal")
        self.accept_cookies_button_tmb = page.get_by_role("button", name=re.compile("Aceptar todas las cookies", re.I))
        self.chatbot_button_tmb = page.get_by_role("button", name=re.compile("chatbot TMBbot", re.I))

        # --- GanaPlay ---
        self.menu_button = page.locator("#openMenu")
        self.chat_item = page.locator("#menuMobile").get_by_role("listitem").filter(has_text="Chat")

        # --- Econocable ---
        self.econocable_iframe = page.locator("#bim-ifr")

        # --- Mataró ---
        self.main_content_mataro = page.get_by_role("main", name="Contenido principal")
        self.close_popup_button_mataro = page.get_by_role("button", name="Cerrar.")
        self.accept_cookies_button_mataro = page.get_by_text("Acepto")

    # --- Avianca ---
    def open_avianca(self):
        self.page.goto("https://www.avianca.com/es/")
        expect(self.main_content_avianca).to_be_visible()

    def accept_cookies_avianca(self):
        self.accept_button.click()

    def open_fixed_button(self):
        self.fixed_button.click()

    def accept_terms_and_start_chat(self):
        self.terms_checkbox.check()
        self.start_chat_button.click()

    # --- TMB ---
    def open_tmb(self):
        self.page.goto("https://www.tmb.cat/es/home")
        expect(self.main_content_tmb).to_be_visible()

    def accept_cookies_tmb(self):
        self.accept_cookies_button_tmb.click()

    def open_chatbot_tmb(self):
        self.chatbot_button_tmb.click()

    # --- GanaPlay ---
    def open_ganaplay(self):
        self.page.goto("https://ganaplay.sv/")
        expect(self.page.get_by_role("button", name=re.compile("MÁS", re.I))).to_be_visible(timeout=15000)

    def open_chat_ganaplay(self):
        self.menu_button.click()
        self.chat_item.click()

    # --- Econocable ---
    def open_econocable(self):
        self.page.goto("https://www.econocable.com/terminosycondicionesmicable/")
        expect(self.econocable_iframe).to_be_visible(timeout=15000)

    # --- Mataró ---
    def open_mataro(self):
        self.page.goto("https://www.mataro.cat/?set_language=es")
        expect(self.main_content_mataro).to_be_visible()

    def close_popup_mataro(self):
        self.close_popup_button_mataro.click()

    def accept_cookies_mataro(self):
        self.accept_cookies_button_mataro.click()
