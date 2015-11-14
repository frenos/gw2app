__author__ = 'Frenos'


def idList2String(idList):
    """
    Will convert a list of items into the format "itemA,itemB,..."
    :param idList: list to use as base
    :return: a String representing the list with commas
    """
    idsString = ",".join(str(x) for x in idList)
    return idsString


def idList2Chunks(idList, size=200):
    """
    Will convert a list given into a list of n list with size items each
    :param size: size of the resulting lists
    :param idList: list to split in multiple lists
    :return: a list of lists each with size elements
    """
    idChunkedLists = []
    for i in range(0, len(idList), size):
        idChunkedLists.append(idList[i:i + size])
    return idChunkedLists
