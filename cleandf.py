import pandas as pd
import numpy as np
import re

headers = ["Cena", "Model", "Negocjacja", "Lokalizacja", "Rok_produkcji", 
           "Przebieg", "Pojemnosc_silnika", "Typ_paliwa"]

df = pd.read_csv("otomoto.csv",
		     sep = ',', engine = 'python',
                 names = headers)
df.describe()
df.shape

df.dtypes
df.info
df.isnull().sum()

#change str into numeric
#pojemnosc w cm3

npoj = df["Pojemnosc_silnika"].str[:-3]
npoj = npoj.str.replace(' ','')
df.drop(columns=["Pojemnosc_silnika"], inplace = True)
df["Pojemnosc_silnika"] = npoj
df["Pojemnosc_silnika"] = pd.to_numeric(df["Pojemnosc_silnika"])

#Przebieg
przeb = df["Przebieg"].str[:-3]
przeb = przeb.str.replace(' ','')
df.drop(columns=["Przebieg"], inplace = True)
df["Przebieg"] = przeb
df["Przebieg"] = pd.to_numeric(df["Przebieg"])

#Cena
cena = df["Cena"].str[:-3]
waluta = df["Cena"].str[-3:]
df.drop(columns=["Cena"],inplace = True)
df["Cena"] = cena
df["Cena"] = df["Cena"].str.replace(',','.')
df["Cena"] = pd.to_numeric(df["Cena"])
df["Waluta"] = waluta

#podstawowe statystyki zmiennych ilosciowych
df.describe()

# text cleaning

#split marka - model

cars = pd.DataFrame(df["Model"].str.split(' ',1).tolist(),
           columns = ["Marka","Model"])
df.drop(columns=["Model"],inplace = True)
df = pd.concat([df,cars], axis = 1)

#Lokalizacja
lok = pd.DataFrame(df["Lokalizacja"].str.split('(',1).tolist(),
           columns = ["Miasto","Wojewodztwo"])

lok["Wojewodztwo"] = lok["Wojewodztwo"].str.replace(')','')
df.drop(columns=["Lokalizacja"], inplace = True)

df = pd.concat([df,lok], axis = 1)


# wstawianie spacji do miasto kilkuwyrazowych
miasto = [re.sub(r"(\w)([A-Z])", r"\1 \2", lok["Miasto"][i]) for i in range(len(lok["Miasto"]))]
miasto = pd.DataFrame(miasto,columns=["Miasto"])
df.drop(columns=["Miasto"], inplace = True)
df = pd.concat([df,miasto], axis = 1)

#Negocjacja
nego = df["Negocjacja"]
df.drop(columns=["Negocjacja"], inplace = True)
nego = nego.str.get_dummies(" , ")
df = pd.concat([df,nego], axis=1)

#zamiana wszystkich cen netto na brutto
for i in df["Netto"]:
	if df["Netto"][i] == 1:
		df["Cena"][i] = df["Cena"][i]*1.23

#dropowanie kolumn Brutto netto oraz faktury vat
df.drop(columns=["Brutto","Netto","Faktura VAT"], inplace = True)


#wstepny export wyczyszczonego zbioru
df.to_csv("otomoto_clean.csv",sep = ',',
	    index = False, header = True)


