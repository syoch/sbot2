def sort(src):
    return "\n".join([
        line
        for line in src.split("\n")
        if line.startswith("import")
    ])
