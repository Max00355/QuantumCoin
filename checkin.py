import landerdb

def checkin(data, obj, conn):
    print conn[0], "checked in"
    addr = data['addr']
    db = landerdb.Connect("nodes.db")
    db.insert("nodes", {conn[0]:5554, 'addr':addr})
    obj.close()
