from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


class Myerson(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Myerson: \ the reserve price", r"Should a seller ever refuse to sell, \ to a buyer who "
             r"values the thing more than the seller does?", "Chapter seven. Myerson: the reserve price.",
             lit={1981: r"Myerson; \ Riley and Samuelson", 1996: r"Bulow and Klemperer", 2007: r"Myerson's Nobel"},
             scale=("market",), horizon=("a day",))
        self.virtual()
        self.curve()
        self.cost()
        self.ought()

    def virtual(self):
        m = load("myerson")
        vs = np.array(m["vs"])
        ax = plane([0, 1], [-1, 1], center=LEFT * 3.0 + DOWN * 0.4, x_length=5.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[-1, -0.5, 0, 0.5, 1], xlabel=r"a bidder's value $v$",
                   font_size=16, xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
        a = ax.ax
        zero = Line(a.c2p(0, 0), a.c2p(1, 0), color=GREY_C, stroke_width=1.5)
        phi = path(ax, vs, m["virtual"], color=RESERVE, width=3.5, smooth=False)
        neg = Polygon(a.c2p(0, 0), a.c2p(0, -1), a.c2p(0.5, 0), stroke_width=0, fill_color=HOLD, fill_opacity=0.25)
        lab = label(r"virtual value \ $2v - 1$", font_size=18, color=RESERVE).move_to(a.c2p(0.3, 0.6))
        rstar = VGroup(Dot(a.c2p(0.5, 0), color=E.ACCENT, radius=0.08),
                       label(r"$r^* = \tfrac12$", font_size=20, color=E.ACCENT).next_to(a.c2p(0.5, 0), UP + LEFT,
                                                                                    buff=0.1))
        side = VGroup(
            MathTex(r"\varphi(v) = v - \frac{1 - F(v)}{f(v)}", font_size=36, color=RESERVE),
            label(r"a buyer's value, \ less what the seller must leave it \\ so that higher types don't pretend to "
                  r"be it", font_size=19, color=GREY_A),
            MathTex(r"\text{revenue} = \mathbb{E}\big[\varphi(v_{\text{winner}})\big]", font_size=34),
            label(r"so sell only when the winner's virtual value is positive: \\ never below $r^*$, \ where "
                  r"$\varphi(r^*) = 0$", font_size=20, color=E.ACCENT),
            label(r"for even values, \ $r^* = \tfrac12$, \ however many bid", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Myerson, Math.\ Oper.\ Res.\ 6(1) (1981)", corner=DR, font_size=13)
        with self.voiceover(
            "In 1981 Roger Myerson asked what the best possible auction is, for a seller who wants the most money: "
            "not the best of the four formats, but the best of every conceivable rule. <bookmark mark='a'/> His key "
            "is a bidder's virtual value: its value, less a correction. To sell to a bidder with value v, the seller "
            "must leave enough to every higher bidder that none of them pretends to be v. The correction is the cost "
            "of that. <bookmark mark='b'/> Myerson showed that a seller's expected revenue equals the expected "
            "virtual value of whoever wins. <bookmark mark='c'/> So the best auction gives the object to the "
            "bidder with the highest virtual value, and to nobody if that is negative. For values spread evenly "
            "between nothing and one, the virtual value is two v minus one, which is negative below one half. "
            "<bookmark mark='d'/> The best auction is any of the standard four, with a reserve price of one half: "
            "no sale below it. And with even values, the right reserve is one half however many bidders come."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(phi), FadeIn(lab), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(neg), FadeIn(rstar), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def curve(self):
        m = load("myerson")
        rs, rev = np.array(m["reserve"]), np.array(m["revenue"])
        ax = plane([0, 1], [0, 0.6], center=LEFT * 2.6 + DOWN * 0.35, x_length=6.6, y_length=4.8,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                   xlabel=r"the reserve price", ylabel=r"expected revenue, \ two bidders", font_size=16,
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.1f}")
        a = ax.ax
        c = path(ax, rs, rev, color=RESERVE, width=3.5)
        zero = VGroup(Dot(a.c2p(0, m["rev_zero"]), color=WHITE, radius=0.07),
                      label(rf"no reserve: \ {m['rev_zero']:.3f}", font_size=17).next_to(a.c2p(0, m["rev_zero"]),
                                                                                        DR, buff=0.15))
        best = VGroup(Dot(a.c2p(m["r_star"], m["rev_star"]), color=E.ACCENT, radius=0.08),
                      label(rf"reserve $\tfrac12$: \ {m['rev_star']:.3f}", font_size=17, color=E.ACCENT).next_to(
                          a.c2p(m["r_star"], m["rev_star"]), UP, buff=0.15))
        more = VGroup(DashedLine(a.c2p(0, m["rev_more"]), a.c2p(1, m["rev_more"]), color=SECOND, stroke_width=2.5),
                      label(rf"a third bidder, \ no reserve: \ {m['rev_more']:.2f}", font_size=17,
                            color=SECOND).next_to(a.c2p(0.75, m["rev_more"]), UP, buff=0.1))
        side = VGroup(
            label(rf"the best reserve raises revenue \\ by {m['gain'] * 100:.0f}\%: \ from a third to five twelfths",
                  font_size=21, color=RESERVE),
            label(r"but one more bidder, \ with no reserve, \\ raises it to a half", font_size=21, color=SECOND),
            label(r"Bulow and Klemperer (1996): \\ an extra bidder beats \\ the best reserve", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "How much is the reserve worth? Here is the expected revenue from two bidders, against the reserve "
            "price. <bookmark mark='a'/> With no reserve the seller expects a third. With a reserve of one half it "
            "expects five twelfths, a quarter more. <bookmark mark='b'/> Now compare one more bidder, and no reserve "
            "at all: a half. <bookmark mark='c'/> Jeremy Bulow and Paul Klemperer proved in 1996 that this is "
            "general: under the standard assumptions, one extra bidder is worth more to a seller than the cleverest "
            "reserve. Attracting bidders comes first; fine-tuning comes second."
        ) as vo:
            self.play(FadeIn(ax), Create(c), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(zero), FadeIn(best), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(more[0]), FadeIn(more[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def cost(self):
        m = load("myerson")
        rows = VGroup(
            label(rf"with two bidders and the reserve of one half, \ the canoe goes unsold "
                  rf"{m['p_no_sale'] * 100:.0f}\% of the time", font_size=24, color=RESERVE),
            label(r"though both bidders value it above the seller's nothing", font_size=24, color=HOLD),
            label(r"the reserve is a monopolist's price: \ it trades some sales for a higher price on the rest",
                  font_size=24),
            label(r"part ten's triangle, \ again: \ the optimal auction is not the efficient one", font_size=24,
                  color=GREY_A),
            label(r"and to set it, \ the seller must know the spread of values: \ chapter thirteen measures what it "
                  r"adds", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The reserve has a cost, and it falls on the buyers and on efficiency. <bookmark mark='a'/> With two "
            "bidders and a reserve of one half, the object goes unsold a quarter of the time, <bookmark mark='b'/> "
            "though both bidders value it above the seller's own value of nothing. <bookmark mark='c'/> The reserve "
            "is a monopolist's price: it gives up some sales for a higher price on the rest. "
            "<bookmark mark='d'/> That is part ten's triangle again. The auction that earns the seller the most is "
            "not the one that puts the object in the best hands. <bookmark mark='e'/> And to set the reserve the "
            "seller must know how values are spread. Chapter thirteen measures what reserves add in a real market."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def ought(self):
        io = is_ought_card(
            r"a reserve above the seller's own value raises expected revenue, \ and sometimes leaves the object with "
            r"nobody, \ or with the wrong buyer",
            r"whether a government selling the airwaves should set one, \ and how high",
            r"how much public revenue is worth, \ against licences left idle or in weaker hands; \ American law "
            r"tells the FCC not to design its auctions mainly to raise money",
            width=12.0, font_size=24).move_to(UP * 0.1)
        with self.voiceover(
            "This is a place where economics stops and a judgment begins. <bookmark mark='a'/> The theory says "
            "what a reserve does: it raises the expected revenue, and sometimes leaves the thing unsold, or with a "
            "buyer who values it less. <bookmark mark='b'/> Whether a government should use one when it sells the "
            "airwaves needs a judgment about how much a pound or a dollar of public revenue is worth, against "
            "spectrum left idle or in weaker hands. American law made that judgment one way: it tells the FCC not to "
            "design its auctions mainly to raise money. <bookmark mark='c'/> Economics measures both sides. It "
            "can't, by itself, say how to weigh them."
        ) as vo:
            self.play(FadeIn(io.card), FadeIn(io.is_row))
            vo.wait_until("b")
            self.play(FadeIn(io.judgment), FadeIn(io[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(io.ought), FadeIn(io[1][3]))
        self.clear_scene()
