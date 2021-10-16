import tornado.web
import tornado.ioloop
import json
import time
#from websocket import create_connection
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
dblist = myclient.list_database_names()
if "messagedb" in dblist:
	print("database is exisit")
	print(dblist)
	mydb = myclient["messagedb"]
	mescol = mydb["messagecol"]
	concol = mydb["cliencol"]
	disconcol = mydb["cliendiscol"]
	subtop = mydb["subtop"]
	unsubtop = mydb["unsubtop"]
	othercol = mydb["othercol"]
else:
	print("database is none exisit,created")
	mydb = myclient["messagedb"]
	mescol = mydb["messagecol"]
	concol = mydb["cliencol"]
	disconcol = mydb["cliendiscol"]
	subtop = mydb["subtop"]
	unsubtop = mydb["unsubtop"]
	othercol = mydb["othercol"]

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.request)
        self.write('this is a tornado test app')
    def post(self):
        req_full = self.request.body
        datatype = json.loads(req_full).get('action')
        print(datatype)
        if datatype == 'message_publish':
        	print(req_full)
        	wrdata = json.dumps({**json.loads(req_full),**{"time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}})
        	x = mescol.insert_one(json.loads(wrdata))
        elif datatype == 'client_connected':
        	print(req_full)
        	wrdata = json.dumps({**json.loads(req_full),**{"time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}})
        	x = concol.insert_one(json.loads(wrdata))
        elif datatype == 'client_disconnected':
        	print(req_full)
        	wrdata = json.dumps({**json.loads(req_full),**{"time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}})
        	x = disconcol.insert_one(json.loads(wrdata))
        elif datatype == 	'session_subscribed':
        	print(req_full)
        	wrdata = json.dumps({**json.loads(req_full),**{"time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}})
        	x = subtop.insert_one(json.loads(wrdata))
        elif datatype == 'session_unsubscribed':
        	print(req_full)
        	wrdata = json.dumps({**json.loads(req_full),**{"time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}})
        	x = unsubtop.insert_one(json.loads(wrdata))
        else:
        	print(req_full)
        	wrdata = json.dumps({**json.loads(req_full),**{"time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}})
        	x = subtop.insert_one(json.loads(wrdata))

if __name__ == '__main__':
    app = tornado.web.Application([(r'/',IndexHandler)])
    app.listen(18888)
    tornado.ioloop.IOLoop.current().start()