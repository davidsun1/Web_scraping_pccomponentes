# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 10:10:31 2022

@author: David
"""

import pandas as pd
import re
from bs4 import BeautifulSoup
import os.path

# Problemas scraping desde la web "https://www.pccomponentes.com/tarjetas-graficas"
# así que se ha bajado el archivo html y se trabaja desde aqui
HTMLFile = open("targetas_graficas.htm", "r", encoding="utf8")
index = HTMLFile.read()

sp = BeautifulSoup(index, 'lxml')

# listas paa guardar los campos
name = []
gb = []
gddr = []
price = []
link = []

# re.Pattern de primero los gb y gddr y luego ambos separados
p = re.compile("[0-9]+[\s]*G[B]{0,1}.{0,5} [G]{0,1}DDR.*[0-9]\w*[^\w\s]*")
gb_re = re.compile("[0-9]+\s*G")
gddr_re = re.compile("[\w]*DD[\w\d]*")


# iteramos bs4.element.ResultSet por cada producto y lo añadimos a las listas
for product in sp.find_all('a', {'class':'c-product-card__title-link cy-product-link'}):
   name.append(product.text)
   
   result = p.search(product.text)
   # hay productos que no son targetas gráficas y no tiene gb ni gddr
   if result is None:
         gb.append('NaN')
         gddr.append('NaN')
   else: 
         # extraemos solo el número de las gb
         result_gb = gb_re.search(result.group(0))
         result_gb = re.sub(r'[^\d]', '', result_gb.group(0))
         
         # extraemos el gddr 
         result_gddr = gddr_re.search(result.group(0))
         
         gb.append(result_gb)
         gddr.append(result_gddr.group(0))
         
   price.append(float(product.attrs['data-price']))
   
   link.append(product.attrs['href'])


# Creamos un df
dict1 = {'name': name,'gb': gb,'gddr': gddr, 'price': price, 'link': link} 
df = pd.DataFrame(dict1)

# eliminamos las filas que no sean targetas gráficas
df1 = df[df['gb'] != 'NaN']

# creamos el csv desde el df1
if os.path.exists('grafica.csv'):
      print ("File already exists")
else:
      df1.to_csv('grafica.csv', index=False)
