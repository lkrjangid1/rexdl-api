import requests
from bs4 import BeautifulSoup
from re import search
from flask import Flask ,jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False

def filecrSearch(title):
    all_data = []
    try:
        for i in range(1,5):
            url = f'https://rexdl.com/page/{i}/?s={title}'

            header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

            r = requests.get(url, headers=header)
            soup = BeautifulSoup(r.content,features='lxml')
            articals = soup.find_all('article')
            for item in articals:
                for url in BeautifulSoup(requests.get(item.find('a')['href'], headers=header).content,features='lxml').find_all('span',class_="readdownload a"):
                    dawnloadurl=url.find('a')['href']
                all_data.append(
                    {
                        'name':item.find('h2', class_='post-title').text,
                        'imgurl':item.find('img')['src'],
                        'dawnloadurl':dawnloadurl,
                        'uploaddate':item.find('p', class_='post-date').text,
                        'url':item.find('a')['href'],
                    }
                )
    except Exception as e:
            print(e)
    return all_data    



@app.route('/')
def home_page():
    return "Welcome to https://rexdl.com/ unofficial API"

@app.route('/<query>')
def home(query):
    

    return jsonify(filecrSearch(query))



if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
