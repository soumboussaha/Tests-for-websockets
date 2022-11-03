from http.server import BaseHTTPRequestHandler, HTTPServer # python3
class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type','multipart/mixed; boundary="boundary"')
        self.send_header('Request-Taint','1')
        self.end_headers()

    def _set_body(self):
        self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>","utf-8"))
        self.wfile.write(bytes("<body><p>'Name':'Data', 'non-private' : 'Data' , 'surname':'Data'<p>","utf-8"))
        taintdetails="1555-1134"
        self.wfile.write(bytes("--boudary content-Type: application/"+taintdetails+"--boundry","utf-8"))
        self.wfile.close()

    def do_GET(self):
        #get body content
        content_len = int(self.headers.get('Content-Length'))
        getBody=str(self.rfile.read(content_len))
        #split the string and print it 
        d = dict(x.split("=") for x in getBody.split("&")) 
        for k, v in d.items():
            print(k, v)   
        #set Body/headers and respond

        self._set_headers()
        self._set_body()

    def do_POST(self):
        #Reads post request body    
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        self.wfile.write(bytes("received post request:<br>{}".format(post_body)))
        self._set_headers()

    def do_PUT(self):
        self.do_POST()

host = ''
port = 8081
HTTPServer((host, port), HandleRequests).serve_forever()
