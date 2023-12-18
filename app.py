# from flask import Flask, request, jsonify
# from datetime import datetime
# import secrets
# from secrets import randbelow

# app = Flask(__name__)

# # Placeholder for storing posts and users (you should implement persistence for production)
# posts = {}
# users = {}
# moderators = {}  # Placeholder for storing moderator keys

# @app.route('/random/<int:sides>', methods=['GET'])
# def roll(sides):
#     if sides <= 0:
#         return {'err': 'need a positive number of sides'}, 400

#     return {'num': randbelow(sides) + 1}

# @app.route('/user', methods=['POST'])
# def create_user():
#     try:
#         data = request.get_json()
#         if 'username' not in data or not isinstance(data['username'], str):
#             return jsonify({'err': 'Invalid username'}), 400

#         # Ensure the username is unique
#         username = data['username']
#         for user_id, user in users.items():
#             if user['username'] == username:
#                 return jsonify({'err': 'Username already exists'}), 400

#         user_id = len(users) + 1
#         user_key = secrets.token_urlsafe(16)

#         users[user_id] = {
#             'id': user_id,
#             'username': username,
#             'key': user_key,
#             'real_name': data.get('real_name', ''),
#             'avatar_icon': data.get('avatar_icon', ''),
#         }

#         return jsonify({
#             'id': user_id,
#             'username': username,
#             'key': user_key,
#             'real_name': data.get('real_name', ''),
#             'avatar_icon': data.get('avatar_icon', ''),
#         }), 201

#     except Exception as e:
#         return jsonify({'err': str(e)}), 500

# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_user_metadata(user_id):
#     if user_id not in users:
#         return jsonify({'err': 'User not found'}), 404

#     user = users[user_id]
#     return jsonify({
#         'id': user_id,
#         'username': user['username'],
#         'real_name': user['real_name'],
#         'avatar_icon': user['avatar_icon'],
#     })

# @app.route('/user/<int:user_id>/edit', methods=['PUT'])
# def edit_user_metadata(user_id):
#     try:
#         data = request.get_json()
#         if 'user_key' not in data:
#             return jsonify({'err': 'User key is required to edit user metadata'}), 400

#         user_key = data['user_key']

#         if user_id not in users or users[user_id]['key'] != user_key:
#             return jsonify({'err': 'Invalid user credentials'}), 403

#         user = users[user_id]
#         if 'real_name' in data:
#             user['real_name'] = data['real_name']
#         if 'avatar_icon' in data:
#             user['avatar_icon'] = data['avatar_icon']

#         return jsonify({
#             'id': user_id,
#             'username': user['username'],
#             'real_name': user['real_name'],
#             'avatar_icon': user['avatar_icon'],
#         })

#     except Exception as e:
#         return jsonify({'err': str(e)}), 500

# @app.route('/post', methods=['POST'])
# def create_post():
#     try:
#         data = request.get_json()
#         if 'msg' not in data or not isinstance(data['msg'], str) or 'user_id' not in data or 'user_key' not in data:
#             return jsonify({'err': 'Invalid message or user credentials'}), 400

#         user_id = data['user_id']
#         user_key = data['user_key']

#         if user_id not in users or users[user_id]['key'] != user_key:
#             return jsonify({'err': 'Invalid user credentials'}), 403

#         post_id = len(posts) + 1
#         key = secrets.token_urlsafe(16)
#         timestamp = datetime.utcnow().isoformat()

#         # Check if the post is a reply to another post
#         reply_to = data.get('reply_to', None)
#         if reply_to and reply_to in posts:
#             posts[reply_to].setdefault('replies', []).append(post_id)

#         posts[post_id] = {
#             'id': post_id,
#             'msg': data['msg'],
#             'key': key,
#             'timestamp': timestamp,
#             'user_id': user_id,
#             'reply_to': reply_to,
#         }

#         return jsonify({
#             'id': post_id,
#             'key': key,
#             'timestamp': timestamp,
#             'user_id': user_id,
#             'reply_to': reply_to,
#         }), 201

