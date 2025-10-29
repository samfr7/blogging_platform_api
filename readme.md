# Blogging Platform API

A RESTful API built with Flask and MySQL for managing blog posts with categories and tags.

#### Project URL: https://roadmap.sh/projects/blogging-platform-api

## Features

- CRUD operations for blog posts
- Category management
- Tag management
- Database transaction handling
- Error handling and validation

## Technologies Used

- Python 3.x
- Flask
- MySQL
- python-dotenv

## Setup

1. Clone the repository
2. Create a virtual environment and activate it:
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```sh
pip install flask mysql-connector-python python-dotenv
```

4. Create a `.env` file with the following variables:
```
DB_HOST=your_host
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=blogging_platform
```

5. Initialize the database:
```sh
python create_db.py
mysql -u your_username -p blogging_platform < init.sql
```

## API Endpoints

### Posts

- `GET /posts` - Get all posts
- `POST /posts` - Create a new post
- `GET /posts/<id>` - Get a specific post
- `PUT /posts/<id>` - Update a specific post
- `DELETE /posts/<id>` - Delete a specific post

### Request Body Format (POST/PUT)

```json
{
    "title": "Post Title",
    "content": "Post Content",
    "category": "Technology",
    "tags": ["Coding", "Tech News"]
}
```

## Database Schema

- `categories` - Stores blog categories
- `tags` - Stores available tags
- `posts` - Stores blog posts
- `post_tags` - Junction table for post-tag relationships

## Running the Application

```sh
python app.py
```

The server will start on `http://localhost:5000`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.