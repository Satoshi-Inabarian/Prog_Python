import cv2
import numpy as np

def waitKeyTest():
    WINDOW_NAME = 'key_bind_test'
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.imshow(WINDOW_NAME, np.zeros([100,100]))
    while True:
        res = cv2.waitKey(1)
        if res != -1:
            print(f"You pressed {res} ({res:#x}), 2LSB: {res % 2**16} ({repr(chr(res%256)) if res%256 < 128 else '?'})")
            if res == 27:
                break


#二値化画像作成 th_min 最低閾値 th_max 最大閾値
def make_BinaryImg(imgfile,th_min,th_max,out_dir): 
    gray_img = cv2.imread(imgfile,cv2.IMREAD_GRAYSCALE)
    cv2.imshow("",gray_img)
    cv2.waitKey(0)
    _,binary_img = cv2.threshold(gray_img,th_min,th_max,cv2.THRESH_BINARY)
    cv2.imshow("",binary_img)
    cv2.waitKey(0)
    cv2.imwrite(out_dir,binary_img)
    
def contoursView(binary_img,th_min,th_max):

    #グレースケールに画像を変更
    ret,binary_img = cv2.threshold(binary_img,th_min,th_max,cv2.THRESH_BINARY)#THRESH_BINARYは黒と白をはっきり分けるという意味
    contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #座標を表示する
    print(contours)
    
