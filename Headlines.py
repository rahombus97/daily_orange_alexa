import feedparser
import re
import random

class HeadLines():
    URL = 'http://dailyorange.com/feed'

    def __init__(self):
        print('Headlines')

    def _stripHTML(self, summary):
        p = re.compile(r'<.*?>')
        return p.sub('', summary)

    def _getRandomTransition(self):
        transitions = [
            'Next', 
            'In other news', 
            'Also', 
            'In addition', 
            'On top of that', 
            'Additionally',
        ] 
        return random.choice(transitions)

    def getHeadlines(self):
        rss = feedparser.parse(self.URL)
        headlines = ''
        for i, headline in enumerate(rss.entries):
            summary = self._stripHTML(headline['summary'].split('<a', 1)[0])
            headline = self._stripHTML(headline['title'])
            if i == 0:
                transition = 'First'
            else:
                transition = self._getRandomTransition()
            headlines += '{}, {}. {}'.format(transition, headline, summary)
        print(headlines)
        return headlines