"""Recomputed measurements must remain translated without swapping their units."""

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from explainer import lang, zh_text


class NumericCaptionTests(unittest.TestCase):
    def translate(self, table, caption):
        with patch.object(lang, "LANG", "zh"), patch.object(zh_text, "_TABLE", table), \
                patch.object(zh_text, "_BY_NUMBERS", None):
            return zh_text.translate(caption)

    def test_reordered_book_and_symbol_counts_follow_recomputed_data(self):
        table = json.loads((Path(__file__).resolve().parents[1] / "videos/ai/ai_text_zh.json").read_text())
        self.assertEqual(self.translate(table, "$22{,}788{,}051$ symbols from $30$ novels"),
                         "来自$30$部小说的$22{,}788{,}051$个符号")
        self.assertEqual(self.translate(table, "$1{,}234$ symbols from $7$ novels"),
                         "来自$7$部小说的$1{,}234$个符号")

    def test_ambiguous_repeated_number_reordering_is_not_inferred(self):
        table = {"strings": {"5 apples and 5 pears cost 10": "花10元买5个苹果和5个梨"}}
        caption = "7 apples and 8 pears cost 12"
        self.assertEqual(self.translate(table, caption), caption)

    def test_same_order_repeated_numbers_keep_existing_behavior(self):
        table = {"strings": {"5 apples and 5 pears": "5个苹果和5个梨"}}
        self.assertEqual(self.translate(table, "7 apples and 8 pears"), "7个苹果和8个梨")

    def test_reordered_templates_regress_both_bilingual_series(self):
        root = Path(__file__).resolve().parents[1] / "videos"
        checked = 0
        for path in sorted(root.glob("*/*_text_zh.json")):
            table = json.loads(path.read_text())
            for en, zh in table.get("strings", {}).items():
                ne, nz = zh_text._NUM.findall(en), zh_text._NUM.findall(zh)
                if not ne or ne == nz or len(ne) != len(set(ne)) or len(nz) != len(ne) or set(ne) != set(nz):
                    continue
                values = [("-" if value.startswith("-") else "") + str(700000 + i)
                          for i, value in enumerate(ne)]
                en_values = iter(values)
                modified = zh_text._NUM.sub(lambda _: next(en_values), en)
                zh_values = iter(values[ne.index(value)] for value in nz)
                expected = zh_text._NUM.sub(lambda _: next(zh_values), zh)
                with self.subTest(table=path.name, caption=en):
                    self.assertEqual(self.translate({"strings": {en: zh}}, modified),
                                     zh_text._SPACE.sub(r"\1\\ }", expected))
                checked += 1
        self.assertGreater(checked, 0)
