from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ43.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ markups and elasticities", r"What do the numbers say?",
             "Chapter thirteen. The Dials: markups and elasticities.",
             lit={2020: r"De Loecker, \ Eeckhout and Unger"}, scale=("firm", "nation"), horizon=("a decade",))
        self.dial_markups()
        self.dial_products()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}"):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=0.55, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip(marks, rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def dial_markups(self):
        R = load("cereal")
        D = load("dlw")
        self._show(dials.DIALS["markups"], r"markups over marginal cost \ (updated)", 1.0, 2.0,
                   [1.0, 1.2, 1.4, 1.6, 1.8, 2.0], r"price over marginal cost",
                   "The first dial picks up a promise from Part ten: how far prices sit above marginal cost. De "
                   "Loecker, Eeckhout and Unger's average for American public firms in 1980: 1.21. "
                   "<bookmark mark='a'/> In 2016: 1.61. <bookmark mark='b'/> The Island's cereal aisle, with twelve "
                   f"brands and four firms competing: {R['markup_med']:.2f} for the median brand, a reminder that "
                   "differentiated products carry large markups without any collusion. <bookmark mark='c'/> The "
                   "Island's plants, by De Loecker and Warzynski's formula with a well-estimated elasticity: "
                   f"{D['median']['acf']:.2f}, as planted. <bookmark mark='z'/> The status: contested. That markups "
                   "differ widely is not in doubt; how much the typical one has risen is.", "abc")

    def dial_products(self):
        C = load("cars")
        B = load("blpdata")
        R = load("cereal")
        self._show(dials.DIALS["product_elasticity"], r"own-price elasticity of one product \ (new)", -5.0, 0.0,
                   [-5, -4, -3, -2, -1, 0], r"percent change in a product's sales per 1\% rise in its price",
                   "The second, new: the own-price elasticity of demand for one differentiated product. Plain logit "
                   "on Berry, Levinsohn and Pakes's cars by ordinary least squares: "
                   f"{say_num(B['ols']['el_med'])} for the median model, impossible for a firm that sets its price. "
                   f"<bookmark mark='a'/> The same by IV: {say_num(B['iv']['el_med'])}. <bookmark mark='b'/> Their "
                   f"random-coefficient estimator on forty Islands: {say_num(C['mean']['el_blp'])}, against a planted "
                   f"{say_num(C['mean']['el_true'])}. <bookmark mark='c'/> The Island's cereal aisle: "
                   f"{say_num(R['own_el_med'])}. <bookmark mark='z'/> The status: depends on the setting, and on "
                   "the method, which is the lesson of this part: estimates of one brand's demand "
                   "that come out inelastic signal a biased method, not a careless firm.", "abc")
