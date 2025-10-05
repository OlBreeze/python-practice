// ============================================
// REDIS: УПРАВЛІННЯ СЕСІЯМИ КОРИСТУВАЧІВ
// ============================================

const redis = require('redis');
const crypto = require('crypto');

// Створення клієнта Redis
const client = redis.createClient({
  host: 'localhost',
  port: 6379
});

client.on('error', (err) => console.error('Redis Error:', err));
client.on('connect', () => console.log('✓ Підключено до Redis'));

// Генерація унікального токена
function generateSessionToken() {
  return crypto.randomBytes(32).toString('hex');
}

// ============================================
// 1. ЗБЕРЕЖЕННЯ СЕСІЙ КОРИСТУВАЧІВ
// ============================================

class SessionManager {
  constructor(redisClient) {
    this.client = redisClient;
    this.SESSION_TTL = 1800; // 30 хвилин в секундах
  }

  // ============================================
  // CREATE: Створити нову сесію
  // ============================================
  async createSession(userId, userInfo = {}) {
    const sessionToken = generateSessionToken();
    const sessionKey = `session:${sessionToken}`;

    const sessionData = {
      user_id: userId,
      session_token: sessionToken,
      login_time: new Date().toISOString(),
      last_activity: new Date().toISOString(),
      ip_address: userInfo.ip || 'unknown',
      user_agent: userInfo.userAgent || 'unknown',
      ...userInfo
    };

    // Зберігаємо сесію як hash
    await this.client.hSet(sessionKey, sessionData);

    // Встановлюємо TTL (час життя)
    await this.client.expire(sessionKey, this.SESSION_TTL);

    // Додаємо токен до списку активних сесій користувача
    await this.client.sAdd(`user:${userId}:sessions`, sessionToken);

    console.log(`✓ Створено сесію для користувача ${userId}`);
    console.log(`  Токен: ${sessionToken}`);
    console.log(`  TTL: ${this.SESSION_TTL} секунд`);

    return sessionToken;
  }

  // ============================================
  // READ: Отримати активну сесію
  // ============================================
  async getSession(sessionToken) {
    const sessionKey = `session:${sessionToken}`;

    // Перевіряємо чи існує сесія
    const exists = await this.client.exists(sessionKey);
    if (!exists) {
      console.log(`✗ Сесія ${sessionToken} не знайдена або закінчилась`);
      return null;
    }

    // Отримуємо всі дані сесії
    const sessionData = await this.client.hGetAll(sessionKey);

    console.log(`✓ Знайдено сесію:`);
    console.log(`  User ID: ${sessionData.user_id}`);
    console.log(`  Login: ${sessionData.login_time}`);
    console.log(`  Last Activity: ${sessionData.last_activity}`);

    return sessionData;
  }

  // Отримати всі активні сесії користувача
  async getUserSessions(userId) {
    const sessionTokens = await this.client.sMembers(`user:${userId}:sessions`);

    console.log(`\n✓ Активні сесії користувача ${userId}:`);
    const sessions = [];

    for (const token of sessionTokens) {
      const session = await this.getSession(token);
      if (session) {
        sessions.push(session);
      } else {
        // Видаляємо неіснуючі токени з набору
        await this.client.sRem(`user:${userId}:sessions`, token);
      }
    }

    return sessions;
  }

  // ============================================
  // UPDATE: Оновити час останньої активності
  // ============================================
  async updateActivity(sessionToken) {
    const sessionKey = `session:${sessionToken}`;

    const exists = await this.client.exists(sessionKey);
    if (!exists) {
      console.log(`✗ Сесія ${sessionToken} не існує`);
      return false;
    }

    // Оновлюємо час останньої активності
    await this.client.hSet(sessionKey, 'last_activity', new Date().toISOString());

    // Продовжуємо TTL
    await this.client.expire(sessionKey, this.SESSION_TTL);

    console.log(`✓ Оновлено активність для сесії ${sessionToken.substring(0, 16)}...`);
    console.log(`  Новий TTL: ${this.SESSION_TTL} секунд`);

    return true;
  }

  // Оновити дані сесії
  async updateSessionData(sessionToken, updates) {
    const sessionKey = `session:${sessionToken}`;

    const exists = await this.client.exists(sessionKey);
    if (!exists) {
      console.log(`✗ Сесія не існує`);
      return false;
    }

    // Оновлюємо поля
    for (const [key, value] of Object.entries(updates)) {
      await this.client.hSet(sessionKey, key, value);
    }

    console.log(`✓ Оновлено дані сесії ${sessionToken.substring(0, 16)}...`);
    return true;
  }

