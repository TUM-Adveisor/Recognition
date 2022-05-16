import cv2
import numpy as np
import matplotlib.pyplot as plt
import sklearn.cluster as sk
from sklearn.metrics import r2_score

def find_intersection():
    image = cv2.imread("original.jpg", cv2.IMREAD_GRAYSCALE)
    n_blur = 6
    ksize = (n_blur, n_blur)
    image = cv2.blur(image, ksize)
    """plt.imshow(image, cmap='gray', vmin = 0, vmax = 255)
    plt.show()"""
    otsu = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[0]
    image_edge = cv2.Canny(image, otsu/2, otsu, apertureSize = 3, L2gradient = True)
    """plt.imshow(image_edge)
    plt.show()"""

    parameter = []
    lines = cv2.HoughLinesP(image_edge,1,np.pi/180,100,minLineLength=75,maxLineGap=15)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        #cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
        k = (y1-y2)/(x1-x2)
        d = y1 - k*x1
        parameter.append([k, d])
    parameter = np.array(parameter)
    db = sk.DBSCAN(eps=50, min_samples=5).fit(parameter)
    labels = db.labels_
    param_ver= []
    param_hor= []
    for i in range(len(np.unique(labels))-1):
        subset = parameter[np.where(labels==i)]
        mean = np.mean(subset, axis=0)
        if mean[0]>0:
            param_hor.append(mean)
        else:
            param_ver.append(mean)
    param_hor = np.array(param_hor)
    param_ver = np.array(param_ver)
    """plt.scatter(parameter[:,0], parameter[:,1])
    plt.scatter(param_hor[:,0], param_hor[:,1], label="Horizontal")
    plt.scatter(param_ver[:,0], param_ver[:,1], label="Vertical")
    plt.legend()
    plt.show()"""

    param_hor = param_hor[param_hor[:,1].argsort()]
    param_ver = param_ver[param_ver[:,1].argsort()]
    #print(len(param_hor))
    #print(len(param_ver))
    while len(param_hor)>9:
        diff_u = np.ediff1d(param_hor[:,1][0:len(param_hor)-1])
        diff_o = np.ediff1d(param_hor[:,1][1:len(param_hor)])
        fit_u = np.poly1d(np.polyfit(range(len(diff_u)), diff_u, 2))
        r_u = r2_score(diff_u, fit_u(range(len(diff_u))))
        fit_o = np.poly1d(np.polyfit(range(len(diff_o)), diff_o, 2))
        r_o = r2_score(diff_o, fit_o(range(len(diff_o))))
        if r_u<r_o:
            param_hor = np.delete(param_hor, 0, axis=0)
        else:
            param_hor = np.delete(param_hor, len(param_hor)-1, axis=0)
    while len(param_ver)>9:
        diff_u = np.ediff1d(param_ver[:,1][0:len(param_ver)-1])
        diff_o = np.ediff1d(param_ver[:,1][1:len(param_ver)])
        fit_u = np.poly1d(np.polyfit(range(len(diff_u)), diff_u, 2))
        r_u = r2_score(diff_u, fit_u(range(len(diff_u))))
        fit_o = np.poly1d(np.polyfit(range(len(diff_o)), diff_o, 2))
        r_o = r2_score(diff_o, fit_o(range(len(diff_o))))
        if r_u<r_o:
            param_ver = np.delete(param_ver, 0, axis=0)
        else:
            param_ver = np.delete(param_ver, len(param_ver)-1, axis=0)

    intersection = []
    for i in param_hor:
        for j in param_ver:
            int_x = (j[1]-i[1])/(i[0]-j[0])
            int_y = i[0]*int_x+i[1]
            intersection.append([int_x, int_y])
    intersection = np.flip(np.array(intersection), axis=0)
    """plt.imshow(image, cmap='gray', vmin = 0, vmax = 255)
    plt.scatter(intersection[:,0], intersection[:,1])
    plt.show()"""

    intersection = intersection.reshape((9,9,2))
    height = 1.8*np.linalg.norm(np.diff(intersection, axis=1), axis=2)
    #print(height)
    return intersection, height
