from datetime import datetime
import time
import rpyc
import sys
import json
import socket
import hashlib

# Constants for terminal color codes.
RED = '\033[91m'
RESET_COLOR = '\033[0m'


def hash_hostname(hostname):
    """
    Hash the hostname using MD5, returning the hex digest.
    """
    return hashlib.md5(hostname.encode()).hexdigest()


def determine_color_code(hostname):
    """
    Determine a color code based on the hashed hostname.
    """
    hash_val = hash_hostname(hostname)
    color_number = int(hash_val, 16) % 256
    return color_number


def get_stock_prices(symbols, max_retries=3):
    """
    Fetche stock prices with retry logic in case of failure.
    """
    results = []
    server_name = ""

    # Iterating through each symbol to fetch its price.
    for symbol in symbols:
        start_time = datetime.now()
        retries = 0

        # Retrying in case of failure up to max_retries.
        while retries < max_retries:
            try:
                conn = rpyc.connect("server", 5000)
                # conn = rpyc.connect("10.105.181.166", 5000)
                stock_service = conn.root

                # Getting the price for each symbol
                response_json = stock_service.get_price(symbol)
                response_data = json.loads(response_json)

                # Collecting the response data
                end_time = datetime.now()
                time_taken = (end_time - start_time).total_seconds()

                results.append({
                    'symbol': symbol,
                    'price': response_data['price'],
                    'server_name': response_data.get('server_name', 'Unknown'),
                    'client_time': round(time_taken, 2)
                })

                conn.close()
                break  # Exiting the retry loop in case of success.
            except Exception as e:
                retries += 1
                print(f"Error fetching price for {symbol} from \033[38;5;{determine_color_code(hostname)}m{hostname}{RESET_COLOR} -> {response_data.get('server_name', 'Unknown')}. (Retry {retries}/{max_retries}): {e}")
    
            
    return results

# Comman to run the Client from VS Code
# sys.argv=["client.py", "TSLA", "BAC", "PLTR", "AMD"]

if __name__ == "__main__":
    # Entry point, fetching prices for symbols given as command-line arguments.
    if len(sys.argv) < 2:
        print("Usage: python client.py SYMBOL1 SYMBOL2 ...")
        sys.exit(1)

    hostname = socket.gethostname()
    color_code = determine_color_code(hostname)

    symbols = sys.argv[1:]
    results = get_stock_prices(symbols)
    
    # Print the prices of the symbols with the corresponding server that handled that symbol
    if results:
        for result in results:
            print(f"\033[38;5;{color_code}m{hostname}{RESET_COLOR} -> \033[38;5;{determine_color_code(result['server_name'])}m{result['server_name']}{RESET_COLOR} ({result['client_time']} sec): The price of {result['symbol']} is: {result['price']}")

    else:
        print("No price data received.")