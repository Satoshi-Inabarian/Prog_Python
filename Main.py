###Pythonライブラリ###
import glob
import cv2
import time
import numpy as np 

##自作クラス・ライブラリ##
import Directory as dirr
import CheckErr
import Class_ContorolColor as C_ConColor
import Analysis
import Util
import Class_GetContour as C_GetCs
CurDir,ImgDirr = dirr.makeCurDir()
#初期設定#
IMGDIR = "D:\Program\Python\PotatoProject\Potato2022\p_R120_G130\OnlyScar" #分析対象画像ファイル
MASKDIR = ImgDirr+"/Mask" #マスク画像一時保存先
BACKCOLOR = "None"  #画像の背景色 1.Grenn 2.White 3.Black  Noneで背景色を変更しない
CIRCLESCALE = 0.8 #内接楕円の縮小割合(%)
MINPERINNER = 0.5 #楕円内にあるきずの割合(%) #これを下回る場合は判断から除外される 
CAMPAS_WIDTH = 680 #描写、表示用のキャンパス幅と高さ //
CAMPAS_HEIGHT = 460
#エラー処理#
ImgfileList = glob.glob(IMGDIR+"/*.jpg")
CheckErr.checkfile(IMGDIR)
#インスタンス#
getCs = C_GetCs.getContour()
ConColor = C_ConColor.ControlColor()


for picidx,Imgfile in enumerate(ImgfileList):
    Campas_Cs = np.ones((CAMPAS_HEIGHT,CAMPAS_WIDTH),np.uint8)*255 #直前初期設定
    Stime = time.time()
    #画像Np形式に変換
    Img_Original = Util.resize(Imgfile,CAMPAS_WIDTH,CAMPAS_HEIGHT)
    Img_Np = Util.resize(Imgfile,CAMPAS_WIDTH,CAMPAS_HEIGHT)
    ImgHsv_Np = cv2.cvtColor(Img_Np,cv2.COLOR_BGR2HSV)#HSV空間変換
    ##背景色変更（指定がある場合のみ)  
    if BACKCOLOR =="None":
        pass
    else:   
        Img_Np = ConColor.toWhite(Img_Np,BACKCOLOR)
        
    #じゃがいも分離
    CsList,_ = getCs.disConnect(Img_Np)
    MINAREA = 1000
    MAXAREA = 2500
    PList = Util.cutImgSave_fromCs(Img_Np,CsList,MINAREA,MAXAREA,IMGDIR,"scar")
    #一個体抽出
    #白傷輪郭抽出
    wlow,wupp = ConColor.getBgrLowUpp_Scar("White")
    WCsList,WCnt,Img_WithScar = getCs.findScar(Img_Np,ImgHsv_Np,wlow,wupp,"White")
    #黒傷輪郭抽出
    blow,bupp = ConColor.getBgrLowUpp_Scar("Black")
    BCsList,BCnt,Img_WithScar= getCs.findScar(Img_Np,ImgHsv_Np,blow,bupp,"Black")
    Wpt5 = getCs.getInner5pt(WCsList)
    Bpt5 = getCs.getInner5pt(BCsList)
    #pt5 = np.append(Wpt5,Bpt5, axis=0) #２次元配列の結合 axis=0で行数無視で結合できる。現在はエラー防止のため使っていない12/15
    ImgCut,CsIncircle = getCs.getInnerCircle(Img_Original,CIRCLESCALE)
    #白傷、黒傷内側、外側判定
    WIndexDel = [] #除外対象となるキズ座標の配列番号を格納する
    BIndexDel = [] 
    WCsOutsidersList,WouterIndex = getCs.getCs_Outsider(CsIncircle,WCsList)
    BCsOutsidersList,BouterIndex = getCs.getCs_Outsider(CsIncircle,BCsList)
    OutsidersList = WCsOutsidersList + BCsOutsidersList #はみだしたの輪郭座標群をまとめる
    #######白傷######     
    if len(WCsOutsidersList) >= 1:
        for x,Index in enumerate(WouterIndex):#Woutindexをもとに、外側にはみ出している傷の座標をWConListから取り出していく
            WCOutt = WCsList[Index] 
            WPerInner = Analysis.getPerInner(WCOutt,WCsOutsidersList[x]) #内在率判定。Outsiderは外側のみの座標群　Outtは内側、外側両方を含む座標群 
            Flag,Index = Analysis.judgeInOut(WPerInner,MINPERINNER,Index) #パーセントから合否判定
            if Flag == "NotGo":
                WIndexDel.append(Index) #除外判断されたものは、削除候補のリストに追加する。
    #######黒傷######
    if len(BCsOutsidersList) >= 1:
        for x,Index in enumerate(BouterIndex):
            BCOutt = BCsList[Index] 
            BPerInner = Analysis.getPerInner(BCOutt,BCsOutsidersList[x]) 
            Flag,Index = Analysis.judgeInOut(BPerInner,MINPERINNER,Index)
            if Flag == "NotGo":
                BIndexDel.append(Index) 
    
    ###########################画像表示用#########################
    Img_WithScar = cv2.drawContours(Img_WithScar,CsIncircle,-1,(0,0,255),1)
    Img_Cs = cv2.drawContours(Campas_Cs,CsIncircle,-1,(0,0,0),1)
    Img_Cs = cv2.drawContours(Img_Cs,WCsList,-1,(0,0,0),1)
    Img_Cs = cv2.drawContours(Img_Cs,BCsList,-1,(0,0,0),1)
    ###########################画像表示用#########################
    
    
    WCsList = Analysis.DeleteList(WIndexDel,WCsList)
    BCsList = Analysis.DeleteList(BIndexDel,BCsList)
    ScarCsList = WCsList + BCsList
    
    ###########################画像表示用#########################
    if len(Wpt5) > 0:
        for pt in Wpt5:
            Img_Cs = cv2.circle(Img_Cs,center=pt,radius=2,color=(0,0,255),thickness=-1)
    if len(Bpt5) > 0:
        for pt in Bpt5:
            Img_Cs = cv2.circle(Img_Cs,center=pt,radius=2,color=(0,0,255),thickness=-1)
    for Index,C in enumerate(ScarCsList):
        xx,yy,w,h = cv2.boundingRect(C) 
        Img_Cs = cv2.putText(Img_Cs,str("In"), (xx-5,yy-5), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255),1, cv2.LINE_AA)  
    ###########################画像表示用#########################
    
    
    
    ##画面上確認する場合##
    cv2.imshow("picture"+str(picidx)+":original",Img_Original)
    cv2.waitKey(0)
    cv2.imshow("scarimg",Img_WithScar)
    cv2.waitKey(0)
    cv2.imshow("judgeInorOut",Img_Cs)
    cv2.waitKey(0)
    Etime = time.time()
    Tim = Etime - Stime 
    print("time",Tim)


    
