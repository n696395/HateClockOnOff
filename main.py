import logging
import configparser
import datetime
import platform
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

URL = "https://URL/index.php?menuaction=timeclock.uitimeclock.index"
USER_NAME = ""
PASSWORD = ""
STATE = ""
OS_NAME = platform.system()

#log config
log_filename = datetime.datetime.now().strftime(".//log//%Y-%m-%d_%H_%M_%S.log")
logging.basicConfig(format='%(asctime)s-%(levelname)s:%(message)s',
                    filename=log_filename,
                    datefmt='%m-%d %H:%M:%S',
                    level=logging.INFO
                    )
logging.info("Start program, OS is " + OS_NAME)

#Get Config
config = configparser.ConfigParser() 
config.read('config.ini')
USER_NAME = config['Account']['USER_NAME']
PASSWORD = config['Account']['PASSWORD']
#STATE = config['Account']['STATE']
logging.info("Load config successed.")

# Start webdriver
if OS_NAME == "Windows":
    browser = webdriver.PhantomJS(".//phantomjs//windows//phantomjs.exe")
elif OS_NAME == "Linux":
    if "32" in platform.architecture()[0]:
        browser = webdriver.PhantomJS(".//phantomjs//linux//x86//phantomjs")
    else: #64
        browser = webdriver.PhantomJS(".//phantomjs//linux//x64//phantomjs")
elif OS_NAME == "Darwin": # MacOS
    browser = webdriver.PhantomJS(".//phantomjs//mac//phantomjs")
browser.get(URL)

# login
browser.find_element_by_name("login").send_keys(USER_NAME)
browser.find_element_by_name("passwd").send_keys(PASSWORD)
browser.find_element_by_name("submit_button").submit()

#wait page load
wait = ui.WebDriverWait(browser,20)
wait.until(lambda browser: browser.find_element_by_name("status_item").is_displayed)
logging.info("Login successed.")

#determine in/out, AM=in and PM=out
if datetime.datetime.now().strftime("%p").upper() == "AM":
    STATE = "in"
elif datetime.datetime.now().strftime("%p").upper() == "PM":
    STATE = "out"

#select in/out
selectOptions = Select(browser.find_element_by_name("status_item")) 
selectOptions.select_by_value(STATE.lower())#上班=in,下班=out
logging.info("Select "+ STATE +".")

#sumit
browser.find_element_by_id("submit_button").click()
logging.info("Sumited")

browser.save_screenshot(datetime.datetime.now().strftime(".//screenshot//%Y-%m-%d_%H_%M_%S.jpg"))
logging.info("Close browser")
browser.quit()
