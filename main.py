import requests
from bs4 import BeautifulSoup as bs
import urllib.parse
from time import sleep
import random
import re

def get_html(url):
        _html = ""
        resp = requests.get(url)
        if resp.status_code == 200:
            _html = resp.text
        return _html

def get_bs(html):
    return bs(html, 'html.parser')

class Get:
    def __init__(self, q):
        self.q = q
        self.base_url = "https://music.bugs.co.kr/search/track"
        self.query_list = \
            {'q': urllib.parse.quote_plus(q), 'target': 'ARTIST_ONLY', 'flac_only': 'false', 'sort': 'A', 'page': 1}

        self.page_bs = get_bs(get_html(self.make_url(1)))
        self._set_max_page()
        

    def _set_max_page(self):
        self.page = 1
        self.max_page = len(self.page_bs.find('div', {'class': 'paging'}).find_all('a'))
        
    def make_url(self, page):
        self.query_list['page'] = page
        return self.base_url + "?" + "&".join("{}={}".format(key, value) for key, value in self.query_list.items())

    def extract_lyrics(self, _bs):
        try:
            return _bs.find('xmp').text
        except:
            return ""
    
    def get_music_list(self, _bs):
        return [x.get('href') for x in _bs.find_all('a', {'class': 'trackInfo'})]

    def get_song(self):
        

        for i in range(1, self.max_page + 1):
            _str = ''
            if i != 1:
                self.page_bs = get_bs(get_html(self.make_url(i)))
                self.page = i
                print(self.make_url(i))

            for song in self.get_music_list(self.page_bs):
                sleep(random.random() * 2)
                print(song)
                song_bs = get_bs(get_html(song))
                data = self.extract_lyrics(song_bs) + "\n\n"

                # Delete languages other than Korean and ASCII code.
                _re = re.compile('[^ ㄱ-ㅣ가-힣\d\x00-\x7F]+')
                if len(_re.findall(data)) > 1:
                    continue
                _str += data

        return _str



q = Get('방탄소년단')
print(q.get_song())