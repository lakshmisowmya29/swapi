"""Import necessary modules"""
import datetime
import time
from multiprocessing import Process
import emoji
from flask import Flask, request
from kaleyra_reply import text_response, media_response
from functions import read_user_messages, store_user_messages, update_user_messages_db, get_menu_data_from_db, update_user_context
import os
from setproctitle import setproctitle

menu_data = "none"
context = "none"
current_time = datetime.datetime.now()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def kaleyra_response():
    """This function is defined to get the user details from kaleyra"""
    user_details = request.args.get("from")
    print(user_details)
    user_msg = request.args.get("body")
    print(user_msg)
    msg = user_msg.lower()
    print (msg)
    response = fetch_reply(user_details, msg)
    for msg in response:
        #print ("msg:",msg)
        if msg["type"] == "text":
            text_response(user_details, msg["reply"])
        if msg["type"] == "media":
            res = msg["reply"].rstrip('\n')
            media_response(user_details, res)
        time.sleep(2)
    return str(response)

def get_menu_items(context):
    """This function is defined to get menu items from the database"""
    msg1 = ""
    msg1_type = ""
    msg2 = ""
    msg2_type = ""
    reply = []
    for row in menu_data:
        if (row["menu_id"] == context and row["icon"] != "none" and row["message_order"] == "1"):
            msg1 += f'{row["menu_items"]} {emoji.emojize(row["icon"])}\n'
            msg1_type += row["message_type"]
        if (row["menu_id"] == context and row["icon"] == "none" and row["message_order"] == "1"):
            msg1 += f'{row["menu_items"]}\n'
            msg1_type += row["message_type"]
        if (row["menu_id"] == context and row["icon"] != "none" and row["message_order"] == "2"):
            msg2 += f'{row["menu_items"]} {emoji.emojize(row["icon"])}\n'
            msg2_type += row["message_type"]
        if (row["menu_id"] == context and row["icon"] == "none" and row["message_order"] == "2"):
            msg2 += f'{row["menu_items"]}\n'
            msg2_type += row["message_type"]

    menu1 = {"reply":msg1, "type":msg1_type}
    menu2 = {"reply":msg2, "type":msg2_type}
    reply.append(menu1)
    reply.append(menu2)
    return reply

def set_menu_context(user_prev_context, msg):
    """Function to set the user context"""
    for row in menu_data:
        if row["menu_id"] == user_prev_context:
            if (str(row["order1"]) == msg or str(row["order2"]) == msg):
                context = row["context"]
                return context

def check_user_msg(user_prev_context, msg):
    """Function to check the user message"""
    for row in menu_data:
        if row["menu_id"] == user_prev_context:
            if (str(row["order1"]) == msg or str(row["order2"]) == msg):
                return True
    else:
        return "Sorry, I didn't understand what you just said please check your message\n\nif you're struck,\ntype *menu* to get the main-menu"

def fetch_reply(phone_no, msg):
    """This function is defined to send the reply back to the kaleyra response"""
    reply = []
    global menu_data
    menu_data = get_menu_data_from_db()
    global context
    user_data = read_user_messages()
    if not any(user["user"] == phone_no for user in user_data):
        context = "main_menu"
        store_user_messages(phone_no, msg, context)
        reply = get_menu_items(context)
        return reply

    user_details = [key for key in user_data if key["user"] == phone_no]
    user_id = user_details[0]["_id"]
    user_prev_context = user_details[0]["context"][-1]

    if user_prev_context == "none":
        context = "main_menu"
        update_user_messages_db(user_id, phone_no, msg, context)
        reply = get_menu_items(context)
        return reply

    if msg == "menu":
        context = "main_menu"
        update_user_messages_db(user_id, phone_no, msg, context)
        reply = get_menu_items(context)
        return reply

    user_msg = check_user_msg(user_prev_context, msg)
    if user_msg == True:
        context = set_menu_context(user_prev_context, msg)
        update_user_messages_db(user_id, phone_no, msg, context)
        reply = get_menu_items(context)
        return reply
    else:
        msg = {"reply":user_msg, "type":"text"}
        reply.append(msg)
        return reply

def user_data_storing():
    count = 0
    setproctitle("UCMonitor")
    """Function is used to set the user context to none after the user time-out"""
    while True:
        print(f"{count}.User actvitiy monitoring service pid :{os.getpid()}")
        data = read_user_messages()
        for user in data:
            user_id = user["_id"]
            phone_no = user["user"]
            context = user["context"][-1]
            time_difference = datetime.datetime.now() - user["time"]
            minutes_difference = (time_difference.seconds)/60
            time.sleep(3)
            print (f'{phone_no}: {minutes_difference}')
            if (minutes_difference > 3 and minutes_difference<3.2):
                print (minutes_difference)
                res = "since we have not recieved any response, we are closing the session, Thank you for contacting us."
                text_response(phone_no, res)
                #data = update_user_context(user_id,context)
        time.sleep(5)
        count += 1
    return

def main():
    """Main function is used to call all the functions"""
    print(f"Parent pid :{os.getpid()}")
    setproctitle("wapiWebServer")
    
    proc = Process(target=user_data_storing)
    proc.start()

    app.run(debug=True)
    return

if __name__ == '__main__':
    main()
