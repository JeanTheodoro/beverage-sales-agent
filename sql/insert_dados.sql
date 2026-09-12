SET search_path TO delivery, public;

INSERT INTO delivery.products
    (name, description, category, volume, price, stock_quantity, is_active)
VALUES

-- =====================================================
-- CERVEJAS
-- =====================================================

('Skol',
 'Cerveja Skol Pilsen leve e refrescante.',
 'cerveja',
 '350ml',
 4.50,
 100,
 TRUE),

('Skol',
 'Cerveja Skol Pilsen leve e refrescante.',
 'cerveja',
 '600ml',
 7.50,
 80,
 TRUE),

('Skol',
 'Cerveja Skol Pilsen em garrafa de dois litros.',
 'cerveja',
 '2L',
 18.00,
 30,
 TRUE),

('Brahma',
 'Cerveja Brahma Chopp Pilsen leve e refrescante.',
 'cerveja',
 '350ml',
 4.50,
 100,
 TRUE),

('Brahma',
 'Cerveja Brahma Chopp Pilsen em garrafa.',
 'cerveja',
 '600ml',
 7.50,
 80,
 TRUE),

('Brahma',
 'Cerveja Brahma Chopp em garrafa de dois litros.',
 'cerveja',
 '2L',
 18.00,
 30,
 TRUE),

('Heineken',
 'Cerveja Heineken Puro Malte de sabor marcante.',
 'cerveja',
 '350ml',
 6.50,
 60,
 TRUE),

('Heineken',
 'Cerveja Heineken Puro Malte em garrafa.',
 'cerveja',
 '600ml',
 11.00,
 40,
 TRUE),

('Corona',
 'Cerveja Corona Extra leve e refrescante.',
 'cerveja',
 '330ml',
 7.50,
 50,
 TRUE),

('Amstel',
 'Cerveja Amstel Puro Malte leve e equilibrada.',
 'cerveja',
 '350ml',
 5.00,
 70,
 TRUE),

('Amstel',
 'Cerveja Amstel Puro Malte em garrafa.',
 'cerveja',
 '600ml',
 8.00,
 50,
 TRUE),


-- =====================================================
-- REFRIGERANTES
-- =====================================================

('Coca-Cola',
 'Refrigerante Coca-Cola sabor original.',
 'refrigerante',
 '350ml',
 4.00,
 100,
 TRUE),

('Coca-Cola',
 'Refrigerante Coca-Cola sabor original em garrafa de dois litros.',
 'refrigerante',
 '2L',
 10.00,
 60,
 TRUE),

('Guaraná Antarctica',
 'Refrigerante Guaraná Antarctica sabor original.',
 'refrigerante',
 '350ml',
 4.00,
 100,
 TRUE),

('Guaraná Antarctica',
 'Refrigerante Guaraná Antarctica em garrafa de dois litros.',
 'refrigerante',
 '2L',
 9.00,
 60,
 TRUE),

('Fanta',
 'Refrigerante Fanta sabor laranja.',
 'refrigerante',
 '350ml',
 4.00,
 80,
 TRUE),

('Fanta',
 'Refrigerante Fanta sabor laranja em garrafa de dois litros.',
 'refrigerante',
 '2L',
 9.00,
 50,
 TRUE),

('Sprite',
 'Refrigerante Sprite sabor limão.',
 'refrigerante',
 '350ml',
 4.00,
 80,
 TRUE),

('Sprite',
 'Refrigerante Sprite sabor limão em garrafa de dois litros.',
 'refrigerante',
 '2L',
 9.00,
 50,
 TRUE),


-- =====================================================
-- ÁGUAS
-- =====================================================

('Água Mineral',
 'Água mineral sem gás para consumo.',
 'agua',
 '500ml',
 2.50,
 150,
 TRUE),

('Água Mineral',
 'Água mineral com gás para consumo.',
 'agua',
 '500ml',
 3.00,
 120,
 TRUE),

('Água Mineral',
 'Água mineral sem gás em garrafa de um litro e meio.',
 'agua',
 '1.5L',
 4.00,
 100,
 TRUE),

('Água Mineral',
 'Água mineral com gás em garrafa de um litro e meio.',
 'agua',
 '1.5L',
 4.50,
 80,
 TRUE);
 