from ServerDownloader.DownSrv import ServerDownloader

if __name__ == "__main__":
    inst = ServerDownloader()
    links = inst.listStableLink()
    for i in links:
        print(i)