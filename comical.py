import requests
import os
from tqdm import tqdm
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama for colored terminal output
init(autoreset=True)

# URL for map data
MAP_DATA_URL = "https://static.resquared.studio/maps/map_index.json"

# Function to print "SPARGAT" using ASCII art in large red letters
def print_spargat():
    ascii_art = pyfiglet.figlet_format("SPARGAT")
    print(f"{Fore.RED}{Style.BRIGHT}{ascii_art}{Style.RESET_ALL}")

# Function to download a file with a progress bar
def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('Content-Length', 0))  # Get file size in bytes
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                # Use tqdm to show the download progress
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename, colour='green') as progress_bar:
                    for chunk in response.iter_content(1024):
                        if chunk:  # Write each chunk of data to the file
                            f.write(chunk)
                            progress_bar.update(len(chunk))
            print(f"{Fore.GREEN}Downloaded: {filename} - {total_size / (1024 * 1024):.2f} MB")
        else:
            print(f"{Fore.RED}Error downloading {filename} from {url}")
    except Exception as e:
        print(f"{Fore.RED}Download error for {filename}: {e}")

# Function to process the map data and download files
def process_maps(map_data):
    for map_entry in map_data:
        map_id = map_entry.get('mapId', 'unknown')
        
        # Download the .zip file if the URL is not empty
        map_zip_url = map_entry.get('mapZipUrl', '')
        if map_zip_url:
            map_zip_filename = os.path.basename(map_zip_url)
            download_file(map_zip_url, map_zip_filename)
        
        # Download the map icon (.png) if the URL is not empty
        map_icon_url = map_entry.get('mapIcon', '')
        if map_icon_url:
            map_icon_filename = os.path.basename(map_icon_url)
            download_file(map_icon_url, map_icon_filename)

# Main function to fetch map data and initiate downloads
def main():
    print_spargat()  # Display "SPARGAT" in large ASCII letters
    try:
        response = requests.get(MAP_DATA_URL)
        if response.status_code == 200:
            map_data = response.json()
            process_maps(map_data)
        else:
            print(f"{Fore.RED}Error fetching map data, status code: {response.status_code}")
    except Exception as e:
        print(f"{Fore.RED}Error fetching data: {e}")

if __name__ == "__main__":
    main()
