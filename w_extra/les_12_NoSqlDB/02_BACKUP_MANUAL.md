# Частина 3: Резервне копіювання та моніторинг

## 📦 1. Резервне копіювання MongoDB

### **Метод 1: mongodump (Рекомендований)**

```bash
# Повний backup бази даних
mongodump --db=online_shop --out=/backup/mongodb/$(date +%Y%m%d)

# Backup конкретної колекції
mongodump --db=online_shop --collection=orders --out=/backup/orders/

# Backup з компресією
mongodump --db=online_shop --gzip --out=/backup/compressed/

# Backup з аутентифікацією
mongodump --uri="mongodb://username:password@localhost:27017/online_shop" \
  --out=/backup/

# Інкрементальний backup (тільки змінені дані)
mongodump --db=online_shop --query='{"updated_at": {$gte: ISODate("2025-10-01")}}'
```

**Переваги mongodump:**
- ✅ Зручний та простий у використанні
- ✅ Підтримує стиснення
- ✅ Працює з будь-якою версією MongoDB
- ✅ Можна робити вибірковий backup

**Недоліки:**
- ❌ Повільніше для великих баз (GB+)
- ❌ Блокує базу під час backup

---

### **Метод 2: Файловий snapshot**

```bash
# Зупинка запису (для консистентності)
mongo --eval "db.fsyncLock()"

# Копіювання даних
cp -r /var/lib/mongodb /backup/snapshot/$(date +%Y%m%d)

# Або використання LVM snapshot
lvcreate --size 10G --snapshot --name mongodb-snap /dev/vg0/mongodb

# Розблокування
mongo --eval "db.fsyncUnlock()"
```

**Переваги:**
- ✅ Дуже швидкий для великих баз
- ✅ Можна використовувати системні інструменти

**Недоліки:**
- ❌ Потребує зупинки запису
- ❌ Займає більше місця

---

### **Метод 3: MongoDB Atlas (Cloud)**

```javascript
// Автоматичні backup в MongoDB Atlas
// Конфігурація через веб-інтерфейс або API

const { MongoClient } = require('mongodb');

// Ручне створення snapshot через API
async function createCloudBackup() {
  const response = await fetch(
    'https://cloud.mongodb.com/api/atlas/v1.0/groups/{GROUP-ID}/clusters/{CLUSTER-NAME}/backup/snapshots',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Digest username:apiKey'
      },
      body: JSON.stringify({
        retentionInDays: 7
      })
    }
  );
  
  return response.json();
}
```

**Переваги Atlas:**
- ✅ Автоматичні backup кожні 6-24 години
- ✅ Point-in-time recovery
- ✅ Географічно розподілені backup
- ✅ Не потребує адміністрування

---

### **Відновлення з backup**

```bash
# Відновлення повної бази
mongorestore --db=online_shop /backup/mongodb/20251003/online_shop/

# Відновлення з архіву
mongorestore --gzip --archive=/backup/online_shop.gz

# Відновлення конкретної колекції
mongorestore --db=online_shop --collection=orders \
  /backup/orders.bson

# Відновлення на новий сервер
mongorestore --host=new-server.com --port=27017 \
  --username=admin --password=pass \
  /backup/mongodb/20251003/
```

---

### **Автоматизація backup (Bash скрипт)**

```bash
#!/bin/bash
# backup-mongodb.sh

# Конфігурація
DB_NAME="online_shop"
BACKUP_DIR="/backup/mongodb"
RETENTION_DAYS=7

# Створення директорії з датою
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/$DATE"

# Створення backup
echo "Початок backup: $(date)"
mongodump --db=$DB_NAME --gzip --out=$BACKUP_PATH

# Перевірка успішності
if [ $? -eq 0 ]; then
    echo "✓ Backup успішний: $BACKUP_PATH"
    
    # Видалення старих backup
    find $BACKUP_DIR -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;
    echo "✓ Старі backup видалено (старіші за $RETENTION_DAYS днів)"
else
    echo "✗ Помилка backup!"
    exit 1
fi

# Відправка на cloud storage (опціонально)
# aws s3 sync $BACKUP_PATH s3://my-backups/mongodb/$DATE/
# gsutil -m rsync -r $BACKUP_PATH gs://my-backups/mongodb/$DATE/

echo "Завершено: $(date)"
```

**Налаштування cron для автоматичних backup:**

```bash
# Додати в crontab (crontab -e)

# Щоденний backup о 2:00 ночі
0 2 * * * /scripts/backup-mongodb.sh >> /var/log/mongodb-backup.log 2>&1

# Щотижневий повний backup (неділя о 3:00)
0 3 * * 0 /scripts/backup-mongodb-full.sh >> /var/log/mongodb-backup.log 2>&1

# Щогодинний інкрементальний backup
0 * * * * /scripts/backup-mongodb-incremental.sh >> /var/log/mongodb-backup.log 2>&1
```

