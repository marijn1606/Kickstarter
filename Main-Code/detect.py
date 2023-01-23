import numpy as np
import cv2

class Detector:
    def __init__(self, pad_range, pcb_range, pixels_per_milimeter, offset):
        self.pad_range = pad_range
        self.pcb_range = pcb_range
        self.pixels_per_milimeter = pixels_per_milimeter
        self.offset = offset

    def makeColorMask(self, image, colorRange):
        lower = np.array(colorRange[0])
        upper = np.array(colorRange[1])
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)

        return mask

    def findAndSortContours(self, image):
        contours, hierarchy = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
        sortedContours = sorted(contours, key=cv2.contourArea, reverse=True)
        return sortedContours, hierarchy

    def isolatePCB(self, image, pcbColor):
        pcbMask = self.makeColorMask(image, pcbColor)
        cv2.imwrite("PCBmask.jpg", pcbMask)
        sortedContours, _ = self.findAndSortContours(pcbMask)
        
        rect = cv2.minAreaRect(sortedContours[0])
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [box], 0, (255, 255, 255), -1)
        cv2.imwrite("PCBmaskContour.jpg", mask)
        out = np.zeros_like(image)
        out[mask == 255] = image[mask == 255]
        cv2.imwrite("IsolatedPCB.jpg", out)
        return out

    def findPads(self, image, padColor, pcbColor):
        isolatedPCB = self.isolatePCB(image, pcbColor)
        padMask = self.makeColorMask(isolatedPCB, padColor)
        cv2.imwrite("padMask.jpg", padMask)
        padContours, hierarchy = self.findAndSortContours(padMask)
        for i in range(len(padContours)):
            rect = cv2.minAreaRect(padContours[i])
            box = cv2.boxPoints(rect)    
            box = np.intp(box)
            padContours[i] = box
        return padContours, hierarchy

    def filterByArea(self, pads, minArea):
        filteredPads = []
        for pad in pads:
            if cv2.contourArea(pad) > minArea:
                filteredPads.append(pad)
        return filteredPads

    def getMiddlePoints(self, pads):
        middlePoints = []
        for i in pads:
            M = cv2.moments(i)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                middlePoints.append((cx, cy))
        return middlePoints

    def pixelToPrinterCoordinate(self, pixelCoordinate, imageOrigin, imageSize):
        centerX = imageSize[0] / 2
        centerY = imageSize[1] / 2
        
        pixelOffsetX = pixelCoordinate[0] - centerX
        pixelOffsetY = pixelCoordinate[1] - centerY

        mmOffsetX = pixelOffsetX / self.pixels_per_milimeter
        mmOffsetY = pixelOffsetY / self.pixels_per_milimeter
        printerX = imageOrigin[0] + mmOffsetY + self.offset[0]
        printerY = imageOrigin[1] + mmOffsetX - self.offset[1]

        return((printerX, printerY))

    def padsToPrinterCoordinates(self, pixelCoordinates, imageOrigin, imageSize):
        coordinates = []
        for coordinate in pixelCoordinates:
            coordinates.append(self.pixelToPrinterCoordinate(coordinate, imageOrigin, imageSize))
        return coordinates

    # callable functions
    def detect(self, image_name, image_origin, image_size):
        image = cv2.imread(image_name)
        pads, hierarchy = self.findPads(image, self.pad_range, self.pcb_range)
        filteredPads = self.filterByArea(pads, 100)
        middle_points = self.getMiddlePoints(filteredPads)
        printer_coordinates = self.padsToPrinterCoordinates(middle_points, image_origin, image_size)
        # cv2.drawContours(image, filteredPads, -1, (0, 0, 0), 5)
        # cv2.imwrite("detected.jpg", image)
        web_coordinates = []
        for i in range(len(filteredPads)):
            web_coordinates.append(filteredPads[i].tolist())
            
        return printer_coordinates, web_coordinates