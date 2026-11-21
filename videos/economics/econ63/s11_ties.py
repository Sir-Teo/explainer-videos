from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403


class Ties(VoiceoverScene):
    def construct(self):
        card(self, 9, r"The strength of weak ties", r"Who tells you about your next job: \ your friends, \ or people "
             r"you barely know?", "Chapter nine. The strength of weak ties.",
             lit={1973: r"Granovetter", 2022: r"Rajkumar et al."}, scale=("person", "city"), horizon=("a year",))
        self.survey()
        self.curves()
        self.called()

    def survey(self):
        vals = (16.7, 55.6, 27.8)
        names = (r"often \\ (twice a week or more)", r"occasionally", r"rarely \\ (once a year or less)")
        cols = (SHOCK, GDP, PEOPLE)
        ax = plane([-0.6, 2.6], [0, 60], center=LEFT * 2.8 + DOWN * 0.3, x_length=5.8, y_length=4.6, xticks=[],
                   yticks=[0, 20, 40, 60], ylabel=r"job-finders who used a contact, \ \%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        b = bars(ax, range(3), vals, cols, width=0.55)
        labs = VGroup(*[label(n, font_size=14, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.12)
                        for k, (n, c) in enumerate(zip(names, cols))])
        vl = VGroup(*[label(f"{v:.0f}", font_size=16, color=c).next_to(x, UP, buff=0.06)
                      for v, c, x in zip(vals, cols, b)])
        side = VGroup(
            label(r"Newton, \ Massachusetts, \ late 1960s: \\ professional, \ technical and managerial \\ workers "
                  r"who had just changed jobs", font_size=19, color=WHITE),
            label(r"how often had they seen \\ the contact who told them?", font_size=19, color=GREY_A),
            label(r"mostly: \ occasionally or rarely", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        tag = published_tag(r"Granovetter, \ American Journal of Sociology 78(6) (1973): \ 54 job-finders who used a "
                            r"contact", corner=DL, font_size=12)
        with self.voiceover(
            "Networks carry information as well as goods and debts. In the late 1960s the sociologist Mark "
            "Granovetter asked professional, technical and managerial workers in Newton, Massachusetts, who had "
            "just changed jobs, how they had heard of the new one. <bookmark mark='a'/> Many had heard through a "
            "personal contact. So he asked how often they had seen that contact at the time. <bookmark mark='b'/> "
            "Often, twice a week or more: only one in six. <bookmark mark='c'/> Occasionally: more than half. "
            "Rarely, once a year or less: more than a quarter. <bookmark mark='d'/> The news came mostly from "
            "acquaintances, not friends. He called it the strength of weak ties."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(vl[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[1], DOWN), GrowFromEdge(b[2], DOWN), FadeIn(vl[1:]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def curves(self):
        W = load("ties")
        s = np.array(W["strength"])
        ax = plane([0, 1], [0, 1.05], center=LEFT * 2.4 + DOWN * 0.3, x_length=6.6, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"strength of the tie \ (how often you meet, \ how many friends you share)",
                   ylabel=r"chance", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        nv = path(ax, s, W["novel"], LINK, 3.2)
        ps = path(ax, s, W["passes"], PEOPLE, 3.2)
        vv = path(ax, s, 2.5 * np.array(W["value"]), GDP, 3.8)
        pk = vline(ax, W["peak"], 0, 1.0, GDP)
        side = VGroup(
            label(r"blue: \ they know of a job you do not", font_size=19, color=LINK),
            label(r"green: \ they bother to tell you", font_size=19, color=PEOPLE),
            label(r"gold: \ both, \ the tie's value \ (scaled)", font_size=19, color=GDP),
            label(rf"best: \ fairly weak ties \ ({W['peak']:.2f})", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"the Island: \ an illustration; \ agora.network.weak\_ties", corner=DL, font_size=12)
        with self.voiceover(
            "Why would acquaintances help more than friends? Two forces pull in opposite directions. <bookmark "
            "mark='a'/> Your close friends move in your circles: they know what you know. The weaker the tie, the "
            "more likely the other person has heard of something you have not. <bookmark mark='b'/> But the "
            "weaker the tie, the less likely they think of you, or bother to pass it on. <bookmark mark='c'/> A "
            "tie is worth the product of the two. <bookmark mark='d'/> It peaks at fairly weak ties: not "
            "strangers, not best friends, but the people you see now and then. Granovetter's survey could not "
            "show which way the causation ran. Fifty years later, a platform's experiments could."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(nv), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ps), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(vv), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(pk), FadeIn(side[3]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["granovetter_1973"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 0.6)
        lesson = label(r"moderately weak ties, \ not the weakest: \ an inverted U, \ as the two forces predict",
                       font_size=21, color=E.ACCENT).next_to(cc, DOWN, buff=0.55)
        tag = published_tag(r"Granovetter (1973); \ Rajkumar, \ Saint-Jacques, \ Bojinov, \ Brynjolfsson and Aral, \ "
                            r"Science 377(6612) (2022)", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1973 Granovetter argued that weak ties, more than strong ones, "
            "carry news of jobs you have not heard of. <bookmark mark='b'/> In 2022 Karthik Rajkumar, Guillaume "
            "Saint-Jacques, Iavor Bojinov, Erik Brynjolfsson and Sinan Aral used LinkedIn's experiments with the "
            "connections it suggests, which changed at random who met whom, among twenty million people over five "
            "years. The ties that most raised the chance of moving to a new job were moderately weak; the strongest "
            "and the very weakest helped least, and weak ties mattered most in digital industries. <bookmark "
            "mark='c'/> The verdict: right. <bookmark mark='d'/> And with the shape the two forces predict: an "
            "inverted U."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cc.left, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.clear_scene()
