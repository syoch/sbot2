from .header import sort as header_sort
from .py_import import sort as py_import_sort

table = {
    "header": ["cpp", header_sort],
    "include": ["cpp", header_sort],
    "import": ["py", py_import_sort],
    "module": ["py", py_import_sort],
}
