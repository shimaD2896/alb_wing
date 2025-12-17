# -------------------------------------------------------------------------
# 使いかた
# 下記Directoryに翼型をすべていれておく。必要に応じて変える。
# 翼型は 後縁->上->前縁->下->後縁 の順になっていることを確認
# 翼弦長などの定義に注意
# 三角肉抜きが変な形になるときは、w_triやr_triを小さく調整するとよい
# ただし、小さくしすぎるとリブが折れるかもしれないので気を付ける

# 使いかたおわり
# ----------------------------------------------------------------------------------------
# 設定

# ファイル関連
# 出力するテキストファイルの名前。拡張子は不要
ProjectName = "0wingpenguin_test"
# 翼型を保管しておき、コマンドファイルを出2024詩集版力するディレクトリのPath
Directory = r"C:\Users\islan\OneDrive - OUMail (Osaka University)\ribwriting"

# 翼関連
# 端、根の翼弦長(流れ方向)[mm]
RootChord =749.49
EndChord = 465
# 端、根のねじり上げ(流れ方向)[°]
RootDelta = 0
EndDelta = -2
# 端、根の桁位置[%]
RootR = 37
EndR = 37
# 端、根の翼型のファイル名 datファイルを入れる
RootFoilName = "DAE-41.dat"
EndFoilName = "DAE-41.dat"
# リブ枚数(1つの翼に立てる枚数)
n = 17
# 分割してリブを出力
isUseBunkatuShuturyoku = True
startRib = 1 # 何枚目から出力を行うか
endRib = 17  # 何枚目まで出力するか
# 何翼?
PlaneNumber = "0"
# 半リブあり?
use_half = True
# 半リブは今回同時に出力するリブの何枚目か
halfRibNumber = [3,5,7,9,11,13,15,17]
# 上反角を付けるために桁をy軸方向へ移動させるか？
use_JouhannkakuChousei = False
# 各リブのy軸の移動量をxに対応する翼厚みに対する％でリスト形式で渡す
y_chousei = [0, 1, 2]
#後縁前端止めの有無
zenntanndome = True
#リブキャップ止めの有無
ribcapddome = False
#🐧たちが被らないように調整
zurashi_x = 200

# リブ以外の要素関連
# プランク厚さ[mm]
tp = 2
# リブキャップ厚さ[mm]
tu = 0.03
td = 0.03
# ストリンガー断面の一辺[mm](翼弦垂直方向)
e = 5
# 下面のリブキャップをどれだけオフセットするか
e1 = td

# 桁径[mm]	楕円の短軸方向
d = 61.396
# 桁径		楕円の長軸-短軸 円なら0
dd = 61.396- d
# アセンブリ棒径[mm]
da = 30  # 元は30
# アセンブリ棒余白[mm]
h = 7
# 後縁材の前縁側の辺の長さ[mm]
htu = 8  # 元は8
htd = 8

# 前縁材があるか boolean
use_l = False
# 前縁材の端線、水平線,offset線の出力
use_la = False
# 前縁材と翼型の前縁のずれ[mm]
lo = 10
# 前縁材のoffset[mm]
offset_l = 1
# 三角肉抜き最小骨格幅[mm]
w_tri = 15
# 三角肉抜き端半径[mm]
r_tri = 10
# 前縁-肉抜き 長さ[%]
first_light_r = 10
# 丸肉抜き 最小骨格幅[mm]
w_circle = 15

# 位置関連
# 主翼用設定値
# # # プランク上開始位置[%]
rpu = 63
# # プランク下開始位置[%] r plank downside
rpd = 14

# # 尾翼用設定値
#rpu = 30
# プランク下開始位置[%] r plank downside
#rpd = 30

# ストリンガー下後縁側位置[%] r stringer downside trailing edge #半リブの切り取り線に依存
rsdt = rpd + 20
# ストリンガー前縁[mm] x stringer leading edge
xsl = 20 + e

# 設定値はあざみ野の翼を参考にしている

# 主翼0-4翼設定
# # リブキャップを🐧のどこまでのばすか[mm]
length_of_adribcapd = 20

