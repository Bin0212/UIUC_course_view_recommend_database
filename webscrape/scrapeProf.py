#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 23:48:48 2019

@author: bin
"""

import requests
import csv
import re
import time
from bs4 import BeautifulSoup

def find(filename):
    mylist = []
    with open(filename, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if row[20] not in mylist: 
                mylist.append(row[20])
    csvFile.close()
    return mylist


def create_soup(url):
    # print(url)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    return soup


def find_prof(soup, prof: list) -> str:
    all_lines = soup.find_all("a", href=True)
    time.sleep(1)
    for line in all_lines:
        #time.sleep(3)
        if (line['href'].startswith('/ShowRatings.jsp?tid=')):
            possible_prof = set(line.find('span', {'class': 'main'}).text.strip().split(', '))
            if set(prof) <= possible_prof:
                return 'http://www.ratemyprofessors.com' + line['href']
            elif prof in possible_prof:
                return 'http://www.ratemyprofessors.com' + line['href']


def get_ratings(soup):
    result = dict()
    for x in ("quality", "difficulty", "takeAgain"):
        line = soup.find('div', {"class": x})
        temp = line.find(class_="grade")
        if temp is not None:
            result[x] = (temp.text.strip())
    return result


def run(prof: str):
    prof = prof.split()
    url = 'http://www.ratemyprofessors.com/search.jsp?query='
    url += 'UIUC+' + prof[-1]

    soup = create_soup(url)
    prof_page = find_prof(soup, prof)

    if(prof_page != None):
        prof_soup = create_soup(prof_page)
        return get_ratings(prof_soup)


if __name__ == '__main__':
    
    filename = 'uiuc-gpa-dataset.csv'
    mylist = find(filename)
    splitname = [re.split(' |, ', i) for i in mylist][5768:7001]
    #All = []
    for name in splitname:
        firstname = name[0]
        url = 'http://www.ratemyprofessors.com/search.jsp?query=UIUC+'
        url += firstname

        soup = create_soup(url)
        prof_page = find_prof(soup, {firstname})
        if prof_page != None:
            prof_soup = create_soup(prof_page)
            ratings = get_ratings(prof_soup)
            All .append(( ' '.join(name), ratings.get('quality'), ratings.get('difficulty'), ratings.get('takeAgain')))
        print(name)