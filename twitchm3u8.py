# Import necessary libraries
import subprocess  # For executing command-line commands
import streamlink  # For retrieving video streams from the M3U8 URL

# Display a header message
print(r"""
 _         _ _       _         ___     ___ 
| |_ _ _ _|_| |_ ___| |_ _____|_  |_ _| . |
|  _| | | | |  _|  _|   |     |_  | | | . |
|_| |_____|_|_| |___|_|_|_|_|_|___|___|___| by TenPassion

""")

# Configuration file name to store the Twitch stream key
config_file = "twitch_config.txt"

# Function to get the Twitch stream key from the configuration file
def get_twitch_stream_key():
    try:
        with open(config_file, "r") as file:
            return file.readline().strip()
    except FileNotFoundError:
        return None

# Function to save the Twitch stream key to the configuration file
def save_twitch_stream_key(stream_key):
    with open(config_file, "w") as file:
        file.write(stream_key)

# Function to ask the user for the Twitch stream key
def ask_for_stream_key():
    stream_key = input("Please enter your Twitch stream key: ")
    save_twitch_stream_key(stream_key)
    return stream_key

# Function to get the best stream link from the M3U8 URL
def get_best_stream_link(m3u8_url):
    try:
        streams = streamlink.streams(m3u8_url)
        best_stream = streams['best']
        return best_stream.url
    except Exception as e:
        print(f"Error while processing M3U8 URL {e}")
        return None

def main():
    # Get the saved Twitch stream key, if available
    stored_stream_key = get_twitch_stream_key()
    
    if stored_stream_key is None:
        print("No Twitch stream key saved.")
        stream_key = ask_for_stream_key()  # Ask the user to input the key
    else:
        use_stored_key = input(f"Use the last Twitch stream key? (y/n): ")
        if use_stored_key.lower() == 'y':
            stream_key = stored_stream_key
        else:
            stream_key = ask_for_stream_key()  # Ask the user to input a new key

    # Ask the user to enter the M3U8 stream URL
    m3u8_url = input("Please enter the M3U8 stream URL: ")

    input("Press Enter to Start...")  # Wait for user input to start streaming

    # Get the best stream link from the M3U8 URL
    best_stream_url = get_best_stream_link(m3u8_url)

    if best_stream_url is None:
        m3u8_url = input("Please enter a valid M3U8 stream URL: ")
        best_stream_url = get_best_stream_link(m3u8_url)

    # Construct the FFmpeg command for streaming to Twitch
    ffmpeg_cmd = [
        'ffmpeg',  # FFmpeg command
        '-i', best_stream_url,  # Input: Best stream link
        '-c:v', 'libx264',  # Video codec: libx264
        '-b:v', '2M',  # Video bitrate: 2 Mbps
        '-c:a', 'aac',  # Audio codec: AAC
        '-f', 'flv',  # Output format: FLV (Flash Video)
        f'rtmp://live.twitch.tv/app/{stream_key}'  # Twitch streaming URL
    ]

    try:
        # Execute the FFmpeg command to start streaming
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during streaming: {e}")

if __name__ == "__main__":
    main()  # Call the main function when the script is executed
