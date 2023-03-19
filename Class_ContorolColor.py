import numpy as np
import cv2
import sys
import statistics


class ControlColor:
    BACKCOLOR:str
    SCARTYPE:str
    
    #コンストラクタ
    def ContorolColor(self):
        self.BACKCOLOR = "None"
        self.SCARTYPE = "None"
        
    #物体背景の色を黒色にする。 戻り値は Img_np型  hsv空間処理
    #BACKCOLORは白、緑のみ 2022/12/08現在
    def toBlack(self,Img_Np,BACKCOLOR): #BACKCOLOR = 1.white,2.green 3.black
        ImgHsv = cv2.cvtColor(Img_Np,cv2.COLOR_BGR2HSV)
        if BACKCOLOR == "Green":
            BGRLOW = np.array([0,0,0]) #for BACKCOLOR = "green" 
            BGRUPP = np.array([22,255,255])
        elif BACKCOLOR == "White":
            BGRLOW = np.array([0,40,0]) #for BACKCOLOR = "white"
            BGRUPP = np.array([255,255,255])
        elif BACKCOLOR == "Black":
            BGRLOW = np.array([0,0,20]) #for BACKCOLOR = "black"
            BGRUPP = np.array([255,255,255])
        else:
            print("Not select BACKCOLOR...")
            return Img_Np
        ImgHsvMask = cv2.inRange(ImgHsv,BGRLOW,BGRUPP)
        ImgResult = cv2.bitwise_and(Img_Np,Img_Np,mask=ImgHsvMask)
        return ImgResult



    #物体背景の色を白色にする。白にする部分はcv2.OTSUを使用（後半の３行）
    def toWhite(self,Img_Np,BACKCOLOR): #BACKCOLOR = 1.white,2.green 3.black
        ImgHsv = cv2.cvtColor(Img_Np,cv2.COLOR_BGR2HSV)
        if BACKCOLOR == "Green":
            BGRLOW = np.array([0,0,0]) #for BACKCOLOR = "green" 
            BGRUPP = np.array([22,255,255])
        elif BACKCOLOR == "White":
            BGRLOW = np.array([0,40,0]) #for BACKCOLOR = "white"
            BGRUPP = np.array([255,255,255])
        elif BACKCOLOR == "Black":
            BGRLOW = np.array([0,0,20]) #for BACKCOLOR = "black"
            BGRUPP = np.array([255,255,255])
        else:
            print("Not selected BACKCOLOR...")
            return Img_Np
        ImgHsvMask = cv2.inRange(ImgHsv,BGRLOW,BGRUPP)
        # 大津二値化を使って、背景黒を白にする
        _, Binary = cv2.threshold(ImgHsvMask, 2, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # 背景を白にする。
        Img_Np[Binary == 0] = 255
        return Img_Np

    def findMostBgr_hsv(self,Img_Np):
        cv2.imshow("hsv_image",Img_Np)
        cv2.waitKey(0)
        Img_Hsv = cv2.cvtColor(Img_Np,cv2.COLOR_BGR2HSV)
        #[:,;,0]は、画像の三次元配列の最後について、rgbの配列番号 rの配列番号は0,gは1,bは2という意味
        B_Mode = statistics.mode(Img_Hsv[:,:,0].flatten())#最も使われているbgrのb数値
        G_Mode = statistics.mode(Img_Hsv[:,:,1].flatten())#g数値
        R_Mode = statistics.mode(Img_Hsv[:,:,2].flatten())#r数値
        print("最頻値【B G R】",B_Mode,G_Mode,R_Mode)
        cv2.imshow("hsv_image",Img_Hsv)
        cv2.waitKey(0)
        return B_Mode,G_Mode,R_Mode,Img_Hsv

    def findMostBgr(self,Img_Np):
        B_Mode = statistics.mode(Img_Np[:,:,0].flatten())
        G_Mode = statistics.mode(Img_Np[:,:,1].flatten())
        R_Mode = statistics.mode(Img_Np[:,:,2].flatten())
        print("最頻値【B G R】",B_Mode,G_Mode,R_Mode)
        cv2.imshow("image",Img_Np)
        cv2.waitKey(0)
        return B_Mode,G_Mode,R_Mode,Img_Np

    import numpy as np

    #2022 12月7日現在 
    #通常じゃがいもの色の抽出値 = np.array([150,135,15])
    def getBgrLowUpp_Scar(self,SCARTYPE):
        if SCARTYPE == "White":#白傷抽出、inRangeのbgr最低最大値
            BGRLOWER = np.array([0,100,0]) 
            BGRUPPER = np.array([50,255,255]) 
            return BGRLOWER,BGRUPPER
        elif SCARTYPE == "Black": #黒傷
            BGRLOWER = np.array([0,0,100]) 
            BGRUPPER = np.array([255,175,255]) 
            return BGRLOWER,BGRUPPER
        else:
            print ("please select scar type 1:White.2:Black")
            sys.exit()

    def getBgrLowUpp_ChangeBkcolr(self,BACKCOLOR:str):
        if BACKCOLOR == "White":#背景白
            BGRLOW = np.array([0,40,0]) #for BACKCOLOR = "white"
            BGRUPP = np.array([255,255,255])
            return BGRLOW,BGRUPP
        elif BACKCOLOR == "Black": #黒
            BGRLOW = np.array([0,0,1]) #for BACKCOLOR = "black"
            BGRUPP = np.array([255,255,255])
            return BGRLOW,BGRUPP
        elif BACKCOLOR == "Green": #緑
            BGRLOW = np.array([0,0,0]) # for BACKCOLOR = "green"
            BGRUPP = np.array([22,255,255])
            return BGRLOW,BGRUPP
        else:
            print ("please select BACKCOLOR 1:White.2:Black,3:Green")
            sys.exit()