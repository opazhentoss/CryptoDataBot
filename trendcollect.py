from fake_useragent import UserAgent
import requests

agent = UserAgent()
rez = []


def collect_data():
    response = requests.get(
        url='https://api.coinmarketcap.com/data-api/v3/cryptocurrency/spotlight?dataType=2&limit=5&rankRange=0&timeframe=24h',
        headers={'user-agent': f'{agent.random}'})

    data = response.json()

    for i in data["data"]["gainerList"]:
        name = i['name']
        change = i['priceChange']['priceChange24h']
        slug = i['slug']
        rez.append(
            {
                'name': name,
                'priceChange24h': change,
                'slug': slug
            }
        )

    for i in data["data"]["loserList"]:
        name = i['name']
        change = i['priceChange']['priceChange24h']
        slug = i['slug']
        rez.append(
            {
                'name': name,
                'priceChange24h': change,
                'slug': slug
            }
        )
    return rez
