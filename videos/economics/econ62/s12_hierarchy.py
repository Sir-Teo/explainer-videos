from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Hierarchy(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Hierarchies of knowledge", r"Who should solve which problems, \ and what does technology do "
             r"to the answer?", "Chapter ten. Hierarchies of knowledge.",
             lit={2000: r"Garicano", 2014: r"Bloom, Garicano, Sadun and Van Reenen"}, scale=("firm",),
             horizon=("a decade",))
        self.team()
        self.technology()

    def team(self):
        z = np.linspace(0, 4, 120)
        ax = plane([0, 4], [0, 1.05], center=LEFT * 3.0 + DOWN * 0.6, x_length=6.2, y_length=3.6,
                   xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 1.0], xlabel=r"how hard a problem is", ylabel=r"share "
                   r"of problems", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        dens = path(ax, z, np.exp(-z), WHITE, 2.4)
        zw, zm = 1.3, 3.2
        fw = Polygon(*[ax.ax.c2p(x, 0) for x in (0, zw)], *[ax.ax.c2p(x, np.exp(-x)) for x in np.linspace(zw, 0, 40)],
                     stroke_width=0, fill_color=WORK, fill_opacity=0.45)
        fm = Polygon(*[ax.ax.c2p(x, 0) for x in (zw, zm)], *[ax.ax.c2p(x, np.exp(-x)) for x in np.linspace(zm, zw, 40)],
                     stroke_width=0, fill_color=MGR, fill_opacity=0.45)
        side = VGroup(
            label(r"most problems are easy; \ a few are hard", font_size=19, color=WHITE),
            label(r"gold: \ workers learn enough to solve the easy ones", font_size=19, color=WORK),
            label(r"purple: \ the rest go up to a manager, \ who knows more", font_size=19, color=MGR),
            label(r"knowledge is costly to learn, \ and asking for help costs the manager's time", font_size=19,
                  color=GREY_A),
            label(r"so: \ how much should workers know, \ and how many can one manager help?", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Garicano, \ Journal of Political Economy 108(5) (2000)", corner=DL, font_size=12)
        with self.voiceover(
            "Why do firms have hierarchies at all? Luis Garicano's answer is knowledge. <bookmark mark='a'/> "
            "Production throws up problems; most are easy and a few are hard. <bookmark mark='b'/> Workers learn "
            "enough to solve the easy ones themselves. <bookmark mark='c'/> The rest go up to a manager, who knows "
            "more. <bookmark mark='d'/> Knowledge is costly to learn, so not everyone should know everything; and "
            "asking for help costs the manager's time, so the more problems workers pass up, the fewer workers one "
            "manager can support. <bookmark mark='e'/> The design question is how much workers should know, and "
            "so how many people one manager can help: the span of control."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(dens), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(fw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(fm), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def technology(self):
        H = load("hierarchy")["rows"]
        hs = sorted({r["h"] for r in H}, reverse=True)
        cs = sorted({r["c"] for r in H}, reverse=True)
        at = {(r["h"], r["c"]): r for r in H}
        c0, h0 = cs[1], hs[2]
        ax1 = plane([0, len(hs) - 1], [0.3, 1.0], center=LEFT * 4.2 + DOWN * 0.4, x_length=3.6, y_length=3.6,
                    xticks=list(range(len(hs))), yticks=[0.4, 0.6, 0.8, 1.0], xlabel=r"cheaper communication $\to$",
                    ylabel=r"share solved by workers", xfmt=lambda v: "", yfmt=lambda v: f"{v:.1f}", font_size=13)
        ax2 = plane([0, len(cs) - 1], [0.3, 1.0], center=LEFT * 0.2 + DOWN * 0.4, x_length=3.0, y_length=3.6,
                    xticks=list(range(len(cs))), yticks=[0.4, 0.6, 0.8, 1.0], xlabel=r"cheaper knowledge $\to$",
                    ylabel="", xfmt=lambda v: "", yfmt=lambda v: f"{v:.1f}", font_size=13)
        p1 = path(ax1, range(len(hs)), [at[(h, c0)]["worker_solves"] for h in hs], COST, 3.0, smooth=False)
        p2 = path(ax2, range(len(cs)), [at[(h0, c)]["worker_solves"] for c in cs], GAIN, 3.0, smooth=False)
        d1 = VGroup(*[dot(ax1, k, at[(h, c0)]["worker_solves"], COST, 0.06) for k, h in enumerate(hs)])
        d2 = VGroup(*[dot(ax2, k, at[(h0, c)]["worker_solves"], GAIN, 0.06) for k, c in enumerate(cs)])
        spans1 = (at[(hs[0], c0)]["span"], at[(hs[-1], c0)]["span"])
        spans2 = (at[(h0, cs[0])]["span"], at[(h0, cs[-1])]["span"])
        side = VGroup(
            label(r"communication technology \\ (email, \ networks): \ asking is cheap, \\ so workers know less and "
                  r"pass more up: \\ decisions centralize", font_size=18, color=COST),
            label(rf"span: \ {spans1[0]:.0f} $\to$ {spans1[1]:.0f} workers per manager", font_size=17, color=COST),
            label(r"information technology \\ (databases, \ design software): \\ knowing is cheap, \ so workers "
                  r"solve more: \\ decisions decentralize", font_size=18, color=GAIN),
            label(rf"span: \ {spans2[0]:.0f} $\to$ {spans2[1]:.0f}", font_size=17, color=GAIN),
            label(r"found in American and European firms \\ (Bloom, \ Garicano, \ Sadun and Van Reenen)",
                  font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 4.6:
            side.width = 4.6
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Bloom, \ Garicano, \ Sadun and Van Reenen, \ Management Science 60(12) (2014); \ "
                            r"computed: \ agora.org.hierarchy", corner=DL, font_size=12)
        with self.voiceover(
            "Now change the technology. The model separates two kinds that are usually lumped together. <bookmark "
            "mark='a'/> Communication technology, email and networks, makes asking cheap. Workers then learn less "
            "and pass more problems up: on the left, the share of problems workers solve falls as communication "
            "gets cheaper. Decisions centralize. <bookmark mark='b'/> Information technology, databases and design "
            "software, makes knowing cheap. <bookmark mark='c'/> Workers then solve more themselves, on the right, "
            "and each manager can support more of them. Decisions decentralize. <bookmark mark='d'/> Nicholas "
            "Bloom, Luis Garicano, Raffaella Sadun and John Van Reenen found exactly this split in American and "
            "European firms: information systems went with more autonomy for plant managers and workers, "
            "communication networks with less. Which matters for chapter sixteen, because a tool that answers "
            "questions is both."
        ) as vo:
            self.play(FadeIn(ax1), FadeIn(ax2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(p1), FadeIn(d1), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(p2), FadeIn(d2), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()
