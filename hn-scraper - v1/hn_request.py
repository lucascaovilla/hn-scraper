import requests
import json

def get_data(url):
  data = requests.get(url).json()
  print(type(data))
  return data