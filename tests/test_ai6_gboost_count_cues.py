"""Actual captured silent word clocks and source-only cue replay; no scene/render/TTS."""
from __future__ import annotations

import ast
import copy
import json
import math
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest import mock

import numpy as np

from explainer import lang, tts
from explainer.zh_templates import Translator, translator
from test_ai1_entropy_prefix_timing import installed_quantizer

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'videos/ai/ai6/s16_gboost.py'
FROZEN_INPUTS = json.loads(r'''{
  "en": {
    "source": "/workspace/runtime/ai6-remaining-qa-serial/runs/20261101T064932/16-GradientBoosting/en/motion/completed/media/videos/480p15/GradientBoosting.narration.json",
    "file_sha256": "e4ab4ed7dd2179282a5d51b856cffd7ed99b3a604949cf79fbea2b3cb5353a7e",
    "block": {
      "start": 90.3333333333336,
      "duration": 29.955541666666665,
      "text": "Watch it learn on the two plotted rates. One tree: a few boxes. Ten, thirty: the boundary sharpens where the authors meet. The training loss keeps falling, but the held-out pages are best after 4 rounds, at 83.2 percent. By round 200 they've slipped to 77.5: with only two numbers per page, the extra detail fits the training pages, not the authors. Stopping early is part of the method.",
      "raw": "Watch it learn on the two plotted rates. <bookmark mark='a'/> One tree: a few boxes. <bookmark mark='b'/> Ten, thirty: the boundary sharpens where the authors meet. <bookmark mark='c'/> The training loss keeps falling, but the held-out pages are best after 4 rounds, at 83.2 percent. <bookmark mark='d'/> By round 200 they've slipped to 77.5: with only two numbers per page, the extra detail fits the training pages, not the authors. Stopping early is part of the method.",
      "words": [
        [
          "Watch",
          90.6333333333336,
          91.06167471819673
        ],
        [
          "it",
          91.06167471819673,
          91.49001610305984
        ],
        [
          "learn",
          91.49001610305984,
          91.91835748792298
        ],
        [
          "on",
          91.91835748792298,
          92.34669887278609
        ],
        [
          "the",
          92.34669887278609,
          92.77504025764922
        ],
        [
          "two",
          92.77504025764922,
          93.20338164251234
        ],
        [
          "plotted",
          93.20338164251234,
          93.63172302737547
        ],
        [
          "rates.",
          93.63172302737547,
          94.06006441223859
        ],
        [
          "One",
          94.06006441223859,
          94.48840579710172
        ],
        [
          "tree:",
          94.48840579710172,
          94.91674718196484
        ],
        [
          "a",
          94.91674718196484,
          95.34508856682797
        ],
        [
          "few",
          95.34508856682797,
          95.77342995169109
        ],
        [
          "boxes.",
          95.77342995169109,
          96.20177133655422
        ],
        [
          "Ten,",
          96.20177133655422,
          96.63011272141733
        ],
        [
          "thirty:",
          96.63011272141733,
          97.05845410628046
        ],
        [
          "the",
          97.05845410628046,
          97.48679549114358
        ],
        [
          "boundary",
          97.48679549114358,
          97.91513687600671
        ],
        [
          "sharpens",
          97.91513687600671,
          98.34347826086983
        ],
        [
          "where",
          98.34347826086983,
          98.77181964573296
        ],
        [
          "the",
          98.77181964573296,
          99.20016103059608
        ],
        [
          "authors",
          99.20016103059608,
          99.62850241545921
        ],
        [
          "meet.",
          99.62850241545921,
          100.05684380032233
        ],
        [
          "The",
          100.05684380032233,
          100.48518518518546
        ],
        [
          "training",
          100.48518518518546,
          100.91352657004857
        ],
        [
          "loss",
          100.91352657004857,
          101.3418679549117
        ],
        [
          "keeps",
          101.3418679549117,
          101.77020933977482
        ],
        [
          "falling,",
          101.77020933977482,
          102.19855072463795
        ],
        [
          "but",
          102.19855072463795,
          102.62689210950107
        ],
        [
          "the",
          102.62689210950107,
          103.0552334943642
        ],
        [
          "held-out",
          103.0552334943642,
          103.48357487922732
        ],
        [
          "pages",
          103.48357487922732,
          103.91191626409045
        ],
        [
          "are",
          103.91191626409045,
          104.34025764895357
        ],
        [
          "best",
          104.34025764895357,
          104.7685990338167
        ],
        [
          "after",
          104.7685990338167,
          105.19694041867982
        ],
        [
          "4",
          105.19694041867982,
          105.62528180354295
        ],
        [
          "rounds,",
          105.62528180354295,
          106.05362318840606
        ],
        [
          "at",
          106.05362318840606,
          106.48196457326918
        ],
        [
          "83.2",
          106.48196457326918,
          106.91030595813231
        ],
        [
          "percent.",
          106.91030595813231,
          107.33864734299544
        ],
        [
          "By",
          107.33864734299544,
          107.76698872785856
        ],
        [
          "round",
          107.76698872785856,
          108.19533011272168
        ],
        [
          "200",
          108.19533011272168,
          108.62367149758481
        ],
        [
          "they've",
          108.62367149758481,
          109.05201288244794
        ],
        [
          "slipped",
          109.05201288244794,
          109.48035426731106
        ],
        [
          "to",
          109.48035426731106,
          109.90869565217417
        ],
        [
          "77.5:",
          109.90869565217417,
          110.3370370370373
        ],
        [
          "with",
          110.3370370370373,
          110.76537842190044
        ],
        [
          "only",
          110.76537842190044,
          111.19371980676355
        ],
        [
          "two",
          111.19371980676355,
          111.62206119162667
        ],
        [
          "numbers",
          111.62206119162667,
          112.0504025764898
        ],
        [
          "per",
          112.0504025764898,
          112.47874396135293
        ],
        [
          "page,",
          112.47874396135293,
          112.90708534621605
        ],
        [
          "the",
          112.90708534621605,
          113.33542673107917
        ],
        [
          "extra",
          113.33542673107917,
          113.7637681159423
        ],
        [
          "detail",
          113.7637681159423,
          114.19210950080543
        ],
        [
          "fits",
          114.19210950080543,
          114.62045088566855
        ],
        [
          "the",
          114.62045088566855,
          115.04879227053166
        ],
        [
          "training",
          115.04879227053166,
          115.4771336553948
        ],
        [
          "pages,",
          115.4771336553948,
          115.90547504025793
        ],
        [
          "not",
          115.90547504025793,
          116.33381642512104
        ],
        [
          "the",
          116.33381642512104,
          116.76215780998416
        ],
        [
          "authors.",
          116.76215780998416,
          117.19049919484729
        ],
        [
          "Stopping",
          117.19049919484729,
          117.61884057971042
        ],
        [
          "early",
          117.61884057971042,
          118.04718196457354
        ],
        [
          "is",
          118.04718196457354,
          118.47552334943666
        ],
        [
          "part",
          118.47552334943666,
          118.90386473429979
        ],
        [
          "of",
          118.90386473429979,
          119.33220611916292
        ],
        [
          "the",
          119.33220611916292,
          119.76054750402604
        ],
        [
          "method.",
          119.76054750402604,
          120.18888888888915
        ]
      ]
    }
  },
  "zh": {
    "source": "/workspace/runtime/ai6-remaining-qa-serial/runs/20261101T064932/16-GradientBoosting/zh/motion/completed/media/videos/480p15/GradientBoosting.narration.json",
    "file_sha256": "886df67b207148d27e7821139f6c0e8a36efc838cfd1f6e32eda1b7e73f5d3e8",
    "block": {
      "start": 95.66666666666693,
      "duration": 32.091833333333334,
      "text": "看它在图上这两个词频上学习。一棵树：几个方格。10棵，30棵：在两位作者交界的地方，边界越来越清晰。训练损失一直在下降，但留出的书页在第4轮之后最好，判对83.2%。到第200轮，已经滑落到77.5%：每页只有两个数，多出来的细节拟合的是训练页，而不是作者。及早停下，本身就是这个方法的一部分。",
      "raw": "Watch it learn on the two plotted rates. <bookmark mark='a'/> One tree: a few boxes. <bookmark mark='b'/> Ten, thirty: the boundary sharpens where the authors meet. <bookmark mark='c'/> The training loss keeps falling, but the held-out pages are best after 4 rounds, at 83.2 percent. <bookmark mark='d'/> By round 200 they've slipped to 77.5: with only two numbers per page, the extra detail fits the training pages, not the authors. Stopping early is part of the method.",
      "words": [
        [
          "看",
          95.96666666666692,
          96.23524175535435
        ],
        [
          "它",
          96.23524175535435,
          96.50381684404178
        ],
        [
          "在",
          96.50381684404178,
          96.7723919327292
        ],
        [
          "图",
          96.7723919327292,
          97.04096702141663
        ],
        [
          "上",
          97.04096702141663,
          97.30954211010406
        ],
        [
          "这",
          97.30954211010406,
          97.57811719879149
        ],
        [
          "两",
          97.57811719879149,
          97.84669228747892
        ],
        [
          "个",
          97.84669228747892,
          98.11526737616633
        ],
        [
          "词",
          98.11526737616633,
          98.38384246485376
        ],
        [
          "频",
          98.38384246485376,
          98.65241755354118
        ],
        [
          "上",
          98.65241755354118,
          98.92099264222861
        ],
        [
          "学",
          98.92099264222861,
          99.18956773091604
        ],
        [
          "习。",
          99.18956773091604,
          99.45814281960347
        ],
        [
          "一",
          99.45814281960347,
          99.7267179082909
        ],
        [
          "棵",
          99.7267179082909,
          99.99529299697832
        ],
        [
          "树：",
          99.99529299697832,
          100.26386808566575
        ],
        [
          "几",
          100.26386808566575,
          100.53244317435318
        ],
        [
          "个",
          100.53244317435318,
          100.8010182630406
        ],
        [
          "方",
          100.8010182630406,
          101.06959335172803
        ],
        [
          "格。",
          101.06959335172803,
          101.33816844041546
        ],
        [
          "10",
          101.33816844041546,
          101.60674352910289
        ],
        [
          "棵，",
          101.60674352910289,
          101.8753186177903
        ],
        [
          "30",
          101.8753186177903,
          102.14389370647773
        ],
        [
          "棵：",
          102.14389370647773,
          102.41246879516515
        ],
        [
          "在",
          102.41246879516515,
          102.68104388385258
        ],
        [
          "两",
          102.68104388385258,
          102.94961897254001
        ],
        [
          "位",
          102.94961897254001,
          103.21819406122744
        ],
        [
          "作",
          103.21819406122744,
          103.48676914991486
        ],
        [
          "者",
          103.48676914991486,
          103.75534423860229
        ],
        [
          "交",
          103.75534423860229,
          104.02391932728972
        ],
        [
          "界",
          104.02391932728972,
          104.29249441597715
        ],
        [
          "的",
          104.29249441597715,
          104.56106950466457
        ],
        [
          "地",
          104.56106950466457,
          104.82964459335199
        ],
        [
          "方，",
          104.82964459335199,
          105.09821968203941
        ],
        [
          "边",
          105.09821968203941,
          105.36679477072684
        ],
        [
          "界",
          105.36679477072684,
          105.63536985941427
        ],
        [
          "越",
          105.63536985941427,
          105.9039449481017
        ],
        [
          "来",
          105.9039449481017,
          106.17252003678912
        ],
        [
          "越",
          106.17252003678912,
          106.44109512547655
        ],
        [
          "清",
          106.44109512547655,
          106.70967021416398
        ],
        [
          "晰。",
          106.70967021416398,
          106.9782453028514
        ],
        [
          "训",
          106.9782453028514,
          107.24682039153882
        ],
        [
          "练",
          107.24682039153882,
          107.51539548022625
        ],
        [
          "损",
          107.51539548022625,
          107.78397056891367
        ],
        [
          "失",
          107.78397056891367,
          108.0525456576011
        ],
        [
          "一",
          108.0525456576011,
          108.32112074628853
        ],
        [
          "直",
          108.32112074628853,
          108.58969583497596
        ],
        [
          "在",
          108.58969583497596,
          108.85827092366338
        ],
        [
          "下",
          108.85827092366338,
          109.1268460123508
        ],
        [
          "降，",
          109.1268460123508,
          109.39542110103822
        ],
        [
          "但",
          109.39542110103822,
          109.66399618972565
        ],
        [
          "留",
          109.66399618972565,
          109.93257127841308
        ],
        [
          "出",
          109.93257127841308,
          110.2011463671005
        ],
        [
          "的",
          110.2011463671005,
          110.46972145578793
        ],
        [
          "书",
          110.46972145578793,
          110.73829654447536
        ],
        [
          "页",
          110.73829654447536,
          111.00687163316279
        ],
        [
          "在",
          111.00687163316279,
          111.27544672185022
        ],
        [
          "第",
          111.27544672185022,
          111.54402181053763
        ],
        [
          "4",
          111.54402181053763,
          111.81259689922506
        ],
        [
          "轮",
          111.81259689922506,
          112.08117198791248
        ],
        [
          "之",
          112.08117198791248,
          112.34974707659991
        ],
        [
          "后",
          112.34974707659991,
          112.61832216528734
        ],
        [
          "最",
          112.61832216528734,
          112.88689725397477
        ],
        [
          "好，",
          112.88689725397477,
          113.1554723426622
        ],
        [
          "判",
          113.1554723426622,
          113.42404743134962
        ],
        [
          "对",
          113.42404743134962,
          113.69262252003705
        ],
        [
          "83.2%。",
          113.69262252003705,
          113.96119760872448
        ],
        [
          "到",
          113.96119760872448,
          114.2297726974119
        ],
        [
          "第",
          114.2297726974119,
          114.49834778609933
        ],
        [
          "200",
          114.49834778609933,
          114.76692287478676
        ],
        [
          "轮，",
          114.76692287478676,
          115.03549796347419
        ],
        [
          "已",
          115.03549796347419,
          115.30407305216161
        ],
        [
          "经",
          115.30407305216161,
          115.57264814084904
        ],
        [
          "滑",
          115.57264814084904,
          115.84122322953647
        ],
        [
          "落",
          115.84122322953647,
          116.1097983182239
        ],
        [
          "到",
          116.1097983182239,
          116.37837340691132
        ],
        [
          "77.5%：",
          116.37837340691132,
          116.64694849559875
        ],
        [
          "每",
          116.64694849559875,
          116.91552358428618
        ],
        [
          "页",
          116.91552358428618,
          117.1840986729736
        ],
        [
          "只",
          117.1840986729736,
          117.45267376166103
        ],
        [
          "有",
          117.45267376166103,
          117.72124885034846
        ],
        [
          "两",
          117.72124885034846,
          117.98982393903589
        ],
        [
          "个",
          117.98982393903589,
          118.25839902772331
        ],
        [
          "数，",
          118.25839902772331,
          118.52697411641074
        ],
        [
          "多",
          118.52697411641074,
          118.79554920509817
        ],
        [
          "出",
          118.79554920509817,
          119.0641242937856
        ],
        [
          "来",
          119.0641242937856,
          119.33269938247302
        ],
        [
          "的",
          119.33269938247302,
          119.60127447116045
        ],
        [
          "细",
          119.60127447116045,
          119.86984955984788
        ],
        [
          "节",
          119.86984955984788,
          120.1384246485353
        ],
        [
          "拟",
          120.1384246485353,
          120.40699973722273
        ],
        [
          "合",
          120.40699973722273,
          120.67557482591016
        ],
        [
          "的",
          120.67557482591016,
          120.94414991459759
        ],
        [
          "是",
          120.94414991459759,
          121.21272500328502
        ],
        [
          "训",
          121.21272500328502,
          121.48130009197244
        ],
        [
          "练",
          121.48130009197244,
          121.74987518065987
        ],
        [
          "页，",
          121.74987518065987,
          122.0184502693473
        ],
        [
          "而",
          122.0184502693473,
          122.28702535803473
        ],
        [
          "不",
          122.28702535803473,
          122.55560044672215
        ],
        [
          "是",
          122.55560044672215,
          122.82417553540958
        ],
        [
          "作",
          122.82417553540958,
          123.09275062409701
        ],
        [
          "者。",
          123.09275062409701,
          123.36132571278443
        ],
        [
          "及",
          123.36132571278443,
          123.62990080147186
        ],
        [
          "早",
          123.62990080147186,
          123.89847589015929
        ],
        [
          "停",
          123.89847589015929,
          124.16705097884672
        ],
        [
          "下，",
          124.16705097884672,
          124.43562606753414
        ],
        [
          "本",
          124.43562606753414,
          124.70420115622157
        ],
        [
          "身",
          124.70420115622157,
          124.972776244909
        ],
        [
          "就",
          124.972776244909,
          125.24135133359643
        ],
        [
          "是",
          125.24135133359643,
          125.50992642228385
        ],
        [
          "这",
          125.50992642228385,
          125.77850151097128
        ],
        [
          "个",
          125.77850151097128,
          126.04707659965871
        ],
        [
          "方",
          126.04707659965871,
          126.31565168834614
        ],
        [
          "法",
          126.31565168834614,
          126.58422677703356
        ],
        [
          "的",
          126.58422677703356,
          126.85280186572099
        ],
        [
          "一",
          126.85280186572099,
          127.12137695440842
        ],
        [
          "部",
          127.12137695440842,
          127.38995204309585
        ],
        [
          "分。",
          127.38995204309585,
          127.65852713178327
        ]
      ]
    }
  }
}
''')


