import pymongo
import datetime
import time

def get_menu_data_from_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["wapimenu"]
    for data in mycol.find():
        return (data["menu_data"])
"""
def read_user_messages():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["hellotesting"]
    mylist = []
    for data in mycol.find():
        mylist.append(data)
    return mylist
"""
def read_user_messages():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["userdata"]
    l1 = []
    for data in mycol.find():
        l1.append (data)
        #print(data["user"],data ["message"],data["message"].count("hi"))
    return(l1)

def store_user_messages(phone_no, msg, con,time):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["hellotesting"]
    mydict = {"user":phone_no, "message":[msg], "context":[con], "time":time}
    x = mycol.insert_one(mydict)
    print ("data is stored")
    return 


def knowing_datetime(data):
    dt = datetime.datetime.now()
    time24 = dt -datetime.timedelta(hours = 24)
    datalist = []
    for user in data:
       # print(user["time"])
        if (user["time"] > time24 and user ["time"] <dt):
           # print(user)
            datalist.append(user)
        

    #print(datetime.datetime.now() )
    return(datalist)

def getting_repeted_user(date):
    print(date[0])
    count = 0
    repuserlist = []
    for i in range (0,len(date)):
        for j in range(i+1,len(date)):
            if (date[i]["user"] == date[j]["user"]):
                count = count+1
                #print(date[i]["user"])
                if date[i]["user"] not in repuserlist:
                    repuserlist.append(date[i]["user"])
    repuserlist.append(count)
    print(count)
    print(repuserlist)
            #return(date[i]["user"],count)
    return

def update_user_messages_db( phone_no, message, context):
    #print ("time:",current_time)
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["hellotesting"]
    myquery = {"user":phone_no}
    new_values = {"$push":{"message":message, "context":context},"$set":{ "time": datetime.datetime.now()}}
    mycol.update_one(myquery, new_values)
    print ("The new data is updated")
    return 
                

def main():
 
    data =read_user_messages ()
    print(len(data))
    lastelement = data[len(data)-1]
    lastcontext =  lastelement["context"][len(lastelement["context"])-1]
   # context = lastelement["context"]
    #for i in range (0,len(data)):
    print(lastcontext)
    #for key in data:
        #print(key)
    #user_details = [key for key in data ]
    #print(user_details[0])

    #print(data)
    #date = knowing_datetime(data)
    #userslist =  getting_repeted_user(date)
    data1=store_user_messages("52364125","hello","main_menu","datetime.datetime.now()")
    data2 = update_user_messages_db("52364125","hello","c_menu")




if __name__ == "__main__":
    main()
