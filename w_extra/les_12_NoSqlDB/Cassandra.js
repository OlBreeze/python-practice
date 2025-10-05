// ============================================
// CASSANDRA: ЗБЕРІГАННЯ ЛОГІВ ПОДІЙ
// ============================================

const cassandra = require('cassandra-driver');
const { v4: uuidv4 } = require('uuid');

// Створення клієнта Cassandra
const client = new cassandra.Client({
  contactPoints: ['127.0.0.1'],
  localDataCenter: 'datacenter1',
  keyspace: 'event_logs'
});

// ============================================
// 1. СТВОРЕННЯ KEYSPACE ТА ТАБЛИЦІ
// ============================================

async function setupCassandra() {
  console.log('=== НАЛАШТУВАННЯ CASSANDRA ===\n');

  // Підключення без keyspace для створення
  const setupClient = new cassandra.Client({
    contactPoints: ['127.0.0.1'],
    localDataCenter: 'datacenter1'
  });

  await setupClient.connect();
  console.log('✓ Підключено до Cassandra');

  // Створення keyspace з реплікацією
  console.log('\n--- Створення Keyspace ---');
  const createKeyspace = `
    CREATE KEYSPACE IF NOT EXISTS event_logs
    WITH replication = {
      'class': 'SimpleStrategy',
      'replication_factor': 3
    }
  `;

  await setupClient.execute(createKeyspace);
  console.log('✓ Keyspace "event_logs" створено');
  console.log('  Стратегія реплікації: SimpleStrategy');
  console.log('  Фактор реплікації: 3 (дані копіюються на 3 вузли)');

  await setupClient.shutdown();
}

// ============================================
// 2. СТВОРЕННЯ ТАБЛИЦЬ
// ============================================

async function createTables() {
  await client.connect();
  console.log('\n--- Створення таблиць ---');

  // Основна таблиця для логів
  const createEventsTable = `
    CREATE TABLE IF NOT EXISTS events (
      event_id uuid,
      user_id text,
      event_type text,
      timestamp timestamp,
      metadata map<text, text>,
      severity text,
      message text,
      source text,
      PRIMARY KEY ((event_type), timestamp, event_id)
    ) WITH CLUSTERING ORDER BY (timestamp DESC)
  `;

  await client.execute(createEventsTable);
  console.log('✓ Таблиця "events" створена');
  console.log('  Partition Key: event_type (розподіл даних по типу події)');
  console.log('  Clustering Keys: timestamp DESC, event_id');
  console.log('  → Дані сортуються за часом (новіші перші)');

  // Додаткова таблиця для пошуку по користувачу
  const createUserEventsTable = `
    CREATE TABLE IF NOT EXISTS user_events (
      user_id text,
      event_id uuid,
      event_type text,
      timestamp timestamp,
      message text,
      PRIMARY KEY ((user_id), timestamp, event_id)
    ) WITH CLUSTERING ORDER BY (timestamp DESC)
  `;

  await client.execute(createUserEventsTable);
  console.log('✓ Таблиця "user_events" створена (для пошуку по користувачу)');

  // Таблиця для статистики
  const createStatsTable = `
    CREATE TABLE IF NOT EXISTS event_stats (
      event_type text,
      date text,
      hour int,
      count counter,
      PRIMARY KEY ((event_type, date), hour)
    )
  `;

  await client.execute(createStatsTable);
  console.log('✓ Таблиця "event_stats" створена (для статистики)');
}

// ============================================
// 3. CRUD ОПЕРАЦІЇ
// ============================================

class EventLogger {
  constructor(cassandraClient) {
    this.client = cassandraClient;
  }

