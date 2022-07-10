from ServerDownloader.DownSrv import ServerDownloader
import wget
if __name__ == "__main__":
    inst = ServerDownloader()
    inst.update()
    j = 0
    for i in inst.snapshotVersionLink:
        print(i, end=": ")
        print(inst.snapshotVersion[j])
        j += 1
    j = 0
    for i in inst.snapshotVersionLink:
        print(i)
        wget.download(inst.getDownloadHref(i), out=f"cache/{inst.snapshotVersion[j]}.jar")
        j += 1