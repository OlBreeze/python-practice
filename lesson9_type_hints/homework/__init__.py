# Импорты из локальных модулей (без /homework)
from .task1_simple_types import calculate_discount
from .task2_list_tuple import filter_adults  
from .task3_union_optional import parse_input
from .task4_generics import get_first
from .task5_callable import apply_operation, double, square

# Список экспортируемых функций
__all__ = [
    'calculate_discount',
    'filter_adults', 
    'parse_input',
    'get_first',
    'apply_operation',
    'double',
    'square'
]