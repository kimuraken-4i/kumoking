from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import FieldStorage
with open('index.html', mode='r')as f:
    index=f.read()

class HelloServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(index.encode('utf-8'))
        return  
    def do_POST(self):
        form=FieldStrage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'}
        )
        res=form['textfield'].value
        self.send_response(200)
        self.end_headers()
        html=next.format(
            message='you need: '+res,
            data=form
        )
        self.wfile.write(html.encode('utf-8'))
        return 
    
    def index(self):
        self.send_response(200)
        self.end_headers()
        html=index.format(
            title="Hello",
            message="Form送信"
        )  
        self.wfile.write(html.encode('utf-8'))
        return 


server=  HTTPServer(('',8000), HelloServerHandler)
server.serve_forever()