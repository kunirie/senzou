import cv2 
import math

def header(input_file): # NCプログラムのヘッダー部分
    file.write('%\n')
    file.write('O0031\n')
    file.write('G90G54G1F400\n')
    file.write('G0G43Z200.0H32\n')
    file.write('G0X0Y0\n')
    file.write('S8000M3\n')

def footer(input_file): # NCプログラムのフッター部分
    file.write('G0Z200.0M5\n')
    file.write('M30\n')
    file.close()

Zmax=0 # 最大Z高さ
Zmin=-0.1333 #　最小Z高さ
pik=0.1 # 1ピクセルを何ミリにするかを設定
pit=0.461 #微小山のピッチ
Ap_Z=5.0 #　アプローチ高さ

img = cv2.imread('onsen.bmp') # 画像の読込
gry=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) # グレイスケールに変換
height1,width1= gry.shape # 画像の高さと幅を変数にセット
file = open('design1.NC', 'w') # 書き込みファイルを設定
header(file) # NCプログラムのヘッダー部分をファイルに書き込み

wid = width1*pik #加工する幅
N=math.ceil(wid/pit) #微小谷の本数（切り上げ）

for i in range(1,N) : # X方向のループ
    Command1=['X',str(round(i*pit+pit*(1/2),3)),'\n']
    file.writelines(Command1)
    Command2=['G0Z',str(Ap_Z),'\n']
    file.writelines(Command2)
    file.write('G1')
    for j in reversed(range(0,height1)): # Y方向のループ
         color1=(gry[j,4*(i+1)]) #各ピクセルの濃淡情報を変数にセット
         Z1=(Zmax-Zmin)*(255-color1)/255+Zmin #濃淡情報を高さ情報に変換(黒が最大値)
         j1=height1-1-j
         Command3=['Y',str(round(j1*pik,3)),'Z',str(round(Z1,3)),'\n']
         file.writelines(Command3)
    file.writelines(Command2)

footer(file) # NCプログラムのフッター部分をファイルに書き込み

#1ピクセルの大きさ小さく
#ピクセルの間引き
#90度のエンドミル