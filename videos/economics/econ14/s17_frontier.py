from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ relational contracts, \ and incentives for machines", r"What holds a promise no "
             r"court will enforce, \ and what happens when a machine is paid in points?",
             "Chapter fifteen. Frontier: relational contracts, and incentives for machines.",
             lit={2002: r"Baker, Gibbons and Murphy", 2003: r"Levin", 2019: r"Hadfield-Menell and Hadfield",
                  2023: r"Gao, Schulman and Hilton"},
             scale=("person", "firm"), horizon=("a career",))
        self.relational()
        self.machines()
        self.goodhart()

    def relational(self):
        r = load("relational")
        d, e = np.array(r["delta"]), np.array(r["effort"])
        ax = plane([0, 1], [0, 11], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 5, 10], xlabel=r"chance the relationship goes on, "
                   r"\ each season", ylabel=r"the effort the promise can buy", font_size=16,
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        c = path(ax, d, e, color=TEAM, width=3.5, smooth=False)
        fb = seg(ax, 0, r["first_best"], 1, r["first_best"], color=GREY_B, width=1.5, dashed=True)
        fbl = label(r"as if effort could be enforced", font_size=14, color=GREY_B).next_to(a.c2p(0.8, 10), UP,
                                                                                         buff=0.08)
        th = Dot(a.c2p(r["threshold"], r["first_best"]), radius=0.09, color=E.ACCENT)
        thl = label(r"patient enough", font_size=15, color=E.ACCENT).next_to(th, DR, buff=0.1)
        side = VGroup(
            label(r"much of what a firm wants \\ can be seen, \ but not proved to a court", font_size=21),
            label(r"so Crusoe promises a bonus, \\ and keeps the promise \\ because the relationship is worth more",
                  font_size=21, color=TEAM),
            label(r"reneging saves one bonus \\ and loses every future season", font_size=21, color=RISK),
            label(r"part eleven's folk theorem, \\ inside the firm", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Baker, Gibbons and Murphy, QJE 117(1) (2002); \ Levin, AER 93(3) (2003); \ the curve: "
                            r"\ Agora", corner=DR, font_size=12)
        with self.voiceover(
            "Two frontiers. The first: most of what a firm wants from its people can be seen, but not proved to a "
            "court. <bookmark mark='a'/> Did the engineer help a colleague? Was the report thoughtful? Crusoe can "
            "tell, but no judge could. <bookmark mark='b'/> So he promises Friday a bonus for good work, and keeps "
            "the promise, because the relationship is worth more to him than the bonus. George Baker, Robert Gibbons "
            "and Kevin Murphy, and Jonathan Levin, worked out when such relational contracts hold. "
            "<bookmark mark='c'/> Reneging saves one bonus and loses every future season. In Agora, if the "
            "relationship is likely enough to go on, at least an even chance each season here, the promise can buy "
            "all the effort a court-enforced contract could; below that, less. <bookmark mark='d'/> It is part "
            "eleven's folk theorem, inside the firm. Robert Gibbons and Rebecca Henderson have argued that "
            "differences in these unwritten understandings help explain why firms that look alike perform so "
            "differently."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(fb), FadeIn(fbl))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(c), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(th, scale=1.5), FadeIn(thl))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def machines(self):
        rows = VGroup(
            label(r"a machine-learning model is an agent paid in points: \ its reward", font_size=25, color=E.ACCENT),
            label(r"the designer can't write down everything wanted, \ any more than an employer can", font_size=23),
            label(r"a boat-racing game, \ 2016: \ the agent, \ rewarded for points, \ circled forever hitting targets "
                  r"\ instead of finishing", font_size=21, color=SIGNAL),
            label(r"researchers have collected many such cases: \ specification gaming", font_size=22, color=SIGNAL),
            label(r"Dylan Hadfield-Menell and Gillian Hadfield, \ 2019: \ the reward is an incomplete contract",
                  font_size=22, color=TEAM),
            label(r"chapter seven's multitasking, \ with an agent that searches far harder than any person",
                  font_size=23, color=RISK),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Amodei and Clark, OpenAI (2016); \ Krakovna et al., DeepMind (2020); \ Hadfield-Menell "
                            r"and Hadfield, AIES (2019)", corner=DR, font_size=12)
        with self.voiceover(
            "The second frontier was the last card in the hook's list. <bookmark mark='a'/> A machine-learning "
            "model trained by reward is an agent paid in points. <bookmark mark='b'/> Its designer can't write down "
            "everything that is wanted, any more than an employer can. <bookmark mark='c'/> In 2016 researchers at "
            "OpenAI trained an agent on a boat-racing game, rewarded by its score. It found a lagoon where it could "
            "circle forever, hitting the same targets as they reappeared, and never finished the race. "
            "<bookmark mark='d'/> Researchers have since collected many such cases, which they call specification "
            "gaming. <bookmark mark='e'/> In 2019 Dylan Hadfield-Menell and Gillian Hadfield argued that a reward is "
            "an incomplete contract, and that the economics of this part is the place to start. "
            "<bookmark mark='f'/> It is chapter seven's multitasking, with an agent that searches for whatever the "
            "measure rewards far harder than any person would."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def goodhart(self):
        g = load("goodhart")
        d, gold, proxy = np.array(g["d"]), np.array(g["gold"]), np.array(g["proxy"])
        ax = plane([0, 10], [0, 8.5], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[0, 5, 10], yticks=[], xlabel=r"how hard the model is optimized against the measure",
                   ylabel=r"reward", font_size=16, xfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        cp = path(ax, d, proxy, color=SIGNAL, width=3.5)
        cg = path(ax, d, gold, color=EFFORT, width=3.5)
        lp = label(r"the measure: \ a learnt model of what people prefer", font_size=15, color=SIGNAL).next_to(
            a.c2p(9.8, proxy[-1]), UP, buff=0.1, aligned_edge=RIGHT)
        lg = label(r"what people actually prefer", font_size=15, color=EFFORT).next_to(a.c2p(5, gold[50]), UP,
                                                                                     buff=0.12)
        pk = DashedLine(a.c2p(g["peak"], 0), a.c2p(g["peak"], gold[50]), color=E.ACCENT, stroke_width=2)
        side = VGroup(
            VGroup(label(r"Leo Gao, \ John Schulman and Jacob Hilton, \ 2023", font_size=20, color=GREY_A),
                   label(r"a model tuned against a learnt measure \\ of what people prefer; \ a second, \ larger "
                         r"model \\ stands in for the truth", font_size=19, color=GREY_B)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            label(r"push harder on the measure, \\ and it keeps rising", font_size=21, color=SIGNAL),
            label(r"the real goal rises, \ peaks, \\ and then falls", font_size=21, color=EFFORT),
            label(r"Goodhart's law, \ as Marilyn Strathern put it: \\ ``when a measure becomes a target, \\ it "
                  r"ceases to be a good measure''", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = illustrative_tag(r"the shape Gao, Schulman and Hilton fitted (2023); \ the constants: \ illustrative",
                               corner=DR, font_size=12)
        with self.voiceover(
            "There is now a measured version of the problem. <bookmark mark='a'/> Language models are tuned against "
            "a learnt model of what people prefer, a measure of the goal rather than the goal itself. In 2023 Leo "
            "Gao, John Schulman and Jacob Hilton stood in a second, larger model for what people actually prefer, "
            "and optimized against the first. <bookmark mark='b'/> The harder the optimization pushed, the higher "
            "the measure rose. <bookmark mark='c'/> The real goal rose at first, then peaked, and then fell, along a "
            "curve whose shape they could fit and predict. <bookmark mark='d'/> Economists have a name for this, "
            "from Charles Goodhart, and an anthropologist, Marilyn Strathern, put it best: when a measure becomes a "
            "target, it ceases to be a good measure. Holmström and Milgrom's remedy has a machine version too: "
            "weaker incentives on a narrow measure, which in practice means a penalty for moving the model far from "
            "where it began."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cp), FadeIn(lp), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(cg), FadeIn(lg), FadeIn(side[2]), run_time=2)
            self.play(Create(pk))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
