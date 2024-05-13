import os
import pyautogui
import pygetwindow as gw
import time
import pyperclip  # Import the pyperclip module
from PIL import ImageGrab
from functools import partial

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
    # Activate the browser tab window
    window.activate()
    # Send ALT-1 key combination to mute the tab
    pyautogui.hotkey('alt', '1')

# Function to unmute the browser tab
def unmute_browser_tab(window):
    # Activate the browser tab window
    window.activate()
    # Send ALT-2 key combination to unmute the tab
    pyautogui.hotkey('alt', '2')

# Function to get the URL of the browser tab
def get_browser_tab_url():
    # Activate the browser window
    browser_window = gw.getWindowsWithTitle("Mozilla Firefox")[0]  # Replace with your browser's name
    browser_window.activate()

    # Simulate pressing Ctrl+L to focus the address bar
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(1)  # Add a small delay to ensure the address bar is focused

    # Simulate pressing Ctrl+C to copy the URL
    pyautogui.hotkey('ctrl', 'c')

    # Retrieve the URL from the clipboard
    url = pyperclip.paste()
    return url

def main():
    # Add a delay to allow the browser to fully load
    time.sleep(5)  # Adjust the delay as needed

    # Get the folder path where the "Scoreboards" folder is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    folder_path = os.path.join(parent_dir, "Scoreboards")
    
    is_muted = False  # Flag to track if tab is muted

    # Get the browser tab window
    browser_tab_window = gw.getWindowsWithTitle("Mozilla Firefox")[0]  # Replace with your browser's name

    # Continuous loop
    while True:
        # Get the current title of the browser tab
        title = browser_tab_window.title

        # Print the current title for verification
        print("Current Title:", title)

        # Check if the title contains "StreamEast"
        if "StreamEast" in title:
            if is_image_present(folder_path):
                if is_muted:
                    print("Image found. Unmuting browser tab...")
                    unmute_browser_tab(browser_tab_window)
                    is_muted = False
                else:
                    print("Image found. Tab is already unmuted.")
            else:
                if not is_muted:
                    print("Image not found. Muting browser tab...")
                    mute_browser_tab(browser_tab_window)
                    is_muted = True
                else:
                    print("Image not found. Tab is already muted.")
        else:
            print("Browser is not on the correct website.")

        # Wait for 5 seconds before checking again
        time.sleep(5)

if __name__ == "__main__":
    main()