  // CREATE: Додати новий лог події
  async logEvent(eventData) {
    const eventId = uuidv4();
    const timestamp = new Date();

    const {
      userId,
      eventType,
      message,
      severity = 'info',
      source = 'application',
      metadata = {}
    } = eventData;

    // Вставка в основну таблицю
    const insertEvent = `
      INSERT INTO events (
        event_id, user_id, event_type, timestamp, 
        metadata, severity, message, source
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `;

    await this.client.execute(insertEvent, [
      eventId,
      userId,
      eventType,
      timestamp,
      metadata,
      severity,
      message,
      source
    ], { prepare: true });

    // Вставка в таблицю user_events для швидкого пошуку
    const insertUserEvent = `
      INSERT INTO user_events (
        user_id, event_id, event_type, timestamp, message
      ) VALUES (?, ?, ?, ?, ?)
    `;

    await this.client.execute(insertUserEvent, [
      userId,
      eventId,
      eventType,
      timestamp,
      message
    ], { prepare: true });

    // Оновлення статистики
    const date = timestamp.toISOString().split('T')[0];
    const hour = timestamp.getHours();

    const updateStats = `
      UPDATE event_stats 
      SET count = count + 1 
      WHERE event_type = ? AND date = ? AND hour = ?
    `;

    await this.client.execute(updateStats, [
      eventType,
      date,
      hour
    ], { prepare: true });

    console.log(`✓ Лог створено: ${eventId}`);
    console.log(`  Тип: ${eventType}`);
    console.log(`  Користувач: ${userId}`);
    console.log(`  Час: ${timestamp.toISOString()}`);

    return eventId;
  }

  // READ: Отримати події певного типу за останні 24 години
  async getRecentEvents(eventType, hoursAgo = 24) {
    const since = new Date(Date.now() - hoursAgo * 60 * 60 * 1000);

    const query = `
      SELECT * FROM events 
      WHERE event_type = ? AND timestamp >= ?
      LIMIT 1000
    `;

    const result = await this.client.execute(query, [eventType, since], {
      prepare: true
    });

    console.log(`\n✓ Знайдено ${result.rows.length} подій типу "${eventType}"`);
    console.log(`  За останні ${hoursAgo} годин(и)`);

    return result.rows;
  }

  // READ: Отримати всі події користувача
  async getUserEvents(userId, limit = 100) {
    const query = `
      SELECT * FROM user_events 
      WHERE user_id = ? 
      LIMIT ?
    `;

    const result = await this.client.execute(query, [userId, limit], {
      prepare: true
    });

    console.log(`\n✓ Знайдено ${result.rows.length} подій користувача "${userId}"`);

    return result.rows;
  }

  // UPDATE: Оновити metadata для події
  async updateEventMetadata(eventType, timestamp, eventId, newMetadata) {
    const query = `
      UPDATE events 
      SET metadata = metadata + ? 
      WHERE event_type = ? AND timestamp = ? AND event_id = ?
    `;

    await this.client.execute(query, [
      newMetadata,
      eventType,
      timestamp,
      eventId
    ], { prepare: true });

    console.log(`✓ Metadata оновлено для події ${eventId}`);
    console.log(`  Нові дані:`, newMetadata);
  }

  // DELETE: Видалити старі події (старші за 7 днів)
  async deleteOldEvents(daysAgo = 7) {
    const cutoffDate = new Date(Date.now() - daysAgo * 24 * 60 * 60 * 1000);

    // В Cassandra краще використовувати TTL при вставці,
    // але для демонстрації показуємо явне видалення

    // Спочатку знаходимо всі типи подій
    const eventTypes = ['login', 'logout', 'purchase', 'error', 'api_call'];

    let totalDeleted = 0;

    for (const eventType of eventTypes) {
      // Знаходимо старі події
      const selectQuery = `
        SELECT event_id, timestamp 
        FROM events 
        WHERE event_type = ? AND timestamp < ?
        ALLOW FILTERING
      `;

      const result = await this.client.execute(selectQuery, [
        eventType,
        cutoffDate
      ]);

      // Видаляємо кожну подію
      for (const row of result.rows) {
        const deleteQuery = `
          DELETE FROM events 
          WHERE event_type = ? AND timestamp = ? AND event_id = ?
        `;

        await this.client.execute(deleteQuery, [
          eventType,
          row.timestamp,
          row.event_id
        ], { prepare: true });

        totalDeleted++;
      }
    }

    console.log(`\n✓ Видалено ${totalDeleted} старих подій`);
    console.log(`  Старіше: ${cutoffDate.toISOString()}`);

    return totalDeleted;
  }