---

## 🔴 2. Резервне копіювання Redis

### **Метод 1: RDB (Redis Database Backup)**

```bash
# Ручне створення snapshot
redis-cli BGSAVE

# Перевірка статусу
redis-cli LASTSAVE

# Копіювання файлу dump.rdb
cp /var/lib/redis/dump.rdb /backup/redis/dump_$(date +%Y%m%d).rdb
```

**Конфігурація автоматичних RDB snapshot:**

```conf
# redis.conf

# Автоматичне збереження:
# save <секунди> <кількість змін>

save 900 1      # Зберегти якщо 1+ змін за 15 хвилин
save 300 10     # Зберегти якщо 10+ змін за 5 хвилин
save 60 10000   # Зберегти якщо 10000+ змін за 1 хвилину

# Шлях до файлу
dir /var/lib/redis
dbfilename dump.rdb

# Компресія
rdbcompression yes

# Перевірка цілісності
rdbchecksum yes
```

---

### **Метод 2: AOF (Append Only File)**

```conf
# redis.conf

# Увімкнути AOF
appendonly yes
appendfilename "appendonly.aof"

# Політика синхронізації:
# always - кожна команда (повільно, безпечно)
# everysec - кожну секунду (баланс)
# no - ОС вирішує (швидко, ризиковано)
appendfsync everysec

# Автоматичне переписування AOF
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

**Переваги AOF:**
- ✅ Більш надійний (менше втрат даних)
- ✅ Можна відновити точний стан
- ✅ Автоматичне переписування

**Недоліки:**
- ❌ Більший розмір файлів
- ❌ Повільніше відновлення

---

### **Скрипт backup Redis**

```bash
#!/bin/bash
# backup-redis.sh

BACKUP_DIR="/backup/redis"
DATE=$(date +%Y%m%d_%H%M%S)
REDIS_DIR="/var/lib/redis"

# Створення snapshot
redis-cli BGSAVE

# Очікування завершення
while [ $(redis-cli LASTSAVE) -eq $(redis-cli LASTSAVE) ]; do
    sleep 1
done

# Копіювання файлів
mkdir -p $BACKUP_DIR/$DATE
cp $REDIS_DIR/dump.rdb $BACKUP_DIR/$DATE/
cp $REDIS_DIR/appendonly.aof $BACKUP_DIR/$DATE/ 2>/dev/null

# Компресія
tar -czf $BACKUP_DIR/redis_backup_$DATE.tar.gz -C $BACKUP_DIR/$DATE .
rm -rf $BACKUP_DIR/$DATE

echo "✓ Redis backup: $BACKUP_DIR/redis_backup_$DATE.tar.gz"

# Видалення старих backup (старіші 7 днів)
find $BACKUP_DIR -name "redis_backup_*.tar.gz" -mtime +7 -delete
```

---

## 📊 3. Моніторинг MongoDB

### **MongoDB Compass (GUI інструмент)**

**Основні можливості:**
- 🔍 Візуалізація структури даних
- 📈 Аналіз продуктивності запитів
- 🎯 Explain plans для оптимізації
- 📊 Індексація та статистика

**Встановлення:**
```bash
# Ubuntu/Debian
wget https://downloads.mongodb.com/compass/mongodb-compass_latest_amd64.deb
sudo dpkg -i mongodb-compass_latest_amd64.deb

# Windows/Mac: завантажити з mongodb.com/try/download/compass
```

**Використання через код:**

```javascript
const { MongoClient } = require('mongodb');

