from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.kirman()
        self.relief()
        self.reversal()
        self.question()
        self.title()
        self.objectives()

    def kirman(self):
        people = crowd(28, 11, 11.0, 4.0, colors=(MANY, POOR, RICH)).move_to(DOWN * 0.9)
        one = Dot(DOWN * 0.9, radius=0.32, color=REP)
        one_lab = label(r"the representative household", font_size=24, color=REP).next_to(one, DOWN, buff=0.3)
        hc = history_card(1992, r"Alan Kirman, \ in the \emph{Journal of Economic Perspectives}",
                          r"``Whom or what does the representative individual represent?''", color=E.ACCENT,
                          width=10.8, font_size=24).to_edge(UP, buff=0.5)
        verdict = label(r"it ``deserves a decent burial''", font_size=30, color=ERR).next_to(one_lab, DOWN, buff=0.35)
        tag = published_tag(r"Kirman, \ JEP 6(2) (1992)", corner=DR, font_size=12)
        with self.voiceover(
            "A country has millions of households: some with savings, some with debts, some one paycheque from "
            "trouble. <bookmark mark='a'/> For a generation, macroeconomics replaced them all with one: a single, "
            "representative household who earns the average income, owns the average wealth and lives for ever. "
            "<bookmark mark='b'/> In 1992 the economist Alan Kirman asked, in the title of an essay, whom or what "
            "the representative individual represents. <bookmark mark='c'/> His answer was that the device has no "
            "general justification, and that it deserves, in his words, a decent burial."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in people], lag_ratio=0.004), run_time=2.5)
            vo.wait_until("a")
            self.play(*[d.animate.move_to(one.get_center()).set_opacity(0.0) for d in people], FadeIn(one),
                      run_time=2.2)
            self.play(FadeIn(one_lab, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=DOWN * 0.1), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()

    def relief(self):
        I = load("island")
        hc = history_card(1998, r"Per Krusell and Anthony Smith",
                          r"solve an economy with a whole distribution of households and aggregate shocks",
                          color=MANY, width=10.8, font_size=24).to_edge(UP, buff=0.5)
        ax = plane([0, 60], [0, 0.08], center=DOWN * 1.1 + LEFT * 1.6, x_length=7.6, y_length=3.4,
                   xticks=[0, 20, 40, 60], yticks=[0, 0.04, 0.08], xlabel=r"wealth, \ in years of the average wage",
                   ylabel=r"share of households", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}",
                   font_size=14)
        bins = np.array(I["bins"])
        bars = VGroup()
        for x0, x1, h in zip(bins[:-1], bins[1:], I["hist"]):
            p0, p1 = ax.ax.c2p(x0, 0), ax.ax.c2p(x1, min(h, 0.08))
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.005), stroke_width=0.4,
                               stroke_color=BLACK, fill_color=DIST, fill_opacity=0.8).move_to((p0 + p1) / 2))
        mean = vline(ax, I["mean"], 0, 0.075, WHITE, 2.4)
        mlab = label(r"the mean", font_size=18, color=WHITE).next_to(ax.ax.c2p(I["mean"], 0.075), UP, buff=0.08)
        quote = label(r"``almost perfectly described \\ using only the mean \\ of the wealth distribution''",
                      font_size=22, color=WHITE).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.6)
        tag = island_tag(rf"{I['n']:,} simulated households, \ this part's economy".replace(",", "{,}"),
                         corner=DL, font_size=12)
        with self.voiceover(
            "Six years later, Per Krusell and Anthony Smith did what Kirman's critics had said was impossible. "
            "<bookmark mark='a'/> They solved an economy with a whole distribution of households, rich and poor, "
            "buffeted by their own luck and by the economy's. <bookmark mark='b'/> To general relief, they found "
            "that the behaviour of the aggregates could be, in their words, almost perfectly described using only "
            "the mean of the wealth distribution. The crowd behaved, on average, almost as if it were one."
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(mlab), FadeIn(quote, shift=LEFT * 0.1))
        self.clear_scene()

    def reversal(self):
        P = load("playit")
        hc = history_card(2018, r"Greg Kaplan, \ Benjamin Moll and Giovanni Violante",
                          r"\emph{Monetary Policy According to HANK}: \ households with little liquid wealth, \ and "
                          r"a central bank that cuts its rate", color=INDIRECT, width=10.8, font_size=23).to_edge(
            UP, buff=0.5)
        old = flow_chain([(r"the rate falls", DIRECT), (r"saving is less rewarded", DIRECT),
                          (r"spending rises", WHITE)], box_w=2.5, box_h=1.0, font_size=20, buff=0.5)
        new = flow_chain([(r"the rate falls", DIRECT), (r"some spend more", DIRECT),
                          (r"firms hire, \ incomes rise", INDIRECT), (r"the rest spend more", INDIRECT)], box_w=2.4,
                         box_h=1.0, font_size=20, buff=0.45)
        VGroup(old, new).arrange(DOWN, buff=0.9).next_to(hc, DOWN, buff=0.6)
        lo = label(r"the textbook: \ directly", font_size=19, color=DIRECT).next_to(old, UP, buff=0.12)
        ln = label(r"with many households: \ mostly through incomes", font_size=19, color=INDIRECT).next_to(
            new, UP, buff=0.12)
        foot = label(rf"this part's economy: \ {100 * (1 - P['share_impact']):.0f}\% of the first quarter's rise "
                     r"comes through incomes", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "And twenty years after that, a model with a realistic distribution turned the textbook account of "
            "monetary policy on its head. <bookmark mark='a'/> In the textbook, when the central bank cuts its "
            "rate, saving is less rewarded, so the household spends more now: a direct effect. <bookmark "
            "mark='b'/> In the economy of Greg Kaplan, Benjamin Moll and Giovanni Violante, the direct effect is "
            "small. Most of the extra spending comes indirectly: some households spend more, firms hire, incomes "
            "rise, and households who live from those incomes spend them. <bookmark mark='c'/> The same split "
            "will appear in this part's own economy."
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(lo), LaggedStart(*[FadeIn(b) for b in old.boxes], lag_ratio=0.4),
                      LaggedStart(*[Create(a) for a in old.arrows], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ln), LaggedStart(*[FadeIn(b) for b in new.boxes], lag_ratio=0.4),
                      LaggedStart(*[Create(a) for a in new.arrows], lag_ratio=0.4), run_time=2.6)
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"when does one household stand for many, \ exactly?", font_size=26, color=REP),
            label(r"what does uninsurable risk do to saving and to interest rates?", font_size=26, color=MANY),
            label(r"can a model with a distribution be solved, \ and fast?", font_size=26, color=DIST),
            label(r"and when does the distribution change the answer?", font_size=26, color=INDIRECT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: what does macroeconomics get wrong by treating a country as one household? <bookmark "
            "mark='a'/> When does one household stand for many, exactly? <bookmark mark='b'/> What does risk that "
            "cannot be insured do to saving and to interest rates? <bookmark mark='c'/> Can an economy with a "
            "whole distribution in it be solved, and quickly? <bookmark mark='d'/> And when does the distribution "
            "change the answer?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([F["t"][0], F["t"][-1]], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["top1"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, DIST, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 52 \ $\cdot$ \ Many Agents", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifty-two: many agents."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act X \ $\cdot$ \ The Graduate Core", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"aggregation: \ when one household is exact, \ and why it rarely is",
            r"Bewley, \ Huggett and Aiyagari: \ risk, \ a borrowing limit, \ the interest rate",
            r"the wealth distribution, \ and what the simple model misses at the top",
            r"Krusell and Smith; \ continuous time; \ HANK and sequence-space Jacobians",
            r"what changes for policy; \ firms that enter, \ grow and exit",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part puts the methods of Part fifty-one to work on whole populations. <bookmark mark='a'/> When "
            "one household is exact, and why it rarely is. <bookmark mark='b'/> Economies of households who face "
            "risk they cannot insure, from Bewley, Huggett and Aiyagari. <bookmark mark='c'/> The wealth "
            "distribution, and what the simple model misses at the top. <bookmark mark='d'/> Aggregate shocks, "
            "continuous time, and the models called HANK, solved by sequence-space Jacobians. <bookmark "
            "mark='e'/> Then what changes for policy, and a population of firms."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
