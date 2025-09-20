class StringProcessor:
    """
    Клас для обробки рядків. task 4 - doctest
    """

    def reverse_string(self, s: str) -> str:
        """
        Повертає перевернутий рядок.

        Args:
            s (str): Вхідний рядок для реверсування.

        Returns:
            str: Перевернутий рядок.

        Examples:
            >>> processor = StringProcessor()
            >>> processor.reverse_string("hello")
            'olleh'
            >>> processor.reverse_string("Python")
            'nohtyP'
        """
        return s[::-1]  # При s[::1] — идём слева направо (обычно).
        # При s[::-1] — идём справа налево, начиная с последнего символа

    def capitalize_string(self, s: str) -> str:
        """
        Робить першу літеру рядка великою, решту - малими.
        Args:
            s (str): Вхідний рядок для капіталізації.

        Returns:
            str: Рядок з великою першою літерою.

        Examples:
            >>> processor = StringProcessor()
            >>> processor.capitalize_string("hello world")
            'Hello world'
            >>> processor.capitalize_string("PYTHON")
            'Python'
        """
        if not s:
            return s
        # return s[0].upper() + s[1:].lower()
        return s.capitalize()

    def count_vowels(self, s: str) -> int:
        """
        Повертає кількість голосних літер у рядку.

        Args:
            s (str): Вхідний рядок для підрахунку голосних.

        Returns:
            int: Кількість голосних літер у рядку.

        Examples:
            >>> processor = StringProcessor()
            >>> processor.count_vowels("hello")
            2
            >>> processor.count_vowels("Programming")
            3
        """
        vowels = "aeiouаеіоуиюяєї"  # англійські і українські
        return sum(1 for char in s.lower() if char in vowels)


# ---- doctest
if __name__ == "__main__":
    import doctest

    doctest.testmod()
