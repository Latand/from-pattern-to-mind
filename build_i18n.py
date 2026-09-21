#!/usr/bin/env python3
"""Build the trilingual page from en.json, uk.json, ru.json and diagram.json.

The existing index.html supplies the layout, CSS, map geometry and interactions.
Only localized content, metadata, accessibility labels and the language handler
are replaced. No third-party Python packages are required. Run from any directory.
"""
from __future__ import annotations
import argparse
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re

LANGUAGES = ('en', 'uk', 'ru')
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
ARIA = {'Language':'aria.language', 'Reading length':'aria.mode',
        'Zoom out':'aria.zoom_out', 'Zoom in':'aria.zoom_in',
        'Reset view':'aria.reset', 'Close modal':'aria.close',
        'Close dialog':'aria.close', 'Toggle detail':'aria.detail',
        'Open full text':'aria.detail'}

class ContentRanges(HTMLParser):
    """Locate editable spans without reserializing the surrounding HTML."""
    def __init__(self, text: str) -> None:
        super().__init__(convert_charrefs=False)
        self.text = text
        self.starts = [0]
        for m in re.finditer('\n', text): self.starts.append(m.end())
        self.stack: list[dict] = []
        self.prose: list[tuple[int,int,str]] = []
        self.labels: dict[str,list[tuple[int,int]]] = {l:[] for l in LANGUAGES}
        self.accessibility: list[tuple[int,int,str]] = []
        self.feed(text)
        self.close()

    def absolute_position(self) -> int:
        line,col = self.getpos()
        return self.starts[line-1]+col

    def handle_starttag(self, tag: str, attrs: list) -> None:
        a=dict(attrs)
        raw=self.get_starttag_text()
        start=self.absolute_position()
        lang=self.stack[-1]['lang'] if self.stack else None
        if tag=='g' and 'dgroup' in (a.get('class') or '').split(): lang=a.get('data-lang')
        key=a.get('data-i18n-aria') or ARIA.get(a.get('aria-label',''))
        if key:
            self.accessibility.append((start,start+len(raw),key))
        if tag not in VOID:
            self.stack.append({'tag':tag,'start':start+len(raw),'key':a.get('data-i18n'),'lang':lang})

    def handle_startendtag(self, tag: str, attrs: list) -> None:
        # SVG primitives are self-closing; localized SVG text uses paired tags.
        pass

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==tag:
                entry=self.stack[i]
                del self.stack[i:]
                end=self.absolute_position()
                if entry['key']: self.prose.append((entry['start'],end,entry['key']))
                if tag=='text' and entry['lang'] in self.labels:
                    self.labels[entry['lang']].append((entry['start'],end))
                return

LANGUAGE_JS = r'''<script>
/* fptm-language:start */
(function () {
  var buttons = document.querySelectorAll('.langswitch button');
  function setLang(lang) {
    if (!I18N[lang]) lang = 'en';
    var strings = I18N[lang];
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (Object.prototype.hasOwnProperty.call(strings, key)) el.innerHTML = strings[key];
    });
    document.querySelectorAll('[data-i18n-aria]').forEach(function (el) {
      var value = strings[el.getAttribute('data-i18n-aria')];
      if (value) el.setAttribute('aria-label', value);
    });
    document.querySelectorAll('svg .dgroup').forEach(function (group) {
      var active = group.getAttribute('data-lang') === lang;
      group.style.display = active ? '' : 'none';
      group.setAttribute('aria-hidden', active ? 'false' : 'true');
    });
    buttons.forEach(function (button) {
      var active = button.getAttribute('data-lang') === lang;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    document.title = strings['doc.title'];
    document.querySelectorAll('meta[name="description"],meta[property="og:description"],meta[name="twitter:description"]').forEach(function (el) {
      el.content = strings['meta.description'];
    });
    document.querySelectorAll('meta[property="og:title"],meta[name="twitter:title"]').forEach(function (el) {
      el.content = strings['doc.title'];
    });
    // Fit the translated diagram labels within the original node/edge geometry.
    document.querySelectorAll('svg .dgroup[data-lang="' + lang + '"] text[data-max-width]').forEach(function (el) {
      el.removeAttribute('textLength');
      var max = Number(el.getAttribute('data-max-width'));
      if (el.getComputedTextLength() > max) {
        el.setAttribute('textLength', max);
        el.setAttribute('lengthAdjust', 'spacingAndGlyphs');
      }
    });
    try { localStorage.setItem('fptm-lang', lang); } catch (e) {}
  }
  var saved = null;
  try { saved = localStorage.getItem('fptm-lang'); } catch (e) {}
  var initial = saved || (navigator.language || 'en').slice(0, 2).toLowerCase();
  buttons.forEach(function (button) {
    button.addEventListener('click', function () { setLang(button.getAttribute('data-lang')); });
  });
  setLang(initial);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { setLang(document.documentElement.lang); });
  }
})();
/* fptm-language:end */
</script>'''

def replace_ranges(text: str, replacements: list[tuple[int,int,str]]) -> str:
    last=len(text)+1
    for a,b,value in sorted(replacements,reverse=True):
        if not (0 <= a <= b < last):
            raise ValueError(f'Overlapping or invalid replacements near offset {a}')
        text=text[:a]+value+text[b:]
        last=a+1
    return text


