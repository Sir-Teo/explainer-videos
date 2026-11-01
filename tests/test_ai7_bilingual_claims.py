"""Actual translation of current Part 7 source expressions; no scene/data imports."""
import ast
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

from explainer import lang, zh_text
from explainer.zh_templates import Translator

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai7'


def method(file, name):
    return next(n for n in ast.walk(ast.parse((PART / file).read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)


def voice(file, name):
    return next(n.args[0] for n in ast.walk(method(file, name))
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == 'voiceover' and n.args)


def value(node, **env):
    return eval(compile(ast.Expression(node), '<actual-source-fixture>', 'eval'), env)


def assigned(file, name, variable):
    return next(n.value for n in ast.walk(method(file, name))
                if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == variable for t in n.targets))


class BilingualClaims(unittest.TestCase):
    def setUp(self):
        self.translator = Translator('ai7')

    def translated(self, english):
        chinese = self.translator(english)
        self.assertIsNotNone(chinese)
        self.assertRegex(chinese, '[一-鿿]')
        self.assertEqual(lang.BOOKMARK.findall(english), lang.BOOKMARK.findall(chinese))
        self.assertNotRegex(chinese, r'\{[^{}]+\}')
        with patch.object(lang, 'LANG', 'zh'):
            self.assertEqual(lang.translate(english, PART, 'source-fixture'), lang.zh_numbers(chinese))
        return chinese

    def test_hook_uses_formatted_current_counts_not_old_default(self):
        english = value(voice('s01_hook.py', 'unlabelled'),
                        p={'n': 1234, 'd': 7}, g={'agree': .913})
        chinese = self.translated(english)
        self.assertIn('1234页', chinese)
        self.assertIn('7维', chinese)
        self.assertIn('91%', chinese)
        self.assertNotIn('639', chinese)
        self.assertNotIn('70维', chinese)

    def test_outro_recap_keeps_twelve_concepts_and_conditional_em_claim(self):
        chinese = self.translated(value(voice('s18_outro.py', 'recap')))
        self.assertEqual(lang.BOOKMARK.findall(chinese),
                         ['pca', 'ica', 'em', 'topics', 'hmm', 'alignment',
                          'counting', 'graphs', 'causes', 'gp', 'optimization', 'vi'])
        self.assertIn('E步取精确后验', chinese)
        self.assertIn('M步不降低同一个下界', chinese)
        self.assertIn('不会降低似然', chinese)

    def test_payoff_cues_preserve_cleaned_original_spoken_words(self):
        chinese = self.translated(value(voice('s18_outro.py', 'payoffs')))
        original = ('隐藏的部分会处处再现。模型1的对齐，在第13部分变成注意力，一种学出来的软对齐。'
                    '第15部分的状态空间模型，带着隐状态穿过时间；第16部分的混合专家，是会学着选择的混合模型。'
                    '前向算法在第23部分训练语音识别器。无限宽的网络就是高斯过程，见第12部分。'
                    'ELBO和重参数化技巧训练自编码器和扩散模型。手动设定激活值就是do算子，见第30部分。'
                    '而Kneser–Ney，是第9部分第一个神经语言模型要打败的那一行。')
        self.assertEqual(lang.clean(lang.BOOKMARK.sub('', chinese), 'zh'), lang.clean(original, 'zh'))
        self.assertEqual(lang.BOOKMARK.findall(chinese),
                         ['alignment', 'state', 'experts', 'forward', 'gp', 'elbo', 'causes', 'counting'])

    def test_validation_verdict_three_outcomes_translate_inside_main_clause(self):
        node = next(n for n in ast.parse((PART / 's03_ppca.py').read_text()).body
                    if isinstance(n, ast.FunctionDef) and n.name == 'ppca_verdict')
        namespace = {}
        exec(compile(ast.Module([node], type_ignores=[]), '<pure-helper>', 'exec'), namespace)
        for score, expected in [(-92.3, '高于'), (-93.1, '相同'), (-94.2, '低于')]:
            with self.subTest(score=score):
                verdict = namespace['ppca_verdict'](3, score, -93.1)
                english = value(voice('s03_ppca.py', 'heldout'),
                                p={'n_train': 321, 'n_test': 109}, verdict=verdict)
                chinese = self.translated(english)
                self.assertIn(expected, chinese)
                self.assertIn('109', chinese)
                self.assertIn('321', chinese)
                self.assertIn('不是一次新的测试', chinese)
                self.assertNotIn('On these validation pages', chinese)

    def test_context_count_branch_is_not_captured_by_obsolete_unique_prefix(self):
        for count in [1, 23]:
            with self.subTest(count=count):
                env = dict(INF_CAP=700, counts=[4321, count], L=2,
                           d={'median_L': 11, 'max_L': 39})
                env['last'] = value(assigned('s11_infini.py', 'grow', 'last'), **env)
                chinese = self.translated(value(voice('s11_infini.py', 'grow'), **env))
                self.assertIn('700', chinese)
                self.assertIn('4321', chinese)
                self.assertIn('39', chinese)
                self.assertNotIn('this context', chinese)
                if count == 23:
                    self.assertIn('23', chinese)
                    self.assertNotIn('再多一个就', chinese)

    def test_cavi_preview_and_final_saved_sweep_survive_recursive_verdict(self):
        for spread in [.2, .8]:
            env = dict(d={'N': 83, 'logp': -132.76, 'sd_mu_true': .5},
                       preview_updates=2, last_sweep=17, sdq=spread, narrower=spread < .5)
            env['verdict'] = value(assigned('s17_vi.py', 'cavi', 'verdict'), **env)
            chinese = self.translated(value(voice('s17_vi.py', 'cavi'), **env))
            self.assertIn('第17轮', chinese)
            self.assertIn('不是收敛检验', chinese)
            self.assertIn('-132.76', chinese)
            self.assertIn(f'{spread:.2f}', chinese)
            self.assertNotIn("q's spread", chinese)

    def test_graph_recursive_collider_and_tree_check_branches_keep_observations(self):
        for explained in [True, False]:
            env = dict(fk={'p_s_r': .23, 'p_s_nr': .71},
                       co={'p_r': .17, 'p_r_w': .67, 'p_r_ws': .19}, explained=explained)
            env['verdict'] = value(assigned('s12_graphs.py', 'dsep', 'verdict'), **env)
            chinese = self.translated(value(voice('s12_graphs.py', 'dsep'), **env))
            for number in ['23', '71', '17', '67', '19']:
                self.assertIn(number, chinese)
            self.assertIn('图所蕴含', chinese)
            self.assertNotIn('Simulate it', chinese)
        for err in [0., .0123]:
            env = dict(n=7, err=err, loopy=.0047)
            env['exact_say'] = value(assigned('s12_graphs.py', 'bp', 'exact_say'), **env)
            chinese = self.translated(value(voice('s12_graphs.py', 'bp'), **env))
            self.assertIn('128', chinese)
            self.assertIn('本地因子', chinese)
            self.assertIn('归一化', chinese)
            self.assertNotIn('it differs', chinese)
            if err:
                self.assertIn('0.0123', chinese)

    def test_occam_and_bo_conditional_verdicts_translate_without_prefix_truncation(self):
        for best in [3, 5]:
            env = dict(best=best, true=3, xp=list(range(19)))
            env['verdict'] = value(assigned('s15_occam.py', 'poly', 'verdict'), **env)
            chinese = self.translated(value(voice('s15_occam.py', 'poly'), **env))
            self.assertIn('19', chinese)
            self.assertIn('最小二乘', chinese)
            self.assertIn(str(best), chinese)
            self.assertNotIn('The evidence peaks', chinese)
        for close in [True, False]:
            for tuned in [True, False]:
                env = dict(close=close, tuned=tuned,
                           b={'evals': 13, 'best_D': .64, 'best_bits': 2.3145,
                              'grid_evals': 71, 'grid_best_bits': 2.3123, 'gt_bits': 2.3156})
                for variable in ['verdict', 'verdict2']:
                    env[variable] = value(assigned('s16_bayesopt.py', 'replay', variable), **env)
                chinese = self.translated(value(voice('s16_bayesopt.py', 'replay'), **env))
                self.assertIn('峰值缩放为一', chinese)
                for number in ['13', '0.64', '2.3145', '71', '2.3156']:
                    self.assertIn(number, chinese)
                self.assertNotIn('After 13 evaluations', chinese)

    def test_topics_bound_branches_are_explicit_source_keys_and_translate_in_context(self):
        for monotone in [True, False]:
            with self.subTest(monotone=monotone):
                rise = value(assigned('s06_lda.py', 'train', 'rise'), mono=monotone)
                self.assertIn(rise, self.translator.zh)
                self.assertEqual(self.translator.zh[rise], self.translator.phrases[rise])
                english = value(voice('s06_lda.py', 'train'), rise=rise,
                                l={'D': 2345, 'seg': 1800, 'V': 2760})
                chinese = self.translated(english)
                self.assertIn('2345', chinese)
                self.assertIn('1800', chinese)
                self.assertIn('2760', chinese)
                self.assertIn('没有下降' if monotone else '有限次更新可能降低', chinese)
                self.assertNotIn('this recorded bound', chinese)

    def test_dynamic_caption_patterns_retain_all_numbers_without_seed_entries(self):
        table = json.loads((ROOT / 'videos/ai/ai_text_zh.json').read_text())
        examples = [
            r'label-chosen cut, on these pages: \ $73\%$ sorted right',
            r'the $1{,}237$ validation pages',
            r'chosen: \ $k = 9$ \\ $42\%$ of training variance',
            r'excess kurtosis: \ $-1.25$ and $0.16$ for the whitened mixes, \ $-2.01$ and $-0.35$ for the voices',
            r'covariance eigenvalue floor: \ $10^{-9}$',
            r'one rule: \ move French adjectives before the noun: \ $0.87$',
            r'no fixed-order count table \\ this replay caps context at $700$ characters',
            r'$9$ length bands $b$ $\times$ $2$ types $s$: \\ one or several distinct next characters; \\ weights fitted on held-out novel text',
        ]
        with patch.object(lang, 'LANG', 'zh'), patch.object(zh_text, '_TABLE', table), \
                patch.object(zh_text, '_BY_NUMBERS', None):
            for english in examples:
                with self.subTest(english=english):
                    chinese = zh_text.translate(english)
                    self.assertRegex(chinese, '[一-鿿]')
                    self.assertEqual(zh_text._NUM.findall(chinese), zh_text._NUM.findall(english))
            self.assertNotIn('the $191$ validation pages', table['strings'])
            self.assertNotIn('label-chosen cut, on these pages: \\ $88\\%$ sorted right', table['strings'])


if __name__ == '__main__':
    unittest.main()
