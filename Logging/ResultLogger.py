import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import datetime
import requests
import os


class ResultLogger:
    def __init__(self, log_path='./return_ingredients_logs.log'):
        load_dotenv()
        self.discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        self.logger = logging.getLogger("ResultLogger")

        handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=3)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def __del__(self):
        self.logger.handlers.clear()

    def log(self, message, is_inference):
        if is_inference:
            name = 'Inference'
        else:
            name = 'Search'
        self.logger.info(f'{name} - {message}')
        now = datetime.datetime.now()
        self.send_alarm(f' {now}: -{name} - {message}')

    def send_alarm(self, message):
        requests.post(self.discord_webhook_url, json={"content": message})
