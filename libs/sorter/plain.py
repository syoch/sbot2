def sort(src):
    return "\n".join(sorted([
        line
        for line in src.split("\n")
    ]))
