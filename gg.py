import requests

# response = requests.post(
#     url='http://127.0.0.1:5000/user',
#     json={'tittle': 'model', 'description': 'ne hochu ', 'author': 'Ibra'}
# )

response = requests.patch(
    url='http://127.0.0.1:5000/user/1',
    json={'author': "NEDENIS"}
)
print(response.text)
print(response.status_code)


