from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import LocationService

class RequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    if self.path == '/find-drone-location':
      content_length = int(self.headers.get('Content-Length', 0))
      body = self.rfile.read(content_length)
      data = json.loads(body)
      query = data.get('query', '')
      service = LocationService()

      result = service.find_location(query)
      
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
      self.wfile.write(json.dumps(result).encode())
    else:
      self.send_response(404)
      self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print(f'Serving on port {port}')
  httpd.serve_forever()

if __name__ == '__main__':
  run()