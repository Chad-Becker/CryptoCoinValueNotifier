import requests
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler

def sendUpdate():
    req = requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD")
    print req.text

    msg = MIMEText(req.text)

    msg["Subject"] = "Testing"
    msg["From"] = "snd_addr"
    msg["To"] = "rcv_addr"

    server = smtplib.SMTP("localhost")
    server.sendmail("snd_addr", "rcv_addr", msg.as_string())
    server.quit()

scheduler = BlockingScheduler()
scheduler.add_job(sendUpdate, 'interval', seconds=10)
scheduler.start()
