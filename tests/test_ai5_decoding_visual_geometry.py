"""Actual local Manim geometry, AST only: no scene, producer or model imports."""
import ast
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np
from manim import (Axes, DecimalNumber, DOWN, RIGHT, Scene, TexTemplate, VGroup,
                   VectorizedPoint, VMobject, WHITE)

from explainer.analysis import WIDE_TEX, label
from explainer import lang, zh_text


ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'videos/ai/ai5/s11_decoding.py'
TREE=ast.parse(SOURCE.read_text())
FIXTURE=json.loads((ROOT/'tests/fixtures/ai5_decoding_cdf_contexts.json').read_text())


def axes():
    return Axes(x_range=[0,40,10],y_range=[0,1,.5],x_length=5.8,y_length=3.2,
                tips=False,axis_config={'include_ticks':False})


def actual_cdf(ax,probabilities):
    fn=next(n for n in ast.walk(TREE) if isinstance(n,ast.FunctionDef) and n.name=='truncate')
    value=next(n.value for n in ast.walk(fn) if isinstance(n,ast.Assign)
               and any(isinstance(t,ast.Name) and t.id=='cum' for t in n.targets))
    return eval(compile(ast.Expression(value),'actual-local-decoding-cdf','eval'),
                {'VMobject':VMobject,'np':np,'C':SimpleNamespace(BITS='#F7D154')},
                {'ax':ax,'N':40,'s':np.asarray(probabilities)})


def curve_coordinates(path,ax):
    return np.array([ax.p2c(path.get_nth_curve_function(i)(t))
                     for i in range(path.get_num_curves()) for t in np.linspace(0,1,33)])


class DecodingCDFGeometryTests(unittest.TestCase):
    def test_actual_cached_contexts_pass_exact_points_and_are_monotone_bounded(self):
        with patch.object(Scene,'__init__',side_effect=AssertionError('no Scene')):
            for row in FIXTURE['contexts']:
                with self.subTest(context=row['context']):
                    ax=axes();p=np.asarray(row['probabilities']);path=actual_cdf(ax,p)
                    expected=np.column_stack([np.arange(41),np.r_[0,np.cumsum(p)]])
                    anchors=np.vstack([path.get_start_anchors(),path.get_end()])
                    actual=np.array([ax.p2c(x) for x in anchors])
                    np.testing.assert_allclose(actual,expected,rtol=0,atol=5e-14)
                    sampled=curve_coordinates(path,ax)
                    self.assertGreaterEqual(float(np.diff(sampled[:,1]).min()),-1e-13)
                    self.assertGreaterEqual(float(sampled[:,1].min()),-1e-13)
                    self.assertLessEqual(float(sampled[:,1].max()),1+1e-13)
                    self.assertAlmostEqual(actual[-1,1],row['retained_mass'])

    def test_historical_smoothing_recipe_exercises_the_confident_regression_fixture(self):
        p=np.asarray(FIXTURE['contexts'][1]['probabilities']);ax=axes()
        # Frozen before recipe, not a requirement that shared curve() retain a
        # defect forever. This fixture must distinguish overshoot from the fix.
        old=VMobject().set_points_smoothly([ax.c2p(x,y) for x,y in zip(np.arange(41),np.r_[0,np.cumsum(p)])])
        sampled=curve_coordinates(old,ax)
        self.assertGreater(float(sampled[:,1].max()),1.01)
        self.assertLess(float(np.diff(sampled[:,1]).min()),-.001)

    def test_extreme_and_flat_probability_vectors_do_not_create_mass(self):
        for p in [np.r_[1.,np.zeros(39)],np.full(40,1/50257),np.zeros(40)]:
            ax=axes();path=actual_cdf(ax,p);sampled=curve_coordinates(path,ax)
            self.assertGreaterEqual(float(np.diff(sampled[:,1]).min()),-1e-13)
            self.assertLessEqual(float(sampled[:,1].max()),float(p.sum())+1e-13)


class EntropyReadoutGeometryTests(unittest.TestCase):
    def test_actual_readout_number_and_translated_units_keep_gap_at_all_widths(self):
        method=next(n for n in ast.walk(TREE) if isinstance(n,ast.FunctionDef) and n.name=='temperature')
        start=next(i for i,n in enumerate(method.body) if isinstance(n,ast.Assign)
                   and any(isinstance(t,ast.Name) and t.id=='hv' for t in n.targets))
        end=next(i for i,n in enumerate(method.body) if i>start and isinstance(n,ast.Expr)
                 and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute)
                 and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id=='hrd'
                 and n.value.func.attr=='next_to')
        block=ast.Module(method.body[start:end+1],type_ignores=[])
        self.assertFalse(any(isinstance(n,(ast.Import,ast.ImportFrom)) for n in ast.walk(block)))
        table=json.loads((ROOT/'videos/ai/ai_text_zh.json').read_text())
        cjk=WIDE_TEX.copy();cjk.tex_compiler='xelatex';cjk.output_format='.xdv'
        cjk.add_to_preamble(r'\usepackage{xeCJK}\setCJKmainfont{FandolSong-Regular.otf}[BoldFont=FandolSong-Bold.otf]')
        with patch.object(Scene,'__init__',side_effect=AssertionError('no Scene')):
            for language in ['en','zh']:
                state={'value':9.0}
                def actual_label(text,**kw):
                    if language=='zh':kw['tex_template']=cjk
                    return label(zh_text.translate(text),**kw)
                with patch.object(lang,'LANG',language),patch.object(zh_text,'_TABLE',table),patch.object(zh_text,'_BY_NUMBERS',None):
                    env=dict(DecimalNumber=DecimalNumber,VGroup=VGroup,label=actual_label,
                             C=SimpleNamespace(SURPRISE='#FF6B8B'),RIGHT=RIGHT,DOWN=DOWN,
                             ent=lambda:state['value'],trd=VectorizedPoint([4.4,.8,0]))
                    exec(compile(block,'actual-entropy-readout-block','exec'),env)
                    left=env['hrd'][0];number=env['hv'];unit=env['entropy_unit'];anchor=left.get_left().copy()
                    for value in [4.7,9.,9.9,10.,10.05,13.5,15.6,12.39,9.,4.7]:
                        with self.subTest(language=language,value=value):
                            state['value']=value;env['hrd'].update(0)
                            self.assertGreaterEqual(float(unit.get_left()[0]-number.get_right()[0]),.15-1e-12)
                            self.assertGreaterEqual(float(number.get_left()[0]-left.get_right()[0]),.15-1e-12)
                            self.assertLess(float(unit.get_right()[0]),6.9)
                            np.testing.assert_allclose(left.get_left(),anchor,atol=1e-12,rtol=0)
                    self.assertEqual(unit.tex_string,'比特' if language=='zh' else 'bits')


if __name__=='__main__':unittest.main()
