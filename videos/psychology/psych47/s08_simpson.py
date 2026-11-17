from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403

PCOLS = ["#7EC8F5", "#F2C14E", "#5BD18B", "#EF6F6C", "#B39DDB", "#F29E4C", "#6F9BF2", "#E07BB5", "#9BD1C7",
         "#C9B26B", "#8FA8D9", "#D98F8F"]


class Simpson(VoiceoverScene):
    def construct(self):
        self.card()
        self.colour()
        self.own()

    def card(self):
        card = chapter_card(7, r"Simpson inside a person", r"Can a relation reverse when you look within?",
                            lit={1951: r"Simpson"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter seven. Simpson inside a person."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def colour(self):
        d = load("simpson")
        head = heading(r"The same cloud, \ by person")
        A = axes([-6, 6], [-7, 7], x_length=6.0, y_length=4.4, xticks=[-4, 0, 4], yticks=[-5, 0, 5],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"words typed per minute (scaled)",
                 ylabel=r"errors (scaled)", center=[-3.0, -0.2, 0], font_size=12)
        x, y, g = d["x"], d["y"], d["g"]
        dots = VGroup(*[scatter(A.ax, x[g == i], y[g == i], PCOLS[i % 12], radius=0.05) for i in range(g.max() + 1)])
        lines = VGroup()
        for i in range(g.max() + 1):
            xi, yi = x[g == i], y[g == i]
            xx = np.linspace(xi.min(), xi.max(), 10)
            lines.add(curve_in(A.ax, xx, yi.mean() + d["within"] * (xx - xi.mean()), PCOLS[i % 12], stroke_width=3))
        rows = rows_of([
            (r"colour the dots by person: \ each person's cloud slopes up", WHITE),
            (rf"across people the slope is {d['between']:+.1f}; \ within every person it is {d['within']:+.1f}", MODEL),
            (r"an example: \ faster typists make fewer errors, \ because they are more skilled; \ but any typist "
             r"makes more errors when typing faster than usual", PERSON),
            (r"Simpson's paradox, \ at the scale of one mind: \ the answer for a person was in the data, \ but not in "
             r"the correlation", AUTH),
        ], 5.6, 19, 0.38).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.simpson\_cloud}, \ 12 simulated people")
        with self.voiceover(
            "Here's the cloud from chapter one again. <bookmark mark='a'/> Colour the dots by person, and each "
            "person's own cloud slopes up. <bookmark mark='b'/> Across people the slope is negative; within every "
            "person it's positive. <bookmark mark='c'/> An example: faster typists make fewer errors, because they're "
            "more skilled. But any typist makes more errors when typing faster than usual. "
            "<bookmark mark='d'/> It's Simpson's paradox, at the scale of one mind. The answer for a person was in "
            "the data, but not in the correlation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.1), run_time=2.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def own(self):
        d = load("ownslopes")
        head = heading(r"Every person, \ one by one")
        A = axes([-1, 1], [0, 13], x_length=5.6, y_length=3.0, xticks=[-1, -0.5, 0, 0.5, 1], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"slope", center=[-3.3, 0.3, 0], font_size=13)
        dots = VGroup(*[Dot(A.ax.c2p(float(s), 1 + k), radius=0.08, color=PCOLS[k % 12]) for k, s in enumerate(d["slopes"])])
        pooled = DashedLine(A.ax.c2p(d["pooled"], 0), A.ax.c2p(d["pooled"], 13), color=AUTH, stroke_width=3)
        p_l = label(r"the pooled slope", font_size=13, color=AUTH).next_to(A.ax.c2p(d["pooled"], 13), UP, buff=0.05)
        rows = rows_of([
            (r"fit each person's own line: \ twelve slopes", WHITE),
            (rf"every one is positive, \ between {d['slopes'].min():.2f} and {d['slopes'].max():.2f}", GOOD),
            (rf"the pooled slope, \ {d['pooled']:.2f}, \ lies outside all of them: \ it is the slope of no one in the "
             rf"study", AUTH),
            (r"the test for a claim about persons: \ does it hold person by person?", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "Make it concrete. <bookmark mark='a'/> Fit each person's own line: twelve slopes. "
            "<bookmark mark='b'/> Every one is positive. <bookmark mark='c'/> The pooled slope, negative, lies "
            "outside all of them. It's the slope of no one in the study. <bookmark mark='d'/> That's the test for a "
            "claim about persons: does it hold person by person?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(pooled), FadeIn(p_l))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
