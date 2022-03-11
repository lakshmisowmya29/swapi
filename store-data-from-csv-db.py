import csv
import json
import pymongo

def csv_to_json(fname):
    data_list = []
    with open(fname) as fd:
        data = csv.DictReader(fd)
        for row in data:
            data_list.append(row)
        print (data_list)
    return data_list

def store_menu_data_in_db(menu_data):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["aurawapimenu"]
    mycol = mydb["wapimenu"]
    mydict = {"menu_data":menu_data}
    x = mycol.insert_one(mydict)
    print ("data is stored")
    return 

def main():
    fname = "aura_menu_final.csv"
    menu_data = csv_to_json(fname)
    print (type(menu_data))
    store_menu_data_in_db(menu_data)

if __name__ == "__main__":
    main()
