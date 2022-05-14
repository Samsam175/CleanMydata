from CleanMydata import *
Common_email_services=[]
Companies=[]

Companies,Common_email_services=impor()


print(Common_email_services)
my_clutter=[] #Companies users are subed to

my_clutter_readable=[]

Subjects,Senders = get_mails()


n=len(Senders)
print(Senders)


for i in range(n):
    send=Senders[i]
    subj=Subjects[i]
    if isitacompany(send)==True :
        add_to_clutter(send,subj)

open('My_clutter.txt', 'w').close()

for i in range(len(my_clutter)):
    write_to_csv(my_clutter[i],"My_clutter.txt")

print("The list of your probable companies is in the file My_cluttter.txt")
