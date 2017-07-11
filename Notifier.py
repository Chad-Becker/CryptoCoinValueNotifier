import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler

def sendUpdate(msg, server, fromAddr, toAddr):
    req = requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD")

    msg.set_payload(MIMEText(req.text))

    server.sendmail(fromAddr, toAddr, msg.as_string())

    print "Sent: " + req.text


fromAddr = "fromAddr"
toAddr = "toAddr"

msg = MIMEMultipart()
msg["From"] = fromAddr
msg["To"] = toAddr
msg["Subject"] = "Testing"

senderAddr = fromAddr
senderPasswd = "password"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login(senderAddr, senderPasswd)

scheduler = BlockingScheduler()
scheduler.add_job(sendUpdate, "interval", [msg, server, fromAddr, toAddr], seconds=10)
scheduler.start()

server.close()
