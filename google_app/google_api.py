from __future__ import annotations

import datetime
import logging

import httplib2
import apiclient.discovery
import requests
import xmltodict as xmltodict
from oauth2client.service_account import ServiceAccountCredentials
from google_app.models import Order
from notifiers import get_notifier

from test_google_api.settings import TG_TOKEN, TG_ID

CREDENTIALS_FILE = './creds.json'

SPREADSHEET_ID = '1lpPGtsooRUJMBk_LIOKVbcGdPzeDdMiAaexn9KhYdME'
RANGE = 'A2:E500'
DIMENSION = 'ROWS'
DOLLARS_EXCHANGE_URL = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req='
DOLLAR_CHAR_CODE = 'USD'
DEFAULT_USD_RATE = '60'

logger = logging.getLogger(__name__)


class GoogleApi:
    def __init__(self):
        #  Auth and get access to API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        http_auth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=http_auth)

    @staticmethod
    def dollar_exchange_rate() -> str:
        current_date = datetime.datetime.now()
        current_date_string = current_date.strftime('%d/%m/%Y')

        url = f'{DOLLARS_EXCHANGE_URL}{current_date_string}'
        if not (data := requests.get(url)):
            raise Exception('Failed to get dollar exchange rate')

        # Let's convert to a dict for convenience
        curs_dict = xmltodict.parse(data.text)
        for item in curs_dict['ValCurs']['Valute']:
            if item['CharCode'] == DOLLAR_CHAR_CODE:
                return item['Value']

        logger.error('USD curs not found')
        return DEFAULT_USD_RATE

    def get_values_by_spreadsheet(self) -> list:
        values = self.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE,
            majorDimension=DIMENSION
        ).execute()
        return values.get('values')

    @staticmethod
    def prepare_data_to_db(data_stub: list, dollar_rate: float) -> list:
        """
        Prepare list dicts for bulk inserting to DB in model Order.
        """

        result = []
        for i in data_stub:
            result.append({'number': i[0],
                           'order_number': i[1],
                           'price_dollars': i[2],
                           'price_rubles': int(i[2]) * dollar_rate,
                           'delivery_time': i[3]
                           })
        return result

    @staticmethod
    def notification_expiration(data_db: list) -> None:
        """
        Let's notify about the delay in Telegram
        """
        telegram = get_notifier('telegram')
        for item in data_db:
            if datetime.datetime.now() > datetime.datetime.strptime(item['delivery_time'], '%d.%m.%Y'):
                telegram.notify(
                    message=f'Delivery time of your order - {item["order_number"]} has expired',
                    token=TG_TOKEN,
                    chat_id=TG_ID
                )

    def proccess(self):
        dollar_rate = float(self.dollar_exchange_rate().replace(',', '.'))
        if not (values_by_spreadsheet := self.get_values_by_spreadsheet()):
            logger.error('Failed to get data from spreadsheet')
            return

        data_db = self.prepare_data_to_db(values_by_spreadsheet, dollar_rate)

        # Delete all orders first
        Order.objects.all().delete()
        Order.bulk_create_orders(uniques=['order_number'], data=data_db)
        self.notification_expiration(data_db)

    def run(self):
        try:
            self.proccess()
        except Exception as err:
            logger.error(f'Failed Google Api Proccess with error - {err}')
