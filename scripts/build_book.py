#!/usr/bin/env python3
"""Build PDF (whole book and chapters) and EPUB from one Markdown source tree."""
from pathlib import Path
import argparse, html, json, re, zipfile, uuid
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'(?<!!)\[([^\]]+)\]\((https?://[^\s)]+)\)')
IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

def blocks(text):
    lines = text.splitlines(); i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s or s == '---': i += 1; continue
        if s.startswith('```'):
            a=[]; i+=1
            while i<len(lines) and not lines[i].startswith('```'): a.append(lines[i]); i+=1
            i+=1; yield ('p', '\n'.join(a)); continue
        if IMAGE.fullmatch(s): yield ('image', IMAGE.fullmatch(s).groups()); i+=1; continue
        if s.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in row): rows.append(row)
                i+=1
            yield ('table', rows); continue
        if s.startswith('#'):
            m=re.match(r'^(#{1,6})\s+(.*)', s)
            if m: yield ('h'+str(len(m[1])),m[2]); i+=1; continue
        if s.startswith('>'): yield ('quote',s.lstrip('> ')); i+=1; continue
        if re.match(r'^([-*]|\d+[.、])\s+',s):
            yield ('li',re.sub(r'^([-*]|\d+[.、])\s+','',s)); i+=1; continue
        a=[s]; i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||!\[|>|[-*] |\d+[.、] |```)',lines[i].strip()):
            a.append(lines[i].strip()); i+=1
        yield ('p',''.join(a))

def clean(s):
    return re.sub(r'[`*_]','',s)

