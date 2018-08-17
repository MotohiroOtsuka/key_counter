# -*- coding: utf-8 -*-
import pyxhook
import time
import tkinter as tk
import sys
import pygame.mixer

count = 0
args = sys.argv

F = open('key_count_ranking.txt','a')#ハイスコアを格納しているファイルを読み込む
F.close()

try:
    if(args[1] == '-s'):
        pygame.mixer.init()
        pygame.mixer.music.load('key_sound.mp3')
except IndexError:
    pass

def kb_up_event(event):#キーを離したときを1カウントとする
    global count
    count += 1
    label_count['text'] = str(count)#カウンターをあげていく



def end_of_count(event):
    global root
    File = open('key_count_ranking.txt','r')#ハイスコアを格納しているファイルを読み込む
    ranking = File.readlines()
    File.close()
    hiscore = label_count['text']#現在のコンボ数を見る
    i = 0
    Flag = False
    j = 11
    while(i<len(ranking)):#ランキングを探索し,適切な場所に保存する（上位10個）
        ranking[i]=ranking[i].replace('\n','')
        if(int(ranking[i].replace('\n',''))<int(hiscore)):
            if(Flag == False):
                j = i
                Flag = True
            else:
                pass
        i+=1
    if(j<=10):
        i = j
    ranking.insert(i,str(hiscore))#ランキングに挿入
    ranking_frame = tk.Canvas(root,width=100,height=100)#ランキングようのフレーム作成
    ranking_frame.create_rectangle(0, 0, 100,100 , fill = 'gray')#フレームをグレーにする
    r_label =tk.Label(ranking_frame,text = str(i+1)+'位',font=('System',40))#順位ラベルをつくる
    r_label.place(x=7,y=10)
    t_label = tk.Label(ranking_frame,text='5秒後に終了',font=('System',10))
    t_label.place(x=10,y=70)
    ranking_frame.place(x=0,y=0)
    File = open('key_count_ranking.txt','w')#ファイルへ書き込み
    if(len(ranking)>10):
        del ranking[-1]
    for r in ranking:
        File.write(str(r)+'\n')
    root.update()#表示項目の更新
    time.sleep(5)#記録表示のための5秒待機
    root.destroy()#画面を消す
    hookman.cancel()#keylogerの終了
    sys.exit()#プログラムの終了

hookman = pyxhook.HookManager()#keylogerスタート準備のおまじない
hookman.KeyUp = kb_up_event#keylogerの処理
hookman.start()#keylogerスタートのおまじない
root = tk.Tk()#windowの枠組みをつくるおまじない
root.title('counter')#windowに名前をつける
root.geometry('100x100')#windownのサイズを決める
label_count = tk.Label(root,text=str(count),font=('System',25))
label_count.pack()
label = tk.Label(root,text='types',font=('System',20))
label.pack()
Button = tk.Button(root,text='Exit')
Button.bind("<Button-1>",end_of_count)
Button.pack()
root.mainloop()#windowの表示と維持