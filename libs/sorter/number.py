def sort(src):
    lst = src.split("\n")
    lst = [x for x in lst if x != ""]
    lst.sort(key=lambda x: float(x))
    return "\n".join(lst)
