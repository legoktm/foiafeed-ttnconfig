from bs4 import BeautifulSoup

def check(article):
    blocked = False

    # Rules that require a BeautifulSoup parse:
    if article.outlet in ['Miami Herald']:
        soup = BeautifulSoup(article.res.text, 'lxml')
        # Attempt to exclude AP and McClatchy articles from other feeds
        if (soup.find(attrs={'class': 'byline'}) and
                any(syndication in
                soup.find(attrs={'class':'byline'}).get_text().lower()
                for syndication in
                ['ap ', 'associated press', 'mcclatchydc'])):
            blocked = True

    # Rules that do not require a BeautifulSoup parse:
    # Exclude articles in LAT "Essential Politics" feed
    # (which shows multiple articles on a single page)
    if article.outlet == 'LA Times':
        if '/opinion/' in article.url or '/politics/essential/' in article.url:
            blocked = True

    # Exclude articles from WaPo's "202" newsletter series.
    # Headline and content don't match well
    if article.outlet == 'Washington Post' and '202' in article.title:
        blocked = True

    return blocked