#     except Exception as e:
#         return jsonify({'err': str(e)}), 500

# @app.route('/post/<int:post_id>', methods=['GET'])
# def read_post(post_id):
#     if post_id not in posts:
#         return jsonify({'err': 'Post not found'}), 404

#     post = posts[post_id]
#     return jsonify(post)

# @app.route('/post/<int:post_id>/delete', methods=['DELETE'])
# def delete_post(post_id):
#     try:
#         data = request.get_json()
#         if 'user_id' not in data or ('user_key' not in data and 'moderator_key' not in data):
#             return jsonify({'err': 'Invalid user credentials'}), 400

#         user_id = data['user_id']

#         # Check if the user is a moderator
#         if 'moderator_key' in data and data['moderator_key'] in moderators:
#             # Moderators can delete any post
#             del posts[post_id]
#             return jsonify({'message': 'Post deleted by moderator'})

#         # Regular users can only delete their own posts
#         if post_id not in posts:
#             return jsonify({'err': 'Post not found'}), 404

#         post = posts[post_id]
#         if post['user_id'] != user_id:
#             return jsonify({'err': 'Unauthorized'}), 403

#         # Handle replies by recursively deleting them
#         def recursive_delete(post_id):
#             post = posts[post_id]
#             if 'replies' in post:
#                 for reply_id in post['replies']:
#                     recursive_delete(reply_id)
#             del posts[post_id]

#         recursive_delete(post_id)

#         return jsonify({'message': 'Post deleted by user'})

#     except Exception as e:
#         return jsonify({'err': str(e)}), 500

# @app.route('/posts/user/<int:user_id>', methods=['GET'])
# def get_posts_by_user(user_id):
#     if user_id not in users:
#         return jsonify({'err': 'User not found'}), 404

#     user_posts = [post for post_id, post in posts.items() if post['user_id'] == user_id]

#     return jsonify(user_posts)

# @app.route('/moderator/key', methods=['POST'])
# def create_moderator_key():
#     try:
#         data = request.get_json()
#         if 'admin_key' not in data or data['admin_key'] != 'your_admin_key':
#             return jsonify({'err': 'Invalid admin key'}), 403

#         moderator_key = secrets.token_urlsafe(16)
#         moderators[moderator_key] = True

#         return jsonify({'moderator_key': moderator_key})

#     except Exception as e:
#         return jsonify({'err': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)













# from flask import Flask, request, jsonify
# import secrets
# from datetime import datetime
# import os
# from whoosh.index import create_in, open_dir
# from whoosh.fields import Schema, TEXT, ID
# from whoosh.qparser import QueryParser

# app = Flask(__name__)

# # In-memory storage for posts
# posts = []


# index_dir = "post_index"
# if not os.path.exists(index_dir):
#     os.mkdir(index_dir)

# schema = Schema(id=ID(stored=True), msg=TEXT(stored=True))
# ix = create_in(index_dir, schema=schema)



# def generate_key():
#     return secrets.token_urlsafe(32)


# users = []


# @app.route('/createuser', methods=['POST'])
# def create_user():
#     try:
#         data = request.get_json()

#         # Check if the request is a JSON object and contains the 'username' field
#         if not isinstance(data, dict) or 'username' not in data or not isinstance(data['username'], str):
#             return jsonify({"error": "Bad request"}), 400

#         user_id = len(users) + 1
#         key = generate_key()
#         timestamp = datetime.utcnow().isoformat()

#         # By default, users have the 'user' role
#         role = 'user'

#         user = {
#             "id": user_id,
#             "key": key,
#             "timestamp": timestamp,
#             "username": data['username'],
#             "role": role  # Assign 'user' role by default
#         }

#         users.append(user)

#         return jsonify(user), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/createmoderator', methods=['POST'])
# def create_moderator():
#     try:
#         data = request.get_json()

#         # Check if the request is a JSON object and contains the 'username' field
#         if not isinstance(data, dict) or 'username' not in data or not isinstance(data['username'], str):
#             return jsonify({"error": "Bad request"}), 400

