#!/usr/bin/python

import cv

if _name_ == "_main_":
    capture = cv.CaptureFromCAM(-1)
    cv.NamedWindow("image")
    while True:
        frame = cv.QueryFrame(capture)
        cv.ShowImage("image", frame)

        k = cv.WaitKey(10)

        if k % 256 == 27:
            break

    cv.DestroyWindow("image")