OLD_ZH_RAW = "看它在图上这两个词频上学习。<bookmark mark='a'/>一棵树：几个方格。<bookmark mark='b'/>10棵，30棵：在两位作者交界的地方，边界越来越清晰。<bookmark mark='c'/>训练损失一直在下降，但留出的书页在第4轮之后最好，判对83.2%。<bookmark mark='d'/>到第200轮，已经滑落到77.5%：每页只有两个数，多出来的细节拟合的是训练页，而不是作者。及早停下，本身就是这个方法的一部分。"

def function(tree,name):
    return next(n for n in ast.walk(tree)if isinstance(n,ast.FunctionDef)and n.name==name)


def compile_nodes(nodes,scope):
    module=ast.Module(body=copy.deepcopy(nodes),type_ignores=[])
    exec(compile(ast.fix_missing_locations(module),'actual GradientBoosting source AST','exec'),scope)
    return scope


def voice_api():
    tree=ast.parse((ROOT/'explainer/voiceover.py').read_text())
    tracker=next(n for n in tree.body if isinstance(n,ast.ClassDef)and n.name=='VoiceoverTracker')
    scope={'lang':lang,'_BOOKMARK':lang.BOOKMARK}
    return compile_nodes([function(tree,'_strip_bookmarks'),tracker],scope)


