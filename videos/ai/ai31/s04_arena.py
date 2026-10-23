from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import ARENA_COLORS, CI, EST, JUDGE, PART, TRUTH, interval_bar, load, node_box, tagline


class Arena(VoiceoverScene):
    def construct(self):
        self.card()
        self.votes()
        self.derive()
        self.converge()
        self.elo_vs_bt()
        self.illusion()

    def card(self):
        card = chapter_card(3, r"Arenas and ratings", r"Can a crowd's votes rank models?", lit=(2023,), part=PART)
        with self.voiceover("Chapter three. Arenas and ratings."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def votes(self):
        prompt = node_box(r"a prompt, \ typed by anyone", GREY_B, font_size=26).move_to([0, 2.6, 0])
        a = RoundedRectangle(width=4.6, height=2.0, corner_radius=0.15, stroke_color=ARENA_COLORS[1], stroke_width=2.5,
                             fill_color=ARENA_COLORS[1], fill_opacity=0.06).move_to([-2.9, 0.4, 0])
        b = RoundedRectangle(width=4.6, height=2.0, corner_radius=0.15, stroke_color=ARENA_COLORS[5], stroke_width=2.5,
                             fill_color=ARENA_COLORS[5], fill_opacity=0.06).move_to([2.9, 0.4, 0])
        la = label(r"model A \ (name hidden)", font_size=24, color=ARENA_COLORS[1]).move_to(a)
        lb = label(r"model B \ (name hidden)", font_size=24, color=ARENA_COLORS[5]).move_to(b)
        vote = label(r"which answer is better?", font_size=30, color=JUDGE).move_to([0, -1.2, 0])
        arrows = VGroup(Arrow(prompt.get_bottom(), a.get_top(), buff=0.1, color=GREY_B, stroke_width=2.5),
                        Arrow(prompt.get_bottom(), b.get_top(), buff=0.1, color=GREY_B, stroke_width=2.5))
        tick = label(r"$\checkmark$", font_size=60, color=JUDGE).next_to(b, RIGHT, buff=0.2)
        hc = history_card(2023, r"Chatbot Arena \ (LMSYS; \ now LMArena)", r"anonymous pairwise votes from the public; "
                          r"\ over $240{,}000$ votes by early 2024 \ (Chiang et al.); \ since then, millions",
                          width=8.6, color=JUDGE, font_size=20).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Some things can't be graded by an answer key: is this explanation clear, is this story good? In the spring of 2023 "
            "a group at Berkeley, LMSYS, opened Chatbot Arena. <bookmark mark='a'/> Anyone can type a prompt; two "
            "anonymous models answer; <bookmark mark='b'/> the person votes for the better answer, and only then "
            "learns which models they were. <bookmark mark='c'/> By early 2024 it had over two hundred and forty "
            "thousand votes; it is now run as LMArena. How do you turn votes into a ranking?"
        ) as vo:
            self.play(FadeIn(prompt), GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(a), FadeIn(b), FadeIn(la),
                      FadeIn(lb))
            vo.wait_until("a")
            self.play(Indicate(prompt, color=WHITE), Indicate(VGroup(a, b), color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(vote), FadeIn(tick, scale=1.4))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"P(i \text{ beats } j)", r"=", r"\sigma(\theta_i - \theta_j)", font_size=36),
            cmath(r"\ell(\theta)", r"=", r"\sum_{\text{votes}} \log \sigma(\theta_{\text{winner}} - "
                  r"\theta_{\text{loser}})", font_size=36),
            cmath(r"\frac{\partial \ell}{\partial \theta_i}", r"=", r"\sum_{\text{votes with } i}"
                  r"\big(S_i - \sigma(\theta_i - \theta_j)\big)", font_size=36),
            cmath(r"\theta_i", r"\leftarrow", r"\theta_i + K\,\big(S_i - E_i\big)", font_size=36),
            cmath(r"\text{Elo}", r"=", r"1000 + \tfrac{400}{\ln 10}\,\theta", font_size=36),
        ]
        rows[2][2].set_color(EST)
        rows[3][2].set_color(JUDGE)
        whys = [why(r"Bradley--Terry \ (1952): \ Part 27's reward model"),
                why(r"maximum likelihood: \ the log of each vote's probability"),
                why(r"$\sigma' = \sigma(1-\sigma)$; \ $S_i = 1$ for a win: \ actual minus expected"),
                why(r"Elo's update: \ one gradient step per game, \ step size $K$"),
                why(r"$400$ points $=$ odds of $10$ to $1$")]
        step = ladder(self, rows, whys, keep=5, top=3.0, x=-1.0, buff=0.42, edge=6.9)
        with self.voiceover(
            "With the model of Part 27's reward models. <bookmark mark='a'/> Give each model a strength theta; the "
            "chance that one beats another is the sigmoid of their difference: the Bradley-Terry model, from 1952. "
            "<bookmark mark='b'/> Choose the strengths that make the observed votes most likely: the log-likelihood is "
            "a sum over votes of the log of the winner's probability. <bookmark mark='c'/> Its gradient, for one "
            "model, is a sum over its games of what happened minus what was expected. <bookmark mark='d'/> Take one "
            "small step along that gradient after every game, and you have Arpad Elo's chess rating update. "
            "<bookmark mark='e'/> The Arena reports strengths on Elo's scale, where four hundred points mean odds of "
            "ten to one."
        ) as vo:
            for k, m in enumerate("abcde"):
                if k:  # the first line comes with the first words
                    vo.wait_until(m)
                step(k)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def converge(self):
        d = load("arena")
        cps = list(d["checkpoints"])
        est, lo, hi = np.asarray(d["est"]), np.asarray(d["lo"]), np.asarray(d["hi"])
        true = np.asarray(d["true"], float)
        names = d["names"]
        M = len(true)
        x0, x1 = 850, 1400
        g = axes([x0, x1], [0, M + 0.5], x_length=8.4, y_length=5.6, xlabel=r"rating \ (Elo scale)",
                 xticks=[900, 1000, 1100, 1200, 1300], center=[0.6, -0.3, 0])
        order = np.argsort(true)
        ypos = {int(m): k + 0.8 for k, m in enumerate(order)}
        truths = VGroup(*[Line(g.ax.c2p(true[m], ypos[m] - 0.32), g.ax.c2p(true[m], ypos[m] + 0.32), color=TRUTH,
                               stroke_width=4) for m in range(M)])
        names_m = VGroup(*[label(rf"model {names[m]}", font_size=22, color=ARENA_COLORS[m])
                           .next_to(g.ax.c2p(x0, ypos[m]), LEFT, buff=0.2) for m in range(M)])

        def bars(k):
            return VGroup(*[interval_bar(g.ax, ypos[m], max(lo[k, m], x0), min(hi[k, m], x1), ARENA_COLORS[m], est[k, m],
                                         stroke_width=6) for m in range(M)])

        cur = bars(0)
        votes = [label(rf"${n:,}$ votes".replace(",", "{,}"), font_size=30, color=WHITE).to_corner(UR, buff=0.4)
                 for n in cps]
        okt = [label(rf"rank order right: \ ${o}$ of ${M}$", font_size=22, color=GREY_A).next_to(votes[k], DOWN,
                                                                                                 buff=0.12)
               .align_to(votes[k], RIGHT) for k, o in enumerate(d["order_ok"])]
        lg = legend([(TRUTH, r"true strength \ (simulated)"), (WHITE, r"estimate, \ with its $95\%$ bootstrap interval")],
                    font_size=18).to_corner(DL, buff=0.25)
        tag = tagline(r"simulated: \ ten models, \ known strengths")
        w = np.asarray(d["width"])
        k1000 = cps.index(1000)
        k10k = cps.index(10_000)
        with self.voiceover(
            "Here is that fit at work on a simulated arena, so that we know the truth: ten models with strengths we "
            "chose, the white ticks, two pairs of them almost tied. <bookmark mark='a'/> After a hundred votes the "
            f"intervals are {w[0]:.0f} points wide on average and the ranking is mostly wrong. "
            f"<bookmark mark='b'/> As votes accumulate the intervals shrink: {w[k1000]:.0f} points at a thousand votes, "
            f"{w[k10k]:.0f} at ten thousand, {w[-1]:.0f} at {cps[-1]:,}, narrowing like one over the square root of the "
            "number of votes. <bookmark mark='c'/> The near-ties never separate: models four points apart would need "
            "millions of votes. An honest leaderboard shows them as tied."
        ) as vo:
            self.play(FadeIn(g), FadeIn(truths), FadeIn(names_m), FadeIn(lg), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cur), FadeIn(votes[0]), FadeIn(okt[0]))
            vo.wait_until("b")
            for k in range(1, len(cps)):
                nxt = bars(k)
                self.play(ReplacementTransform(cur, nxt), ReplacementTransform(votes[k - 1], votes[k]),
                          ReplacementTransform(okt[k - 1], okt[k]), run_time=1.0)
                cur = nxt
            vo.wait_until("c")
            ties = [m for m in range(M) if any(abs(true[m] - true[o]) < 6 for o in range(M) if o != m)]
            self.play(*[Indicate(cur[m], color=WHITE, scale_factor=1.05) for m in ties])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def elo_vs_bt(self):
        d = load("arena")
        path = np.asarray(d["elo_path"])  # every 100 votes, 10 models
        bt = np.asarray(d["bt10"])
        true = np.asarray(d["true"], float)
        M = len(true)
        n = path.shape[0]
        y0 = float(np.floor(min(path.min(), bt.min()) / 100) * 100)
        y1 = float(np.ceil(max(path.max(), bt.max()) / 100) * 100)
        g = axes([0, n * 100], [y0, y1], x_length=8.0, y_length=4.6, xlabel=r"votes, \ in the order they arrived",
                 ylabel=r"online Elo rating, \ $K = 32$", xticks=[0, 5000, 10000],
                 yticks=list(range(int(y0) + 100, int(y1), 200)),
                 center=[-1.2, -0.4, 0])
        lines = VGroup(*[VMobject().set_points_as_corners([g.ax.c2p(100 * (k + 1), path[k, m]) for k in range(n)])
                         .set_stroke(ARENA_COLORS[m], 2.5) for m in range(M)])
        ticks = VGroup(*[Line(g.ax.c2p(n * 100, bt[m]) + RIGHT * 0.05, g.ax.c2p(n * 100, bt[m]) + RIGHT * 0.35,
                              color=ARENA_COLORS[m], stroke_width=5) for m in range(M)])
        tl = label(r"Bradley--Terry, \\ all $10{,}000$ at once", font_size=20, color=GREY_A).next_to(ticks, RIGHT,
                                                                                                  buff=0.15)
        sd = d["elo_perm_sd"]
        sdl = label(rf"the same votes in $20$ other orders: \ final online ratings vary by ${sd:.0f}$ points "
                    r"(standard deviation)", font_size=22, color=JUDGE).to_edge(DOWN, buff=0.3)
        hc = note(r"LMSYS, \textit{Chatbot Arena: New models \& Elo system update} (December 2023); \ Arena-Rank "
                  r"(December 2025): \ closed-form intervals", font_size=18).to_corner(UL, buff=0.25)
        tag = tagline(r"simulated")
        with self.voiceover(
            "The Arena began with the online version, Elo's update after every vote. <bookmark mark='a'/> On ten "
            "thousand simulated votes, the ratings never settle: each chases its latest games. <bookmark mark='b'/> "
            f"And they depend on the order: shuffle the votes twenty times, and the final ratings differ by {sd:.0f} "
            "points. <bookmark mark='c'/> Bradley-Terry, fitted to all the votes at once, is the same for any order; "
            "the Arena switched to it in December 2023, and later to intervals computed in closed form."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(hc))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.05), run_time=3.0)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(sdl, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(t, LEFT) for t in ticks], lag_ratio=0.05), FadeIn(tl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def illusion(self):
        d = load("arena")
        ks, infl = list(d["ks"]), np.asarray(d["inflation"])
        g = axes([0, len(ks)], [0, float(np.ceil(infl.max() / 5) * 5 + 2)], x_length=5.6, y_length=3.4,
                 ylabel=r"published rating minus the truth \ (Elo)", yticks=[0, 5, 10, 15], center=[3.3, -0.6, 0])
        bars = VGroup()
        labs = VGroup()
        for k, (kk, v) in enumerate(zip(ks, infl)):
            p0, p1 = g.ax.c2p(k + 0.2, 0), g.ax.c2p(k + 0.8, max(v, 0.05))
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=C.PENALTY,
                               fill_opacity=0.85).move_to((p0 + p1) / 2))
            labs.add(MathTex(rf"{kk}", font_size=24, color=GREY_A).next_to(g.ax.c2p(k + 0.5, 0), DOWN, buff=0.12))
        xl = label(r"private variants tested, \ best one published", font_size=20, color=GREY_A).next_to(labs, DOWN,
                                                                                                       buff=0.15)
        vals = VGroup(*[MathTex("0.0" if abs(v) < 0.05 else f"{v:+.1f}", font_size=20, color=C.PENALTY)
                        .next_to(b, UP, buff=0.05) for b, v in zip(bars, infl)])
        cards = VGroup(
            history_card(2024, r"style control \ (LMArena)", r"length and markdown sway votes; \ a regression on them "
                         r"changes the ranking: \ length was the dominant style factor", width=5.6, color=JUDGE,
                         font_size=20),
            history_card(2025, r"\textit{The Leaderboard Illusion} \ (Singh et al.)", r"some providers tested many "
                         r"private variants and published the best: \ $27$ for Meta before Llama 4; \ Google and "
                         r"OpenAI had about $20\%$ of all the data each", width=5.6, color=C.PENALTY, font_size=20),
        ).arrange(DOWN, buff=0.3).move_to([-3.6, -0.5, 0])
        tag = tagline(rf"simulated: \ ${d['variant_votes']:,}$ votes per variant".replace(",", "{,}"))
        head = label(r"What sways a leaderboard", font_size=36).to_edge(UP, buff=0.4)

        def answer(n_lines, headings, color):
            box = RoundedRectangle(width=2.3, height=2.7, corner_radius=0.12, stroke_color=color, stroke_width=2,
                                   fill_color=color, fill_opacity=0.08)
            rows = VGroup()
            for k in range(n_lines):
                if k in headings:
                    rows.add(Line(LEFT, RIGHT, color=color, stroke_width=6).set_length(1.1))
                else:
                    rows.add(VGroup(Dot(radius=0.035, color=GREY_B), Line(LEFT, RIGHT, color=GREY_B, stroke_width=3)
                                    .set_length(1.4)).arrange(RIGHT, buff=0.1))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(box).align_to(box, UP).shift(DOWN * 0.25)
            return VGroup(box, rows)

        short = answer(2, (), GREY_B)
        long_ = answer(9, (0, 5), C.MODEL_Q)
        styl = VGroup(short, long_).arrange(RIGHT, buff=0.6).move_to([3.4, 0.3, 0])
        sl = label(r"short and plain", font_size=20, color=GREY_A).next_to(short, DOWN, buff=0.15)
        ll = label(r"long, \ with headings and lists", font_size=20, color=GREY_A).next_to(long_, DOWN, buff=0.15)
        vt = label(r"$\checkmark$", font_size=54, color=JUDGE).next_to(long_, UP, buff=0.1)
        sch = note(r"schematic").next_to(VGroup(sl, ll), DOWN, buff=0.2)
        style_vis = VGroup(styl, sl, ll, vt, sch)
        with self.voiceover(
            "Two things can still go wrong. <bookmark mark='a'/> The voters are people, and people like long answers "
            "with headings and lists. In 2024 the Arena added style control, a regression that separates a model's "
            "strength from the length and formatting of its answers, and the ranking changed. "
            "<bookmark mark='b'/> And the leaderboard can be gamed by selection. In 2025, researchers at Cohere "
            "reported that some providers tested many private variants and published only the best; Meta tested "
            "twenty-seven before releasing Llama 4. <bookmark mark='c'/> Simulate it: variants that are all equally "
            f"good, each rated from {d['variant_votes']:,} votes. Publish the best of two, and it overstates the truth "
            f"by {infl[1]:.0f} points; the best of {ks[-1]}, by {infl[-1]:.0f}. Nothing improved but the luck of the "
            "draw."
        ) as vo:
            self.play(FadeIn(head), FadeIn(styl), FadeIn(sl), FadeIn(ll), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.15), FadeIn(vt, scale=1.4))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeOut(style_vis), FadeIn(g), FadeIn(labs), FadeIn(xl), FadeIn(tag))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(vals), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()
