#!/usr/bin/env python3
"""Validate locale parity, HTML fragments and reproducible builds (stdlib only)."""
from __future__ import annotations
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent
class FragmentCheck(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.errors=[]
        self.feed(text); self.close()
        if self.stack: self.errors.append('unclosed tags: '+repr(self.stack))
    def handle_starttag(self,tag,attrs):
        if tag not in {'br','hr','img','input','meta','link'}: self.stack.append(tag)
        if tag in {'script','iframe'}: self.errors.append('unexpected active element: '+tag)
    def handle_startendtag(self,tag,attrs): pass
    def handle_endtag(self,tag):
        if not self.stack or self.stack[-1]!=tag: self.errors.append('unmatched tag: '+tag)
        else: self.stack.pop()

class RevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.locales={l:json.loads((ROOT/(l+'.json')).read_text(encoding='utf-8')) for l in ('en','uk','ru')}
        cls.diagram=json.loads((ROOT/'diagram.json').read_text(encoding='utf-8'))
        spec=importlib.util.spec_from_file_location('revision_build',ROOT/'build_i18n.py')
        cls.module=importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.module)
    def test_equal_translation_keys(self):
        for l in self.locales: self.assertEqual(set(self.locales['en']),set(self.locales[l]),l)
    def test_all_fragments_well_formed(self):
        for l,strings in self.locales.items():
            for key,text in strings.items():
                with self.subTest(language=l,key=key):
                    self.assertTrue(text.strip()); self.assertFalse(FragmentCheck(text).errors)
    def test_all_sections_have_both_lengths(self):
        for l,d in self.locales.items():
            for key in ['ladder','logic','agency','compute','beauty','reality','existence','ideas','selection','neighbors']:
                self.assertIn(key+'.short',d); self.assertIn(key+'.full',d)
    def test_bibliography_count_and_identity(self):
        for l,d in self.locales.items():
            self.assertEqual(d['sources.full'].count('<li '),29)
            for title in ['Nonlinear Dynamics and Chaos','The Strategy of the Genes','Driven by Compression Progress','Process and Reality','The Road to Reality']:
                self.assertIn(title,d['sources.full'])
    def test_removed_specific_slop(self):
        forbidden=['who, if not us','charges rent','hold it loosely','one caution keeps',
                   'хто, як не ми','не пропоную як догму','підйом легко перечитати',
                   'кто, если не мы','подъём легко перечитать','по основному хребтом','безмозглых клетках']
        for d in self.locales.values():
            text=' '.join(d.values()).lower()
            for term in forbidden: self.assertNotIn(term,text)
    def test_scientific_qualifications_retained(self):
        for l,words in {'en':['metaphysical','analogy','subjective experience'],
                       'uk':['метафізич','аналогі','суб’єктив'],
                       'ru':['метафизич','аналоги','субъектив']}.items():
            text=' '.join(self.locales[l].values()).lower()
            for word in words: self.assertIn(word,text)
    def test_diagram_parity(self):
        for l in self.locales:
            self.assertEqual(len(self.diagram[l]),73)
            self.assertTrue(all(isinstance(x,str) and x.strip() for x in self.diagram[l]))
    def test_english_has_no_accidental_cyrillic(self):
        self.assertFalse(re.search('[А-Яа-яІіЇїЄєҐґ]', ' '.join(self.locales['en'].values())))
    def test_html_and_runtime_have_same_strings(self):
        page=(ROOT/'index.html').read_text(encoding='utf-8')
        parsed=self.module.ContentRanges(page)
        for a,b,key in parsed.prose: self.assertEqual(page[a:b],self.locales['en'][key],key)
        js=(ROOT/'i18n.js').read_text(encoding='utf-8')
        actual=json.loads(js.split('const I18N = ',1)[1].rsplit(';',1)[0])
        self.assertEqual(actual,self.locales)
    def test_build_is_idempotent(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            for name in ['index.html','en.json','uk.json','ru.json','diagram.json']:
                shutil.copy2(ROOT/name,p/name)
            self.module.build(p)
            first={name:(p/name).read_bytes() for name in ('index.html','i18n.js')}
            self.module.build(p)
            for name,data in first.items(): self.assertEqual(data,(p/name).read_bytes(),name)

if __name__=='__main__': unittest.main(verbosity=2)
