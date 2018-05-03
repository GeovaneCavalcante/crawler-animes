import requests
from bs4 import BeautifulSoup as bs
import pprint
import json


class CrawlerAnimes(object):

    animesAll = {}
    epListDescription = []
    epListFrame = []
    animes = []

    def getAnimes(self, url):

        r  = requests.get(url)
        soup = bs(r.content, 'html.parser')
        divAnimesDublados = soup.find_all("div", class_="contentBox")

        for link in divAnimesDublados[0].find_all('div', class_='thumb'):
            link1 = link.find('a')
            if link.get('class') == ['number']:
                self.getAnimesList(link.get('href'))
            else:
                self.animes.append(link1)

        for link in divAnimesDublados[0].find_all('a'):
            if link.get('class') == ['number']:
                self.getAnimesList(link.get('href'))

        a = 1
        for ani in self.animes:
            a += 1
        
            anime = {}
            anime['title'] = ani['title']
            anime['linkEpDescription'] = ani['href']
            anime['imgAnime'] = ani.find_all('img')[0]['src']
        
            self.animesAll[a] = anime


    def getAnimesList(self, url):

        r  = requests.get(url)
        soup = bs(r.content, 'html.parser')
        divAnimesDublados = soup.find_all("div", class_="contentBox")

        for link in divAnimesDublados[0].find_all('div', class_='thumb'):
            link = link.find('a')
         
            if link.get('class') != ['number']:
                self.animes.append(link)
         
           
          
    
    def getAnimesEpList(self):

        a = 0
        
        for anime in self.animesAll: 

            r  = requests.get(self.animesAll[anime]['linkEpDescription'])
            soup = bs(r.content, 'html.parser')
            
            ul = soup.find_all("ul", id="lcp_instance_0") 
            
            listEp = []

            for li in ul[0].find_all('a'):
                ep = {}
                ep['frame'] = self.getAnimesEpFrame(li.get('href'))
                ep['titleEp'] = li.get('title')
                listEp.append(ep)

            self.animesAll[anime]['Epsodios'] = listEp
            #print(self.animesAll[anime])  
            #print(json.dumps(self.animesAll[anime], sort_keys=True, indent=4, separators=(',', ': ')))    


    def getAnimesEpFrame(self, link):

        r  = requests.get(link)
        soup = bs(r.content, 'html.parser')

        ep={
            'linkFrame': soup.find_all("source")[0]['src'],
            'posterEp': soup.find_all("video")[0]['poster']

        }

        return ep

   
# Epsódio list
url = 'https://www.animesorion.tv/animes-dublados'

teste = CrawlerAnimes()
teste.getAnimes(url)
teste.getAnimesEpList()

#print(len(teste.animes))
print(json.dumps(teste.animesAll, sort_keys=True, indent=4, separators=(',', ': ')))    



 
   