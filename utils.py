import cv2
import numpy as np
import pytesseract

def extract_sudoku_grid(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(img, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest = max(contours, key=cv2.contourArea)

    peri = cv2.arcLength(biggest, True)
    approx = cv2.approxPolyDP(biggest, 0.02 * peri, True)

    pts = np.float32([pt[0] for pt in approx])
    ordered = np.array(sorted(pts, key=lambda x: (x[1], x[0])))
    dst = np.array([[0,0],[450,0],[450,450],[0,450]], dtype='float32')

    M = cv2.getPerspectiveTransform(pts, dst)
    warp = cv2.warpPerspective(img, M, (450,450))
    return warp

def recognize_digits(grid_img):
    board = []
    height, width = grid_img.shape
    cell_h, cell_w = height//9, width//9

    for i in range(9):
        row = []
        for j in range(9):
            cell = grid_img[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
            cell = cell[5:-5, 5:-5]  # trim borders
            _, cell = cv2.threshold(cell, 128, 255, cv2.THRESH_BINARY_INV)
            text = pytesseract.image_to_string(cell, config='--psm 10 digits')
            try:
                val = int(text.strip())
                row.append(val)
            except:
                row.append(0)
        board.append(row)
    return board
