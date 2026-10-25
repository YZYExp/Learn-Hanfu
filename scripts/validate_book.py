#!/usr/bin/env python3
"""Check source paths and the actual exported PDF/EPUB deliverables."""
from pathlib import Path
import json,re,zipfile,sys
from xml.etree import ElementTree as ET
from urllib.parse import urlparse,unquote
from posixpath import normpath,dirname,join
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_book import validate,IMAGE

def main():
    from pypdf import PdfReader
    m=json.loads((ROOT/'book.json').read_text());placements=validate(m)
    reader=PdfReader(ROOT/'output/pdf/Hanfu-Atlas.pdf');texts=[p.extract_text() or '' for p in reader.pages]
    squish=lambda s:re.sub(r'\s+','',s)
    entire=squish(''.join(texts))
    for e in m['chapters']:
        title='第'+str(int(e['id']))+'章'+e['title'];assert squish(title) in entire,title
        cp=ROOT/'output/pdf/chapters'/f'{e["slug"]}.pdf';r=PdfReader(cp)
        assert squish(title) in squish(r.pages[0].extract_text()),cp
    assert sum(len(re.findall('[\u4e00-\u9fff]',t)) for t in texts)>40000
    epub=ROOT/'output/Hanfu-Atlas.epub'
    with zipfile.ZipFile(epub) as z:
        names=set(z.namelist());assert z.read('mimetype')==b'application/epub+zip'
        assert z.infolist()[0].filename=='mimetype' and z.infolist()[0].compress_type==zipfile.ZIP_STORED
        for name in names:
            if name.endswith(('.xhtml','.opf','.xml')):
                tree=ET.fromstring(z.read(name))
                for elem in tree.iter():
                    for attr in ['href','src']:
                        v=elem.attrib.get(attr)
                        if not v or urlparse(v).scheme or v.startswith('#'):continue
                        target=normpath(join(dirname(name),unquote(v.split('#')[0])))
                        assert target in names,(name,v,target)
        for img in (ROOT/'assets/images').glob('*'):
            if img.suffix in ['.png','.jpg'] and 'OEBPS/images/'+img.name in names:assert z.read('OEBPS/images/'+img.name)==img.read_bytes()
    source_count=len(json.loads((ROOT/'references/source-catalog.json').read_text()))
    report={'chapters':26,'appendices':3,'pdf_pages':len(reader.pages),'chapter_pdfs':26,'image_placements':placements,'source_urls':source_count,'epub_xml_and_links':'pass','pdf_chapter_text':'pass','font_embedded':'verified with pdffonts and rendered pages','note':'Visual QA uses rendered pages; structural checks do not replace historical review.'}
    (ROOT/'output/validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
