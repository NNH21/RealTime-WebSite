import http.server
import socketserver
import urllib.parse
import serial
import threading

# Cấu hình cổng Serial (thay đổi thành cổng của bạn, ví dụ: COM3 trên Windows hoặc /dev/ttyUSB0 trên Linux)
SERIAL_PORT = "COM3"  # Thay đổi thành cổng Serial của bạn
SERIAL_BAUDRATE = 9600

# Kết nối Serial với Arduino
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/update":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            print("Received POST data:", post_data)

            # Gửi dữ liệu qua Serial đến Arduino
            ser.write((post_data + "\n").encode('utf-8'))

            # Gửi phản hồi về client
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Text updated successfully")
        else:
            self.send_response(404)
            self.end_headers()

# Cấu hình server HTTP
PORT = 8000
Handler = MyHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server started at localhost:" + str(PORT))
    httpd.serve_forever()