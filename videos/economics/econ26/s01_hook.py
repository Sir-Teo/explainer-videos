from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.thirty_six()
        self.weekly()
        self.question()
        self.title()
        self.advice()
        self.objectives()

    def thirty_six(self):
        s = load("svb")
        rows = VGroup(
            label(r"Silicon Valley Bank, \ March 2023", font_size=30, color=E.ACCENT),
            label(r"Wednesday 8 March: \ it announces a loss on selling bonds, \ and plans to raise capital",
                  font_size=22, color=GREY_A),
            label(rf"Thursday 9 March: \ customers withdraw \${s['withdrawn_mar9'] / 1e9:.0f} billion in a day, \ "
                  r"mostly from their phones", font_size=24, color=RUN),
            label(rf"overnight: \ \${s['requested_mar10'] / 1e9:.0f} billion more is requested for the morning",
                  font_size=24, color=RUN),
            label(r"Friday 10 March: \ the bank is closed by its regulator", font_size=24, color=WHITE),
            label(rf"about {100 * s['uninsured_share']:.0f}\% of its deposits were above the insured limit",
                  font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Barr, \ Senate testimony, \ 28 March 2023; \ the Federal Reserve's review (April 2023)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In March 2023, Silicon Valley Bank was the sixteenth largest bank in America, banker to thousands of "
            "technology start-ups. <bookmark mark='a'/> On Wednesday the eighth it announced it had sold bonds at a "
            "loss and would raise new capital. <bookmark mark='b'/> On Thursday its customers withdrew forty-two "
            "billion dollars, in a single day, most of it from their phones. <bookmark mark='c'/> Overnight they asked "
            "for a hundred billion more, to be paid in the morning. <bookmark mark='d'/> On Friday morning the bank "
            "was closed by its regulator. <bookmark mark='e'/> About ninety-four percent of its deposits had been "
            "above the insured limit."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def weekly(self):
        s = load("svb")
        sm = s["small"]
        ax = plane([2022.0, 2025.0], [4850, 5350], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[2022, 2023, 2024, 2025], yticks=[4900, 5100, 5300], ylabel=r"deposits at small US banks, \ "
                   r"billions of dollars", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: commas(v), font_size=16)
        line_ = path(ax, sm["t"], sm["v"], color=DEPOSIT, width=3, smooth=False)
        k = sm["dates"].index("2023-03-15")
        mark = dot(ax, sm["t"][k], sm["v"][k], color=RUN, r=0.09)
        side = VGroup(
            label(rf"the week to 15 March 2023: \\ $-$\${s['small_drop']:.0f} billion", font_size=22, color=RUN),
            label(rf"large banks gained \\ \${s['large_change']:.0f} billion", font_size=20, color=GREY_A),
            label(r"a run is contagious: \\ depositors asked \\ which bank is next", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Federal Reserve, \ H.8: \ deposits of small domestically chartered banks, \ weekly, \ via "
                       r"FRED", corner=DR, font_size=12)
        with self.voiceover(
            "It did not stop at one bank. Here are deposits at America's small banks, week by week. "
            f"<bookmark mark='a'/> In the week to the fifteenth of March they fell by about {s['small_drop']:.0f} "
            f"billion dollars. <bookmark mark='b'/> Large banks gained about {s['large_change']:.0f} billion. "
            "<bookmark mark='c'/> Depositors everywhere were asking which bank would be next. Two more failed that "
            "spring. The model that explains all of this was written forty years earlier, and it explains a run on "
            "a London bank in 1866 just as well."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(line_), run_time=2)
            vo.wait_until("a")
            self.play(GrowFromCenter(mark), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why does a bank that does nothing wrong fail when its depositors panic?", font_size=26,
                  color=RUN),
            label(r"what stops a run: \ suspension, \ insurance, \ a lender of last resort?", font_size=26,
                  color=CB),
            label(r"and what does each of those cost?", font_size=26, color=EQUITY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: why are banks fragile, and can they be made safe? <bookmark mark='a'/> Why can a "
            "bank that has done nothing wrong fail when its depositors panic? <bookmark mark='b'/> What stops a run: "
            "suspending payments, insuring deposits, or a lender of last resort? <bookmark mark='c'/> And what does "
            "each of those cost?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        d = load("dd")
        mini = plane([0, 0.85], [0, 2.0], x_length=4.2, y_length=1.6)
        logo = VGroup(path(mini, d["f"], d["stay"], STAY, width=3), seg(mini, 0, d["c1"], 0.85, d["c1"], RUN, width=3))
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 26 \ $\cdot$ \ Banks and Runs", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part twenty-six: banks and runs."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def advice(self):
        c = label(r"This part explains how banks work and fail. \ It is not financial advice about any bank or "
                  r"deposit.",
                  font_size=26, color=GREY_A)
        with self.voiceover("A note before we start: this part explains how banks work and why they fail. It is not "
                            "advice about any bank or any deposit."):
            self.play(FadeIn(c))
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VI \ $\cdot$ \ Money and the Cycle", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"what a bank does; \ stay or withdraw? \ you choose",
            r"Diamond and Dybvig: \ the contract, \ the run, \ two equilibria",
            r"suspension, \ insurance, \ Bagehot's lender, \ and the moral hazard they create",
            r"capital; \ runs on repo and money funds; \ global games",
            r"the evidence; \ banks as monitors; \ two dials; \ supervision; \ digital runs",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> What a bank does, and a choice for you: stay, or withdraw? "
            "<bookmark mark='b'/> Then the model of 1983 that explains it, with its two equilibria. "
            "<bookmark mark='c'/> The three cures, and the moral hazard each creates. <bookmark mark='d'/> Capital, "
            "runs without any depositors at all, and a refinement that picks one equilibrium. "
            "<bookmark mark='e'/> And the evidence, what is lost when banks fail, two dials, the supervisors, and "
            "runs at the speed of a phone."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
