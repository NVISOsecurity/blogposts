import argparse
import os
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText  

#change your smtp login details here.
fromaddr = ""
smtp_password=""
smtp_server =""
smtp_port = 587

#change your signal REGISTRATION number here:
signal_registration_number =""


#leave these blank, they get handles by the aggressor.
smsaddr = ""
mailaddr = ""


parser = argparse.ArgumentParser(description='beacon info')
parser.add_argument('--computer')
parser.add_argument('--ip')
parser.add_argument('--receive-texts', action="store_true")
parser.add_argument('--receive-emails', action="store_true")
parser.add_argument('--receive-signalmessage', action="store_true")
parser.add_argument('--email-address')
parser.add_argument('--mail_totext')
parser.add_argument('--signal-number')

args = parser.parse_args()
toaddr = []

#take care off email and email2text:
if args.receive_texts and args.mail_totext:
    toaddr.append(smsaddr)
if args.receive_emails and args.email_address:
    toaddr.append(args.email_address)


#message contents:
hostname = args.computer
internal_ip = args.ip
body = "Check your teamserver! \nHostname - " + str(hostname) + "\nInternal IP - " + str(internal_ip)

#email logic
if toaddr:
	print("debug")
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = ", ".join(toaddr)
	msg['Subject'] = "INCOMING BEACON"
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP(smtp_server, smtp_port)
	server.starttls()
	server.login(fromaddr,smtp_password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

#signal-cli
if args.signal_number and args.receive_signalmessage:
	#take care of signal
	print(f"{args.signal_number}")
	os.system(f"signal-cli -u {signal_registration_number} send -m " + "\"" + str(body) + "\"" +  f" {args.signal_number}")
