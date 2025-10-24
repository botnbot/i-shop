from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import mimetypes

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """
    Класс для обработки входящих GET-запросов.
    """

    def do_GET(self):
        # Определяем путь к файлу
        if self.path == "/":
            filepath = "contacts.html"
        else:
            filepath = self.path.lstrip("/")

        # Проверяем, существует ли файл
        if os.path.exists(filepath) and os.path.isfile(filepath):
            # Определяем MIME-тип
            mime_type, _ = mimetypes.guess_type(filepath)
            if mime_type is None:
                mime_type = "application/octet-stream"

            # Отправляем файл
            self.send_response(200)
            self.send_header("Content-type", f"{mime_type}; charset=utf-8")
            self.end_headers()

            with open(filepath, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, f"File not found: {filepath}")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер запущен: http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Сервер остановлен.")
