import requests


class Post:
    def __init__(self):
        self.post_url = 'https://api.npoint.io/c790b4d5cab58020d391'

    def get_data(self):
        response = requests.get(url=self.post_url)
        response.raise_for_status()
        return response.json()

# post = Post()
# print(post.all_posts)
