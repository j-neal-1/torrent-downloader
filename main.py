from search import search
from qbitt import download
from filemanager import moveFiles

if __name__ == "__main__":
    moviedata = search()

    if moviedata:
        filesInfo = download(moviedata)
        moveFiles(filesInfo)
    else:
        print("goodbye!")