# # 尾翼用
# ストリンガー位置翼上部[%]
#stringerU1Rate = 4
#stringerU2Rate = 10
#stringerU3Rate = 65
# ストリンガー位置翼下部[%]
#stringerD1Rate = 4
#stringerD2Rate = 10
#stringerD3Rate = 65

# # 5翼用
# # 設定値はあざみ野の翼を参考にしている
# # ストリンガー位置翼上部[%]
# stringerU1Rate = 6
# stringerU2Rate = 53
# stringerU3Rate = 99
# # ストリンガー位置翼下部[%]
# stringerD1Rate = 6
# stringerD2Rate = 99
# stringerD3Rate = 20.5



##リブガキの際の分割数を指定
# 基本は200、数が大きいほど精密なリブが書けるが大きくし過ぎるとエラー
bunnkatyu = 200


# 機体諸元
# 0翼取り付け角[°]
alpha = 0
# 後退角(リブ厚みの修正用)[°]
sweep = 0

# 設定おわり
# ------------------------------------------------------------------------------------------
# 準備

import os
import numpy

# import matplotlib.pyplot as pyplot
import scipy.interpolate as interp
import scipy.optimize as optimize
import sympy

inter = interp.Akima1DInterpolator
import math

sin, cos, tan, atan2 = (math.sin, math.cos, math.tan, math.atan2)
from scipy.optimize import fsolve
import warnings
import csv
import time

os.chdir(Directory)  # ディレクトリ移動

# ライブラリおわり
# ----------------------------------------------------------------------------------------
# 関数、クラス定義


class vector:
    """(x,y,z)の点、ベクトル
    z=0 がデフォルト
    v + w, v - w, v*k, v/k は通常の定義済み　ただし*、/の前はベクトル
    v @ w　は内積、v * wは外積
    abs(v)　はvの大きさ
    .iで反時計回りに回転
    """

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        if self.z == 0:
            return "({}, {})".format(self.x, self.y)
        else:
            return "({}, {}, {})".format(self.x, self.y, self.z)

    def __repr__(self):
        if self.z == 0:
            return "vector({}, {})".format(self.x, self.y)
        else:
            return "vector({}, {}, {})".format(self.x, self.y, self.z)

    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, k):  # 入力により実数倍か外積を返す
        if type(self) == vector and type(k) != vector:
            return vector(self.x * k, self.y * k, self.z * k)
        elif type(self) == vector and type(k) == vector:
            return vector(
                self.y * k.z - self.z * k.y,
                -self.x * k.z + self.z * k.x,
                self.x * k.y - self.y * k.x,
            )

    def __matmul__(self, other):  # 内積
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __truediv__(self, k):
        return vector(self.x / k, self.y / k, self.z / k)

    def __abs__(self):
        return (self @ self) ** (1 / 2)

    @property
    def i(self):
        return vector(-self.y, self.x)

    def rotate(self, angle, unit="degree"):
        """
        ベクトルvを反時計回りにangleだけ回転させる
        angleの単位はunitを"degree"か"radian"にして指定
        """
        if unit == "degree":
            angle *= numpy.pi / 180
        elif unit == "radian":
            pass
        else:
            print("単位が不正です")
            raise ValueError("単位が不正です")
        return vector(
            self.x * cos(angle) - self.y * sin(angle),
            self.x * sin(angle) + self.y * cos(angle),
        )


class stringer:
    """
    ストリンガーを図のように定義できる。これをそのまま用いてコマンドも出力できる。
    Aを一点に持つ。Pで方向を決める。eは一辺。RがFalseならそのまま、Trueなら反転。
    A、Pはvectorオブジェクト
    .A、.B、.C、.Dがそれぞれの点
    """

    def __init__(self, A, P, e, R=False):
        self.A = A
        self.P = P
        self.e = e
        self.R = R

    @property
    def AB(self):
        return (self.P - self.A) / abs(self.P - self.A) * self.e  # ABベクトル

    @property
    def B(self):
        return self.A + self.AB

    @property
    def D(self):
        ABVec_e = self.AB / abs(self.AB)
        ABVecForLineAD = (
            ABVec_e * e1
        )  # ABベクトルの長さをe1へ、これを回転させてADベクトルを作る
        if not self.R:
            return self.A + ABVecForLineAD.i
        else:
            return self.A - ABVecForLineAD.i

    @property
    def C(self):
        return self.B + self.D - self.A


