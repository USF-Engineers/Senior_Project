import os
import subprocess
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from threading import Thread

account_sid = "AC3516d00fc578410654c5a771d4558d1c"
token = "b0bbba38d5d53bf6cf6d692301b52369"

client = Client(account_sid, token)
app = Flask(__name__)


class PhoneClient:
    def __init__(self, a):
       pass
    def SendMessage(self, message, toNumber="17273247781", fromNumber = "+18139579643"):
        client.messages.create(
            to = toNumber,
            from_ = fromNumber,
            body = message
            )


def StartNgrok():
    return_code = subprocess.call("C:\\Users\\wade2\\Downloads\\ngrok http 5000", shell=True) 
    print("here")
    print(return_code)


    pass

#This data is going to be in the database

#Messages
def Hello(message):
    message = message.strip().lower()
    return {
        "hi": True,
        "hello": True,
        "hey": True

    }.get(message, False) 

def Question(message):
    message = message.strip().lower()
    return {
        "i have a question": True,
        "i have a question.": True

    }.get(message, False) 




#End of messages


#Reply to messages
def GetReply(message):
    if(Hello(message)):
        return "Hello how are you"
    if(Question(message)):
        return "What is your question?"





    return "No reply yet"


#End of reply




@app.route("/sms", methods=['GET', 'POST'])
def IncomingSms():
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    resp.message(GetReply(body))

    print("test")
    thread = threading.Thread(target=StartNgrok, args=[])
    thread.start()

    return str(resp)




def main():
    print("test")
    thread = threading.Thread(target=StartNgrok, args=[])
    thread.start()


if __name__ == "__main__":
    app.run(debug=True)







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
