"""Measured captions must translate after locale formatting changes."""

from unittest.mock import patch

from explainer import lang, zh_text


def translate(strings, text):
    with patch.object(lang, "LANG", "zh"), patch.object(zh_text, "_TABLE", {"strings": strings}), \
            patch.object(zh_text, "_BY_NUMBERS", None):
        return zh_text.translate(text)


def test_grouped_english_and_ungrouped_chinese_numbers_form_a_template():
    table = {"our table-filler (Python): 118,503 rows a second": "我们的填表程序（Python）：每秒118503行"}
    assert translate(table, "our table-filler (Python): 102,957 rows a second") == \
        "我们的填表程序（Python）：每秒102,957行"


def test_reordered_grouped_values_keep_their_roles():
    assert translate({"1,000 trials in 20 runs": "20次运行共1000次试验"},
                     "2,000 trials in 40 runs") == "40次运行共2,000次试验"


def test_tex_grouping_matches_plain_digits():
    assert translate({r"1{,}000 rows": "1000行"}, r"2{,}000 rows") == r"2{,}000行"


def test_decimal_comma_is_not_assumed_to_be_thousands_grouping():
    text = "rate 2,5"
    assert translate({"rate 1,5": "速率15"}, text) == text


def test_semantically_duplicate_values_do_not_allow_guessed_reordering():
    text = "a 2,000 b 2000 c 30"
    assert translate({"a 1,000 b 1000 c 20": "20与1000与1000"}, text) == text
