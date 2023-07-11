from config import KEYS, API_KEY, RATE
import requests
import json


class APIException(Exception):
    def __str__(self):
        return "Server error"

class CurrenciesException(APIException):
    def __str__(self):
        return "User currencies identical"

class QuoteException(APIException):
    def __str__(self):
        return "User 1 value error"

class BaseException(APIException):
    def __str__(self):
        return "User 2 value error"

class AmountException(APIException):
    def __str__(self):
        return "User amount error"

class LenException(APIException):
    def __str__(self):
        return "User len(value) != 3"

class CurrencyConverted:

    @staticmethod
    def get_price(value: list):

        try:
            if len(value) != 3:
                raise LenException
        except LenException as e:
            print(e)
            return "Ошибка неверное количество параметров \n" \
                   "Посмотрите пример введя команду /request"

        quote, base, amount = value



        try:
            quote = KEYS[quote.lower()]
        except KeyError:
            try:
                raise QuoteException
            except QuoteException as e:
                print(e)
                return f"Не нашли 1 валюту {quote}"

        try:
            base = KEYS[base.lower()]
        except KeyError:
            try:
                raise BaseException
            except BaseException as e:
                print(e)
                return f"Не нашли 2 валюту {base}"

        try:
            amount = float(amount)
        except ValueError:
            try:
                raise AmountException
            except AmountException as e:
                print(e)
                return f"Неверно введено число {amount}"

        try:
            if quote == base:
                raise CurrenciesException
        except CurrenciesException as e:
            print(e)
            return "Ввели 2 одинаковые валюты"

        result = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{quote}/{base}").json()[RATE]
        return result * amount






