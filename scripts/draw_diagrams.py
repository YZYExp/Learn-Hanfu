#!/usr/bin/env python3
"""Reproducible, non-reconstruction teaching diagrams for Hanfu Atlas."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, math, os

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'
FONT=os.environ.get('HANFU_DIAGRAM_FONT',str(ROOT/'assets/fonts/HanfuDiagram.ttf'))
W,H=1600,1800
BG='#F7F3EA'; INK='#263944'; RED='#A84B3C'; BLUE='#355E76'; GREEN='#738873'; GREY='#777B76'; LIGHT='#E6DFD1'; WHITE='#FFFDF8'
INDEX=[]
def f(n): return ImageFont.truetype(FONT,n)
def txt(d,xy,s,n=40,c=INK,anchor=None): d.text(xy,s,font=f(n),fill=c,anchor=anchor)
def line(d,pts,c=INK,w=5): d.line(pts,fill=c,width=w,joint='curve')
def arrow(d,a,b,c=RED,w=6):
    line(d,[a,b],c,w);ang=math.atan2(b[1]-a[1],b[0]-a[0]);r=22
    d.polygon([b,(b[0]-r*math.cos(ang-.55),b[1]-r*math.sin(ang-.55)),(b[0]-r*math.cos(ang+.55),b[1]-r*math.sin(ang+.55))],fill=c)
def base(num,title,sub):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    txt(d,(110,80),'衣冠之间  /  结构与观察',29,GREY)
    txt(d,(110,145),title,66)
    txt(d,(110,245),sub,32,GREY)
    line(d,[(110,315),(1490,315)],LIGHT,3)
    line(d,[(110,1650),(1490,1650)],LIGHT,3)
    txt(d,(110,1690),'原创教学示意；非文物照片，非裁剪纸样',29,GREY)
    txt(d,(1490,1690),f'{num:02}',29,GREY,'ra')
    return im,d
def save(im,num,ch,title,caption,limits):
    fn=f'diagram-{num:02}.png';im.save(OUT/fn,optimize=True)
    INDEX.append(dict(path=f'assets/images/{fn}',chapter=ch,title=title,caption=caption,limitations=limits))
def rounded(d,box,fill=WHITE,outline=LIGHT,r=28,width=3):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def body(d,cx,top,scale=1,fill=LIGHT,sleeve='narrow',length=650):
    # Generic diagram, no historical reconstruction or seam-line assertion.
    sx=lambda x:cx+x*scale;sy=lambda y:top+y*scale
    wide=220 if sleeve=='wide' else 90
    pts=[(-90,0),(-190,55),(-340,180),(-280,180+wide),(-130,160),( -170,length),(170,length),(130,160),(280,180+wide),(340,180),(190,55),(90,0)]
    d.polygon([(sx(x),sy(y)) for x,y in pts],fill=fill,outline=INK,width=4)
    d.arc((sx(-90),sy(-35),sx(90),sy(85)),0,180,fill=INK,width=4)

def evidence():
    im,d=base(1,'证据能回答什么','同一件衣物，需要不同材料互相校验')
    rows=[('实物',BLUE,'组织、缝线、尺寸、破损','不自动给出完整穿法'),('同期图像',RED,'外观、层次、动作、组合','常遮挡背面与内层'),('文献',GREEN,'名称、制度、用料、语境','文字名称未必一物一名')]
    for i,(t,c,a,b) in enumerate(rows):
        y=385+i*330;rounded(d,(110,y,1490,y+270));d.ellipse((155,y+60,285,y+190),fill=c)
        txt(d,(220,y+125),str(i+1),56,WHITE,'mm');txt(d,(330,y+45),t,49,c);txt(d,(330,y+125),a,38);txt(d,(330,y+190),b,32,GREY)
    txt(d,(800,1470),'复原 = 有依据的解释 + 明示的假设',42,INK,'mm')
    save(im,1,'01','证据能回答什么','实物、同期图像和文献分别支持不同判断；互证不等于消除全部未知。','不构成证据等级排序；具体材料可靠性仍需个案评估。')

def anatomy():
    im,d=base(2,'先把部位认清','领型、开合与衣长，是不同观察维度')
    body(d,800,480,1.1,fill='#D7DDD6',length=720)
    # Crossed-front overlap, wearer left = viewer right.
    line(d,[(715,505),(800,637)],BLUE,10)
    line(d,[(885,505),(650,870),(630,1230)],RED,13)
    labels=[((850,550),(1150,440),'领：围绕颈部'),((685,820),(250,840),'襟：前部开合衣片'),((1100,720),(1270,830),'袖：包覆手臂'),((810,980),(1200,1140),'身：躯干部位'),((820,1270),(820,1470),'裾：衣服下缘')]
    for a,b,t in labels:
        arrow(d,b,a,RED,4);txt(d,(b[0],b[1]-40),t,31,INK,'mm')
    txt(d,(800,1560),'正面观察：左右须以穿着者身体为准',34,GREY,'mm')
    save(im,2,'02','衣物部位','示意衣物的领、襟、袖、衣身与下缘；交叠的方向从穿着者视角判断。','通用部位图，非某时代具体服装；线条不是裁剪纸样或真实缝线。')

def timeline():
    im,d=base(3,'把衣冠放回时间','这是阅读定位，不是单一形制的进化阶梯')
    rows=[('先秦','地域与礼制，多种材料并读'),('秦汉','袍服与丝织衣物的实物线索'),('魏晋南北朝','不同地区，宽衣与小袖并存'),('隋唐五代','袍、襦、裙与多样穿着'),('宋、辽、金','同时代的不同政治与文化空间'),('元','多族群衣着与跨区域联系'),('明','制度服饰与生活衣物'),('清','变革、延续与身份差异'),('近代','新旧服装体系的变动'),('当代','复原、设计与日常穿用')]
    line(d,[(230,400),(230,1510)],LIGHT,9)
    for i,(a,b) in enumerate(rows):
        y=410+i*118;c=[BLUE,RED,GREEN][i%3];d.ellipse((210,y-20,250,y+20),fill=c)
        txt(d,(300,y-25),a,38,c);txt(d,(660,y-19),b,30)
    save(im,3,'03','时间定位','各时期衣冠变化由制度、材料、交流及生活共同塑造；同一时段也存在差异。','按阅读顺序概括，非按时长比例绘制；未穷尽全部政权和地区。')

def sleeves():
    im,d=base(4,'袖量改变活动空间','比较同样的抬臂动作，避免把袖宽当成朝代')
    for cx,sl,c,label in [(440,'narrow','#CAD7DC','袖量较小'),(1160,'wide','#DDD0C4','袖量较大')]:
        body(d,cx,490,.75,c,sl,650);d.ellipse((cx-55,380,cx+55,490),fill=LIGHT,outline=INK,width=3)
        txt(d,(cx,1150),label,43,INK,'mm')
    line(d,[(180,1290),(1420,1290)],LIGHT,3)
    txt(d,(800,1390),'还要同时看：腋下放量、衣长、面料与内层',37,INK,'mm')
    txt(d,(800,1490),'图中轮廓只比较袖量；不能据此判定穿着者身份',31,GREY,'mm')
    save(im,4,'05','袖量与空间','以通用衣物轮廓比较袖量；大袖增加布料垂落范围，但活动感受还受腋下和衣身结构影响。','不是魏晋服装复原图，不能据此确定时期或制作尺寸。')

def outer_views():
    im,d=base(5,'一件外衣，三个观察面','前、侧、背的信息各不相同')
    for cx,label in [(330,'正面'),(800,'侧面'),(1270,'背面')]:
        if label=='侧面':
            d.polygon([(cx-45,530),(cx+60,530),(cx+85,1120),(cx-70,1120)],fill='#D7DDD6',outline=INK,width=4)
            line(d,[(cx+60,810),(cx+70,1120)],RED,10)
        else:
            body(d,cx,530,.55,'#D7DDD6',length=1070)
            if label=='正面':
                line(d,[(cx-24,535),(cx-24,1115)],BLUE,8);line(d,[(cx+24,535),(cx+24,1115)],BLUE,8)
            else: line(d,[(cx,550),(cx,1115)],GREY,3)
        txt(d,(cx,1220),label,44,INK,'mm')
    txt(d,(330,1370),'开合与领缘',33,BLUE,'mm');txt(d,(800,1370),'开衩与遮覆',33,RED,'mm');txt(d,(1270,1370),'拼接与轮廓',33,GREEN,'mm')
    txt(d,(800,1490),'正面看不见的部位，须另找实物或图像支持',35,GREY,'mm')
    txt(d,(800,1570),'背中线仅作观察位置提示，并非所有外衣都有此线',29,GREY,'mm')
    save(im,5,'08','外衣的三个观察面','用对襟长外衣概念轮廓展示正面开合、侧面开衩与背面拼接的不同观察任务。','不是宋代褙子的精确复原；图中背中线仅作拼接观察位置提示，不宣称所有衣物都有此线。')

def skirt():
    im,d=base(6,'两片怎样围成一条裙','从上方看：重叠与褶量承担不同作用')
    box=(420,470,1180,1230)
    # Two 240-degree panels start 180 degrees apart: 60-degree overlap front/back.
    d.arc(box,240,480,fill=BLUE,width=42);d.arc((435,485,1165,1215),60,300,fill=RED,width=42)
    d.ellipse((590,640,1010,1060),fill=LIGHT,outline=GREY,width=3);txt(d,(800,850),'身体截面',36,GREY,'mm')
    txt(d,(800,410),'前方：两片重叠',38,INK,'mm');txt(d,(800,1310),'后方：两片重叠',38,INK,'mm')
    arrow(d,(800,450),(800,505),GREEN,5);arrow(d,(800,1260),(800,1190),GREEN,5)
    for x,c in [(350,RED),(1250,BLUE)]:
        for y in range(720,1000,48): line(d,[(x-40,y),(x+15,y+20),(x-40,y+40)],c,5)
    txt(d,(270,1100),'侧部褶量',31,RED,'mm');txt(d,(1330,1100),'侧部褶量',31,BLUE,'mm')
    txt(d,(800,1460),'蓝、红各代表一片；圆弧不表示真实裁片形状',32,GREY,'mm')
    txt(d,(800,1530),'围合角度与重叠宽度因实物而异',32,GREY,'mm')
    save(im,6,'13','两片围合裙概念','两片式围裙类结构可通过前后重叠获得遮覆，侧部褶量提供容量；需结合具体裙实物理解。','圆截面为围合关系示意，非马面裙裁剪图；不代表所有历史裙装。')

def slit():
    im,d=base(7,'开衩处怎样保持遮覆','看外层开口，也要看里面有什么')
    rounded(d,(250,410,1350,1460),WHITE)
    d.polygon([(600,500),(1000,500),(1080,1320),(520,1320)],fill='#D5DCCF',outline=INK,width=4)
    d.polygon([(480,500),(740,500),(700,1000),(570,1320),(400,1320)],fill='#C9D5DA',outline=INK,width=4)
    d.polygon([(860,500),(1120,500),(1200,1320),(1030,1320),(900,1000)],fill='#C9D5DA',outline=INK,width=4)
    arrow(d,(1190,850),(915,1080),RED,6);txt(d,(1180,780),'外层开口',34,RED,'mm')
    arrow(d,(400,1100),(750,1170),GREEN,6);txt(d,(410,1010),'内层仍可遮覆',34,GREEN,'mm')
    txt(d,(800,1530),'开衩、内摆和内层衣物须分别辨认',37,INK,'mm')
    save(im,7,'14','开衩与内层遮覆','放大示意开口边缘与内层遮覆的关系；外部开口不能单独说明完整衣着结构。','几何概念图，非某一种道袍或直身结构，不能据此判断具体衣物的摆与缝合。')

def layers():
    im,d=base(8,'内、中、外层一起观察','可见的长短，不等于全部衣物的长短')
    for cx,L,c,title in [(360,580,'#DCCBB7','内层'),(800,770,'#D4DDD1','中层'),(1240,900,'#C8D6DE','外层')]:
        body(d,cx,480,.52,c,length=L);txt(d,(cx,1080),title,44,INK,'mm')
        line(d,[(cx-140,1190),(cx+140,1190)],c,18)
    txt(d,(800,1320),'领缘露出多少？  衣摆到哪里？',42,INK,'mm')
    txt(d,(800,1420),'先记录看见的层次，再核对被遮住的部分',35,GREY,'mm')
    txt(d,(800,1520),'此处层数与长度仅为比较示例，不是通用穿法',31,GREY,'mm')
    save(im,8,'15','分层观察','以三个通用衣物轮廓说明内中外层的长度可不同，实际层数与组合取决于时代、场合和具体衣物。','示意不是任何历史时期的标准三层配置；图中没有断言内衣形制。')

def weave():
    im,d=base(9,'纤维是原料，组织是织法','同一原料，可以织出不同交织规律')
    cases=[('平纹','经纬一上一下',2,lambda x,y:(x+y)%2==0),('斜纹','交织点逐行斜向移动',3,lambda x,y:(x-y)%3<2),('五枚经面缎纹','经浮长，交织点分散',5,lambda x,y:(x-2*y)%5!=0)]
    for k,(title,desc,n,rule) in enumerate(cases):
        y0=390+k*375;txt(d,(150,y0+40),title,43,INK);txt(d,(150,y0+115),desc,29,GREY)
        x0=900;cell=45;N=7 if k<2 else 5
        for y in range(N):
            for x in range(N):
                b=(x0+x*cell,y0+y*cell,x0+(x+1)*cell-3,y0+(y+1)*cell-3)
                d.rectangle(b,fill=BLUE if rule(x,y) else RED)
        txt(d,(x0+N*cell+40,y0+40),'经向 ↓',28,BLUE)
        txt(d,(x0+30,y0+N*cell+17),'纬向 →',28,RED)
    txt(d,(800,1570),'蓝 = 经线在上   红 = 纬线在上；均为放大组织图',30,GREY,'mm')
    save(im,9,'17','组织与原料','平纹、二上一下斜纹与五枚经面缎纹的简化组织图，以蓝色表示经线在上、红色表示纬线在上。','不表示历史织物的密度、线径或光泽；“缎纹”是组织类别，不能据图推断纤维成分。')

def decoration():
    im,d=base(10,'织出来，还是绣上去','观察图案与底布的关系')
    for i,(title,color) in enumerate([('织纹：图案由经纬交织形成',BLUE),('刺绣：另加绣线附着于底布',RED)]):
        y0=450+i*580;txt(d,(160,y0-40),title,40,color)
        for yy in range(y0+50,y0+330,32):line(d,[(200,yy),(1400,yy)],'#C5BDAF',11)
        for xx in range(200,1420,32):line(d,[(xx,y0+45),(xx,y0+335)],'#D8D1C3',11)
        if i==0:
            for yy in range(7):
                for xx in range(7):
                    if abs(xx-3)+abs(yy-3)<=3:d.rectangle((650+xx*34,y0+65+yy*34,680+xx*34,y0+90+yy*34),fill=BLUE)
        else:
            for x in range(630,900,25):line(d,[(x,y0+90),(x+130,y0+290)],RED,14)
        txt(d,(800,y0+405),'放大概念：真实工艺还需查看正反面与组织',29,GREY,'mm')
    save(im,10,'18','织纹与刺绣','以放大概念图比较图案进入经纬交织系统、与在底布上另加绣线的区别。','不是具体历史纹样或织绣工艺的完整操作图；复杂织锦和刺绣还存在多种技术。')

def reconstruction():
    im,d=base(11,'复原不是一次猜中','保留证据、假设与修订记录')
    steps=[('01','记录证据','尺寸、缝痕、组织、图像',BLUE),('02','提出结构假设','哪些能确定，哪些仍未知',RED),('03','制作试样','先用试验材料检验结构',GREEN),('04','试穿与修订','活动、层次、受力与遮覆',BLUE)]
    for i,(n,t,s,c) in enumerate(steps):
        y=390+i*285;rounded(d,(150,y,1450,y+220));txt(d,(220,y+60),n,55,c);txt(d,(390,y+40),t,47,c);txt(d,(390,y+125),s,33)
    txt(d,(800,1560),'每次修改，都写清“为什么改”与“依据是什么”',34,INK,'mm')
    save(im,11,'20','复原的工作循环','把服饰复原作为有记录、可修订的解释过程，证据与假设须分别保留。','流程是现代研究工作方法概括，并非对某一历史服装纸样的证明。')

def observation():
    im,d=base(12,'留下一张可比较的记录','先描述，再命名；先量观察，再推断')
    for cx,l in [(350,'正面'),(800,'侧面'),(1250,'背面')]:
        if l=='侧面':
            d.polygon([(cx-45,480),(cx+45,480),(cx+70,1010),(cx-70,1010)],fill=LIGHT,outline=GREY,width=3)
        else:body(d,cx,480,.45,LIGHT,length=1180)
        txt(d,(cx,1100),l,39,INK,'mm')
    fields=['对象 / 收藏机构 / 编号','年代与地区 / 出处链接','领襟 / 袖形 / 衣长 / 开衩','可见层次 / 系结 / 未知部位']
    for i,t in enumerate(fields):
        y=1220+i*90;txt(d,(170,y),t,32,INK);line(d,[(820,y+35),(1430,y+35)],LIGHT,3)
    save(im,12,'26','衣冠观察记录模板','正侧背观察与来源、年代、结构、层次、未知项可合并记录，便于不同对象之间比较。','轮廓仅提供记录位置，不指向特定历史服装；不要用模板补画实际不可见的部位。')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for fn in [evidence,anatomy,timeline,sleeves,outer_views,skirt,slit,layers,weave,decoration,reconstruction,observation]:fn()
    (ROOT/'references/diagram-index.json').write_text(json.dumps(INDEX,ensure_ascii=False,indent=2))
    sheet=Image.new('RGB',(1600,1800),WHITE)
    for i,item in enumerate(INDEX):
        p=Image.open(ROOT/item['path']);p.thumbnail((390,560));sheet.paste(p,((i%4)*400,(i//4)*600))
    (ROOT/'build').mkdir(exist_ok=True);sheet.save(ROOT/'build/diagram-contact-sheet.jpg')
    print(f'Wrote {len(INDEX)} diagrams.')
if __name__=='__main__':main()