async function monitorMongoDB() {
  const client = await MongoClient.connect('mongodb://localhost:27017');
  const db = client.db('online_shop');

  // 1. Перевірка статусу сервера
  const serverStatus = await db.admin().serverStatus();
  console.log('MongoDB Server Status:');
  console.log('- Version:', serverStatus.version);
  console.log('- Uptime:', serverStatus.uptimeMillis / 1000, 'seconds');
  console.log('- Connections:', serverStatus.connections);
  console.log('- Memory:', serverStatus.mem);

  // 2. Статистика бази даних
  const dbStats = await db.stats();
  console.log('\nDatabase Stats:');
  console.log('- Collections:', dbStats.collections);
  console.log('- Data Size:', dbStats.dataSize / 1024 / 1024, 'MB');
  console.log('- Index Size:', dbStats.indexSize / 1024 / 1024, 'MB');
  console.log('- Documents:', dbStats.objects);

  // 3. Аналіз повільних запитів
  const slowQueries = await db.admin().command({
    profile: -1
  });
  console.log('\nSlow Queries:', slowQueries);

  // 4. Статистика колекції
  const products = db.collection('products');
  const collStats = await products.stats();
  console.log('\nProducts Collection Stats:');
  console.log('- Documents:', collStats.count);
  console.log('- Avg Document Size:', collStats.avgObjSize, 'bytes');
  console.log('- Indexes:', collStats.nindexes);

  // 5. Explain план запиту
  const explainResult = await products.find({ category: 'Електроніка' })
    .explain('executionStats');
  
  console.log('\nQuery Execution Stats:');
  console.log('- Execution Time:', explainResult.executionStats.executionTimeMillis, 'ms');
  console.log('- Documents Examined:', explainResult.executionStats.totalDocsExamined);
  console.log('- Documents Returned:', explainResult.executionStats.nReturned);
  console.log('- Index Used:', explainResult.executionStats.executionStages.indexName);

  await client.close();
}
```

---

### **MongoDB Atlas Monitoring (Cloud)**

```javascript
// Отримання метрик через Atlas API
async function getAtlasMetrics() {
  const response = await fetch(
    'https://cloud.mongodb.com/api/atlas/v1.0/groups/{GROUP-ID}/processes/{HOST}:{PORT}/measurements',
    {
      headers: {
        'Authorization': 'Digest username:apiKey'
      },
      params: {
        granularity: 'PT1M',  // 1 хвилина
        period: 'PT1H',       // остання година
        m: [
          'CONNECTIONS',
          'OPCOUNTER_QUERY',
          'OPCOUNTER_INSERT',
          'OPCOUNTER_UPDATE',
          'OPCOUNTER_DELETE',
          'QUERY_EXECUTOR_SCANNED',
          'TICKETS_AVAILABLE_READS',
          'TICKETS_AVAILABLE_WRITES'
        ]
      }
    }
  );
  
  return response.json();
}
```

**Основні метрики для моніторингу:**
- 📈 **Connections**: Кількість активних з'єднань
- ⚡ **Operations/sec**: Операції в секунду
- 💾 **Memory Usage**: Використання пам'яті
- 🔄 **Replication Lag**: Затримка реплікації
- 📊 **Query Performance**: Час виконання запитів
- 💿 **Disk Usage**: Використання диску

---

### **Профілювання MongoDB**

```javascript
// Увімкнення профілювання
await db.setProfilingLevel(2);  // 0=off, 1=slow, 2=all

// Налаштування порогу повільних запитів
await db.setProfilingLevel(1, { slowms: 100 });

// Аналіз повільних запитів
const slowQueries = await db.collection('system.profile')
  .find({ millis: { $gt: 100 } })
  .sort({ ts: -1 })
  .limit(10)
  .toArray();

console.log('Топ-10 повільних запитів:');
slowQueries.forEach(query => {
  console.log(`- ${query.ns}: ${query.millis}ms`);
  console.log(`  Command:`, query.command);
});
```

---

### **Prometheus + Grafana для MongoDB**

**Встановлення MongoDB Exporter:**

```bash
# Завантаження exporter
wget https://github.com/percona/mongodb_exporter/releases/download/v0.40.0/mongodb_exporter-0.40.0.linux-amd64.tar.gz
tar -xvf mongodb_exporter-0.40.0.linux-amd64.tar.gz

# Запуск
./mongodb_exporter --mongodb.uri=mongodb://localhost:27017
```

**Конфігурація Prometheus:**

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'mongodb'
    static_configs:
      - targets: ['localhost:9216']
```

**Приклад Dashboard Grafana:**
- Connection Pool Usage
- Operations per Second
- Query Execution Time
- Index Efficiency
- Replication Lag
- Memory and CPU Usage

---

## 🔍 4. Моніторинг Redis

### **Redis CLI Commands**

```bash
# Загальна інформація
redis-cli INFO

# Статистика по секціях
redis-cli INFO server
redis-cli INFO clients
redis-cli INFO memory
redis-cli INFO persistence
redis-cli INFO stats
redis-cli INFO replication

# Моніторинг в реальному часі
redis-cli --stat

# Перегляд команд в реальному часі
redis-cli MONITOR

# Повільні команди
redis-cli SLOWLOG GET 10

# Використання пам'яті
redis-cli --bigkeys

# Перевірка латентності
redis-cli --latency
redis-cli --latency-history
```

---

### **Node.js моніторинг Redis**

