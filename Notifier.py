import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler


def initPivotValue():
    global pivotValue
    req = requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD")
    pivotValue = req.json()["USD"]
    #print pivotValue

def sendUpdate(msg, server, fromAddr, toAddr):
    global pivotValue
    
    req = requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD")
    currentValue = req.json()["USD"]    

    percentChange = abs(1 - currentValue / pivotValue)

    if percentChange >= 0.2:
        sendString = "Pivot Value: $" + str(pivotValue) + "\nCurrent Value: $" + str(currentValue)
        #print sendString
        
        pivotValue = currentValue
    
        msg.set_payload(MIMEText(sendString))
        server.sendmail(fromAddr, toAddr, msg.as_string()) 


fromAddr = "from_addr"
toAddr = "to_addr"

msg = MIMEMultipart()
msg["From"] = fromAddr
msg["To"] = toAddr
msg["Subject"] = "Ethereum Notification"

senderAddr = fromAddr
senderPasswd = "password"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login(senderAddr, senderPasswd)

initPivotValue()

scheduler = BlockingScheduler()
scheduler.add_job(sendUpdate, "interval", [msg, server, fromAddr, toAddr], minutes=30)
scheduler.start()

server.close()
