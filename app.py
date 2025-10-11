from flask import Flask, jsonify, request, Response
import create_db
from mysql.connector import connection, Error
import os
from dotenv import load_dotenv
from collections.abc import Iterable

app = Flask(__name__)
load_dotenv()

def get_conn():
    conn = connection.MySQLConnection(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME')
    )

    return conn

@app.route('/posts', methods=['GET', 'POST'])
def get_posts():
    res = {}
    res_code = 200    
    try:
        conn = get_conn()
        cursor = conn.cursor()

        if request.method == "GET":
            cursor.execute('SELECT * FROM posts')
            posts_description = cursor.description

            results = cursor.fetchall()
            res= []
            for post in results:
                r = dict(zip([event[0] for event in posts_description], post))
                # Getting the category name from the category id
                cursor.execute('SELECT category FROM categories WHERE category_id = %s', [r.get('category')])
                c = cursor.fetchone()
                r['category'] = str(c[0])

                # To add tags details
                cursor.execute('SELECT tag FROM tags WHERE tag_id IN (SELECT tag_id FROM post_tags WHERE post_id = %s)',(r.get('id'),))
                tags_db = cursor.fetchall()
                tags = []
                for tag in tags_db:
                    tags.append(tag[0])
                r['tags'] = tags     
                res.append(r)
        elif request.method == 'POST':
            '''
            Validation Paramters
            1. Check the number of keys whether they are are meeting the required count
            2. Check whether they are the ones we need
            3. Validate Category
                i) Check wheter the category is present in the DB
                ii) If so get the category_id
            4. Validate tags
                i) Validate wheter the tags is Iteratable
                ii) If so, get the id of each, if any one not found, raise error
            5. Insert into posts table
            6. Insert into posts_tags table
            7. Commit the changes
            '''

            # Start the transaction
            conn.start_transaction(isolation_level='REPEATABLE READ')
            data = request.json
            mandatory_keys = set(['title', 'content', 'category', 'tags'])

            # Checking for the count of the keys
            if len(data.keys()) != 4:
                raise Error("The required fields are not present. Please add title, content, category, tags ONLY!")
            
            # Checking all the keys one by one
            for key in data.keys():
                if key not in mandatory_keys:
                    raise Error("The required fields are not present. Please add title, content, category, tags ONLY!")
            
            # Validating Category and Tags
            # Validating Category

            cursor.execute('SELECT category_id FROM categories WHERE LOWER(category) = LOWER(%s)',[data.get('category')])
            category_id = cursor.fetchone()

            if not category_id:
                raise Error("Please select the existing Category only")
            
            category_id = category_id[0]

            # Validating Tags

            tags = data.get('tags')

            if not isinstance(tags, Iterable):
                raise Error("The Tags should be iterable")

            tag_ids = []

            for tag in tags:
                cursor.execute('SELECT tag_id FROM tags WHERE LOWER(tag) = LOWER(%s)', [tag])
                tag_id = cursor.fetchone()

                if not tag_id:
                    raise Error("The Tag is not present in the DB, Please select existing tags")
                
                tag_ids.append(tag_id[0])
            
            # Inserting the data

            cursor.execute('INSERT INTO posts (title, content, category, createdAt, updatedAt) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)',[data.get('title'), data.get('content'), category_id])

            # cursor.execute('select id from posts where id = last_insert_id()')

            post_id = cursor.lastrowid

            for tag_id in tag_ids:
                cursor.execute('INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s)', [post_id, tag_id])
            
            

            cursor.execute('SELECT * FROM posts where id = %s', [post_id])

            post = cursor.fetchone()
            if not post:
                raise Error("Post Not Found")        

            res = dict(zip([event[0] for event in cursor.description], post))

            # Getting the category name from the category id
            cursor.execute('SELECT category FROM categories WHERE category_id = %s', [res.get('category')])
            c = cursor.fetchone()
            res['category'] = str(c[0])

            # To add tags details
            cursor.execute('SELECT tag FROM tags WHERE tag_id IN (SELECT tag_id FROM post_tags WHERE post_id = %s)',(res.get('id'),))
            tags_db = cursor.fetchall()
            tags = []
            for tag in tags_db:
                tags.append(tag[0])
            res['tags'] = tags
            res_code = 201

            conn.commit()
    except Error as e:
        res = {
            'msg' : str(e)
        }
        res_code = 400
        conn.rollback()
    finally:    
        cursor.close()
        conn.close()

    return jsonify(res), res_code

