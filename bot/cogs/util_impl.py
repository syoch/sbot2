from libs.eval import safeeval


def eval(expr: str):
    try:
        (ret, stdout) = safeeval._eval(expr)
    except Exception as ex:
        import traceback
        return [
            "Exception has occured!",
            "```",
            ''.join(
                traceback.TracebackException.from_exception(ex).format()),
            "```"
        ]

    # Create Content
    code = expr.replace("```", "'''")

    ret_len = len(ret)
    if ret_len >= 1500:
        ret = f"long object({ret_len})"
    ret = ret.replace("```", "'''")

    stdout_len = len(stdout)
    if stdout_len >= 1500:
        stdout = f"long object({stdout_len})"
    stdout = stdout.replace("```", "'''")

    lines = []
    lines.extend([
        "sources",
        "```py",
        code,
        "```",
        ""
    ])
    if ret:
        lines.extend([
            "return value",
            "```",
            ret,
            "```"
        ])
    if stdout:
        lines.extend([
            "standard output",
            "```",
            stdout,
            "```"
        ])

    return lines
