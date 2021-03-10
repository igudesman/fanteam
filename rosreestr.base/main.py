from selenium import webdriver
from time import sleep


def next_page():
	driver.find_element_by_xpath('/html/body/div/div[4]/div[3]/div/div[1]/div[1]/ul/li[8]/a').click()


driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get('https://rosreestr.base-n.ru/reestr/16-tatarskij/16:50-kazanskij/')

oks = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/table/tbody/tr[1]/td[2]/div/a').get_attribute('href')
driver.get(oks)

move_to_first = driver.find_element_by_xpath('/html/body/div/div[4]/div[3]/div/div[1]/div[1]/ul/li[1]/a')
move_to_first.click()

index = 1
while True:
	try:
		if index == 51:
			index = 1
			next_page()
	except:
		print('No more pages!')
		
	try:
		cad_number = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/table/tbody/tr[{0}]/td[1]/div/a'.format(index)).text
		print(cad_number)
		sleep(5)
	except:
		print('Oops!')
	
	index += 1