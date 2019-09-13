# MCQ_Scanner
Project to scan and grade MCQ answer sheets
Python based Software system to grade multiple-choice questions using webcam. This will save lot of money which is required to print OMR sheets as MCQ sheets required by our software can be printed by any traditional printer. Also, there will be no need to buy special OMR scanners as system will be using a webcam to scan and grade the MCQs.

## Logic to detect filled options is explained below:
A. Boundaries detection: To detect the boundaries of the MCQ sheet this project uses the open CV’s simple blob detection function and identifies the top, bottom, right and left boundaries by sorting the detected blobs.
B. Filled options detection: For filled options detection we created new logic which is explained below
1. Scan the image using web cam, once all the boundary blobs are detected capture that image frame.
2. Perform threshold processing on the captured image to convert the image into binary (Black and White).
3. Identify the centre point of each option’s circle by intersecting the virtual lines generated using boundary blobs.
4. Identify the smallest boundary blob and calculate its radius to be used in next step.
5. Draw virtual circles using the centre points detected in step3 and radius obtained in step 4.
6. Read each pixel of the area covered by the circles (from step 5), calculate the filled pixels and store these values in a list.
7. Depending upon the percentage of filled pixels, decide whether an option is filled or not.
8. Pass the list containing option wise pixel filled information to the marks calculation module.
9. Display the score after performing the calculation.
