from ServerDownloader.DownSrv import ServerDownloader
import time

if __name__ == "__main__":
    inst = ServerDownloader("cache/")
    j = 0
    for i in inst.stableVersion:
        inst.downloadServer(i)
        print(i)
        j += 1
