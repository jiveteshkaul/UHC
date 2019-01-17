from selenium import webdriver
import time
import sys
import traceback
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json

def get_pdf(driver):
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="skip-to-main-content"]/div/div[3]/div[1]/a')))
    driver.find_element_by_xpath('//*[@id="skip-to-main-content"]/div/div[3]/div[1]/a').click() # click print/email option
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ngdialog2"]/div[2]/div/div/div[2]/div/div/ul/li[2]/a/div[2]')))
    driver.find_element_by_xpath('//*[@id="ngdialog2"]/div[2]/div/div/div[2]/div/div/ul/li[2]/a/div[2]').click() #click email option
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ngdialog2"]/div[2]/div/div/div[2]/div/div/div/form/div[1]/div[1]/input')))
    driver.find_element_by_xpath('//*[@id="ngdialog2"]/div[2]/div/div/div[2]/div/div/div/form/div[1]/div[1]/input').send_keys(mail_rec_1,Keys.TAB,mail_rec_2,Keys.TAB,mail_rec_3,Keys.TAB,mail_rec_4,Keys.ENTER)
    time.sleep(5)


def navigate_to_page(state):
    driver = webdriver.Chrome(chrome_driver_loc)
    driver.get('https://connect.werally.com/plans/allSavers/1') # SITE
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1"]/div[2]/ul/li[2]/h2/div/button')))
    driver.find_element_by_xpath('//*[@id="step-1"]/div[2]/ul/li[2]/h2/div/button').click() # click choice plus
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="changeLocationBtn"]/div[2]/span')))
    driver.find_element_by_xpath('//*[@id="changeLocationBtn"]/div[2]/span').click() # click change location
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="location"]')))
    driver.find_element_by_xpath('//*[@id="location"]').send_keys(state) # send state
    
    time.sleep(8)
    driver.find_element_by_xpath('//*[@id="ngdialog1"]/div[2]/div/div/div/div/div/div/div/location-form/div/autocomplete/div/div/form/div[2]/div/button[2]').click() # click update location
    
    time.sleep(5)
    #WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-0"]/div[3]/div[1]/ul/li[1]/guided-search-link/button/div[1]/img')))
    driver.find_element_by_xpath('//*[@id="step-0"]/div[3]/div[1]/ul/li[1]/guided-search-link/button/div[1]/img').click() # click people
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1"]/div[2]/div[1]/ul/li[1]/guided-search-link/button/div[1]/img')))
    driver.find_element_by_xpath('//*[@id="step-1"]/div[2]/div[1]/ul/li[1]/guided-search-link/button/div[1]/img').click() # click primary care
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-6"]/div[2]/div[1]/ul/li[1]/h2/div/guided-search-link/button')))
    driver.find_element_by_xpath('//*[@id="step-6"]/div[2]/div[1]/ul/li[1]/h2/div/guided-search-link/button').click() # click all primary care physi
    return(driver)


def main():
    global state_from_config, mail_rec_1, mail_rec_2, mail_rec_3, mail_rec_4, chrome_driver_loc
    filename="./UHC_config.json"
    configFile = open(filename)
    root = json.load(configFile)
    configFile.close()
    
    for config in root:
        state_from_config = config['state']
        mail_rec_1=config['mail_receiver_1']
        mail_rec_2=config['mail_receiver_2']
        mail_rec_3=config['mail_receiver_3']
        mail_rec_4=config['mail_receiver_4']
        chrome_driver_loc=config['chrome_driver_location']
    
#capitalize first letter    
    args=state_from_config
    words=args.split(" ")
    state=""
    for item in words:
        state=state+item.capitalize()+" "
             
    chrome_driver=navigate_to_page(state)
    get_pdf(chrome_driver)

    
if __name__=="__main__":
    
    try:
        main()
        print('PDFs Sent successfully via email')
    except Exception as e:
        print(traceback.format_exc())
        print("Error: {0}".format(e))



