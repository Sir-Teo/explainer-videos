from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Disability(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Disability insurance", r"Do disability benefits keep people from working?",
             "Chapter ten. Disability insurance.", lit={2013: r"Maestas, \ Mullen and Strand"},
             scale=("person", "nation"), horizon=("a year", "a decade"))
        self.screening()
        self.examiners()
        self.heterogeneity()

    def screening(self):
        steps = flow_chain([(r"an applicant", UNEMP), (r"an examiner \\ judges the \\ impairment", HOLD),
                            (r"allowed: \\ benefits, \\ little work", LOSS), (r"denied: \\ some work, \\ some do not",
                                                                              WORK)],
                           notes=[r"severity \\ partly hidden", r"some strict, \\ some lenient", r"if they could "
                                  r"\\ have worked, \\ a cost", r"if they could \\ not, \ a hardship"], box_w=2.6,
                           font_size=19, note_size=15).move_to(UP * 0.9)
        foot = label(r"the question: \ for those on the margin, \ how much would they work without benefits?",
                     font_size=21, color=E.ACCENT).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Disability insurance replaces the earnings of people who can no longer work. Its difficulty is "
            "screening. <bookmark mark='a'/> An applicant's ability to work is only partly visible. "
            "<bookmark mark='b'/> An examiner, or a judge on appeal, decides from the medical record. "
            "<bookmark mark='c'/> Those allowed rarely work again, partly because they cannot and partly because "
            "work would cost them the benefit. <bookmark mark='d'/> Those denied: some go back to work, some cannot. "
            "Errors go both ways, and both are costly. <bookmark mark='e'/> The key question is about the applicants "
            "on the margin, the ones an examiner might allow or deny: how much would they work without benefits?"
        ) as vo:
            self.play(FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            for mk, k in zip("bcd", range(1, 4)):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k - 1]), FadeIn(steps.boxes[k]), FadeIn(steps.notes[k]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def examiners(self):
        X = load("examiners")
        rates = np.array(X["rates"])
        ax = plane([0.1, 0.9], [0, 45], center=LEFT * 3.4 + DOWN * 0.3, x_length=5.4, y_length=4.2,
                   xticks=[0.2, 0.4, 0.6, 0.8], yticks=[0, 20, 40], xlabel=r"examiner's allowance rate",
                   ylabel=r"examiners", xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.0f}",
                   font_size=13)
        edges = np.linspace(0.1, 0.9, 17)
        h, _ = np.histogram(rates, edges)
        hist = VGroup()
        for a, b, n in zip(edges[:-1], edges[1:], h):
            if n == 0:
                continue
            p0, p1 = ax.ax.c2p(a, 0), ax.ax.c2p(b, n)
            hist.add(Rectangle(width=(p1[0] - p0[0]) * 0.92, height=p1[1] - p0[1], stroke_width=0,
                               fill_color=HOLD, fill_opacity=0.8).move_to((p0 + p1) / 2))
        vals = [(r"naive: \ allowed against \\ denied applicants", X["naive"], LOSS),
                (r"the examiner instrument", X["iv"], GAIN),
                (r"the truth for those \\ on the margin", X["true_marginal"], WHITE)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(vals):
            y = 1.2 - 1.1 * k
            w = abs(v) * 5.0
            r = Rectangle(width=w, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([1.2 + w / 2, y, 0]))
            bars.add(VGroup(r, label(nm, font_size=16, color=col).next_to(np.array([1.2, y + 0.4, 0]), RIGHT,
                                                                           buff=0.0),
                            label(rf"$-${100 * abs(v):.0f} points", font_size=18, color=col).next_to(r, RIGHT,
                                                                                                buff=0.1)))
        bh = label(r"effect of benefits on working", font_size=19, color=GREY_A).move_to(np.array([3.2, 2.3, 0]))
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 2013 Nicole Maestas, Kathleen Mullen and Alexander Strand found a natural experiment inside the "
            "system. Applications are assigned to examiners essentially at random, and examiners differ. "
            "<bookmark mark='a'/> On the Island, two hundred examiners see similar applicants, yet most allow "
            "between about a quarter and three quarters of the claims they see. <bookmark mark='b'/> Compare "
            "allowed with denied applicants directly, and "
            f"benefits seem to cut work by {abs(100 * X['naive']):.0f} percentage points. But the allowed are sicker; "
            "they would have worked less anyway. <bookmark mark='c'/> Instead, use the examiner's leniency as an "
            f"instrument: the answer is {abs(100 * X['iv']):.0f} points, <bookmark mark='d'/> close to the "
            f"truth for applicants on the margin, {abs(100 * X['true_marginal']):.0f}. Assignment by chance turns "
            "a judge's temperament into an experiment."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(bh), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in hist], lag_ratio=0.05), run_time=1.5)
            for mk, b_ in zip("bcd", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b_[0], LEFT), FadeIn(b_[1]), FadeIn(b_[2]))
        self.clear_scene()

    def heterogeneity(self):
        X = load("examiners")
        D = tables.DISABILITY_2013.data
        sev = np.array(X["severity"])
        eff = -np.array(X["effect_by_severity"])
        ax = plane([0, 1], [0, 1.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"severity of the impairment \ (Island scale)",
                   ylabel=r"work lost to benefits, \ percentage points", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{100 * v:.0f}", font_size=14)
        ln = path(ax, sev, eff, LOSS, 3.4)
        side = VGroup(
            label(r"the Island: \ the less severe, \\ the more work benefits \\ displace", font_size=18,
                  color=LOSS),
            label(rf"Maestas, \ Mullen and Strand: \\ from {D['lo']} for the most \\ severe to {D['hi']} points "
                  r"\\ for the least", font_size=18, color=E.ACCENT),
            label(r"the hard part: \\ telling them apart", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.DISABILITY_2013.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The average hides a range. <bookmark mark='a'/> On the Island, benefits displace a lot of work for "
            "applicants with mild impairments and almost none for the most severe, who could not work anyway. "
            "<bookmark mark='b'/> Maestas, Mullen and Strand found the same pattern in American data: no effect for "
            "those with the most severe impairments, and up to fifty percentage points for those with the least. "
            "<bookmark mark='c'/> So disability insurance works well where impairments are clear and less well "
            "where they are not, and the design question is how to tell the two apart, or how to let people try "
            "work without losing their benefits."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