```javascript
const redis = require('redis');

async function monitorRedis() {
  const client = redis.createClient();
  await client.connect();

  // 1. Загальна інформація
  const info = await client.info();
  console.log('Redis Server Info:');
  
  // Парсинг info
  const lines = info.split('\r\n');
  const stats = {};
  lines.forEach(line => {
    if (line.includes(':')) {
      const [key, value] = line.split(':');
      stats[key] = value;
    }
  });

  console.log('- Version:', stats.redis_version);
  console.log('- Uptime:', stats.uptime_in_seconds, 'seconds');
  console.log('- Connected Clients:', stats.connected_clients);
  console.log('- Used Memory:', stats.used_memory_human);
  console.log('- Total Commands:', stats.total_commands_processed);

  // 2. Memory Stats
  const memoryStats = await client.info('memory');
  console.log('\nMemory Stats:', memoryStats);

  // 3. Slow Log
  const slowLog = await client.sendCommand(['SLOWLOG', 'GET', '5']);
  console.log('\nSlow Commands:', slowLog);

  // 4. Keyspace Info
  const keyspaceInfo = await client.info('keyspace');
  console.log('\nKeyspace:', keyspaceInfo);

  // 5. Persistence Info
  const persistenceInfo = await client.info('persistence');
  console.log('\nPersistence:', persistenceInfo);

  await client.quit();
}
```

---

### **Redis Monitoring Tools**

**1. RedisInsight (офіційний GUI)**
```bash
# Завантажити з https://redis.com/redis-enterprise/redis-insight/
# Можливості:
# - Візуалізація даних
# - Profiling команд
# - Memory аналіз
# - Slow log viewer
```

**2. Redis Exporter для Prometheus**
```bash
# Встановлення
docker run -d --name redis_exporter \
  -p 9121:9121 \
  oliver006/redis_exporter \
  --redis.addr=redis://localhost:6379
```

**Конфігурація Prometheus:**
```yaml
scrape_configs:
  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']
```

---

## 📱 5. Alerting та Notifications

### **Приклад скрипту моніторингу з alerting**

```javascript
const nodemailer = require('nodemailer');

// Email transporter
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'alerts@example.com',
    pass: 'password'
  }
});

async function checkDatabaseHealth() {
  const alerts = [];

  // Перевірка MongoDB
  const mongoClient = await MongoClient.connect('mongodb://localhost:27017');
  const db = mongoClient.db('online_shop');
  
  const serverStatus = await db.admin().serverStatus();
  
  // Alert: Забагато з'єднань
  if (serverStatus.connections.current > 100) {
    alerts.push({
      severity: 'WARNING',
      service: 'MongoDB',
      message: `High connection count: ${serverStatus.connections.current}`
    });
  }

  // Alert: Низька пам'ять
  if (serverStatus.mem.resident > 1000) {  // >1GB
    alerts.push({
      severity: 'WARNING',
      service: 'MongoDB',
      message: `High memory usage: ${serverStatus.mem.resident}MB`
    });
  }

  await mongoClient.close();

  // Перевірка Redis
  const redisClient = redis.createClient();
  await redisClient.connect();
  
  const redisInfo = await redisClient.info('memory');
  const usedMemory = parseInt(redisInfo.match(/used_memory:(\d+)/)[1]);
  
  if (usedMemory > 500 * 1024 * 1024) {  // >500MB
    alerts.push({
      severity: 'WARNING',
      service: 'Redis',
      message: `High memory usage: ${usedMemory / 1024 / 1024}MB`
    });
  }

  await redisClient.quit();

  // Відправка alerts
  if (alerts.length > 0) {
    const emailBody = alerts.map(alert => 
      `[${alert.severity}] ${alert.service}: ${alert.message}`
    ).join('\n');

    await transporter.sendMail({
      from: 'alerts@example.com',
      to: 'admin@example.com',
      subject: `Database Alerts - ${alerts.length} issue(s)`,
      text: emailBody
    });

    console.log(`📧 Sent ${alerts.length} alert(s)`);
  } else {
    console.log('✓ All systems healthy');
  }
}

// Запуск кожні 5 хвилин
setInterval(checkDatabaseHealth, 5 * 60 * 1000);
```

---

## 🎯 Висновок

### **Best Practices:**

**Backup:**
- ✅ Автоматизуйте backup (щоденні + щотижневі)
- ✅ Тестуйте відновлення регулярно
- ✅ Зберігайте backup в різних локаціях
- ✅ Використовуйте інкрементальні backup для економії
- ✅ Шифруйте backup конфіденційних даних

**Моніторинг:**
- ✅ Відстежуйте ключові метрики (CPU, RAM, Disk I/O)
- ✅ Налаштуйте alerting для критичних проблем
- ✅ Аналізуйте повільні запити регулярно
- ✅ Моніторте розмір даних та плануйте масштабування
- ✅ Використовуйте візуалізацію (Grafana, Compass)

**Безпека:**
- ✅ Обмежуйте доступ до backup
- ✅ Використовуйте аутентифікацію
- ✅ Шифруйте з'єднання (TLS/SSL)
- ✅ Регулярно оновлюйте ПЗ
- ✅ Аудит логів доступу