import cv2


###Pythonライブラリ###
import glob
import cv2
import numpy as np

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
##リスト宣言##
xyList_str =[]
##メイン##
print("【Start】")
counter = 0
f = open(IMGDIR+"\XYWH_DATA.txt","r")
##一行ずつ読み込み##
list = f.readlines()
##リストに格納
for s in list:
    xyList_str.append(s)
print(xyList_str[0])
#tmp = int(tmp)
#print(type(tmp))
    
    
    
#xywh_list = list(str_list)

#print(xywh_list)
#カット地点読み込み#

for Imgfile in ImgfileList:
    ImgOrg_Np = Util.resize(Imgfile,CAMPAS_WIDTH,CAMPAS_HEIGHT)
    ##じゃがいも１個体の画像##
    #for ImgP in 
print("【Task completed List Datas.")