class circle:
    """
    円の半径と中心を保持するオブジェクト
    """

    def __init__(self, r, O):
        self.r = r
        self.O = O


class ellipse:
    """
    中心座標C、長軸上の一点P、短軸と中心の距離b を保持するオブジェクト
    """

    def __init__(self, C, P, b):
        self.C = C
        self.P = P
        self.b = b


def spline(file, l, O=vector(0, 0)):
    """
    リストl=[vector,vector,...]のspline曲線を描くコマンドをfileに出力
    Oに原点を移して描ける
    """
    file.write("spline\nm\nf\nk\nc\n")  # spline設定
    for P in l:
        file.write("{},{}\n".format(P.x + O.x, P.y + O.y))
    file.write("\n")


def line(file, P1, P2, O=vector(0, 0)):
    """
    点P1,P2(vector)を結ぶ線分を描くコマンドをfileに出力
    """
    file.write(f"line\n{P1.x+O.x},{P1.y+O.y}\n{P2.x+O.x},{P2.y+O.y}\n\n")


def WriteEllipse(file, ell, O=vector(0, 0)):
    file.write(
        f"ellipse\nc\n{ell.C.x+O.x},{ell.C.y+O.y}\n{ell.P.x+O.x},{ell.P.y+O.y}\n{ell.b}\n"
    )

def WriteARC(file, center, P1, P2, O=vector(0,0)):
    """中心center、始点P1、終点P2の円弧を描くコマンドをfileに出力"""
    file.write(
        f"arc\n_c\n{center.x+O.x},{center.y+O.y}\n{P1.x+O.x},{P1.y+O.y}\n{P2.x+O.x},{P2.y+O.y}\n\n"
    )

def fillet(file, P1, P2, r, O=vector(0,0)):
    """三角肉抜き穴の角を丸めるコマンドをfileに出力
    P1,P2をそれぞれ通る線の角を半径rで丸める"""
    file.write(
        f"fillet\n_r\n{r}\n{P1.x+O.x},{P1.y+O.y}\n{P2.x+O.x},{P2.y+O.y}\n"
    )
    
def WriteCircle(file, circle, O=vector(0, 0), WriteCenter=True):
    """circleオブジェクトを出力するコマンドを出力"""
    file.write(
        """circle
{xc},{yc}
{r}
""".format(
            xc=circle.O.x + O.x, yc=circle.O.y + O.y, r=circle.r
        )
    )
    if WriteCenter:
        line(file, circle.O + vector(0, 5), circle.O + vector(0, -5), O)
        line(file, circle.O + vector(5, 0), circle.O + vector(-5, 0), O)


def div_P(P1, P2, known, index):
    """
    P1,P2を結ぶ直線上にP3があってP3.index=knownがわかっているとき、その点をvectorとして返す。
    index=0のときx、1のときy
    """
    if index == 0:
        return div_P2(P1, P2, (known - P1.x) / (P2.x - P1.x))
    if index == 1:
        return div_P2(P1, P2, (known - P1.y) / (P2.y - P1.y))


def div_P2(P1, P2, ratio):
    """
    P1,P2をP1P2:P1P3=1:ratioに内分、外分する点P3の座標をvectorとして返す。
    """
    return P1 + (P2 - P1) * ratio


def WriteStringer(file, stringer, O=vector(0, 0)):
    """上のstringerを入力にしてこれを描くコマンドを出力"""
    line(file, stringer.D, stringer.A, O)
    line(file, stringer.C, stringer.B, O)
    file.write(
        """line
{ax},{ay}
{dx},{dy}

""".format(
            ax=stringer.A.x + O.x,
            ay=stringer.A.y + O.y,
            dx=stringer.D.x + O.x,
            dy=stringer.D.y + O.y,
        )
    )


