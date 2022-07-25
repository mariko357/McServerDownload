from ServerDownloader.dsrv import ServerDownloader

if __name__ == "__main__":
    inst = ServerDownloader("cache/")
    j = 0
    for i in inst.stableVersion:
        print(inst.getDownloadLinkByVersion(i))
        j += 1

