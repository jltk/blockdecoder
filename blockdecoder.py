#!/usr/bin/env python
"""
blockdecoder.py

Convert Bitcoin block data to ASCII format.
"""
import sys
import urllib.request
import threading
import itertools
import time

def fetch_block_data(block_hash):
    """
    Fetches block data from the blockchain in hexadecimal format.
    """
    try:
        with urllib.request.urlopen(f"https://blockchain.info/rawblock/{block_hash}?format=hex") as response:
            html = response.read()
            return html.decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    return None

def decode_to_ascii(hex_data):
    """
    Converts hexadecimal block data to an ASCII representation.
    """
    try:
        ascii_block = bytes.fromhex(hex_data).decode("utf-8", "ignore")
        return ascii_block
    except ValueError as e:
        print(f"Decoding Error: {e}")
    return None

def show_loading_animation():
    """
    Displays a loading animation while fetching and processing data.
    """
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_loading:
            break
        sys.stdout.write(f'\rLoading {c}')
        sys.stdout.flush()
        time.sleep(0.1)

def output_data(ascii_block, to_file):
    """
    Outputs the ASCII block data either to a text file or the terminal.
    """
    if to_file:
        try:
            with open('block_ascii_output.txt', 'w', encoding='utf-8') as f:
                f.write(ascii_block)
            print("Output written to block_ascii_output.txt")
        except IOError as e:
            print(f"File Error: {e}")
    else:
        print("\n\033[1mConverted to ASCII:\033[0m\n" + ascii_block)

def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python script.py <block_hash>")
        sys.exit(1)

    block_hash = args[0]
    print(f"\033[1mBlock: \033[0m{block_hash}")

    choice = input("Do you want to save the output to a text file? (y/n): ").strip().lower()
    to_file = choice == 'y'

    global stop_loading
    stop_loading = False
    loading_thread = threading.Thread(target=show_loading_animation)
    loading_thread.start()

    hex_data = fetch_block_data(block_hash)
    stop_loading = True
    loading_thread.join()

    if hex_data:
        ascii_block = decode_to_ascii(hex_data)
        if ascii_block:
            output_data(ascii_block, to_file)
    else:
        print("Failed to fetch or decode block data.")

if __name__ == "__main__":
    main()
