import pymongo
import datetime

msg_list = []

def get_menu_data_from_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["wapimenu"]
    for data in mycol.find():
        return (data["menu_data"])

def read_user_messages():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["userdata"]
    mylist = []
    for data in mycol.find():
        mylist.append(data)
    return mylist

def store_user_messages(phone_no, msg, context):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["userdata"]
    mydict = {"user":phone_no, "message":[msg], "context":context, "time": datetime.datetime.now()}
    x = mycol.insert_one(mydict)
    print ("data is stored")
    return 

def update_user_messages_db(user_id, phone_no, message, context):
    #print ("time:",current_time)
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["userdata"]
    myquery = {"user":phone_no}
    new_values = {"$push":{"message":message}, "$set":{"context":context, "time": datetime.datetime.now()}}
    mycol.update_one(myquery, new_values)
    print ("The new data is updated")
    return 

def update_user_context(user_id):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["userdata"]
    myquery = {"_id":user_id}
    new_values = {"$set":{"context":"none"}}
    mycol.update_one(myquery, new_values)
    return

