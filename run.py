from requests_html import HTMLSession
import chompjs
import pandas as pd


def fetch(x):
    base_url = 'https://www.rei.com'
    r = s.get(f'https://www.rei.com/c/hiking-backpacks?page={x}')
    results = [base_url + link.attrs['href'] for link in r.html.find('#search-results > ul > li > a')]
    return list(dict.fromkeys(results))


def parse_product(url):
    r = s.get(url)
    details = r.html.find('script[type="application/ld+json"]', first=True)
    data = chompjs.parse_js_object(details.text)
    return data


def main():
    products = [url for x in range(1, 3) for url in fetch(x)]
    return [parse_product(url) for url in products]


if __name__ == '__main__':
    s = HTMLSession()
    df = pd.json_normalize(main())
    df.to_csv('rei-backpacks.csv', index=False)
    print('finished')
