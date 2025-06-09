from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes

hostName = "localhost"
serverPort = 8080

path = os.path.abspath(__file__)
src_path = os.path.dirname(path)
base_dir = os.path.dirname(src_path)
contacts_path = os.path.join(base_dir, "contacts.html")


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        requested_path = self.path
        if requested_path == "/":
            requested_path = "/contacts.html"
        filepath = os.path.join(base_dir, requested_path[1:])

        if os.path.exists(filepath) and os.path.isfile(filepath):
            mimetype, _ = mimetypes.guess_type(filepath)

            if mimetype:
                self.send_response(200)
                self.send_header("Content-Type", mimetype)
                self.end_headers()
                with open(filepath, "rb") as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(415)
                self.end_headers()
                self.wfile.write(
                    b"Unsupported media type"
                )

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")