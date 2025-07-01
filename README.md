# Hand Gesture Menu Selection

This project demonstrates a real-time interactive menu selection system controlled by hand gestures. It uses OpenCV for video processing and `cvzone` for efficient hand detection. Users can navigate and make selections in a menu by simply showing a specific number of fingers to the camera.

## Features

* **Hand Gesture Recognition:** Detects the number of fingers held up (1, 2, or 3) to control menu selections.
* **Interactive Menu:** A graphical interface with distinct selection areas/modes.
* **Visual Feedback:** Provides an animated progress indicator (an expanding ellipse) for selection confirmation.
* **Multi-Stage Selection:** Supports multiple levels of selection, with chosen items displayed at the bottom of the screen.
* **Modular Hand Tracking:** Leverages `cvzone`'s `HandDetector` for robust and straightforward hand tracking.
* **Intuitive UI:** Overlays live camera feed onto a custom background image with dynamic mode and icon displays.

## Prerequisites

To run this project, you need:
* Python installed (3.6 or higher recommended).
* A webcam connected to your computer.
* A `Resources` folder containing:
    * `Background.png`: The main background image for the UI.
    * `Modes` folder: Contains images representing different selection modes/screens (e.g., `mode1.png`, `mode2.png`, `mode3.png`). These images are displayed in the right panel.
    * `Icons` folder: Contains images for the actual selections made (e.g., `icon1.png`, `icon2.png`, `icon3.png`, `icon4.png`, etc.). These are displayed at the bottom after a selection is confirmed.

## Installation

1.  **Clone or Download the Repository:**
    Get the project files to your local machine.

2.  **Install Required Libraries:**
    Open your terminal or command prompt and run:
    ```bash
    pip install opencv-python cvzone
    ```

## Usage

1.  **Prepare Resources:** Ensure you have the `Resources` folder set up with `Background.png` and subfolders `Modes` and `Icons` containing your necessary images. The naming/ordering of images within `Modes` and `Icons` is important as the code accesses them by list index.
    * Example structure:
        ```
        project_root/
        ├── main.py
        ├── Background.png
        ├── Modes/
        │   ├── 1.png
        │   ├── 2.png
        |   ├── 3.png
        │   └── 4.png
        └── Icons/
            ├── 1.png
            ├── 2.png
            ├── 3.png
            ├── 4.png
            ├── 5.png
            ├── 6.png
            ├── 7.png
            ├── 8.png
            └── 9.png
        ```
2.  **Run the script:**
    Open your terminal or command prompt, navigate to the project directory, and execute the script:
    ```bash
    python main.py
    ```
3.  **Interact with Gestures:**
    * The application will display a window showing your webcam feed on the left and a selection menu on the right.
    * **Selection:** Hold up **1, 2, or 3 fingers** (excluding the thumb) to select the corresponding option in the right-hand menu.
    * **Confirmation:** Once you hold up a specific number of fingers, an ellipse will start to fill around the selected option. Keep your fingers steady until the ellipse completes a full circle (360 degrees) to confirm your selection.
    * **Mode Progression:** After a selection is confirmed, the system will move to the next "mode" (displaying a new image from the `Modes` folder on the right panel).
    * **Selected Items:** Your confirmed selections will appear as icons at the bottom of the screen.
4.  **Exit:** Press the `q` key on your keyboard to close the application window.

## How it Works

1.  **Video Capture & Overlay:** The webcam feed is captured, horizontally flipped, and then overlaid onto a predefined `Background.png` image. The current `mode` image is also overlaid on a specific area of the background.
2.  **Hand Detection:** `cvzone.HandDetector` continuously tracks a single hand and determines which fingers are extended.
3.  **Gesture-Based Selection:**
    * If 1, 2, or 3 fingers are detected, a `selection` variable is set, and a `counter` starts.
    * An `ellipse` is drawn around the `modePosition` corresponding to the `selection`. This ellipse progressively fills (`counter * selectionSpeed`) to indicate progress.
    * Once the ellipse completes a full circle (`> 360` degrees), the selection is confirmed.
4.  **Mode Transition:** Upon confirmation, the `modeType` increments, moving to the next selection screen. A `counterPause` is activated to prevent immediate, accidental re-selections.
5.  **Displaying Selections:** Confirmed selections for each mode are stored in `selectionList` and displayed as icons at predefined positions at the bottom of the screen.

## Customization

* **Camera Resolution:** Adjust `cap.set(3, 650)` and `cap.set(4, 480)` for different webcam resolutions.
* **UI Layout:** Modify the overlay positions (e.g., `imgBackground[139:139 + 480, 50:50 + 640]`) to fit your `Background.png` design.
* **Selection Speed:** Change `selectionSpeed = 7` to make the selection animation faster or slower.
* **Pause Duration:** Adjust `counterPause > 60` to change the duration of the pause after a selection.
* **Mode/Icon Images:** Customize the `Resources/Modes` and `Resources/Icons` folders with your own images. Ensure they are correctly sized and named if you rely on `os.listdir()`'s default ordering.
* **Number of Modes/Selections:** The current setup supports 3 modes (up to `modeType < 3`). You can extend this by adding more images to `Resources/Modes` and adjusting the `modeType` condition and `selectionList` size. Similarly, more icon types can be added and mapped correctly within the display logic.
