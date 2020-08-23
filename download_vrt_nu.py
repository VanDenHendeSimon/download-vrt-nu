import os
import pickle
import requests
from bs4 import BeautifulSoup


def get_text(url):
    return requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text


def get_season_data(season_url):
    season = season_url.rstrip('/').split('/')[-1].split('.')[0]
    season_soup = BeautifulSoup(get_text(
        'https://www.vrt.be%s' % season_url
    ), 'html.parser')
    episodes_list = season_soup.find_all('li')

    episodes = dict()
    for episode in episodes_list:
        h3 = episode.find('h3')
        episode_title = h3.text.strip()
        episode_url = 'https://www.vrt.be%s' % h3.find('a')['href']
        episodes[episode_title] = episode_url

    return season, episodes


def main(show_title):
    show_url = 'https://www.vrt.be/vrtnu/a-z/%s/' % show_title
    soup = BeautifulSoup(get_text(show_url), 'html.parser')

    season_list = soup.find(id='seasons-list')
    season_episode_urls = [
        a['href'] for a in season_list.find_all('a', href=True)
    ]

    for season_episode_url in season_episode_urls:
        season, episodes = get_season_data(season_episode_url)
        print("Season %s" % season)
        for idx, episode in enumerate(episodes.keys()):
            print("Episode %s: %s (%s)" % (
                idx+1, episode, episodes[episode]
            ))


if __name__ == '__main__':
    main('dertigers')
