from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟数据库
users = {}

# 创建新用户（POST）
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = len(users) + 1
    users[user_id] = {
        "id": user_id,
        "name": data.get('name'),
        "email": data.get('email')
    }
    return jsonify(users[user_id]), 201

# 获取用户信息（GET）
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

# 更新整个用户信息（PUT）
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    users[user_id] = {
        "id": user_id,
        "name": data.get('name'),
        "email": data.get('email')
    }
    return jsonify(users[user_id]), 200

# 部分更新用户信息（PATCH）
@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    users[user_id].update(data)
    return jsonify(users[user_id]), 200

# 删除用户（DELETE）
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return '', 204
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)