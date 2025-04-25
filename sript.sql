-- Создание базы данных для магазина "Шелкопряд"
CREATE DATABASE IF NOT EXISTS silkweb;
USE silkweb;

-- Роли пользователей
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Статусы заказа
CREATE TABLE IF NOT EXISTS statuses (
    id TINYINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    sequence_order TINYINT NOT NULL
);

-- Таблица ковровых покрытий (продукты)
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(100) NOT NULL,
    fabric VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    pile_height_mm DECIMAL(5,2) NOT NULL COMMENT 'Высота ворса в мм',
    price_per_cm2 DECIMAL(10,4) NOT NULL COMMENT 'Цена за см²',
    image_path VARCHAR(255) DEFAULT NULL
);

-- Таблица типов окантовки края ковра
CREATE TABLE IF NOT EXISTS borders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    image_path VARCHAR(255) DEFAULT NULL
);

-- Таблица пользователей (заказчики и менеджеры)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Таблица заказов
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL COMMENT 'Сумма без учета скидки',
    discount_percent TINYINT NOT NULL DEFAULT 0,
    final_amount DECIMAL(12,2) NOT NULL COMMENT 'Сумма с учетом скидки',
    status_id TINYINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (status_id) REFERENCES statuses(id)
);

-- Таблица пунктов заказа (детали каждого изделия)
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    length_cm DECIMAL(7,2) NOT NULL,
    width_cm DECIMAL(7,2) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    border_id INT NOT NULL,
    item_total DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (border_id) REFERENCES borders(id)
);
















-- ------------------------------------------------------------------
-- Тестовые данные
-- ------------------------------------------------------------------

-- Роли
INSERT INTO roles (name) VALUES
('customer'),
('manager');

-- Статусы
INSERT INTO statuses (id, name, sequence_order) VALUES
(1, 'новый',        1),
(2, 'в обработке',   2),
(3, 'готов',         3),
(4, 'оплачен',       4);

-- Продукты
INSERT INTO products (model, fabric, country, pile_height_mm, price_per_cm2, image_path) VALUES
('Arabesque', 'Полиэстер', 'Турция', 8.00, 0.1500, 'images/arabesque.jpg'),
('Classic',  'Шерсть',    'Иран',    10.00, 0.2000, 'images/classic.jpg'),
('Modern',   'Кодекс',     'Бельгия',  6.50, 0.1800, NULL);

-- Окантовки
INSERT INTO borders (name, image_path) VALUES
('Прямая', 'images/border_rect.jpg'),
('Косая',  'images/border_bias.jpg');

-- Пользователи
INSERT INTO users (email, password, role_id) VALUES
('alice@example.com', 'password123', 1),
('bob.manager@example.com', 'ManagerPass!', 2);

-- Заказы
INSERT INTO orders (user_id, total_amount, discount_percent, final_amount, status_id) VALUES
(1, 5000.00, 0, 5000.00, 1);

-- Позиции заказа (пример Alice)
INSERT INTO order_items (order_id, product_id, length_cm, width_cm, quantity, border_id, item_total) VALUES
(LAST_INSERT_ID(), 1, 200.00, 150.00, 1, 1, 200.00 * 150.00 * 0.1500);
