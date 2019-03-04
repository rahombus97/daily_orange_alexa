import feedparser
import re
import random

class HeadLines():
    def __init__(self):
        print('Headlines')

    def _stripHTML(self, summary):
        p = re.compile(r'<.*?>')
        return p.sub('', summary)

    def _getRandomTransition(self):
        transitions = [
                    "Next", 
                    "In other news", 
                    "Also", 
                    "In addition", 
                    "On top of that", 
                    "Additionaly",
                ] 
        return random.choice(transitions)

    def getHeadlines(self):
        url = "http://dailyorange.com/feed"
        rss = feedparser.parse(url)
        headlines = ""
        for i, headline in enumerate(rss.entries):
            summary = self._stripHTML(headline["summary"].split("<a", 1)[0])
            headline = self._stripHTML(headline["title"])
            if i == 0:
                transition = "First"
            else:
                transition = self._getRandomTransition()
            headlines += "{}, {}. {}".format(transition, headline, summary)
        return headlines
