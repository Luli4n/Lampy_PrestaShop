# coding=utf8
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

driver = webdriver.Chrome(r'C:\Users\Julian.Krabel\OneDrive - IHS Markit\Desktop\BE\Lampy_PrestaShop\scripts\ImportSeleniumScript\seleniumdriver\win\chromedriver.exe')
driver.maximize_window()
driver.get("http://localhost/admin007k7wti0/")
assert "Imperium Lamp" in driver.title
emailbox = driver.find_element(By.ID,"email")
emailbox.clear()
emailbox.send_keys("julekkrabel@gmail.com")
passwordbox = driver.find_element(By.ID,"passwd")
passwordbox.clear()
passwordbox.send_keys("rootroot")
passwordbox.send_keys(Keys.RETURN)

delay = 6
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID,"subtab-AdminImport")))
    print ("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

nav = driver.find_element(By.ID,"nav-sidebar")

driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", nav)


driver.find_elements(By.CSS_SELECTOR, ".material-icons.mi-settings_applications")[0].click()
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, 'Importuj')))
    print ("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", nav)

driver.find_element(By.LINK_TEXT, 'Importuj').click()

category = Select(driver.find_element(By.ID, 'entity'))
category.select_by_value('1')

driver.find_element(By.ID,"file").send_keys(os.getcwd()+"\productsInCSV.csv")
driver.implicitly_wait(0.5)

element = driver.find_element(By.CSS_SELECTOR,"[for='truncate_1']")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

element.click()

submit_button = driver.find_element(By.NAME, "submitImportFile")

submit_button.click()
driver.switch_to.alert.accept()

importConfig = Select(driver.find_element(By.ID,"valueImportMatchs"))
importConfig.select_by_visible_text("domyslny")

driver.find_element(By.ID,"loadImportMatchs").click()

driver.find_element(By.ID,"import").click()

close_button = WebDriverWait(driver, 200).until(
EC.element_to_be_clickable((By.ID, "import_close_button")))

driver.close()
