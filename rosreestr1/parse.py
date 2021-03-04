from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
from recognize import recognize
import config as conf
import pandas as pd

from chrome_config import get_chromedriver
import proxies


def delete_line(cad):

    a_file = open('cad-numbers.txt', 'r')
    lines = a_file.readlines()
    a_file.close()

    new_file = open('cad-numbers.txt', 'w')
    for line in lines:
        if line.strip("\n") != cad.strip("\n"):
            new_file.write(line)

    new_file.close()
    

def getStatement(cadastralNumber):
    
    cadastralField = driver.find_element_by_xpath('//*[@id="online_request_search_form_span"]/table/tbody/tr[1]/td[1]/table/tbody/tr[3]/td/table[1]/tbody/tr[2]/td[3]/input')
    cadastralField.clear()
    time.sleep(1)
    cadastralField.send_keys(cadastralNumber)
    time.sleep(1)


def RecognizeCaptcha(c):
    img_base64 = driver.execute_script("""var ele = arguments[0];var cnv = document.createElement('canvas');cnv.width = 180; cnv.height = 50;cnv.getContext('2d').drawImage(ele, 0, 0);return cnv.toDataURL('image/png').substring(22);""", c)
    captcha = recognize(img_base64)
    return captcha


def getCaptcha():

    while (True):
    
        img = driver.find_element_by_xpath('//*[@id="captchaImage2"]')
        captcha_input = driver.find_element_by_xpath('//*[@id="online_request_search_form_span"]/table/tbody/tr[1]/td[1]/table/tbody/tr[3]/td/table[2]/tbody/tr[6]/td[3]/table/tbody/tr/td[2]/div[1]/input')
        send_button = driver.find_element_by_xpath('//*[@id="submit-button"]')
        reload_captcha = driver.find_element_by_xpath('//*[@id="online_request_search_form_span"]/table/tbody/tr[1]/td[1]/table/tbody/tr[3]/td/table[2]/tbody/tr[6]/td[3]/table/tbody/tr/td[2]/span')
        
        try:
            captcha = RecognizeCaptcha(img)
        except:
            reload_captcha.click()
            continue
            
        if ((captcha != None) and (captcha != 'empty image')):
            captcha_input.send_keys(captcha)
            time.sleep(0.5)
            send_button.click()

            try:
                PopUp = driver.find_element_by_xpath('//*[@id="layoutContainers"]/div[4]/div/div[2]/section/div[2]/div[2]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/span')
                reload_captcha.click()
                continue
            except:
                break
        else:
            reload_captcha.click()
    
    
    found = False
    try:
        no_elements = driver.find_element_by_xpath('//*[@id="layoutContainers"]/div[4]/div/div[2]/section/div[2]/div[2]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td')
    except:
        found = True
    
    return found
        

def get_info(cad_number):

    object = driver.find_element_by_xpath('//*[@id="js_oTr0"]/td[1]/a')
    object.click()
    
    more = driver.find_element_by_xpath('//*[@id="sw_r_enc"]').click()
    
    index = 3
    data = {'Кадастровый номер': [], 'Право': [], 'Ограничение': []}
    pravo = ''
    ogran = ''
    try:
        restrictions = driver.find_element_by_xpath('//*[@id="sw_r_enc"]')
    except:
        return data
        

    while True:
        try:
            row = driver.find_element_by_xpath('//*[@id="r_enc"]/table/tbody/tr[{index}]'.format(index=index))
        except:
            break
            
        law = driver.find_element_by_xpath('//*[@id="r_enc"]/table/tbody/tr[{index}]/td[1]'.format(index=index)).text
        restriction = driver.find_element_by_xpath('//*[@id="r_enc"]/table/tbody/tr[{index}]/td[2]'.format(index=index)).text

        pravo += law + ', '
        ogran += restriction + ', '
        index += 2
    
    data['Кадастровый номер'].append(cad_number)
    data['Право'].append(pravo[:-2:])
    data['Ограничение'].append(ogran[:-2:])
    
    new_request = driver.find_element_by_xpath('//*[@id="js_es_3"]')
    new_request.click()
    
    return data
    

if __name__ == '__main__':

    proxy_list = proxies.proxy_list
    id = proxies.proxy_index
    driver = get_chromedriver(True, None, proxy_list[id]['PROXY_HOST'], proxy_list[id]['PROXY_PORT'], proxy_list[id]['PROXY_USER'], proxy_list[id]['PROXY_PASS'])

    try:
        driver.get('https://rosreestr.gov.ru/wps/portal/online_request')
        driver.implicitly_wait(0.5)
    except:
        print('Сайт Росреестра не работает')

    file = open('cad-numbers.txt', 'r')
    cadastralNumbers = file.readlines()
    # already_proceeded = []

    for cadNum in cadastralNumbers:
        start = time.time()
        found = False
        print('Запрос по объекту {} выполняется...'.format(cadNum))
        
        try:
            getStatement(cadNum)
            found = getCaptcha()
        except:
            pass
        
            
        if found:
            delete_line(cadNum)
            try:
                data = get_info(cadNum)
            except:
                data = {'Кадастровый номер': [], 'Право': [], 'Ограничение': []}
            print(data)
            df = pd.DataFrame(data=data, columns=['Кадастровый номер', 'Право', 'Ограничение'])
            try:
                temp_df = pd.read_csv('data.csv')
                df = pd.concat([temp_df, df], ignore_index=True)
            except:
                pass

            df.to_csv('data.csv', index=False)
        else:
            print('Не найдены данные, удовлетворяющие Вашему запросу. Попробуйте изменить запрос или воспользуйтесь поиском по устаревшим номерам.')
        end = time.time()
        print('Запрос обработан за {} сек.'.format(end - start))


    print('Done!')
    driver.close()