#         user_id = len(users) + 1
#         key = generate_key()
#         timestamp = datetime.utcnow().isoformat()

#         # Create a new moderator user with the 'moderator' role
#         role = 'moderator'

#         user = {
#             "id": user_id,
#             "key": key,
#             "timestamp": timestamp,
#             "username": data['username'],
#             "role": role  # Assign 'moderator' role
#         }

#         users.append(user)

#         return jsonify(user), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/post', methods=['POST'])
# def create_post():
#     try:
#         data = request.get_json()

#         # Check if the request is a JSON object and contains the 'msg' field
#         if not isinstance(data, dict) or 'msg' not in data or not isinstance(data['msg'], str):
#             return jsonify({"error": "Bad request"}), 400

#         post_id = len(posts) + 1
#         key = generate_key()
#         timestamp = datetime.utcnow().isoformat()

#         post = {
#             "id": post_id,
#             "key": key,
#             "timestamp": timestamp,
#             "msg": data['msg']
#         }

#         posts.append(post)

#         return jsonify(post), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/post/<int:post_id>', methods=['GET'])
# def read_post(post_id):
#     post = next((p for p in posts if p['id'] == post_id), None)

#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     # Exclude the 'key' field from the response
#     response = {key: value for key, value in post.items() if key != 'key'}

#     return jsonify(response)


# @app.route('/post/<int:post_id>/delete/<string:key>', methods=['DELETE'])
# def delete_post(post_id, key):
#     post = next((p for p in posts if p['id'] == post_id), None)

#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     if post['key'] != key:
#         return jsonify({"error": "Forbidden"}), 403

#     posts.remove(post)

#     # Exclude the 'key' field from the response
#     response = {k: v for k, v in post.items() if k != 'key'}

#     return jsonify(response)


# @app.route('/createpost', methods=['POST'])
# def create_post_with_user():
#     try:
#         data = request.get_json()

#         # Check if the request is a JSON object and contains the required fields
#         if not isinstance(data, dict) or 'msg' not in data or not isinstance(data['msg'], str) \
#                 or 'user_id' not in data or 'user_key' not in data:
#             return jsonify({"error": "Bad request"}), 400

#         user_id = data['user_id']
#         user_key = data['user_key']

#         # Verify if the user exists
#         user = next((u for u in users if u['id'] == user_id), None)

#         if not user or user['key'] != user_key:
#             return jsonify({"error": "User not found or unauthorized"}), 401

#         post_id = len(posts) + 1
#         post_key = generate_key()
#         timestamp = datetime.utcnow().isoformat()

#         post = {
#             "id": post_id,
#             "key": post_key,
#             "timestamp": timestamp,
#             "msg": data['msg'],
#             "user_id": user_id  # Include user_id in the post data
#         }

#         posts.append(post)

#         return jsonify(post), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/readpost/<int:post_id>', methods=['GET'])
# def read_post_with_user(post_id):
#     post = next((p for p in posts if p['id'] == post_id), None)

#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     # Include user_id in the response
#     # Exclude 'key' from the response
#     response = {key: value for key, value in post.items() if key != 'key'}

#     # If the post has an associated user, include user_id in the response
#     if 'user_id' in post:
#         response['user_id'] = post['user_id']

#     return jsonify(response)


# @app.route('/deletepost/<int:post_id>', methods=['DELETE'])
# def delete_post_with_user(post_id):
#     try:
#         data = request.get_json()

#         # Check if the request is a JSON object and contains the required fields
#         if not isinstance(data, dict) or 'key' not in data or 'user_id' not in data:
#             return jsonify({"error": "Bad request"}), 400

#         user_id = data['user_id']
#         key = data['key']

#         post = next((p for p in posts if p['id'] == post_id), None)

#         if not post:
#             return jsonify({"error": "Post not found"}), 404

#         # Check if the user is authorized to delete the post
#         if (post['user_id'] == user_id and post['key'] == key) or (user_id in [user['id'] for user in users if user['role'] == 'moderator'] and key == moderator_key):
#             posts.remove(post)

