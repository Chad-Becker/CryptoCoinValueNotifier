import json
import requests
import smtplib
from email.mime.text import MIMEText

class Notifier:

    def __init__(self, msg, server, config, cryptoCurrency, comparableCurrency):
        self._msg = msg
        self._server = server
        self._config = config
        self._cryptoCurrency = cryptoCurrency
        self._comparableCurrency = comparableCurrency
        req = requests.get(config["url"][cryptoCurrency])
        self._pivotValue = req.json()[config["comparableCurrency"][comparableCurrency]]

    def sendUpdate(self):       
        req = requests.get(self._config["url"][self._cryptoCurrency])
        currentValue = req.json()[self._config["comparableCurrency"][self._comparableCurrency]]

        percentChange = abs(1 - currentValue / self._pivotValue)

        if percentChange >= self._config["threshold"]:
            sendString = "Pivot Value: $%d\nCurrent Value: $%d" % (self._pivotValue, currentValue)
            
            self._pivotValue = currentValue
        
            self._msg.set_payload(MIMEText(sendString))
            self._server.sendmail(self._config["email"]["fromAddr"], self._config["email"]["toAddr"], self._msg.as_string())