from __future__ import annotations

from explainer.psychology.psyche import precision as Pr
from videos.psychology.psych59.common import *  # noqa: F403


class Phones(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"Digital phenotyping", r"Can a phone measure a mood?", scale=("person",))
        self.insel()
        self.sim()
        self.limits()

    def insel(self):
        rows_section(self, r"The phone as an instrument", [
            (r"Insel, \ 2017: \ phones record movement, \ sleep, \ typing and talk continuously; \ a "
             r"``digital phenotype'' could track illness between visits", WHITE),
            (r"active data: \ brief questionnaires several times a day (Part 47's experience sampling)", MODEL),
            (r"passive data: \ GPS, \ accelerometer, \ screen use, \ calls, \ with no effort from the person", PERSON),
            (r"early studies of a few dozen people found strong links between GPS features and depression scores; \ "
             r"larger studies found much weaker ones", AUTH),
        ], "Can a phone measure a mood? <bookmark mark='a'/> In 2017 Thomas Insel argued that phones record "
           "movement, sleep, typing and talk continuously, so a digital phenotype could track illness between "
           "visits. <bookmark mark='b'/> Active data are brief questionnaires several times a day, Part 47's "
           "experience sampling. <bookmark mark='c'/> Passive data come from GPS, the accelerometer, screen use and "
           "calls, with no effort from the person. <bookmark mark='d'/> Early studies of a few dozen people found "
           "strong links between GPS features and depression scores. Larger studies found much weaker ones.",
           tag=published_tag(r"Insel (2017)"))

    def sim(self):
        head = heading(r"A small sample's strong correlation")
        rng = np.random.default_rng(5904)
        rs = []
        for n in (30, 300):
            out = []
            for _ in range(400):
                x = rng.standard_normal(n)
                y = 0.2 * x + np.sqrt(1 - 0.04) * rng.standard_normal(n)
                out.append(np.corrcoef(x, y)[0, 1])
            rs.append(np.array(out))
        A = axes([-0.5, 0.8], [0.4, 2.6], x_length=5.6, y_length=2.8, xticks=[-0.4, 0, 0.2, 0.4, 0.8],
                 yticks=None, xfmt=lambda v: f"{v:g}", xlabel=r"observed correlation (true 0.2)",
                 center=[-3.3, 0.4, 0], font_size=12)
        jit = np.random.default_rng(1).uniform(-0.3, 0.3, 400)
        s30 = scatter(A.ax, rs[0], 2.0 + jit, AUTH, radius=0.025)
        s300 = scatter(A.ax, rs[1], 1.0 + jit, GOOD, radius=0.025)
        truth = DashedLine(A.ax.c2p(0.2, 0.4), A.ax.c2p(0.2, 2.6), color=WHITE, stroke_width=2)
        l30 = label(r"30 people", font_size=14, color=AUTH).next_to(A.ax.c2p(-0.5, 2.0), LEFT, buff=0.1)
        l300 = label(r"300 people", font_size=14, color=GOOD).next_to(A.ax.c2p(-0.5, 1.0), LEFT, buff=0.1)
        big = float(np.mean(rs[0] > 0.5))
        rows = rows_of([
            (r"400 simulated studies of a feature whose true correlation with mood is 0.2", WHITE),
            (rf"with 30 people, \ correlations range widely; \ {pct(big)} exceed 0.5", AUTH),
            (r"with 300, \ they cluster near the truth", GOOD),
            (r"the strong early results were the lucky tail of small samples, \ selected for publication (Part 4)",
             YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "Here's why. <bookmark mark='a'/> Four hundred simulated studies of a phone feature whose true correlation "
            "with mood is zero point two. <bookmark mark='b'/> With thirty people, the correlations range widely, and "
            "a few percent exceed zero point five. <bookmark mark='c'/> With three hundred, they cluster near the "
            "truth. <bookmark mark='d'/> The strong early results were the lucky tail of small samples, selected for "
            "publication, as in Part 4."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(truth), FadeIn(l30), FadeIn(l300))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(s30))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(s300))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def limits(self):
        chips_section(self, r"What a phone can and cannot do", [
            (r"within a person", r"changes from a person's own baseline (Part 47) may be more useful than "
                                 r"comparisons between people", GOOD),
            (r"missing data", r"people stop using apps; \ the days with no data may be the worst ones", AUTH),
            (r"privacy", r"location and messages are intimate; \ consent, \ storage and who sees the data are part "
                         r"of the design", CARE),
            (r"action", r"a signal is useful only if someone can act on it in time, \ with a person in the loop", PERSON),
        ], "What can a phone do, and what can't it? <bookmark mark='a'/> Within a person, changes from their own "
           "baseline, Part 47's idea, may be more useful than comparisons between people. <bookmark mark='b'/> "
           "Missing data: people stop using apps, and the days with no data may be the worst ones. "
           "<bookmark mark='c'/> Privacy: location and messages are intimate, so consent, storage, and who sees the "
           "data are part of the design. <bookmark mark='d'/> And action: a signal is useful only if someone can act "
           "on it in time, with a person in the loop.")
