#import os
#from time import sleep
from bs4 import BeautifulSoup
import requests 


def getUrlList() -> list:                           #good. returns list of active thepiratebay mirrors
    linklist = []
    url = "https://piratebayproxy.info/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for tr in soup.find_all("tr"):
        for a in tr.find_all("a", href=True):
            linklist.append(a["href"])
    return linklist

def getServer(linklist: list) -> str:                #good. gets user input for what thepiratebay mirror (url) to use moving forward
    while True:
        try:
            linkindex = int(input(f"which server? (1 min, {len(linklist)} max) "))
        except TypeError:
            print("must be a number")
        if linkindex>max or linkindex<1:
            print("invalid")
        else:
            return linklist[linkindex] 
    

def howManyOptionsToDisplay() -> int:                 #good. gets user input for how many search results to display
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


def getData(numresults: int, movielink: str) -> list[list]:               #TODO: ***OPTIMIZE***, test to make sure nothing broke
    data = [[]]
    response = requests.get(movielink)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table#searchResult tr")
    iteration = 0
    for row in rows:

        for a in row.find_all("a", href=True):

            if (a["href"]).startswith("magnet"):
                magnetlink = (a["href"])[:60]
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
            
            data.append([])                         #make sure theres room in the array to append to
            iteration += 1
            if iteration == numresults:             #stop once enough links have been collected
                data.pop(len(data)-1)               #removes empty list at end of data 
                return data
    


def printData(data: list[list]) -> None:                #good. prints search results
    iteration = 1
    for list in data:
        print(f"{iteration}: ")
        print(f"title: {list[0]}")
        print(f"size: {list[1]}")
        print(f"seeders: {list[2]}")
        print(f"link: {list[3]}")
        print("\n")
        iteration += 1

def getMovieInfo(data: list[list]) -> int | str:             #good. gets user input for which movie to select
    while True:
        try:
            selectedlinkindex = (input("which to download? ('none' to skip) "))
            if selectedlinkindex == "none":
                return "none"
            else:
                selectedlinkindex = int(selectedlinkindex)
        except ValueError:
            print("must be a number")
            continue
        if selectedlinkindex>len(data) or selectedlinkindex<1:
            print("invalid")
        else:
            return selectedlinkindex
        

def saveFinalData(moviedata: list[list], movielinks: list, savelocation: str) -> None:         #good
    with open(savelocation, "a") as file:
            iteration=1
            for movie in moviedata:
                file.write(f"{iteration}: {movie[0]}, {movie[1]}, {movie[2]}\n")
                iteration+=1
            for link in movielinks:
                file.write(f"{link}\n")
            file.close()

def printFinalData(moviedata: list[list], movielinks: list) -> None:                     #good
        iteration=1
        for movie in moviedata:
            print(f"{iteration}: {movie[0]}, {movie[1]}, {movie[2]}")
            iteration+=1
        for link in movielinks:
            print(link)
