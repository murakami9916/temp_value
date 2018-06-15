import cv2
import numpy as np
import csv
import matplotlib.pyplot as plt
import sys
import os

# OpenCVのイベントリストの出力
def printEvents():
    events = [i for i in dir(cv2) if 'EVENT' in i]
    print (events)

# OpenCVのマウスイベントを扱うためのクラス
class CVMouseEvent:
    def __init__(self, press_func=None, drag_func=None, release_func=None):
        self._press_func = press_func
        self._drag_func = drag_func
        self._release_func = release_func

        self._is_drag = False

    # Callback登録関数
    def setCallBack(self, win_name):
        cv2.setMouseCallback(win_name, self._callBack)

    def _doEvent(self, event_func, x, y):
        if event_func is not None:
            event_func(x, y)

    def _callBack(self, event, x, y, flags, param):
        # マウス左ボタンが押された時の処理
        if event == cv2.EVENT_LBUTTONDOWN:
            self._doEvent(self._press_func, x, y)
            self._is_drag = True

        # マウス左ドラッグ時の処理
        elif event == cv2.EVENT_MOUSEMOVE:
            if self._is_drag:
                self._doEvent(self._drag_func, x, y)

        # マウス左ボタンが離された時の処理
        elif event == cv2.EVENT_LBUTTONUP:
            self._doEvent(self._release_func, x, y)
            self._is_drag = False


# 描画用の空画像作成
def emptyImage():
	#読み込み画像***************************
    piet = cv2.imread('images/y.png')
    #*************************************
    piet_hsv = cv2.cvtColor(piet, cv2.COLOR_BGR2HSV)

    #print(piet.shape[0])#:y
    #print(piet.shape[1])#:x
    xx = piet.shape[1]
    yy = piet.shape[0]

    # threshold for hue channel in blue range
    blue_min = np.array([0, 0, 0], np.uint8)
    blue_max = np.array([190, 210, 200], np.uint8)
    threshold_blue_img = cv2.inRange(piet_hsv, blue_min, blue_max)
    #threshold_blue_img = cv2.cvtColor(piet, cv2.COLOR_BGR2GRAY)
    threshold_blue_img = cv2.cvtColor(threshold_blue_img, cv2.COLOR_GRAY2RGB)
    return threshold_blue_img, xx, yy
#    return cv2.imread("images/coin.jpg")
#    return np.zeros((512, 512, 3), np.uint8)


# シンプルなマウス描画のデモ
def getdata():
    img, xx, yy = emptyImage()

    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
    color = colors[0]

    # ドラッグ時に描画する関数の定義
    def brushPaint(x, y):
        cv2.circle(img, (x, y), 1, color, -1)
        #描画時の座標
        print("MOUSE COORDINATE")
        print("x:%d" %x)
        print("y:%d\n" %y)
        array =[[]]

        img_src, xx, yy = emptyImage()
        if x > 0 and x < xx and y > 0 and y < yy:
        	tmp = []
        	s = []
        	for i in range(img_src.shape[0]):
        		if img_src[i, x][0] == 255:
			        tmp.append(i)
			        s.append(np.absolute(y-i))
        	'''
        	print("tmp")
        	print(tmp)
        	print("s")
        	print(s)
			'''

        	y_re = range(yy-1, -1, -1)

        	count = len(tmp)
        	if count != 0:
        		array = [[ x, tmp[int(s.index(min(s)))] ]]
        		print("array")
        		print(array)
        		dataList_y[x] = y_re[ tmp[ int(s.index(min(s))) ] ]

    win_name = 'GetData'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    # CVMouseEventクラスによるドラッグ描画関数の登録
    mouse_event = CVMouseEvent(drag_func=brushPaint)
    mouse_event.setCallBack(win_name)

    while(True):
        cv2.imshow(win_name, img)

        key = cv2.waitKey(30) & 0xFF

        # 色切り替えの実装
        if key == ord('1'):
            color = colors[0]
        elif key == ord('2'):
            color = colors[1]
        elif key == ord('3'):
            color = colors[2]

        # 画像のリセット
        elif key == ord('r'):
            img, xx, yy = emptyImage()

        elif key == ord('q'):
            break

        elif key == ord('d'):
            bool_file = os.path.isfile("output.csv")
            if bool_file:
                os.remove("output.csv")
                print("remove now!")

    cv2.destroyAllWindows()

def catImage(event_cat, xc, yc, flags, param):
	global img
	global y_start
	global x_start
	global xmax, xmin
	global ymax, ymin

	if event_cat == cv2.EVENT_RBUTTONDOWN:
		x_start = xc
		y_start = yc
		#cv2.circle(img, (xc, yc), 50, (0, 0, 255), -1)
		print("MOUSE DOWN!!")

	elif event_cat == cv2.EVENT_RBUTTONUP:
		x_end = xc
		y_end = yc
		xmax = max([x_start, x_end])
		xmin = min([x_start, x_end])
		ymax = max([y_start, y_end])
		ymin = min([y_start, y_end])
		#img = img[ymin:ymax, xmin:xmax]
		print("MOUSE UP!!")
		print("********************")
		print("* please, press q! *")
		print("********************")

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    img, num_x, num_y = emptyImage()

    dataList_x = range(num_x)
    dataList_y = [0] * num_x

    if(argc != 3):
        print("error!!")
        sys.exit()

    printEvents()

    y_start = 0
    x_start = 0

    xmax = 0
    xmin = 0
    ymax = 0
    ymin = 0
    print("please, select the range")
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("img", catImage)

    while (True):
    	cv2.imshow("img", img)
    	if cv2.waitKey(1) & 0xFF == ord("q"):
    		break
    cv2.destroyAllWindows()

    getdata()
    
    dataList_y[0]=0.1 # エラー対策

    #　データ補間　
    for (i, t) in enumerate(dataList_y):
        if t == 0 :
            if i == 0 or i == num_x-1:
                print("end point:%d" %i)
            else:
                c = 0
                if dataList_y[i-1] != 0:c = c + 1
                if dataList_y[i+1] != 0:c = c + 1
                dataList_y[i] = (dataList_y[i-1] + dataList_y[i+1]) / c if c!=0 else print("error!! O is NG")

    print("xmin=%d, xmax=%d, listsize=%d" %(xmin, xmax, len(dataList_x)))
    reDataList_x = np.array(dataList_x)
    reDataList_x = np.delete(reDataList_x, range(0, xmin))
    reDataList_x = np.delete(reDataList_x, range(xmax-xmin, num_x-xmin))
    reDataList_y = np.array(dataList_y)
    reDataList_y = np.delete(reDataList_y, range(0, xmin))
    reDataList_y = np.delete(reDataList_y, range(xmax-xmin, num_x-xmin))

    n = np.array((reDataList_x, reDataList_y))
    n = n.transpose()
    np.savetxt("result/output.csv",n,fmt="%5f",delimiter=",")

    #-----------------------------------------------
    argvs = sys.argv
    min_x = int(argvs[1])
    max_x = int(argvs[2])

    fp = np.loadtxt("result/output.csv", delimiter = ",")

    f_x = np.array(fp[:,0])
    f_y = np.array(fp[:,1])
    #print(f_x.shape[0])

    y_new = f_y
    x_new = np.zeros(f_x.shape[0])
    for i in range(f_x.shape[0]):
        x_new[i] = ( (max_x - min_x) / f_x.shape[0] ) * i + min_x

    data=np.array((x_new, y_new))
    data=data.transpose()

    np.savetxt("result/output.csv",data,fmt="%5f",delimiter=",")