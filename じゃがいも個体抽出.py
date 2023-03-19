###Pythonライブラリ###
import glob
import cv2
import os

##自作クラス・ライブラリ##
import Directory as dirr
import CheckErr
import Class_ContorolColor as C_ConColor
import Util
import Class_GetContour as C_GetCs
CurDir,ImgDirr = dirr.makeCurDir()
#初期設定#
IMGDIR = "D:\Program\Python\PotatoProject\Prog\Image\Test" #分析対象画像ファイル
BACKCOLOR = "None"  #画像の背景色 1.Grenn 2.White 3.Black  Noneで背景色を変更しない
CAMPAS_WIDTH = 680 #描写、表示用のキャンパス幅と高さ //
CAMPAS_HEIGHT = 460
#エラー処理#
ImgfileList = glob.glob(IMGDIR+"\*.jpg")
CheckErr.checkfile(IMGDIR)
#インスタンス#          
getCs = C_GetCs.getContour()
ConColor = C_ConColor.ControlColor()

##メイン##
print("【Start】")
counter = 0
for Imgfile in ImgfileList:
    SAVENAME = os.path.splitext(os.path.basename(Imgfile))[0] #ファイル名テキスト形式で取得
    ImgOrg_Np = Util.resize(Imgfile,CAMPAS_WIDTH,CAMPAS_HEIGHT)
    ##背景色変更（指定がある場合のみ)  
    if BACKCOLOR =="None":
        pass 
    else:   
        ImgOrg_Np = ConColor.toWhite(ImgOrg_Np,BACKCOLOR)
    CsList,Img_Np = getCs.disConnect(ImgOrg_Np)                      
    for Cs in CsList: 
        area = cv2.contourArea(Cs)
        #1000以上が、じゃがいも個体目安  
        MINAREA = 1000
        MAXAREA = 2500         
        xywhlist = Util.cutImgSave_fromCs(ImgOrg_Np,CsList,MINAREA,MAXAREA,IMGDIR ,SAVENAME)
    counter = counter+1
    f = open(IMGDIR+"\XYWH_DATA.css","a")
    for string in xywhlist:
        f.write(int(string))
    f.write("\n")
    print("finished:"+str(counter)+"/"+str(len(ImgfileList)))
    f.close()
print("【Task completed List Datas.")

    
