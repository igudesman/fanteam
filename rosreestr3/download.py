from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import config as conf
import zipfile

from parse_xml import xml_to_exel
        

def authorization(token):
    splittedToken = token.split('-')
    tokenFields = ['//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/div/input',
                   '//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[3]/div/input',
                   '//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[5]/div/input',
                   '//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[7]/div/input',
                   '//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[9]/div/input']
    for i in range(5):
        tokenField = driver.find_element_by_xpath(tokenFields[i])
        tokenField.send_keys(Keys.CONTROL, 'a')
        tokenField.send_keys(Keys.BACKSPACE)
        tokenField.send_keys(splittedToken[i])
        time.sleep(0.1)

    loginButton = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/span/span')
    loginButton.click()

    try:
        closeButton = driver.find_element_by_xpath('/html/body/div[3]/div/div')
        closeButton.click()
        authorization(token)
    except:
        pass
        

def next_page():
    next_button = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[4]/div/div/div/div/div[1]/div/div/div/div[5]/div/div')
    class_name = next_button.get_attribute('class')
    if 'disabled' in class_name:
        return False
    else:
        next_button.click()
        time.sleep(5)
        return True

        
def download():
    my_requests = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/span/span')
    my_requests.click()
    
    time.sleep(5)
    
    element = 1
    while True:
        try:
            temp = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr[{element}]'.format(element=element))
            # print('ELEMENT: ', element)
        except:
            ok = next_page()
            if ok:
                element = 1
                continue
            else:
                print('Done!')
                break 
                
        status = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr[{element}]/td[3]/div/div/div/div[1]/div/div'.format(element=element)).text
        # print('ELEMENT: ', status)
        if 'Завершена' not in status:
            element += 1
            continue
        
        print('Downloading element: ', element)
        download_button = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr[{element}]/td[4]/div/div/a'.format(element=element))
        download_button.click()
        
        element += 1


def unzip():

    dir_name = os.getcwd() + '/requests'
    extension = '.zip'

    os.chdir(dir_name) # change directory from working dir to dir with files

    for item in os.listdir(dir_name): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(dir_name) # extract file to dir
            zip_ref.close() # close file
            os.remove(file_name) # delete zipped file
    
    extension = '.zip.sig'
    for item in os.listdir(dir_name): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            os.remove(file_name) # delete zipped file
    
    
    extension = '.zip'
    for item in os.listdir(dir_name): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(dir_name) # extract file to dir
            zip_ref.close() # close file
            os.remove(file_name) # delete zipped file


if __name__ == '__main__':

    current_dir = os.getcwd()   

    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : current_dir + r'\requests'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(5)

    try:
        driver.get('https://rosreestr.ru/wps/portal/p/cc_present/ir_egrn')
    except:
        print('Сайт Росреестра не работает')

    authorization(conf.TOKEN)
    download()
    unzip()
    xml_to_exel()

#driver.close()