from utils import getUrlList, getServer, howManyOptions, shortenlink, getData, printData, getMagnetLink, inputHandler


def main():
    alllinks = getUrlList()

    finallink = getServer(alllinks)

    print(finallink)

    linklist=[[]]
    justlinks=[]
    iteration = 0
    while True:
        todo = inputHandler() 
        if todo=="":
            pass
        if todo=="exit":
            break

        movie = input("search for a movie: ")

        movielink = finallink + f"/search/{movie}/1/99/0"

        print(f"searching on: {movielink}")

        numresults = 4           #howManyOptions()

        data = getData(numresults, movielink)

        printData()

        whichlink = getMagnetLink()
        if whichlink=="none":
            pass
        else:
            linklist.append([])
            linklist[iteration].append(movie)     #title, could use data[whichlink-1][0]
            linklist[iteration].append(data[whichlink-1][1])
            linklist[iteration].append(data[whichlink-1][3])
            justlinks.append(data[whichlink-1][3])

            iteration+=1
            print(f"added to list")

    i = 0
    for element in linklist:
        if not element:
            linklist.pop(i)
        i+=1
    print(linklist)


    with open("results.txt", "a") as file:
        i=1
        for movie in linklist:
            file.write(f"{i}: {movie[0]}, ")
            file.write(f"{movie[1]}, ")
            file.write(f"{movie[2]}\n")
            i+=1
        print(f"links:\n")
        for link in justlinks:
            file.write(f"{link}\n")
        file.close()
    
    print("responses saved to results.txt")


if __name__ == "__main__":
    main()
