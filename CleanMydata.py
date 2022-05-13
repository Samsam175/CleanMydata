import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import numpy as np
import csv

def impor():
    data1,data2=[],[]
    with open('Companies.txt', newline='', encoding="utf8") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            data1.append(row)
    with open('Common_email_services.txt', newline='', encoding="utf8") as f2:
        reader = csv.reader(f2, delimiter=';')
        for row in reader:
            data2.append(row)
    return data1,data2


# account credentials
username = input("Email")
password = input("Mot de passe")

# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
imap.login(username, password)

status, messages = imap.select("INBOX")
# number of top emails to fetch
N = 3
# total number of emails
messages = int(messages[0])


Common_email_services=[]
Companies=[]

Companies,Common_email_services=impor()


print(Common_email_services)
Subjects=np.ndarray(0)
Senders=np.ndarray(0)



def isitacompany(address):
    domain= From.split('@')[1]
    if domain not in Common_email_services:
            print("Not in my list, is this a company email : " + address + "?")


for i in range(messages, messages-N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            
            
            print("Subject:", subject)
            print("From:", From)
            np.append(Subjects,subject)
            np.append(Senders,From)
            print("="*100)

# close the connection and logout
imap.close()
imap.logout()
