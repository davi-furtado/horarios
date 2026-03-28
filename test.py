from requests import get

print(get('http://localhost:8000/').json())