def offset(l, t, updown, end=0):
    """
    l=[vector,...]をtだけずらした点のリストを出力。
    endが0のとき、最初、最後の点は除かれる。つまり、出力は元のリストより要素が2つすくない。
    endが1のときは全ての点が残る。端の点は端から2番目の点との傾きを使う。
    点の向きに対して左にずらすときupdown=0、右にずらすとき1。
    """
    ret = []
    i = 1
    while i + 1 < len(l):
        ret.append(
            (l[i + 1] - l[i - 1]).i / abs(l[i + 1] - l[i - 1]) * t * (-1) ** updown
            + l[i]
        )
        i += 1
    if end == 1:
        ret = (
            [(l[1] - l[0]).i / abs(l[1] - l[0]) * t * (-1) ** updown + l[0]]
            + ret
            + [(l[-1] - l[-2]).i / abs(l[-1] - l[-2]) * t * (-1) ** updown + l[-1]]
        )
    return ret


def color(file, r, g, b):
    """
    r,g,bで次から出力するオブジェクトの色を変えるコマンドをfileに出力
    """
    file.write(f"-color\nt\n{r},{g},{b}\n")


def to_vectors(array):
    """numpyで書かれた配列をvectorのリストに直して返す"""
    return [vector(P[0], P[1]) for P in array]


def to_vectors2(numpy_x, numpy_y):
    """numpyで書かれた配列をvectorのリストに直して返す"""
    ret = [vector(numpy_x[i], numpy_y[i]) for i in range(len(numpy_x))]
    return ret


def to_numpy_x(vectors):
    """numpyで書かれた配列をvectorのリストに直して返す"""
    ret = numpy.zeros(len(vectors))
    for i in range(len(vectors)):
        ret[i] = vectors[i].x
    return ret


def to_numpy_y(vectors):
    """numpyで書かれた配列をvectorのリストに直して返す"""
    ret = numpy.zeros(len(vectors))
    for i in range(len(vectors)):
        ret[i] = vectors[i].y
    return ret


def to_numpy(vectors):
    """numpyで書かれた配列をvectorのリストに直して返す"""
    ret = numpy.zeros((len(vectors), 2))
    for i in range(len(vectors)):
        ret[i][0] = vectors[i].x
        ret[i][1] = vectors[i].y
    return ret


def relation(Ps, r, O):
    """
    半径r、中心Oの円とPsがかぶっていないとき"Separated"
    かぶっていてPsが下にある時"Downside"、上にある時"Upside"を返す
    """
    for P in Ps:
        if abs(O - P) > r:  # OP > rならPは円の外
            pass
        elif O.y > P.y:  # 円の中で、下のほうがかぶっているとき
            print("距離が" + str(abs(O - P)))
            return "Downside"
        else:
            print("距離が" + str(abs(O - P)))
            return "Upside"
    return "Separated"


