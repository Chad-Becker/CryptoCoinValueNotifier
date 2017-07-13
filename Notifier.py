import json
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler


def initPivotValue():
    global pivotValue
    global config
    req = requests.get(config["url"]["eth"])
    pivotValue = req.json()[config["comparableCurrency"]["usd"]]
    #print pivotValue

def sendUpdate(msg, server, fromAddr, toAddr):
    global pivotValue
    
    req = requests.get(config["url"]["eth"])
    currentValue = req.json()[config["comparableCurrency"]["usd"]]    

    percentChange = abs(1 - currentValue / pivotValue)

    if percentChange >= config["threshold"]:
        sendString = "Pivot Value: $" + str(pivotValue) + "\nCurrent Value: $" + str(currentValue)
        #print sendString
        
        pivotValue = currentValue
    
        msg.set_payload(MIMEText(sendString))
        server.sendmail(fromAddr, toAddr, msg.as_string()) 


fObj = open("NotifierConfig.json", "r")
config = json.load(fObj)

fromAddr = config["email"]["fromAddr"]
toAddr = config["email"]["toAddr"]

msg = MIMEMultipart()
msg["From"] = fromAddr
msg["To"] = toAddr
msg["Subject"] = config["email"]["subject"]["eth"]

senderAddr = fromAddr
senderPasswd = config["email"]["passwd"]

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login(senderAddr, senderPasswd)

initPivotValue()

scheduler = BlockingScheduler()
scheduler.add_job(sendUpdate, "interval", [msg, server, fromAddr, toAddr], minutes=config["interval"]["min"])
scheduler.start()

server.close()
