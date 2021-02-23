from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 1234

devices = {}
test_devices = {"device1" : "1", "device2" : "0", "device3" : "0"}
last_request_time = {"device1" : "0", "device2" : "0", "device3" : "0"}

class MyServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return
    def do_GET(self):
        path = str(self.path)
        resp = self.parceReq(path)
        if(path[1:2] == "!"):
            temp = path.find("/", 2)
            reqDevice = path[2:temp]
            print(reqDevice)
            if(reqDevice in devices):
                last_request_time[reqDevice] = time.time()
                resp = self.parceReq(path[temp:])
                print(last_request_time)
            else:
                resp = "DEVICE_REQUEST_MADE_FROM_NOT_RECOGNIZED"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", str(len(resp)))
        self.end_headers()

        self.wfile.write(bytes(resp, "utf-8"))
        print("GETResp:" + resp)
    
    def do_POST(self):
        path = str(self.path)
        resp = "NO_POST_MATCH"
        print("\nPOSTReq:" + path)
        if(path[:5] == "/new/"):
            newDevName = path[5:]
            if(newDevName in devices):
                resp = "DEVICE_ALREADY_EXISTS"
            else:
                devices[newDevName] = "0"
                print(devices)
                resp = "NEW_DEVICE_CREATED:" + newDevName
        
        if(path[:5] == "/set/"):
            i0 = path.find("/", 6)
            setDevName = path[5:i0]
            if(setDevName in devices):
                val = path[i0+1:]
                devices[setDevName] = val
                print(devices)
                resp = "SET:" + setDevName + ":TO:" +val
            else:
                resp = "DEVICE_DOESNT_EXIST"

        if(path[:8] == "/delete/"):
            i0 = path.find("/", 6) + 1
            setDevName = path[i0:]
            print(setDevName)
            resp = "DEVICE_DOESNT_EXIST_TO_DELETE"
            if(setDevName in devices):
                del devices[setDevName] 
                resp = "DELETED:" + setDevName

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", str(len(resp)))
        self.end_headers()

        self.wfile.write(bytes(resp, "utf-8"))
        print("POSTResp:" + resp)

    def parceReq(self, path):
        resp = "ERROR_NO_PATH_MATCH"
        print("\nGETReq:"+path)
        if(path == "/"):
            resp = "ServerIsAlive"
        if(path == "/all"):
            resp = "{"
            for dev in devices:
                resp = resp + dev + ":" + devices[dev] + ","
            resp = resp[:-1] + "}"

        if(path[1:] in devices):
            resp = "{" + devices[path[1:]] + "}"

        return resp

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    devices = test_devices #remove in  prod
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")