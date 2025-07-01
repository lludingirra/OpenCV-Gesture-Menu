import cv2 # Import the OpenCV library for computer vision tasks.
import os # Import the os module for interacting with the operating system, like listing directories.
from cvzone.HandTrackingModule import HandDetector # Import HandDetector from cvzone for hand detection and tracking.

# Initialize video capture from the default webcam (index 0).
cap = cv2.VideoCapture(0)
# Set the width of the captured video frame to 650 pixels.
cap.set(3, 650)
# Set the height of the captured video frame to 480 pixels.
cap.set(4, 480)

# Load the background image for the application interface.
imgBackground = cv2.imread("Resources/Background.png")

# --- Load Mode Images ---
folderPathModes = "Resources/Modes" # Define the path to the folder containing mode images.
listImgModesPath = os.listdir(folderPathModes) # Get a list of all file names in the modes folder.
listImgModes = [] # Initialize an empty list to store loaded mode images.
for imgMode in listImgModesPath:
    # Read each mode image and append it to the listImgModes.
    # os.path.join handles path concatenation correctly across different OS.
    listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgMode)))

# --- Load Icon Images ---
folderPathIcons = "Resources/Icons" # Define the path to the folder containing icon images.
listImgIconsPath = os.listdir(folderPathIcons) # Get a list of all file names in the icons folder.
listImgIcons = [] # Initialize an empty list to store loaded icon images.
for imgIcon in listImgIconsPath:
    # Read each icon image and append it to the listImgIcons.
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIcon)))

# --- Application State Variables ---
modeType = 0 # Current mode of selection (0, 1, 2, etc., corresponds to different selection screens).
selection = -1 # Stores the current selection (1, 2, or 3 based on finger count). -1 means no selection.
counter = 0 # Counter for selection animation/progress.
selectionSpeed = 7 # Speed of the selection animation (determines how fast the ellipse fills).

# Initialize HandDetector with max 1 hand and a detection confidence of 0.5.
detector = HandDetector(maxHands=1, detectionCon=0.5)
# Predefined positions for the selection circles/ellipses on the background image.
modePositions = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0 # Counter to introduce a pause after a selection is made.
selectionList = [-1, -1, -1] # Stores the final selections for each mode. -1 means no selection made for that mode yet.

# --- Main Application Loop ---
while True:
    success, img = cap.read() # Read a frame from the webcam.
    
    if success: # If the frame was read successfully:
        img = cv2.flip(img, 1) # Flip the image horizontally (mirror effect for user).
        
        hands, img = detector.findHands(img) # Detect hands in the image and draw landmarks (if draw=True, default).
        
        # Overlay the live camera feed onto a specific region of the background image.
        imgBackground[139:139 + 480, 50:50 + 640] = img
        # Overlay the current mode image onto a specific region of the background image.
        imgBackground[0:720, 847:1280] = listImgModes[modeType]
        
        # Check for hand gestures only if a hand is detected, no pause is active, and modes are available (modeType < 3).
        if hands and counterPause == 0 and modeType < 3:
            
            hand1 = hands[0] # Get the first detected hand.
            fingers1 = detector.fingersUp(hand1) # Get the count of fingers that are up for the detected hand.
            
            # --- Selection Logic based on Finger Count ---
            if sum(fingers1) == 1: # If only one finger (index finger) is up:
                if selection != 1: # If the selection has changed to 1:
                    counter = 1 # Reset counter to 1 for new selection animation.
                selection = 1 # Set current selection to 1.
                
            elif sum(fingers1) == 2: # If two fingers are up:
                if selection != 2:
                    counter = 1
                selection = 2
                
            elif sum(fingers1) == 3: # If three fingers are up:
                if selection != 3:
                    counter = 1
                selection = 3
                
            else: # If other than 1, 2, or 3 fingers are up:
                selection = -1 # No valid selection.
                counter = 0 # Reset counter.
                    
            # --- Selection Animation and Confirmation ---
            if counter > 0: # If a valid selection is ongoing:
                counter += 1 # Increment counter for animation progress.
                
                # Draw an ellipse (progress indicator) around the selected mode position.
                # The ellipse fills up as 'counter*selectionSpeed' increases from 0 to 360 degrees.
                cv2.ellipse(imgBackground, modePositions[selection - 1], (103, 103),
                            0, 0, counter * selectionSpeed, (0, 255, 0), 20)
                
                if counter * selectionSpeed > 360: # If the ellipse completes a full circle (selection confirmed):
                    selectionList[modeType] = selection # Store the confirmed selection for the current mode.
                    modeType += 1 # Advance to the next mode/selection screen.
                    counter = 0 # Reset counter.
                    selection = -1 # Reset selection.
                    counterPause = 1 # Activate a pause to prevent immediate re-selection.
    
    # --- Pause Logic ---
    if counterPause > 0: # If pause is active:
        counterPause += 1 # Increment pause counter.
        
        if counterPause > 60: # If pause duration (60 frames) is over:
            counterPause = 0 # Deactivate pause.
            
    # --- Display Selected Icons at the Bottom ---
    # Display the selected icon for the first mode (if a selection was made).
    if selectionList[0] != -1:
        # Place the corresponding icon image from listImgIcons.
        # selectionList[0] - 1 is used because selections are 1, 2, 3 but list indices are 0, 1, 2.
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
    
    # Display the selected icon for the second mode (if a selection was made).
    if selectionList[1] != -1:
        # Indices are adjusted to get the correct icon for mode 2.
        imgBackground[636:636 + 65, 350:350 + 65] = listImgIcons[2 + selectionList[1]]
        
    # Display the selected icon for the third mode (if a selection was made).
    if selectionList[2] != -1:
        # Indices are adjusted to get the correct icon for mode 3.
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]
    
    # Display the final composite image.
    cv2.imshow("Background", imgBackground)
    # Wait for 1ms for a key press. If 'q' is pressed, break the loop.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Resource Release ---
cap.release() # Release the webcam object.
cv2.destroyAllWindows() # Close all OpenCV windows.