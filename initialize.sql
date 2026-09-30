CREATE TABLE user(
	user_id INT PRIMARY KEY,
	user_name VARCHAR(30),
	user_address VARCHAR(100),
	user_postal_code INT
	);


CREATE TABLE post(
	post_id INT PRIMARY KEY,
	user_id INT,
	post_cont TEXT
	);

INSERT INTO user
VALUES 
	(89, 'WhiteCloverMarkets', '305 - 14th Ave. S. Suite 3B', 98128),
	(90, 'Wilman Kala', 'Keskuskatu 45', 21240),
	(91, 'Wolski', 'ul. Filtrowa 68', 01012);

INSERT INTO post
VALUES
	(201, 89, 'Ni hao, shijie!'),
	(202, 90, 'Hello, world!'),
	(203, 91, 'Konnichiwa, sekai!'),
	(204, 89, 'Annyeonghaseyo, segye!'),
	(205, 90, 'Bonjour, le monde !'),
	(206, 91, 'Hola, mundo!'),
	(207, 89, 'Hallo, Welt!');

