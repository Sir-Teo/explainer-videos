"""Subtitle boundaries must preserve the identity of versioned model names."""
import copy
import re
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from explainer import lang
from explainer.voiceover import _keep_subtitle_terms, _sentences, _strip_bookmarks, _subtitle_term_boundaries, subtitle_cues


def timed(text, language="zh"):
    return [[word, i * 0.3, (i + 1) * 0.3]
            for i, word in enumerate(lang.tokens(text, language))]


class SubtitleModelVersionTests(unittest.TestCase):
    def test_rendered_part25_regressions(self):
        for text, model in [
            ("用AlphaFold-Multimer的预测来训练，教会了AlphaFold 3让这些区域保持松散。", "AlphaFold 3"),
            ("DeepMind报告说AlphaFold 3比最好的传统方法精确百分之五十。", "AlphaFold 3"),
            ("BindCraft通过在AlphaFold 2本身里做梯度下降来设计结合子，", "AlphaFold 2"),
            ("一年后，AlphaGeometry 2解出了2000年以来国际数学奥林匹克几何题的百分之八十四。", "AlphaGeometry 2"),
        ]:
            with self.subTest(model=model, text=text):
                lines = [{"words": timed(text)}]
                original = copy.deepcopy(lines)
                cues = subtitle_cues(lines, language="zh", preserve_terms=True)
                self.assertEqual(lines, original)
                self.assertTrue(any(model in cue[2] for cue in cues), cues)
                self.assertEqual("".join(c[2] for c in cues), text)
                self.assertTrue(all(a[1] <= b[0] for a, b in zip(cues, cues[1:])))

    def test_neighbour_cuts_and_token_times_survive(self):
        parts = [timed("一年后，AlphaGeometry"), timed(" 2解出了国际数学"), timed("奥林匹克题。")]
        parts[1][0][0] = " 2"
        original = copy.deepcopy(parts)
        result = _keep_subtitle_terms(parts, "zh", 24)
        self.assertEqual(parts, original)
        self.assertEqual(result[0], original[0] + [original[1][0]])
        self.assertEqual(result[1], original[1][1:])
        self.assertEqual(result[2], original[2])

    def test_move_name_right_when_left_has_no_room(self):
        parts = [timed("甲乙丙AlphaFold"), timed("2好")]
        result = _keep_subtitle_terms(parts, "zh", 11)
        self.assertEqual(lang.join([w[0] for w in result[0]], "zh"), "甲乙丙")
        self.assertEqual(lang.join([w[0] for w in result[1]], "zh"), "AlphaFold2好")

    def test_own_cue_when_both_neighbours_are_full(self):
        parts = [timed("甲乙丙AlphaFold"), timed("2甲乙丙丁戊己庚辛壬癸子丑")]
        result = _keep_subtitle_terms(parts, "zh", 11)
        self.assertEqual(len(result), 3)
        self.assertEqual(lang.join([w[0] for w in result[1]], "zh"), "AlphaFold2")
        self.assertEqual([w for part in result for w in part], [w for part in parts for w in part])

    def test_english_and_punctuation_boundaries_are_unchanged(self):
        for language, parts in [
            ("en", [timed("AlphaFold", "en"), timed("3 works.", "en")]),
            ("zh", [timed("AlphaFold，"), timed("3种方法。")]),
            ("zh", [timed("模型"), timed("3个。")]),
        ]:
            self.assertEqual(_keep_subtitle_terms(parts, language, 24), parts)

    def test_quoted_modifier_does_not_end_a_sentence(self):
        words = timed("再加门控，这叫“外向”更新；指向内的边也同样处理。")
        parts = _sentences(words, lang.SENTENCE_END["zh"], preserve_terms=True)
        self.assertEqual(lang.join([w[0] for w in parts[0]], "zh"), "再加门控，这叫“外向”更新；")
        quoted_sentence = timed("他说“完成。”然后离开。")
        self.assertEqual(len(_sentences(quoted_sentence, lang.SENTENCE_END["zh"], preserve_terms=True)), 2)

    def test_isolated_latin_subject_can_share_its_predicate(self):
        parts = [timed("而一个没有位置编码的"), timed("Transformer"), timed("把它的词元当作一个集合：")]
        result = _keep_subtitle_terms(parts, "zh", 24)
        self.assertEqual(len(result), 2)
        self.assertEqual(lang.join([w[0] for w in result[1]], "zh"), "Transformer把它的词元当作一个集合：")
        self.assertEqual([w for part in result for w in part], [w for part in parts for w in part])

    def test_long_versioned_name_respects_existing_wrapping_limit(self):
        text = "这是一个足够长的前缀，VeryLongScientificModel 2026负责处理接下来这段文字和数字。"
        lines = [{"words": timed(text)}]
        original = copy.deepcopy(lines)
        cues = subtitle_cues(lines, language="zh", preserve_terms=True)
        self.assertTrue(all(len(c[2]) <= lang.CUE_CHARS["zh"] for c in cues), cues)
        self.assertEqual("".join(c[2] for c in cues).replace(" ", ""), text.replace(" ", ""))
        self.assertEqual(lines, original)

    def test_math_and_numeric_tokens_survive_with_offset(self):
        text = "令L 2空间中的f(x)=x²，误差-3.5e-4，概率50%，样本30,000个，区间2000–2024。"
        lines = [{"words": timed(text)}]
        cues = subtitle_cues(lines, language="zh", preserve_terms=True)
        shifted = subtitle_cues(lines, offset=7.25, language="zh", preserve_terms=True)
        self.assertEqual(re.sub(r"\s", "", "".join(c[2] for c in cues)), re.sub(r"\s", "", text))
        for a, b in zip(cues, shifted):
            self.assertAlmostEqual(b[0] - a[0], 7.25)
            self.assertAlmostEqual(b[1] - a[1], 7.25)
            self.assertEqual(a[2], b[2])

    def test_bookmark_token_anchors_survive_subtitle_export(self):
        raw = ("前缀<bookmark mark='start'/>AlphaFold 2的误差为0.074。"
               "<bookmark mark='next'/>接下来推导。")
        with patch.object(lang, "LANG", "zh"):
            clean, marks = _strip_bookmarks(raw)
        tokens = lang.tokens(clean, "zh")
        self.assertEqual(tokens[marks["start"]], "AlphaFold")
        self.assertEqual(tokens[marks["next"]], "接")
        lines = [{"raw": raw, "words": timed(clean)}]
        original = copy.deepcopy(lines)
        subtitle_cues(lines, language="zh", preserve_terms=True)
        self.assertEqual(lines, original)


    def test_term_repairs_require_explicit_opt_in(self):
        text = "DeepMind报告说AlphaFold 3比最好的传统方法精确百分之五十。"
        lines = [{"words": timed(text)}]
        legacy = subtitle_cues(lines, language="zh")
        opted_in = subtitle_cues(lines, language="zh", preserve_terms=True)
        self.assertFalse(any("AlphaFold 3" in cue[2] for cue in legacy))
        self.assertTrue(any("AlphaFold 3" in cue[2] for cue in opted_in))

    def test_only_a_static_true_manifest_flag_enables_term_repairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "manifest.py"
            self.assertFalse(_subtitle_term_boundaries(manifest))
            for value, expected in [("True", True), ("False", False), ("'True'", False)]:
                manifest.write_text("SUBTITLE_TERM_BOUNDARIES = " + value + "\n")
                self.assertEqual(_subtitle_term_boundaries(manifest), expected)
            manifest.write_text("raise RuntimeError('must never execute')\n")
            self.assertFalse(_subtitle_term_boundaries(manifest))


if __name__ == "__main__":
    unittest.main()
