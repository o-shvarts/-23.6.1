import json
import requests
from config import keys

class ConvertionException(Exception):
    pass



class Exceptions:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        #  Ошибку с количеством переменных вынес в основной код, так же решил, что ввод одинаковых валют для конвертации
        #  некритичен, так как в этом случае бот отрабатывает корректно



        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_quote = json.loads(r.content)[keys[quote]]
        return total_quote

