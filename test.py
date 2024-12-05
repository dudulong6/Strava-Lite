import requests
import constants  # Assumes you have constants defined for API paths and ports


class UserAPI:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers if headers else {'Content-Type': 'application/json'}

    def register_user(self, name, age):
        """Register a user"""
        user_register_post_api = self.base_url + constants.USER_API_PATH
        user_register_data_dict = {
            "name": name,
            "age": age
        }
        response = requests.post(url=user_register_post_api, headers=self.headers, json=user_register_data_dict)
        return response.json()  # Return the server response content

    def list_users(self):
        """List all users"""
        users_get_api = self.base_url + constants.USERS_API_PATH
        response = requests.get(url=users_get_api, headers=self.headers)
        return response.json()  # Return user list

    def get_user(self, user_id):
        """Get specified user information"""
        user_get_api = self.base_url + constants.USER_API_PATH + f'/{user_id}'
        response = requests.get(url=user_get_api, headers=self.headers)
        return response.json()  # Return user information

    def delete_user(self, user_id):
        """Delete specified user"""
        user_delete_api = self.base_url + constants.USER_API_PATH + f'/{user_id}'
        response = requests.delete(url=user_delete_api, headers=self.headers)
        return response.json()  # Return deletion result

    def put_user_workouts(self, user_id, workouts_dict):
        """Add workouts for specified user"""
        put_user_workouts_api = self.base_url + constants.WORKOUT_API_PATH + f'/{user_id}'
        response = requests.put(url=put_user_workouts_api, headers=self.headers, json=workouts_dict)
        return response.json()  # Return result of adding workouts

    def get_user_workouts(self, user_id):
        """List all workouts added by specified user"""
        get_user_workouts_api = self.base_url + constants.WORKOUT_API_PATH + f'/{user_id}'
        response = requests.get(url=get_user_workouts_api, headers=self.headers)
        return response.json()  # Return all workouts added by specified user

    def put_follow_user(self, user_id, follow_id):
        """
        :param user_id: ID of the current user
        :param follow_id: ID of the user to be followed
        :return: List of IDs that the user is currently following (including the new one)
        """
        follow_id_info = {
            'follow_id': follow_id
        }
        put_follow_user_api = self.base_url + constants.FOLLOW_LIST_API_PATH + f'/{user_id}'
        response = requests.put(url=put_follow_user_api, headers=self.headers, json=follow_id_info)
        return response.json()  # Return list of IDs being followed (including the new one)

    def get_show_friend_workouts(self, user_id, follow_id):
        """
        :param user_id: ID of the current user
        :param follow_id: ID of the user to check for workouts
        """
        get_show_friend_workouts_api = self.base_url + constants.FOLLOW_LIST_API_PATH + f'/{user_id}/{follow_id}'
        response = requests.get(url=get_show_friend_workouts_api, headers=self.headers)
        return response.status_code, response.json()


if __name__ == '__main__':
    # Set base URL and headers for requests
    base_url = f'http://127.0.0.1:{constants.PORT}'
    user_api = UserAPI(base_url)

    # *** Register user ***
    print('Registering user...')
    register_response = user_api.register_user("Rocco", 18)
    print('Register response:', register_response)
    print('\n--- Divider ---')

    # *** List all users ***
    print('Listing all users...')
    all_user_info = user_api.list_users()
    print('All users:', all_user_info)

    # Get the first user ID
    if all_user_info.get('users'):
        user_id = all_user_info['users'][0]['id']  # Can customize
        print('Fetching user with ID:', user_id)

        # *** Get user information ***
        print('Getting user info...')
        user_info = user_api.get_user(user_id)
        print('User info:', user_info)
        print('\n--- Divider ---')

        # *** Delete user ***
        print('Deleting user...')
        delete_response = user_api.delete_user(user_id)
        print('Delete response:', delete_response)
    else:
        print('No users found.')
        all_user_info = user_api.list_users()
        print('All users:', all_user_info)

        print('\n--- 分割线 ---')
        print('Registering user...')
        register_response = user_api.register_user("嘟嘟龙_v2", 22)
        print('Register response:', register_response)

        user_id = all_user_info['users'][0]['id']
        print('user_id', user_id)

        # *** 添加锻炼 ***
        workouts_dict = {
            "date": '2024-12-05',
            "time": '13-27',
            "distance": '123456'
        }
        put_user_workouts_response = user_api.put_user_workouts(user_id, workouts_dict)
        print('Put Workout response:', put_user_workouts_response)
        get_user_workouts_response = user_api.get_user_workouts(user_id)
        print('Get Workout response:', put_user_workouts_response)

        print('\n--- 分割线 ---')
        all_user_info = user_api.list_users()
        print('All users:', all_user_info)
        # *** 关注好友 ***
        current_user_id = all_user_info['users'][0]['id']  # 是当前用户的 ID
        follow_id = all_user_info['users'][1]['id']  # 是用户想要关注的 ID
        print('current_user_id', current_user_id)
        print('follow_id', follow_id)
        put_follow_user_response = user_api.put_follow_user(user_id, follow_id)
        print('Put follow user response:', put_follow_user_response)

        print('\n--- 分割线 ---')
        # *** 显示朋友锻炼 ***
        # 但它不会列出您自己的，而是仅当您关注了他们时才会列出朋友的。
        # get_show_friend_workouts_response = user_api.get_show_friend_workouts(current_user_id, follow_id)
        # 如果您不关注他们，则状态代码必须是403。---> 找一个当前用户 未 关注的 id 替换即可。
        get_show_friend_workouts_response = user_api.get_show_friend_workouts(current_user_id,
                                                                              '6d3b23a1-6ec2-4d8c-b709-9b94d17b2a00')
        print('Get show friend workouts response:', get_show_friend_workouts_response)