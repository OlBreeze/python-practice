Чтобы узнать, **какие зависимости установлены в Python**, 
есть несколько способов — в зависимости от того, 
используешь ты виртуальную среду, pip или poetry/pipenv.

# ✅ **1. Все установленные пакеты (pip)**

```bash
pip list
```

или:

```bash
pip freeze
```

**Разница:**

* `pip list` — показывает установленные пакеты в человекочитаемом виде.
* `pip freeze` — выводит точные версии в формате `package==version` (обычно для requirements.txt).

---

# ✅ **2. Посмотреть, где они установлены**

```bash
pip show <package_name>
```

Например:

```bash
pip show django
```

Покажет путь, версию, зависимости и т.д.

---

# ✅ **3. Если используешь virtualenv / venv**

Сначала активируй виртуальную среду:

```bash
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

А потом `pip list` покажет **только зависимости этой среды**.

---

# ✅ **4. Если проект использует requirements.txt**

Посмотреть зависимости:

```bash
cat requirements.txt
```

---

# ✅ **5. Если используешь Poetry**

```bash
poetry show
```

Для дерева зависимостей:

```bash
poetry show --tree
```

---

# ✅ **6. Если используешь Pipenv**

```bash
pipenv graph
```
