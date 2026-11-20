from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ spending through unemployment", r"What do bank accounts show about how "
             r"households live through a lost job?", "Chapter fifteen. Frontier: spending through unemployment.",
             lit={2019: r"Ganong and Noel", 2018: r"Kaplan, Moll, Violante"}, scale=("household",),
             horizon=("a month", "a year"))
        self.path()
        self.meaning()
        self.open()

    def path(self):
        g = tables.MPC_STUDIES.data["ganong_noel"]
        months = np.arange(-3, 10)
        onset, exhaust = 0, 6
        spend = np.where(months < onset, 1.0, 1.0 - g["onset"])
        during = np.clip(months - onset, 0, exhaust - onset) * 0.005
        spend = spend - np.where(months >= onset, during, 0)
        spend = np.where(months >= exhaust, spend[exhaust - 1 + 3] - g["exhaustion"], spend)
        ax = plane([-3.5, 9.5], [0.7, 1.05], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.8,
                   xticks=[-3, 0, 3, 6, 9], yticks=[0.75, 0.8, 0.85, 0.9, 0.95, 1.0],
                   xlabel=r"months from the job loss", ylabel=r"nondurable spending \ (before $= 1$)",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.2f}", font_size=16)
        steps = VGroup()
        for k in range(len(months) - 1):
            steps.add(Line(ax.ax.c2p(months[k], spend[k]), ax.ax.c2p(months[k + 1], spend[k]), color=SPEND,
                           stroke_width=4))
            steps.add(Line(ax.ax.c2p(months[k + 1], spend[k]), ax.ax.c2p(months[k + 1], spend[k + 1]), color=SPEND,
                           stroke_width=4))
        v1 = DashedLine(ax.ax.c2p(onset, 0.7), ax.ax.c2p(onset, 1.05), color=RISK, stroke_width=2)
        v2 = DashedLine(ax.ax.c2p(exhaust, 0.7), ax.ax.c2p(exhaust, 1.05), color=HOLD, stroke_width=2)
        l1 = label(r"job lost; \\ benefits begin", font_size=16, color=RISK).next_to(ax.ax.c2p(onset, 0.75), RIGHT,
                                                                                  buff=0.1)
        l2 = label(r"benefits run out \\ (foreseeable)", font_size=16, color=HOLD).next_to(ax.ax.c2p(exhaust, 0.75),
                                                                                         RIGHT, buff=0.1)
        side = VGroup(
            label(r"Peter Ganong and Pascal Noel", font_size=21, color=E.ACCENT),
            label(r"bank accounts of people who \\ lost jobs and drew benefits", font_size=19, color=GREY_A),
            label(rf"at the job loss: \ $-{100 * g['onset']:.0f}\%$", font_size=21, color=RISK),
            label(r"while benefits last: \\ under 1\% a month", font_size=19, color=GREY_A),
            label(rf"when benefits run out: \ $-{100 * g['exhaustion']:.0f}\%$", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Ganong and Noel, AER 109(7) (2019): \ 2383--2424; \ magnitudes from NBER WP 25417; \ "
                            r"the path drawn from them", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier is in bank accounts. <bookmark mark='a'/> Peter Ganong and Pascal Noel followed the "
            "accounts of people who lost their jobs and drew unemployment benefits, month by month. "
            "<bookmark mark='b'/> When the job is lost, nondurable spending drops about six percent. "
            "<bookmark mark='c'/> While benefits last, it drifts down by less than one percent a month. "
            "<bookmark mark='d'/> And when the benefits run out, on a date everyone knew from the start, spending "
            f"drops about {100 * g['exhaustion']:.0f} percent, more than in all the months before combined. "
            "<bookmark mark='e'/> A permanent-income household would have seen that date coming and cut back early, "
            "spreading the loss. These households did not."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), Create(VGroup(*steps[:5])), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(v1), FadeIn(l1), FadeIn(side[2]), Create(VGroup(*steps[5:8])))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), Create(VGroup(*steps[8:17])), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(v2), FadeIn(l2), FadeIn(side[4]), Create(VGroup(*steps[17:])), run_time=1.5)
        self.clear_scene()

    def meaning(self):
        rows = VGroup(
            label(r"what it means", font_size=28, color=E.ACCENT),
            label(r"a foreseeable drop in income moves spending: \ Hall's test, \ failed in account data", font_size=23,
                  color=HOLD),
            label(r"for insurance: \ the authors find extending benefits smooths spending four times as much as "
                  r"raising them", font_size=22, color=PENSION),
            label(r"for macroeconomics: \ heterogeneous-agent models, \ where who holds the cash matters "
                  r"\ (Kaplan, \ Moll and Violante's HANK, \ 2018)", font_size=22, color=INCOME),
            label(r"Part 52 builds them, \ by the endogenous grid method of chapter 6", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Ganong and Noel (2019), \ abstract; \ Kaplan, Moll and Violante, AER 108(3) (2018)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "What it means. <bookmark mark='a'/> A drop in income that could be foreseen moved spending when it "
            "came: Hall's test, failed again, in data far better than any survey. <bookmark mark='b'/> For social "
            "insurance, Ganong and Noel calculate that making benefits last longer would smooth spending about four "
            "times as much as making them larger. <bookmark mark='c'/> For macroeconomics, it means models in which "
            "it matters who holds the cash. Greg Kaplan, Benjamin Moll and Giovanni Violante's heterogeneous-agent "
            "New Keynesian model, HANK, showed in 2018 that monetary policy then works less through interest rates "
            "on saving and more through jobs and incomes. <bookmark mark='d'/> Part fifty-two builds such economies, "
            "using the endogenous grid method of chapter six."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def open(self):
        cards = point_cards([
            (r"why the gap?", r"cash shortage, \ inattention, \\ or the bother of planning?", HOLD),
            (r"present bias", r"do people plan to save \\ and then not?", SAVE),
            (r"who saves for whom", r"bequests, \ family, \\ and the state", HOUSE),
            (r"the new data", r"accounts, \ cards \\ and payrolls, \ day by day", CASH),
        ], width=12.4, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Open questions. <bookmark mark='a'/> Why the gap between theory and data: a shortage of cash, "
            "inattention, or the bother of planning, which Kueng's high earners suggest? <bookmark mark='b'/> "
            "Present bias: do people plan to save and then not, as Part forty-five will ask? "
            "<bookmark mark='c'/> Who saves for whom: bequests, families, and the state. <bookmark mark='d'/> And "
            "what the new data, from accounts, cards and payrolls, will show, day by day."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
