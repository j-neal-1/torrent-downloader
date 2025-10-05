from bs4 import BeautifulSoup
import requests 

#MAIN.PY

def getUrlList() -> list:         #good. returns list of active thepiratebay mirrors
    linklist = []
    url = "https://piratebayproxy.info/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for tr in soup.find_all("tr"):
        for a in tr.find_all("a", href=True):
            linklist.append(a["href"])
    return linklist


def getServer(linklist: list) -> str:         #good. gets user input for what thepiratebay mirror (url) to use moving forward
    while True:
        try:
            linkindex = int(input(f"which server? (1 min, {len(linklist)} max) "))
            if linkindex>len(linklist) or linkindex<1:
                print("invalid")
            else:
                return linklist[linkindex] 
        except ValueError:
            print("must be a number")
    

def argParser(userInput): #returns list of [link, num of results to display]
    if "--" not in userInput:
        return [userInput.strip(), 4]
    try:
        num = int((userInput.split("--"))[1])
        if num > 30 or num < 1:
            print("invalid number, range 1-30")
            num = 4
        link = userInput[:userInput.find("--")]
        return [link.strip(), num]
    except:
        print("invalid argument, printing 4 results")
        return [userInput.strip(), 4]


def getData(numresults: int, movielink: str) -> list[list]:               #TODO: optimize, test to make sure nothing is broken, use enumerate() wherever possible
    data = []
    i = 0
    response = requests.get(movielink)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table#searchResult tr")
    
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

            sizepiece = pieces[4]
            size = sizepiece.text
            size = size.strip()

            seederspiece = pieces[5]
            seeders = seederspiece.text
            seeders = seeders.strip()
            
            data.append([title, size, seeders, magnetlink])

            if len(data) == numresults:             #stop once enough links have been collected
                return data

    if 0 < len(data) < numresults:
        print(f"\nonly {len(data)} links found!")
        return data
    

def printData(data: list[list]) -> None:                #good. prints search results
    if data == None:
        return
    for index, list in enumerate(data, start=1):
        print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{index}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"title: {list[0]}")
        print(f"size: {list[1]}")
        print(f"seeders: {list[2]}")
        print(f"link: {list[3]}")


def getMovieInfo(data: list[list]) -> int | str:             #good. gets user input for which movie(s) to select
    while True:
        try:
            indexes = input("which to download? ('n' to skip) ")
            if indexes == "n":
                return "n"
            
            invalid = False
            indexes = indexes.split(" ")
            for value in indexes:
                value = int(value)
                if value>len(data) or value<1:
                    print("invalid argument(s)")
                    invalid = True       
            if not invalid:
                return indexes
        except ValueError:
            print("must be a number")
            pass


def saveFinalData(moviedata: list[list], savelocation: str) -> None:         #good
    with open(savelocation, "a") as file:
            for index, movie in enumerate(moviedata, start=1):
                file.write(f"{index}: {movie[0]}, {movie[1]}, {movie[2]}\n")
            for movie in moviedata:
                file.write(f"{movie[2]}\n")
            file.close()


def printFinalData(moviedata: list[list]) -> None:                     #good
        for index, movie in enumerate(moviedata, start=1):
            print(f"{index}: {movie[0]}, {movie[1]}, {movie[2]}")
        for movie in moviedata:
            print(movie[2])


#FILEMANAGER.PY

def getSaveLocation():
    baseLocation = "/home/james/Downloads/"
    while True:
        location = input("where to save? (movies, other)")
        if location == "sus":
            return f"{baseLocation}.sus/"
        if location == "movies":
            return f"{baseLocation}movies/"
        if location == "other":
            return baseLocation