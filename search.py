from utils import getUrlList, getServer, getData, printData, getMovieInfo, saveFinalData, printFinalData, argParser

def search():
    alllinks = getUrlList()
    moviedata = []
    finallink = getServer(alllinks)
    print(f"\nsearching on server: {finallink}")
    print("\nby default prints 4 results per search. to override,\nend your input with '--(num results, 1-30)\n")
    
    while True:
        userInput = input("search for a movie (or type 'exit' if finished): ")
        info = argParser(userInput)
        movie = info[0]
        numsearchresults = info[1]
        
        if movie=='exit':
            break

        print("\n")
        movielink = finallink + f"/search/{movie}/1/99/0"
        print(f"searching on: {movielink}")

        data = getData(numsearchresults, movielink)
        if data == None:
            print("no results")
            continue
        else: printData(data)

        indexes = getMovieInfo(data)
        if indexes=="n":
            pass
        else:
            for index in indexes:
                index = int(index)-1
                moviedata.append([movie, data[index][1], data[index][3]])
                print(f"added {index+1} to list")

    #print(moviedata)

    saveorno = input("save results? (y/n) ")
    if saveorno=="y":
        saveFinalData(moviedata, f"{input("save file title?")}.txt")
        print("responses saved to results.txt")
    else:
        printFinalData(moviedata)
        print("\n")

    return moviedata
