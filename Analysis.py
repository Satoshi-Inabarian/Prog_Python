def getPerInner(C_Base,C_Outside):
    numall = len(C_Base)
    numout = len(C_Outside)
    numinn = numall-numout
    PerInner = round(numinn/numall,2)
    return PerInner
    
#引数＝getPerInnerで取得した内在率と、最低内在率、対象となる傷のインデックス（配列番号）
#戻り値 = judge_flag,flag"Go"のときのインデックス番号(配列番号)
def judgeInOut(PerInner,MinPerInner,Index):
    Judge_Flag = "NotGo"
    if PerInner > MinPerInner:
        Judge_Flag = "Go"
        return Judge_Flag,Index
    else:
        return Judge_Flag,Index

def DeleteList(DelIndex,DelList):
    if len(DelIndex)>0:
        for x in sorted(DelIndex, reverse=True): #末尾から削除することで、ずれを気にせず、リストの要素を全部削除する
            del DelList[x]
        return DelList
    else:
        return DelList