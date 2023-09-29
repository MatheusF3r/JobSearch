import support
import pandas as pd

cargo = ["atendimento", "B2C",
         "supervisor", "B2B",
         "vendedor", "customer%20experience",
         "customer%20success", "Analista%20de%20BackOffice",
         "coordenador"]

plan = {'Empresa':[],
'Link':[],
'Cargo':[],
'Local':[],
'Salário':[],
'Abertura':[],
'Tempo log':[]}

for nome in cargo:
  var_ = support.busca_vaga(nome)
  for i in var_:
    plan['Empresa'].append(i['Empresa'])
    plan['Link'].append(i['Link'])
    plan['Cargo'].append(i['Cargo'])
    plan['Local'].append(i['Local'])
    plan['Salário'].append(i['Salário'])
    plan['Abertura'].append(i['Abertura'])
    plan['Tempo log'].append(i['Horário da vaga'])

support.bd(plan)

dataframe = pd.read_excel('vagas.xlsx')
for i, vagas in enumerate(dataframe['Empresa']):
  empresa = dataframe.loc[i, 'Empresa']
  cargo = dataframe.loc[i, 'Cargo']
  salario = dataframe.loc[i,'Salário']
  local = dataframe.loc[i, 'Local']
  link = dataframe.loc[i, 'Link']
  try:
    if salario > 1.500:
      print(f'EMPRESA: {empresa} \n CARGO: {cargo} \n SALÁRIO: {salario} \n LOCAL: {local} \n LINK: {link} \n')
  except TypeError as erro:
    print(f'EMPRESA: {empresa} \n CARGO: {cargo} \n SALÁRIO: {salario} \n LOCAL: {local} \n LINK: {link} \n')
