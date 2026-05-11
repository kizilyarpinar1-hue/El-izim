import cv2
import mediapipe as mp
import numpy as np
import sys

def is_hand_open(hand_landmarks):
    """Check if hand is open by comparing finger tip and pip joint distances"""
    # Get landmarks for index, middle, ring, and pinky fingers
    # Each finger: tip, pip (middle joint)
    fingers = [
        (8, 6),   # Index finger: tip, pip
        (12, 10), # Middle finger: tip, pip
        (16, 14), # Ring finger: tip, pip
        (20, 18)  # Pinky finger: tip, pip
    ]
    
    open_fingers = 0
    for tip_id, pip_id in fingers:
        tip = hand_landmarks.landmark[tip_id]
        pip = hand_landmarks.landmark[pip_id]
        
        # If tip is above pip (lower y value), finger is extended
        if tip.y < pip.y:
            open_fingers += 1
    
    # Hand is considered open if at least 3 fingers are extended
    return open_fingers >= 3

def main() -> int:
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    if not ret:
        print("Failed to access camera")
        return 1

    height, width, _ = frame.shape
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    draw_color = (0, 255, 0)  # Green
    brush_thickness = 5
    prev_x, prev_y = None, None

    print("Controls:")
    print("- OPEN your hand and move INDEX FINGER to draw")
    print("- CLOSE your hand (make a fist) to stop drawing")
    print("- Press 'c' to clear the canvas")
    print("- Press 'r' for red, 'g' for green, 'b' for blue")
    print("- Press '+' to increase brush size, '-' to decrease")
    print("- Press 'q' to quit")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                    )

                    hand_is_open = is_hand_open(hand_landmarks)

                    index_finger_tip = hand_landmarks.landmark[8]
                    x = int(index_finger_tip.x * width)
                    y = int(index_finger_tip.y * height)

                    circle_color = draw_color if hand_is_open else (128, 128, 128)
                    cv2.circle(frame, (x, y), 10, circle_color, -1)

                    if hand_is_open:
                        if prev_x is not None and prev_y is not None:
                            cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, brush_thickness)
                        prev_x, prev_y = x, y
                    else:
                        prev_x, prev_y = None, None
            else:
                prev_x, prev_y = None, None

            combined = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)
            cv2.putText(
                combined,
                f"Brush Size: {brush_thickness}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.imshow("Finger Drawing", combined)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
            if key == ord("c"):
                canvas = np.zeros((height, width, 3), dtype=np.uint8)
            elif key == ord("r"):
                draw_color = (0, 0, 255)
            elif key == ord("g"):
                draw_color = (0, 255, 0)
            elif key == ord("b"):
                draw_color = (255, 0, 0)
            elif key in (ord("+"), ord("=")):
                brush_thickness = min(brush_thickness + 2, 30)
            elif key in (ord("-"), ord("_")):
                brush_thickness = max(brush_thickness - 2, 1)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