def current_english():
    plane=function(ast.parse(SOURCE.read_text()),'plane')
    voice=next(n for n in ast.walk(plane)if isinstance(n,ast.With))
    acc=np.zeros(200);acc[3]=.832;acc[-1]=.775
    scope={'best':4,'n':200,'acc':acc,'slips':True}
    end=next(n.value for n in plane.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='end'for t in n.targets))
    scope['end']=eval(compile(ast.Expression(copy.deepcopy(end)),'actual end phrase','eval'),scope)
    return eval(compile(ast.Expression(copy.deepcopy(voice.items[0].context_expr.args[0])),'actual plane narration','eval'),scope)


def translated(language):
    english=current_english()
    if language=='en':return english
    translator.cache_clear();lang._table.cache_clear()
    with mock.patch.object(lang,'LANG','zh'):
        return lang.translate(english,ROOT/'videos/ai/ai6','GradientBoosting')


class Tracker:
    def __init__(self):self.value=1
    def get_value(self):return self.value
    def set_value(self,value):self.value=value;return self
    @property
    def animate(self):return SimpleNamespace(set_value=lambda value:('counter-animation',value))


class Readout:
    def __init__(self,name,counter):self.name=name;self.counter=counter;self.value=1;self.updates=[]
    def update(self,dt):self.value=self.counter.get_value();self.updates.append(dt);return self


