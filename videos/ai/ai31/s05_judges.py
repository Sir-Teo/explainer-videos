from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import ARENA_COLORS, CI, EST, JUDGE, PART, TRUTH, load, tagline


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Judges(VoiceoverScene):
    def construct(self):
        self.card()
        self.zheng()
        self.biased()
        self.corrected()
        self.irt()
        self.few_items()

    def card(self):
        card = chapter_card(4, r"Judges, and what an item tells you", r"Can a model grade other models fairly?",
                            lit=(2023, 2024), part=PART)
        with self.voiceover("Chapter four. Judges, and what an item tells you."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def zheng(self):
        head = label(r"A model as the judge \ (Zheng et al., 2023)", font_size=36).to_edge(UP, buff=0.4)
        agree = history_card(2023, r"agreement", r"GPT-4's verdicts matched human experts' over $80\%$ of the time: "
                             r"\ as often as experts matched each other", width=6.3, color=CI, font_size=20)
        pos = history_card(2023, r"position", r"the same two answers, \ both orders: \ GPT-4 consistent $65\%$ of the "
                           r"time, \ favouring the first answer in $30\%$; \ Claude-v1 consistent $24\%$", width=6.3,
                           color=JUDGE, font_size=20)
        verb = history_card(2023, r"verbosity", r"a list padded with a rephrased copy of itself: \ judged better "
                            r"$91\%$ of the time by GPT-3.5 and Claude-v1, \ $9\%$ by GPT-4", width=6.3, color=EST,
                            font_size=20)
        selfp = history_card(2023, r"self-preference", r"GPT-4 rated its own answers' win rate about $10$ points "
                             r"higher than people did, \ Claude-v1 $25$; \ the authors call the evidence inconclusive",
                             width=6.3, color=C.PENALTY, font_size=20)
        grid = VGroup(agree, pos, verb, selfp).arrange_in_grid(rows=2, cols=2, buff=0.3).next_to(head, DOWN, buff=0.4)
        cite_ = cite(r"Zheng et al., \textit{Judging LLM-as-a-judge with MT-Bench and Chatbot Arena} (2023)")
        with self.voiceover(
            "Votes from people are slow and expensive, so the field often asks a strong model to judge instead. "
            "<bookmark mark='a'/> In 2023 the team behind the Arena measured how well that works. GPT-4's verdicts "
            "agreed with human experts over eighty percent of the time, as often as the experts agreed with each "
            "other. But they found biases. <bookmark mark='b'/> Position: shown the same two answers in both orders, "
            "GPT-4 gave the same verdict only sixty-five percent of the time, and when it didn't, it mostly favored "
            "whichever came first. <bookmark mark='c'/> Length: padding an answer's list with a reworded copy of itself fooled two of the "
            "three judges ninety-one percent of the time. <bookmark mark='d'/> And self-preference: GPT-4 seemed to "
            "favor its own answers, though the authors judged the evidence inconclusive."
        ) as vo:
            full = [c_.copy() for c_ in (agree, pos, verb, selfp)]
            for card_ in (agree, pos, verb, selfp):
                card_.fade(0.78)
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(grid))
            for card_, f_, m in zip((agree, pos, verb, selfp), full, "abcd"):
                vo.wait_until(m)
                self.play(Transform(card_, f_))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def slope(self, left, right, ltitle, rtitle, names, y0=-3.0, y1=2.4, lo=940, hi=1320):
        """Two columns of ratings joined by lines: where each model lands under two judges."""
        Y = lambda v: y0 + (v - lo) / (hi - lo) * (y1 - y0)  # noqa: E731
        xl, xr = -2.2, 2.2

        def spread(ys, gap=0.24):
            """Label heights near ys, at least ``gap`` apart, in the same order."""
            order = np.argsort(ys)
            out = np.array(ys, float)
            for i in range(1, len(order)):
                out[order[i]] = max(out[order[i]], out[order[i - 1]] + gap)
            shift = (np.mean(ys) - np.mean(out))  # keep them centred on the data
            return out + shift

        ya, yb = spread([Y(a) for a in left]), spread([Y(b) for b in right])
        lcol, rcol = VGroup(), VGroup()
        for m, (a, b) in enumerate(zip(left, right)):
            col = ARENA_COLORS[m]
            lcol.add(Dot([xl, Y(a), 0], radius=0.07, color=col),
                     label(rf"{names[m]}", font_size=22, color=col).move_to([xl - 0.3, ya[m], 0]))
            rcol.add(Line([xl, Y(a), 0], [xr, Y(b), 0], color=col, stroke_width=3),
                     Dot([xr, Y(b), 0], radius=0.07, color=col),
                     MathTex(f"{b:.0f}", font_size=20, color=col).move_to([xr + 0.45, yb[m], 0]))
        t1 = label(ltitle, font_size=24, color=TRUTH).move_to([xl, y1 + 0.6, 0])
        t2 = label(rtitle, font_size=24, color=JUDGE).move_to([xr, y1 + 0.6, 0])
        return VGroup(VGroup(lcol, rcol), t1, t2)

    def biased(self):
        d = load("judge")
        names = d["names"]
        fair, bias = np.asarray(d["fair"]), np.asarray(d["biased"])
        length = np.asarray(d["length"])
        sib = np.asarray(d["sibling"]).astype(bool)
        sl = self.slope(fair, bias, r"an unbiased judge", r"the biased judge", names).shift(LEFT * 2.2)
        legend_rows = VGroup(
            label(rf"prefers the first answer: \ it wins ${d['first_wins'] * 100:.0f}\%$ of verdicts", font_size=20,
                  color=GREY_A),
            label(r"prefers longer answers: \ C and A write the longest", font_size=20, color=GREY_A),
            label(r"prefers its own family: \ F and J", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.3, 0.9, 0])
        gain = bias - fair
        up = int(np.argmax(gain))
        down = int(np.argmin(gain))
        tag = tagline(rf"simulated: \ ${d['n']:,}$ verdicts, \ biases set by hand".replace(",", "{,}"))
        r_f, r_b = np.asarray(d["fair_rank"]), np.asarray(d["biased_rank"])
        moved = int((r_f != r_b).sum())
        sib_names = " and ".join(n for n, s in zip(names, sib) if s)
        if sib[up]:
            why_up = "one of its own family"
        elif length[up] > 0.3:
            why_up = "a long-winded writer"
        else:
            why_up = "helped by others falling"
        why_down = "which writes short answers" if length[down] < -0.3 else "outshone by the favoured"
        n_up, n_down = names[up], names[down]
        g_up, g_down = gain[up], -gain[down]
        with self.voiceover(
            "How far can a biased judge move a leaderboard? Simulate it with the ten models of the arena. "
            "<bookmark mark='a'/> Give the judge three habits: it leans toward whichever answer it reads first, "
            f"toward longer answers, and toward models of its own family, here {sib_names}. "
            f"<bookmark mark='b'/> Rated by this judge, {moved} of the ten models change places. Model {n_up}, "
            f"{why_up}, climbs {g_up:.0f} points; model {n_down}, {why_down}, falls {g_down:.0f}."
        ) as vo:
            self.play(FadeIn(sl[1]), FadeIn(sl[2]), FadeIn(tag), FadeIn(sl[0][0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in legend_rows], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(sl[0][1]), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def corrected(self):
        d = load("judge")
        names = d["names"]
        fair = np.asarray(d["fair"])
        sw, ct = np.asarray(d["swapped"]), np.asarray(d["controlled"])
        sib = np.asarray(d["sibling"]).astype(bool)
        sl1 = self.slope(fair, sw, r"an unbiased judge", r"both orders", names).shift(LEFT * 2.2)
        sl2 = self.slope(fair, ct, r"an unbiased judge", r"length controlled", names).shift(LEFT * 2.2)
        err = lambda r: float(np.abs(r - fair).mean())  # noqa: E731
        e_b, e_s, e_c = err(np.asarray(d["biased"])), err(sw), err(ct)
        sib_gain = float((ct - fair)[sib].mean())
        rows = VGroup(
            label(rf"both orders, \ a split verdict a tie: \ consistent ${d['consistency'] * 100:.0f}\%$", font_size=20,
                  color=GREY_A),
            label(rf"mean error: \ biased ${e_b:.0f}$, \ both orders ${e_s:.0f}$", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, 1.5, 0])
        rows2 = VGroup(
            label(r"Bradley--Terry with the length gap \\ as a covariate \ (``style control'')", font_size=20,
                  color=GREY_A),
            label(rf"mean error: \ ${e_c:.0f}$", font_size=20, color=GREY_A),
            label(rf"the judge's own family: \ still $+{sib_gain:.0f}$", font_size=22, color=C.PENALTY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, -0.6, 0])
        tag = tagline(r"simulated")
        swap_help = e_s < e_b - 2
        cons = d["consistency"] * 100
        if swap_help:
            swap_said = "Swapping removes the tilt toward the first answer, and the ratings move back, a little."
        else:
            swap_said = ("Swapping removes the tilt toward the first answer, but here that tilt was mostly noise: "
                         "with the order random, it pushes every model equally. The damage is elsewhere.")
        with self.voiceover(
            "Two repairs. First, show each pair in both orders and call a split verdict a tie. <bookmark mark='a'/> "
            f"This judge agrees with itself only {cons:.0f} percent of the time. {swap_said} "
            "<bookmark mark='b'/> Second, fit Bradley-Terry with the difference in length as an extra "
            "variable, the Arena's style control. Long answers stop paying, and the ratings fall back into line, "
            f"to within {e_c:.0f} points on average. <bookmark mark='c'/> Except for the judge's own family: they "
            f"are still {sib_gain:.0f} points too high. No rearrangement of the votes removes a judge's taste for "
            "itself. Use a judge from another family, or a panel of several."
        ) as vo:
            self.play(FadeIn(sl1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows))
            vo.wait_until("b")
            self.play(ReplacementTransform(sl1, sl2), FadeIn(rows2[0]), FadeIn(rows2[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows2[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def irt(self):
        d = load("irt")
        a, b = np.asarray(d["show_a"]), np.asarray(d["show_b"])
        g = axes([-3, 3], [0, 1], x_length=5.6, y_length=3.0, xlabel=r"ability $\theta$", ylabel=r"chance of a right "
                 r"answer", xticks=[-2, 0, 2], yticks=[0, 0.5, 1], center=[-3.5, 0.9, 0])
        th = np.linspace(-3, 3, 200)
        cols = [C.COUNTING, JUDGE, C.PENALTY]
        iccs = VGroup(*[curve(g.ax, th, sigmoid(a[k] * (th - b[k])), cols[k], 3.5) for k in range(3)])
        info = axes([-3, 3], [0, 1.2], x_length=5.6, y_length=1.8, xlabel=r"ability $\theta$",
                    ylabel=r"information", xticks=[-2, 0, 2], center=[-3.5, -2.4, 0])
        ic = VGroup(*[curve(info.ax, th, (a[k] ** 2 * sigmoid(a[k] * (th - b[k])) * (1 - sigmoid(a[k] * (th - b[k]))))
                            / max(a.max() ** 2 / 4, 1e-9), cols[k], 3) for k in range(3)])
        rows = [
            cmath(r"P(\text{right} \mid \theta)", r"=", r"\sigma\big(a\,(\theta - b)\big)", font_size=34),
            cmath(r"\frac{\partial}{\partial \theta} \log P(y \mid \theta)", r"=", r"a\,(y - p)", font_size=34),
            cmath(r"I(\theta)", r"=", r"\mathbb E\big[a^2 (y - p)^2\big] = a^2\, p\,(1 - p)", font_size=34),
        ]
        rows[2][2].set_color(CI)
        whys = [why(r"$b$: \ difficulty; \ $a$: \ discrimination"), why(r"$y \in \{0, 1\}$; \ $\sigma' = \sigma(1 - \sigma)$"),
                why(r"Fisher information: \ largest where $p = \tfrac12$, \ i.e.\ $\theta = b$")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=3.2, buff=0.7, edge=6.9)
        tag = tagline(r"three simulated items")
        with self.voiceover(
            "Judging aside, which questions are worth asking? Educational testing's answer, item response theory, "
            "models the questions as well as the test-takers. "
            "<bookmark mark='a'/> The chance that a test-taker of ability theta gets an item right is a sigmoid of a "
            "times theta minus b: b is the item's difficulty, a its discrimination, how sharply it separates the "
            "weak from the strong. <bookmark mark='b'/> How much does one answer tell you about theta? Differentiate "
            "the log-likelihood: a times y minus p. <bookmark mark='c'/> Its expected square, the Fisher "
            "information, is a squared times p times one minus p. An item is most informative about test-takers near "
            "its own difficulty: too easy or too hard, and its answer is a foregone conclusion."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            self.play(LaggedStart(*[Create(c_) for c_ in iccs], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(info), LaggedStart(*[Create(c_) for c_ in ic], lag_ratio=0.3), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def few_items(self):
        d = load("irt")
        ks = list(d["ks"])
        ep, ei = np.asarray(d["err_plain"]) * 100, np.asarray(d["err_irt"]) * 100
        ytop = float(np.ceil(ep.max() + 1))
        g = axes([0, len(ks) - 1], [0, ytop], x_length=5.6, y_length=3.4,
                 ylabel=r"error in the predicted score \ (points)", yticks=[0, 4, 8], center=[-3.3, -0.3, 0])
        xs = np.arange(len(ks))
        labs = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(g.ax.c2p(i, 0), DOWN, buff=0.12)
                        for i, k in enumerate(ks)])
        lp, li = curve(g.ax, xs, ep, GREY_B, 4), curve(g.ax, xs, ei, CI, 4)
        dp = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.06, color=GREY_B) for x, y in zip(xs, ep)])
        di = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.06, color=CI) for x, y in zip(xs, ei)])
        xl_ = label(r"items asked, \ of $2{,}000$", font_size=22, color=GREY_A).next_to(labs, DOWN, buff=0.18)
        lg = legend([(GREY_B, r"the share answered right"), (CI, r"item response theory")], font_size=20)
        lg.move_to(g.ax.c2p(len(ks) - 1, ytop), aligned_edge=UR)
        cards = VGroup(
            history_card(2024, r"tinyBenchmarks \ (Maia Polo et al.)", r"$100$ curated questions predicted accuracy on "
                         r"all $14{,}000$ of MMLU \ within $1.9\%$", width=5.6, color=CI, font_size=20),
            history_card(2025, r"the Epoch Capabilities Index \ (Ho et al.)", r"the same model stitches more than $50$ "
                         r"benchmarks onto one scale, \ so models stay comparable after a benchmark saturates",
                         width=5.6, color=EST, font_size=20),
        ).arrange(DOWN, buff=0.3).move_to([3.6, -0.2, 0])
        tag = tagline(rf"simulated: \ $2{{,}}000$ items, \ ${d['train_models']}$ models to fit them, \ "
                      rf"${d['test_models']}$ to test")
        k25 = ks.index(25)
        k100 = ks.index(100)
        gain_small = ep[k25] - ei[k25]
        gain_100 = ep[k100] - ei[k100]
        e25p, e25i, e100p, e100i = ep[k25], ei[k25], ep[k100], ei[k100]
        if gain_small > 0.5:
            verdict = (f"With twenty-five items, the plain share answered right is off by {e25p:.1f} points on average; "
                       f"the item-response estimate, by {e25i:.1f}.")
            if gain_100 < 0.5:
                then = (f"By a hundred items the two are nearly level, {e100p:.1f} and {e100i:.1f}: the gain is largest "
                        "when items are few.")
            else:
                then = f"At a hundred items, {e100p:.1f} against {e100i:.1f}."
        else:
            verdict = (f"Here the gain is small: with twenty-five items the two estimates are off by {e25p:.1f} and "
                       f"{e25i:.1f} points.")
            then = f"At a hundred items, {e100p:.1f} against {e100i:.1f}."
        with self.voiceover(
            "Fit the items once, on models already tested, and a new model can be measured with far fewer questions. "
            "<bookmark mark='a'/> On a simulated benchmark of two thousand items, predict each new model's full score "
            f"from a few random items. {verdict} <bookmark mark='m'/> {then} <bookmark mark='b'/> On real data, tinyBenchmarks predicted accuracy "
            "on all fourteen thousand questions of MMLU within two points from a hundred well-chosen ones. "
            "<bookmark mark='c'/> And Epoch AI uses the same model to stitch more than fifty benchmarks onto one "
            "scale, its Capabilities Index, so that models stay comparable after any one benchmark is saturated."
        ) as vo:
            full = cards.copy()
            cards.fade(0.82)  # the published results wait, dimmed, beside the simulation
            self.play(FadeIn(g), FadeIn(labs), FadeIn(xl_), FadeIn(tag), FadeIn(cards))
            self.play(Create(lp), FadeIn(dp), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(Create(li), FadeIn(di), FadeIn(lg[1]))
            vo.wait_until("b")
            self.play(Transform(cards[0], full[0]))
            vo.wait_until("c")
            self.play(Transform(cards[1], full[1]))
        self.wait(0.4)
        self.clear_scene()
