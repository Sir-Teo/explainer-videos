from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


def defendants(n_guilty: int = 30, n: int = 100, cols: int = 20, gap: float = 0.36):
    """A hundred defendants as dots in five rows: the guilty first (red), then the innocent (green)."""
    g = VGroup()
    for k in range(n):
        r, c = divmod(k, cols)
        g.add(Dot([(c - (cols - 1) / 2) * gap, -r * gap, 0], radius=0.11, color=GUILTY if k < n_guilty else INNOCENT))
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.court()
        self.three()
        self.question()
        self.title()
        self.objectives()

    def court(self):
        Pr = load("prosecutor")
        people = defendants().move_to(DOWN * 0.4)
        roles = VGroup(
            VGroup(label(r"the prosecutor", font_size=26, color=SENDER),
                   label(r"wants convictions; \\ cannot lie; \\ chooses the investigation", font_size=19,
                         color=GREY_A)).arrange(DOWN, buff=0.15),
            VGroup(label(r"the judge", font_size=26, color=RECEIVER),
                   label(r"convicts only if guilt is \\ more likely than not; \\ sees the result, \ knows the "
                         r"design", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=3.2).to_edge(UP, buff=0.6)
        key = label(rf"red: \ guilty, \ {100 * Pr['prior']:.0f} in 100 \qquad green: \ innocent", font_size=20,
                    color=WHITE).next_to(people, DOWN, buff=0.5)
        tag = published_tag(r"Kamenica and Gentzkow, \ AER 101(6) (2011)", corner=DR, font_size=12)
        with self.voiceover(
            "A prosecutor wants convictions. <bookmark mark='a'/> A judge will convict only if guilt is more likely "
            "than not. <bookmark mark='b'/> Of every hundred defendants who come before them, "
            f"{100 * Pr['prior']:.0f} are guilty, and both know it. <bookmark mark='c'/> The prosecutor cannot lie, "
            "cannot hide evidence and cannot bribe anyone. The one thing she controls is which investigation to "
            "run: what will be looked at, and what will be reported. The judge sees the result, knows how the "
            "investigation was designed, and reasons correctly. How many defendants can she get convicted?"
        ) as vo:
            self.play(FadeIn(roles[0], shift=DOWN * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(roles[1], shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in people], lag_ratio=0.01), FadeIn(key),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(roles[0], color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def three(self):
        Pr = load("prosecutor")
        n_inn = int(round(100 * (1 - Pr["prior"])))
        flagged_inn = int(round(100 * Pr["innocent_convicted"]))
        cols = VGroup()
        specs = [
            (r"no investigation", r"the judge knows only the 30\%: \\ acquit everyone", 0, 0),
            (r"a perfect investigation", r"the guilty are found guilty: \\ 30 convicted", 30, 0),
            (r"a designed investigation", rf"every guilty one flagged, \ and {flagged_inn} \\ of the {n_inn} innocent: "
                                          rf"\ {int(round(100 * Pr['optimal']))} convicted", 30, flagged_inn),
        ]
        for title, body, g_conv, i_conv in specs:
            people = VGroup()
            for k in range(100):
                r_, c_ = divmod(k, 10)
                guilty = k < 30
                convicted = (guilty and k < g_conv) or ((not guilty) and (k - 30) < i_conv)
                col = GUILTY if guilty else INNOCENT
                d = Dot([(c_ - 4.5) * 0.3, -r_ * 0.3, 0], radius=0.09, color=col)
                if not convicted:
                    d.set_opacity(0.25)
                people.add(d)
            ring = SurroundingRectangle(people, buff=0.12, color=GREY_D, stroke_width=1.5)
            col_ = VGroup(label(title, font_size=21, color=SENDER), VGroup(people, ring),
                          label(body, font_size=17, color=WHITE)).arrange(DOWN, buff=0.25)
            cols.add(col_)
        cols.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.1)
        if cols.width > 13.2:
            cols.width = 13.2
        foot = label(r"bright: \ convicted \qquad faint: \ acquitted", font_size=17, color=GREY_A).to_edge(DOWN,
                                                                                                   buff=0.3)
        with self.voiceover(
            "Three investigations. <bookmark mark='a'/> With none, the judge knows only that thirty percent are "
            "guilty. That is less likely than not, so everyone is acquitted. <bookmark mark='b'/> With a perfect "
            "investigation, the judge learns the truth, and the thirty guilty are convicted. <bookmark mark='c'/> "
            "Now a designed one. It flags every guilty defendant, and also flags "
            f"{flagged_inn} of the {n_inn} innocent ones. Among the flagged, exactly half are guilty: just enough "
            "for the judge to convict, which a judge who follows the evidence must. <bookmark mark='d'/> "
            f"{int(round(100 * Pr['optimal']))} convictions out of a hundred: twice the truth, with nobody "
            "deceived. Emir Kamenica and Matthew Gentzkow called this Bayesian persuasion."
        ) as vo:
            self.play(FadeIn(foot))
            for mk, c_ in zip("abc", cols):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1), run_time=1.2)
            vo.wait_until("d")
            self.play(Indicate(cols[2][1], color=SENDER, scale_factor=1.03))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what do people infer from what they are shown?", font_size=26, color=BELIEF),
            label(r"when does talk carry information, \ and how much?", font_size=26, color=SIGNAL),
            label(r"what is the best way to reveal, \ and what can it achieve?", font_size=26, color=SENDER),
            label(r"and what happens when many people learn from each other?", font_size=26, color=RECEIVER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: how does someone who controls only what others learn get them to do what she wants? "
            "<bookmark mark='a'/> What do people infer from what they are shown? <bookmark mark='b'/> When does "
            "talk carry information, and how much? <bookmark mark='c'/> What is the best way to reveal, and what "
            "can it achieve? <bookmark mark='d'/> And what happens when many people learn from each other?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([F["t"][0], F["t"][-1]], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["expected"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, BELIEF, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 53 \ $\cdot$ \ Information and Persuasion", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifty-three: information and persuasion."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act X \ $\cdot$ \ The Graduate Core", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"Bayesian games, \ and equilibria with beliefs on and off the path",
            r"cheap talk; \ Bayesian persuasion; \ information design for many",
            r"Blackwell's order; \ common knowledge; \ global games",
            r"herds, \ reputation, \ bargaining with private values",
            r"relational contracts: \ promises kept because the future matters",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part is about information as a strategic object. <bookmark mark='a'/> Games in which players "
            "know different things, and equilibria with beliefs. <bookmark mark='b'/> Talk that costs nothing, "
            "persuasion by design, and information designed for many people at once. <bookmark mark='c'/> When "
            "one source of information is better than another for everyone; common knowledge; and global games. "
            "<bookmark mark='d'/> Herds, reputation, and bargaining when values are private. <bookmark mark='e'/> "
            "And promises that are kept only because the future matters."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
