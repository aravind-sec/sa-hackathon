import webview
import threading
from dashboard import app


def run_flask():
    app.run(port=5001)


if __name__ == "__main__":
    threading.Thread(target=run_flask).start()

    webview.create_window("API Shield Dashboard", "http://127.0.0.1:5001")
    webview.start()