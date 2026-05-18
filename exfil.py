from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import datetime
import json

EVENTS_FILE = "/exfil_data/events.json"

def load_events():
    try:
        with open(EVENTS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_event(event_type, message):
    events = load_events()
    events.append({
        "type": event_type,
        "message": message,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f)

class ExfilHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/events':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            events = load_events()
            self.wfile.write(json.dumps(events).encode('utf-8'))
        elif self.path == '/events/clear':
            open(EVENTS_FILE, 'w').write('[]')
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length).decode('utf-8')
        
        if self.path == '/alerte/exfil':
            save_event("exfil", data)
        elif self.path == '/alerte/cowrie':
            save_event("cowrie", data)
        elif self.path == '/alerte/rdp-win11':
            save_event("rdp-win11", data)
        elif self.path == '/alerte/rdp-ad':
            save_event("rdp-ad", data)
        elif self.path == '/alerte':
            save_event("alerte", data)
        else:
            length2 = int(self.headers.get('Content-Length', 0))
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs("/exfil_data", exist_ok=True)
            with open(f"/exfil_data/capture_{timestamp}.txt", 'wb') as f:
                f.write(data.encode('utf-8'))
        
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        print(format % args)

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8080), ExfilHandler).serve_forever()
