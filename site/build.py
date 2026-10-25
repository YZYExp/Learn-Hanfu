#!/usr/bin/env python3
"""Build the reader without importing PDF/EPUB tooling."""
from pathlib import Path
import html, json, re, shutil, os
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
import markdown
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/site'
BOOK = json.loads((ROOT / 'book.json').read_text())
ENTRIES = BOOK['chapters'] + BOOK.get('appendices', [])
REPO = 'https://github.com/YZYExp/Learn-Hanfu'
E = html.escape
PAGES = {x['source']: x['slug'] + '.html' for x in ENTRIES}

def shell(title, body, active=None):
    links = ''.join(f'<li><a {"aria-current=\"page\"" if x == active else ""} href="{x["slug"]}.html"><span>{E(x["id"])}</span>{E(x["title"])}</a></li>' for x in ENTRIES)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="衣冠之间：汉服的历史、结构与日常。26章图解知识书，分章在线阅读。"><title>{E(title)} · 衣冠之间</title><link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#main">跳到正文</a><header><a class="brand" href="index.html">衣冠之间<small>汉服的历史、结构与日常</small></a><nav aria-label="主导航"><a href="index.html#contents">目录</a><a href="c-image-credits.html">图像与来源</a><a href="downloads.html">下载</a></nav></header><div class="layout"><aside><details><summary>全书目录 · 26 章</summary><ol>{links}</ol></details></aside><main id="main">{body}</main></div><footer>衣冠之间 · 图解知识书项目 · {E(BOOK['version'])}<br>馆藏图、原创示意、AI 插画分别标注。<a href="c-image-credits.html">图像权利说明</a> · <a href="{REPO}">查看源稿</a></footer><script>if(matchMedia("(min-width:901px)").matches)document.querySelector("aside details").open=true;</script></body></html>'''

class Rewrite(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False); self.source=source; self.parts=[]
    def handle_starttag(self, tag, attrs):
        out=[]
        for k,v in attrs:
            if k in ('href','src') and v and not urlsplit(v).scheme and not v.startswith(('#','//')):
                u=urlsplit(v); path=(ROOT/self.source).parent.joinpath(unquote(u.path)).resolve()
                rel=path.relative_to(ROOT).as_posix()
                if rel in PAGES: v=PAGES[rel]
                elif path.is_file(): v=rel; dest=OUT/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(path,dest)
                else: raise ValueError(f'Missing local target: {self.source}: {v}')
                if u.fragment: v += '#'+u.fragment
            out.append((k,v))
        if tag=='img': out += [('loading','lazy'),('decoding','async')]
        self.parts.append('<'+tag+''.join(' '+k+(f'="{E(v,quote=True)}"' if v is not None else '') for k,v in out)+'>')
    def handle_endtag(self,tag): self.parts.append('</'+tag+'>')
    def handle_data(self,d): self.parts.append(d)
    def handle_entityref(self,n): self.parts.append('&'+n+';')
    def handle_charref(self,n): self.parts.append('&#'+n+';')
    def handle_comment(self,d): self.parts.append('<!--'+d+'-->')