#             # Exclude the 'key' field from the response
#             response = {k: v for k, v in post.items() if k != 'key'}

#             # If the post has an associated user, include user_id in the response
#             if 'user_id' in post:
#                 response['user_id'] = post['user_id']

#             return jsonify(response)

#         return jsonify({"error": "Unauthorized"}), 401

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/searchposts', methods=['GET'])
# def search_posts():
#     try:
#         start_time_str = request.args.get('start_time')
#         end_time_str = request.args.get('end_time')

#         if not start_time_str and not end_time_str:
#             return jsonify({"error": "At least one of 'start_time' or 'end_time' must be provided"}), 400

#         # Update the format string to include fractional seconds
#         datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

#         start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S.%f")
#         end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S.%f") if end_time_str else datetime.max


#         # Filter posts within the specified date/time range
#         filtered_posts = [post for post in posts if start_time <= post['timestamp'] <= end_time]

#         if not filtered_posts:
#             return jsonify({"error": "No posts found in the specified date/time range"}), 404

#         # Exclude the 'key' field from each post in the response
#         response = [
#             {key: value for key, value in post.items() if key != 'key'}
#             for post in filtered_posts
#         ]

#         # If the posts have associated users, include user_id in the response
#         for post in response:
#             if 'user_id' in post:
#                 post['user_id'] = post['user_id']

#         return jsonify(response), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



# @app.route('/searchpostsbyuser/<int:user_id>', methods=['GET'])
# def search_posts_by_user(user_id):
#     try:
#         user = next((u for u in users if u['id'] == user_id), None)

#         if not user:
#             return jsonify({"error": "User not found"}), 404

#         user_posts = [post for post in posts if 'user_id' in post and post['user_id'] == user_id]

#         if not user_posts:
#             return jsonify({"error": "No posts found for the specified user"}), 404

#         # Exclude the 'key' field from each post in the response
#         response = [
#             {key: value for key, value in post.items() if key != 'key'}
#             for post in user_posts
#         ]

#         return jsonify(response), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/fulltextsearch', methods=['GET'])
# def fulltext_search():
#     try:
#         query = request.args.get('q')

#         if not query:
#             return jsonify({"error": "Search query ('q' parameter) must be provided"}), 400

#         # Open the Whoosh index
#         ix = open_dir(index_dir)

#         # Create a QueryParser to parse the user's query
#         with ix.searcher() as searcher:
#             query_parser = QueryParser("msg", schema=ix.schema)
#             parsed_query = query_parser.parse(query)

#             # Perform the search
#             results = searcher.search(parsed_query)

#             # Extract the matching posts
#             matching_posts = []
#             for result in results:
#                 post = next((p for p in posts if p['id'] == int(result['id'])), None)
#                 if post:
#                     # Exclude the 'key' field from the response
#                     response = {key: value for key, value in post.items() if key != 'key'}
#                     matching_posts.append(response)

#             if not matching_posts:
#                 return jsonify({"error": "No matching posts found"}), 404

#             return jsonify(matching_posts), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, request, jsonify
import secrets
from datetime import datetime
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

app = Flask(__name__)

# In-memory storage for posts and replies
posts = []


index_dir = "post_index"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

schema = Schema(id=ID(stored=True), msg=TEXT(stored=True), parent_id=ID(stored=True))
ix = create_in(index_dir, schema=schema)


def generate_key():
    return secrets.token_urlsafe(32)


users = []


