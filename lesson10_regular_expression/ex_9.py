import re

pattern1 = r'^L{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
print(re.search(pattern1, string='LDMV'))

pattern2 = r"""^  # start
    L{0,3}
    (CM|CD|D?C{0,3})
    (XC|XL|L?X{0,3})
    (IX|IV|V?I{0,3})
    $  # end
"""
print(pattern2)
print(re.search(pattern2, string='LDLV', flags=re.VERBOSE))

# Використання прапора компіляції
re.compile(pattern=r"""
    [\w\.\-]+    # Набір символів для імені користувача
    @            # Символ @
    [\w\.\-]+    # Набір символів для доменного імені
    ,
    """,
    flags=re.VERBOSE)