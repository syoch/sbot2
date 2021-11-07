from .header import sort as header_sort
from .py_import import sort as py_import_sort
from .plain import sort as plain_sort
from .number import sort as number_sort

table = {
    "cpp": header_sort,
    "py": py_import_sort,
    "plain": plain_sort,
    "num": number_sort,
}
