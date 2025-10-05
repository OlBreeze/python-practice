// ============================================
// MONGODB: ОНЛАЙН-МАГАЗИН - ПОВНА РЕАЛІЗАЦІЯ
// ============================================

// Підключення до MongoDB
const { MongoClient } = require('mongodb');

const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri);

async function runOnlineShop() {
  try {
    await client.connect();
    console.log('✓ Підключено до MongoDB');

    const db = client.db('online_shop');
    const products = db.collection('products');
    const orders = db.collection('orders');

    // ============================================
    // 1. СТВОРЕННЯ БАЗИ ДАНИХ ТА КОЛЕКЦІЙ
    // ============================================
    console.log('\n=== 1. СТВОРЕННЯ КОЛЕКЦІЙ ===');

    // Очищення колекцій для демонстрації
    await products.deleteMany({});
    await orders.deleteMany({});

    // ============================================
    // 2. CRUD ОПЕРАЦІЇ
    // ============================================
    console.log('\n=== 2. CRUD ОПЕРАЦІЇ ===');

    // CREATE: Додавання продуктів
    console.log('\n--- CREATE: Додавання продуктів ---');
    const productsData = [
      {
        name: 'Ноутбук Lenovo ThinkPad',
        price: 25000,
        category: 'Електроніка',
        stock: 15,
        created_at: new Date()
      },
      {
        name: 'Мишка Logitech MX Master',
        price: 2500,
        category: 'Аксесуари',
        stock: 50,
        created_at: new Date()
      },
      {
        name: 'Монітор Dell 27"',
        price: 8000,
        category: 'Електроніка',
        stock: 20,
        created_at: new Date()
      },
      {
        name: 'Клавіатура Keychron K2',
        price: 3500,
        category: 'Аксесуари',
        stock: 0, // Немає на складі
        created_at: new Date()
      },
      {
        name: 'Навушники Sony WH-1000XM5',
        price: 12000,
        category: 'Аудіо',
        stock: 30,
        created_at: new Date()
      }
    ];

    const insertedProducts = await products.insertMany(productsData);
    console.log(`Додано ${insertedProducts.insertedCount} продуктів`);

    // CREATE: Додавання замовлень
    console.log('\n--- CREATE: Додавання замовлень ---');
    const ordersData = [
      {
        order_number: 'ORD-2025-001',
        customer: {
          name: 'Іван Петренко',
          email: 'ivan@example.com',
          phone: '+380501234567'
        },
        items: [
          {
            product_id: insertedProducts.insertedIds[0],
            product_name: 'Ноутбук Lenovo ThinkPad',
            quantity: 1,
            price: 25000
          },
          {
            product_id: insertedProducts.insertedIds[1],
            product_name: 'Мишка Logitech MX Master',
            quantity: 1,
            price: 2500
          }
        ],
        total_amount: 27500,
        status: 'completed',
        order_date: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000), // 10 днів тому
        created_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000)
      },
      {
        order_number: 'ORD-2025-002',
        customer: {
          name: 'Марія Коваленко',
          email: 'maria@example.com',
          phone: '+380671234567'
        },
        items: [
          {
            product_id: insertedProducts.insertedIds[4],
            product_name: 'Навушники Sony WH-1000XM5',
            quantity: 2,
            price: 12000
          }
        ],
        total_amount: 24000,
        status: 'processing',
        order_date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000), // 5 днів тому
        created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
      },
      {
        order_number: 'ORD-2025-003',
        customer: {
          name: 'Іван Петренко',
          email: 'ivan@example.com',
          phone: '+380501234567'
        },
        items: [
          {
            product_id: insertedProducts.insertedIds[2],
            product_name: 'Монітор Dell 27"',
            quantity: 1,
            price: 8000
          }
        ],
        total_amount: 8000,
        status: 'completed',
        order_date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 дні тому
        created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
      },
      {
        order_number: 'ORD-2025-004',
        customer: {
          name: 'Олег Сидоренко',
          email: 'oleg@example.com',
          phone: '+380931234567'
        },
        items: [
          {
            product_id: insertedProducts.insertedIds[0],
            product_name: 'Ноутбук Lenovo ThinkPad',
            quantity: 1,
            price: 25000
          }
        ],
        total_amount: 25000,
        status: 'pending',
        order_date: new Date(), // Сьогодні
        created_at: new Date()
      }
    ];

    const insertedOrders = await orders.insertMany(ordersData);
    console.log(`Додано ${insertedOrders.insertedCount} замовлень`);

    // READ: Витягнути всі замовлення за останні 30 днів
    console.log('\n--- READ: Замовлення за останні 30 днів ---');
    const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
    const recentOrders = await orders.find({
      order_date: { $gte: thirtyDaysAgo }
    }).toArray();

    console.log(`Знайдено ${recentOrders.length} замовлень за останні 30 днів:`);
    recentOrders.forEach(order => {
      console.log(`- ${order.order_number}: ${order.customer.name}, сума: ${order.total_amount} грн`);
    });

    // UPDATE: Оновити кількість продукту на складі після покупки
    console.log('\n--- UPDATE: Оновлення кількості на складі ---');
    const laptopPurchase = {
      product_id: insertedProducts.insertedIds[0],
      quantity: 1
    };

    const updateResult = await products.updateOne(
      { _id: laptopPurchase.product_id },
      {
        $inc: { stock: -laptopPurchase.quantity },
        $set: { updated_at: new Date() }
      }
    );

    console.log(`Оновлено ${updateResult.modifiedCount} продукт(ів)`);
    const updatedProduct = await products.findOne({ _id: laptopPurchase.product_id });
    console.log(`Нова кількість "${updatedProduct.name}": ${updatedProduct.stock}`);

    // DELETE: Видалити продукти, яких немає на складі
    console.log('\n--- DELETE: Видалення недоступних продуктів ---');
    const deleteResult = await products.deleteMany({ stock: 0 });
    console.log(`Видалено ${deleteResult.deletedCount} недоступних продуктів`);

    // ============================================
    // 3. АГРЕГАЦІЯ ДАНИХ
    // ============================================
    console.log('\n=== 3. АГРЕГАЦІЯ ДАНИХ ===');

    // Підрахунок загальної кількості проданих продуктів
    console.log('\n--- Загальна кількість проданих продуктів ---');
    const soldProductsAgg = await orders.aggregate([
      { $match: { status: 'completed' } },
      { $unwind: '$items' },
      {
        $group: {
          _id: '$items.product_name',
          total_quantity: { $sum: '$items.quantity' },
          total_revenue: { $sum: { $multiply: ['$items.quantity', '$items.price'] } }
        }
      },
      { $sort: { total_quantity: -1 } }
    ]).toArray();

    console.log('Статистика продажів:');
    soldProductsAgg.forEach(item => {
      console.log(`- ${item._id}: ${item.total_quantity} шт., виручка: ${item.total_revenue} грн`);
    });

    // Підрахунок загальної суми всіх замовлень клієнта
    console.log('\n--- Загальна сума замовлень по клієнтах ---');
    const customerTotalsAgg = await orders.aggregate([
      {
        $group: {
          _id: '$customer.email',
          customer_name: { $first: '$customer.name' },
          total_orders: { $sum: 1 },
          total_spent: { $sum: '$total_amount' },
          orders: { $push: '$order_number' }
        }
      },
      { $sort: { total_spent: -1 } }
    ]).toArray();

    console.log('Статистика по клієнтах:');
    customerTotalsAgg.forEach(customer => {
      console.log(`\nКлієнт: ${customer.customer_name} (${customer._id})`);
      console.log(`  Замовлень: ${customer.total_orders}`);
      console.log(`  Загальна сума: ${customer.total_spent} грн`);
      console.log(`  Номери замовлень: ${customer.orders.join(', ')}`);
    });

    // Додаткова агрегація: статистика по категоріях
    console.log('\n--- Статистика продажів по категоріях ---');
    const categoryStats = await orders.aggregate([
      { $match: { status: 'completed' } },
      { $unwind: '$items' },
      {
        $lookup: {
          from: 'products',
          localField: 'items.product_id',
          foreignField: '_id',
          as: 'product_info'
        }
      },
      { $unwind: { path: '$product_info', preserveNullAndEmptyArrays: true } },
      {
        $group: {
          _id: '$product_info.category',
          total_items_sold: { $sum: '$items.quantity' },
          total_revenue: { $sum: { $multiply: ['$items.quantity', '$items.price'] } }
        }
      },
      { $sort: { total_revenue: -1 } }
    ]).toArray();

    console.log('Продажі по категоріях:');
    categoryStats.forEach(cat => {
      console.log(`- ${cat._id || 'Невідома категорія'}: ${cat.total_items_sold} шт., ${cat.total_revenue} грн`);
    });

    // ============================================
    // 4. ІНДЕКСИ
    // ============================================
    console.log('\n=== 4. СТВОРЕННЯ ІНДЕКСІВ ===');

    // Індекс для category
    await products.createIndex({ category: 1 });
    console.log('✓ Створено індекс для поля "category"');

    // Додаткові корисні індекси
    await products.createIndex({ price: 1 });
    console.log('✓ Створено індекс для поля "price"');

    await orders.createIndex({ order_date: -1 });
    console.log('✓ Створено індекс для поля "order_date"');

    await orders.createIndex({ 'customer.email': 1 });
    console.log('✓ Створено індекс для поля "customer.email"');

    // Показати всі індекси
    console.log('\n--- Список індексів для products ---');
    const productIndexes = await products.indexes();
    productIndexes.forEach(index => {
      console.log(`- ${index.name}: ${JSON.stringify(index.key)}`);
    });

    console.log('\n--- Список індексів для orders ---');
    const orderIndexes = await orders.indexes();
    orderIndexes.forEach(index => {
      console.log(`- ${index.name}: ${JSON.stringify(index.key)}`);
    });

    // Демонстрація швидкості пошуку з індексом
    console.log('\n--- Тестування швидкості пошуку ---');
    console.time('Пошук з індексом (category)');
    const electronicsProducts = await products.find({ category: 'Електроніка' }).toArray();
    console.timeEnd('Пошук з індексом (category)');
    console.log(`Знайдено ${electronicsProducts.length} продуктів в категорії "Електроніка"`);

    console.log('\n✓ Всі операції MongoDB виконано успішно!');

  } catch (error) {
    console.error('Помилка:', error);
  } finally {
    await client.close();
    console.log('\n✓ З\'єднання з MongoDB закрито');
  }
}

// Запуск
runOnlineShop();