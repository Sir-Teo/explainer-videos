from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Corrections(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"Why observed validities mislead", r"Why does a good test look weak among the hired?",
                     marr=("how",))
        self.restriction()
        self.chain()

    def restriction(self):
        d = load("selection")
        head = heading(r"Range restriction")
        x, y, h = np.asarray(d["x"]), np.asarray(d["y"]), np.asarray(d["hired"]).astype(bool)
        A = axes([-3.5, 3.5], [-3.5, 3.5], x_length=4.6, y_length=4.0, xticks=[-2, 0, 2], yticks=[-2, 0, 2],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"test score (z)",
                 ylabel=r"rated performance (z)", center=[-3.6, 0.0, 0], font_size=12)
        rej = scatter(A.ax, np.clip(x[~h][:1000], -3.4, 3.4), np.clip(y[~h][:1000], -3.4, 3.4), OFF, radius=0.025)
        hire = scatter(A.ax, np.clip(x[h], -3.4, 3.4), np.clip(y[h], -3.4, 3.4), PERSON, radius=0.03)
        cut = DashedLine(A.ax.c2p(float(np.min(x[h])), -3.5), A.ax.c2p(float(np.min(x[h])), 3.5), color=AUTH)
        rows = rows_of([
            (r"a company hires the top 20\% on the test: \ performance is observed only for them", WHITE),
            (rf"within the hired, \ the test's spread is less than half the applicants' (a ratio of {d['u']:.2f}), \ and the observed "
             rf"correlation falls to {d['r_obs']:.2f}", PERSON),
            (r"the test still works: \ the hired are better on average; \ but the correlation inside the narrow "
             r"slice cannot show it", MODEL),
            (r"the more selective the company, \ the weaker its own test looks: \ a reason good tests get dropped", YOU),
        ], 7.2, 19, 0.36).move_to([2.9, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.selection}, \ 200{,}000 simulated applicants")
        with self.voiceover(
            "Why does a good test look weak among the people it hired? <bookmark mark='a'/> A company hires the top "
            "fifth on the test, and observes performance only for them. <bookmark mark='b'/> Within the hired, the "
            "test's spread is less than half the applicants', and the observed correlation falls to zero point one "
            "nine. <bookmark mark='c'/> The test still works. The hired are better on average. But the correlation "
            "inside that narrow slice can't show it. <bookmark mark='d'/> So the more selective the company, the "
            "weaker its own test looks. That's one reason good tests get dropped."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rej), FadeIn(hire))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cut), rej.animate.set_opacity(0.25))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def chain(self):
        d = load("selection")
        head = heading(r"Two corrections, \ in order")
        A = axes([0.3, 4.7], [0, 0.6], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.2, 0.4, 0.6],
                 yfmt=lambda v: f"{v:.1f}", ylabel=r"validity", center=[-3.3, 0.3, 0], font_size=12)
        vals = [d["r_obs"], d["r_rel_only"], d["r_both"], d["r_all_true"]]
        cols = [PERSON, SYMP, MODEL, GOOD]
        b = bars(A.ax, [1, 2, 3, 4], vals, cols, width=0.6)
        names = VGroup(*[label(s, font_size=13, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, s in enumerate([r"observed", r"+ reliability", r"+ restriction", r"truth"])])
        nums = VGroup(*[label(f"{v:.2f}", font_size=14, color=c).next_to(A.ax.c2p(i + 1, v), UP, buff=0.08)
                        for i, (v, c) in enumerate(zip(vals, cols))])
        rows = rows_of([
            (rf"criterion unreliability: \ divide by the root of the rating's reliability among incumbents "
             rf"({d['rel_incumbents']:.2f}): \ {d['r_rel_only']:.2f}", SYMP),
            (rf"range restriction, \ Thorndike's Case II with $u$ = {d['u']:.2f}: \ "
             rf"$r_c = r u / \sqrt{{1 + r^2(u^2 - 1)}}$ gives {d['r_both']:.2f}", MODEL),
            (rf"the truth among applicants was {d['r_all_true']:.2f}: \ done right, \ the corrections recover it", GOOD),
            (r"done with the wrong $u$, \ or the wrong reliability, \ they can overshoot just as far: \ the next "
             r"chapter's story", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.selection}, \ \texttt{work.case2}")
        with self.voiceover(
            "Two corrections, applied in order, can undo the damage. <bookmark mark='a'/> First, criterion "
            "unreliability: divide by the square root of the rating's reliability among the incumbents. That gives "
            "zero point two five. <bookmark mark='b'/> Then range restriction. Thorndike's Case Two formula, using "
            "the ratio of the applicants' spread to the hires', gives zero point four nine. "
            "<bookmark mark='c'/> The truth among applicants was zero point five. Done right, the corrections "
            "recover it. <bookmark mark='d'/> But done with the wrong ratio, or the wrong reliability, they can "
            "overshoot just as far. That's the next chapter's story."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(b[0]), FadeIn(nums[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[1]), FadeIn(nums[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[2]), FadeIn(nums[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[3]), FadeIn(nums[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
