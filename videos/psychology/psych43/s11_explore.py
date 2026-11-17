from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


class Explore(VoiceoverScene):
    def construct(self):
        self.card()
        self.multiverse()
        self.garden()

    def card(self):
        card = chapter_card(10, r"Exploratory, \ and labelled", r"What else do the data say?", lit=(), part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter ten. Exploratory, and labelled."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def multiverse(self):
        m = load("multiverse")
        head = heading(r"A small multiverse")
        n = len(m["ed_est"])
        A = axes([-0.3, 0.5], [0, n + 1], x_length=5.2, y_length=4.4, xticks=[-0.2, 0, 0.2, 0.4], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"ego depletion, \ $g$", center=[-3.3, 0.0, 0], font_size=13)
        rows_g = VGroup()
        for i in range(n):
            y = n - i
            col = AUTH if "English" not in str(m["ed_label"][i]) else PERSON
            rows_g.add(VGroup(Line(A.ax.c2p(max(-0.3, m["ed_lo"][i]), y), A.ax.c2p(min(0.5, m["ed_hi"][i]), y),
                                   color=GREY_B, stroke_width=1.5),
                              Dot(A.ax.c2p(m["ed_est"][i], y), radius=0.05, color=col),
                              label(str(m["ed_label"][i]), font_size=10, color=GREY_A).next_to(A.ax.c2p(0.5, y), RIGHT,
                                                                                               buff=0.1)))
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, n + 1), color=GREY_B, stroke_width=1.5)
        eng = m["ed_est"][["English" in str(x) for x in m["ed_label"]]]
        lo_s, hi_s = f"{eng.min():.2f}", f"{eng.max():.2f}"
        rows = rows_of([
            (r"exploratory analyses are allowed, \ and labelled as such: \ they suggest, \ they do not test", WHITE),
            (r"every combination of estimator (fixed or random), \ exclusion rule and subset of labs, \ shown at "
             r"once", MODEL),
            (rf"in English-speaking labs, \ the estimate rises to between {lo_s} and {hi_s}", PERSON),
            (r"a hypothesis for a new registered study, \ not a finding: \ eight forks invite the garden of Part 4", YOU),
        ], 4.6, 18, 0.36).move_to([4.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{capstone.multiverse}")
        with self.voiceover(
            f"After the confirmatory test, exploration is allowed, as long as it's labelled. <bookmark mark='a'/> "
            f"Exploratory analyses suggest; they don't test. <bookmark mark='b'/> Here is a small multiverse for ego "
            f"depletion: every combination of estimator, exclusion rule and subset of labs, shown at once. "
            f"<bookmark mark='c'/> In the English-speaking labs, the estimate rises to between {lo_s} and {hi_s}. "
            f"<bookmark mark='d'/> That's a hypothesis for a new registered study, not a finding. Eight forks are "
            f"already the start of Part 4's garden."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(r) for r in rows_g], lag_ratio=0.2), run_time=2.0)
            for mk, r in zip("cd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def garden(self):
        g = load("garden")
        head = heading(r"The garden, \ simulated")
        A = axes([0.3, 2.7], [0, 0.15], x_length=4.4, y_length=3.2, xticks=None, yticks=[0, 0.05, 0.1, 0.15],
                 yfmt=lambda v: f"{v:g}", ylabel=r"false-positive rate", center=[-3.6, 0.3, 0], font_size=13)
        b = bars(A.ax, [1, 2], [g["one"], g["any"]], [GOOD, AUTH], width=0.6)
        names = VGroup(wrapped_label(r"the one planned analysis", 1.8, 13, GOOD).next_to(A.ax.c2p(1, 0), DOWN, buff=0.12),
                       wrapped_label(rf"best of {g['n_analyses']}", 1.8, 13, AUTH).next_to(A.ax.c2p(2, 0), DOWN, buff=0.12))
        five = DashedLine(A.ax.c2p(0.3, 0.05), A.ax.c2p(2.7, 0.05), color=GREY_B, stroke_width=1.5)
        rows = rows_of([
            (rf"Psyche runs the replication {g['reps']} times with no effect at all", WHITE),
            (rf"the planned analysis is significant in {100 * g['one']:.0f}\% of runs: \ the promised 5\%, \ "
             rf"within noise", GOOD),
            (rf"let an analyst choose afterwards among {g['n_analyses']} defensible analyses (two estimators; \ all "
             rf"labs, \ or either half of three splits): \ {100 * g['any']:.0f}\%", AUTH),
            (r"that is why the multiverse is labelled exploratory: \ its best result is a hypothesis for the next study",
             YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{capstone.simulate\_labs}, \ \texttt{multiverse}")
        with self.voiceover(
            "Why label it? <bookmark mark='a'/> Psyche runs the whole replication three hundred times, with no effect "
            "at all. <bookmark mark='b'/> The planned analysis comes out significant in about four percent of runs: "
            "the promised five, within noise. <bookmark mark='c'/> But let an analyst choose afterwards among fourteen "
            "defensible analyses, and something comes out significant about twelve percent of the time. "
            "<bookmark mark='d'/> That's why the multiverse is labelled exploratory. Its best result is a hypothesis "
            "for the next study."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(five))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
