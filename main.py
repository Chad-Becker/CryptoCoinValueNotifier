import json
import smtplib
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.blocking import BlockingScheduler
from notifier import Notifier

def run():
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

    notifier = Notifier(msg, server, config, "eth", "usd")

    scheduler = BlockingScheduler()
    scheduler.add_job(notifier.sendUpdate, "interval", minutes=config["interval"]["min"])
    scheduler.start()

    server.close()

if __name__ == "__main__":
    run()