from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import AGENT, ENV, PART, PRIOR, REWARD, SEARCH, VALUE, node_box


class MuZero(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.unroll()
        self.results()

    def card(self):
        card = chapter_card(14, r"Planning with a learned model", r"Can you search a game whose rules you don't know?",
                            lit=(2019,), part=PART)
        with self.voiceover("Chapter fourteen. Planning with a learned model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        left = VGroup(label(r"AlphaZero's search", font_size=30, color=SEARCH),
                      label(r"needs the rules: \ ``if I play here, \\ the board becomes this''", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.25).move_to([-3.4, 1.2, 0])
        right = VGroup(label(r"most of the world", font_size=30, color=ENV),
                       label(r"no rulebook: \ a robot, \ a video game's pixels, \\ a data centre's cooling",
                             font_size=24, color=GREY_A)).arrange(DOWN, buff=0.25).move_to([3.4, 1.2, 0])
        q = label(r"learn a model of the world, \ and search inside it", font_size=30, color=AGENT).move_to(DOWN * 1.4)
        with self.voiceover(
            "AlphaZero searches by playing moves forward in its head, and for that it needs the rules: a perfect "
            "simulator that says what the board looks like after each move. <bookmark mark='a'/> Most problems have "
            "no rulebook. A robot, a video game seen as pixels, a cooling plant. <bookmark mark='b'/> So: learn a "
            "model of the world from experience, and search inside the model."
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(right))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unroll(self):
        obs = Square(1.0, stroke_color=ENV, stroke_width=2, fill_color="#20283A", fill_opacity=1).move_to([-6.0, 0.6, 0])
        ol = MathTex(r"o_t", font_size=30, color=ENV).next_to(obs, DOWN, buff=0.15)
        xs = [-3.9, -1.0, 1.9, 4.8]
        states = VGroup(*[Circle(radius=0.38, color=AGENT, stroke_width=3, fill_color=AGENT, fill_opacity=0.15)
                          .move_to([x, 0.6, 0]) for x in xs])
        sl = VGroup(*[MathTex(rf"s^{k}", font_size=30, color=AGENT).move_to(c) for k, c in enumerate(states)])
        h = Arrow(obs.get_right(), states[0].get_left(), buff=0.1, color=AGENT, stroke_width=3)
        hl = MathTex(r"h", font_size=30, color=AGENT).next_to(h, UP, buff=0.05)
        gs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=ENV, stroke_width=3)
                      for a, b in zip(states, states[1:])])
        gl = VGroup(*[MathTex(rf"g(\cdot, a_{k + 1})", font_size=26, color=ENV).next_to(a_, UP, buff=0.05)
                      for k, a_ in enumerate(gs)])
        rl = VGroup(*[MathTex(rf"r^{k + 1}", font_size=26, color=REWARD).next_to(a_, DOWN, buff=0.05)
                      for k, a_ in enumerate(gs)])
        fs = VGroup()
        for k, c in enumerate(states):
            out = MathTex(rf"\mathbf p^{k},\ v^{k}", font_size=26).move_to(c.get_center() + DOWN * 1.5)
            out[0][:2].set_color(PRIOR)
            fs.add(VGroup(Arrow(c.get_bottom(), out.get_top(), buff=0.08, color=VALUE, stroke_width=2.5), out))
        fl = MathTex(r"f", font_size=28, color=VALUE).next_to(fs[0][0], LEFT, buff=0.08)
        roles = VGroup(label(r"$h$: \ representation: \ observation $\to$ hidden state", font_size=22, color=AGENT),
                       label(r"$g$: \ dynamics: \ hidden state, action $\to$ reward, next hidden state", font_size=22,
                             color=ENV),
                       label(r"$f$: \ prediction: \ hidden state $\to$ policy and value \ (AlphaZero's network)",
                             font_size=22, color=VALUE)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        roles.to_edge(UP, buff=0.35)
        train = label(r"trained so that, unrolled along real games, \ $r^k$, $v^k$, $\mathbf p^k$ match the real "
                      r"rewards, returns and search policies", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.75)
        ve = label(r"value-equivalent: \ $s^k$ never has to look like the world, \ only to predict what matters for "
                   r"planning", font_size=22, color=C.BITS).to_edge(DOWN, buff=0.75)
        cite_ = cite(r"J.~Schrittwieser et al., \textit{Mastering Atari, Go, chess and shogi by planning with a learned "
                     r"model}, \textit{Nature} (2020)", corner=DR)
        with self.voiceover(
            "MuZero, from DeepMind in 2019, does exactly that with three learned functions. <bookmark mark='a'/> A "
            "representation function h turns the current observation into a hidden state. <bookmark mark='b'/> A "
            "dynamics function g takes a hidden state and an action, and predicts the reward and the next hidden "
            "state: an imagined step. <bookmark mark='c'/> And a prediction function f, AlphaZero's network, gives a "
            "policy and a value for any hidden state. The tree search runs entirely on hidden states. "
            "<bookmark mark='d'/> They are trained together: unroll the model five steps along real trajectories and "
            "make its predicted rewards, values and policies match the real rewards, the returns, and the search's "
            "choices. <bookmark mark='e'/> The crucial choice: the hidden state is never asked to reconstruct the "
            "screen or the board. It only has to predict what matters for planning. A model of the world that "
            "knows only what's useful."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(obs), FadeIn(ol), GrowArrow(h), FadeIn(hl), FadeIn(states[0]), FadeIn(sl[0]), FadeIn(roles[0]))
            vo.wait_until("b")
            self.play(FadeIn(roles[1]), LaggedStart(*[AnimationGroup(GrowArrow(gs[k]), FadeIn(gl[k]), FadeIn(rl[k]),
                                                                     FadeIn(states[k + 1]), FadeIn(sl[k + 1]))
                                                      for k in range(3)], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(roles[2]), FadeIn(fl), LaggedStart(*[FadeIn(f_) for f_ in fs], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(train))
            vo.wait_until("e")
            self.play(FadeOut(train, shift=UP * 0.2), FadeIn(ve, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        cards = VGroup(
            history_card(2019, r"MuZero", r"matches AlphaZero at Go, chess and shogi without being told the rules; "
                         r"\ a new state of the art on $57$ Atari games", width=6.2, color=AGENT),
            history_card(2021, r"EfficientZero", r"above the median human on Atari after the equivalent of two hours "
                         r"of play", width=6.2, color=REWARD),
            history_card(2022, r"Gumbel MuZero", r"guaranteed policy improvement even with a handful of simulations",
                         width=6.2, color=SEARCH),
            history_card(2022, r"MuZero in production", r"choosing how to compress YouTube videos: \ about $4\%$ fewer "
                         r"bits at the same quality", width=6.2, color=ENV),
        ).arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(UP * 0.2)
        cite_ = cite(r"Ye et al.\ (2021); \ Danihelka et al.\ (2022); \ Mandhane et al.\ (2022)")
        nxt = label(r"learned models of the world return in Part 29", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "MuZero matched AlphaZero at Go, chess and shogi without ever being given the rules, and set a new state "
            "of the art on the Atari games. <bookmark mark='a'/> EfficientZero made it frugal: above the median human "
            "on Atari after the equivalent of two hours of play. <bookmark mark='b'/> Gumbel MuZero made search "
            "provably improve the policy even with a handful of simulations. <bookmark mark='c'/> And a version went "
            "to work compressing YouTube videos, saving about four percent of the bits. <bookmark mark='d'/> Models "
            "that learn how the world works, and plan inside it, come back in Part 29."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.15), FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()
