import json
import unittest
from pathlib import Path


class TextTableTests(unittest.TestCase):
    def test_ai_translation_entries_are_inside_supported_sections(self):
        root = Path(__file__).resolve().parents[1] / "videos" / "ai"
        paths = [root / "ai_text_zh.json", *root.glob("ai*/text_zh_add.json")]
        for path in paths:
            with self.subTest(table=path.name, part=path.parent.name):
                table = json.loads(path.read_text())
                self.assertLessEqual(set(table), {"strings", "phrases", "patterns"})
                self.assertIsInstance(table["strings"], dict)
                for key, value in table["strings"].items():
                    self.assertIsInstance(key, str)
                    self.assertIsInstance(value, str)


if __name__ == "__main__":
    unittest.main()
