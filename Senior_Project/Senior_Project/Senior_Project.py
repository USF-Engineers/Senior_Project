import os
import subprocess
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from threading import Thread
from time import sleep
import atexit
import sys
import json
import sqlite3
from sqlite3 import Error



database = ".\\Twilio.db"


account_sid = "AC3516d00fc578410654c5a771d4558d1c"
token = "b0bbba38d5d53bf6cf6d692301b52369"
pn_sid = "PN71239c86b7fc6b418d05d208e04fc79e"
ngrokPath = "C:\\Users\\wade2\\Downloads\\ngrok"

client = Client(account_sid, token)
app = Flask(__name__)



class PhoneClient:
    def __init__(self, a):
       pass
    def SendMessage(self, message, toNumber="17273247781", fromNumber="+18139579643"):
        client.messages.create(to = toNumber,
            from_ = fromNumber,
            body = message)


        pass
    pass

#Create connection to db
def CreateConnection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
conn = CreateConnection(database)

#This data is going to be in the database


#Messages
def Hello(message):
   return SelectContent(conn, "Hello", message)

def Question(message):
    return SelectContent(conn, "Question", message)





#Reply to messages
def GetReply(message):
    if(Hello(message)):
        return "Hello how are you"
    if(Question(message)):
        return "What is your question?"


    return "No reply yet"









#Ngrok methods
#Call ngrok
def StartNgrok():
    os.system("start cmd /c " + ngrokPath + "  http 5000")

    pass

#Get the random ngrok url
def GetUrl():

    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

    with open('tunnels.json') as data_file:    
        datajson = json.load(data_file)

    for i in datajson['tunnels']:
        return i['public_url'] + "\n"
    return ""


#Set the webhook
def WebHook():
    #Phone calls
    curl =  'curl -XPOST https://api.twilio.com/2010-04-01/Accounts/' + account_sid + '/IncomingPhoneNumbers/' + pn_sid + '.json --data-urlencode "VoiceUrl=' + GetUrl().strip() + '/voice" -u ' + account_sid + ':' + token
    os.system(curl)
    #Sms
    curl =  'curl -XPOST https://api.twilio.com/2010-04-01/Accounts/' + account_sid + '/IncomingPhoneNumbers/' + pn_sid + '.json --data-urlencode "SmsUrl=' + GetUrl().strip() + '/sms" -u ' + account_sid + ':' + token
    os.system(curl)
    pass



@app.route("/sms", methods=['GET', 'POST'])
def IncomingSms():
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    resp.message(GetReply(body))

    return str(resp)


#Kill the ngrok process on close
@atexit.register
def Kill():
    os.system("start cmd /c taskkill /f /IM ngrok.exe")
    pass






#Database methods

#Select content of a given task
def SelectContent(conn, task, question):
   
    cur = conn.cursor()
    cur.execute("SELECT Content FROM Questions where Task=?", (task,))
 
    rows = cur.fetchall()
 
    for row in rows:
        if(StripTask(row) == question):
            return True
    return False

#Strip format of content
def StripTask(content):
    ret = ""
    for letter in content:
        if(letter != ')' or letter !="'" or letter != '('):
            ret += letter
    return ret





if __name__ == "__main__":
    
    thread = Thread(target = StartNgrok)
    thread.start()
    
    sleep(3)
    WebHook()
     
    app.run()
  
      
    
    
    
    







#Auto reply
#@app.route("/sms", methods=['GET', 'POST'])
#def sms_ahoy_reply():
#    """Respond to incoming messages with a friendly SMS."""
#    # Start our response
#    resp = MessagingResponse()

#    # Add a message
#    resp.message("Ahoy! Thanks so much for your message.")

#    return str(resp)
##return_code = subprocess.call("C:\\Users\\wade2\\Downloads\\ngrok http 5000", shell=True) 
#if __name__ == "__main__":
#    app.run(debug=True)