class Clock:
    def __init__(self,fps,counter,readouts,start):
        self.fps=fps;self.quantizer=installed_quantizer(fps);self.renderer=SimpleNamespace(time=start)
        self.counter=counter;self.readouts=readouts;self.regions=set();self.foreground=None;self.snapshots=[];self.plays=[]
    def advance(self,seconds):
        seconds=self.quantizer.validate_run_time(seconds,self.advance)
        self.renderer.time+=len(self.quantizer.get_time_progression(seconds,'source-only clock'))/self.fps
    def wait(self,seconds):self.advance(seconds)
    def add(self,*items):
        for item in items:
            if isinstance(item,str)and item.startswith('region-'):self.regions.add(item)
    def remove(self,*items):
        for item in items:self.regions.discard(item)
    def play(self,*animations,run_time=1.,**kwargs):
        start=self.renderer.time;self.advance(run_time)
        for kind,item in animations:
            if kind=='counter-animation':self.counter.set_value(item)
            elif kind=='FadeIn':self.add(item)
            elif kind=='FadeOut':self.remove(item)
        for item in self.readouts:item.update(0)
        self.plays.append({'start':start,'end':self.renderer.time,'requested':run_time,'round':self.counter.get_value()})
    def bring_to_front(self,dots):
        self.foreground=dots
        self.snapshots.append({'time':self.renderer.time,'round':self.counter.get_value(),'regions':set(self.regions),
                               'readouts':[m.value for m in self.readouts],'foreground':dots,
                               'updates':[len(m.updates)for m in self.readouts]})


