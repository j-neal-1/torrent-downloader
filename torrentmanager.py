import os
from time import sleep
from bs4 import BeautifulSoup
import requests 


def getUrlList():
    links = []
    url = "https://piratebayproxy.info/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for tr in soup.find_all("tr"):
        for a in tr.find_all("a", href=True):
            links.append(a["href"])
    return links


def howManyOptions():
    while True:
        try:
            numresults = int(input("how many results? (max 30) "))
        except ValueError:
            print("must be a number")
            continue
        if numresults>30 or numresults<1:
            print("invalid")
        else:
            return numresults


def shortenlink(link):
    linklist = []
    for char in link:
        if char == "&":
            finallink = "".join(linklist)
            return finallink
        linklist.append(char)


def getData(numresults):
    iteration = 0
    global data
    data = [[]]
    response = requests.get(movielink)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table#searchResult tr")

    for row in rows:

        for a in row.find_all("a", href=True):

            if (a["href"]).startswith("magnet"):
                ogmagnetlink = (a["href"])
                magnetlink = shortenlink(ogmagnetlink)
                linkfound = True
                break
            else:
                linkfound = False
                
        if linkfound:

            pieces = row.find_all("td")

            titlepiece = pieces[1]
            title = titlepiece.text
            title = title.strip()
            data[iteration].append(title)

            sizepiece = pieces[4]
            size = sizepiece.text
            size = size.strip()
            data[iteration].append(size)

            seederspiece = pieces[5]
            seeders = seederspiece.text
            seeders = seeders.strip()
            data[iteration].append(seeders)

            data[iteration].append(magnetlink)
            
            iteration += 1
            if iteration == numresults:             #stop once enough links have been collected
                return
            data.append([])                         #make sure theres room in the array to append to
    
    data.pop(len(data)-1)                           #removes empty list at end of data 
    return

def printData():
    iteration = 1
    for list in data:
        print(f"{iteration}: ")
        print(f"title: {list[0]}")
        print(f"size: {list[1]}")
        print(f"seeders: {list[2]}")
        print(f"link: {list[3]}")
        print("\n")
        iteration += 1

def getMagnetLink():
    while True:
        try:
            whichlink = int(input("which to download? "))
        except ValueError:
            print("must be a number")
            continue
        if whichlink>len(data) or whichlink<1:
            print("invalid")
        else:
            return whichlink



alllinks = getUrlList()

finallink=alllinks[0]

movie = input("search for a movie: ")

movielink = finallink + f"/search/{movie}/1/99/0"

print(f"searching on: {movielink}")

numresults = howManyOptions()

getData(numresults)

printData()

whichlink = getMagnetLink()

print(f"your link: {data[whichlink-1][3]}") 