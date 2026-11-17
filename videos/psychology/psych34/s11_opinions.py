from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403


def opinion_color(x: float):
    return interpolate_color(ManimColor(CROWD), ManimColor(PERSON), float(np.clip(x, 0, 1)))


def ring_points(n: int, r: float, center) -> np.ndarray:
    a = np.pi / 2 - 2 * np.pi * np.arange(n) / n
    return np.column_stack([center[0] + r * np.cos(a), center[1] + r * np.sin(a), np.zeros(n)])


def network(edges, pts, color=GREY_D, width=1.0) -> VGroup:
    return VGroup(*[Line(pts[i], pts[j], color=color, stroke_width=width) for i, j in edges])


class Opinions(VoiceoverScene):
    def construct(self):
        self.card()
        self.degroot()
        self.camps()
        self.contagion()
        self.reach()

    def card(self):
        card = chapter_card(10, r"Opinions on a network", r"When do people agree, \ and what spreads?",
                            lit={1974: r"DeGroot", 2002: r"Hegselmann \& Krause", 2010: r"Centola"}, part=PART,
                            scale=("group", "society"), marr=("what", "how"))
        with self.voiceover("Chapter ten. Opinions on a network."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def degroot(self):
        d = load("degroot")
        W, path = np.asarray(d["W"]), np.asarray(d["path"])
        head = heading(r"Listening and averaging")
        pts = ring_points(5, 1.5, [-4.9, 0.2])
        links = VGroup()
        for i in range(5):
            for j in range(i + 1, 5):
                w = W[i, j] + W[j, i]
                if w > 0:
                    links.add(Line(pts[i], pts[j], color=GREY_B, stroke_width=2 + 10 * w, stroke_opacity=0.6))
        nodes = VGroup(*[Circle(radius=0.3, stroke_width=2, stroke_color=WHITE, fill_color=opinion_color(path[0, i]),
                                fill_opacity=1).move_to(pts[i]) for i in range(5)])
        A = axes([0, 30], [0, 1.0], x_length=3.9, y_length=3.4, xticks=[0, 10, 20, 30], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"round", ylabel=r"opinion",
                 center=[-0.4, 0.0, 0], font_size=14)
        lines = VGroup(*[curve(A.ax, np.arange(len(path)), path[:, i], opinion_color(path[0, i]), stroke_width=3)
                         for i in range(5)])
        mean = DashedLine(A.ax.c2p(0, d["plain_mean"]), A.ax.c2p(30, d["plain_mean"]), color=GREY_B, stroke_width=2)
        rows = rows_of([
            (r"DeGroot, \ 1974: \ each round, \ everyone replaces their opinion with a weighted average of the "
             r"opinions of those they listen to", WHITE),
            (rf"if everyone is connected, \ they reach one opinion: \ here {d['consensus']:.2f}, \ not the plain "
             rf"average, \ {d['plain_mean']:.2f}", PERSON),
            (rf"the consensus weights each person by how much the others listen to them, \ the matrix's left "
             rf"eigenvector: \ the middle person counts {d['weights'][2]:.2f}", MODEL),
        ], 4.3, 18, 0.3).move_to([4.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{social.degroot, \ influence\_weights}")
        with self.voiceover(
            "The simplest model of influence is just averaging. <bookmark mark='a'/> In 1974 the statistician "
            "DeGroot proposed that in each round, everyone replaces their opinion with a weighted average of "
            "the opinions of the people they listen to. The thicker the line, the more two people listen to each "
            "other. <bookmark mark='b'/> If everyone is connected, they reach one opinion. Here it's "
            f"{d['consensus']:.2f}, not the plain average of {d['plain_mean']:.2f}. <bookmark mark='c'/> The "
            "consensus counts each person by how much the others listen to them, which is the matrix's left "
            f"eigenvector. The person in the middle, whom everyone hears, counts for {d['weights'][2]:.2f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(links), FadeIn(nodes), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            steps = [1, 2, 3, 5, 8, 12, 30]
            self.play(Create(lines), Create(mean), FadeIn(rows[1]), run_time=2.5)
            for k in steps:
                self.play(*[nodes[i].animate.set_fill(opinion_color(path[k, i])) for i in range(5)], run_time=0.35)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(nodes[2], color=PERSON))
        self.clear_scene()

    def camps(self):
        d = load("camps")
        head = heading(r"Listening only to the near")
        panels = VGroup()
        for k, (e, nm) in enumerate(((5, r"$\varepsilon = 0.05$"), (12, r"$\varepsilon = 0.12$"),
                                     (30, r"$\varepsilon = 0.30$"))):
            p = np.asarray(d[f"path_{e}"])
            A = axes([0, 20], [0, 1.0], x_length=3.6, y_length=2.9, xticks=[0, 10, 20], yticks=[0, 0.5, 1.0],
                     xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"round",
                     ylabel=r"opinion" if k == 0 else "", center=[-4.4 + 4.3 * k, 0.7, 0], font_size=13)
            tr = VGroup(*[curve(A.ax, np.arange(len(p)), p[:, i], opinion_color(p[0, i]), stroke_width=1.4)
                          for i in range(p.shape[1])])
            cap = label(rf"{nm}: \ {int(d[f'camps_{e}'])} camp" + ("s" if int(d[f"camps_{e}"]) != 1 else ""),
                        font_size=20, color=WHITE).next_to(A, UP, buff=0.15)
            panels.add(VGroup(A, tr, cap))
        rows = rows_of([
            (r"Hegselmann and Krause, \ 2002: \ people average only the opinions within a distance $\varepsilon$ of "
             r"their own", WHITE),
            (r"narrow confidence leaves several camps that never meet, \ about $1/(2\varepsilon)$ of them; \ wide "
             r"confidence ends in one", PERSON),
            (r"nobody in a camp is stubborn or irrational: \ polarization can come from who listens to whom", YOU),
        ], 12.4, 20, 0.26).move_to([0, -2.45, 0])
        tag = psyche_tag(r"\texttt{social.bounded\_confidence}")
        with self.voiceover(
            "But people don't listen to everyone. <bookmark mark='a'/> In 2002 Rainer Hegselmann and Ulrich Krause "
            "studied people who average only the opinions within some distance of their own. Sixty people start "
            "spread across the range. <bookmark mark='b'/> With narrow confidence, they settle into several camps "
            "that never meet again, roughly one over twice the distance of them. With wide confidence, everyone "
            "ends in one. <bookmark mark='c'/> Nobody in those camps is stubborn or irrational. Polarization can "
            "come from nothing more than who listens to whom."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(pn[0]) for pn in panels])
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[Create(pn[1]) for pn in panels], *[FadeIn(pn[2]) for pn in panels], FadeIn(rows[1]),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def contagion(self):
        d = load("contagion")
        head = heading(r"Simple and complex contagion")
        pl = ring_points(60, 1.75, [-3.4, 0.55])
        pr = ring_points(60, 1.75, [3.4, 0.55])
        netl, netr = network(d["edges_l"], pl), network(d["edges_r"], pr, width=0.7)
        dots_l = VGroup(*[Dot(pl[i], radius=0.07, color=OFF) for i in range(60)])
        dots_r = VGroup(*[Dot(pr[i], radius=0.07, color=OFF) for i in range(60)])
        caps = VGroup(label(r"clustered: \ ties to near neighbours", font_size=20, color=GOOD).next_to(netl, UP, buff=0.2),
                      label(r"rewired: \ the same number of ties, \ at random", font_size=20,
                            color=CROWD).next_to(netr, UP, buff=0.2))
        rows = rows_of([
            (r"a simple contagion, \ like news, \ needs one contact; \ a complex one, \ like a costly new habit, \ "
             r"needs two who have adopted it", WHITE),
            (r"complex contagion: \ the clustered ring fills, \ neighbour by neighbour; \ in the rewired network "
             r"the first four never reach a second contact", PERSON),
            (r"Centola's online experiment, \ 2010: \ 1{,}528 people; \ joining a health forum spread further and "
             r"faster in clustered networks than in random ones", GOOD),
        ], 12.4, 20, 0.26).move_to([0, -2.6, 0])
        tag = psyche_tag(r"\texttt{social.contagion, \ rewire}")
        wl, wr = np.asarray(d["when_l2"]), np.asarray(d["when_r2"])
        T = int(max(wl.max(), wr.max()))
        with self.voiceover(
            "Opinions are one thing that spreads; behaviours are another. <bookmark mark='a'/> A simple contagion, "
            "like a piece of news, needs only one contact to pass. A complex contagion, like a costly new habit, "
            "needs reinforcement: here, two neighbours who've already adopted it. On the left, sixty people tied to "
            "their nearest neighbours. On the right, the same sixty with the same number of ties, rewired at "
            "random. <bookmark mark='b'/> Seed four neighbours with a complex contagion. On the clustered ring it "
            "fills, neighbour by neighbour. In the random network the first four never give anyone a second "
            "contact, and it stops. <bookmark mark='c'/> In 2010 Damon Centola ran this as an online experiment "
            "with fifteen hundred people and an invitation to join a health forum. It spread further and faster in "
            "the clustered networks than in the random ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(netl), FadeIn(netr), FadeIn(dots_l), FadeIn(dots_r),
                      FadeIn(caps))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            for t in range(T + 1):
                anims = [dots_l[i].animate.set_color(PERSON) for i in range(60) if wl[i] == t]
                anims += [dots_r[i].animate.set_color(PERSON) for i in range(60) if wr[i] == t]
                if anims:
                    self.play(*anims, run_time=0.25)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def reach(self):
        d = load("contagion")
        head = heading(r"How much randomness kills a complex contagion?")
        q, r = np.asarray(d["q"]), np.asarray(d["reach"])
        names = [f"{100 * v:g}\\%" for v in q]
        A = axes([-0.5, len(q) - 0.5], [0, 1.05], x_length=6.0, y_length=3.6, xticks=list(range(len(q))),
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], xfmt=lambda v: names[int(round(v))], yfmt=lambda v: f"{v:g}",
                 xlabel=r"share of ties rewired", ylabel=r"share reached", center=[-2.9, -0.4, 0], font_size=13)
        xs = np.arange(len(q))
        c = VGroup(curve(A.ax, xs, r, PERSON, stroke_width=4), scatter(A.ax, xs, r, PERSON, radius=0.06))
        p1, p2 = np.asarray(d["path_l1"]), np.asarray(d["path_r1"])
        rows = rows_of([
            (r"a ring of 400, \ complex contagion, \ eight rewirings at each level", WHITE),
            (rf"rewire 1\% of the ties and the reach falls from everyone to {pct(r[1])}: \ a few shortcuts break "
             r"the wide bridges a complex contagion needs", PERSON),
            (rf"a simple contagion does the opposite: \ it reaches all 400 in {len(p2) - 1} steps on the rewired "
             rf"network and {len(p1) - 1} on the ring", CROWD),
            (r"so the shortcuts that spread news fast can stop behaviour from spreading at all", YOU),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.contagion}")
        with self.voiceover(
            "How much randomness does it take? <bookmark mark='a'/> Here's a ring of four hundred, with a complex "
            "contagion, rewired by different amounts. <bookmark mark='b'/> Rewire one percent of the ties, and "
            f"the reach falls from everyone to about {spct(r[1])}. A few shortcuts break the wide bridges a complex "
            "contagion needs. <bookmark mark='c'/> A simple contagion does the opposite. It reaches all four "
            f"hundred in {len(p2) - 1} steps on the rewired network, and takes {len(p1) - 1} on the ring. "
            "<bookmark mark='d'/> So the shortcuts that spread news fast can stop a behaviour from spreading at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c[0]), FadeIn(c[1]), FadeIn(rows[1]))
            for m, rr in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(rr, shift=RIGHT * 0.15))
        self.clear_scene()
