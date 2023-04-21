import cv2

# Define the mouse callback function for selecting the AOIs
def select_roi(event, x, y, flags, param):
    global ix1, iy1, fx1, fy1, ix2, iy2, fx2, fy2, drawing, video1_selected, video2_selected
    if event == cv2.EVENT_LBUTTONDOWN:
        if not video1_selected:
            ix1, iy1 = x, y
            drawing = True
        elif not video2_selected:
            ix2, iy2 = x, y
            drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if not video1_selected:
                cv2.rectangle(frame1, (ix1, iy1), (x, y), (0, 255, 0), 2)
            elif not video2_selected:
                cv2.rectangle(frame2, (ix2, iy2), (x, y), (0, 255, 0), 2)
    elif event == cv2.EVENT_LBUTTONUP:
        if not video1_selected:
            fx1, fy1 = x, y
            drawing = False
            video1_selected = True
        elif not video2_selected:
            fx2, fy2 = x, y
            drawing = False
            video2_selected = True


# Create two video capture objects
cap1 = cv2.VideoCapture('video.mp4')
cap2 = cv2.VideoCapture('video.mp4')

# Set the mouse callback function for both video windows
cv2.namedWindow('Video 1')
cv2.namedWindow('Video 2')
cv2.setMouseCallback('Video 1', select_roi)
cv2.setMouseCallback('Video 2', select_roi)

# Initialize variables for selecting the AOIs
ix1, iy1, fx1, fy1 = -1, -1, -1, -1
ix2, iy2, fx2, fy2 = -1, -1, -1, -1
drawing = False
video1_selected = False
video2_selected = False

# Initialize variables for calculating the duration of the object inside the AOIs
duration1 = 0
duration2 = 0

# Pause the videos for 1 second to allow for selecting the AOIs
while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        break

    cv2.imshow('Video 1', frame1)
    cv2.imshow('Video 2', frame2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    if video1_selected and video2_selected:
        break

    cv2.waitKey(1000)

# Check if the AOIs have been selected in both videos
if video1_selected and video2_selected:
    # Initialize variables for calculating the total duration
    total_duration = 0

    # Loop over the video frames
    while True:
        # Read a frame from each video
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        # If either video has reached its end, break out of the loop
        if not ret1 or not ret2:
            break

        # Convert the ROIs to grayscale
        gray1 = cv2.cvtColor(frame1[iy1:fy1, ix1:fx1], cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2[iy2:fy2, ix2:fx2], cv2.COLOR_BGR2GRAY)

        # Apply thresholding to the ROIs
        _, thresh1 = cv2.threshold(gray1, 50, 255, cv2.THRESH_BINARY)
        _, thresh2 = cv2.threshold(gray2, 50, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded ROI
        contours1, _ = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the contours on the original frame for visual feedback
        cv2.drawContours(frame1, contours1, -1, (0, 0, 255), 2)
        cv2.drawContours(frame2, contours2, -1, (0, 0, 255), 2)

        # Check if any contours were found in the ROI
        if len(contours1) > 0:
            duration1 += 1

        if len(contours2) > 0:
            duration2 += 1

        # Display the frame with the selected ROIs
        cv2.imshow('Video 1', frame1)
        cv2.imshow('Video 2', frame2)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Calculate the total duration that the object was inside the AOIs
    total_duration = duration1 + duration2

    # Print out the total duration in the console
    print(f'Total duration inside AOIs: {total_duration} frames')

# Release the video capture objects and close the windows
cap1.release()
cap2.release()
cv2.destroyAllWindows()
