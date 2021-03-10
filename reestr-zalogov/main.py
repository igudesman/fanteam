from selenium import webdriver
from selenium.webdriver import ActionChains

from time import sleep
import random
import os

from chrome_config import get_chromedriver
import proxies
                

def restart(driver):
    driver.maximize_window()
    actionChains = ActionChains(driver)
    driver.implicitly_wait(10)
    
    driver.get('https://www.reestr-zalogov.ru/search/index')
    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://antcpt.com/rus/information/demo-form/recaptcha-3-test-score.html')
    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get('https://accounts.google.com/')
    
    driver.switch_to.window(driver.window_handles[0])


def move_mouse(driver):
    canvas = driver.find_element_by_xpath('//*[@id="find-btn"]')
    action = ActionChains(driver) 
    action.move_to_element(canvas) 
    action.click()
    action.move_by_offset(8,1) 
    action.move_by_offset(6,1) 
    action.move_by_offset(4,1) 
    action.move_by_offset(2,1) 
    action.move_by_offset(1,1) 
    action.move_by_offset(1,2) 
    action.move_by_offset(1,4) 
    action.move_by_offset(1,6) 
    action.move_by_offset(1,8) 
    action.release() 
    action.perform()
    
    
def prevent_captcha():
    
    check_status = driver.find_element_by_xpath('//*[@id="menu"]/div[1]/a')
    check_status.click()
    sleep(random.uniform(2, 3))
    move_mouse()
    back = driver.find_element_by_xpath('//*[@id="menu"]/div[3]/a')
    back.click()
    sleep(random.uniform(2, 3))
    
    info = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[2]/div/div[1]/ul/li[2]/a')
    info.click()
    sleep(random.uniform(1, 2))
    move_mouse()
    back = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[2]/div/div[1]/ul/li[1]/a')
    back.click()
    
    
def get_new_proxy(id):
    proxy_list = proxies.proxy_list
    print(proxy_list)
    if id == len(proxy_list):
        print('Own IP')
        driver = get_chromedriver()
        id = 0
    else:
        id %= len(proxy_list)
        print(proxy_list[id]['PROXY_HOST'])
        driver = get_chromedriver(True, None, proxy_list[id]['PROXY_HOST'], proxy_list[id]['PROXY_PORT'], proxy_list[id]['PROXY_USER'], proxy_list[id]['PROXY_PASS'])
        id += 1
    return id, driver

    
def count_files():
    path, dirs, files = next(os.walk(os.getcwd() + '/pdfs'))
    file_count = len(files)
    return file_count
    
    
if __name__ == '__main__':

    
    proxy_index = 0
    
    proxy_index, driver = get_new_proxy(proxy_index)
    restart(driver)

    file = open('cad.txt', 'r')
    cadastralNumbers = file.readlines()

    cadastrals = [cad for cad in cadastralNumbers]
    already_proceeded = []
        
    
    index = 0
    while index < len(cadastrals):

        files = count_files()
        cad = cadastrals[index]
        if cad in already_proceeded:
            index += 1
            continue
            
        print(cad)
        sleep(3)
        try:
            sleep(random.uniform(2, 3))
            input = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[2]/div/div[2]/div/form/div[1]/div[2]/input')
            input.clear()
            sleep(1)
            input.send_keys(cad.rstrip())
            sleep(random.uniform(2, 3))

            find = driver.find_element_by_xpath('//*[@id="find-btn"]').click()
            sleep(random.uniform(2, 3))
                
            download_pdf = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[2]/div/div[2]/table/tbody/tr/td[3]/span[1]')
            download_pdf.click()
            sleep(random.uniform(4, 5))
            
            back = driver.find_element_by_xpath('//*[@id="back-btn"]')
            back.click()
            
            if count_files() != files + 1:
                print('ERROR')
                driver.quit()
                proxy_index, driver = get_new_proxy(proxy_index)
                restart(driver)
                continue
            
            already_proceeded.append(cad)
            index += 1
            
            with open('cad.txt', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('cad.txt', 'w') as fout:
                fout.writelines(data[1:])
            
        except:
            print('DETECTED!')
            tab = 3
            while True:
                try:
                    driver.switch_to.window(driver.window_handles[tab])
                    driver.close()
                    tab += 1
                except:
                    break
            driver.switch_to.window(driver.window_handles[0])
            
            
            driver.quit()
            proxy_index, driver = get_new_proxy(proxy_index)
            restart(driver)
            
            
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[3])
            driver.get('https://www.expressvpn.com/what-is-my-ip')
            sleep(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.get('https://www.reestr-zalogov.ru/search/index')
            
    driver.quit()
