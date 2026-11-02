"""Synthetic prose wrap contracts, with no scene, font or data imports."""
import importlib.util
from pathlib import Path
import re
import unittest

SOURCE=Path(__file__).resolve().parents[1]/'videos/ai/ai9/text_layout.py'
spec=importlib.util.spec_from_file_location('ai9_pure_text_layout',SOURCE)
layout=importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)


class ProseWrapping(unittest.TestCase):
    def test_closing_punctuation_stays_with_preceding_character(self):
        text='“甲乙丙丁，戊己庚辛。壬癸（甲乙），丙丁！”'
        for width in range(3,10):
            lines=layout.prose_lines(text,width,len)
            self.assertEqual(''.join(lines),text)
            self.assertTrue(all(line[0] not in layout._CLOSE for line in lines))
            self.assertTrue(all(line[-1] not in layout._OPEN for line in lines))
            self.assertTrue(all(len(line)<=width for line in lines))

    def test_latin_names_and_explicit_lines_retain_wording(self):
        text='甲 ADALINE，乙 Widrow-Hoff。\n丙1960年，丁。'
        lines=layout.prose_lines(text,12,len)
        self.assertEqual(re.sub(r'\s+','',''.join(lines)),re.sub(r'\s+','',text))
        self.assertTrue(any('ADALINE' in line for line in lines))
        self.assertTrue(any('Widrow-Hoff' in line for line in lines))
        self.assertTrue(any(line.startswith('丙') for line in lines))
        self.assertTrue(all(line[0] not in layout._CLOSE for line in lines))

    def test_real_font_measure_callback_controls_breaks(self):
        widths={'甲':2,'乙':2,'丙':2,'丁':2,'，':1}
        measure=lambda s:sum(widths[c] for c in s)
        lines=layout.prose_lines('甲乙丙，丁',5,measure)
        self.assertEqual(''.join(lines),'甲乙丙，丁')
        self.assertTrue(all(measure(line)<=5 for line in lines))
        self.assertTrue(all(not line.startswith('，') for line in lines))

    def test_named_phrases_remain_whole_when_a_break_is_needed(self):
        text='甲乙丙丁戊己， 斯坦福： ADALINE'
        lines=layout.prose_lines(text,10,len,atoms=['甲乙丙丁戊己，','斯坦福：','ADALINE'])
        self.assertEqual(re.sub(r'\s+','',''.join(lines)),re.sub(r'\s+','',text))
        self.assertTrue(any('斯坦福：' in line for line in lines))
        self.assertTrue(any('ADALINE' in line for line in lines))


if __name__=='__main__':unittest.main()
