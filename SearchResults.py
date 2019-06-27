from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

file = open("search-results-consumer-credit.txt","w")

source = requests.get('https://register.fca.org.uk/shpo_searchresultspage?search=consumer+credit&TOKEN=3wq1nht7eg7tr').text

soup = BeautifulSoup(source, 'html.parser')

results = soup.select(".ResultName a[href]")

for i in results: 
    href = i.get('href')
    companyName = i.text

    if href.startswith("http://fca"):
        print(href)
        print(companyName)
        
        file.write(href + '\n')

file.close() 
