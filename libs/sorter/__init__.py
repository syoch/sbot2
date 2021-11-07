from .header import sort as header_sort
from .py_import import sort as py_import_sort
from .plain import sort as plain_sort
table = {
    "header": ["cpp", header_sort],
    "include": ["cpp", header_sort],
    "import": ["py", py_import_sort],
    "module": ["py", py_import_sort],
    "normal": ["plain", plain_sort],
}
