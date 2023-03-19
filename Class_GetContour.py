import cv2
import numpy as np
import sys

class getContour:
    
    #メンバ変数(クラス内変数)
    #初期設定
    MAXAREA = int(200) #面積振り分け最小初期値
    MINAREA = int(5000)#面積振り分け最大初期値
    MIN_WHITE_AREA = int(200) #白傷最低面積 #最大面積値の0.4～0.6%
    MAX_WHITE_AREA = int(4000) #白傷最大面積
    MIN_BLACK_AREA = int(300) #黒傷最低面積値 #最大面積値の0.4～0.6%
    MAX_BLACK_AREA = int(5000) #黒傷最大面積値
    Campas = np.ones((460,680),np.uint8)*255 #描写用キャンパス
    Cscolor = (0,0,0) #描写用の色
    
    #コンストラクタ
    def set(self, MAXAREA,MINAREA,MIN_WHITE_AREA, MAX_WIHTE_AREA,MIN_BLACK_AREA,MAX_BLACK_AREA,SMALLSCALE,CsColor,Campas):
        self.MAXAREA = MAXAREA
        self.MINAREA = MINAREA
        self.MIN_WHITE_AREA = MIN_WHITE_AREA
        self.MAX_WHITE_AREA = MAX_WIHTE_AREA
        self.MIN_BLACK_AREA = MIN_BLACK_AREA
        self.MAX_BLACK_AREA = MAX_BLACK_AREA
        self.SMALLSCALE = SMALLSCALE
        self.Cscolor = CsColor
        self.Campas = Campas

    def findObject(self,ImgHsv_Np,BGRLOW,BGRUPP,MINAREA,MAXAREA):
        CsList = []
        Img_Binary = cv2.inRange(ImgHsv_Np,BGRLOW,BGRUPP)
        Cs,_ = cv2.findContours(Img_Binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for C in Cs:
            Area = cv2.contourArea(C)
            if MINAREA < Area < MAXAREA:
                CsList.append(C) 
        return CsList
          

    def findScar(self,Img_Np,ImgHsv_Np,BGRLOW,BGRUPP,ScarType:str):
        Cs = []
        ScarCnt = 0
        ImgBinary_Hsv = cv2.inRange(ImgHsv_Np,BGRLOW,BGRUPP)
        cv2.imshow("",ImgBinary_Hsv)
        cv2.waitKey(0)
        Cs_Hsv,_ = cv2.findContours(ImgBinary_Hsv,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
        if ScarType == "White":
            MAXAREA = self.MAX_WHITE_AREA
            MINAREA = self.MIN_WHITE_AREA
            Cscolor = (255,255,255)
        elif ScarType == "Black":
            MAXAREA = self.MAX_BLACK_AREA
            MINAREA = self.MIN_BLACK_AREA
            Cscolor = self.Cscolor
        else:
            print("分析の最低・最大面積値が指定されていません。初期値が使用されています。")
        for x in range(int(len(Cs_Hsv))):
            Area = cv2.contourArea(Cs_Hsv[x])
            if MAXAREA >= Area > MINAREA:
                xx,yy,w,h= cv2.boundingRect(Cs_Hsv[x]) 
                #画像表示#
                Img_Np = cv2.rectangle(Img_Np,(xx,yy),(xx+w,yy+h),Cscolor, thickness=1) 
                Img_Np = cv2.putText(Img_Np,str(Area), (xx,yy), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0),1, cv2.LINE_AA)                       
                ##画像表示#
                ScarCnt = ScarCnt + 1
                Cs.append(Cs_Hsv[x])
                Img_Cs = cv2.drawContours(self.Campas,Cs_Hsv[x],-1,(0,0,0),1)
        return Cs,ScarCnt,Img_Np

    def getInner5pt(self,Cs):
        Centers = []
        if len(Cs) > 0: #バグ処理
            for C in Cs:
                mu = cv2.moments(C) #重心取得
                x,y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
                Retval = cv2.pointPolygonTest(C,(x,y),False)
                if Retval > 0: #外側の重心を除外する
                    xy = (x,y)
                    Centers.append(xy)
            Centers = np.array(Centers)
            #https://teratail.com/questions/196189 argmin()を利用して、最小値の配列番号を取得する
            # 方法1: numpy の indexing でやる方法
            Lefts = np.array([C[C[..., 0].argmin()] for C in Cs])
            Rights = np.array([C[C[..., 0].argmax()] for C in Cs])
            Ups = np.array([C[C[..., 1].argmin()] for C in Cs])
            Downs = np.array([C[C[..., 1].argmax()] for C in Cs])
            Lefts = np.squeeze(Lefts)  
            Rights = np.squeeze(Rights) 
            Ups = np.squeeze(Ups)  
            Downs = np.squeeze(Downs) 
            if len(Centers) < 1:#バグ処理
                pt5 = np.block([[Lefts],[Rights],[Ups],[Downs]])#２次元配列を結合
            else:
                pt5 = np.block([[Centers],[Lefts],[Rights],[Ups],[Downs]])#２次元配列を結合
            cv2.waitKey(0)
            return pt5
        else:
            pt5 = []
            return pt5
        
    def getInnerCircle(self,Img_Np,SMALLSCALE = int(0.8)):
        LOWER = np.array([0,0,100]) #黒を除外
        UPPER = np.array([100,255,255]) #白を除外
        ImgBinary = cv2.inRange(Img_Np,LOWER,UPPER)
        Cs,_ = cv2.findContours(ImgBinary,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
        MaxCs = max(Cs, key=lambda x: cv2.contourArea(x))#面積が最大の輪郭を取得
        xx,yy,w,h = cv2.boundingRect(MaxCs)
        CenterX = (xx+round(w/2)) #中心座標
        CenterY = (yy+round(h/2))
        if SMALLSCALE> 1:
            print("スケールは１(=100%)以下で設定してください。")
            sys.exit(1)
        CampasB = np.zeros(Img_Np.shape, dtype=np.uint8)#マスク画像作成用
        ImgMask = cv2.ellipse(CampasB,((CenterX,CenterY),(round(w*SMALLSCALE),round(h*SMALLSCALE)),0),(255,255,255),-1) 
        ImgGray = cv2.cvtColor(ImgMask, cv2.COLOR_BGR2GRAY) #輪郭取得用にグレースケール化
        CInner,_ = cv2.findContours(ImgGray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        if len(CInner) == 1:
            cv2.waitKey(10)
        else:
            print("getInnerCircleの輪郭座標取得に問題が発生しています。")
        Img_inner = Img_Np & ImgMask
        return Img_inner,CInner

    def getScarPosition(self,CInner,WScarC,BScarC):
        Cs = []
        Cs.append(CInner)
        Cs.append(WScarC)
        Cs.append(BScarC)
        for _,C in enumerate(Cs):
            Img_C = cv2.drawContours(self.Campas,C,-1,(0,0,0),1)
        for x,wcon in enumerate(WScarC): #白傷テキスト書き込み
            x = wcon[0][0][0] #x座標
            y = wcon[0][0][1] #y座標        
            Img_C = cv2.putText(Img_C,"W",(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2,cv2.LINE_4)
        for x,bcon in enumerate(BScarC): #白傷テキスト書き込み
            x = bcon[0][0][0] #x座標
            y = bcon[0][0][1] #y座標        
            Img_C = cv2.putText(Img_C,"B",(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2,cv2.LINE_4)
        return Cs,WScarC,BScarC


    #白傷、黒傷内側、外側判定
    #外側座標群,外側判定を受けた座標の配列番号 = getContourOutsiders(判定基準の座標（１つ）、ターゲット座標群（複数）)
    def getCs_Outsider(self,C_Base,Cs_Target):
        Cs_Outsider = []
        Index = []
        if len(Cs_Target) > 0: #例外処理
            for x,C in enumerate(Cs_Target):
                Pt_Outsider = [] #リセット
                for t,pt in enumerate(C):#座標抽出                   
                    measureDist = False
                    #pointPolygontestの引数として、typeをintに変更する
                    Pt_X= pt[0][0]; Pt_Y = pt [0][1]
                    Pt_X = int(Pt_X); Pt_Y = int(Pt_Y)
                    Pt_XY = (Pt_X,Pt_Y)
                    Retval = cv2.pointPolygonTest(C_Base[0],Pt_XY,measureDist)                    
                    if Retval < 0:#retval=-1は、外側座標のフラグ。 
                        Pt_Outsider.append(pt)#外側輪郭座標の抽出
                if len(Pt_Outsider) >=1: #バグ処理
                    Index.append(x) #外側座標が見つかったインデックス（配列番号)
                    Cs_Outsider.append(Pt_Outsider)
        return Cs_Outsider,Index
    #measureDist=False の場合、点が輪郭の内側の場合は +1、輪郭の境界線上の場合は 0、輪郭の外側の場合は -1 を返す。 
    #measureDist=True の場合、点と輪郭との距離を返す。点が輪郭の内側の場合は正の値、輪郭の境界線上の場合は 0、輪郭の外側の場合は負の値を返す。

    def getPt_Outside(self,C,pt):
        measureDist = False
        #pointPolygontestの引数として、typeをintに変更する
        Pt_X= pt[0][0]; Pt_Y = pt [0][1]
        Pt_X = int(Pt_X); Pt_Y = int(Pt_Y)
        Pt_XY = (Pt_X,Pt_Y)
        Retval = cv2.pointPolygonTest(C,Pt_XY,measureDist)
        return Retval,Pt_XY

    def disConnect(self,Img_Np):
        CsList = []

        #二値化
        img_hsv = cv2.cvtColor(Img_Np,cv2.COLOR_BGR2HSV)
        img_binary = cv2.inRange(img_hsv,(0,0,100),(255,175,255)) #
        #img_binary = cv2.cvtColor(Img_Np,cv2.COLOR_BGR2GRAY)
        #_,img_binary = cv2.threshold(img_binary,0,255,cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        img_binary = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel, iterations=3) 
        sure_bg = cv2.dilate(img_binary,kernel,iterations = 3)
        dst= cv2.distanceTransform(img_binary,cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dst, 0.01* dst.max(), 255, cv2.THRESH_BINARY)
        sure_fg = sure_fg.astype(np.uint8)  
        unknown = cv2.subtract(sure_bg,sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers += 1
        markers[unknown == 255] = 0
        
        # watershed アルゴリズムを適用する。
        markers = cv2.watershed(Img_Np, markers)
        labels = np.unique(markers)
        CsList = []
        for label in labels[2:]:  # 0:背景ラベル １：境界ラベル は無視する。
            target = np.where(markers == label, 255, 0).astype(np.uint8)
            contours,_ = cv2.findContours(target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            CsList.append(contours[0])
        #Img_Cs = cv2.drawContours(Img_Np, CsList, -1, color=(0, 0, 255), thickness=1)
        #cv2.imshow("",Img_Cs)
        #cv2.waitKey(0)
        return CsList,Img_Np