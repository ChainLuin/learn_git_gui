import requests

BASE_URL = 'http://127.0.0.1:5000'

# 1. 创建用户（POST）
def create_user(name, email):
    response = requests.post(f'{BASE_URL}/users', json={
        'name': name,
        'email': email
    })
    print('Create:', response.status_code, response.json())

# 2. 获取用户信息（GET）
def get_user(user_id):
    response = requests.get(f'{BASE_URL}/users/{user_id}')
    print('Get:', response.status_code, response.json())

# 3. 更新整个用户信息（PUT）
def update_user(user_id, name, email):
    response = requests.put(f'{BASE_URL}/users/{user_id}', json={
        'name': name,
        'email': email
    })
    print('Update (PUT):', response.status_code, response.json())

# 4. 部分更新用户信息（PATCH）
def patch_user(user_id, data):
    response = requests.patch(f'{BASE_URL}/users/{user_id}', json=data)
    print('Patch:', response.status_code, response.json())

# 5. 删除用户（DELETE）
def delete_user(user_id):
    response = requests.delete(f'{BASE_URL}/users/{user_id}')
    print('Delete:', response.status_code)

if __name__ == '__main__':
    # 测试流程
    create_user('Alice', 'alice@example.com')
    create_user('Bob', 'bob@example.com')
    get_user(1)
    update_user(1, 'Alice Updated', 'alice.new@example.com')
    patch_user(2, {'email': 'bob.new@example.com'})
    delete_user(1)
    get_user(1)  # 查看删除后是否还能查到