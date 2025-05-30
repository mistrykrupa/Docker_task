CREATE TABLE IF NOT EXISTS movie (
  movie_id INT AUTO_INCREMENT PRIMARY KEY,
  movie_name VARCHAR(255),
  genre VARCHAR(255),
  year VARCHAR(4)
);

-- INSERT INTO movie (movie_name, genre, year)
-- VALUES 
--   ('Interstellar', 'Sci-Fi', '2014'),
--   ('Joker', 'Drama', '2019');
