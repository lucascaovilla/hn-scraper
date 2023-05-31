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
    return render_template('home.html', news = pop_list)
  elif keyword == 'new':
    new_list = new_news['hits']
    return render_template('home.html', news = new_list)

@app.route('/index')
def index():
  news_id = request.args.get('news_id')
  news_root_url = 'http://hn.algolia.com/api/v1/items/' + news_id
  info = get_data(news_root_url)
  raw_comments = info['children']
  comments = []
  for comment in raw_comments:
    if comment['text'] == None:
      continue
    else:
      comment['text'] = comment['text'].replace('<p>', "")
      comment['text'] = comment['text'].replace('</p>', "")
      comment['text'] = comment['text'].replace('<a>', "")
      comment['text'] = comment['text'].replace('</a>', "")
      comments.append(comment)
  return render_template('index.html', news = info, comments = comments)



app.run(host='0.0.0.0')