  // ============================================
  // DELETE: Видалити сесію (logout)
  // ============================================
  async deleteSession(sessionToken) {
    const sessionKey = `session:${sessionToken}`;

    // Отримуємо user_id перед видаленням
    const userId = await this.client.hGet(sessionKey, 'user_id');

    // Видаляємо сесію
    const deleted = await this.client.del(sessionKey);

    if (deleted && userId) {
      // Видаляємо токен з набору сесій користувача
      await this.client.sRem(`user:${userId}:sessions`, sessionToken);
      console.log(`✓ Сесію ${sessionToken.substring(0, 16)}... видалено`);
      return true;
    }

    console.log(`✗ Сесія не знайдена`);
    return false;
  }

  // Видалити всі сесії користувача
  async deleteAllUserSessions(userId) {
    const sessionTokens = await this.client.sMembers(`user:${userId}:sessions`);

    let deleted = 0;
    for (const token of sessionTokens) {
      const result = await this.deleteSession(token);
      if (result) deleted++;
    }

    console.log(`✓ Видалено ${deleted} сесій користувача ${userId}`);
    return deleted;
  }

  // ============================================
  // 3. TTL (Time to Live)
  // ============================================

  // Перевірити залишковий час життя сесії
  async getSessionTTL(sessionToken) {
    const sessionKey = `session:${sessionToken}`;
    const ttl = await this.client.ttl(sessionKey);

    if (ttl === -2) {
      console.log(`✗ Сесія не існує`);
      return null;
    }

    if (ttl === -1) {
      console.log(`⚠ Сесія існує, але не має TTL (не закінчиться автоматично)`);
      return -1;
    }

    const minutes = Math.floor(ttl / 60);
    const seconds = ttl % 60;
    console.log(`⏱ Залишок часу сесії: ${minutes}м ${seconds}с`);

    return ttl;
  }

  // Налаштувати інший TTL для конкретної сесії
  async setCustomTTL(sessionToken, ttlSeconds) {
    const sessionKey = `session:${sessionToken}`;
    const result = await this.client.expire(sessionKey, ttlSeconds);

    if (result) {
      console.log(`✓ Встановлено TTL ${ttlSeconds}с для сесії`);
    } else {
      console.log(`✗ Не вдалося встановити TTL (сесія не існує)`);
    }

    return result;
  }

  // ============================================
  // ДОДАТКОВІ ФУНКЦІЇ
  // ============================================

  // Підрахунок активних сесій
  async getActiveSessionsCount() {
    const keys = await this.client.keys('session:*');
    console.log(`📊 Всього активних сесій: ${keys.length}`);
    return keys.length;
  }

  // Статистика по користувачах
  async getUserStats(userId) {
    const sessions = await this.getUserSessions(userId);
    const sessionCount = sessions.length;

    if (sessionCount === 0) {
      console.log(`📊 Користувач ${userId} не має активних сесій`);
      return null;
    }

    const loginTimes = sessions.map(s => new Date(s.login_time));
    const lastLogin = new Date(Math.max(...loginTimes));

    console.log(`📊 Статистика користувача ${userId}:`);
    console.log(`  Активних сесій: ${sessionCount}`);
    console.log(`  Останній вхід: ${lastLogin.toISOString()}`);

    return {
      userId,
      sessionCount,
      lastLogin
    };
  }

  // Очистити всі сесії (для тестування)
  async clearAllSessions() {
    const sessionKeys = await this.client.keys('session:*');
    const userKeys = await this.client.keys('user:*:sessions');

    if (sessionKeys.length > 0) {
      await this.client.del(sessionKeys);
    }
    if (userKeys.length > 0) {
      await this.client.del(userKeys);
    }

    console.log(`🧹 Очищено ${sessionKeys.length} сесій`);
  }
}

// ============================================
// ДЕМОНСТРАЦІЯ РОБОТИ
// ============================================

