from utils import *


def main():
    alllinks = getUrlList()

    finallink = getServer(alllinks)

    print(finallink)

    movie = input("search for a movie: ")

    movielink = finallink + f"/search/{movie}/1/99/0"

    print(f"searching on: {movielink}")

    numresults = howManyOptions()

    getData(numresults, movielink)

    printData()

    whichlink = getMagnetLink()


    print(f"your link: {data[whichlink-1][3]}") 

if __name__ == "__main__":
    main()
