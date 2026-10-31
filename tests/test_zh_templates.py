import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from explainer import lang, zh_text
from explainer.zh_templates import Translator, source_startswith, sources, table


class TemplateTests(unittest.TestCase):
    def test_quote_choice_does_not_hide_translation(self):
        self.assertTrue(source_startswith('f"After Bull, Durham costs {bits:.1f} bits."',
                                         "f'After Bull, Durham costs"))
        self.assertTrue(source_startswith('f"{row[\'P\']:.4f} percent"', "f'{row['P']:.4f} percent"))
        self.assertFalse(source_startswith('f"After Bull, Durham costs {bits:.1f} bits."',
                                          "f'After Bull, GPT-2"))
        self.assertTrue(source_startswith('f\"\"\"One of its {m[\'hidden\']} cells says "hello".\"\"\"',
                                         "f'One of its"))

    def test_computed_part_one_line_translates_with_current_source(self):
        tr = Translator("ai1")
        result = tr("The jump from counting, at 2.3 bits, to Qwen3 at 1.2 bits, is what this series is about: "
                    "what these models learned, and how.")
        self.assertIsNotNone(result)
        self.assertIn("2.3", result)
        self.assertIn("Qwen3 at 1.2 bits", result)
        self.assertNotIn("{", result)

    def test_complete_key_does_not_swallow_a_longer_conditional_branch(self):
        self.assertFalse(source_startswith('f"Needs {n} bits. Another sentence."', "f'Needs {n} bits.'"))
        self.assertTrue(source_startswith('f"Needs {n} bits."', "f'Needs {n} bits.'"))
        self.assertTrue(source_startswith('f"Needs {n} bits. Another sentence."', "f'Needs {n} bits."))

    def test_data_dependent_conclusions_have_unambiguous_translation_keys(self):
        # Quote normalization must not make opposite experimental conclusions
        # choose whichever translation happens to occur first in the table.
        for video in ("ai15", "ai16", "ai18", "ai20", "ai24", "ai28"):
            translations = table(video)["ZH"]
            for source in sources(video):
                text = source.get("en") or source["tpl"]
                hits = [key for key in translations if source_startswith(text, key)]
                with self.subTest(video=video, source=text):
                    self.assertTrue(hits)
                    self.assertEqual(len({translations[key] for key in hits}), 1)

    def test_new_math_caption_translates_with_any_computed_number(self):
        table = json.loads((Path(__file__).resolve().parents[1] / "videos/ai/ai_text_zh.json").read_text())
        with patch.object(lang, "LANG", "zh"), patch.object(zh_text, "_TABLE", table):
            translated = zh_text.translate(r"\text{ideal lower:}\ \sum_i i(q_i-q_{i+1})\log_2 i=1.36")
        self.assertNotIn("ideal lower", translated)
        self.assertIn("理想猜测下界", translated)
        self.assertIn("1.36", translated)

    def test_nested_verbatim_preserves_the_outer_guard(self):
        with zh_text.verbatim():
            with zh_text.verbatim():
                self.assertTrue(zh_text._VERBATIM[0])
            self.assertTrue(zh_text._VERBATIM[0])
        self.assertFalse(zh_text._VERBATIM[0])

    def test_displayed_code_identifiers_are_not_translated_as_labels(self):
        from manim import tempconfig
        from explainer.ai.viz import code_block

        with tempfile.TemporaryDirectory() as directory, tempconfig({"text_dir": directory}):
            with patch.object(lang, "LANG", "zh"), patch.object(zh_text, "_TABLE", {"strings": {"step": "步数"}}):
                code = code_block(["step"])
        self.assertEqual(code[0].text, "step")

    def test_scientific_notation_caption_survives_different_roundoff(self):
        table = json.loads((Path(__file__).resolve().parents[1] / "videos/ai/ai_text_zh.json").read_text())
        captions = [r"one example: \ singular values $0.101$, \ then $5 \times 10^{-18}$ and below",
                    r"by hand \ vs \ PyTorch: \ $5 \times 10^{-17}$"]
        with patch.object(lang, "LANG", "zh"), patch.object(zh_text, "_TABLE", table):
            for caption in captions:
                translated = zh_text.translate(caption)
                self.assertNotEqual(translated, caption)
                self.assertIn(r"\times 10^{", translated)
                self.assertFalse(zh_text.needs_translation(translated.replace("PyTorch", ""), False))


if __name__ == "__main__":
    unittest.main()
