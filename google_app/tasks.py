from google_app.google_api import GoogleApi
import threading

from test_google_api.settings import INTERVAL_SCRAPING


def start_scrap_spreadsheet() -> None:
    """
    Let's start the process of updating information by interval.
    Set the daemon to true so that it does not survive the main thread
    """

    def loop(done, interval=INTERVAL_SCRAPING):
        while not done.wait(interval):
            GoogleApi().run()

    done = threading.Event()
    threading.Thread(target=loop, args=[done], daemon=True).start()


