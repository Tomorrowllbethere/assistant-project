import scrapy
import json


class RateUsdEurSpider(scrapy.Spider):
    name = "rate_usd_eur"
    allowed_domains = ["api.privatbank.ua"]
    start_urls = ["https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"]

    def parse(self, response):
       # Перетворюємо JSON-відповідь на Python-структуру (список словників)
        data = json.loads(response.text)
        
        # Створюємо словник для збереження курсів валют
        rates = {}
        
        # Проходимо по кожному елементу списку і зберігаємо необхідні дані
        for item in data:
            currency = item['ccy']
            rate = item['sale']
            rates[currency] = rate
        
        # Повертаємо результат у вигляді словника
        return rates
