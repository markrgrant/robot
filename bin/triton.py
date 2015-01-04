map = map

getattr = getattr

def getitem(obj, attr, index):
    return getattr(obj, attr)[index]