def contoursWrite(imgfile,th_min,th_max,c_color,outdir):
    gray_img = cv2.imread(imgfile,cv2.IMREAD_GRAYSCALE)
    width,height = gray_img.shape
    #OpenCvでは、画像は全てnumpy.ndarrayとして扱われるため、新規イメージを作成するためには、#
    #単純に、numpy.ndarray配列を作成する。
    # numpy.onesを利用し、すべての要素が1のnumppy.ndarray配列を作成したあと、２５５倍する
    campas_numpy = np.ones((width,height),np.uint8)*255 
    print(campas_numpy)
    _,binary_img = cv2.threshold(gray_img,th_min,th_max,cv2.THRESH_BINARY) 
    contours,_ = cv2.findContours(binary_img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    img_contours = cv2.drawContours(campas_numpy,contours,-1,c_color,1)
    cv2.imshow("",img_contours)
    cv2.waitKey(1000)
    cv2.imwrite(outdir,img_contours)
    
#コールバック関数
def checkPt(campas,event,x,y,flags,param):
    if event == cv2.EVENT_MOUSEMOVE:#マウスの動作をeventに代入し、その後の内容を記述できる
        img2 = np.copy(campas)#座標書き出し用のマスク画像np型
        cv2.circle(img2,center=(x,y),radius=2,color=255,thickness=-1)
        pos_str='(x,y)=('+str(x)+','+str(y)+')'
        cv2.putText(img2,pos_str,(200,20),cv2.FONT_HERSHEY_PLAIN,1,255,1,cv2.LINE_AA)
        cv2.imshow("window",img2)
    if event ==cv2.EVENT_LBUTTONDOWN:
        print(x,y)
    cv2.imshow("window",campas)#初めの画像
    cv2.setMouseCallback("window",checkPt)#マウス動作に関するopencv2のsetMouseCallback関数を使用する。
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def writePt(imgfile,CorX,CorY):
    img = cv2.imread(imgfile)
    #(画像,テキスト,座標,フォント,文字サイズ,色,文字太さ,フォント整形)
    img = cv2.circle(img,center=(CorX,CorY),radius=2,color=(0,0,255),thickness=-1)
    cv2.imshow("",img)
    cv2.waitKey(0)
    cv2.imwrite(imgfile,img)
 
#ndarray型img,xy座標,w幅、h高さ  座標が-になるとエラーになるので注意
def clopImg(img_np,ptx,pty,w,h):
    #img.npを利用して、画像を切り取る
    img_clop = img_np[ptx:ptx+w,pty:pty+h]
    cv2.imshow("clop",img_clop)
    cv2.waitKey(0)

#hsvイメージを二値化画像にする.bgrL=最低閾値、bgrU=最大閾値(それぞれの値はHSV空間のBGR値となっている。)
def hsvimgToBinary(readDir,bgrLower,bgrUpper,minArea):
    import glob
    #jpg画像をreadImgListに配列保存
    readImgList = glob.glob(readDir+"\*.jpg")
    for x in range(len(readImgList)):
        img = cv2.imread(readImgList[x])
        width,height,_ = img.shape #ndarray配列からwidth,heightの情報だけを取り出す
        campas = np.ones((width,height),np.uint8)*255
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)#HSV変換
        img_mask = cv2.inRange(img_hsv,bgrLower,bgrUpper)
        contours,_ = cv2.findContours(img_mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area >= minArea:#条件設定
                campas = cv2.drawContours(campas,contours[i],-1,(0,0,0),1)
        cv2.imshow("image",campas)
        cv2.waitKey(0)

def findMostHsvBgr(img_np):
    import statistics
    cv2.imshow("hsv_image",img_np)
    cv2.waitKey(0)
    img_np = cv2.cvtColor(img_np,cv2.COLOR_BGR2HSV)
    #[:,;,0]は、画像の三次元配列の最後について、rgbの配列番号 rの配列番号は0,gは1,bは2という意味
    B_mode = statistics.mode(img_np[:,:,0].flatten())#最も使われているbgrのb数値
    G_mode = statistics.mode(img_np[:,:,1].flatten())#g数値
    R_mode = statistics.mode(img_np[:,:,2].flatten())#r数値
    print("最頻値【B G R】",B_mode,G_mode,R_mode)
    cv2.imshow("hsv_image",img_np)
    cv2.waitKey(0)
    return B_mode,G_mode,R_mode,img_np

def findMostBgr(img_np):
    import statistics
    B_mode = statistics.mode(img_np[:,:,0].flatten())
    G_mode = statistics.mode(img_np[:,:,1].flatten())
    R_mode = statistics.mode(img_np[:,:,2].flatten())
    print("最頻値【B G R】",B_mode,G_mode,R_mode)
    cv2.imshow("image",img_np)
    cv2.waitKey(0)
    return B_mode,G_mode,R_mode,img_np


# 1.画像(opencv2の二値化画像)から重心を取る方法と、
#2.輪郭から重心をとる方法二つがある。微妙に位置が異なる
#　参考URL https://cvtech.cc/pycvmoment/
#1.画像（二値化画像）から、重心を探す
def centerG_withImgfile(imgfile):
    import CheckErr
    CheckErr.checkfile(imgfile)
    img_np = cv2.imread(imgfile)
    MostB,MostG,MostR,img_hsv = findMostHsvBgr(imgfile)
    bgrLower = np.array([(MostB-50),(MostG-50),(MostR-20)])
    bgrUpper = np.array([(MostB+50),(MostG+50),(MostR+20)])
    img_binary = cv2.inRange(img_hsv,bgrLower,bgrUpper)   
    mu = cv2.moments(img_binary, False)
    x,y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
    img_mu = cv2.circle(img_np, (x,y), 4, 100, 2, 4)
    cv2.imshow("",img_np)
    cv2.waitKey(0)
    
    return img_mu

#2.最大 輪郭から重心をとる。2022/11/29現在動かない
def centerGWithC(contours):

    mu = cv2.moments(contours)
    if (mu["m00"]) > 0:
        CenterG_X,CenterG_Y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
    else:
        print("画像が正しく認識されていないため、重心が求められません")
        CenterG_X = 0
        CenterG_Y = 0
    return CenterG_X,CenterG_Y

#1.画像（二値化画像）から、重心を探す
def centerGwithImg(img_binary):
    mu = cv2.moments(img_binary, False)
    if (mu["m00"]) > 0:
        CenterG_X,CenterG_Y = int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"]) #重心座標計算式 
    else:
        CenterG_X = 0
        CenterG_Y = 0
    return CenterG_X,CenterG_Y,mu["m00"]#重心座標

#画像ファイルにある特定の大きさの物体座標を返す関数
# 戻り値 = (全ての輪郭座標,左上座標、画像幅、画像高さ、輪郭の面積,numpy二値化画像(inrangeで処理済))
# 引数 = (画像,bgr値最低値,bgr値最高値,最低面積値)
def getContourOfPic(img_np,bgrLower,bgrUpper,minArea,maxArea):
    import time
    sTime = time.time()
    img_binary = cv2.inRange(img_np,bgrLower,bgrUpper)
    cv2.imshow("img_binary",img_binary)
    cv2.waitKey(0)
    contours,_ = cv2.findContours(img_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cam_width,cam_height= img_binary.shape #幅、高さを取得
    img =np.ones((cam_width,cam_height),np.uint8)*255 #例外処理
    campas = np.ones((cam_width,cam_height),np.uint8)*255 #minAreapy.ndarray配列を使ってキャンパス画像作成
    all_XY = []
    upLeft_X = []
    upLeft_Y = []
    width = []
    height = []
    area = []

    for x in range(int(len(contours))):
        if  maxArea >= cv2.contourArea(contours[x]) >= minArea:
            img =  cv2.drawContours(campas,contours[x],-1,(0,0,0),1)
            areaa = cv2.contourArea(contours[x])
            all_XY.append(contours[x]) 
            area.append(areaa)
            xx,yy,w,h= cv2.boundingRect(contours[x]) #物体の左上座標を取得する
            upLeft_X.append(xx)
            upLeft_Y.append(yy)
            width.append(w)
            height.append(h)
    print(str("面積"),minArea,str("以上の輪郭数:"),len(area))
    cv2.imshow("window",img)
    cv2.waitKey(0)
    eTime = time.time()
    print("find_corXandY Time:",(eTime - sTime))
    return all_XY,upLeft_X,upLeft_Y,width,height,area,img_binary

#撮影し、画像を保存する。savefile_nameは、画像の保存名、outdirは画像出力先
def filmAndSave(savefile_name,outDir):
    import winsound
    from playsound import playsound
    import random
    import CheckErr
    import os
    print("カメラデバイスを起動中です")
    #カメラの設定　デバイスIDは0
    cap = cv2.VideoCapture(0)
    n = 0

    print("撮影:Spaceキー,終了:Escキー")
    #繰り返しのためのwhile文
    while True:
        #カメラからの画像取得
        ret, frame = cap.read()
        #カメラの画像の出力
        cv2.imshow('camera' , frame)
        key =cv2.waitKey(5)
        #繰り返し分から抜けるためのif文
        if key == 32:
            cv2.imwrite(outDir+savefile_name+str(n)+".jpg",frame)
            CheckErr.checkfile(outDir+savefile_name+str(n)+".jpg") 
            num = random.randint(0,10)
            if num <= 8:
                winsound.Beep(1000,500)
            elif num <= 9:
                playsound("D:\Program\Python\PotatoProject\Prog\Sound\kasha.mp3")
            else:
                playsound("D:\Program\Python\PotatoProject\Prog\Sound\poyon.mp3")
            n = n+1
        elif key == 27:
            break
    print("撮影が終了しました。")

    #メモリを解放して終了するためのコマンド
    cap.release()
    cv2.destroyAllWindows()
    
def resize(imgfile,width,height):
    img = cv2.imread(imgfile)
    size = (width,height) #幅、高さの順でリサイズ
    img_resize = cv2.resize(img,size)
    return img_resize

def cutImgSave_fromCs(img_np,CsList:list,MINAREA:int,MAXAREA:int,SAVEDIR:str,SAVENAME:str):
    import os
    #各座標、高さ、幅を格納する２次元リスト
    xywhList = [[0]*4]
    #保存フォルダ作成
    dirr = SAVEDIR+"/Cut/"
    if not os.path.exists(dirr):
        os.mkdir(dirr)
    ##背景色変更（指定がある場合のみ)  
    for xx,cs in enumerate(CsList):
        area = cv2.contourArea(cs)
        if MINAREA < area <MAXAREA:
            x,y,w,h = cv2.boundingRect(cs)
            ImgCut_Np = img_np[y:y+h,x:x+w]
            cv2.imwrite(dirr+SAVENAME+"_"+str(xx)+".jpg",ImgCut_Np)
            xywhList.append([x,y,w,h])           
    del xywhList[0]#先頭部分を削除
    return xywhList 


