import os
import pyautogui
import pygetwindow as gw
import time
import pyperclip  # Import the pyperclip module
import pygetwindow
from PIL import ImageGrab
from functools import partial
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# Modify the behavior of ImageGrab.grab to grab screens from all monitors
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

# Function to check if any image in the specified folder is present on the screen
def is_image_present(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            if pyautogui.locateOnScreen(image_path, confidence=.7) is not None:
                return True
    return False

# Function to mute the browser tab
def mute_browser_tab(window):
    try:
        if window.isActive:
            # Activate the browser tab window
            window.activate()
            # Send ALT-1 key combination to mute the tab
            pyautogui.hotkey('alt', '1')
        else:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session.SimpleAudioVolume
                if session.Process and session.Process.name() == browser_process_name:
                    volume.SetMute(1, None)
                    print(f"Muting {browser_name} via pycaw")
                    break
    except pygetwindow.PyGetWindowException as e:
        print("Error occurred while muting browser tab:", e)

# Function to unmute the browser tab
def unmute_browser_tab(window):
    try:
        if window.isActive:
            # Activate the browser tab window
            window.activate()
            # Send ALT-2 key combination to unmute the tab
            pyautogui.hotkey('alt', '2')
        else:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session.SimpleAudioVolume
                if session.Process and session.Process.name() == browser_process_name:
                    volume.SetMute(0, None)
                    print(f"Unmuting {browser_name} via pycaw")
                    break
    except pygetwindow.PyGetWindowException as e:
        print("Error occurred while unmuting browser tab:", e)
        
# Function to get the URL of the browser tab
def get_browser_tab_url():
    # Activate the browser window
    browser_window = gw.getWindowsWithTitle(browser_name)[0]  # Use dynamically obtained browser name
    browser_window.activate()

    # Simulate pressing Ctrl+L to focus the address bar
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(1)  # Add a small delay to ensure the address bar is focused

    # Simulate pressing Ctrl+C to copy the URL
    pyautogui.hotkey('ctrl', 'c')

    # Retrieve the URL from the clipboard
    url = pyperclip.paste()
    return url

# Function to read settings from settings.txt file
def get_settings():
    settings_path = os.path.join(os.path.dirname(__file__), "Internal", "settings.txt")
    settings = {}
    with open(settings_path, "r") as file:
        for line in file:
            key, value = line.strip().split(":")
            settings[key.strip()] = value.strip()
    return settings

# Function to play or pause Spotify using the specified keybind
def play_pause_spotify(keybind):
    # Split the keybind into individual keys
    keys = keybind.split("+")
    # Press each key in the sequence
    for key in keys:
        pyautogui.keyDown(key)
    # Release each key in reverse order
    for key in reversed(keys):
        pyautogui.keyUp(key)

# Function to play Spotify
def play_spotify():
    settings = get_settings()
    spotify_keybind = settings.get("Spotify Play/Pause Keybind", "ctrl+=")
    play_pause_spotify(spotify_keybind)

# Function to pause Spotify
def pause_spotify():
    settings = get_settings()
    spotify_keybind = settings.get("Spotify Play/Pause Keybind", "ctrl+=")
    play_pause_spotify(spotify_keybind)

# Function to increase volume
def increase_volume():
    print("Increasing volume")
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMasterVolume(volume.GetMasterVolume() + 0.1, None)

# Function to decrease volume
def decrease_volume():
    print("Decreasing volume")
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMasterVolume(volume.GetMasterVolume() - 0.1, None)

# Function to mute volume
def mute_volume():
    print("Muting volume")
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMute(True, None)

def main():
    global browser_name, browser_process_name

    # Get settings
    settings = get_settings()
    spotify_keybind = settings.get("Spotify Play/Pause Keybind", "ctrl+=")
    browser_name = settings.get("Browser", "Mozilla Firefox")
    if browser_name.lower() == "mozilla firefox":
        browser_process_name = "firefox.exe"
    elif browser_name.lower() == "chrome":
        browser_process_name = "chrome.exe"
    elif browser_name.lower() == "edge":
        browser_process_name = "msedge.exe"

    # Wait until the browser window is active
    browser_window = None
    while browser_window is None or not browser_window.isActive:
        browser_window = gw.getWindowsWithTitle(browser_name)[0]  # Use dynamically obtained browser name
        time.sleep(1)  # Check every second

    # Add a delay to allow the browser to fully load
    time.sleep(1)  # Adjust the delay as needed

    # Get the folder path where the "Scoreboards" folder is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    folder_path = os.path.join(script_dir, "Scoreboards")

    is_muted = False  # Flag to track if tab is muted

    # Continuous loop
    while True:
        # Get the current title of the browser tab
        title = browser_window.title

        # Print the current title for verification
        print("Current Title:", title)

        # Check if the title contains "StreamEast"
        if "StreamEast" in title:
            if is_image_present(folder_path):
                if is_muted:
                    print("Image found. Unmuting browser tab...")
                    unmute_browser_tab(browser_window)
                    time.sleep(.1)  # Add a small delay
                    is_muted = False
                    # Pause Spotify
                    pause_spotify()
                else:
                    print("Image found. Tab is already unmuted.")
            else:
                if not is_muted:
                    print("Image not found. Muting browser tab...")
                    mute_browser_tab(browser_window)
                    time.sleep(1)  # Add a small delay
                    is_muted = True
                    # Play Spotify
                    play_spotify()
                else:
                    print("Image not found. Tab is already muted.")
        else:
            print("Browser is not on the correct website.")

        # Wait for 5 seconds before checking again
        time.sleep(2)

if __name__ == "__main__":
    main()
