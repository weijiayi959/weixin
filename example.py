from lxml import etree
from urllib.parse import urlencode


import requests
from requests import ConnectionError


max_numbers = 5

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'CXID=2093D0F043C474DC4B66E12A239C41BC; SUID=957EF23A3765860A5B8E911A0001BC7D; ABTEST=8|1536935576|v1; IPLOC=CN3407; weixinIndexVisited=1; SUV=00671DEE3AF27E775B9BC69981957590; ad=$WCapZllll2b0I9zlllllVmbhV6lllllnsJMOyllll9lllllRklll5@@@@@@@@@@; JSESSIONID=aaaunwcyDSwqR5CaRXBvw; sct=1; PHPSESSID=732c9iuqpijifkdk8s5c8m7531; SUIR=8A70FC350E0B7BD2FB5B91800F221138; SNUID=8B70FD340F0B7AD1475FC3950FB9ABF6; ppinf=5|1536973604|1538183204|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo1NDpBcG9sbG8lRTElQjUlOTYlQ0ElQjglRTElQjUlOTclQ0ElQjAlRTElQjUlOTIlRTIlODElQkZ8Y3J0OjEwOjE1MzY5NzM2MDR8cmVmbmljazo1NDpBcG9sbG8lRTElQjUlOTYlQ0ElQjglRTElQjUlOTclQ0ElQjAlRTElQjUlOTIlRTIlODElQkZ8dXNlcmlkOjQ0Om85dDJsdUs1dGJHa0RqU3lYNkVtOGhDbDlSTzBAd2VpeGluLnNvaHUuY29tfA; pprdig=ly1Y7KW3E9H4wamtCA83eNcjOjWBLigF5KD1qjOAlywBsy5W9hZZQ8oXOCsA_VkUHeQpWYhuHPmzc_cw_8PG64QofRGxd6P4OdE23ziZuZdZoBZRKegbe-HzfTqlsQXQNloJc01J8XCrArNwVQK7q1TrSENZ9fGmH6vbLo2EelE; sgid=08-37104503-AVucWyQIbdJKubZc26PibAaw; ppmdig=1536973605000000f827cd44d6a950db3be0cda1287d5465',
    'Host': 'weixin.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
    }

proxy = None


def get_proxies():
    response = requests.get('http://localhost:5555/random')
    return response.text


def get_html(url, count=1):
    global proxy

    if count >= max_numbers:
        print('Too many.')
        return None

    try:
        if proxy:
            proxies = {
                'http': 'http://' + get_proxies()
                }
            response = requests.get(url, headers=headers, allow_redirects=False, proxies=proxies)
        else:
            response = requests.get(url, headers=headers, allow_redirects=False)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            proxy = get_proxies()
            if proxy:
                print('Useing proxy.', proxy)
                return get_html(url)
            else:
                print('Get proxy fiald.')
                return None
    except ConnectionError:
        proxy = get_proxies()
        count += 1
        return get_html(url)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'page': page,
        'type': 2,
        'ie': 'utf8'
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html



def get_url(html):
    try:
        response = etree.HTML(html)
        url = response.xpath('//div[@class="txt-box"]/h3/a/@href')
        return url
    except ValueError:
        pass


def parse_detail(url):
    response = requests.get(url)
    response = etree.HTML(response)
    title = response.xpath('//h2[contains(@class,"rich_media_title") and @id="activity-name"]/text()')
    print(title)


def main():

    for i in range(1, 101):
        html = get_index('风景', i)
        for url in get_url(html):
            parse_detail(url)


if __name__ == "__main__":
    main()
