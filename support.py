from datetime import datetime, timezone, timedelta

import requests as rq
from bs4 import BeautifulSoup
import urllib

import pandas as pd



def tempo():
  tempo_atual = datetime.now(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M:%S') #log
  hora_atual = datetime.now(timezone(timedelta(hours=-3))).strftime('%H:%M') #exceução
  return tempo_atual, hora_atual



def busca_glassdoor(link= str()):
  HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
  URL = f"https://webcache.googleusercontent.com/search?q=cache:{link}"
  r = rq.get(URL, headers=HEADER)
  if 'https://www.google.com/sorry' in r.url:
    salario = r.url ############################ TROCAR PARA: 'Erro recaptcha'
    return salario, True
  else:
    soup = BeautifulSoup(r.content, 'html.parser')
    box_resultado = soup.find('div', class_=" gd-ui-module css-rntt2a ec4dwm00")
    try:
      box_texto = soup.find('div', class_="d-flex align-items-baseline").find('h2').text
      #salario = float(box_texto[box_texto.find('R$')+2:box_texto.find(' ')])
      salario = box_texto
      return salario, True
    except AttributeError as erro:
      salario = erro
      return salario, True # Sem informações salariais não sera inserido no bd



def busca_indeed(link= str()):
  HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
  URL = f"https://webcache.googleusercontent.com/search?q=cache:{link}"
  r = rq.get(URL, headers=HEADER)
  if 'https://www.google.com/sorry' in r.url:
    salario = r.url ############################ TROCAR PARA: 'Erro recaptcha'
    return salario, True
  else:
    soup = BeautifulSoup(r.content, 'html.parser')
    box_resultado = soup.find('div', class_='css-kveeyw eu4oa1w0')
    try:
      box_texto = box_resultado.find('span', class_="cmp-SalarySummaryAverage-salary cmp-SalarySummaryAverage-salary--summary css-mfbg43 e1wnkr790").text
      salario = float(box_texto.replace('R$',''))
      return salario, True
    except AttributeError as erro:
      salario = erro
      return salario, True # Sem informações salariais não sera inserido no bd



def busca_salario(cargo= str(), empresa= str()):
  HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
  URL = f'https://www.google.com.br/search?q={urllib.parse.quote(f"Salario + {cargo} + {empresa}")}'
  r = rq.get(URL, headers=HEADER)
  resultados = dict() ###
  soup = BeautifulSoup(r.content, 'html.parser')
  box_resultado = soup.find('div', class_='s6JM6d').find_all('div', class_='MjjYud')
  for resultado in box_resultado:
    try:
      a = resultado.find('a')['href']
    except (TypeError, AttributeError) as erro:
      try:
        box_resultado = soup.find('div', class_="V3FYCf").find('div',class_="yuRUbf")
        a = resultado.find('a')['href']
      except (TypeError, AttributeError) as erro:
        a = erro
    #try: retornar depois dos testes
    if 'https://www.glassdoor.com.br/' in a:
      salario = busca_glassdoor(a)
      if salario[1]:
        resultados[a] = salario[0]
      else:
        resultados[a] = salario[0]
    elif 'https://br.indeed.com' in a:
      salario = busca_indeed(a)
      if salario[1]:
        resultados[a] = salario[0]
      else:
        resultados[a] = salario[0]
    else:
      
      return 'Não localizada informações salariais.', True #####
    #except TypeError as erro: retornar depois dos testes
      salario = erro
      return salario, True
  for v in resultados.values():
    if ' ' != v:
      return v, True



def busca_vaga(nome_vaga):
  HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
  url = f'https://www.linkedin.com/jobs/search/?currentJobId=3707657236&distance=25&f_TPR=r86400&geoId=105818291&keywords={nome_vaga}&location=Belo%20Horizonte%2C%20Minas%20Gerais%2C%20Brasil&originalSubdomain=br&sortBy=DD'
  r = rq.get(url, headers=HEADER)
  print(r.url)
  soup = BeautifulSoup(r.text, 'html.parser')
  box_resultado = soup.find_all('div', class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")
  lista_info_vagas = []
  for resultado in box_resultado:
    info_vagas = {}
    empresa = resultado.find('a',class_="hidden-nested-link").text.strip()
    link = resultado.find('a',class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]")['href']
    cargo = resultado.find('h3', class_="base-search-card__title").text.strip()
    local = resultado.find('span', class_="job-search-card__location").text.strip()
    abertura = resultado.find('time').text.strip()
    tempo_, _ = tempo()
    salario = busca_salario(cargo, empresa)

    try:
      if salario[1]:
        info_vagas['Empresa'] = empresa
        info_vagas['Link'] = link
        info_vagas['Cargo'] = cargo
        info_vagas['Salário'] = salario[0]
        info_vagas['Local'] = local
        info_vagas['Abertura'] = abertura
        info_vagas['Horário da vaga'] = tempo_
        lista_info_vagas.append(info_vagas)
      else: 
        None
    except:
      None
  return lista_info_vagas



def bd(plan = dict()):
  try: #verifica se a planilha existe
    df_original = pd.read_excel('vagas.xlsx')
    plan_convertida_df = pd.DataFrame.from_dict(plan) #converte a planilha em df
    df = pd.merge(plan_convertida_df, df_original, how = 'outer') #mescla ambas planilhas
    df.to_excel('vagas.xlsx', index=False)
    return 2
  except FileNotFoundError: #caso nao exista, cria
    plan_convertida_df = pd.DataFrame.from_dict(plan) #converte a planilha em df
    plan_convertida_df.to_excel('vagas.xlsx', index=False)
    return 1
  else:
    return 0
