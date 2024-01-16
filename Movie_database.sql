CREATE TABLE IF NOT EXISTS Movie(
    title TEXT PRIMARY KEY,
    genre TEXT, 
    avg_rating FLOAT, 
    Movie_Synopsis TEXT
    );

CREATE TABLE IF NOT EXISTS User(
    username CHAR(80) PRIMARY KEY, 
    password CHAR(80) NOT NULL
    );

CREATE TABLE IF NOT EXISTS rate_review(
    user TEXT NOT NULL,
    title TEXT NOT NULL,
    review CHAR(80), 
    rating FLOAT NOT NULL,
    FOREIGN KEY(title) REFERENCES Movie(title),
    FOREIGN KEY(user) REFERENCES User(username),
    PRIMARY KEY (user, title)
    );

CREATE TABLE IF NOT EXISTS People(
   name TEXT NOT NULL,
   title TEXT NOT NULL,
   profession TEXT NOT NULL CHECK (profession='Actor' OR profession='Director' OR profession='Producer'),
   PRIMARY KEY(name, title, profession),
   FOREIGN KEY(title) REFERENCES Movie(title)
   );

INSERT OR IGNORE INTO User (username, password) VALUES
('Jack', '2002'),
('John', '2001'),
('Eli', '2003');

INSERT OR IGNORE INTO Movie (title, genre, Movie_Synopsis) VALUES
('Oppenheimer', 'thriller', 'During World War II, Lt. Gen. Leslie Groves Jr. appoints physicist J. Robert Oppenheimer to work on the top-secret Manhattan Project. Oppenheimer and a team of scientists spend years developing and designing the atomic bomb. Their work comes to fruition on July 16, 1945, as they witness the world''s first nuclear explosion, forever changing the course of history.'),
('Inception', 'action', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project and his team to disaster.'),
('Titanic', 'romance','James Cameron''s "Titanic" is an epic, action-packed romance set against the ill-fated maiden voyage of the R.M.S. Titanic; the pride and joy of the White Star Line and, at the time, the largest moving object ever built. She was the most luxurious liner of her era -- the "ship of dreams" -- which ultimately carried over 1,500 people to their death in the ice cold waters of the North Atlantic in the early hours of April 15, 1912.'),
('The Godfather', 'crime','Widely regarded as one of the greatest films of all time, this mob drama, based on Mario Puzo''s novel of the same name, focuses on the powerful Italian-American crime family of Don Vito Corleone. When the don''s youngest son, Michael, reluctantly joins the Mafia, he becomes involved in the inevitable cycle of violence and betrayal. Although Michael tries to maintain a normal relationship with his wife, Kay (Diane Keaton), he is drawn deeper into the family business.');


INSERT OR IGNORE INTO rate_review (user, title, review, rating) VALUES
('Jack', 'Oppenheimer','A thought-provoking documentary that delves into the complex persona of J. Robert Oppenheimer, the father of the atomic bomb. The film masterfully combines historical footage and interviews, offering a nuanced exploration of the moral dilemmas faced by scientists during wartime.', '4.5'),
('John', 'Oppenheimer', 'Oppenheimer is a riveting journey through the life of a brilliant yet conflicted scientist. The filmmaker''s use of archival material and interviews paints a vivid picture of the man behind the bomb. The documentary raises profound questions about the consequences of scientific innovation.','5'),
('Eli', 'Oppenheimer','A compelling and insightful documentary that skillfully navigates the moral complexities surrounding Oppenheimer''s contributions to the atomic bomb. The film''s narrative structure keeps the audience engaged, while its depth invites contemplation on the ethical responsibilities of scientific advancements.','4.7'),


('Jack', 'Inception','Inception is a mind-bending masterpiece that seamlessly blends stunning visuals with a complex, multi-layered narrative. Christopher Nolan''s direction and the exceptional cast deliver a cinematic experience that challenges the audience''s perception of reality. ','4.3'),
('John', 'Inception','Visually breathtaking and intellectually stimulating film, Inception takes the viewer on a rollercoaster of dreams within dreams. Nolan''s visionary storytelling, paired with an outstanding ensemble cast, creates a cinematic gem that lingers in the mind long after the credits roll.','4.6'),
('Eli', 'Inception','Inception is a cinematic puzzle that demands attention and rewards it with a mesmerizing experience. The film''s intricate plot, coupled with Hans Zimmer''s unforgettable score, makes for a truly immersive journey into the realm of dreams.','4.7'),


('Jack', 'Titanic','Titanic remains an epic romance that stands the test of time. James Cameron''s direction, combined with the enchanting performances of Leonardo DiCaprio and Kate Winslet, creates a timeless love story set against the backdrop of a tragic historical event.','4'),
('John', 'Titanic','A cinematic spectacle that captures the grandeur of the ill-fated voyage, Titanic is a poignant love story that resonates across generations. Cameron''s meticulous attention to detail and the chemistry between the lead actors elevate this film to iconic status.','4.5'),
('Eli', 'Titanic','Titanic is a cinematic triumph, seamlessly blending romance, drama, and tragedy. The film''s scale, coupled with the authentic performances, transports the audience to the heart of the disaster. A classic that continues to tug at the heartstrings.','3.25'),

('Jack', 'The Godfather','The Godfather is a cinematic masterpiece that redefined the crime genre. Marlon Brando''s iconic performance, coupled with Francis Ford Coppola''s impeccable direction, crafts an immersive and unforgettable tale of power, family, and betrayal','5'),
('John', 'The Godfather','A timeless classic, The Godfather is a tour de force in storytelling and character development. The film''s exploration of power dynamics within a mafia family is both gripping and thought-provoking. A must-watch for any film enthusiast.','4.8'),
('Eli', 'The Godfather','The Godfather is a cinematic gem that stands as a testament to the art of storytelling. Brando''s portrayal of Don Vito Corleone and the film''s rich narrative make it a compelling exploration of power, loyalty, and the consequences of a life in organized crime.','4.9');

UPDATE Movie SET avg_rating = (SELECT AVG(rating) FROM rate_review WHERE title = Movie.title);

INSERT OR IGNORE INTO People (name, title, profession) VALUES
('Leonardo Dicaprio', 'Inception', 'Actor'),
('Leonardo Dicaprio', 'Titanic', 'Actor'),
('Kate Winslet', 'Titanic', 'Actor'),
('Tom Hardy', 'Inception', 'Actor'),
('Marlon Brando', 'The Godfather', 'Actor'),
('Al Pacino', 'The Godfather', 'Actor'),
('Cillian Murphy', 'Oppenheimer', 'Actor'),
('Emily Blunt', 'Oppenheimer', 'Actor'),


('James Cameron', 'Titanic', 'Director'),
('Christopher Nolan', 'Inception', 'Director'),
('Christopher Nolan', 'Oppenheimer', 'Director'),
('Francis Ford Coppola', 'The Godfather', 'Director'),

('Albert S. Rudy', 'The Godfather', 'Producer'),
('Albert S. Rudy', 'The Godfather', 'Producer'),

('Emma Thomas', 'Oppenheimer', 'Producer'),
('Charles Roven', 'Oppenheimer', 'Producer'),


('Emma Thomas', 'Inception ', 'Producer'),
('Christopher Nolan', 'Inception', 'Producer'),

('James Cameron', 'Titanic ', 'Producer'),
('Jon Landau', 'Titanic', 'Producer');