def inline_epub(s):
    s=html.escape(s)
    s=LINK.sub(lambda m:f'<a href="{m[2]}">{m[1]}</a>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    return s

def build_epub(manifest, out):
    entries=manifest['chapters']+manifest.get('appendices',[])
    items=[]; pages=[]; images={}
    for n, entry in enumerate(entries):
        p=ROOT/entry['source']; body=[]
        for kind,val in blocks(p.read_text()):
            if kind=='image':
                alt,rel=val; ip=(p.parent/rel).resolve(); name=ip.name; images[name]=ip
                body.append(f'<figure><img src="images/{name}" alt="{html.escape(alt)}"/></figure>')
            elif kind=='table':
                body.append('<table>'+''.join('<tr>'+''.join(f'<td>{inline_epub(c)}</td>' for c in row)+'</tr>' for row in val)+'</table>')
            elif kind.startswith('h') and kind[1:].isdigit(): body.append(f'<{kind}>{inline_epub(val)}</{kind}>')
            else: body.append(f'<p class="{kind}">{inline_epub(val)}</p>')
        name=f'ch{n+1:02}.xhtml'; pages.append((name,entry['title']))
        items.append((name, f'<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN"><head><title>{html.escape(entry["title"])}</title><link rel="stylesheet" href="style.css"/></head><body>{"".join(body)}</body></html>'))
    nav='<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>目录</title></head><body><h1>衣冠之间</h1><p>汉服的历史、结构与日常</p><nav epub:type="toc" id="toc"><ol>'+''.join(f'<li><a href="{n}">{html.escape(t)}</a></li>' for n,t in pages)+'</ol></nav></body></html>'
    css='body{font-family:serif;line-height:1.8;margin:5%;color:#28343a}h1,h2{color:#7b3f37;line-height:1.4}h1{page-break-before:always}figure{margin:1em 0;text-align:center}img{max-width:100%;max-height:85vh}table{border-collapse:collapse;font-size:.9em;width:100%}td{border-bottom:1px solid #ddd;padding:.5em;vertical-align:top}.quote{padding:.7em;border-left:3px solid #b28b71;background:#f7f3ed}.li{margin-left:1em}a{color:#315b65}code{font-family:monospace}'
    uid='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'hanfu-atlas-2026-10-25'))
    mime=lambda x:'image/png' if x.endswith('.png') else 'image/jpeg'
    opf=f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="bookid">{uid}</dc:identifier><dc:title>衣冠之间：汉服的历史、结构与日常</dc:title><dc:language>zh-CN</dc:language><dc:creator>图解知识书项目</dc:creator><meta property="dcterms:modified">2026-10-25T00:00:00Z</meta></metadata><manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="style" href="style.css" media-type="text/css"/>'''+''.join(f'<item id="c{i}" href="{n}" media-type="application/xhtml+xml"/>' for i,(n,t) in enumerate(pages))+''.join(f'<item id="img{i}" href="images/{html.escape(n)}" media-type="{mime(n)}"/>' for i,n in enumerate(images))+ '</manifest><spine>'+''.join(f'<itemref idref="c{i}"/>' for i in range(len(pages)))+'</spine></package>'
    with zipfile.ZipFile(out,'w') as z:
        z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml','<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        for n,b in items+[('nav.xhtml',nav),('style.css',css),('content.opf',opf)]: z.writestr('OEBPS/'+n,b,compress_type=zipfile.ZIP_DEFLATED)
        for n,p in images.items(): z.write(p,'OEBPS/images/'+n,compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(out) as z:
        for n in z.namelist():
            if n.endswith(('.xhtml','.opf','.xml')): ET.fromstring(z.read(n))
    return len(pages),len(images)

def build_pdf(manifest, outdir):
    from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.colors import HexColor, white
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import A4
    from PIL import Image as PILImage
    pdfmetrics.registerFont(TTFont('STSong-Light',str(ROOT/'assets/fonts/HanfuBookReader.ttf')))
    pdfmetrics.registerFontFamily('STSong-Light',normal='STSong-Light',bold='STSong-Light',italic='STSong-Light',boldItalic='STSong-Light')
    W,H=A4; margin=50; bodywidth=W-2*margin; refs={}; keys={}
    base=dict(fontName='STSong-Light',wordWrap='CJK',fontSize=10.5,leading=17.2,textColor=HexColor('#27343a'),spaceAfter=8)
    styles={k:ParagraphStyle(k,**(base|v)) for k,v in {
        'p':{},'li':{'leftIndent':12,'spaceAfter':5},'quote':{'leftIndent':12,'rightIndent':12,'backColor':HexColor('#f4f0e8'),'borderPadding':8,'spaceBefore':7,'spaceAfter':13},
        'h1':{'fontSize':24,'leading':33,'textColor':HexColor('#713f37'),'spaceAfter':20,'keepWithNext':True},
        'h2':{'fontSize':15,'leading':22,'textColor':HexColor('#315965'),'spaceBefore':12,'spaceAfter':9,'keepWithNext':True},
        'h3':{'fontSize':12,'leading':19,'spaceBefore':9,'keepWithNext':True},
        'small':{'fontSize':8.3,'leading':12,'textColor':HexColor('#526064'),'spaceAfter':10},
        'caption':{'fontSize':8.8,'leading':13.5,'textColor':HexColor('#526064'),'spaceAfter':12},
        'toc':{'fontSize':9.2,'leading':14,'spaceAfter':3},
        'biblio':{'fontSize':8.5,'leading':13,'spaceAfter':4},
        'cover-title':{'fontSize':43,'leading':56,'textColor':HexColor('#713f37'),'spaceAfter':20},
        'cover-subtitle':{'fontSize':21,'leading':30,'textColor':HexColor('#315965'),'spaceAfter':13},
        'cell':{'fontSize':8.3,'leading':13,'spaceAfter':0},
    }.items()}
    class RP(Paragraph):
        def __init__(self,txt,style,refkeys=(),**kw):
            super().__init__(txt,style,**kw); self.refkeys=set(refkeys)
        def split(self,a,b):
            chunks=super().split(a,b)
            for ch in chunks: ch.refkeys=set(self.refkeys)
            return chunks
    class RT(Table):
        def split(self,a,b):
            chunks=super().split(a,b)
            for ch in chunks: ch.refkeys=set(getattr(self,'refkeys',[]))
            return chunks
    def inline(s):
        rk=[]
        def repl(m):
            label,url=m.groups()
            if url not in keys:
                key=len(keys)+1;keys[url]=key;refs[key]=(clean(label),url)
            key=keys[url];rk.append(key)
            return f'<link href="{html.escape(url,quote=True)}" color="#315965">{html.escape(label)}</link><super size="7">[{key}]</super>'
        tokens=[]
        s=LINK.sub(lambda m:tokens.append(repl(m)) or f'ZZREF{len(tokens)-1}ZZ',s)
        s=html.escape(s)
        s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
        s=re.sub(r'`([^`]+)`',r'\1',s)
        for n,t in enumerate(tokens):s=s.replace(f'ZZREF{n}ZZ',t)
        return s,rk
    class Doc(BaseDocTemplate):
        def __init__(self,path):
            super().__init__(str(path),pagesize=A4,title='衣冠之间：汉服的历史、结构与日常',author='图解知识书项目',leftMargin=margin,rightMargin=margin,topMargin=60,bottomMargin=150)
            self.page_refs=set();self.chapter='衣冠之间';self.chapter_pages={}
            self.addPageTemplates(PageTemplate('normal',frames=[Frame(margin,150,bodywidth,H-215,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=self.start,onPageEnd=self.end))
        def start(self,c,d):
            self.page_refs=set()
            if self.page==1:
                c.saveState();c.setFillColor(HexColor('#f6f1e8'));c.rect(0,0,W,H,fill=1,stroke=0)
                c.setFillColor(HexColor('#853f35'));c.rect(33,H-270,3,190,fill=1,stroke=0)
                c.drawImage(str(ROOT/'assets/images/evidence-met-65598.jpg'),margin,175,width=bodywidth,height=170,preserveAspectRatio=True,anchor='c')
                c.setFillColor(HexColor('#526064'));c.setFont('STSong-Light',7)
                c.drawString(margin,158,'动物纹铭文锦，1—3世纪 / 大都会艺术博物馆 2003.385a–e / Public Domain')
                c.linkURL('https://www.metmuseum.org/art/collection/search/65598',(margin,154,W-margin,169),relative=0,thickness=0);c.restoreState()
        def afterFlowable(self,f):
            self.page_refs.update(getattr(f,'refkeys',[]))
            if hasattr(f,'chapter_title'):
                self.chapter=f.chapter_title;self.chapter_pages[self.chapter]=self.page
                bookmark='chapter-'+getattr(f,'chapter_slug',str(self.page))
                self.canv.bookmarkPage(bookmark);self.canv.addOutlineEntry(self.chapter,bookmark,0)
        def end(self,c,d):
            c.saveState();c.setStrokeColor(HexColor('#d9d0c3'));c.line(margin,H-40,W-margin,H-40)
            if self.page==1:c.restoreState();return
            c.setFont('STSong-Light',8);c.setFillColor(HexColor('#627074'));c.drawString(margin,H-30,'衣冠之间 / 汉服的历史、结构与日常');c.drawRightString(W-margin,H-30,str(self.page))
            if len(self.page_refs)>12:raise RuntimeError(f'too many references on page {self.page}: {len(self.page_refs)}')
            if self.page_refs:
                c.setStrokeColor(HexColor('#d9d0c3'));c.line(margin,137,W-margin,137)
                y=124;c.setFont('STSong-Light',7)
                for k in sorted(self.page_refs):
                    label,url=refs[k];domain=urlparse(url).netloc.removeprefix('www.')
                    s=f'[{k}] {label[:42]} | {domain}'
                    c.drawString(margin,y,s);c.linkURL(url,(margin,y-2,W-margin,y+8),relative=0,thickness=0);y-=9
            c.restoreState()
    def chapter_story(entry):
        p=ROOT/entry['source'];story=[]
        block_items=list(blocks(p.read_text()));skip=False;in_biblio=False
        for index,(kind,val) in enumerate(block_items):
            if skip:skip=False;continue
            if kind.startswith('h') and '本章资料' in val:
                prior={u for _,v in block_items[:index] for _,u in LINK.findall(str(v))}
                tail={u for _,v in block_items[index:] for _,u in LINK.findall(str(v))}
                # The PDF already supplies same-page source notes. Avoid an extra
                # almost-empty page containing only duplicate bibliography links.
                if tail<=prior:break
            if kind=='image':
                alt,rel=val;ip=(p.parent/rel).resolve()
                with PILImage.open(ip) as im:iw,ih=im.size
                scale=min(bodywidth/iw,350/ih);img=Image(str(ip),width=iw*scale,height=ih*scale);img.hAlign='CENTER'
                group=[Spacer(1,6),img,Spacer(1,8)]
                if index+1<len(block_items) and block_items[index+1][0]=='p' and block_items[index+1][1].startswith('图｜'):
                    t,r=inline(block_items[index+1][1]);group.append(RP(t,styles['caption'],r));skip=True
                story.append(KeepTogether(group));continue
            if kind=='table':
                width=max(len(r) for r in val);rows=[];rk=[]
                for row in val:
                    cells=[]
                    for cell in row+['']*(width-len(row)):
                        t,r=inline(cell);rk+=r;cells.append(RP(t,styles['cell'],r))
                    rows.append(cells)
                table=RT(rows,colWidths=[bodywidth/width]*width,repeatRows=1,hAlign='LEFT');table.refkeys=set(rk)
                table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#e9eee9')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#d8d9d1')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.extend([table,Spacer(1,10)]);continue
            if kind.startswith('h') and '本章资料' in val:in_biblio=True
            t,r=inline(val);sty=styles.get(kind,styles['p'])
            if in_biblio:sty=styles['h3'] if kind.startswith('h') else styles['biblio']
            f=RP(('· '+t) if kind=='li' else t,sty,r)
            if kind=='h1':f.chapter_title=clean(val);f.chapter_slug=entry['slug']
            story.append(f)
        return story
    outdir.mkdir(parents=True,exist_ok=True);(outdir/'chapters').mkdir(exist_ok=True)
    entries=manifest['chapters']+manifest.get('appendices',[])
    story=[]
    story.extend([Spacer(1,72),RP('衣冠之间',styles['cover-title']),RP('汉服的历史、结构与日常',styles['cover-subtitle']),Spacer(1,16),RP('《衣着有名》姊妹篇 · 独立新编',styles['p']),RP('从先秦衣裳到当代穿用，以证据认识衣冠，以结构理解穿着。',styles['p']),Spacer(1,22),RP('阅读版 · 2026年10月25日',styles['small']),RP('文物照片、历史图像、原创结构示意和生成插画均标明性质。涉及结构争议处保留证据限度；本书不提供等比例裁剪纸样。',styles['small']),PageBreak(),RP('目录与阅读路线',styles['h1'])])
    for e in entries:story.append(RP(f'<link href="#chapter-{e["slug"]}" color="#315965">{e["id"]}　{html.escape(e["title"])}</link>',styles['toc']))
    story.extend([Spacer(1,9),RP('历史线：03—12；结构与工艺线：02、13—20；案例与实践线：21—26。也可以从博物馆案例章开始，再回到相应时期。',styles['p'])])
    for e in entries:story.append(PageBreak());story+=chapter_story(e)
    doc=Doc(outdir/'Hanfu-Atlas.pdf');doc.build(story)
    chapter_pages=doc.chapter_pages
    for e in manifest['chapters']:Doc(outdir/'chapters'/f'{e["slug"]}.pdf').build(chapter_story(e))
    (ROOT/'references/source-catalog.json').write_text(json.dumps([{'id':k,'title':v[0],'url':v[1]} for k,v in refs.items()],ensure_ascii=False,indent=2))
    (outdir/'chapter-pages.json').write_text(json.dumps(chapter_pages,ensure_ascii=False,indent=2))
    return len(refs)

def validate(m):
    entries=m['chapters']+m.get('appendices',[]);count=0
    for e in entries:
        p=ROOT/e['source'];s=p.read_text()
        assert len(s)>250,f'Empty/short: {p}'
        assert not re.search(r'TODO|待补图|待撰写',s),p
        for alt,rel in IMAGE.findall(s):
            assert (p.parent/rel).is_file(),(p,rel);count+=1
    return count

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--format',choices=['pdf','epub','all','check'],default='all');a=ap.parse_args()
    m=json.loads((ROOT/'book.json').read_text());images=validate(m);out=ROOT/'output';out.mkdir(exist_ok=True)
    combined='# 衣冠之间\n\n## 汉服的历史、结构与日常\n\n《衣着有名》姊妹篇 · 独立新编\n\n'
    for e in m['chapters']+m.get('appendices',[]):combined+=(ROOT/e['source']).read_text()+'\n\n---\n\n'
    (out/'Hanfu-Atlas.md').write_text(combined)
    report={'chapters':len(m['chapters']),'image_placements':images}
    if a.format in ('all','pdf'):report['source_count']=build_pdf(m,out/'pdf')
    if a.format in ('all','epub'):report['epub_items']=build_epub(m,out/'Hanfu-Atlas.epub')
    (out/'build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
