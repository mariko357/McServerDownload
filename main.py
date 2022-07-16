from ServerDownloader.DownSrv import ServerDownloader
import wget
import time

if __name__ == "__main__":
    inst = ServerDownloader()
    j = 0
    for i in inst.snapshotVersion:
        print(i, j)
        j += 1
    print(inst.stableVersion[5])
    time.sleep(10)
    inst.downloadServer(inst.stableVersion[5])
    j = 0
