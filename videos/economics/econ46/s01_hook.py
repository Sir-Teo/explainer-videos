from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.nets()
        self.island()
        self.question()
        self.title()
        self.objectives()

    def nets(self):
        T = tables.COHEN_DUPAS_2010.data
        chain = flow_chain([(r"a bed net, \\ treated with \\ insecticide", HEALTH),
                            (r"give it away, \\ or sell it \\ cheaply?", POOR),
                            (rf"{T['clinics']} clinics, \\ prices drawn \\ at random", TRIAL)],
                           notes=[r"a few dollars; \\ prevents malaria", r"who would take it? \\ who would use it?",
                                  rf"from free to {T['price_ksh']} \\ shillings, \ about \\ 60 cents"],
                           box_w=3.2, font_size=23, note_size=18)
        chain.move_to(UP * 1.25)
        sides = VGroup(
            VGroup(label(r"for a price", font_size=22, color=POOR),
                   label(r"people who pay \\ value it, \ and will \\ use it", font_size=19, color=GREY_A)
                   ).arrange(DOWN, buff=0.12),
            VGroup(label(r"for free", font_size=22, color=HEALTH),
                   label(r"more people covered, \\ and a net used by one \\ protects the neighbours", font_size=19,
                         color=GREY_A)).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=2.2).move_to(DOWN * 1.9)
        result = label(rf"demand fell by about {T['drop']}\% \ at 60 cents; \ those who paid \\ used their nets no "
                       r"more than those who did not", font_size=22, color=E.ACCENT).move_to(DOWN * 1.9)
        tag = published_tag(tables.COHEN_DUPAS_2010.tag, corner=DR, font_size=11)
        with self.voiceover(
            "A bed net treated with insecticide costs a few dollars, and a child who sleeps under one is far less "
            "likely to catch malaria. <bookmark mark='a'/> For years donors argued over how to hand them out. "
            "<bookmark mark='b'/> One side said: sell them, cheaply. People who pay for a net are people who value "
            "it, and they will hang it up and use it; a free net may end up as a fishing net. <bookmark mark='c'/> "
            "The other side said: give them away. More people will be covered, and a net protects the neighbours "
            "too, because it kills the mosquitoes. <bookmark mark='d'/> In Kenya, Jessica Cohen and Pascaline Dupas "
            f"settled it with an experiment. At {T['clinics']} prenatal clinics, they drew the price at random, from "
            f"free up to {T['price_ksh']} shillings, about sixty cents. <bookmark mark='e'/> At sixty cents, demand "
            f"fell by about {T['drop']} percent. And the women who paid were no more likely to use their nets than "
            "the women who got one free."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]), FadeIn(chain.notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(sides[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(sides[1], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]), FadeIn(chain.notes[2]))
            vo.wait_until("e")
            self.play(FadeOut(sides), FadeIn(result, shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        N = load("nets")
        S = N["screening"]
        prices = N["price"]
        ax = plane([-0.5, 4.5], [0, 1], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.0, y_length=4.6, xticks=[],
                   yticks=[0, 0.25, 0.5, 0.75, 1.0], ylabel=r"share of mothers", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        take, use, sus = VGroup(), VGroup(), VGroup()
        for i, p in enumerate(prices):
            for grp, val, col, dx in ((take, N["take"][i], POOR, -0.18), (use, N["protected"][i], HEALTH, 0.18)):
                p0, p1 = ax.ax.c2p(i + dx - 0.16, 0), ax.ax.c2p(i + dx + 0.16, val)
                grp.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                  fill_opacity=0.85).move_to((p0 + p1) / 2))
            sus.add(label(r"free" if p == 0 else rf"{100 * p:.0f} cents", font_size=15,
                          color=WHITE).next_to(ax.ax.c2p(i, 0), DOWN, buff=0.12))
        side = VGroup(
            label(r"the Island's clinic: \\ the price drawn \\ at random", font_size=19, color=WHITE),
            label(r"gold: \ took a net", font_size=19, color=POOR),
            label(r"green: \ took one \\ and slept under it", font_size=19, color=HEALTH),
            label(rf"of those who took one, \\ {100 * N['use_if_taken'][0]:.0f}\% use it \\ at every price",
                  font_size=19,
                  color=GREY_A),
            label(rf"if paying screened \\ for use: \ {100 * S['use_if_taken'][0]:.0f}\% free, \\ "
                  rf"{100 * S['use_if_taken'][-1]:.0f}\% at 60 cents", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island runs the same experiment at its own clinic. <bookmark mark='a'/> In gold, the share of "
            "mothers who take a net at each price. Free, nearly all of them. At sixty cents, "
            f"{100 * N['take'][-1]:.0f} percent: a fall of {100 * N['drop']:.0f} percent, as in Kenya. "
            "<bookmark mark='b'/> In green, the share who take a net and sleep under it. Of those who take one, "
            f"{100 * N['use_if_taken'][0]:.0f} percent use it, whatever they paid. <bookmark mark='c'/> So charging "
            "does not pick out the users; it just leaves fewer people protected. <bookmark mark='d'/> If paying had "
            "screened for use, the share using their nets would rise with the price, from "
            f"{100 * S['use_if_taken'][0]:.0f} to {100 * S['use_if_taken'][-1]:.0f} percent. That is the question "
            "the experiment answered, and the answer is in the data, not in the argument."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(sus), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in take], lag_ratio=0.2), FadeIn(side[1]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in use], lag_ratio=0.2), FadeIn(side[2]),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"who is poor, \ and how would we count them?", font_size=26, color=POOR),
            label(r"is poverty a trap, \ or a slow start?", font_size=26, color=TRAP),
            label(r"which markets fail the poor: \ credit, \ insurance, \ land, \ labour?", font_size=26,
                  color=CREDIT),
            label(r"what do cash, \ schools, \ medicine and loans actually do, \ and how do we know?", font_size=26,
                  color=TRIAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "This part asks why the poor stay poor, and what actually helps. <bookmark mark='a'/> Who is poor, and "
            "how would we count them across a world of different prices? <bookmark mark='b'/> Is poverty a trap, "
            "from which people cannot climb out on their own, or only a slow start? <bookmark mark='c'/> Which "
            "markets fail the poor, and why: credit, insurance, land and labour? <bookmark mark='d'/> And what do "
            "cash, schools, medicine and loans actually do, and how could anyone know?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1981, 2024], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, POOR, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 46 \ $\cdot$ \ Development", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part forty-six: development."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IX \ $\cdot$ \ The Fields", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"counting the poor; \ an aid budget to spend; \ poverty traps",
            r"farm and town; \ credit, \ cash, \ and a programme for the poorest",
            r"schools, \ health, \ risk, \ farms and phones; \ history that persists",
            r"the debate over experiments, \ with real data from four of them",
            r"three dials; \ the people who use this; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> How the world counts its poor, an aid budget for you to spend, "
            "and whether poverty is a trap. <bookmark mark='b'/> The farm and the town; what credit and cash do, "
            "and a programme built for the very poorest. <bookmark mark='c'/> Schools, health, risk, fertilizer "
            "and mobile money, and history that is still visible in today's incomes. <bookmark mark='d'/> The "
            "debate over what experiments can teach, with real data from four of them. <bookmark mark='e'/> Three "
            "dials, the people who use these ideas, and the frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
