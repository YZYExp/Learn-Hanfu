#!/usr/bin/env python3
"""Prepare an embedded, renamed TrueType subset from OFL Noto Serif CJK."""
from pathlib import Path
import argparse, urllib.request
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
ROOT=Path(__file__).resolve().parents[1]
URL='https://raw.githubusercontent.com/notofonts/noto-cjk/main/Serif/OTF/SimplifiedChinese/NotoSerifCJKsc-Regular.otf'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--output',type=Path);ap.add_argument('--family',default='Hanfu Book Reader');ap.add_argument('--source-url',default=URL);a=ap.parse_args()
    source=a.source or ROOT/'build/NotoSerifCJKsc-Regular.otf'
    if not source.exists():
        source.parent.mkdir(parents=True,exist_ok=True)
        with urllib.request.urlopen(URL,timeout=60) as r:source.write_bytes(r.read())
    f=TTFont(source);original_names=f['name'];license_text=original_names.getDebugName(13) or 'SIL Open Font License 1.1';license_url=original_names.getDebugName(14) or 'https://openfontlicense.org/'
    corpus=''.join(p.read_text() for folder in ['chapters','appendices','scripts','references'] for p in (ROOT/folder).rglob('*') if p.suffix in ['.md','.py','.json'])
    chars={ord(c) for c in corpus}|set(range(32,127))|{0xb7,0x3000,0xff5c}
    missing=chars-set(f.getBestCmap());missing={x for x in missing if x>31}
    if missing:print('Characters absent in font:', ''.join(chr(x) for x in sorted(missing)))
    opt=subset.Options();opt.name_IDs=['*'];s=subset.Subsetter(options=opt);s.populate(unicodes=chars);s.subset(f)
    order=f.getGlyphOrder();gs=f.getGlyphSet();glyphs={}
    for name in order:
        pen=TTGlyphPen(gs);gs[name].draw(Cu2QuPen(pen,1,reverse_direction=True));glyphs[name]=pen.glyph()
    fb=FontBuilder(f['head'].unitsPerEm,isTTF=True);fb.setupGlyphOrder(order);fb.setupCharacterMap(f.getBestCmap());fb.setupGlyf(glyphs);fb.setupHorizontalMetrics(f['hmtx'].metrics)
    fb.setupHorizontalHeader(ascent=f['hhea'].ascent,descent=f['hhea'].descent)
    family=a.family;ps=family.replace(' ','')
    fb.setupNameTable({'familyName':family,'styleName':'Regular','uniqueFontIdentifier':ps+'-2026','fullName':family+' Regular','psName':ps+'-Regular','version':'Version 1.0','copyright':original_names.getDebugName(0) or 'Noto contributors','licenseDescription':license_text,'licenseInfoURL':license_url})
    fb.setupOS2(sTypoAscender=f['OS/2'].sTypoAscender,sTypoDescender=f['OS/2'].sTypoDescender,usWinAscent=f['OS/2'].usWinAscent,usWinDescent=f['OS/2'].usWinDescent);fb.setupPost();fb.setupMaxp()
    target=a.output or ROOT/'assets/fonts/HanfuBookReader.ttf'
    if not target.is_absolute():target=ROOT/target
    target.parent.mkdir(exist_ok=True);fb.save(target)
    (target.parent/('FONT-NOTICE-'+target.stem+'.md')).write_text('# Embedded font\n\n'+family+' is a renamed, subsetted TrueType derivative of the Noto CJK font named by the source URL, © Noto contributors, under SIL Open Font License 1.1. Cubic outlines were converted to quadratic outlines; only project characters are retained.\n\nSource: '+a.source_url+'\n\nLicense: '+license_url+'\n\n'+license_text+'\n')
    print('Prepared',len(order),'glyphs at',target)
if __name__=='__main__':main()
