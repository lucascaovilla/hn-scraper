from hn_request import get_data
from flask import Flask, render_template, request, redirect


app = Flask('Maratona News')

@app.route('/')
def home():
  popular_news = get_data('https://hn.algolia.com/api/v1/search?tags=story')
  new_news = get_data('http://hn.algolia.com/api/v1/search_by_date?tags=story')
  keyword = request.args.get('order_by')
  if keyword == 'popular' or keyword == None:
    pop_list = popular_news['hits']
    for news in pop_list:
      news['id_url'] = news['objectID']
    return render_template('home.html', news = pop_list)
  elif keyword == 'new':
    new_list = new_news['hits']
    for news in new_list:
      news['id_url'] = news['objectID']
    return render_template('home.html', news = new_list)

@app.route('/index')
def index():
  news_id = request.args.get('news_id')
  news_root_url = 'http://hn.algolia.com/api/v1/items/' + news_id
  info = get_data(news_root_url)
  comments = info['children']
  for comment in comments:
    comment['text'] = comment['text']
  return render_template('index.html', news = info, comments = comments)



app.run(host='0.0.0.0')