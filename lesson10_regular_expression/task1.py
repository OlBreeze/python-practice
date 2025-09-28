import re
from collections import Counter
from typing import Dict
import string  # в нём есть готовый список знаков пунктуации

s = ("President Donald Trump has signed an executive order, approving a proposal "
     "that would allow TikTok to continue operating in the US under American ownership.  "
     "But details of the deal have not been confirmed by China, or the app's Chinese owner ByteDance.  "
     "The BBC's Suranjana Tewari explains everything we know so far about how the deal might work.")

def word_count_with_index1(text: str) -> Dict[int, int]:
   # 0
    raw_words = text.lower().split()
    words0 = [w.strip(string.punctuation) for w in raw_words if w.strip(string.punctuation)]
    counts = Counter(words0)
    print(counts)

    words = re.findall(r"\w+", text.lower())


    # 1 считаем количество каждого слова
    counts = Counter(words)

    print(counts)
    ee = {i: counts[word] for i, word in enumerate(words)}
    print(ee)
    # 2 считаем количество каждого слова
    counts2 = {word: words.count(word) for word in set(words)}

    # строим словарь: индекс -> количество повторов
    result = {i: counts2[word] for i, word in enumerate(words)}
    return result




print(word_count_with_index1(s))