@app.route('/createuser', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        # Check if the request is a JSON object and contains the 'username' field
        if not isinstance(data, dict) or 'username' not in data or not isinstance(data['username'], str):
            return jsonify({"error": "Bad request"}), 400

        user_id = len(users) + 1
        key = generate_key()
        timestamp = datetime.utcnow().isoformat()

        # By default, users have the 'user' role
        role = 'user'

        user = {
            "id": user_id,
            "key": key,
            "timestamp": timestamp,
            "username": data['username'],
            "role": role  # Assign 'user' role by default
        }

        users.append(user)

        return jsonify(user), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/createmoderator', methods=['POST'])
def create_moderator():
    try:
        data = request.get_json()

        # Check if the request is a JSON object and contains the 'username' field
        if not isinstance(data, dict) or 'username' not in data or not isinstance(data['username'], str):
            return jsonify({"error": "Bad request"}), 400

        user_id = len(users) + 1
        key = generate_key()
        timestamp = datetime.utcnow().isoformat()

        # Create a new moderator user with the 'moderator' role
        role = 'moderator'

        user = {
            "id": user_id,
            "key": key,
            "timestamp": timestamp,
            "username": data['username'],
            "role": role  # Assign 'moderator' role
        }

        users.append(user)

        return jsonify(user), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/post', methods=['POST'])
def create_post():
    try:
        data = request.get_json()

        # Check if the request is a JSON object and contains the 'msg' field
        if not isinstance(data, dict) or 'msg' not in data or not isinstance(data['msg'], str):
            return jsonify({"error": "Bad request"}), 400

        post_id = len(posts) + 1
        key = generate_key()
        timestamp = datetime.utcnow().isoformat()

        # Check if the post is a reply
        parent_id = data.get('parent_id')

        post = {
            "id": post_id,
            "key": key,
            "timestamp": timestamp,
            "msg": data['msg']
        }

        # If it's a reply, include parent_id in the post data
        if parent_id:
            post['parent_id'] = parent_id

        posts.append(post)

        return jsonify(post), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)

    if not post:
        return jsonify({"error": "Post not found"}), 404

    # Exclude the 'key' field from the response
    response = {key: value for key, value in post.items() if key != 'key'}

    return jsonify(response)


@app.route('/post/<int:post_id>/delete/<string:key>', methods=['DELETE'])
def delete_post(post_id, key):
    post = next((p for p in posts if p['id'] == post_id), None)

    if not post:
        return jsonify({"error": "Post not found"}), 404

    if post['key'] != key:
        return jsonify({"error": "Forbidden"}), 403

    posts.remove(post)

    # Exclude the 'key' field from the response
    response = {k: v for k, v in post.items() if k != 'key'}

    return jsonify(response)


@app.route('/createpost', methods=['POST'])
def create_post_with_user():
    try:
        data = request.get_json()

        # Check if the request is a JSON object and contains the required fields
        if not isinstance(data, dict) or 'msg' not in data or not isinstance(data['msg'], str) \
                or 'user_id' not in data or 'user_key' not in data:
            return jsonify({"error": "Bad request"}), 400

        user_id = data['user_id']
        user_key = data['user_key']

        # Verify if the user exists
        user = next((u for u in users if u['id'] == user_id), None)

        if not user or user['key'] != user_key:
            return jsonify({"error": "User not found or unauthorized"}), 401

        post_id = len(posts) + 1
        post_key = generate_key()
        timestamp = datetime.utcnow().isoformat()

        # Check if the post is a reply
        parent_id = data.get('parent_id')

        post = {
            "id": post_id,
            "key": post_key,
            "timestamp": timestamp,
            "msg": data['msg'],
            "user_id": user_id  # Include user_id in the post data
        }

        # If it's a reply, include parent_id in the post data
        if parent_id:
            post['parent_id'] = parent_id

        posts.append(post)

        return jsonify(post), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/readpost/<int:post_id>', methods=['GET'])
def read_post_with_user(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)

    if not post:
        return jsonify({"error": "Post not found"}), 404

    # Include user_id in the response
    # Exclude 'key' from the response
    response = {key: value for key, value in post.items() if key != 'key'}

    # If the post has an associated user, include user_id in the response
    if 'user_id' in post:
        response['user_id'] = post['user_id']

    return jsonify(response)


