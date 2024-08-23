#!/usr/bin/env python
"""
blockdecoder.py

Convert Bitcoin block data to ASCII format.
"""
import sys
import urllib.request
import threading
import time

def fetch_block_data(block_hash):
    """Fetch block data from blockchain.info as a hex string."""
    url = f"https://blockchain.info/rawblock/{block_hash}?format=hex"
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        sys.exit(f"Error retrieving block data: {e}")

def hex_to_ascii(hex_data):
    """Convert hex string to ASCII, ignoring errors."""
    return bytes.fromhex(hex_data).decode("utf-8", "ignore")

def loading_animation():
    """Display a loading animation."""
    while not done_loading:
        for char in "/—\\|":
            sys.stdout.write(f'\rLoading {char}')
            sys.stdout.flush()
            time.sleep(0.1)

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python script.py <block_hash>")

    block_hash = sys.argv[1]
    output_choice = input("(d)isplay or (w)rite to file? [d/w]: ").strip().lower()
    if output_choice not in ['d', 'w']:
        sys.exit("Invalid choice. Please select 'd' or 'w'.")

    global done_loading
    done_loading = False
    threading.Thread(target=loading_animation).start()

    raw_block = fetch_block_data(block_hash)
    ascii_block = hex_to_ascii(raw_block)

    done_loading = True
    sys.stdout.write('\rDone!            \n')
    sys.stdout.flush()

    if output_choice == 'd':
        print("\nWarning: Potentially large output ahead! Consider writing to file.\n")
        input("Press Enter to continue or CTRL+C to abort...")
        print(f"\n\033[1mBlock: {block_hash}\033[0m\n{ascii_block}")
    else:
        with open(f"{block_hash}_output.txt", 'w', encoding='utf-8') as f:
            f.write(ascii_block)
        print(f"\nOutput written to {block_hash}_output.txt")

if __name__ == "__main__":
    main()
