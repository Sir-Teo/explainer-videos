from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403

OWNERS = ["#F2C14E", "#7EC8F5", "#7BD88F", "#F29E8E"]


class Public(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Public goods, \ and the lighthouse", r"How much of something everyone shares should be made, "
             r"\ and who will pay?", "Chapter six. Public goods, and the lighthouse.",
             lit={1919: r"Lindahl", 1954: r"Samuelson", 1974: r"Coase's lighthouse"}, scale=("community", "nation"),
             horizon=("a decade",))
        self.grid()
        self.samuelson()
        self.lighthouse()

    def grid(self):
        cells = [
            (r"private goods", r"a fish, \ a pot", r"rival, \ excludable", DEMAND),
            (r"club goods", r"a toll road, \ a streaming service", r"non-rival, \ excludable", GOOD),
            (r"common resources", r"the lagoon's fish, \ a pasture", r"rival, \ not excludable", FISH),
            (r"public goods", r"a lighthouse's beam, \ defence, \ clean air", r"non-rival, \ not excludable", POT),
        ]
        boxes = VGroup()
        for name, ex, kind, col in cells:
            box = RoundedRectangle(width=5.2, height=1.9, corner_radius=0.12, stroke_color=col, stroke_width=2.5,
                                   fill_color=col, fill_opacity=0.07)
            t = VGroup(label(name, font_size=26, color=col), label(ex, font_size=20), label(kind, font_size=18,
                                                                                            color=GREY_B)
                       ).arrange(DOWN, buff=0.12).move_to(box)
            boxes.add(VGroup(box, t))
        boxes.arrange_in_grid(rows=2, cols=2, buff=0.25).move_to(DOWN * 0.3 + RIGHT * 0.6)
        top = VGroup(label(r"excludable", font_size=20, color=GREY_A), label(r"not excludable", font_size=20,
                                                                              color=GREY_A))
        top[0].next_to(boxes[0], UP, buff=0.15)
        top[1].next_to(boxes[1], UP, buff=0.15)
        left = VGroup(label(r"rival", font_size=20, color=GREY_A), label(r"non-rival", font_size=20, color=GREY_A))
        left[0].next_to(boxes[0], LEFT, buff=0.2)
        left[1].next_to(boxes[2], LEFT, buff=0.2)
        # rearrange so rows are rival/non-rival and columns excludable/not
        order = [0, 2, 1, 3]
        boxes2 = VGroup(*[boxes[k] for k in order]).arrange_in_grid(rows=2, cols=2, buff=0.25).move_to(
            DOWN * 0.3 + RIGHT * 0.6)
        top[0].next_to(boxes2[0], UP, buff=0.15)
        top[1].next_to(boxes2[1], UP, buff=0.15)
        left[0].next_to(boxes2[0], LEFT, buff=0.2)
        left[1].next_to(boxes2[2], LEFT, buff=0.2)
        with self.voiceover(
            "A public good is the spillover taken to its limit. Two questions sort every good. "
            "<bookmark mark='a'/> Is it rival: does my use leave less for you? And is it excludable: can someone who "
            "doesn't pay be kept from using it? <bookmark mark='b'/> A fish or a pot is both: a private good, and "
            "markets handle it well. <bookmark mark='c'/> The lagoon's fish are rival but hard to fence off: a "
            "common resource, chapter eight's subject. <bookmark mark='d'/> A toll road or a streaming service is "
            "non-rival, at least until it's crowded, but a gate keeps non-payers out: a club good. "
            "<bookmark mark='e'/> And a lighthouse's beam, a country's defence or clean air are neither rival nor "
            "excludable: public goods. Every ship sees the light, and no ship's seeing it dims it for another."
        ) as vo:
            self.play(FadeIn(top), FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(boxes2[0]))
            vo.wait_until("c")
            self.play(FadeIn(boxes2[1]))
            vo.wait_until("d")
            self.play(FadeIn(boxes2[2]))
            vo.wait_until("e")
            self.play(FadeIn(boxes2[3]))
        self.clear_scene()

    def samuelson(self):
        lh = load("lighthouse")
        gs = np.array(lh["gs"])
        ax = plane([0, 14], [0, 10.5], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.4, y_length=4.6,
                   xticks=[0, 3, 6, 9, 12], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"hours of light a night",
                   ylabel=r"value of one more hour", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        mbs = VGroup(*[path(ax, gs, mb, color=c, width=2.5) for mb, c in zip(lh["mbs"], OWNERS)])
        tot = path(ax, gs, lh["sum_mb"], color=WHITE, width=3.5)
        mc = seg(ax, 0, lh["mc"], 14, lh["mc"], color=SOCIAL, width=2.5)
        mcl = label(r"cost of an hour", font_size=15, color=SOCIAL).next_to(a.c2p(13.5, lh["mc"]), UP, buff=0.08,
                                                                          aligned_edge=RIGHT)
        totl = label(r"the four values added", font_size=15, color=WHITE).next_to(a.c2p(2.3, lh["sum_mb"][23]), UR,
                                                                                buff=0.05)
        gstar = Dot(a.c2p(lh["g_star"], lh["mc"]), radius=0.09, color=E.ACCENT)
        gnash = Dot(a.c2p(lh["g_nash"], lh["mc"]), radius=0.09, color=OWNERS[0])
        side = VGroup(
            label(r"four ship-owners, \ each valuing the light \\ (the coloured curves)", font_size=21),
            label(r"everyone sees every hour: \\ add the values up, \ not across", font_size=21, color=WHITE),
            label(rf"Samuelson's rule: \ the sum equals the cost \\ at {lh['g_star']:.0f} hours", font_size=21,
                  color=E.ACCENT),
            label(rf"left to themselves, \ only the keenest pays: \\ {lh['g_nash']:.0f} hours, \ and the rest ride free",
                  font_size=21, color=OWNERS[0]),
            label(r"Lindahl's prices: \ charge each their own value's share \\ (40, 30, 20, 10\%), \ and all agree on 9",
                  font_size=21, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Samuelson, REStat 36(4) (1954); \ Lindahl (1919); \ the curves: \ Agora", corner=DR,
                            font_size=13)
        with self.voiceover(
            "How much of a public good should be made? Take a lighthouse on the island, and four ship-owners who "
            "value its light. <bookmark mark='a'/> Each coloured curve is what one more hour of light a night is "
            "worth to one owner. <bookmark mark='b'/> Every owner sees every hour, so to find what an hour is worth "
            "to all of them, add their values up, one on top of another, not side by side as for fish. "
            "<bookmark mark='c'/> Paul Samuelson's rule, from 1954: provide the good until the sum of everyone's "
            "values equals its cost. Here, nine hours. <bookmark mark='d'/> Left to pay voluntarily, each owner "
            "weighs only their own value. Only the keenest pays at all, for three hours, and the others ride free on "
            "the light. <bookmark mark='e'/> Erik Lindahl's answer, from 1919, was to charge each owner a share equal "
            "to their share of the value: forty, thirty, twenty and ten percent. At those prices all four ask for "
            "nine hours. The catch is that each owner gains by understating their value, which is the free rider "
            "again."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(mc), FadeIn(mcl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(m) for m in mbs], lag_ratio=0.3), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(tot), FadeIn(totl), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(gstar, scale=1.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(gnash, scale=1.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def lighthouse(self):
        rows = VGroup(
            label(r"the lighthouse: \ the textbooks' public good, \ from Mill to Samuelson", font_size=25,
                  color=POT),
            label(r"Ronald Coase, \ 1974: \ many of Britain's lighthouses were built and run privately", font_size=23),
            label(r"paid for by light dues, \ collected from ships in port", font_size=23, color=GOOD),
            label(r"the trick: \ the light was free, \ but the harbour was not", font_size=24, color=E.ACCENT),
            label(r"critics: \ the dues were set and enforced by the state, \ under patents from the Crown",
                  font_size=22, color=GREY_A),
            label(r"both are right: \ private provision of a public good needs a way to exclude, \ and often a state",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.34).move_to(UP * 0.1)
        tag = published_tag(r"Coase, JLE 17(2) (1974); \ Van Zandt, JLS 22(1) (1993); \ Bertrand, CJE 30(3) (2006)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "The lighthouse has a history of its own. <bookmark mark='a'/> From John Stuart Mill to Samuelson, it was "
            "the textbook's example of a good that only a government could provide. <bookmark mark='b'/> In 1974 "
            "Coase went to the records and found that many of Britain's lighthouses had been built and run by "
            "private owners. <bookmark mark='c'/> They were paid for with light dues, collected from ships when they "
            "came into port. <bookmark mark='d'/> The trick was a tie: the light could not be withheld, but the "
            "harbour could. <bookmark mark='e'/> Later historians pointed out that the dues were set by the state and "
            "enforced by it, under patents from the Crown. <bookmark mark='f'/> Both sides are right, and together "
            "they make the lesson: private provision of a public good needs some way to exclude those who don't "
            "pay, and the way is often lent by a state."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
