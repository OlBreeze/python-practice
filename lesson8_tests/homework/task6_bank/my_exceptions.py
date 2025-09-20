class InsufficientFundsError(Exception):
    """Виняток для недостатньої кількості коштів на рахунку"""
    pass


class InvalidAmountError(Exception):
    """Виняток для некоректної суми транзакції"""
    pass