  // КРАЩА ПРАКТИКА: Використання TTL при вставці
  async logEventWithTTL(eventData, ttlSeconds = 7 * 24 * 60 * 60) {
    const eventId = uuidv4();
    const timestamp = new Date();

    const insertEvent = `
      INSERT INTO events (
        event_id, user_id, event_type, timestamp, 
        metadata, severity, message, source
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      USING TTL ?
    `;

    await this.client.execute(insertEvent, [
      eventId,
      eventData.userId,
      eventData.eventType,
      timestamp,
      eventData.metadata || {},
      eventData.severity || 'info',
      eventData.message,
      eventData.source || 'application',
      ttlSeconds
    ], { prepare: true });

    console.log(`✓ Лог створено з TTL ${ttlSeconds}с (${ttlSeconds / 86400} днів)`);

    return eventId;
  }

  // Отримати статистику
  async getEventStats(eventType, date) {
    const query = `
      SELECT * FROM event_stats 
      WHERE event_type = ? AND date = ?
    `;

    const result = await this.client.execute(query, [eventType, date], {
      prepare: true
    });

    console.log(`\n📊 Статистика подій "${eventType}" за ${date}:`);

    const hourlyStats = {};
    result.rows.forEach(row => {
      hourlyStats[row.hour] = row.count.toNumber();
    });

    return hourlyStats;
  }
}

// ============================================
// 4. РЕПЛІКАЦІЯ ТА МАСШТАБУВАННЯ
// ============================================

function explainReplicationAndScaling() {
  console.log('\n=== РЕПЛІКАЦІЯ ТА МАСШТАБУВАННЯ В CASSANDRA ===\n');

  console.log('📚 РЕПЛІКАЦІЯ:');
  console.log('─────────────────────────────────────────────────');
  console.log('1. Keyspace визначає стратегію реплікації:');
  console.log('   • SimpleStrategy - для одного датацентру');
  console.log('   • NetworkTopologyStrategy - для кількох датацентрів');
  console.log('');
  console.log('2. Фактор реплікації (RF) визначає кількість копій:');
  console.log('   • RF=1: дані на одному вузлі (без відмовостійкості)');
  console.log('   • RF=3: дані на трьох вузлах (рекомендовано)');
  console.log('   • RF=5: дані на п\'яти вузлах (висока відмовостійкість)');
  console.log('');
  console.log('3. Автоматична реплікація:');
  console.log('   • Cassandra автоматично копіює дані на інші вузли');
  console.log('   • При відмові вузла дані доступні з реплік');
  console.log('   • Немає single point of failure');
  console.log('');

  console.log('⚖️ CONSISTENCY LEVELS:');
  console.log('─────────────────────────────────────────────────');
  console.log('• ONE: відповідь від одного вузла (швидко, менш надійно)');
  console.log('• QUORUM: більшість вузлів (баланс швидкості/надійності)');
  console.log('• ALL: всі вузли (повільно, максимальна надійність)');
  console.log('• LOCAL_QUORUM: більшість у локальному датацентрі');
  console.log('');

  console.log('📈 ГОРИЗОНТАЛЬНЕ МАСШТАБУВАННЯ:');
  console.log('─────────────────────────────────────────────────');
  console.log('1. Додавання нових вузлів:');
  console.log('   • Просто додати новий сервер до кластеру');
  console.log('   • Cassandra автоматично перерозподілить дані');
  console.log('   • Не потрібно зупиняти систему');
  console.log('');
  console.log('2. Partition Key визначає розподіл:');
  console.log('   • event_type як partition key');
  console.log('   • login події → вузли 1, 3, 5');
  console.log('   • error події → вузли 2, 4, 6');
  console.log('   • Рівномірний розподіл навантаження');
  console.log('');
  console.log('3. Лінійне масштабування:');
  console.log('   • 3 вузли → 30K ops/sec');
  console.log('   • 6 вузлів → 60K ops/sec');
  console.log('   • 12 вузлів → 120K ops/sec');
  console.log('');

  console.log('🌍 MULTI-DATACENTER:');
  console.log('─────────────────────────────────────────────────');
  console.log('• Реплікація між датацентрами для геолокації');
  console.log('• Користувачі в Європі → European DC');
  console.log('• Користувачі в США → US DC');
  console.log('• Низька затримка + відмовостійкість');
  console.log('');

  console.log('💾 ПРИКЛАД КОНФІГУРАЦІЇ:');
  console.log('─────────────────────────────────────────────────');
  console.log(`
  CREATE KEYSPACE event_logs
  WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'DC1': 3,  // 3 репліки в датацентрі 1
    'DC2': 3   // 3 репліки в датацентрі 2
  };
  `);
  console.log('');

  console.log('⚙️ ПЕРЕВАГИ:');
  console.log('─────────────────────────────────────────────────');
  console.log('✅ Лінійне масштабування (додаємо вузли = більше потужності)');
  console.log('✅ Немає центральної точки відмови');
  console.log('✅ Автоматичне відновлення після збоїв');
  console.log('✅ Висока доступність (99.99%+)');
  console.log('✅ Підходить дляWrite-Heavy навантаження');
  console.log('✅ Чудово для логів, сенсорів IoT, таймсерій');
  console.log('');
}

