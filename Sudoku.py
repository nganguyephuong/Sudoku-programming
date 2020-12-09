# Sudoku-programming
import cv2
import pytesseract
import imutils
import re

def replace_chars(text):
    list_of_numbers = re.findall(r'\d+', text)
    result_number = ''.join(list_of_numbers)
    return result_number

def xuat(a):
    img = cv2.imread(path) #test.png is your original image
    img = imutils.resize(img, width=900, height=900)
    x = 0
    y = -100
    fontScale = 2.3    
    # Blue color in BGR 
    color = (255, 0, 0)     
    # Line thickness of 2 px 
    thickness = 2
    for un in a:
        print(un)
    for row in range(0, 9):
        x += 100
        y = 0
        for col in range (0,9):
            y += 100
            cv2.putText(img, str(a[int((x-100)/100)][int((y-100)/100)]) , (y-80,x-30), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow("Bai giai Sodoku", img)
    cv2.waitKey()
    path2 = path.split(".")[0] + "_OUT.jpg"
    cv2.imwrite(path2, img)
    exit()

def process(k):
    # print(k)
    while (a[int(k/9)][int(k%9)] != 0):
        k = k + 1
    # print(k)
    i = int(k/9)
    j = k%9
    # print(i, j)
    for x in range(1, 10):
        # print(x)
        if isOK(i, j, x):
            a[i][j] = x
            if k == lastK:
                # print(k, lastK)
                print("Bai giai:")
                xuat(a)
                break
            else:
                process(k+1)
                a[i][j] = 0

    return 0

def isOK(i, j, x):
    # print(x)
    for t in range(0, 9):
        if a[i][t] == x:
            return False
    for t in range(0, 9):
        if a[t][j] == x:
            return False
    tmpX = i%3
    tmpY = j%3
    for u in range(i-tmpX, i-tmpX+3):
        for t in range(j-tmpY, j-tmpY+3):
            if a[u][t] == x:
                return False
    return True

def findLastK():
    for i in range(8, 0, -1):
        for j in range(8, 0, -1):
            if a[i][j] == 0:
                return i*9 + j
    return 0

print("Nhap ten anh can giai (bao gom duoi):")
path = str(input())

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img = cv2.imread(path) #test.png is your original image
img = imutils.resize(img, width=900, height=900)
x = 0
y = -100

digits = []
for i in range(0, 9):
    x += 100
    y = 0
    for j in range (0,9):
        y += 100
        # print(x, y)
        crop = img[x-95:x-20, y-95:y-20]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thresh = cv2.GaussianBlur(thresh, (3,3), 0)
        data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
        data = replace_chars(data.strip()).strip()
        if len(data) == 0:
            data = "0"
        digits.append(int(data))
        # print(data)
        # cv2.imshow('crop', thresh)
        # cv2.waitKey()
k = -1
a = []
b = []
# print(len(digits))
for i in range(0,9):
    for j in range(0, 9):
        k+=1
        b.append(digits[k])
    a.append(b)
    b = []

print("Sogoku:")
for un in a:
    print(un)
lastK = 0
lastK=int(findLastK())
process(0)
print("De sai hoac anh khong dung yeu cau!")
