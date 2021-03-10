from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
from recognize import recognize
import config as conf

from chrome_config import get_chromedriver
import proxies


def delete_line(l):

    a_file = open('cad-numbers.txt', 'r', encoding="utf8")
    lines = a_file.readlines()
    a_file.close()

    new_file = open('cad-numbers.txt', 'w', encoding="utf8")
    for line in lines:
        if line.strip("\n") != l.strip("\n"):
            new_file.write(line)

    new_file.close()


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def wait(t):
    items = list(range(0, t))
    l = len(items)

    # Initial call to print 0% progress
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(1)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        

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


def set_region(region):
    
    print(region)
    menu = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div')
    menu.click()
    prev = driver.find_element_by_xpath('//*[@id="VAADIN_COMBOBOX_OPTIONLIST"]/div/div[1]/span')
    next = driver.find_element_by_xpath('//*[@id="VAADIN_COMBOBOX_OPTIONLIST"]/div/div[3]/span')
    
    page = driver.find_element_by_xpath('//*[@id="VAADIN_COMBOBOX_OPTIONLIST"]/div/div[4]').text
    while '1-9' not in page:
        prev.click()
        time.sleep(2)
        page = driver.find_element_by_xpath('//*[@id="VAADIN_COMBOBOX_OPTIONLIST"]/div/div[4]').text

    index = 1
    while True:
        try:
            reg = driver.find_element_by_xpath('//*[@id="VAADIN_COMBOBOX_OPTIONLIST"]/div/div[2]/table/tbody/tr[{index}]/td/span'.format(index=index))
            if region in reg.text:
                reg.click()
                time.sleep(1)
                return True
            
            index += 1
            if index > 10:
                next.click()
                time.sleep(2)
                index = 1
        except:
            return False
    

# Authorization is required!
def getStatement(cadastralNumber, region):

    ERROR = False

    findObject = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div[1]/div/div/span')
    findObject.click()
    
    time.sleep(5)
    
        
    while True:
        try:
            if ERROR:
                break
            
            object = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[5]/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/div/div')
            object.click()
            break
        except:
            cadastralField = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/input')
            cadastralField.clear()
            cadastralField.send_keys(cadastralNumber)

            time.sleep(1)
            
            status = set_region(region)
            if not status:
                return True
            
            # regionField = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/input')
            # regionField.click()
            # regionField.send_keys('Республика Татарстан')
            time.sleep(5)

            try:
                findButton = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/div/div/span/span')
                findButton.click()
            except:
                continue
                
            count = 0
            driver.implicitly_wait(1)
            while count < 10:
                try:
                    error = driver.find_element_by_xpath('/html/body/div[3]/div/div/h1').text
                    ERROR = True
                    break
                except:
                    count += 1
                    time.sleep(1)
            driver.implicitly_wait(5)
    
    return ERROR
            
        

def RecognizeCaptcha(c):
    img_base64 = driver.execute_script("""var ele = arguments[0];var cnv = document.createElement('canvas');cnv.width = 180; cnv.height = 50;cnv.getContext('2d').drawImage(ele, 0, 0);return cnv.toDataURL('image/png').substring(22);""", c)
    captcha = recognize(img_base64)
    return captcha

def getCaptcha():

    vapp = driver.find_element_by_css_selector("div.v-app")
    CaptchaReload = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[2]/div/div')
    CaptchaField = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/div/input')
    SendButton = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[4]/div/div/div/div[1]/div/div/div/div[1]/div/div')
    img = driver.find_element_by_xpath('//*[@id="v-Z7_01HA1A42KODT90AR30VLN22003"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/div/img')

    while (True):
        captcha = RecognizeCaptcha(img)
        if ((captcha != None) and (captcha != 'empty image')):
            CaptchaField.send_keys(captcha)
            time.sleep(1)
            SendButton.click()

            time.sleep(1)

            PopUp = vapp.find_elements_by_xpath("//div[@class='v-window']")

            if (len(PopUp) != 0):
                OkButton = PopUp[0].find_elements_by_xpath("//span[contains(@class,'v-button-caption') and contains(text(),'Продолжить работу')]")[0]
                OkButton.click()
                wait(conf.TIMEOUT)
                break
        else:
            CaptchaReload.click()


if __name__ == '__main__':

    proxy_list = proxies.proxy_list
    id = proxies.proxy_index
    driver = get_chromedriver(True, None, proxy_list[id]['PROXY_HOST'], proxy_list[id]['PROXY_PORT'], proxy_list[id]['PROXY_USER'], proxy_list[id]['PROXY_PASS'])
    driver.implicitly_wait(5)

    try:
        driver.get('https://rosreestr.ru/wps/portal/p/cc_present/ir_egrn')
    except:
        print('Сайт Росреестра не работает')

    file = open('cad-numbers.txt', encoding="utf8")
    cadastralNumbers = file.readlines()
    file.close()
    authorization(conf.TOKEN)


    for line in cadastralNumbers:
        line = line.replace('\n', '')
        cadNum = line.split(',')[0]
        region = line.split(',')[1]
    
        print('###################################')
        start = time.time()
        print('Запрос по объекту {} выполняется...'.format(line))
        try:
            status = getStatement(cadNum, region)
        except:
            print('Ошибка!')
            continue

        if status:
            print('Не найдены данные, удовлетворяющие Вашему запросу.')
            driver.get('https://rosreestr.gov.ru/wps/portal/p/cc_present/ir_egrn')
            continue
            
        try:
            getCaptcha()
            delete_line(line)
        except:
            print('Ошибка прохождения капчи!')
            continue
        end = time.time()
        print('Запрос обработан за {} сек.'.format(end - start - conf.TIMEOUT))

    driver.close()