// ============================================
// ДЕМОНСТРАЦІЯ
// ============================================

async function demonstrate() {
  try {
    console.log('🚀 CASSANDRA: ДЕМОНСТРАЦІЯ РОБОТИ\n');

    // Налаштування
    await setupCassandra();
    await createTables();

    const logger = new EventLogger(client);

    // CREATE: Логування подій
    console.log('\n=== CREATE: Логування подій ===');

    await logger.logEvent({
      userId: 'user123',
      eventType: 'login',
      message: 'User logged in from Chrome',
      severity: 'info',
      metadata: {
        ip: '192.168.1.100',
        browser: 'Chrome',
        os: 'Windows 10'
      }
    });

    await logger.logEvent({
      userId: 'user456',
      eventType: 'purchase',
      message: 'User purchased laptop',
      severity: 'info',
      metadata: {
        product_id: 'LP001',
        amount: '25000',
        currency: 'UAH'
      }
    });

    await logger.logEvent({
      userId: 'user123',
      eventType: 'error',
      message: 'Failed to load dashboard',
      severity: 'error',
      source: 'frontend',
      metadata: {
        error_code: '500',
        endpoint: '/api/dashboard'
      }
    });

    // Додаємо більше подій для статистики
    for (let i = 0; i < 10; i++) {
      await logger.logEvent({
        userId: `user${100 + i}`,
        eventType: 'api_call',
        message: `API call to /products`,
        severity: 'info'
      });
    }

    // READ: Отримання подій
    console.log('\n=== READ: Отримання подій ===');

    const loginEvents = await logger.getRecentEvents('login', 24);
    if (loginEvents.length > 0) {
      console.log('\nПриклад події:');
      console.log(JSON.stringify(loginEvents[0], null, 2));
    }

    const userEvents = await logger.getUserEvents('user123');
    console.log(`\nПодії користувача user123: ${userEvents.length}`);

    // UPDATE: Оновлення metadata
    console.log('\n=== UPDATE: Оновлення metadata ===');

    if (loginEvents.length > 0) {
      await logger.updateEventMetadata(
        loginEvents[0].event_type,
        loginEvents[0].timestamp,
        loginEvents[0].event_id,
        {
          session_duration: '3600',
          pages_visited: '15'
        }
      );
    }

    // Статистика
    console.log('\n=== СТАТИСТИКА ===');
    const today = new Date().toISOString().split('T')[0];
    const stats = await logger.getEventStats('api_call', today);

    Object.entries(stats).forEach(([hour, count]) => {
      console.log(`  ${hour}:00 - ${count} подій`);
    });

    // TTL Demo
    console.log('\n=== ДЕМОНСТРАЦІЯ TTL ===');
    await logger.logEventWithTTL({
      userId: 'user999',
      eventType: 'test',
      message: 'This event will expire in 60 seconds'
    }, 60);

    // DELETE: Видалення старих подій
    console.log('\n=== DELETE: Видалення старих подій ===');
    console.log('(У продакшені краще використовувати TTL)');

    // Пояснення реплікації та масштабування
    explainReplicationAndScaling();

    console.log('\n✅ Демонстрація завершена!\n');

  } catch (error) {
    console.error('❌ Помилка:', error);
  } finally {
    await client.shutdown();
  }
}

// Запуск
demonstrate();