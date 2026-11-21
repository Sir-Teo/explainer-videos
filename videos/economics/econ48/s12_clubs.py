from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Clubs(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Leakage, \ borders and clubs", r"How do you get the world to join?",
             "Chapter ten. Leakage, borders and clubs.", lit={2015: r"Nordhaus's clubs", 2023: r"the EU's CBAM"},
             scale=("nation", "world"), horizon=("a decade",))
        self.leakage()
        self.club()

    def leakage(self):
        T = tables.INSTRUMENTS_48.data
        chain = flow_chain([(r"one country \\ prices carbon", POLICY), (r"its steel and \\ cement cost more", LOSS),
                            (r"production moves \\ to countries \\ that do not", LOSS), (r"a border \\ adjustment",
                                                                                         GAIN)],
                           notes=[r"its emissions fall", r"against importers", r"leakage: \ emissions \\ just move",
                                  r"charge imports \\ for their carbon"],
                           box_w=2.8, font_size=20, note_size=16).move_to(UP * 1.2)
        cbam = VGroup(
            label(r"the EU's Carbon Border Adjustment Mechanism", font_size=23, color=GAIN),
            label(rf"importers report embedded emissions from October {T['cbam_report']}, \ and pay from "
                  rf"January {T['cbam_pay']}", font_size=20, color=WHITE),
            label(r"cement, \ aluminium, \ fertilisers, \ iron and steel, \ hydrogen, \ electricity", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.85)
        tag = published_tag(tables.INSTRUMENTS_48.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Climate is a global public good, Part fifteen's problem on the scale of the planet. Every country gains "
            "from the others' cuts and pays alone for its own. <bookmark mark='a'/> Suppose one country prices "
            "carbon. <bookmark mark='b'/> Its steel and cement now cost more to make than its rivals'. <bookmark "
            "mark='c'/> Some production moves to countries without a price, and the emissions with it: leakage. "
            "<bookmark mark='d'/> The answer on offer is a border adjustment: charge imports for the carbon emitted "
            "in making them, as if they had been made at home. <bookmark mark='e'/> The European Union has built "
            f"one. Importers began reporting the emissions in their goods in October {T['cbam_report']}, <bookmark "
            f"mark='f'/> and from January {T['cbam_pay']} they pay for them, <bookmark mark='g'/> for cement, "
            "aluminium, fertilisers, iron and steel, hydrogen and electricity. A border adjustment protects a "
            "country's own carbon price. It also does something more: it gives other countries a reason to price "
            "carbon themselves."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            for mk, r_ in zip("efg", cbam):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def club(self):
        C = load("club")
        Tc = TRUTH["club"]
        tr = np.array(C["tariff"])
        ax = plane([0, 0.12], [0, Tc["n"] + 1], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.4, y_length=4.6,
                   xticks=[0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12], yticks=[0, 5, 10, 15],
                   xlabel=r"the club's penalty tariff on non-members", ylabel=r"members of the stable club",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.0f}", font_size=14)
        steps = VMobject(stroke_color=GAIN, stroke_width=3.4)
        pts = []
        for i in range(len(tr)):
            x2 = tr[i + 1] if i + 1 < len(tr) else 0.12
            pts += [ax.ax.c2p(tr[i], C["members"][i]), ax.ax.c2p(x2, C["members"][i])]
        steps.set_points_as_corners(pts)
        side = VGroup(
            label(rf"{Tc['n']} countries of different \\ sizes; \ cutting costs \\ about 1\% of output; \\ the "
                  r"damage avoided is \\ about 3\% if all cut", font_size=17, color=WHITE),
            label(r"no tariff: \ each country's \\ own share of the gain \\ is too small: \ nobody \\ stays",
                  font_size=17, color=LOSS),
            label(rf"a tariff of {100 * C['first']:.0f}\%: \ {C['members'][list(tr).index(C['first'])]} join; "
                  rf"\\ {100 * C['full']:.0f}\%: \ all {Tc['n']}", font_size=18, color=GAIN),
            label(r"Nordhaus, \ 2015: \ without \\ sanctions, \ only clubs \\ that do little are stable", font_size=17,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "William Nordhaus took the idea further: a climate club. <bookmark mark='a'/> Fifteen Island countries "
            "of different sizes. Cutting emissions costs each about one percent of its output; if the whole world "
            "cuts, each avoids damage worth about three percent. Everyone would gain if all cut. <bookmark "
            "mark='b'/> But each country gains only the part of the benefit its own cuts bring, which for any "
            "single country is too small. Start with everyone in the club, let countries leave whenever leaving "
            "pays, and with no penalty the club unravels to nobody. <bookmark mark='c'/> Now let members charge "
            "a uniform tariff on imports from non-members. Leaving now costs something. At "
            f"{100 * C['first']:.0f} percent, {C['members'][list(tr).index(C['first'])]} countries stay; at "
            f"{100 * C['full']:.0f} percent, all {Tc['n']}. <bookmark mark='d'/> Nordhaus found the same in a "
            "far richer model: without sanctions on non-participants, the only stable coalitions are those that "
            "cut very little. The Kyoto Protocol, which had no sanctions, lost its members; a club with a penalty "
            "can hold together."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("b")
            self.play(Create(steps), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
