import requests
import bs4

import sys


def main(argv):
    article_url = argv[1]
    
    gsch_url = f'https://scholar.google.com/scholar?q={article_url}'
    
    page = requests.get(gsch_url)
    
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    results = soup.find()
    
    # print(gsch_url)
    print(soup.contents)
    # print(results)

if __name__=='__main__':
    main(sys.argv)