def build():
    shutil.rmtree(OUT,ignore_errors=True); OUT.mkdir(parents=True)
    assert len(PAGES)==len(ENTRIES), 'Duplicate sources'
    assert len(set(PAGES.values()))==len(ENTRIES), 'Duplicate slugs'
    for i,x in enumerate(ENTRIES):
        md=markdown.Markdown(extensions=['tables','fenced_code','toc','sane_lists'])
        content=md.convert((ROOT/x['source']).read_text())
        parser=Rewrite(x['source']); parser.feed(content)
        nav='<nav class="pager" aria-label="章节翻页">'
        if i: nav+=f'<a href="{ENTRIES[i-1]["slug"]}.html">← 上一篇<br>{E(ENTRIES[i-1]["title"])}</a>'
        if i+1<len(ENTRIES): nav+=f'<a href="{ENTRIES[i+1]["slug"]}.html">下一篇 →<br>{E(ENTRIES[i+1]["title"])}</a>'
        nav+='</nav>'
        body=f'<div class="eyebrow">衣冠之间 / {E(x["id"])}</div><details class="inpage"><summary>本篇内容</summary>{md.toc}</details><article>'+''.join(parser.parts)+'</article>'+nav
        (OUT/PAGES[x['source']]).write_text(shell(x['title'],body,x))
    groups=[('从证据出发',ENTRIES[:2]),('循历史阅读',ENTRIES[2:12]),('结构、材料与工艺',ENTRIES[12:20]),('案例与日常实践',ENTRIES[20:26]),('阅读工具',ENTRIES[26:])]
    cards=''.join(f'<section><h2>{title}</h2><div class="cards">'+''.join(f'<a href="{x["slug"]}.html"><span>{E(x["id"])}</span><strong>{E(x["title"])}</strong></a>' for x in group)+'</div></section>' for title,group in groups)
    home=f'''<section class="hero"><div class="eyebrow">一本面向兴趣读者的图解知识书</div><h1>衣冠之间</h1><p class="subtitle">汉服的历史、结构与日常</p><p>从一件衣物的领襟袖身出发，沿着历史、实物与日常生活，学会观察衣冠，也学会判断证据。</p><p class="meta">26 章 · 3 个附录 · 29 幅配图</p><a class="button" href="{ENTRIES[0]['slug']}.html">从第一章开始 →</a><a class="secondary" href="downloads.html">离线阅读与下载</a></section><img class="hero-image" src="assets/images/diagram-01.png" alt="实物、同期图像和文献能回答什么：原创教学示意"><p class="caption">原创教学示意。不同证据支持不同判断，不构成简单的证据等级排序。</p><div id="contents">{cards}</div>'''
    (OUT/'index.html').write_text(shell('在线阅读',home))
    downloads=[]
    for p in sorted((ROOT/'downloads').glob('*')):
        if p.is_file() and p.suffix in ('.pdf','.epub','.zip'):
            dest=OUT/'downloads'/p.name; dest.parent.mkdir(exist_ok=True); shutil.copyfile(p,dest)
            downloads.append(f'<li><a href="downloads/{E(p.name)}" download>{E(p.name)}</a> · {p.stat().st_size/1024/1024:.1f} MB</li>')
    body='<h1>离线阅读与下载</h1><p>在线正文与仓库 Markdown 使用同一套章节清单。</p>'
    body+=('<ul>'+''.join(downloads)+'</ul>') if downloads else '<p>PDF 与 EPUB 已另行交付，尚未附加到公共仓库。本页不提供失效或私有下载链接。</p>'
    body+=f'<p><a href="{REPO}/archive/refs/heads/main.zip">下载当前工程 ZIP</a> · <a href="{REPO}#构建">查看电子书构建方法</a></p><h2>使用与图像权利</h2><p>5 张中国博物馆官方图片仅为相关藏品的必要教学评述引用，保留原署名与水印，未获开放许可。不要将素材目录视为可自由再发布的图片包。10 张海外馆藏图的 Public Domain / CC0 标记及其余原创教学图、AI 示意性质见<a href="c-image-credits.html">图像来源与阅读资料</a>；下载不改变原始权利。</p>'
    (OUT/'downloads.html').write_text(shell('下载与使用',body))
    shutil.copyfile(ROOT/'site/style.css',OUT/'style.css'); (OUT/'.nojekyll').touch()
    (OUT/'build-info.json').write_text(json.dumps({'source_commit':os.environ.get('GITHUB_SHA','local'),'chapters':len(BOOK['chapters']),'appendices':len(BOOK['appendices'])}))
    check()

def check():
    class Links(HTMLParser):
        def handle_starttag(self,t,a):
            attrs=dict(a)
            for key in ('href','src'):
                u=urlsplit(attrs.get(key,''))
                if u.path and not u.scheme and not u.netloc:
                    target=(self.file.parent/unquote(u.path)).resolve()
                    assert target.is_relative_to(OUT.resolve()) and target.is_file(), f'{self.file}: missing {u.path}'
            if t=='img': assert attrs.get('alt'), f'{self.file}: missing alt'
    for p in OUT.glob('*.html'):
        parser=Links(); parser.file=p; parser.feed(p.read_text())
    assert len(list(OUT.glob('*.html')))==len(ENTRIES)+2
    assert len(list((OUT/'assets/images').glob('*')))==29
    print(f'PASS: {len(ENTRIES)+2} pages, 29 images, all local links and image alternatives')
if __name__=='__main__': build()
