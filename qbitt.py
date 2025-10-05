import qbittorrentapi as qbitt
import getpass
from time import sleep
from os import system

def download(data) -> list[list]:
    system("qbittorrent-nox &> /dev/null &")
    print("qbittorrent started")
    links = []
    names = []
    for movie in data:
        links.append(movie[2])
        names.append(movie[0])
    
    info = dict(
        host="localhost",
        port=8080,
        username="admin"
    )

    while True:
        pw = getpass.getpass("enter password for qbittorrent: ")
        try:
            client = qbitt.Client(**info, password=pw)      
            client.auth_log_in()
            break
        except qbitt.LoginFailed:
            print("incorrect")
        except qbitt.APIConnectionError:
            print("client is not running, you fucking idiot")
    print("logged in")

    client.torrents_delete(torrent_hashes="all", delete_files=True)

    input("proceed?")

    for index, link in enumerate(links):
        status = client.torrents_add(urls=link)
        print(f"status for {names[index]}: {status}")
        if status != "Ok.":
            client.torrents_delete(torrent_hashs=torrent.hash, delete_files=False)
    print("\n")


    print("getting files...")
    filesInfo = []
    for index, torrent in enumerate(client.torrents_info()):
        filesInfo.append([])
        torrent.set_location(location="/home/james/.torrentworkspace/")

        while not filesInfo[index]:
            files = client.torrents_files(torrent_hash=torrent.hash)
            for file in files:
                filesInfo[index].append(file.name)

    numfiles = 0
    for movie in filesInfo:
        for file in movie:
            numfiles += 1

    print(f"{numfiles} file(s) found")

    finished = []
    while True:
        ongoing = []        
        for index, torrent in enumerate(client.torrents_info()):

            if torrent.state == "stalledUP" or torrent.state == "uploading":
                finished.append(f"{torrent.name[:40]}...: DONE")
                client.torrents_delete(torrent_hashes=torrent.hash, delete_files=False)
            else:
                ongoing.append(f"{torrent.name[:30]}...:): {torrent.state} {torrent.progress*100:.2f}%")
            
        for line in finished:
            print(f"{line}                              ")    
        for line in ongoing:
            print(f"{line}                          ")

        sleep(1)
        print(f"\x1B[{len(ongoing)+len(finished)}A\x1B[K", end="")
        
        if len(client.torrents_info()) == 0:
            break
        

    print("\n\nlogging out")
    client.auth_log_out()
    
    system("pkill qbittorrent-nox &> /dev/null &")
    print("shutdown qbittorrent")
    return filesInfo
