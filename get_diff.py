import json
import landerdb


def difficulty():
    coins = landerdb.Connect("coins.db")
    coins = coins.find("coins", "all")
    if coins:
        return len(coins) / 205000 + 7  
    if not coins:
        return 7

def get_diff(data, obj, conn):
    obj.send(json.dumps({"difficulty":difficulty()}))
    obj.close()
