// ============================================
// POSTGRESQL: ОНЛАЙН-МАГАЗИН - РЕАЛІЗАЦІЯ
// ============================================

const { Client } = require('pg');

const client = new Client({
  host: 'localhost',
  port: 5432,
  database: 'online_shop',
  user: 'postgres',
  password: 'password'
});

async function runPostgreSQLShop() {
  try {
    await client.connect();
    console.log('✓ Підключено до PostgreSQL');

    // ============================================
    // 1. СТВОРЕННЯ ТАБЛИЦЬ (СХЕМА БД)
    // ============================================
    console.log('\n=== 1. СТВОРЕННЯ СХЕМИ БД ===');

    // Видалення існуючих таблиць
    await client.query('DROP TABLE IF EXISTS order_items CASCADE');
    await client.query('DROP TABLE IF EXISTS orders CASCADE');
    await client.query('DROP TABLE IF EXISTS products CASCADE');
    await client.query('DROP TABLE IF EXISTS customers CASCADE');

    // Створення таблиці customers
    await client.query(`
      CREATE TABLE customers (
        customer_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✓ Створено таблицю customers');

    // Створення таблиці products
    await client.query(`
      CREATE TABLE products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        category VARCHAR(50) NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✓ Створено таблицю products');

    // Створення таблиці orders
    await client.query(`
      CREATE TABLE orders (
        order_id SERIAL PRIMARY KEY,
        order_number VARCHAR(50) UNIQUE NOT NULL,
        customer_id INTEGER REFERENCES customers(customer_id),
        total_amount DECIMAL(10, 2) NOT NULL,
        status VARCHAR(20) NOT NULL,
        order_date TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✓ Створено таблицю orders');

    // Створення таблиці order_items
    await client.query(`
      CREATE TABLE order_items (
        order_item_id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
        product_id INTEGER REFERENCES products(product_id),
        product_name VARCHAR(200) NOT NULL,
        quantity INTEGER NOT NULL,
        price DECIMAL(10, 2) NOT NULL
      )
    `);
    console.log('✓ Створено таблицю order_items');

    // ============================================
    // 2. CRUD ОПЕРАЦІЇ
    // ============================================
    console.log('\n=== 2. CRUD ОПЕРАЦІЇ ===');

    // CREATE: Додавання клієнтів
    console.log('\n--- CREATE: Додавання клієнтів ---');
    const customersData = [
      ['Іван Петренко', 'ivan@example.com', '+380501234567'],
      ['Марія Коваленко', 'maria@example.com', '+380671234567'],
      ['Олег Сидоренко', 'oleg@example.com', '+380931234567']
    ];

    for (const [name, email, phone] of customersData) {
      await client.query(
        'INSERT INTO customers (name, email, phone) VALUES ($1, $2, $3)',
        [name, email, phone]
      );
    }
    console.log(`✓ Додано ${customersData.length} клієнтів`);

    // CREATE: Додавання продуктів
    console.log('\n--- CREATE: Додавання продуктів ---');
    const productsData = [
      ['Ноутбук Lenovo ThinkPad', 25000, 'Електроніка', 15],
      ['Мишка Logitech MX Master', 2500, 'Аксесуари', 50],
      ['Монітор Dell 27"', 8000, 'Електроніка', 20],
      ['Клавіатура Keychron K2', 3500, 'Аксесуари', 0],
      ['Навушники Sony WH-1000XM5', 12000, 'Аудіо', 30]
    ];

    for (const [name, price, category, stock] of productsData) {
      await client.query(
        'INSERT INTO products (name, price, category, stock) VALUES ($1, $2, $3, $4)',
        [name, price, category, stock]
      );
    }
    console.log(`✓ Додано ${productsData.length} продуктів`);

    // CREATE: Додавання замовлень (з транзакцією)
    console.log('\n--- CREATE: Додавання замовлень ---');

    await client.query('BEGIN');
    try {
      // Замовлення 1
      const order1 = await client.query(
        `INSERT INTO orders (order_number, customer_id, total_amount, status, order_date)
         VALUES ($1, $2, $3, $4, $5) RETURNING order_id`,
        ['ORD-2025-001', 1, 27500, 'completed', new Date(Date.now() - 10 * 24 * 60 * 60 * 1000)]
      );
      await client.query(
        'INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES ($1, $2, $3, $4, $5)',
        [order1.rows[0].order_id, 1, 'Ноутбук Lenovo ThinkPad', 1, 25000]
      );
      await client.query(
        'INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES ($1, $2, $3, $4, $5)',
        [order1.rows[0].order_id, 2, 'Мишка Logitech MX Master', 1, 2500]
      );

      // Замовлення 2
      const order2 = await client.query(
        `INSERT INTO orders (order_number, customer_id, total_amount, status, order_date)
         VALUES ($1, $2, $3, $4, $5) RETURNING order_id`,
        ['ORD-2025-002', 2, 24000, 'processing', new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)]
      );
      await client.query(
        'INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES ($1, $2, $3, $4, $5)',
        [order2.rows[0].order_id, 5, 'Навушники Sony WH-1000XM5', 2, 12000]
      );

      // Замовлення 3
      const order3 = await client.query(
        `INSERT INTO orders (order_number, customer_id, total_amount, status, order_date)
         VALUES ($1, $2, $3, $4, $5) RETURNING order_id`,
        ['ORD-2025-003', 1, 8000, 'completed', new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)]
      );
      await client.query(
        'INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES ($1, $2, $3, $4, $5)',
        [order3.rows[0].order_id, 3, 'Монітор Dell 27"', 1, 8000]
      );

      await client.query('COMMIT');
      console.log('✓ Додано 3 замовлення');
    } catch (err) {
      await client.query('ROLLBACK');
      throw err;
    }

    // READ: Витягнути всі замовлення за останні 30 днів
    console.log('\n--- READ: Замовлення за останні 30 днів ---');
    const recentOrders = await client.query(`
      SELECT o.order_number, c.name as customer_name, o.total_amount, o.order_date
      FROM orders o
      JOIN customers c ON o.customer_id = c.customer_id
      WHERE o.order_date >= CURRENT_TIMESTAMP - INTERVAL '30 days'
      ORDER BY o.order_date DESC
    `);

    console.log(`Знайдено ${recentOrders.rows.length} замовлень:`);
    recentOrders.rows.forEach(order => {
      console.log(`- ${order.order_number}: ${order.customer_name}, сума: ${order.total_amount} грн`);
    });

    // UPDATE: Оновити кількість продукту на складі
    console.log('\n--- UPDATE: Оновлення кількості на складі ---');
    const updateResult = await client.query(`
      UPDATE products 
      SET stock = stock - 1, updated_at = CURRENT_TIMESTAMP
      WHERE product_id = 1
      RETURNING name, stock
    `);

    console.log(`✓ Оновлено продукт: ${updateResult.rows[0].name}`);
    console.log(`  Нова кількість: ${updateResult.rows[0].stock}`);

    // DELETE: Видалити продукти, яких немає на складі
    console.log('\n--- DELETE: Видалення недоступних продуктів ---');
    const deleteResult = await client.query(`
      DELETE FROM products WHERE stock = 0
    `);
    console.log(`✓ Видалено ${deleteResult.rowCount} недоступних продуктів`);

    // ============================================
    // 3. АГРЕГАЦІЯ ДАНИХ (АНАЛІТИЧНІ ЗАПИТИ)
    // ============================================
    console.log('\n=== 3. АГРЕГАЦІЯ ДАНИХ ===');

    // Підрахунок загальної кількості проданих продуктів
    console.log('\n--- Статистика продажів ---');
    const soldProducts = await client.query(`
      SELECT 
        oi.product_name,
        SUM(oi.quantity) as total_quantity,
        SUM(oi.quantity * oi.price) as total_revenue
      FROM order_items oi
      JOIN orders o ON oi.order_id = o.order_id
      WHERE o.status = 'completed'
      GROUP BY oi.product_name
      ORDER BY total_quantity DESC
    `);

    console.log('Статистика продажів:');
    soldProducts.rows.forEach(item => {
      console.log(`- ${item.product_name}: ${item.total_quantity} шт., виручка: ${item.total_revenue} грн`);
    });

    // Підрахунок загальної суми всіх замовлень по клієнтах
    console.log('\n--- Статистика по клієнтах ---');
    const customerTotals = await client.query(`
      SELECT 
        c.name,
        c.email,
        COUNT(o.order_id) as total_orders,
        SUM(o.total_amount) as total_spent,
        STRING_AGG(o.order_number, ', ') as order_numbers
      FROM customers c
      JOIN orders o ON c.customer_id = o.customer_id
      GROUP BY c.customer_id, c.name, c.email
      ORDER BY total_spent DESC
    `);

    console.log('Статистика по клієнтах:');
    customerTotals.rows.forEach(customer => {
      console.log(`\nКлієнт: ${customer.name} (${customer.email})`);
      console.log(`  Замовлень: ${customer.total_orders}`);
      console.log(`  Загальна сума: ${customer.total_spent} грн`);
      console.log(`  Номери замовлень: ${customer.order_numbers}`);
    });

    // Статистика по категоріях
    console.log('\n--- Продажі по категоріях ---');
    const categoryStats = await client.query(`
      SELECT 
        p.category,
        SUM(oi.quantity) as total_items_sold,
        SUM(oi.quantity * oi.price) as total_revenue
      FROM order_items oi
      JOIN orders o ON oi.order_id = o.order_id
      JOIN products p ON oi.product_id = p.product_id
      WHERE o.status = 'completed'
      GROUP BY p.category
      ORDER BY total_revenue DESC
    `);

    console.log('Продажі по категоріях:');
    categoryStats.rows.forEach(cat => {
      console.log(`- ${cat.category}: ${cat.total_items_sold} шт., ${cat.total_revenue} грн`);
    });

    // ============================================
    // 4. ІНДЕКСИ
    // ============================================
    console.log('\n=== 4. СТВОРЕННЯ ІНДЕКСІВ ===');

    await client.query('CREATE INDEX idx_products_category ON products(category)');
    console.log('✓ Створено індекс для products.category');

    await client.query('CREATE INDEX idx_products_price ON products(price)');
    console.log('✓ Створено індекс для products.price');

    await client.query('CREATE INDEX idx_orders_date ON orders(order_date DESC)');
    console.log('✓ Створено індекс для orders.order_date');

    await client.query('CREATE INDEX idx_customers_email ON customers(email)');
    console.log('✓ Створено індекс для customers.email');

    await client.query('CREATE INDEX idx_orders_customer ON orders(customer_id)');
    console.log('✓ Створено індекс для orders.customer_id');

    // Показати план виконання запиту
    console.log('\n--- EXPLAIN: Аналіз плану запиту ---');
    const explainResult = await client.query(`
      EXPLAIN ANALYZE
      SELECT * FROM products WHERE category = 'Електроніка'
    `);

    console.log('План виконання запиту з індексом:');
    explainResult.rows.forEach(row => {
      console.log(row['QUERY PLAN']);
    });

    console.log('\n✓ Всі операції PostgreSQL виконано успішно!');

  } catch (error) {
    console.error('Помилка:', error);
  } finally {
    await client.end();
    console.log('\n✓ З\'єднання з PostgreSQL закрито');
  }
}

// Запуск
runPostgreSQLShop();