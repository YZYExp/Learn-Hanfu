#!/usr/bin/env python3
"""Idempotently insert the editorially selected illustrations and credit lists."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'book.json').read_text())
chapters={e['id']:ROOT/e['source'] for e in manifest['chapters']}
diagrams=json.loads((ROOT/'references/diagram-index.json').read_text())
evidence=json.loads((ROOT/'references/image-evidence.json').read_text())['images']
byname={e['filename']:e for e in evidence}
placements=[]

def figure(path,title,caption):
    return f'\n\n![{title}](../{path})\n\n图｜{caption}\n\n'

def place(ch,path,title,caption,section=None):
    p=chapters[ch];s=p.read_text()
    placements.append({'chapter':ch,'path':path,'title':title})
    if '../'+path in s:return
    f=figure(path,title,caption)
    if section:
        start=s.index(section);m=re.search(r'\n## ',s[start+len(section):]);pos=start+len(section)+m.start() if m else len(s)
    else:
        m=re.search(r'\n## ',s);pos=m.start() if m else len(s)
    s=s[:pos]+f+s[pos:];p.write_text(s)

for d in diagrams:
    place(d['chapter'],d['path'],d['title'],d['caption']+' '+d['limitations']+' 原创教学示意。')

mapping={
 '04':['evidence-met-65598.jpg'],
 '06':['evidence-met-54077.jpg'],
 '07':['evidence-met-54075.jpg'],
 '09':['evidence-cma-1995-20.jpg'],
 '10':['evidence-met-70324.jpg'],
 '11':['evidence-met-48939.jpg'],
 '12':['evidence-cma-1956-78.jpg'],
 '13':['evidence-met-skirt-30766.jpg'],
 '16':['evidence-met-42180.jpg'],
 '19':['evidence-cma-1916-1353.jpg'],
}
def evidence_caption(e):
    credit=e['institution']+('，'+e['object_number'] if e.get('object_number') else '')
    rights=('版权归原权利人，本节教学评述引用，未标为开放授权' if e.get('license_status')=='copyrighted-or-not-cleared' else e['license'].split('。')[0])
    return f'{e["title"]}，{e["date"]}。{e["observation"]} {e["limitations"]} 资料与图片：[{credit}]({e["url"]})。图片权利：{rights}。'
for ch,names in mapping.items():
    for name in names:
        e=byname[name];place(ch,'assets/images/'+name,e['title'],evidence_caption(e))

cnmap={
 'evidence-cn-north-jiaoxie.jpg':'## 一、',
 'evidence-cn-tang-figure.jpg':'## 二、',
 'evidence-cn-song-beizi.jpg':'## 四、',
 'evidence-cn-ming-three.jpg':'## 五、',
 'evidence-cn-ming-skirt.jpg':'## 六、',
}
for name,section in cnmap.items():
    if name in byname:
        e=byname[name];place('21','assets/images/'+name,e['title'],evidence_caption(e),section=section)

place('22','assets/images/illustration-contemporary.png','当代汉服穿着插画','当代穿着的层次与衣长关系，AI教学插画。用于观察外衣、上衣和下装的长度及行走状态，不代表某一朝代的标准套装。')
place('06','assets/images/illustration-high-skirt.png','高束裙与短衣的外观示意','窄袖短衣与高束条纹裙的组合，AI教学插画；参考本章故宫陶俑条目中的可见服装描述。颜色、面料质感与人物造型是示意性选择，不作为原件复原或裁片证据。')

credits=['# 附录C　图像来源与阅读资料','本书的文物图片、历史图像、原创教学图与生成插画分开记录。图像中的修复、衬托、缺损与拍摄角度都可能影响观察。出版、再发布或单独分发图片时，应分别核对各权利状态；本书的文字与脚本不改变原图权利。','## 馆藏文物与历史图像']
for e in evidence:
    number=('；编号'+e['object_number']) if e.get('object_number') else ''
    credits += [f'### {e["title"]}',f'{e["date"]}；{e["institution"]}{number}。[官方对象资料]({e["url"]})。',f'图片权利：{e["license"]}。',f'阅读限度：{e["limitations"]}']
credits+=['## 原创教学图','全书12幅原创教学示意由脚本绘制：证据类型、衣物部位、时间定位、袖量、正侧背、裙片围合、开衩遮覆、穿着分层、织物组织、织绣区别、复原过程与观察记录。它们解释指定关系，不是文物照片或等比例纸样。图注中的适用范围与局限同样属于图像内容。','## 生成插画','第6章的高束裙短衣图、第22章的当代穿着图为AI教学插画。二者只辅助观察可见外观、层次和比例，不充当历史年代、裁剪、穿用场景或工艺技术的证据。','## 如何沿资料继续读','需要确认一件衣服时，先打开章内紧邻事实的藏品页，核对题名、编号、年代、材料和视图；再从馆方文章或报告看结构与出土组合。研究方法与大众介绍的详略不同，应回到实际问题选择资料。','博物馆网页与馆藏说明会更新。书中记录以本版整理时所核对的信息为准；不能打开某个网页时，先以馆名、藏品全名与编号在该机构检索。正文没有阅读并核实的书籍不被列为已参考材料。']
(ROOT/'appendices/c-image-credits.md').write_text('\n\n'.join(credits)+'\n')
manifest['appendices']=[{'id':'A','title':'时间坐标与并行的历史','source':'appendices/a-timeline.md','slug':'a-timeline'},{'id':'B','title':'衣冠观察词汇','source':'appendices/b-glossary.md','slug':'b-glossary'},{'id':'C','title':'图像来源与阅读资料','source':'appendices/c-image-credits.md','slug':'c-image-credits'}]
(ROOT/'book.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(ROOT/'references/image-placements.json').write_text(json.dumps(placements,ensure_ascii=False,indent=2)+'\n')
print('Integrated',len(placements),'figures')
