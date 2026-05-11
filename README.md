# Finger Drawing with Hand Tracking

This project explores real time hand motion capture for free space drawing. The program observes the hand through a webcam feed and uses a common library for landmark recognition to identify the position of the index finger. When the hand remains open the fingertip acts as a contact point for drawing across a blank digital surface layered on top of the live camera output. When the hand closes the drawing motion pauses which allows more control and less visual noise. It is surprisingly intuitive once you try it and feels almost like moving a brush in the air.

The system relies on a popular hand landmark model together with a video processing toolkit. A short sequence of geometric checks decides whether the hand is open. After that the fingertip coordinates translate directly into drawing strokes with adjustable thickness and adjustable color. Even though the idea is simple the experience can feel expressive and lightly playful which makes it a useful small demonstration or teaching example.

## Requirements

- Python 3
- A functional webcam
- The libraries listed in `requirements.txt`

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```



## Running the program

Execute the script:

```bash
python3 finger_draw.py
```



If the camera is accessible a new window will appear. Move your hand within view and begin to draw.
## Controls
- Open your hand and move your **index finger** to draw
- Close your hand (make a fist) to stop drawing
- `c`: clear the canvas
- `r` / `g` / `b`: change color
- `+` / `-`: change brush size
- `q`: quit

## Notes
It may be helpful to experiment with lighting to obtain smoother detection. A small amount of ambient light usually gives the most stable tracking. You might also consider small adjustments in color and brush scale to suit your desired effect.
