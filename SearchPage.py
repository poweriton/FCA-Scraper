from flask import Flask, render_template
from bs4 import BeautifulSoup
from bs4 import Comment
import requests

# remove all attributes except some tags(only saving ['href','src'] attr)
def _remove_all_attrs_except_saving(soup):
    whitelist = ['a','img']
    for tag in soup.find_all(True):
        if tag.name not in whitelist:
            tag.attrs = {}
        else:
            attrs = dict(tag.attrs)
            for attr in attrs:
                if attr not in ['src','href']:
                    del tag.attrs[attr]

    for script in soup(["script"]): 
        script.extract()

    return soup

# open a list of url's to parse
file = open("search-results.txt","r")

# split to list
x = file.read().splitlines()
file.close()

# for each link in the list
file2 = open("export.csv","w")

for l in x:
    #get the first URL
    source = requests.get(l).text
    #create soup
    soup = BeautifulSoup(source) 

    # remove all unused tags from the html
    clean_soup = _remove_all_attrs_except_saving(soup)

    #select the second table in list
    resultsT = soup("table")[1]

    resultsTb = resultsT.tbody

    subtable = resultsTb.table

    subtable.decompose()

    trs = resultsTb("tr")

    for r in trs:
        th = r.find("th")
        td = r.find("td")

        try:
            if "Address" in th.text:
                continue
        except:
            continue
            
        lines = td.text.splitlines()
        print(lines)

        for l in lines:
            print(l)

            if len(l.strip()) > 5:
                # print(l.strip())
                file2.write(l.strip()+",")
            if len(l.strip()) == 0:
                file2.write(",")        
    file2.write("\n")
file2.close()
