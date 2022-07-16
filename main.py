from ServerDownloader.DownSrv import ServerDownloader
import wget
import asyncio

if __name__ == "__main__":
    inst = ServerDownloader()
    inst.update()
    j = 0
    for i in inst.snapshotVersionDownloadLink:
        print(i, j)
        j += 1
    j = 0
    """for i in inst.snapshotVersionLink:
        print(i)
        wget.download(inst.getDownloadHref(i), out=f"cache/{inst.snapshotVersion[j]}.jar")
        j += 1"""