import http.server
import socketserver
import webbrowser
import json
import csv

PORT = 8000

class TraceRequestHandler(http.server.CGIHTTPRequestHandler):
    fields = ["session", "ts", "cat", "action", "label", "details"]
    def __init__(self, *args, **kwargs):
        fname = 'trace.csv'
        csvfile = open(fname, 'a')
        self._csvwriter = csv.writer(csvfile)
        super(TraceRequestHandler, self).__init__(*args, **kwargs)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def log_request(self, code='-', size='-'):
        pass

    def write_csv(self, js):
        events = json.loads(js)
        for evt in events:
            line = []
            for field in self.fields:
                if field in evt:
                    line.append(str(evt[field]))
                else:
                    line.append('')
            #print(line)
            self._csvwriter.writerow(line)

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self.write_csv(post_data)
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

Handler = TraceRequestHandler

HTTPD = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
webbrowser.open('http://localhost:%s/index.html'%PORT)
HTTPD.serve_forever()
