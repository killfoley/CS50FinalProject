-- Add default admin user
INSERT INTO users (username, hash)
VALUES ('admin', 'pbkdf2:sha256:1000000$Xglu7noF9imK9VgX$fe663fa4372d17b98171c5318738892311d8d7411a9ac2fa14a75028d8e4aab8');

-- Add seed stock
INSERT INTO products (name, category, quantity, price, added_by)
VALUES
    ('Hammer', 'Tools', 10, 14.99, 1),
    ('Screwdriver', 'Tools', 25, 6.49, 1),
    ('Drill', 'Tools', 5, 79.99, 1),
    ('Paint Brush', 'Paint', 20, 4.99, 1),
    ('Measuring Tape', 'Tools', 15, 7.99, 1),
    ('Sandpaper Pack', 'Paint', 12, 3.49, 1);
