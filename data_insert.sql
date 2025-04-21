CREATE TABLE IF NOT EXISTS test_table (
    id serial PRIMARY KEY,
    num integer
);

DO $$
BEGIN
    FOR i IN 1..500000 LOOP
        INSERT INTO public.test_table (num) VALUES (FLOOR(RANDOM() * 5000) + 1); -- Генерируем случайное число от 1 до 5000
    END LOOP;
END $$;;