def define_Oa(
    EndFoilPs,
    RootFoilPs,
    da,
    h,
    EndPipeO,
    RootPipeO,
    sharpness=0.1,
    StartO=vector(0, 0),
):
    """
    EndFoilPsでも、RootFoilPsでもh以上の余白を持ったアセンブリ棒穴(直径da)の中心のうち最も後方にあるものを求める
    原点は桁の中心
    FoilPsはvectorのリスト
    First_Oは翼内に入っている必要がある。
    桁穴+StartOの地点から試行できる
    sharpnessの精度で返す
    """
    # 円の半径に使う
    r = da / 2 + h
    FoilPs = [EndFoilPs, RootFoilPs]
    Os = [EndPipeO, RootPipeO]

    ret = [0, 0]
    for i in range(2):
        dx = 2 * r  # 最初からdx=sharpnessでもいいが、収束を速くする
        current_O = Os[i] + StartO  # 前縁原点
        PastRelation = 0  # 過去の値を保持して比較する
        while True:
            Relation = relation(FoilPs[i], r, current_O)
            if Relation == "Separated":
                # 穴が翼型内ならdxだけ右にずらす
                current_O += vector(dx, 0)
            elif dx == 2 * r:
                # まだ精度が悪いとき、一つ前に戻して精度を上げる
                current_O -= vector(dx, 0)
                dx = sharpness
            elif (PastRelation != 0) and (Relation != PastRelation):
                # 上下に行ってもはみ出るとき
                ret[i] = current_O - Os[i]  # 原点を桁の中心に
                break
            elif Relation == "Downside":
                # 穴が翼型からはみ出たが、dxだけ上に行くとはみ出ないとき
                current_O += vector(0, dx)
                PastRelation = Relation
            elif Relation == "Upside":
                # dxだけ下に行くとはみ出ないとき
                current_O -= vector(0, dx)
                PastRelation = Relation
            else:
                print("define_Oaに不明なエラー")
        if (
            relation(FoilPs[1], r, ret[0] + Os[1]) == "Separated"
        ):  # ret[0]がRootでも中に入っていたら
            return ret[0]
    return ret[1]


def WriteText(file, O, text, height=20, angle=0):
    """
    fileにtextを入力するコマンドを出力
    Oから始める。フォントの高さはheight、angleは字の角度[°]
    """
    file.write(f"text\n{O.x},{O.y}\n{str(height)}\n{str(angle)}\n{text}\n\n")


# 関数、クラス定義おわり
# ------------------------------------------------------------------------------------------------
# メイン
sweep *= numpy.pi / 180

# リブの分割出力を行う
if isUseBunkatuShuturyoku:
    deltaC = (RootChord - EndChord) / (n - 1)
    RootChord = RootChord - deltaC * (startRib - 1)
    EndChord = RootChord - deltaC * (endRib - 1)
    n = endRib - startRib + 1

# 翼型読み込み
EndFoilData = to_vectors(
    numpy.loadtxt(EndFoilName, skiprows=1, dtype=float)
)  # 上下で分けるためにベクトルに変換 1行目は翼型名なのでスキップ
# 端の上側だけの点(無次元)                           ↓上側ではx座標が減少することを利用
EndFoilDataU = [
    EndFoilData[i]
    for i in range(len(EndFoilData) - 1)
    if EndFoilData[i].x - EndFoilData[i + 1].x >= 0
] + [vector(0, 0)]
EndFoilDataU_x = to_numpy_x(EndFoilDataU)  # 上側のx座標(無次元)
EndFoilDataU_y = to_numpy_y(EndFoilDataU)  # 上側のy座標(無次元)
# 端の下側
EndFoilDataD = [vector(0, 0)] + [
    EndFoilData[i]
    for i in range(1, len(EndFoilData))
    if EndFoilData[i].x - EndFoilData[i - 1].x >= 0
]
EndFoilDataD_x = to_numpy_x(EndFoilDataD)  # 下側のx座標(無次元)
EndFoilDataD_y = to_numpy_y(EndFoilDataD)  # 下側のy座標(無次元)

RootFoilData = to_vectors(
    numpy.loadtxt(RootFoilName, skiprows=1, dtype=float)
)  # 上下で分けるためにベクトルに変換
# 根の上側
RootFoilDataU = [
    RootFoilData[i]
    for i in range(len(RootFoilData) - 1)
    if RootFoilData[i].x - RootFoilData[i + 1].x >= 0
] + [vector(0, 0)]
RootFoilDataU_x = to_numpy_x(RootFoilDataU)  # 上側のx座標(無次元)
RootFoilDataU_y = to_numpy_y(RootFoilDataU)  # 上側のy座標(無次元)
# 根の下側
RootFoilDataD = [vector(0, 0)] + [
    RootFoilData[i]
    for i in range(1, len(RootFoilData))
    if RootFoilData[i].x - RootFoilData[i - 1].x >= 0
]
RootFoilDataD_x = to_numpy_x(RootFoilDataD)  # 下側のx座標(無次元)
RootFoilDataD_y = to_numpy_y(RootFoilDataD)  # 下側のy座標(無次元)


