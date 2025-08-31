import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class IECAdminPanel:
    def __init__(self):
        # Initialize Chrome driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://www.igrejaemcontagem.com.br"

    def access_site(self, url):
        self.driver.get(url)

    def login(self, username, password):
        """
        Logs into the IEC Admin Panel using provided username and password.
        """
        self.access_site(self.base_url + "/admin")

        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input')

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

    def add_pregacao(self, link, title, description, publish_date, preacher_name):
        """
        Adds a new pregacao (sermon) into the admin panel.
        """
        self.access_site(self.base_url + "/admin/pregacoes/pregacao/add/")
        
        publish_date = datetime.strptime(publish_date, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')

        link_field = self.wait.until(EC.presence_of_element_located((By.ID, 'id_youtube_link')))
        preacher_field = Select(self.driver.find_element(By.ID, 'id_preletor'))
        location_field = Select(self.driver.find_element(By.ID, 'id_local'))
        title_field = self.driver.find_element(By.ID, 'id_titulo')
        description_field = self.driver.find_element(By.ID, 'id_resumo')
        date_field = self.driver.find_element(By.ID, 'id_data_pregacao')
        save_button = self.driver.find_element(By.NAME, '_save')
        publicado_checkbox = self.driver.find_element(By.ID, 'id_publicado')

        link_field.send_keys(link)
        location_field.select_by_index(1)

        try:
            preacher_field.select_by_visible_text(preacher_name)
        except:
            preacher_field.select_by_index(1)

        title_field.send_keys(title)
        description_field.send_keys(description)
        date_field.send_keys(publish_date)

        if not publicado_checkbox.is_selected():
            publicado_checkbox.click()

        time.sleep(2)

        save_button.click()

        time.sleep(5)

    def close(self):
        """
        Closes the WebDriver.
        """
        self.driver.quit()
