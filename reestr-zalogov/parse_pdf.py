import tabula
import pandas as pd
import os
import glob

def convert_to_csv(name):
	tabula.convert_into('{0}\\pdfs\\{1}.pdf'.format(os.getcwd(), name), "{0}\\csvs\\{1}.csv".format(os.getcwd(), name), output_format="csv", stream=True, pages='all')
	df = pd.read_csv("{0}\\csvs\\{1}.csv".format(os.getcwd(), name), names=['index', 'key', 'value'], encoding='ANSI')
	os.remove("{0}\\csvs\\{1}.csv".format(os.getcwd(), name))
	return df
	
	# df.to_excel('{0}\\xlsxs\\{1}.xlsx'.format(os.getcwd(), name), index = False)


pdf_paths = glob.glob(os.getcwd() + '\\pdfs\\*.pdf')
pdf_names = [pdf.split('\\')[-1].split('.')[0] for pdf in pdf_paths]

columns_1 = {'VIN': 1, 'PIN': 1, 'Описание транспортного средства': 3, 'Номер шасси (рамы)': 1, 'Номер кузова': 1,
			'Фамилия': 1, 'Имя': 1, 'Отчество': 1, 'Фамилия (латинскими буквами)': 2, 'Имя (латинскими буквами)': 2, 'Отчество (латинскими буквами)': 2, 'Дата рождения': 1, 'Документ, удостоверяющий личность': 3, 'Адрес фактического места жительства в Российской Федерации': 4,
			'Полное наименование': 2, 'ИНН': 1, 'ОГРН': 1, 'Место нахождения': 1, 'Наименование': 0,
			'Дата договора': 1, 'Номер договора': 1, 'Срок исполнения обязательства, обеспеченного залогом движимого имущества': 4
			}

columns_2 = {'VIN': 1, 'PIN': 1, 'Описание транспортного средства': 3, 'Номер шасси (рамы)': 1, 'Номер кузова': 1,
			'Фамилия': 1, 'Имя': 1, 'Отчество': 1, 'Фамилия (латинскими буквами)': 2, 'Имя (латинскими буквами)': 2, 'Отчество (латинскими буквами)': 2, 'Дата рождения': 1, 'Документ, удостоверяющий личность': 3, 'Адрес фактического места жительства в Российской Федерации': 4,
			'Наименование': 1, 'Дата договора': 1, 'Номер договора': 1, 'Срок исполнения обязательства, обеспеченного залогом движимого имущества': 4
			}


data = {}
data['Номер уведомления'] = []
for value in columns_1.keys():
	data[value] = []

for pdf_name in pdf_names:
	print('Выполняется {0}'.format(pdf_name))
	try:
		df = convert_to_csv(pdf_name)
	except:
		print('Проблема с конвертацией в csv!')
		continue
	# print(df['key'])
	# print(df['value'])
	
	result = {}
	key_starts = -1
	key = ''
	value = ''
	row = 0
	
	while row < len(df['key']):
		# print(df['key'][row])
		if df['key'].isnull()[row]:
			row += 1
			continue
		elif df['key'][row][0].isupper():
			if key_starts == -1:
				key_starts = row
			else:
				while key_starts < row and not (df['value'].isnull()[key_starts] and df['key'].isnull()[key_starts]):
					# print(row)
					value += str(df['value'][key_starts]) + ' '
					key += str(df['key'][key_starts]) + ' '
					key_starts += 1
				result[key] = value
				value = ''
				key = ''
				key_starts = row
		else:
			pass
		
		row += 1
	
	key_starts = -1	
	row = 0
	while row < len(df['key']):
		if df['index'].isnull()[row]:
			row += 1
			continue
		elif df['index'][row][0].isupper():
			if key_starts == -1:
				key_starts = row
			else:
				while key_starts < row and not (df['index'].isnull()[key_starts] and df['key'].isnull()[key_starts]):
					# print(row)
					value += str(df['key'][key_starts]) + ' '
					key += str(df['index'][key_starts]) + ' '
					key_starts += 1
				result[key] = value
				value = ''
				key = ''
				key_starts = row
		else:
			pass
		
		row += 1
	
	if key_starts != row:
		while key_starts < row and not (df['index'].isnull()[key_starts] and df['key'].isnull()[key_starts]):
			# print(row)
			value += str(df['key'][key_starts]) + ' '
			key += str(df['index'][key_starts]) + ' '
			key_starts += 1
		result[key] = value
		

	result2 = {}
	for k in result:
		new_key = k.replace('nan', '')
		result2[new_key] = result[k].replace('nan', '')
	
	for dk in list(data.keys()):
		found = False
		for rk in list(result2.keys()):
			if dk in rk:
				found = True
				data[dk].append(result2[rk])
				break
		if not found:
			data[dk].append(' ')
	data['Номер уведомления'][-1] = pdf_name
		
	# if (len(df['key']) == 35) or (len(df['key']) == 36):
	#     if len(df['key']) == 36:
	#         columns_1['Описание транспортного средства'] = 4
	#     index = 0
	#     for column in columns_1:
	#         if index > 28:
	#             data[column].append(df['key'][index])
	#             index += columns_1[column]
	#         else:
	#             data[column].append(df['value'][index])
	#             index += columns_1[column]
	#     data['Номер уведомления'].append(pdf_name)
	#     data['Наименование'][-1] = 'None'
	#     os.remove('{0}\\pdfs\\{1}.pdf'.format(os.getcwd(), pdf_name))
	# elif len(df['key']) == 31:
	#     index = 0
	#     for column in columns_2:
	#         if index > 23:
	#             data[column].append(df['key'][index])
	#             index += columns_2[column]
	#         else:
	#             data[column].append(df['value'][index])
	#             index += columns_2[column]
	#     data['Номер уведомления'].append(pdf_name)
		
	#     data['Полное наименование'].append('None')
	#     data['ИНН'].append('None')
	#     data['ОГРН'].append('None')
	#     data['Место нахождения'].append('None')
	#     os.remove('{0}\\pdfs\\{1}.pdf'.format(os.getcwd(), pdf_name))
	# else:
	#     print('Длина листа неизветсна: {0}!'.format(len(df['key'])))

print('Создание csv и exel файлов')
# for row in data:
#    print('{0}: {1}'.format(row, data[row]))
result_df = pd.DataFrame(data, columns=data.keys())     

try:
	data = pd.read_csv('{0}\\csvs\\data.csv'.format(os.getcwd()))
	result_df = pd.concat([data, result_df], ignore_index=True)
except:
	pass

result_df.to_csv('{0}\\csvs\\data.csv'.format(os.getcwd()), index=False, encoding='utf-8')
result_df.to_excel('{0}\\xlsxs\\data.xlsx'.format(os.getcwd())) 