def replay(language,fps,phase):
    tree=ast.parse(SOURCE.read_text());plane=function(tree,'plane');voice=next(n for n in ast.walk(plane)if isinstance(n,ast.With))
    # Start just after the existing a-wait; preceding geometry remains unchanged.
    first=next(i for i,n in enumerate(voice.body)if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)
               and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='play'
               and any(isinstance(a,ast.Call)and ast.unparse(a).startswith('FadeIn(imgs[1])')for a in n.value.args))
    counter=Tracker();readouts=[Readout(name,counter)for name in ('counter','training loss','held-out accuracy','mini-curve')]
    block=FROZEN_INPUTS[language]['block'];api=voice_api();raw=translated(language)
    with mock.patch.object(lang,'LANG',language):clean,marks=api['_strip_bookmarks'](raw)
    assert clean==block['text']
    words=[SimpleNamespace(text=w,start=start-block['start'],end=end-block['start'])for w,start,end in block['words']]
    initial=words[marks['a']].start+phase/fps
    clock=Clock(fps,counter,readouts,initial)
    vo=api['VoiceoverTracker'](clock,SimpleNamespace(duration=block['duration'],words=words),marks,0.)
    scope={'math':math,'config':SimpleNamespace(frame_rate=fps),'r':counter,'cnt':readouts[0],'tv':readouts[1],
           'av':readouts[2],'mc':readouts[3],'imgs':{k:f'region-{k}'for k in (1,3,10,30,100,200)},
           'reads':'reads','mini':'mini','dots':'training-dots','n':200,'linear':'linear',
           'FadeIn':lambda item:('FadeIn',item),'FadeOut':lambda item:('FadeOut',item)}
    compile_nodes([function(tree,'_run_time_before')],scope)
    method=ast.FunctionDef(name='run',args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='self'),ast.arg(arg='vo')],
        kwonlyargs=[],kw_defaults=[],defaults=[]),body=copy.deepcopy(voice.body[first:]),decorator_list=[])
    compile_nodes([method],scope);scope['run'](clock,vo)
    return clock,vo


