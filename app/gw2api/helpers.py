__author__ = 'Frenos'


def idList2String(idList):
    idsString = ",".join(str(x) for x in idList)
    return idsString


def idList2Chunks(idList):
    idChunkedLists = []
    for i in range(0, len(idList), 200):
        idChunkedLists.append(idList[i:i + 200])
    return idChunkedLists