@app.route('/deletepost/<int:post_id>', methods=['DELETE'])
def delete_post_with_user(post_id):
    try:
        data = request.get_json()

        # Check if the request is a JSON object and contains the required fields
        if not isinstance(data, dict) or 'key' not in data or 'user_id' not in data:
            return jsonify({"error": "Bad request"}), 400

        user_id = data['user_id']
        key = data['key']

        post = next((p for p in posts if p['id'] == post_id), None)

        if not post:
            return jsonify({"error": "Post not found"}), 404

        # Check if the user is authorized to delete the post
        if (post['user_id'] == user_id and post['key'] == key) or (
                user_id in [user['id'] for user in users if user['role'] == 'moderator'] and key == moderator_key):
            posts.remove(post)

            # Exclude the 'key' field from the response
            response = {k: v for k, v in post.items() if k != 'key'}

            # If the post has an associated user, include user_id in the response
            if 'user_id' in post:
                response['user_id'] = post['user_id']

            return jsonify(response)

        return jsonify({"error": "Unauthorized"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/searchposts', methods=['GET'])
def search_posts():
    try:
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')

        if not start_time_str and not end_time_str:
            return jsonify({"error": "At least one of 'start_time' or 'end_time' must be provided"}), 400

        # Update the format string to include fractional seconds
        datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

        start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S.%f")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S.%f") if end_time_str else datetime.max

        # Filter posts within the specified date/time range
        filtered_posts = [post for post in posts if start_time <= post['timestamp'] <= end_time]

        if not filtered_posts:
            return jsonify({"error": "No posts found in the specified date/time range"}), 404

        # Exclude the 'key' field from each post in the response
        response = [
            {key: value for key, value in post.items() if key != 'key'}
            for post in filtered_posts
        ]

        # If the posts have associated users, include user_id in the response
        for post in response:
            if 'user_id' in post:
                post['user_id'] = post['user_id']

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/searchpostsbyuser/<int:user_id>', methods=['GET'])
def search_posts_by_user(user_id):
    try:
        user = next((u for u in users if u['id'] == user_id), None)

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_posts = [post for post in posts if 'user_id' in post and post['user_id'] == user_id]

        if not user_posts:
            return jsonify({"error": "No posts found for the specified user"}), 404

        # Exclude the 'key' field from each post in the response
        response = [
            {key: value for key, value in post.items() if key != 'key'}
            for post in user_posts
        ]

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/fulltextsearch', methods=['GET'])
def fulltext_search():
    try:
        query = request.args.get('q')

        if not query:
            return jsonify({"error": "Search query ('q' parameter) must be provided"}), 400

        # Open the Whoosh index
        ix = open_dir(index_dir)

        # Create a QueryParser to parse the user's query
        with ix.searcher() as searcher:
            query_parser = QueryParser("msg", schema=ix.schema)
            parsed_query = query_parser.parse(query)

            # Perform the search
            results = searcher.search(parsed_query)

            # Extract the matching posts
            matching_posts = []
            for result in results:
                post = next((p for p in posts if p['id'] == int(result['id'])), None)
                if post:
                    # Exclude the 'key' field from the response
                    response = {key: value for key, value in post.items() if key != 'key'}
                    matching_posts.append(response)

            if not matching_posts:
                return jsonify({"error": "No matching posts found"}), 404

            return jsonify(matching_posts), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/thread/<int:post_id>', methods=['GET'])
def get_thread(post_id):
    try:
        # Find the post that corresponds to the requested post_id
        post = next((p for p in posts if p['id'] == post_id), None)

        if not post:
            return jsonify({"error": "Post not found"}), 404

        # Initialize the list of posts in the thread with the current post
        thread_posts = [post]

        # Find all posts that are replies to the current post (upwards in the thread)
        parent_id = post.get('parent_id')
        while parent_id is not None:
            parent_post = next((p for p in posts if p['id'] == parent_id), None)
            if parent_post:
                thread_posts.insert(0, parent_post)  # Insert at the beginning to maintain order
                parent_id = parent_post.get('parent_id')
            else:
                break

        # Find all posts that have the current post as their parent (downwards in the thread)
        post_id_to_find = post['id']
        child_posts = [p for p in posts if p.get('parent_id') == post_id_to_find]
        thread_posts.extend(child_posts)

        # Exclude the 'key' field from each post in the response
        response = [
            {key: value for key, value in post.items() if key != 'key'}
            for post in thread_posts
        ]

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)













