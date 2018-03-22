import requests

user = {"user_email": "theo@gmail.com",
        "user_age": 24,
        "heart_rate": 40}
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=user)

user = {"user_email": "joe@gmail.com",
        "user_age": 44,
        "heart_rate": 120}
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=user)
user = {"user_email": "joe@gmail.com",
        "heart_rate_average_since": "2018-03-22 10:00:36.0"}
r = requests.post(
    "http://127.0.0.1:5000/api/heart_rate/interval_average", json=user)
