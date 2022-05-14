import imaplib
import email
from email.header import decode_header
import numpy as np
import csv

def impor(): #Import the list of companies and common email providers allready known
    data1,data2=[],[]
    with open('Companies.txt', newline='', encoding="utf8") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            data1.append(row[0])
    with open('Common_email_services.txt', newline='', encoding="utf8") as f2:
        reader = csv.reader(f2, delimiter=';')
        for row in reader:
            data2.append(row[0])
    return data1,data2

def write_to_csv(text,csvf): #Append Text at the end of a csv file
    with open(csvf, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([text])

#Import the list of companies and common email providers allready known
Common_email_services=[]
Companies=[]
Companies,Common_email_services=impor()

#Companies user is subed to
my_clutter=[] 

def isitacompany(address): #Check if an address come from a company if the programm can t tell it will ask the user
    if "@" in address :
        try:#They are some pretty rare exceptions where the address isn t correctly formated
            main, domain= address.split('@') #This should be fixed in the future i haven t find why yet
            domain=domain[:len(domain)-1]
            if domain in Companies:
                return True
            elif domain not in Common_email_services:
                    if ("no-reply" or "noreply" or "nepasrepondre" or "ne-pas-repondre" or "contact" or "notifications") in main:
                        Companies.append(domain)
                        write_to_csv(domain,'Companies.txt')
                        return True
                    print("Not in my list, is this a company email : " + address + "?")
                    r=input("Y or N ?")
                    if r=="n" or r=="N":
                        Common_email_services.append(domain)
                        write_to_csv(str("@"+domain),'Common_email_services.txt')
                        return False
                    elif r=="y" or r=="Y":
                        Companies.append(domain)
                        write_to_csv(domain,'Companies.txt')
                        return True
                    else:
                        isitacompany(address)
        except Exception:
            pass
            print("ignored the exception in isitacompany")    

def get_mails():
    # account credentials
    username = input("Email address")
    password = input("Password")
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    messages = int(messages[0])
    Subjects=[]
    Senders=[]
    for i in range(messages, 0, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            try:#They are rare exceptions in the encoding mainly some spams being encoded as unknown 8bit
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])

                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes) and encoding==None:
                        # if it's a bytes and no encoding info, decode to str asuming its utf8
                        subject = subject.decode("utf-8")
                    elif isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)

                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes) and encoding==None:
                        # if it's a bytes and no encoding info, decode to str asuming its utf8
                        From = From.decode("utf-8")
                    elif isinstance(From, bytes):
                        # if it's a bytes, decode to str
                        From = From.decode(encoding)
                    
                    Subjects.append(subject)
                    Senders.append(From)
            except Exception:
                pass
                print("ignored the exception in get_mails")
        if i%100 == 0 : #Just to know if it s doing smth
            print(i)
    imap.close()
    imap.logout()
    for i in range(len(Subjects)):#Writing fetched info to csv in order to avoid relaunching it when testing
        write_to_csv(Subjects[i],"Subjects.txt")
        write_to_csv(Senders[i],"Senders.txt")
    return Subjects,Senders

def add_to_clutter(send,subj):
    domain= send.split('@')[1] #Getting the name of the company which probably is the domain name in the email
    
    if domain not in my_clutter :
        my_clutter.append(domain[:len(domain)-1])

Subjects,Senders = get_mails()

#Looking at every Senders of email to try to know if its a company or not
for i in range(len(Senders)):
    send=Senders[i]
    subj=Subjects[i]
    if isitacompany(send)==True :
        add_to_clutter(send,subj)


open('My_clutter.txt', 'w').close() #Deleting the old list to avoid duplicates in the text file
mc= list(dict.fromkeys(my_clutter)) #Deleting duplicates in the list
for i in range(len(mc)): #Writting Domain names/Companies to txt file
    write_to_csv(my_clutter[i],"My_clutter.txt")

print("The list of your probable companies is in the file My_cluttter.txt")