async function demonstrateRedis() {
  await client.connect();

  const sessionManager = new SessionManager(client);

  console.log('\n=== ДЕМОНСТРАЦІЯ РОБОТИ З REDIS ===\n');

  // Очищення для демонстрації
  await sessionManager.clearAllSessions();

  // 1. CREATE: Створення сесій
  console.log('\n--- 1. CREATE: Створення сесій ---');
  const token1 = await sessionManager.createSession('user123', {
    ip: '192.168.1.100',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
  });

  const token2 = await sessionManager.createSession('user123', {
    ip: '192.168.1.101',
    userAgent: 'Mobile Safari/15.0'
  });

  const token3 = await sessionManager.createSession('user456', {
    ip: '10.0.0.5',
    userAgent: 'Chrome/120.0'
  });

  // 2. READ: Читання сесій
  console.log('\n--- 2. READ: Читання сесій ---');
  await sessionManager.getSession(token1);

  console.log('\n--- Всі сесії користувача user123 ---');
  await sessionManager.getUserSessions('user123');

  // 3. UPDATE: Оновлення активності
  console.log('\n--- 3. UPDATE: Оновлення активності ---');

  // Симуляція паузи
  await new Promise(resolve => setTimeout(resolve, 2000));

  await sessionManager.updateActivity(token1);

  // Оновлення додаткових даних
  await sessionManager.updateSessionData(token1, {
    last_page: '/dashboard',
    cart_items: '3'
  });

  // 4. TTL: Робота з часом життя
  console.log('\n--- 4. TTL: Перевірка часу життя ---');
  await sessionManager.getSessionTTL(token1);

  // Встановлення іншого TTL (наприклад, "Remember me" - 7 днів)
  await sessionManager.setCustomTTL(token2, 7 * 24 * 60 * 60);
  await sessionManager.getSessionTTL(token2);

  // 5. Статистика
  console.log('\n--- 5. СТАТИСТИКА ---');
  await sessionManager.getActiveSessionsCount();
  await sessionManager.getUserStats('user123');

  // 6. DELETE: Видалення сесій
  console.log('\n--- 6. DELETE: Видалення сесій ---');
  await sessionManager.deleteSession(token1);

  // Перевірка після видалення
  await sessionManager.getSession(token1);

  // Видалення всіх сесій користувача (logout на всіх пристроях)
  console.log('\n--- Logout на всіх пристроях ---');
  await sessionManager.deleteAllUserSessions('user123');

  console.log('\n--- Фінальна статистика ---');
  await sessionManager.getActiveSessionsCount();

  // 7. Демонстрація автоматичного видалення по TTL
  console.log('\n--- 7. ДЕМОНСТРАЦІЯ AUTO-EXPIRE ---');
  console.log('Створюємо сесію з TTL 5 секунд...');
  const shortToken = await sessionManager.createSession('user789', {
    ip: '127.0.0.1'
  });
  await sessionManager.setCustomTTL(shortToken, 5);

  console.log('Перевіряємо існування...');
  await sessionManager.getSession(shortToken);

  console.log('\nЧекаємо 6 секунд...');
  await new Promise(resolve => setTimeout(resolve, 6000));

  console.log('Перевіряємо після закінчення TTL...');
  await sessionManager.getSession(shortToken);

  console.log('\n✓ Демонстрація Redis завершена!');

  await client.quit();
}

// Запуск
demonstrateRedis().catch(console.error);

// ============================================
// ДОДАТКОВО: ПРИКЛАД ВИКОРИСТАННЯ В EXPRESS
// ============================================

/*
const express = require('express');
const app = express();

const sessionManager = new SessionManager(client);

// Middleware для перевірки сесії
async function authenticateSession(req, res, next) {
  const token = req.headers['authorization']?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'No session token' });
  }

  const session = await sessionManager.getSession(token);

  if (!session) {
    return res.status(401).json({ error: 'Invalid or expired session' });
  }

  // Оновлюємо активність
  await sessionManager.updateActivity(token);

  // Додаємо дані сесії до request
  req.session = session;
  req.userId = session.user_id;

  next();
}

// Endpoint для login
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;

  // Тут має бути перевірка credentials
  const userId = 'user123'; // отримано після аутентифікації

  const token = await sessionManager.createSession(userId, {
    ip: req.ip,
    userAgent: req.get('user-agent')
  });

  res.json({ token });
});

// Захищений endpoint
app.get('/api/profile', authenticateSession, async (req, res) => {
  res.json({
    userId: req.userId,
    session: req.session
  });
});

// Endpoint для logout
app.post('/api/logout', authenticateSession, async (req, res) => {
  const token = req.headers['authorization']?.replace('Bearer ', '');
  await sessionManager.deleteSession(token);
  res.json({ message: 'Logged out successfully' });
});

// Logout на всіх пристроях
app.post('/api/logout-all', authenticateSession, async (req, res) => {
  await sessionManager.deleteAllUserSessions(req.userId);
  res.json({ message: 'Logged out from all devices' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
*/