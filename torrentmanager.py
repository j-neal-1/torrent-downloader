from utils import getUrlList, getServer, howManyOptionsToDisplay, getData, printData, getMovieInfo, saveFinalData, printFinalData


def main():
    alllinks = getUrlList()
    finallink = getServer(alllinks)

    print(f"searching on server: {finallink}")

    moviedata = [[]]
    movielinks = []
    position = 0
    while True:
        movie = input("search for a movie (or type 'exit' if finished): ")
        
        if movie=='exit':
            break

        movielink = finallink + f"/search/{movie}/1/99/0"                       #print(f"searching on: {movielink}")
        numsearchresults = 4                                                    #howManyOptionsToDisplay()

        data = getData(numsearchresults, movielink)
        printData(data)

        selectedlinkindex = getMovieInfo(data)
        if selectedlinkindex=="none":
            pass
        else:
            moviedata.append([])
            moviedata[position].append(movie)                                   #title, could use data[selectedlinkindex-1][0] 
            moviedata[position].append(data[selectedlinkindex-1][1])            #for actual name, this uses user's search as name
            moviedata[position].append(data[selectedlinkindex-1][3])
            movielinks.append(data[selectedlinkindex-1][3])
            position+=1
            print(f"added to list")




    i = 0
    for element in moviedata:                                                   #cleanup moviedata
        if not element:
            moviedata.pop(i)
        i+=1

    #print(moviedata)
    #print(movielinks)
    

    saveorno = input("save results? (y/n) ")
    if saveorno=="y":
        saveFinalData(moviedata, movielinks, "results.txt")
        print("responses saved to results.txt")
    else:
        printFinalData(moviedata, movielinks)
        print("exiting")

    for link in movielinks:
        print(len(link))

if __name__ == "__main__":
    main()