# アセンブリ棒用
# 翼型を上下別に関数に近似。 上下一緒に近似する方法は思いつかなかった。 fはfunctionの略
f_uEnd = inter(
    EndFoilDataU_x[::-1] * EndChord * cos(sweep), EndFoilDataU_y[::-1] * EndChord
)
f_dEnd = inter(EndFoilDataD_x * EndChord* cos(sweep), EndFoilDataD_y * EndChord)
f_uRoot = inter(
    RootFoilDataU_x[::-1] * RootChord * cos(sweep), RootFoilDataU_y[::-1] * RootChord
)
f_dRoot = inter(RootFoilDataD_x * RootChord * cos(sweep), RootFoilDataD_y * RootChord)
EndFoilPs = [vector(P.x * EndChord * cos(sweep), P.y * EndChord) for P in EndFoilData]
RootFoilPs = [
    vector(P.x * RootChord * cos(sweep), P.y * RootChord) for P in RootFoilData
]
# パイプの中心
EndPipeO = vector(
    EndR * EndChord / 100, f_uEnd(0.25 * EndChord) / 2 + f_dEnd(0.25 * EndChord) / 2
)
RootPipeO = vector(
    RootR * RootChord / 100,
    f_uRoot(0.25 * RootChord) / 2 + f_dRoot(0.25 * RootChord) / 2,
)
# アセンブリ棒の準備
Oa = define_Oa(
    EndFoilPs,
    RootFoilPs,
    da,
    h + tu,
    EndPipeO,
    RootPipeO,
    StartO=vector(
        0.6 * EndChord, f_uEnd(0.6 * EndChord) / 2 + f_dEnd(0.6 * EndChord) / 2
    )
    - EndPipeO,
)

file = open(f"{ProjectName}.txt", "w",encoding="utf-8")

file.write("texted\n1\n")  # textをコマンドで入力できるように設定
file.write("-lweight\n0.001\n")  # 線の太さ設定

