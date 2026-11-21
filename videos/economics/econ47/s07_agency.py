from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Agency(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Politicians as agents", r"Can elections stop politicians from taking what they can?",
             "Chapter six. Politicians as agents.", lit={1973: r"Barro", 1986: r"Ferejohn", 2011: r"Ferraz and Finan"},
             scale=("town", "nation"), horizon=("a term",))
        self.model()
        self.threshold()
        self.mayors()

    def model(self):
        chain = flow_chain([(r"voters hire \\ a politician", VOTER), (r"who could \\ take rents", POL),
                            (r"re-elected only if \\ rents stay small", VOTER), (r"office must be \\ worth keeping",
                                                                                 E.ACCENT)],
                           notes=[r"they cannot \\ watch everything", r"up to $R$ \\ a term", r"a threshold $r^*$",
                                  r"the value of \\ the next terms"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 1.1)
        eq = MathTex(r"\frac{W + r^*}{1-\delta} \;\ge\; W + R \quad\Longrightarrow\quad r^* = (1-\delta)(W+R) - W",
                     font_size=34, color=THEORY).to_edge(DOWN, buff=1.5)
        el = label(r"$W$: \ what a term in office is worth; \ $\delta$: \ how much the future counts; \ a lame duck "
                   r"takes $R$", font_size=19, color=GREY_A).next_to(eq, DOWN, buff=0.25)
        tag = published_tag(tables.AGENCY_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Robert Barro in 1973 and John Ferejohn in 1986 treated politicians as agents of the voters, like the "
            "managers of Part fourteen. <bookmark mark='a'/> Voters hire a politician, but cannot watch everything "
            "they do. <bookmark mark='b'/> In office, the politician could take rents, up to some amount R a term, "
            "by graft, favours or slacking. <bookmark mark='c'/> Voters re-elect only if rents stay below a "
            "threshold. <bookmark mark='d'/> The politician complies if keeping office, term after term, is worth "
            "more than one big grab followed by defeat. <bookmark mark='e'/> So the lowest threshold voters can "
            "enforce is one minus delta, times W plus R, minus W: smaller when office pays well and when the "
            "future counts. And a politician who cannot run again, a lame duck, has nothing to lose, and takes R."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(Write(eq), FadeIn(el), run_time=2.0)
        self.clear_scene()

    def threshold(self):
        ax = plane([0, 1.0], [0, 1.0], center=LEFT * 2.0 + DOWN * 0.35, x_length=6.6, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"what a term in office is worth, \ $W$", ylabel=r"rents voters must tolerate, \ $r^*/R$",
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        Ws = np.linspace(0, 1, 101)
        curves = VGroup()
        cols = (LOSS, POL, AUDIT)
        for d, col in zip((0.3, 0.5, 0.7), cols):
            r = [politics.agency(w, 1.0, d)["share_taken"] for w in Ws]
            curves.add(path(ax, Ws, r, col, 3.0, smooth=False))
        labs = VGroup(*[label(rf"$\delta$ = {d}", font_size=16, color=c) for d, c in zip((0.3, 0.5, 0.7), cols)])
        side = VGroup(
            label(r"rents of up to 1 a term", font_size=18, color=WHITE),
            labs.arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            label(r"pay politicians more, \\ or make them value \\ the future, \ and the \\ tolerated rents fall",
                  font_size=18,
                  color=E.ACCENT),
            label(r"Part 14's efficiency wage, \\ for the state", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the threshold, for rents of up to one a term. <bookmark mark='a'/> Across, what a term in "
            "office is worth to the politician; up the side, the rents voters must tolerate to keep them honest. "
            "<bookmark mark='b'/> The three lines are politicians who weigh the future less or more. <bookmark "
            "mark='c'/> The more office pays, and the more the future counts, the less voters have to tolerate, "
            "until it reaches zero. <bookmark mark='d'/> It is Part fourteen's efficiency wage, applied to the "
            "state: a job worth keeping is a job not worth risking."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(curves[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(curves[0]), Create(curves[2]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def mayors(self):
        M = load("mayors")
        T = tables.AGENCY_47.data
        ax = plane([0, 2], [0, 0.05], center=LEFT * 2.6 + DOWN * 0.4, x_length=4.6, y_length=4.4, xticks=[],
                   yticks=[0, 0.01, 0.02, 0.03, 0.04, 0.05], ylabel=r"share of audited spending misappropriated",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        bars = VGroup()
        for i, (nm, v, col) in enumerate(((r"can run \\ again", M["first_term"], AUDIT),
                                          (r"barred: \\ a lame duck", M["lame_duck"], CORRUPT))):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=15, color=WHITE).next_to(r, DOWN, buff=0.1),
                            label(rf"{100 * v:.1f}\%", font_size=17, color=WHITE).next_to(r, UP, buff=0.06)))
        side = VGroup(
            label(rf"the Island: \ {TRUTH['mayors']['n']:,} towns, \\ mayors who differ \\ in what office is worth \\ "
                  r"and in honesty".replace(",", "{,}"), font_size=18, color=WHITE),
            label(rf"first-term mayors take \\ {100 * M['fewer']:.0f}\% less", font_size=19, color=AUDIT),
            label(rf"Brazil's random audits: \\ mayors who could run \\ again took {T['fewer']}\% less", font_size=19,
                  color=E.ACCENT),
            label(r"a 2025 replication: \\ smaller, \ and near zero \\ in later terms", font_size=17, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The model predicts that lame ducks steal more. <bookmark mark='a'/> On the Island, "
            f"{TRUTH['mayors']['n']:,} towns have mayors who differ in how much they value office and in honesty. "
            "First-term mayors can run again; second-term mayors are barred. <bookmark mark='b'/> Audits find that "
            f"first-term mayors misappropriate {100 * M['fewer']:.0f} percent less. <bookmark mark='c'/> Brazil "
            "ran this experiment for real. Its federal government audited municipal spending in towns chosen by "
            "lottery, and mayors were limited to two terms. Claudio Ferraz and Frederico Finan found that mayors "
            f"who could run again misappropriated {T['fewer']} percent less than mayors in their last term. "
            "<bookmark mark='d'/> A replication published in 2025, with more years of audits, finds a smaller "
            "effect for the same period, and almost none in later terms. Accountability works, but less reliably "
            "than the first study suggested."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), *[FadeIn(b[1]) for b in bars], run_time=1.0)
            vo.wait_until("a")
            self.play(Indicate(side[0], color=WHITE))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in bars], *[FadeIn(b[2]) for b in bars], FadeIn(side[1]),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