class GradientBoostingCueTests(unittest.TestCase):
    def test_actual_bilingual_translator_strip_and_cache_key_preserve_spoken_words(self):
        api=voice_api()
        for language in ('en','zh'):
            with self.subTest(language=language),mock.patch.object(lang,'LANG',language),mock.patch.object(tts,'synthesize',side_effect=AssertionError('no TTS job'))as synth:
                current=translated(language);clean,marks=api['_strip_bookmarks'](current)
                oldraw = FROZEN_INPUTS[language]['block']['raw'] if language == 'en' else OLD_ZH_RAW
                oldclean,oldmarks=api['_strip_bookmarks'](oldraw)
                self.assertEqual(clean,oldclean);self.assertEqual(clean,FROZEN_INPUTS[language]['block']['text'])
                self.assertEqual(tts.cache_key(clean),tts.cache_key(oldclean));self.assertEqual(list(marks),['a','b','thirty','c','d'])
                self.assertEqual({k:marks[k]for k in ('a','b','c','d')},oldmarks)
                words=lang.tokens(clean,language);self.assertTrue(words[marks['thirty']].startswith('thirty'if language=='en'else'30'))
                if language=='zh':self.assertEqual(api['_strip_bookmarks'](lang.zh_numbers(Translator('ai6')(current_english())))[0],clean)
                synth.assert_not_called()

    def test_actual_source_replay_on_both_word_clocks_and_frame_phases(self):
        for language in ('en','zh'):
            for fps in (15,30,60):
                for phase in (0.,.49,1.):
                    with self.subTest(language=language,fps=fps,phase=phase):
                        clock,vo=replay(language,fps,phase);states={int(s['round']):s for s in clock.snapshots}
                        self.assertEqual(set(states),{1,10,30,100,200});self.assertNotIn(3,states)
                        self.assertLessEqual(states[10]['time'],vo.mark_time('b')-1/fps+1e-9)
                        self.assertGreaterEqual(states[30]['time'],vo.mark_time('thirty')-1/60-1e-9)
                        self.assertLessEqual(states[30]['time'],vo.mark_time('thirty')+1/fps+1e-9)
                        self.assertLessEqual(states[200]['time'],vo.mark_time('d')+1/fps+1e-9)
                        self.assertGreater(states[30]['time']-states[10]['time'],.35)
                        for value in (30,200):
                            self.assertEqual(states[value]['regions'],{f'region-{value}'})
                            self.assertEqual(states[value]['readouts'],[value]*4)
                            self.assertEqual(states[value]['foreground'],'training-dots')
                        # The unspoken100 tween keeps its original duration; named30/200 do not tween.
                        tweens={int(p['round']):p for p in clock.plays if p['round']!=1}
                        self.assertEqual(set(tweens),{10,100});self.assertEqual(tweens[100]['requested'],1.2)

    def test_budget_cap_and_impossible_deadline_have_honest_limits(self):
        scope={'math':math};compile_nodes([function(ast.parse(SOURCE.read_text()),'_run_time_before')],scope)
        budget=scope['_run_time_before']
        for fps in (15,30,60):
            vo=SimpleNamespace(mark_time=lambda mark:1.,elapsed=lambda:.8)
            self.assertLessEqual(budget(vo,'b',fps),.2-2/fps+1e-12)
            overdue=SimpleNamespace(mark_time=lambda mark:1.,elapsed=lambda:1.1)
            self.assertEqual(budget(overdue,'b',fps),0.)
            subframe=SimpleNamespace(mark_time=lambda mark:1.,elapsed=lambda:1.-.5/fps)
            self.assertEqual(budget(subframe,'b',fps),0.)
            # Zero requests a same-instant snapshot, not a claim that an already
            # missed cue or the next encoded frame can be recovered.
            self.assertGreater(overdue.elapsed(),overdue.mark_time('b'))
        for fps in (0.,-1.,float('nan')):
            with self.assertRaises(ValueError):budget(vo,'b',fps)


if __name__=='__main__':unittest.main()
