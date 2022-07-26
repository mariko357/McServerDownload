import ServerDownloader.dsrv as dsrv

if __name__ == "__main__":
    inst = dsrv.init("cache/")
    j = 0
    for i in dsrv.snapshotVersion:
        print(dsrv.getDownloadLinkByVersion(i))
        j += 1

