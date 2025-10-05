# 🚀 Інструкція по встановленню та запуску

## 📋 Зміст

1. [Встановлення MongoDB](#mongodb)
2. [Встановлення Redis](#redis)
3. [Встановлення Cassandra](#cassandra)
4. [Встановлення PostgreSQL](#postgresql)
5. [Встановлення Node.js залежностей](#nodejs)
6. [Запуск прикладів](#запуск)

---

## 🍃 MongoDB

### **Ubuntu/Debian:**

```bash
# Імпорт публічного ключа
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

# Додавання репозиторію
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
   sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Встановлення
sudo apt-get update
sudo apt-get install -y mongodb-org

# Запуск сервісу
sudo systemctl start mongod
sudo systemctl enable mongod

# Перевірка статусу
sudo systemctl status mongod

# Підключення через CLI
mongosh
```

### **macOS (Homebrew):**

```bash
# Встановлення
brew tap mongodb/brew
brew install mongodb-community@7.0

# Запуск
brew services start mongodb-community@7.0

# Перевірка
mongosh
```

### **Windows:**

1. Завантажити MSI інсталятор з https://www.mongodb.com/try/download/community
2. Запустити інсталятор
3. Вибрати "Complete" installation
4. Встановити як Windows Service
5. Опціонально встановити MongoDB Compass

**Запуск:**
```powershell
# MongoDB запускається автоматично як сервіс
# Для підключення:
mongosh
```

### **Docker (всі ОС):**

```bash
# Запуск MongoDB в Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -v mongodb_data:/data/db \
  mongo:7.0

# Підключення
docker exec -it mongodb mongosh -u admin -p password
```

---

## 🔴 Redis

### **Ubuntu/Debian:**

```bash
# Встановлення
sudo apt-get update
sudo apt-get install redis-server

# Налаштування (опціонально)
sudo nano /etc/redis/redis.conf

# Запуск
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Перевірка
redis-cli ping
# Відповідь: PONG
```

### **macOS (Homebrew):**

```bash
# Встановлення
brew install redis

# Запуск
brew services start redis

# Перевірка
redis-cli ping
```

### **Windows:**

```bash
# Використовуйте WSL2 або Docker

# WSL2:
wsl --install
# Потім встановіть Redis в WSL як на Ubuntu

# Docker:
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:latest
```

### **Docker:**

```bash
# Запуск Redis
docker run -d \
  --name redis \
  -p 6379:6379 \
  -v redis_data:/data \
  redis:latest redis-server --appendonly yes

# Підключення
docker exec -it redis redis-cli
```

---

## 🗄️ Cassandra

### **Ubuntu/Debian:**

```bash
# Встановлення Java
sudo apt-get update
sudo apt-get install -y openjdk-11-jdk

# Додавання репозиторію Cassandra
echo "deb https://debian.cassandra.apache.org 41x main" | \
  sudo tee /etc/apt/sources.list.d/cassandra.list

curl https://downloads.apache.org/cassandra/KEYS | sudo apt-key add -

# Встановлення
sudo apt-get update
sudo apt-get install cassandra

# Запуск
sudo systemctl start cassandra
sudo systemctl enable cassandra

# Перевірка
nodetool status

# Підключення через cqlsh
cqlsh
```

### **macOS (Homebrew):**

```bash
# Встановлення Java
brew install openjdk@11

# Встановлення Cassandra
brew install cassandra

# Запуск
brew services start cassandra

# Підключення
cqlsh
```

### **Docker (рекомендовано):**

```bash
# Запуск Cassandra
docker run -d \
  --name cassandra \
  -p 9042:9042 \
  -v cassandra_data:/var/lib/cassandra \
  cassandra:latest

# Очікування старту (1-2 хвилини)
docker logs -f cassandra

# Підключення
docker exec -it cassandra cqlsh
```

---

## 🐘 PostgreSQL

### **Ubuntu/Debian:**

```bash
# Встановлення
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Запуск
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Створення користувача та бази
sudo -u postgres psql
```

```sql
CREATE USER admin WITH PASSWORD 'password';
CREATE DATABASE online_shop OWNER admin;
GRANT ALL PRIVILEGES ON DATABASE online_shop TO admin;
\q
```

### **macOS (Homebrew):**

```bash
# Встановлення
brew install postgresql@15

# Запуск
brew services start postgresql@15

# Створення бази
createdb online_shop
```

### **Docker:**

```bash
# Запуск PostgreSQL
docker run -d \
  --name postgres \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=online_shop \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15

# Підключення
docker exec -it postgres psql -U postgres -d online_shop
```

---

## 📦 Node.js та залежності

### **Встановлення Node.js:**

```bash
# Ubuntu/Debian (через NodeSource)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS (Homebrew)
brew install node@20

# Windows
# Завантажити інсталятор з https://nodejs.org/

# Перевірка
node --version
npm --version
```

### **Створення проекту:**

```bash
# Створення директорії проекту
mkdir nosql-practice
cd nosql-practice

# Ініціалізація npm
npm init -y

# Встановлення залежностей
npm install mongodb redis cassandra-driver pg nodemailer

# Встановлення dev залежностей
npm install --save-dev nodemon
```

### **package.json:**

```json
{
  "name": "nosql-practice",
  "version": "1.0.0",
  "description": "NoSQL databases practice",
  "main": "index.js",
  "scripts": {
    "mongodb": "node mongodb-shop.js",
    "postgresql": "node postgresql-shop.js",
    "redis": "node redis-sessions.js",
    "cassandra": "node cassandra-logs.js",
    "backup-mongo": "bash backup-mongodb.sh",
    "backup-redis": "bash backup-redis.sh"
  },
  "dependencies": {
    "mongodb": "^6.3.0",
    "redis": "^4.6.0",
    "cassandra-driver": "^4.7.2",
    "pg": "^8.11.3",
    "nodemailer": "^6.9.7"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}
```

---

## ▶️ Запуск прикладів

### **1. MongoDB - Онлайн магазин:**

```bash
# Переконайтесь що MongoDB запущено
mongosh --eval "db.serverStatus()"

# Створіть файл mongodb-shop.js з кодом з артефакту
# Запуск:
node mongodb-shop.js

# Або через npm:
npm run mongodb
```

**Очікуваний результат:**
```
✓ Підключено до MongoDB
=== 1. СТВОРЕННЯ КОЛЕКЦІЙ ===
=== 2. CRUD ОПЕРАЦІЇ ===
--- CREATE: Додавання продуктів ---
Додано 5 продуктів
...
✓ Всі операції MongoDB виконано успішно!
```

---

### **2. PostgreSQL - Порівняння з SQL:**

```bash
# Переконайтесь що PostgreSQL запущено
psql -U postgres -c "SELECT version();"

# Створіть базу даних (якщо не створена)
createdb online_shop

# Запуск:
node postgresql-shop.js

# Або:
npm run postgresql
```

---

### **3. Redis - Управління сесіями:**

```bash
# Перевірка Redis
redis-cli ping

# Запуск:
node redis-sessions.js

# Або:
npm run redis
```

**Очікуваний результат:**
```
✓ Підключено до Redis
=== ДЕМОНСТРАЦІЯ РОБОТИ З REDIS ===
--- 1. CREATE: Створення сесій ---
✓ Створено сесію для користувача user123
...
✓ Демонстрація Redis завершена!
```

---

### **4. Cassandra - Логи подій:**

```bash
# Перевірка Cassandra (може зайняти 1-2 хвилини після старту)
nodetool status

# Або для Docker:
docker exec cassandra nodetool status

# Запуск:
node cassandra-logs.js

# Або:
npm run cassandra
```

**Примітка:** Cassandra потребує часу для старту. Якщо отримуєте помилку підключення, зачекайте 1-2 хвилини.

---

### **5. Резервне копіювання:**

#### **MongoDB Backup:**

```bash
# Створіть скрипт backup-mongodb.sh
chmod +x backup-mongodb.sh

# Ручний запуск:
./backup-mongodb.sh

# Або через npm:
npm run backup-mongo

# Налаштування cron (автоматичний backup):
crontab -e
# Додати: 0 2 * * * /path/to/backup-mongodb.sh
```

#### **Redis Backup:**

```bash
# Створіть скрипт backup-redis.sh
chmod +x backup-redis.sh

# Запуск:
./backup-redis.sh

# Або:
npm run backup-redis
```

---

## 🛠️ Troubleshooting (Вирішення проблем)

### **MongoDB не запускається:**

```bash
# Перевірка логів
sudo tail -f /var/log/mongodb/mongod.log

# Перевірка порту
sudo netstat -tlnp | grep 27017

# Перевірка прав доступу
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown mongodb:mongodb /tmp/mongodb-27017.sock

# Перезапуск
sudo systemctl restart mongod
```

### **Redis connection refused:**

```bash
# Перевірка статусу
sudo systemctl status redis-server

# Перевірка конфігурації
sudo nano /etc/redis/redis.conf
# Знайти: bind 127.0.0.1 ::1
# Перевірити: protected-mode yes

# Перезапуск
sudo systemctl restart redis-server

# Тест підключення
redis-cli ping
```

### **Cassandra не стартує:**

```bash
# Збільшення heap memory (якщо мало RAM)
sudo nano /etc/cassandra/jvm.options
# Змінити:
# -Xms512M
# -Xmx512M

# Перевірка логів
sudo tail -f /var/log/cassandra/system.log

# Очистка даних (УВАГА: видалить всі дані)
sudo rm -rf /var/lib/cassandra/data/*
sudo systemctl restart cassandra
```

### **PostgreSQL помилки підключення:**

```bash
# Перевірка статусу
sudo systemctl status postgresql

# Налаштування аутентифікації
sudo nano /etc/postgresql/15/main/pg_hba.conf
# Додати:
# local   all   all   trust
# host    all   all   127.0.0.1/32   md5

# Перезапуск
sudo systemctl restart postgresql

# Створення користувача
sudo -u postgres createuser -s $USER
```

### **Node.js помилки:**

```bash
# Помилка "Cannot find module"
npm install

# Помилка версії Node.js
node --version  # Має бути >= 16.x

# Оновлення npm
npm install -g npm@latest

# Очистка кешу
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## 🐳 Docker Compose (Все в одному)

Для зручності можна запустити всі бази даних через Docker Compose:

### **docker-compose.yml:**

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb_data:/data/db
    networks:
      - nosql_network

  redis:
    image: redis:latest
    container_name: redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - nosql_network

  cassandra:
    image: cassandra:latest
    container_name: cassandra
    ports:
      - "9042:9042"
    environment:
      CASSANDRA_CLUSTER_NAME: TestCluster
      CASSANDRA_DC: dc1
      CASSANDRA_RACK: rack1
    volumes:
      - cassandra_data:/var/lib/cassandra
    networks:
      - nosql_network
    healthcheck:
      test: ["CMD-SHELL", "cqlsh -e 'describe cluster'"]
      interval: 30s
      timeout: 10s
      retries: 5

  postgres:
    image: postgres:15
    container_name: postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
      POSTGRES_DB: online_shop
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - nosql_network

  # Опціонально: GUI інструменти
  mongo-express:
    image: mongo-express
    container_name: mongo-express
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: password
      ME_CONFIG_MONGODB_URL: mongodb://admin:password@mongodb:27017/
    depends_on:
      - mongodb
    networks:
      - nosql_network

  redis-commander:
    image: rediscommander/redis-commander
    container_name: redis-commander
    ports:
      - "8082:8081"
    environment:
      REDIS_HOSTS: local:redis:6379
    depends_on:
      - redis
    networks:
      - nosql_network

  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin
    ports:
      - "8083:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: password
    depends_on:
      - postgres
    networks:
      - nosql_network

volumes:
  mongodb_data:
  redis_data:
  cassandra_data:
  postgres_data:

networks:
  nosql_network:
    driver: bridge
```

### **Запуск через Docker Compose:**

```bash
# Запуск всіх сервісів
docker-compose up -d

# Перевірка статусу
docker-compose ps

# Перегляд логів
docker-compose logs -f

# Зупинка
docker-compose down

# Зупинка з видаленням даних
docker-compose down -v
```

### **Доступ до GUI інструментів:**

- **Mongo Express**: http://localhost:8081
- **Redis Commander**: http://localhost:8082
- **pgAdmin**: http://localhost:8083

---

## 📚 Корисні команди

### **MongoDB:**

```bash
# Підключення
mongosh

# Показати бази даних
show dbs

# Використати базу
use online_shop

# Показати колекції
show collections

# Знайти документи
db.products.find().pretty()

# Підрахунок
db.orders.countDocuments()

# Видалити базу
db.dropDatabase()
```

### **Redis:**

```bash
# Підключення
redis-cli

# Інформація
INFO

# Список ключів
KEYS *

# Отримати значення
GET key

# Видалити ключ
DEL key

# Очистити всю базу
FLUSHALL

# Вийти
EXIT
```

### **Cassandra:**

```bash
# Підключення
cqlsh

# Показати keyspaces
DESCRIBE KEYSPACES;

# Використати keyspace
USE event_logs;

# Показати таблиці
DESCRIBE TABLES;

# Структура таблиці
DESCRIBE TABLE events;

# Вибірка даних
SELECT * FROM events LIMIT 10;

# Вийти
EXIT
```

### **PostgreSQL:**

```bash
# Підключення
psql -U admin -d online_shop

# Список баз даних
\l

# Підключення до бази
\c online_shop

# Список таблиць
\dt

# Структура таблиці
\d products

# Вибірка даних
SELECT * FROM products;

# Вийти
\q
```

---

## 📊 Моніторинг

### **Швидка перевірка всіх сервісів:**

```bash
#!/bin/bash
# check-services.sh

echo "=== Перевірка сервісів ==="

# MongoDB
echo -n "MongoDB: "
mongosh --quiet --eval "db.serverStatus().ok" 2>/dev/null && echo "✓ OK" || echo "✗ FAILED"

# Redis
echo -n "Redis: "
redis-cli ping 2>/dev/null | grep -q PONG && echo "✓ OK" || echo "✗ FAILED"

# Cassandra
echo -n "Cassandra: "
nodetool status 2>/dev/null | grep -q UN && echo "✓ OK" || echo "✗ FAILED"

# PostgreSQL
echo -n "PostgreSQL: "
pg_isready -q && echo "✓ OK" || echo "✗ FAILED"
```

```bash
chmod +x check-services.sh
./check-services.sh
```

---

## 🎓 Навчальні матеріали

### **Офіційна документація:**

- **MongoDB**: https://docs.mongodb.com/
- **Redis**: https://redis.io/documentation
- **Cassandra**: https://cassandra.apache.org/doc/
- **PostgreSQL**: https://www.postgresql.org/docs/

### **Онлайн курси:**

- MongoDB University (безкоштовно): https://university.mongodb.com/
- Redis University (безкоштовно): https://university.redis.com/
- DataStax Academy для Cassandra: https://www.datastax.com/dev

### **Інтерактивні туторіали:**

- MongoDB Atlas (безкоштовний tier): https://www.mongodb.com/cloud/atlas
- Redis Labs (безкоштовний tier): https://redis.com/try-free/
- Try PostgreSQL: https://www.postgresql.org/download/

---

## ✅ Чек-лист перед запуском

- [ ] Node.js встановлено (версія >= 16.x)
- [ ] MongoDB запущено і доступне на порту 27017
- [ ] Redis запущено і доступне на порту 6379
- [ ] Cassandra запущено і доступне на порту 9042 (опціонально)
- [ ] PostgreSQL запущено і доступне на порту 5432
- [ ] npm залежності встановлені (`npm install`)
- [ ] Всі скрипти мають права на виконання (`chmod +x`)
- [ ] Директорії для backup створені
- [ ] Перевірено підключення до всіх БД

---

## 🆘 Підтримка

Якщо виникли проблеми:

1. **Перевірте логи** відповідного сервісу
2. **Google/Stack Overflow** - більшість проблем вже вирішені
3. **Офіційна документація** - найкращий ресурс
4. **GitHub Issues** проектів баз даних

---

## 📝 Примітки

- Всі паролі в прикладах (`password`, `admin`) **НЕ** використовуйте в production!
- Для production налаштуйте proper authentication, SSL/TLS, firewall rules
- Регулярно робіть backup та тестуйте відновлення
- Моніторьте продуктивність та масштабуйте за потреби

**Успішної роботи з NoSQL базами даних! 🚀**