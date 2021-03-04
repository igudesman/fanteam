from selenium import webdriver
from time import sleep

from chrome_config import get_chromedriver
import proxies


def generate_numbers(base_kad, first, last):
	last_num = int(last.split(':')[-1])
	first_num = int(first.split(':')[-1])
	
	count = last_num - first_num
	f = open('cad_numbers.txt', 'a')
	for i in range(count + 1):
		kad = base_kad + ':' + str(first_num + i) + '\n'
		f.write(kad)
	f.write('\n')
	f.close()

	
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


def main():
	proxy_index = 0
	proxy_index, driver = get_new_proxy(proxy_index)
	driver.implicitly_wait(0.1)
	
	page = 0
	row = 1

	while True:
		driver.implicitly_wait(1)
		driver.get('https://rosreestr.base-n.ru/reestr/16-tatarskij/16:50-kazanskij/?page={page}'.format(page=page))
		print('Page: {0}; Row: {1}'.format(page, row))
		try:
			# print(driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/table/tbody/tr[{row}]/td[2]/div'.format(row=row)).text)
			if 'объектов нет' in driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/table/tbody/tr[{row}]/td[2]/div'.format(row=row)).text:
				row += 1
				print('Объектов нет')
				continue
			base_kad = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/table/tbody/tr[{row}]/td[1]/div'.format(row=row)).text
			oks = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/table/tbody/tr[{row}]/td[2]/div/a'.format(row=row)).get_attribute('href')
			oks += '?page=0'
			
			driver.get(oks)	
			starting_kad = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/table/tbody/tr[1]/td[1]/div/a').text
			
		except:
			if 'заблокирован' in driver.find_element_by_xpath('/html/body').text:
				driver.quit()
				proxy_index, driver = get_new_proxy(proxy_index)
				sleep(1)
				continue

			page += 1
			driver.get('https://rosreestr.base-n.ru/reestr/16-tatarskij/16:50-kazanskij/?page={page}'.format(page=page))
			try:
				error = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/h1').text
				if error == 'Ошибка 404':
					break
			except:
				row = 1
				continue
		
		try:
			last_page = driver.find_element_by_xpath('/html/body/div/div[4]/div[3]/div/div[1]/div[1]/ul/li[5]/a').get_attribute('href')
			driver.get(last_page)
		except:
			pass

		driver.implicitly_wait(0.1)
		first_page_row = 50
		while first_page_row > 0:
			# print(first_page_row)
			try:
				last_kad_number = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/table/tbody/tr[{first_page_row}]/td[1]/div/a'.format(first_page_row=first_page_row)).text
				break
			except:
				first_page_row -= 1
		
		if first_page_row == 0:
			last_kad_number = starting_kad
		
		# print('Generating!')
		generate_numbers(base_kad, starting_kad, last_kad_number)
		print('Done with {0}!'.format(base_kad))
		row += 1
				
	
if __name__ == '__main__':
	main()