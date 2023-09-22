import pandas as pd
import requests as rq
from bs4 import BeautifulSoup


def busca_vaga(nome_vaga):
  HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
  #URL Linkedin
  url = f'https://www.linkedin.com/jobs/search/?currentJobId=3707657236&distance=25&f_TPR=r86400&geoId=105818291&keywords={nome_vaga}&location=Belo%20Horizonte%2C%20Minas%20Gerais%2C%20Brasil&originalSubdomain=br&sortBy=DD'

  #requisção
  r = rq.get(url, headers=HEADER)
  print('\n', r.status_code, ":::", url,'\n')

  soup = BeautifulSoup(r.text, 'html.parser')

  box_resultado = soup.find_all('div',class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

  lista_info_vagas = []

  for resultado in box_resultado:
    info_vagas = {}
    info_vagas['Empresa'] = resultado.find('a',class_="hidden-nested-link").text.strip()
    info_vagas['Link'] = resultado.find('a',class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]")['href']
    info_vagas['Cargo'] = resultado.find('h3', class_="base-search-card__title").text.strip()
    info_vagas['Local'] = resultado.find('span', class_="job-search-card__location").text.strip()
    info_vagas['Abertura'] = resultado.find('time').text.strip()
    #info_vagas['Abertura'] = resultado.find('time', class_="job-search-card__listdate").text.strip()

    lista_info_vagas.append(info_vagas)

  return lista_info_vagas

cargo = ["atendimento", "B2C", "supervisor", "B2B", "vendedor", "customer%20experience", "customer%20success", "Analista%20de%20BackOffice", "coordenador"]

#dados para planilha
plan = {'Empresa':[],
'Link':[],
'Cargo':[],
'Local':[],
'Abertura':[]}

for nome in cargo:
  var_ = busca_vaga(nome)
  for i in var_:
    plan['Empresa'].append(i['Empresa'])
    plan['Link'].append(i['Link'])
    plan['Cargo'].append(i['Cargo'])
    plan['Local'].append(i['Local'])
    plan['Abertura'].append(i['Abertura'])

dataframe = pd.DataFrame(plan)
dataframe.to_excel('vagas1.xlsx')

