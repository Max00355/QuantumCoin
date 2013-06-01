import json
import landerdb
from hashlib import sha512
from get_diff import difficulty

def check(data, obj, conn):
    """{"cmd":"check", "addr":str, "hash":str, "plain":str}"""
    coins = landerdb.Connect("coins.db")
    coins = coins.find("coins", "all")
    check = sha512(data['plain']).hexdigest() == data['hash']
    exists = False
    exist = {"addr":data['addr'], 'hash':data['hash']}
    if exist in coins:
        exists = True 
    if not exists and check:
        if data['hash'].startswith("1"*difficulty()):
            coins.insert({"addr":data['addr'], "hash":data['hash']})
            obj.send(json.dumps({"message":"Success"}))
        else:
            obj.send(json.dumps({"message":"Failed"}))
    else:
        obj.send(json.dumps({"message":"Failed"}))

    obj.close()
