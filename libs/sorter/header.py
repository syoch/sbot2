def grep_header_name(src):
    if "<" in src:
        first = src.find("<")
        end = src.find(">", first)
    if "\"" in src:
        first = src.find("\"")
        end = src.find("\"", first+1)
    return src[first:end + 1]


def sort(src):
    lines = [
        grep_header_name(line)
        for line in src.split("\n")
        if line.startswith("#include")
    ]

    return "\n".join([
        *sorted([
            "#include " + line for line in lines if line.startswith("<")
        ]),
        "",
        *sorted([
            "#include " + line for line in lines if line.startswith("\"")
        ]),
    ])
