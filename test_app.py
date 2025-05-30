import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "helloooo!!"}


@patch('app.mysql.connector.connect')
def test_get_all(mock_connect, client):
    # Mock DB connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, 'Inception', 'Sci-Fi', 2010)]
    
    response = client.get('/get')
    assert response.status_code == 200
    assert 'Movies fetched successfully!' in response.json['message']
    assert response.json[1]['data'] == [(1, 'Inception', 'Sci-Fi', 2010)]
    
    mock_cursor.execute.assert_called_once_with("Select * from movie")
    mock_cursor.close.assert_called()
    mock_conn.close.assert_called()


@patch('app.mysql.connector.connect')
def test_insert(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    data = {
        "movie_id": 2,
        "movie_name": "Interstellar",
        "genre": "Sci-Fi",
        "year": 2014
    }
    response = client.post('/create', json=data)
    assert response.status_code == 200
    assert 'create movie successfully!!' in response.json['message']

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called()
    mock_conn.close.assert_called()


@patch('app.mysql.connector.connect')
def test_search(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, 'Inception', 'Sci-Fi', 2010)]
    
    data = {"word": "Sci-Fi"}
    response = client.post('/search', json=data)
    
    assert response.status_code == 200
    assert response.json == [{
        "movie_id": 1,
        "movie_name": "Inception",
        "genre": "Sci-Fi",
        "year": 2010
    }]

    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called()
    mock_conn.close.assert_called()
