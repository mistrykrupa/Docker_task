"""
Flask REST API for managing a movie database using MySQL.

Endpoints:
- GET /              : Health check route.
- GET /get           : Fetch all movies.
- POST /create       : Insert a new movie record.
- POST /search       : Search movies by genre or year.

Author: [Your Name]
"""

from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    "port": int(os.getenv("DB_PORT", 3306)),
    "host": os.getenv("DB_HOST", "db"),
    # 'host': os.getenv('DB_HOST', 'localhost'),  1
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "123"),
    "database": os.getenv("DB_NAME", "movies"),
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "helloooo!!"})


@app.route("/get", methods=["GET"])
def get_all():
    """
    Fetch all movie records from the database.

    Returns:
        JSON response with a success message and list of movies.
    """
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "Select * from movie"
    cursor.execute(
        query,
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"message": "Movies fetched successfully!"}, {"data": rows})


@app.route("/create", methods=["POST"])
def insert():
    data = request.get_json()
    movie_id = data.get("movie_id")
    movie_name = data.get("movie_name")
    genre = data.get("genre")
    year = data.get("year")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """INSERT INTO movie(movie_id, movie_name, genre, year)
            VALUES (%s, %s, %s, %s)"""
    values = (movie_id, movie_name, genre, year)
    cursor.execute(query, values)
    rows = cursor.fetchall()
    print(rows)
    result = conn.commit()
    print(result)
    cursor.close()
    conn.close()

    return jsonify({"message": "create movie successfully!!"}, {"data": rows})


@app.route("/search", methods=["POST"])
def search():
    """
    Search for movies by genre or year.

    Request JSON:
        {
            "word": str   # keyword to match genre or year
        }

    Returns:
        JSON response with matched movie records.
    """
    data = request.get_json()
    keyword = data.get("word", "")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """
        SELECT movie_id, movie_name, genre, year FROM movie
        WHERE genre LIKE %s OR year LIKE %s
    """
    values = (f"%{keyword}%", f"%{keyword}%")
    cursor.execute(query, values)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    result = [
        {
            "movie_id": row[0],
            "movie_name": row[1],
            "genre": row[2],
            "year": row[3]
        }
        for row in rows
    ]
    # print(result)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
