from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import spark_config
import spark_creditors
import time
import os


def logout():
    menu = driver.find_element_by_xpath('//*[@id="react-menu-root"]/div[1]/div/div[1]/div')
    menu.click()

    sign_out = driver.find_element_by_xpath('//*[@id="react-menu-root"]/div[1]/div/div[2]/div[1]/div[2]/div[4]/div/div[1]')
    sign_out.click()
    

def login():

    print('I am logging in!')
	                                           
    login_form = driver.find_element_by_xpath('/html/body/header/div/div[1]/div[2]/div[2]/div[1]/form/div[1]/input[1]')
    login_form.send_keys(spark_config.LOGIN)
    
    password_form = driver.find_element_by_xpath('/html/body/header/div/div[1]/div[2]/div[2]/div[1]/form/div[1]/input[2]')
    password_form.send_keys(spark_config.PASSWORD)
    
    submit = driver.find_element_by_xpath('/html/body/header/div/div[1]/div[2]/div[2]/div[1]/form/div[1]/button')
    submit.click()
	
    close_window = driver.find_element_by_xpath('//*[@id="view87"]/div/div/div[1]/button')
    close_window.click()


def write_to_file(result):
    f = open('cad.txt', 'a')
    filesize = os.path.getsize('cad.txt')
    if filesize != 0:
        f.write('\n')

    for i in range(len(result)):
        f.write(result[i])
        if i != len(result) - 1:
            f.write('\n')

    f.close()


def load_more():
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
    # driver.execute_script("window.scrollTo(0, 1080);")
    # html = driver.find_element_by_tag_name('html')
    # html.send_keys(Keys.END)
    print('load_more!')
    

def get_statements(id, start):
    index = start
    result = []
    already_loaded_more = False
    driver.find_element_by_xpath('//*[@id="{id}"]/div/div[2]/table/tbody/tr/td/table[2]/thead/tr'.format(id=id)).click()
    
    while True:
        try:
            row = driver.find_element_by_xpath('//*[@id="{id}"]/div/div[2]/table/tbody/tr/td/table[2]/tbody/tr[{index}]/td[2]/div/button'.format(id=id, index=index))
            row.click()
            
            tr = 1
            while True:
                try:
                    driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/table[1]/tbody/tr[{tr}]'.format(tr=tr))
                    statement = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/table[1]/tbody/tr[{tr}]/td[1]'.format(tr=tr)).text
                    if statement == 'Регистрационный номер':
                        statement = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/table[1]/tbody/tr[{tr}]/td[2]'.format(tr=tr)).text
                        break
                    tr += 1
                except:
                    statement = 'None'
                    break
            
            close = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[1]/button')
            close.click()
            
            print('{index}. {statement}'.format(index=index, statement=statement))
            write_to_file([statement])
            result.append(statement)
            index += 1
            already_loaded_more = False
            
        except:
            if not already_loaded_more:
                load_more()
                # already_loaded_more = True
                continue
            else:
                break
    
    return result
            

def search(creditor, start):
    search_form = driver.find_element_by_xpath('//*[@id="react-root"]/div[1]/div[1]/div/div/div/div[1]/div/div[1]/div/span/input')
    search_form.clear()
    time.sleep(1)
    search_form.send_keys(creditor)
    
    driver.implicitly_wait(5)
    
    submit = driver.find_element_by_xpath('//*[@id="react-root"]/div[1]/div[1]/div/div/div/div[1]/div/div[1]/div/div[4]/button')
    submit.click()
    
    try:
        link = driver.find_element_by_xpath('//*[@id="react-root"]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/a').get_attribute('href')
    except:
        print('No elements for {0}'.format(creditor))
        return False
    
    driver.get(link)
    id = link.split('/')[-2]
    button = 2
    while True:
        try:
            razdel = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/div/div[5]/div/div[2]/div[2]/div/div[1]/div/div[4]/button[{0}]/div/div/span'.format(button)).text
            if razdel == 'Залоги':
                zalogi = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/div/div[5]/div/div[2]/div[2]/div/div[1]/div/div[4]/button[{0}]'.format(button))
                zalogi.click()
                break
            else:
                button += 1
        except:
            print('Did not find "Залоги"!')
            return False

    tr = 1
    while True:
        try:
            zalog = driver.find_element_by_xpath('//*[@id="{id}"]/div/div[2]/table/tbody/tr/td/table[2]/tbody/tr[{tr}]/td[1]/div'.format(id=id, tr=tr)).text
            if zalog == 'Физические лица':
                deistvuet = driver.find_element_by_xpath('//*[@id="{id}"]/div/div[2]/table/tbody/tr/td/table[2]/tbody/tr[{tr}]/td[2]/div/button'.format(id=id, tr=tr))
                deistvuet.click()
                break
            tr += 1
        except:
            deistvuet = driver.find_element_by_xpath('//*[@id="{id}"]/div/div[2]/table/tbody/tr/td/table[1]/tbody/tr/td/div[2]/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/button'.format(id=id))
            deistvuet.click()
    
    result = get_statements(id, start)
    # write_to_file(result)
    
    return {'Number of statements': len(result), 'Statements': result}
    
    
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://www.spark-interfax.ru/')
    driver.implicitly_wait(1000)
    driver.maximize_window()
    
    login()
    for creditor in spark_creditors.creditors:
        result = search(creditor, spark_creditors.creditors[creditor])
        if result != False:
            print('All OK: {0} ({1})'.format(creditor, result['Number of statements']))
        else:
            print('Something went wrong with {0}'.format(creditor))
        driver.get('https://www.spark-interfax.ru/system/#/dashboard')
        
    logout()
    driver.quit()
    