def build(directory: Path) -> dict:
    page_path=directory/'index.html'
    text=page_path.read_text(encoding='utf-8')
    locales={l:json.loads((directory/(l+'.json')).read_text(encoding='utf-8')) for l in LANGUAGES}
    labels=json.loads((directory/'diagram.json').read_text(encoding='utf-8'))
    keys=set(locales['en'])
    for lang in LANGUAGES:
        if set(locales[lang]) != keys: raise ValueError(f'Mismatched translation keys: {lang}')
        if any(not isinstance(v,str) or not v.strip() for v in locales[lang].values()):
            raise ValueError(f'Empty or non-string translation: {lang}')
    parsed=ContentRanges(text)
    if not parsed.prose: raise ValueError('No data-i18n content found in index.html')
    edits=[]
    for a,b,key in parsed.prose:
        if key not in locales['en']: raise ValueError(f'Missing translation: {key}')
        edits.append((a,b,locales['en'][key]))
    for lang in LANGUAGES:
        spans=parsed.labels[lang]
        if len(spans)!=len(labels[lang]):
            raise ValueError(f'{lang}: found {len(spans)} SVG labels, expected {len(labels[lang])}')
        for (a,b),value in zip(spans,labels[lang]): edits.append((a,b,html.escape(value)))
    for a,b,key in parsed.accessibility:
        tag=text[a:b]
        value=html.escape(locales['en'][key],quote=True)
        tag=re.sub(r'aria-label=("[^"]*"|\x27[^\x27]*\x27)', 'aria-label="'+value+'"',tag)
        if 'data-i18n-aria=' not in tag: tag=tag[:-1]+' data-i18n-aria="'+key+'">'
        edits.append((a,b,tag))
    text=replace_ranges(text,edits)
    text=re.sub(r'<html\b[^>]*>', '<html lang="en">',text,count=1)
    text=re.sub(r'<title>.*?</title>', '<title>'+html.escape(locales['en']['doc.title'])+'</title>',text,count=1,flags=re.S)
    def metadata(m: re.Match) -> str:
        tag=m.group(0)
        if re.search(r'(?:name|property)=["\x27](?:description|og:description|twitter:description)["\x27]',tag):
            value=locales['en']['meta.description']
        elif re.search(r'(?:name|property)=["\x27](?:og:title|twitter:title)["\x27]',tag):
            value=locales['en']['doc.title']
        else: return tag
        return re.sub(r'content=("[^"]*"|\x27[^\x27]*\x27)',lambda _: 'content="'+html.escape(value,quote=True)+'"',tag)
    text=re.sub(r'<meta\b[^>]*>',metadata,text)
    # Older page templates omit the card IDs used by the existing map/modal code.
    def card_id(match: re.Match) -> str:
        opening,body,closing=match.groups()
        key=re.search(r'data-i18n="k\.([a-z]+)"',body)
        if key and not re.search(r'\bid=',opening):
            opening=opening[:-1]+' id="card-'+key.group(1)+'">'
        return opening+body+closing
    text=re.sub(r'(<section\b[^>]*>)(.*?)(</section>)',card_id,text,flags=re.S)
    # Set width limits on SVG labels only; retain every existing path and position.
    p=ContentRanges(text)
    edits=[]
    widths=[210,226,210,200,200,210,238,178,224,196,228,216,200,234,198,252,216,244,210,226]
    for lang,spans in p.labels.items():
        for i,(a,b) in enumerate(spans):
            maxwidth=None
            if 2<=i<42:
                w=widths[(i-2)//2]
                maxwidth=w-18 if i%2==0 else max(w+22,230)
            elif 42<=i<63: maxwidth=180
            elif 63<=i<67: maxwidth=220
            elif 68<=i<72: maxwidth=255
            elif i==72: maxwidth=1500
            if maxwidth:
                start=text.rfind('<text',0,a)
                tag=text[start:a]
                tag=re.sub(r'\s+(?:textLength|lengthAdjust|data-max-width)="[^"]*"','',tag)
                if i==72:
                    tag=re.sub(r'\bx="[^"]*"','x="40"',tag)
                    tag=re.sub(r'text-anchor="[^"]*"','text-anchor="start"',tag)
                tag=tag[:-1]+f' data-max-width="{maxwidth}">'
                edits.append((start,a,tag))
    text=replace_ranges(text,edits)
    # Replace only the language handler, leaving all pan/zoom/modal code intact.
    scripts=list(re.finditer(r'<script\b[^>]*>.*?</script>',text,re.S))
    handlers=[m for m in scripts if ('fptm-lang' in m.group(0) and 'setLang' in m.group(0))]
    if len(handlers)!=1: raise ValueError(f'Expected one language handler; found {len(handlers)}')
    h=handlers[0]
    text=text[:h.start()]+LANGUAGE_JS+text[h.end():]
    text=text.replace("var saved = localStorage.getItem('fptm-mode');",
                      "var saved = null; try { saved = localStorage.getItem('fptm-mode'); } catch (e) {}")
    js='// Generated by build_i18n.py. Edit the locale JSON files instead.\nconst I18N = '+json.dumps(locales,ensure_ascii=False,indent=2)+';\n'
    # Avoid HTML script termination if these strings are embedded in a preview.
    js=js.replace('</script','<\\/script')
    page_path.write_text(text,encoding='utf-8')
    (directory/'i18n.js').write_text(js,encoding='utf-8')
    return {'languages':list(LANGUAGES),'keys_per_language':len(keys),
            'diagram_labels_per_language':{l:len(labels[l]) for l in LANGUAGES},
            'html_bytes':len(text.encode('utf-8'))}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args()
    print(json.dumps(build(args.directory.resolve()),ensure_ascii=False,indent=2))
