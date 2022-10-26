from constant import *
import requests
import bs4

response = requests.get(URL, headers=HEADERS)
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')

articles = soup.find_all("article")
# print(len(articles))


def insert_text(article) -> str:
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


# поиск по preview в статье
def find_in_preview():
    for article in articles:
        text = insert_text(article)
        for word in KEYWORDS:
            if word in text.lower():
                date = article.find('time').attrs["title"]
                href = article.find(class_='tm-article-snippet__title-link').attrs["href"]
                title = article.find('h2').find("span").text
                result = f'{date} - {title} - {URL[0:-8]}{href}'
                print(result)


def insert_text_blog(url) -> str:
    response = requests.get(url, headers=HEADERS)
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    post_body = soup.find(id='post-content-body').text
    return post_body


# поиск по тексту в статьях
def find_in_blog():
    for article in articles:
        href = article.find(class_='tm-article-snippet__title-link').attrs["href"]
        blog_url = f'{URL[0:-8]}{href}'
        text = insert_text_blog(blog_url)
        for word in KEYWORDS:
            if word in text.lower():
                date = article.find('time').attrs["title"]
                href = article.find(class_='tm-article-snippet__title-link').attrs["href"]
                title = article.find('h2').find("span").text
                result = f'{date} - {title} - {URL[0:-8]}{href}'
                print(result)


# Вывести в консоль список подходящих статей в формате: <дата> - <заголовок> - <ссылка>
if __name__ == "__main__":
    # find_in_preview()
    find_in_blog()