@app.route('/posts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def post(id):
    if request.method == 'GET':
        try:
            conn = get_conn()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM posts WHERE id = %s', [id])
            post = cursor.fetchone()
            if not post:
                raise Error("Post Not Found")        

            res = dict(zip([event[0] for event in cursor.description], post))
            res_code = 200

            # Getting the category name from the category id
            cursor.execute('SELECT category FROM categories WHERE category_id = %s', [res.get('category')])
            c = cursor.fetchone()
            res['category'] = str(c[0])

            # To add tags details
            cursor.execute('SELECT tag FROM tags WHERE tag_id IN (SELECT tag_id FROM post_tags WHERE post_id = %s)',(res.get('id'),))
            tags_db = cursor.fetchall()
            tags = []
            for tag in tags_db:
                tags.append(tag[0])
            res['tags'] = tags 

        except Error as e:
            res = {
                'msg' : str(e)
            }
            res_code = 404
        finally:
            cursor.close()
            conn.close()
    elif request.method == 'PUT':
        res_code = 200
        res = {}
        try:
            conn = get_conn()
            cursor = conn.cursor(dictionary=True)
            conn.start_transaction(isolation_level='READ COMMITTED')

            '''
            Method to put a value:

            PUT: a method where we will replace the whole row.

            1. Check if the id for post is there
            2. If it exist the validate all the validations done on POST
            3. Update that id and return the POST
            '''

            cursor.execute('SELECT * FROM posts WHERE id = %s', [id])
            res = cursor.fetchone()

            if not res:
                res_code = 404
                raise Error(f"The post with id {id} not Found")

            data = request.json
            mandatory_keys = set(['title', 'content', 'category', 'tags'])

            # Checking for the count of the keys
            if len(data.keys()) != 4:
                raise Error("The required fields are not present. Please add title, content, category, tags ONLY!")
            
            # Checking all the keys one by one
            for key in data.keys():
                if key not in mandatory_keys:
                    raise Error("The required fields are not present. Please add title, content, category, tags ONLY!")
            
            # Validating Category and Tags
            # Validating Category

            cursor.execute('SELECT category_id FROM categories WHERE LOWER(category) = LOWER(%s)',[data.get('category')])
            category_id = cursor.fetchone()
            print(category_id)

            if not category_id:
                raise Error("Please select the existing Category only")
            
            category_id = category_id['category_id']

            # Validating Tags

            tags = data.get('tags')

            if not isinstance(tags, Iterable):
                raise Error("The Tags should be iterable")

            tag_ids = []

            for tag in tags:
                cursor.execute('SELECT tag_id FROM tags WHERE LOWER(tag) = LOWER(%s)', [tag])
                tag_id = cursor.fetchone()

                if not tag_id:
                    raise Error("The Tag is not present in the DB, Please select existing tags")
                
                tag_ids.append(tag_id['tag_id'])

            cursor.execute('DELETE FROM post_tags WHERE post_id = %s', [id])
            cursor.execute('UPDATE posts SET title = %s, content = %s, category = %s, updatedAt = CURRENT_TIMESTAMP WHERE id = %s',[data.get('title'), data.get('content'), category_id, id])

            for tag_id in tag_ids:
                cursor.execute('INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s)', [id, tag_id])
            
            # After Modification, fetching the row
            cursor.execute('SELECT * FROM posts where id = %s', [id])

            res = cursor.fetchone()
            # if not post:
            #     raise Error("Post Not Found")        

            # res = dict(zip([event[0] for event in cursor.description], post))

            # Getting the category name from the category id
            cursor.execute('SELECT category FROM categories WHERE category_id = %s', [res.get('category')])
            c = cursor.fetchone()
            res['category'] = str(c['category'])

            # To add tags details
            cursor.execute('SELECT tag FROM tags WHERE tag_id IN (SELECT tag_id FROM post_tags WHERE post_id = %s)',(res.get('id'),))
            tags_db = cursor.fetchall()
            tags = []
            for tag in tags_db:
                tags.append(tag['tag'])
            res['tags'] = tags
            res_code = 200

            conn.commit()

        except Error as e:
            res = {
                'msg': str(e)
            }
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    elif request.method == 'DELETE':
        try:
            conn = get_conn()
            cursor = conn.cursor(dictionary=True)
            conn.start_transaction(isolation_level='READ COMMITTED')
            res_code = 204

            cursor.execute('SELECT * FROM posts WHERE id = %s', [id])
            post = cursor.fetchone()
            if not post:
                res_code = 404
                raise Error("Post Not Found")        

            cursor.execute('DELETE FROM posts WHERE id = %s', [id])

            conn.commit()

            return Response(status=res_code)

        except Error as e:
            res = {
                'msg' : str(e)
            }
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    return jsonify(res), res_code



if __name__ == "__main__":
    app.run(debug=True)