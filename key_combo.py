# -*- coding: utf-8 -*-
import pyxhook
import time
import tkinter as tk
import sys
import pygame.mixer
from time import sleep

start = 0#コンボ間の時間計測開始時間
end = 0#コンボ間の時間計測終了時間
behaind = 5.0#コンボが続く時間
combo = 0#何コンボかを示す変数
args = sys.argv#効果音が必要な場合はプログラム引数を'-s'で実行
hiscore = 0#現状のハイスコアを格納
F = open('key_combo_ranking.txt','a')#ハイスコアを格納しているファイルを読み込む
F.close()

try:
    if(args[1] == '-s'):
        pygame.mixer.init()#効果音使用するための設定
        pygame.mixer.music.load('key_sound.mp3')#効果音の読み込み
except IndexError:
    pass

def kb_down_event(event):#キーが押されたときの処理
    global end
    global args
    try:
        if(args[1] == '-s'):
            pygame.mixer.music.play()
    except IndexError:
        pass
    end = time.time()#時間を記録

def kb_up_event(event):
    global start
    global end
    global behaind
    global combo
    global hiscore
    
    if (end - start <= behaind):#記録した時間と比較し,コンボを追加するか，ハイスコアとして格納する
        combo += 1
    else:
        if(int(hiscore)<int(combo)):
            hiscore = combo
        combo = 1
    #print(combo)
    label_combo['text'] = str(combo)#テキストラベルを更新する
    start = time.time()
    if(combo < 30):#30コンボ以上で色を変える
        label_combo['fg'] = 'black'
        label['fg'] = 'black'
    elif(combo < 60):
        label_combo['fg'] = 'cyan'
        label['fg'] = 'cyan'
    elif(combo < 90):
        label_combo['fg'] = 'pink'
        label['fg'] = 'pink'
    else:
        label_combo['fg'] = 'red'
        label['fg'] = 'red'
    if(combo % 10 == 0 and combo > 0 and behaind > 0.5):#10コンボおきにコンボ継続時間を0.3秒短くする
        behaind -= 0.3
    elif(combo == 1):#コンボがコンボ継続時間を切れたら元に戻す
        behaind = 5.0

def end_of_combo(event):#アプリを終了する時の処理
    global root
    global hiscore
    File = open('key_combo_ranking.txt','r')#ハイスコアを格納しているファイルを読み込む
    ranking = File.readlines()
    File.close()
    score = label_combo['text']#現在のコンボ数を見る
    if(int(score)>int(hiscore)):#もっとも大きいコンボを今回の記録として保存する.
        hiscore = score
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
    ranking.insert(i,str(hiscore))
    ranking_frame = tk.Canvas(root,width=100,height=130)
    ranking_frame.create_rectangle(0, 0, 100,130 , fill = 'gray')
    if(i+1 <= 10):
        r_label =tk.Label(ranking_frame,text = str(i+1)+'位',font=('System',40))
        r_label.place(x=7,y=10)
    else:
        r_rabel = tk.Label(ranking_frame,text='ランク外',font = ('System',13))
        r_rabel.place(x=15,y=10)
    max_combo = tk.Label(ranking_frame,text='Max',font=('System',10))
    max_combo.place(x=0,y=70)
    score_label = tk.Label(ranking_frame,text = str(hiscore),font=('System',25))
    score_label.place(x=30,y=60)
    combo = tk.Label(ranking_frame,text = 'combo',font=('System,10'))
    combo.place(x=20,y=90)
    t_label = tk.Label(ranking_frame,text='5秒後に終了',font=('System',10))
    t_label.place(x=10,y=110)
    ranking_frame.place(x=0,y=0)
    File = open('key_combo_ranking.txt','w')#ファイルへ書き込み
    if(len(ranking)>10):
        del ranking[-1]
    for r in ranking:
        File.write(str(r)+'\n')
    root.update()
    time.sleep(5)#記録表示のための5秒待機
    root.destroy()#画面を消す
    hookman.cancel()#keylogerの終了
    sys.exit()#プログラムの終了

hookman = pyxhook.HookManager()
hookman.KeyDown = kb_down_event
hookman.KeyUp = kb_up_event
hookman.start()
root = tk.Tk()
root.title('combo')
root.geometry('100x130')
label_combo = tk.Label(root,text=str(combo),font=('System',50))
label_combo.pack()
label = tk.Label(root,text='Combo',font=('System',20))
label.pack()
Button = tk.Button(root,text='Exit')
Button.bind("<Button-1>",end_of_combo)
Button.pack()
root.mainloop()
