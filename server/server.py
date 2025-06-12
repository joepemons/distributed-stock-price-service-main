import hashlib
import json
import os
import rpyc
from rpyc.utils.server import ThreadedServer
from requests.exceptions import RequestException
from datetime import datetime
import yfinance as yf


RESET_COLOR = '\033[0m'

@rpyc.service
class StockPriceServerService(rpyc.Service):
    def __init__(self):
        # Initialize server with essential configurations.
        self.server_name = os.getenv("SERVER_NAME", "Unknown")
        self.color_code = self.determine_color_code(self.server_name)
        print(f"[{self.get_time()}] Server \033[38;5;{self.color_code}m{self.server_name}{RESET_COLOR} is running")
        super().__init__()
    
    def get_time(self):
        # Get current time
        return datetime.now().strftime("%H:%M:%S")

    def determine_color_code(self, hostname):
        """
        Determine a color code based on the MD5 hash of the input hostname.
        """
        hash_val = hashlib.md5(hostname.encode()).hexdigest()
        color_number = int(hash_val, 16) % 256
        return color_number

    @rpyc.exposed
    def get_price(self, symbol):
        """
        Exposed method that returns the current price of the symbol
        """
        print(f"[{self.get_time()}] Client request to Server \033[38;5;{self.color_code}m{self.server_name}{RESET_COLOR}: {symbol}")
        price = self.get_api_price(symbol) 

        # Preparing result dictionary with required information.
        result = {
            "symbol": symbol,
            "price": price,
            "server_name": self.server_name
        }

        return json.dumps(result)

    def get_api_price(self, symbol):
        """
        Access API to get the price of the symbol
        """
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="1d")
            price = history['Close'].iloc[-1] if not history.empty else "No data available"
        except RequestException as e:
            # Handle network or connection errors
            price = f"ERROR: Failed to connect to the Yahoo Finance API. {str(e)}"
        except Exception as e:
            # Handle other exceptions
            price = f"ERROR: {str(e)}"

        return price
    
if __name__ == "__main__":
    # Start the server on the specified port.
    server = ThreadedServer(StockPriceServerService(), port=5000)
    server.start()