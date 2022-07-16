from ServerDownloader.DownSrv import ServerDownloader
import wget

if __name__ == "__main__":
    inst = ServerDownloader()
    inst.update()
    j = 0
    for i in inst.snapshotVersion:
        print(i, j)
        j += 1
    inst.downloadSnapshotServer(inst.stableVersion[5])
    j = 0
