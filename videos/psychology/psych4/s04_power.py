from __future__ import annotations

import numpy as np

from videos.psychology.psych4.common import *  # noqa: F403


class Power(VoiceoverScene):
    def construct(self):
        self.card()
        self.curves()
        self.literature()
        self.truth_of_a_finding()
        self.ioannidis()

    def card(self):
        card = chapter_card(3, r"Power", r"If the effect is real, how often will a study find it?",
                            lit={1962: r"Cohen surveys a year of a journal"}, part=PART, scale=("group",),
                            marr=("what",))
        with self.voiceover(
            "Chapter three. Power."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def curves(self):
        d = load("power")
        c = d["cohen"]
        head = heading(r"Power: \ the chance of finding an effect that is really there")
        ns = np.asarray(d["ns"])
        A = axes([0, 400], [0, 1.0], x_length=7.2, y_length=4.0, xticks=[20, 100, 200, 300, 400],
                 yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], xlabel=r"people in each group", ylabel=r"power",
                 center=[-2.8, -0.4, 0])
        ax = A.ax
        lines = VGroup(*[curve(ax, ns, d[f"curve_{k}"], SIZE[k], stroke_width=4) for k in ("0.8", "0.5", "0.2")])
        target = DashedLine(ax.c2p(0, 0.8), ax.c2p(400, 0.8), color=GREY_B, stroke_width=2)
        target_l = label(r"the usual target: \ four chances in five", font_size=20, color=GREY_B)
        target_l.next_to(ax.c2p(400, 0.8), UL, buff=0.06)
        intro = VGroup(
            label(r"power", font_size=36, color=P.ACCENT),
            wrapped_label(r"the chance that a study reaches $p < .05$ when the effect is real", 4.8, 27, WHITE),
            label(r"it depends on", font_size=24, color=GREY_A),
            label(r"1. \ how big the effect is", font_size=28, color=WHITE),
            label(r"2. \ how many people were tested", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.3, 0.0, 0])
        leg = legend([(SIZE["0.8"], r"large effect, $d = 0.8$"), (SIZE["0.5"], r"medium, $d = 0.5$"),
                      (SIZE["0.2"], r"small, $d = 0.2$")], font_size=24).move_to([4.5, 2.0, 0])
        hc = history_card(1962, r"Jacob Cohen", rf"works out the power of every study in a year of one journal",
                          color=P.ARCHIVE, width=5.4, font_size=24).move_to([4.2, 0.35, 0])
        cohen = VGroup(
            label(rf"for a medium effect: \ {r2(c['power_medium'])}", font_size=36, color=SIZE["0.5"]),
            label(r"a coin toss, for a real effect of ordinary size", font_size=24, color=GREY_A),
            label(rf"{c['later_year']}, the same journal: \ {r2(c['later_power_medium'])}", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(hc, DOWN, buff=0.3).align_to(hc, LEFT)
        src = published_tag(archive.COHEN_1962.cite)
        with self.voiceover(
            "Suppose an effect is real. How likely is a study to find it, meaning to reach p below point oh five? "
            "<bookmark mark='i'/> That probability is called the power of the study, <bookmark mark='j'/> and it "
            "depends on two things: how big the effect is, and how many people you tested. <bookmark mark='a'/> For a large effect, twenty-five people in "
            "each group give you four chances in five, which is the usual target. <bookmark mark='b'/> For a "
            "medium effect you need sixty-three. <bookmark mark='c'/> For a small one, nearly four hundred in "
            "each group. <bookmark mark='d'/> In 1962 Jacob Cohen did something nobody had thought to do. He took "
            "a year of a leading journal and worked out the power of every study in it. <bookmark mark='e'/> For "
            f"an effect of medium size, the average was {c['power_medium']}. A real effect of ordinary size had "
            "about the chance of a coin toss of being detected. Cohen published this, and it has been cited ever "
            f"since. <bookmark mark='f'/> Twenty-four years later two researchers went "
            "back to the same journal. The power hadn't gone up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(target), FadeIn(target_l))
            vo.wait_until("i")
            self.play(FadeIn(intro[0]), FadeIn(intro[1]))
            vo.wait_until("j")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in intro[2:]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeOut(intro), Create(lines[0]), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(leg[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(hc, shift=UP * 0.15), FadeIn(src))
            vo.wait_until("e")
            self.play(FadeIn(cohen[0]), FadeIn(cohen[1]))
            vo.wait_until("f")
            self.play(FadeIn(cohen[2], shift=UP * 0.1))
        self.clear_scene()

    def literature(self):
        d = load("power")
        head = heading(rf"{fmt_int(d['studies'])} studies of one real effect, {d['n']} people a group")
        edges = np.asarray(d["edges"])
        top = float(np.max(d["hist_all"])) * 1.15
        A = axes([-0.8, 1.6], [0, top], x_length=8.4, y_length=3.7, xticks=[-0.8, -0.4, 0, 0.4, 0.8, 1.2, 1.6],
                 xlabel=r"effect a study reports ($d$)", center=[-2.2, -0.45, 0])
        ax = A.ax
        allb = hist(ax, edges, np.asarray(d["hist_all"]), DRAWER, 0.9)
        sigb = hist(ax, edges, np.asarray(d["hist_sig"]), SIG, 0.95)
        truth = DashedLine(ax.c2p(d["d_true"], 0), ax.c2p(d["d_true"], top), color=TRUTH, stroke_width=3)
        tl = label(rf"the truth: \ {d['d_true']}", font_size=24, color=TRUTH).next_to(truth, UP, buff=0.05)
        cut = DashedLine(ax.c2p(d["smallest_significant"], 0), ax.c2p(d["smallest_significant"], top * 0.8),
                         color=SIG, stroke_width=2)
        cl = label(rf"smallest effect that can reach $p < .05$: \ {r2(d['smallest_significant'])}", font_size=20,
                   color=SIG).next_to(cut, UP, buff=0.05).shift(RIGHT * 1.7)
        side = VGroup(
            label(rf"found in {pct(d['found'])} of the studies", font_size=30, color=SIG),
            wrapped_label(rf"three laboratories in four find nothing, and are tempted to conclude there is "
                          r"nothing", 4.4, 24, GREY_A),
            label(rf"the ones that find it report {r2(d['mean_significant'])}", font_size=28, color=BAD),
            wrapped_label(r"twice the truth: \ in a small study, only an overestimate can be significant", 4.4, 24,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.75, 0.3, 0])
        tag = note(r"simulated: the false-positive lab").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here's what low power does to a literature, and it does two things, not one. Take a real effect of "
            f"moderate size, d of {d['d_true']}, <bookmark mark='s'/> and let two thousand laboratories each study it with "
            f"{d['n']} people a group, which for a long time was a common sample. <bookmark mark='a'/> "
            "Their estimates scatter widely round the truth, as they must. <bookmark mark='b'/> Only "
            f"{100 * d['found']:.0f} per cent of them reach significance. So the first cost is the obvious one: "
            "three laboratories in four miss an effect that's really there. <bookmark mark='c'/> The second cost "
            "is the one people don't expect. Look at which studies were significant. With twenty people a group, "
            f"a result can't reach p below point oh five unless it's at least {d['smallest_significant']:.2f}. "
            "So every study that finds the effect has overestimated it. <bookmark mark='d'/> On average they "
            f"report {d['mean_significant']:.2f}: twice the truth. This is called the winner's curse. In a "
            "small study, being significant and being accurate are opposed. Remember that when we run studies "
            "again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(truth), FadeIn(tl), FadeIn(tag))
            vo.wait_until("s")
            self.play(FadeIn(allb, lag_ratio=0.2), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(sigb, lag_ratio=0.03), FadeIn(side[0]), run_time=2.0)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cut), FadeIn(cl))
            vo.wait_until("d")
            self.play(FadeIn(side[2], shift=UP * 0.1), FadeIn(side[3]))
        self.clear_scene()

    def truth_of_a_finding(self):
        from explainer.psychology import evidence as E
        head = heading(r"How many significant findings are true?")
        prior, pw = 0.1, 0.35
        n = 1000
        true_n, null_n = int(prior * n), int((1 - prior) * n)
        hits, false = round(true_n * pw), round(null_n * 0.05)
        ppv = E.ppv(prior, pw)
        rows = VGroup(
            label(rf"{fmt_int(n)} hypotheses are tested", font_size=32, color=WHITE),
            label(rf"{true_n} are true \ $\rightarrow$ \ {hits} reach $p < .05$ \ (power {r2(pw)})", font_size=30,
                  color=TRUTH),
            label(rf"{null_n} are false \ $\rightarrow$ \ {false} reach $p < .05$ \ (the 5\% that chance allows)",
                  font_size=30, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, 1.75, 0])
        grid = VGroup(tiles(hits, hits, TRUTH, size=0.3, buff=0.07, cols=9),
                      tiles(false, false, BAD, size=0.3, buff=0.07, cols=9)).arrange(RIGHT, buff=0.9, aligned_edge=UP)
        grid.move_to([0, -0.75, 0])
        res = VGroup(
            label(rf"of the {hits + false} significant findings, {hits} are true: \ {pct(ppv)}", font_size=36,
                  color=P.ACCENT),
            label(r"the p-values said 5\%. \ The share that are wrong is more than half.", font_size=28, color=WHITE),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.55)
        tag = note(r"computed: illustrative shares; \ one hypothesis in ten true, power 0.35").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Put power together with one more number and you can answer the question the p-value couldn't. "
            "Of the findings that reach significance, how many are true? <bookmark mark='a'/> Suppose a field "
            "tests a thousand hypotheses, and suppose one in ten of them is actually true. That's a guess, and "
            "we'll see some evidence about it at the frontier. <bookmark mark='b'/> With power of point three "
            f"five, {hits} of the hundred true ones reach significance. <bookmark mark='c'/> Of the nine hundred "
            f"false ones, five per cent get through by chance: {false}. <bookmark mark='d'/> So the journals "
            f"print {hits + false} significant findings, and {hits} of them are true. That's "
            f"{100 * ppv:.0f} per cent. Every one of those papers reported p below point oh five, and more than "
            "half are wrong. Nobody cheated. This is only arithmetic, and it follows from testing unlikely ideas "
            "with small samples. It gets worse from here, because so far everyone has been perfectly honest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(grid[0], lag_ratio=0.02))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(grid[1], lag_ratio=0.02))
            vo.wait_until("d")
            self.play(FadeIn(res[0], shift=UP * 0.15))
            self.play(FadeIn(res[1]))
        self.clear_scene()

    def ioannidis(self):
        head = heading(r"Why most published research findings are false, \ 2005")
        A = axes([-2, 1], [0, 1], x_length=6.2, y_length=3.9, xticks=[-2, -1, 0, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: {-2: "1:100", -1: "1:10", 0: "1:1", 1: "10:1"}[int(round(v))],
                 yfmt=lambda v: f"{v:g}", xlabel=r"prior odds that a tested idea is true, \ $R$",
                 ylabel=r"share of significant findings that are true", center=[-3.0, -0.55, 0], font_size=17)
        ax = A.ax
        lx = np.linspace(-2, 1, 200)
        R = 10 ** lx
        curves, keys = VGroup(), []
        for pw, c in ((0.2, SIZE["0.2"]), (0.5, SIZE["0.5"]), (0.8, SIZE["0.8"])):
            curves.add(curve(ax, lx, pw * R / (pw * R + 0.05), c, 4))
            keys.append((c, rf"power {pw:g}"))
        half = DashedLine(ax.c2p(-2, 0.5), ax.c2p(1, 0.5), color=GREY_C, stroke_width=2)
        key = legend(keys, font_size=18).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        key.move_to(ax.c2p(-1.45, 0.82))
        ex = Dot(ax.c2p(np.log10(1 / 9), 0.35 / 9 / (0.35 / 9 + 0.05)), radius=0.09, color=SIG)
        ex_l = label(r"the last screen", font_size=17, color=SIG).next_to(ex, RIGHT, buff=0.12)
        eq = MathTex(r"\mathrm{PPV} = \frac{(1-\beta)\,R}{(1-\beta)\,R + \alpha}", font_size=40, color=WHITE)
        eq.move_to([3.6, 1.55, 0])
        cards = point_cards([
            (r"More likely true than false", r"only when $R > \alpha/(1-\beta)$: \ odds better than 1 in 16 at "
             r"power 0.8, \ 1 in 4 at power 0.2", SIG),
            (r"And then the rest", r"bias, \ many teams on one question, \ flexible analysis: \ each pulls the "
             r"curve down", BAD),
        ], width=6.0, cols=1, font_size=19, buff=0.22)
        cards.next_to(eq, DOWN, buff=0.35)
        tag = published_tag(r"Ioannidis (2005)")
        with self.voiceover(
            "That arithmetic has a famous name. <bookmark mark='a'/> In 2005 John Ioannidis, a physician, published "
            "it as an essay with a deliberately provocative title: Why most published research findings are false. "
            "Write R for the odds that an idea a field tests is true, beta for the chance of missing a true effect, "
            "and alpha for the threshold. The share of significant findings that are true is the power times R, "
            "divided by that plus alpha. <bookmark mark='b'/> Draw it against the odds. With power of point eight, "
            "a significant finding is more likely true than false once the odds pass about one in sixteen. With "
            "power of point two, the odds have to be better than one in four. The field on the last screen sits "
            "here. <bookmark mark='c'/> Then he added what the formula leaves out: bias, many teams chasing the "
            "same question, and flexible analysis, each of which pulls the curve down. <bookmark mark='d'/> "
            "Whether most findings really are false depends on numbers no one sees directly, the odds and the power "
            "of a whole field, and estimates differ widely. Chapter nine measures it the other way, by running the "
            "studies again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(A))
            vo.wait_until("b")
            self.play(Create(half), LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(key),
                      run_time=2.2)
            self.play(FadeIn(cards.cards[0], shift=UP * 0.15))
            self.play(FadeIn(ex, scale=1.5), FadeIn(ex_l))
            vo.wait_until("c")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(Indicate(curves[0], color=SIZE["0.2"]))
        self.clear_scene()
