import requests
import bs4

# headers из браузера
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
}

URL = 'https://habr.com/ru/all/'
KEYWORDS = ['браузер', 'алгоритм', 'инфраструктура', 'python', 'робот']

response = requests.get(URL, headers=HEADERS)
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')

articles = soup.find_all("article")
# print(len(articles))


def insert_text() -> str:
    tmp = ''
    text = article.find_all('p')
    if text == []:
        try:
            text = article.find(
                class_='article-formatted-body article-formatted-body article-formatted-body_version-1').text
            return text
        except AttributeError:
            text = article.find(class_='tm-voice-article__body').text
            return text
    else:
        for el in text:
            string = article.find('p').text
            tmp += string
        return tmp

# Вывести в консоль список подходящих статей в формате: <дата> - <заголовок> - <ссылка>
for article in articles:
    text = insert_text()
    for word in KEYWORDS:
        if word in text.lower():
            date = article.find('time').attrs["title"]
            href = article.find(class_='tm-article-snippet__title-link').attrs["href"]
            title = article.find('h2').find("span").text
            result = f'{date} - {title} - {URL[0:-5]}{href}'
            print(result)
