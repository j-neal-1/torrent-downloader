import os
from utils import getSaveLocation


def moveFiles(filesInfo: list[list]):

    location = getSaveLocation()

    os.chdir("/home/james/.torrentworkspace")

    goodfiles = []
    for movie in filesInfo:
        for file in movie:
            if file.endswith(".mp4"):
                goodfiles.append([file, ".mp4"])
            if file.endswith(".mkv"):
                goodfiles.append([file, ".mkv"])

                
    print(goodfiles)

    for file in goodfiles:
        name = (input(f"what name for {file[0][:45]}...? ")).strip()
        os.rename(file[0], f"{location}{name}{file[1]}")
    