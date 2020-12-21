import cv2
import numpy as np
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage.morphology import watershed
import math

class ProcessImage:

    baseurl = 'http://localhost:5000/static/'

    filename = ''

    def __init__(self, filename):
        self.filename = filename

    def process(self):
        # Input Gambar
        img = cv2.imread("static/temp/"+self.filename)

        # Ubah Gambar ke Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Ubah Grayscale ke Biner
        ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        newimg = cv2.bitwise_not(thresh)

        kernel = np.ones((2, 2), np.uint8)
        opening = cv2.morphologyEx(newimg, cv2.MORPH_OPEN, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            cv2.drawContours(opening, [cnt], 0, 255, -1)

        D = ndimage.distance_transform_edt(opening)
        localMax = peak_local_max(D, indices=False, min_distance=15, labels=thresh)
        markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
        labels = watershed(-D, markers, mask=opening)

        tinggi, lebar = img.shape[:2]

        obj = []
        luas = []
        thimg = []
        kebulatan = []
        keliling = []

        for indeks in range(1, (len(np.unique(labels)) - 1)):
            cadar = np.zeros((tinggi, lebar), np.uint8)
            cadar[labels == indeks + 1] = 1
            objek = img * cadar[:, :, np.newaxis]
            objek = objek[..., :: -1]

            gra2 = cv2.cvtColor(objek, cv2.COLOR_BGR2GRAY)
            ret2, thresh2 = cv2.threshold(gra2, 180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            ctr, hrc = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if len(ctr) != 0 and cv2.contourArea(ctr[0], False) > 500:
                obj.append(objek)
                thimg.append(thresh2)

                iluas = cv2.contourArea(ctr[0], False)
                ikeliling = cv2.arcLength(ctr[0], True)
                kebulatan.append(4 * math.pi * (iluas / (ikeliling * ikeliling)))
                luas.append(iluas)
                keliling.append(ikeliling)

        normal = []
        mikrositik = []

        for index in range(1, len(kebulatan)):
            if kebulatan[index - 1] > 0.64 and luas[index - 1] > 2900:
                normal.append(index - 1)
                M = cv2.moments(thimg[index - 1])
                X = int(M["m10"] / M["m00"])
                Y = int(M["m01"] / M["m00"])
                img = cv2.circle(img, (X, Y), 50, (255, 0, 0), 4)
            elif kebulatan[index - 1] > 0.64 and luas[index - 1] < 2900:
                mikrositik.append(index - 1)
                M = cv2.moments(thimg[index - 1])
                X = int(M["m10"] / M["m00"])
                Y = int(M["m01"] / M["m00"])
                img = cv2.circle(img, (X, Y), 50, (0, 0, 255), 4)
            elif (kebulatan[index - 1] > 0.52 and kebulatan[index - 1] < 0.63) and (
                    luas[index - 1] > 2200 and luas[index - 1] < 3450):
                mikrositik.append(index - 1)
                M = cv2.moments(thimg[index - 1])
                X = int(M["m10"] / M["m00"])
                Y = int(M["m01"] / M["m00"])
                img = cv2.circle(img, (X, Y), 50, (0, 0, 255), 4)

        cv2.imwrite("static/temp/edit-" + self.filename,img)
        urledit = self.baseurl+"temp/edit-"+self.filename
        jmlnormal = str(len(normal))
        jmlmikrositik = str(len(mikrositik))
        return jmlnormal, jmlmikrositik, urledit, self.filename

    def process2(self):
        # Input Gambar
        img = cv2.imread("static/temp/"+self.filename)

        # Ubah Gambar ke Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Ubah Grayscale ke Biner
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        newimg = cv2.bitwise_not(thresh)

        kernel = np.ones((2, 2), np.uint8)
        opening = cv2.morphologyEx(newimg, cv2.MORPH_OPEN, kernel, iterations=3)

        contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            cv2.drawContours(opening, [cnt], 0, 255, -1)

        D = ndimage.distance_transform_edt(opening)
        localMax = peak_local_max(D, indices=False, min_distance=15, labels=thresh)
        markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
        labels = watershed(-D, markers, mask=opening)

        tinggi, lebar = img.shape[:2]

        obj = []
        luas = []
        thimg = []
        kebulatan = []
        keliling = []

        for indeks in range(1, (len(np.unique(labels)) - 1)):
            cadar = np.zeros((tinggi, lebar), np.uint8)
            cadar[labels == indeks + 1] = 1
            objek = img * cadar[:, :, np.newaxis]
            objek = objek[..., :: -1]

            gra2 = cv2.cvtColor(objek, cv2.COLOR_BGR2GRAY)
            ret2, thresh2 = cv2.threshold(gra2, 180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            ctr, hrc = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if len(ctr) != 0 and cv2.contourArea(ctr[0], False) > 500:
                obj.append(objek)
                thimg.append(thresh2)

                iluas = cv2.contourArea(ctr[0], False)
                ikeliling = cv2.arcLength(ctr[0], True)
                kebulatan.append(4 * math.pi * (iluas / (ikeliling * ikeliling)))
                luas.append(iluas)
                keliling.append(ikeliling)

        normal = []
        mikrositik = []

        for index in range(1, len(kebulatan)):
            if kebulatan[index - 1] > 0.65 and luas[index - 1] > 6000 and luas[index - 1] < 8300:
                normal.append(index - 1)
                M = cv2.moments(thimg[index - 1])
                X = int(M["m10"] / M["m00"])
                Y = int(M["m01"] / M["m00"])
                img = cv2.circle(img, (X, Y), 60, (255, 0, 0), 5)
            elif kebulatan[index - 1] > 0.56 and luas[index - 1] > 4500 and luas[index - 1] < 6000:
                mikrositik.append(index - 1)
                M = cv2.moments(thimg[index - 1])
                X = int(M["m10"] / M["m00"])
                Y = int(M["m01"] / M["m00"])
                img = cv2.circle(img, (X, Y), 60, (0, 0, 255), 5)

        cv2.imwrite("static/temp/edit-" + self.filename,img)
        urledit = self.baseurl+"temp/edit-"+self.filename
        jmlnormal = str(len(normal))
        jmlmikrositik = str(len(mikrositik))
        return jmlnormal, jmlmikrositik, urledit, self.filename