O = vector(0, 0)  # それぞれのリブの前縁のy座標
for k in range(1, n + 1):  # range(1,n+1):				 	#根から k 枚目のリブ
    # x座標の設定 かぶらないようにするため。
    if k > 1:  # k=1のときO=(0,0)にしている
        if k in halfRibNumber:
            O.x -= 0
        elif k not in halfRibNumber:
            O.x -= zurashi_x

    # 翼型の点のリストの出力。 上下の翼型を関数として作成。
    # 混ぜる割合。　根で0、端で1。
    r = (k - 1) / (n - 1)
    # 翼弦 流れ方向
    c = RootChord + (EndChord - RootChord) * r
    # 翼型を上下別に関数に近似。 上下一緒に近似する方法は思いつかなかった。 fはfunctionの略
    f_uEnd = inter(EndFoilDataU_x[::-1] * c * cos(sweep), EndFoilDataU_y[::-1] * c)
    f_dEnd = inter(EndFoilDataD_x * c * cos(sweep), EndFoilDataD_y * c)
    f_uRoot = inter(RootFoilDataU_x[::-1] * c * cos(sweep), RootFoilDataU_y[::-1] * c)
    f_dRoot = inter(RootFoilDataD_x * c * cos(sweep), RootFoilDataD_y * c)

    # x座標の列を端と同じにする
    s = numpy.linspace(0, 1, bunnkatyu)
    x_d = numpy.delete(
        numpy.cos(numpy.pi * (s - 1) / 2) ** 2 * c * cos(sweep), 1
    )  # 再前縁から2番目の点があると不安定になることを防ぐ
    # 端点は正確に
    x_d[0] = 0
    x_d[-1] = c * cos(sweep)
    # x_uは点の向きと同じ(降順)
    x_u = x_d[::-1]

    # 翼型の混合
    y_u = f_uRoot(x_u) + (f_uEnd(x_u) - f_uRoot(x_u)) * r
    y_d = f_dRoot(x_d) + (f_dEnd(x_d) - f_dRoot(x_d)) * r

    # 翼型をベクトルのリストにする
    FoilU = to_vectors2(x_u, y_u)
    FoilD = to_vectors2(x_d, y_d)
    FoilPs = FoilU + FoilD[1:]  # FoilDは(0,0)を取り除く
    # 上下の翼型を関数として扱えるようにする
    f_u = inter(x_u[::-1], y_u[::-1])
    f_d = inter(x_d, y_d)
    del s

    # 中心線の関数、点のリスト
    s = numpy.linspace(
        0, x_d[-1], 50
    )  # 端で定義域を狭くするのは計算誤差でf_uの定義域を超えないため。
    f_camber = inter(
        s, (f_u(s) + f_d(s)) / 2
    )  # 上下の翼型の関数の平均であると近似 特に前縁付近は信用できない
    CamberPs = to_vectors2(s, f_camber(s))
    del s

    # 境目になるようなx座標を定義する
    x_plank_u = c * (rpu / 100) * cos(sweep)
    x_plank_d = c * (rpd / 100) * cos(sweep)
    x_stringer_dt = c * (rsdt / 100 )* cos(sweep)
    x_pipe = c * (RootR + (EndR - RootR) * r) / 100 * cos(sweep)
    x_25pc = c * cos(sweep) * 0.25

    # プランクの点のリストの出力
    PlankPs = offset(
        [FoilU[i] for i in range(len(FoilU) - 2) if FoilU[i + 2].x <= x_plank_u]
        + [FoilU[-2], FoilD[0], FoilD[1]]
        + [FoilD[i] for i in range(2, len(FoilD)) if FoilD[i - 2].x <= x_plank_d],
        tp,
        0,
    )
    PlankPsU = [P for P in PlankPs if P.y >= 0][::-1]
    PlankPsD = [P for P in PlankPs if P.y <= 0] 
    
    
    # 後縁材の出力
    # 後縁材の上側の一点を求める。下をoffsetした関数と上の関数の交点とする。
    FoilD_offsetPs = offset(FoilD[5:], htu, 0)
    s = numpy.linspace(FoilD_offsetPs[0].x, FoilD_offsetPs[-1].x)
    xs = numpy.array(to_numpy_x(FoilD_offsetPs))
    ys = numpy.array(to_numpy_y(FoilD_offsetPs))

    # xでソート（念のため）
    order = numpy.argsort(xs)
    xs = xs[order]
    ys = ys[order]

    # 重複を削除
    xs_unique, idx = numpy.unique(xs, return_index=True)
    ys_unique = ys[idx]

    f_dOffset = inter(xs_unique, ys_unique)
    TrailU_x = optimize.newton(lambda x: f_dOffset(x) - f_u(x), c * cos(sweep) * 0.95)
    TrailU = vector(TrailU_x, f_u(TrailU_x))
    print(to_numpy_x(FoilD_offsetPs))
    del s

    # 後縁材の下側の一点を求める。 TrailUを挟む点を求め、これら三点でoffsetする。
    FoilU_offsetPs = offset(FoilU[::-1][15:], htd, 1)
    s = numpy.linspace(FoilU_offsetPs[0].x, FoilU_offsetPs[-1].x)
    f_uOffset = inter(to_numpy_x(FoilU_offsetPs), to_numpy_y(FoilU_offsetPs))
    TrailD_x = optimize.newton(lambda x: f_uOffset(x) - f_d(x), c * cos(sweep) * 0.95)
    TrailD = vector(TrailD_x, f_d(TrailD_x))
    del s

    x_stringer_D1 = TrailD_x + length_of_adribcapd
    stringerD1 = [
        FoilD[i]
        for i in range(1, len(FoilD))
        if FoilD[i - 1].x <= x_stringer_D1
    ][-2:]
    stringerD1ToVec = stringer(
        div_P(stringerD1[0], stringerD1[1], x_stringer_D1, 0), stringerD1[0], e, R=True
    )    

    #🐧の凹の部分の点
    TrailC_x = TrailD_x + 10  #+2は勘 
    TrailC = vector(TrailC_x, f_camber(TrailC_x))
    
    # リブキャップの点のリストの出力 プランクの開始点より後縁側であることを利用
    RibCap_uPs = offset(
        [FoilU[i] for i in range(0, len(FoilU)) if FoilU[i - 2].x >= TrailU_x], tu, 0
    )
    if ribcapddome:
        RibCap_dPs =offset(
            [FoilD[i] for i in range(len(FoilD)-2) if (FoilD[i + 2].x >= TrailD_x) and (FoilD[i + 2].x < x_stringer_D1)], td, 0
        )
        RibCap_dPs.append(stringerD1ToVec.D)

        FoilD =[FoilD[i] for i in range(len(FoilD)-2) if FoilD[i + 2].x > x_stringer_D1]
        FoilD.insert(0,stringerD1ToVec.A)
    else:
        RibCap_dPs = offset(
            [FoilD[i] for i in range(len(FoilD)-2) if FoilD[i + 2].x >= TrailD_x], td, 0
        )

    if zenntanndome:
        RibCap_doffset = inter(to_numpy_x(RibCap_dPs), to_numpy_y(RibCap_dPs))
        #後縁前端棒止め
        ht = 5
        htl = 5.1
        FoilU_offsetKs = offset(RibCap_uPs[::-1][5:], ht, 1)
        s = numpy.linspace(FoilU_offsetKs[0].x, FoilU_offsetKs[-1].x)
        dome_uOffset = inter(to_numpy_x(FoilU_offsetKs), to_numpy_y(FoilU_offsetKs))
        DomeD_x = optimize.newton(lambda x: dome_uOffset(x) - RibCap_doffset(x), c * cos(sweep) * 0.96)
        DomeD = vector(DomeD_x, RibCap_doffset(DomeD_x))
        del s
        print(DomeD)
        # 後縁材の下側の一点を求める。 TrailUを挟む点を求め、これら三点でoffsetする。
        EdgedomeD = [
            FoilU_offsetKs[i]
            for i in range(1, len(FoilU_offsetKs))
            if FoilU_offsetKs[i - 1].x <= DomeD.x
        ][
            -2:
        ]  # TrailUを挟む点
        DomeU = offset([EdgedomeD[0], DomeD, EdgedomeD[1]], ht, 0)[0]

        DomeUl = DomeU + vector(DomeD.y - DomeU.y, DomeU.x - DomeD.x)* htl / math.sqrt((DomeU.y - DomeD.y)**2 + (DomeD.x - DomeU.x)**2)
        DomeDl = DomeD + vector(DomeD.y - DomeU.y, DomeU.x - DomeD.x)* htl / math.sqrt((DomeU.y - DomeD.y)**2 + (DomeD.x - DomeU.x)**2)

        if k not in halfRibNumber:
            #後縁前端棒止め
            color(file, 255, 0, 255)
            line(file, DomeU, DomeD, O)
            line(file, DomeD, DomeDl, O)
            line(file, DomeDl, DomeUl, O)
            line(file, DomeUl, DomeU, O)

    if k not in halfRibNumber:
        # リブキャップ
        color(file, 255, 0, 255)
        spline(file, RibCap_uPs, O)
        spline(file, RibCap_dPs, O)
        if ribcapddome:
            spline(file, FoilD, O)
            line(file, stringerD1ToVec.A, stringerD1ToVec.D, O)
            line(file, RibCap_uPs[0], FoilD[-1], O)
        else:
            line(file, RibCap_uPs[0], RibCap_dPs[-1], O)

        # 後縁材の前縁側の一辺を出力 
        color(file, 255, 0, 255)
        #line(file, TrailU, TrailD, O)  # 後縁材の前縁側の一辺を出力
        line(file, TrailU, TrailC, O)
        line(file, TrailD, TrailC, O)

        color(file, 255, 0, 255)
        WriteText(file, vector(O.x + c - 60, f_camber(c * 0.95)-30), f"{PlaneNumber}-{k}", height=8)

        

file.close()
print("completed")
