import cv2

# Define the video capture objects for both videos
cap1 = cv2.VideoCapture("video.mp4")
cap2 = cv2.VideoCapture("video.mp4")

## In_roi:
in_roi1 = False
in_roi2 = False

# Define the duration of the object inside the AOI in both videos
duration1 = 0
duration2 = 0

# Wait for 1 second for the videos to start playing
cv2.waitKey(1000)

# Define the variables for the selected AOIs in both videos
ix1, iy1, fx1, fy1 = 0, 0, 0, 0
ix2, iy2, fx2, fy2 = 0, 0, 0, 0

# Define the flag to check if the AOIs have been selected
selected = False

# Start a loop to process the frames in both videos
while True:
    # Read the frames in both videos
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    # Stop the loop if any of the videos end
    if not ret1 or not ret2:
        break

    # Resize the frames to a common width
    frame1 = cv2.resize(frame1, (640, 480))
    frame2 = cv2.resize(frame2, (640, 480))

    # Display the frames in both videos
    cv2.imshow("Video 1", frame1)
    cv2.imshow("Video 2", frame2)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # If the 'q' key is pressed, exit the loop
    if key == ord("q"):
        break

    # If the 'p' key is pressed, pause the videos and start selecting the AOIs
    if key == ord("p"):
        # Pause the videos
        #cv2.waitKey(-1)

        # Start selecting the AOI in video 1
        print("Select the AOI in Video 1")
        roi1 = cv2.selectROI("Video 1", frame1, fromCenter=False, showCrosshair=True)
        ix1, iy1, fx1, fy1 = roi1
        print("AOI in Video 1 selected:", roi1)

        # Start selecting the AOI in video 2
        print("Select the AOI in Video 2")
        roi2 = cv2.selectROI("Video 2", frame2, fromCenter=False, showCrosshair=True)
        ix2, iy2, fx2, fy2 = roi2
        print("AOI in Video 2 selected:", roi2)

        # Set the flag to indicate that the AOIs have been selected
        selected = True

    # If the AOIs have been selected, start processing the frames in both videos
    if selected:
        # Convert the selected ROIs to integers
        ix1, iy1, fx1, fy1 = map(int, [ix1, iy1, fx1, fy1])
        ix2, iy2, fx2, fy2 = map(int, [ix2, iy2, fx2, fy2])

        # Define the ROIs in both videos
        roi1 = frame1[iy1:fy1, ix1:fx1]
        roi2 = frame2[iy2:fy2, ix2:fx2]

        # Convert the ROIs to grayscale
        gray1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to the ROIs
        thresh1 = cv2.threshold(gray1, 150, 255, cv2.THRESH_BINARY)[1]
        thresh2 = cv2.threshold(gray2, 150, 255, cv2.THRESH_BINARY)[1]

        # Find contours in the thresholded ROI in video 1
        contours1, _ = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        ## Inserted:
        # Loop over the contours
        for contour in contours1:
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)

            # If the bounding box overlaps with the ROI, set in_roi to True and start the timer
            if roi1 is not None and x < fx1 and x + w > ix1 and y < fy1 and y + h > iy1:
                if not in_roi1:
                    start_time1 = cap1.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                    in_roi1 = True

            # If the bounding box does not overlap with the ROI, add the time spent in the ROI to the total
            # and reset the timer
            elif in_roi1:
                end_time1 = cap1.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                duration1 += end_time1 - start_time1
                in_roi1 = False

        # Draw a rectangle around the selected AOI in video 1
        cv2.rectangle(frame1, (ix1, iy1), (fx1, fy1), (0, 255, 0), 2)

        # # Find the duration of the object inside the AOI in video 1
        # if len(contours1) > 0:
        #     duration1 += 1

        # Find contours in the thresholded ROI in video 2
        contours2, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


                ## Inserted:
        # Loop over the contours
        for contour in contours2:
            # Get the bounding box of the contour
            x2, y2, w2, h2 = cv2.boundingRect(contour)

            # If the bounding box overlaps with the ROI, set in_roi to True and start the timer
            if roi2 is not None and x2 < fx2 and x2 + w2 > ix2 and y2 < fy2 and y2 + h2 > iy2:
                if not in_roi2:
                    start_time2 = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                    in_roi2 = True

            # If the bounding box does not overlap with the ROI, add the time spent in the ROI to the total
            # and reset the timer
            elif in_roi2:
                end_time2 = cap2.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                duration2 += end_time2 - start_time2
                in_roi2 = False

        # Draw a rectangle around the selected AOI in video 2
        cv2.rectangle(frame2, (ix2, iy2), (fx2, fy2), (0, 255, 0), 2)

        # # Find the duration of the object inside the AOI in video 2
        # if len(contours2) > 0:
        #     duration2 += 1

        # # Print the duration of the object inside the AOI in both videos
        # print("Duration in Video 1:", duration1)
        # print("Duration in Video 2:", duration2)

    # If the AOIs have not been selected yet, show the frames without processing
    else:
        # Display the frames in both videos
        cv2.imshow("Video 1", frame1)
        cv2.imshow("Video 2", frame2)

# Release the video capture objects and close all windows
cap1.release()
cap2.release()
cv2.destroyAllWindows()

print("Duration in Video 1:", duration1)
print("Duration in Video 2:", duration2)