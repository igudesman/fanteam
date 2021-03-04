from bs4 import BeautifulSoup
import os
import pandas as pd

def xml_to_exel():
	data = {
		'CadastralBlock': [], 'RegDate': [], 'adrsNote': [], 'FamilyName': [], 
		'FirstName': [], 'Patronymic': [], 'CadastralCost': []
	}
	
	dir_name = os.getcwd()
	extension = '.xml'
	

	for item in os.listdir(dir_name):
		if item.endswith(extension):
			print(item)
			file_name = os.path.abspath(item)
			xml_parser = BeautifulSoup(open(file_name, encoding='utf-8'), 'xml')
			try:
				data['CadastralBlock'].append(xml_parser.find('CadastralBlock').contents[0])
			except:
				data['CadastralBlock'].append('')
				
			try:
				data['RegDate'].append(xml_parser.find('RegDate').contents[0])
			except:
				data['RegDate'].append('')
				
			try:
				data['adrsNote'].append(xml_parser.find('adrs:Note').contents[0])
			except:
				data['adrsNote'].append('')
				
				
			try:
				data['FamilyName'].append(xml_parser.find('FamilyName').contents[0])
			except:
				data['FamilyName'].append('')
				
			try:
				data['FirstName'].append(xml_parser.find('FirstName').contents[0])
			except:
				data['FirstName'].append('')
				
			try:
				data['Patronymic'].append(xml_parser.find('Patronymic').contents[0])
			except:
				data['Patronymic'].append('')
				
			try:
				data['CadastralCost'].append(xml_parser.find('CadastralCost').get('Value'))
			except:
				data['CadastralCost'].append('')
			
			os.remove(file_name)



	result_df = pd.DataFrame(data, columns=data.keys())     

	try:
		data = pd.read_csv('data.csv')
		result_df = pd.concat([data, result_df], ignore_index=True)
	except:
		pass

	result_df.to_csv('data.csv', index=False, encoding='utf-8')
	result_df.to_excel('data.xlsx') 

