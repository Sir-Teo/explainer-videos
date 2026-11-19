from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


class Shading(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Shading in a first-price auction", r"When you pay your own bid, \ how far below your value "
             r"should you bid?", "Chapter four. Shading in a first-price auction.",
             lit={1961: r"Vickrey", 1982: r"Milgrom and Weber"}, scale=("person",), horizon=("a day",))
        self.derive()
        self.picture()
        self.meaning()

    def derive(self):
        head = label(r"values uniform on 0 to 1; \ n bidders; \ guess that rivals bid $\beta(w) = c\,w$",
                     font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        steps = VGroup(
            MathTex(r"\Pr(\text{beat one rival}) = \Pr(c\,w < b) = \frac{b}{c}", font_size=36),
            MathTex(r"\Pr(\text{win}) = \Big(\frac{b}{c}\Big)^{n-1}", font_size=36),
            MathTex(r"\pi(b) = (v - b)\Big(\frac{b}{c}\Big)^{n-1}", font_size=40, color=FIRST),
            MathTex(r"\pi'(b) = 0:\quad -\Big(\frac{b}{c}\Big)^{n-1} + (v-b)\,\frac{(n-1)\,b^{n-2}}{c^{n-1}} = 0",
                    font_size=34),
            MathTex(r"b = \frac{n-1}{n}\,v", font_size=46, color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.45)
        side = VGroup(
            label(r"bid higher: \ win more often", font_size=21, color=YOU),
            label(r"bid higher: \ keep less when you win", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(steps[2], RIGHT, buff=0.5)
        foot = label(r"$c$ cancels: \ whatever the rivals' slope, \ your best slope is $(n-1)/n$; \ so all bid that "
                     r"way: \ an equilibrium", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How much should you shade in sale A? Here is the derivation, for values spread evenly from nothing to "
            "one, in units of a hundred shells, and n bidders. Guess that each rival bids a fixed fraction c of their "
            "value. <bookmark mark='a'/> Your bid b beats one rival when that rival's value is below b over c, "
            "which happens with probability b over c. <bookmark mark='b'/> To win, you must beat all n minus one "
            "rivals. <bookmark mark='c'/> So your expected profit is your value less your bid, times the chance of "
            "winning. <bookmark mark='d'/> The two forces are on the right: bidding higher wins more often, and "
            "leaves less when you win. Set the derivative to zero. <bookmark mark='e'/> The best bid is n minus "
            "one over n of your value. <bookmark mark='f'/> Notice that c has cancelled: whatever fraction the rivals "
            "bid, your best fraction is the same. So if everyone bids that fraction, nobody wants to change. That is "
            "the equilibrium, and with four bidders it is three quarters, which made your best bid in Play it fifty-"
            "two and a half."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(side), FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4], scale=1.1))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def picture(self):
        f = load("formats")
        vs = np.array(f["vs"])
        ax = plane([0, 1], [0, 1], center=LEFT * 2.6 + DOWN * 0.3, x_length=5.6, y_length=5.2,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"your value",
                   ylabel=r"your bid", font_size=16, xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
        a = ax.ax
        diag = DashedLine(a.c2p(0, 0), a.c2p(1, 1), color=GREY_C, stroke_width=2)
        dl = label(r"bid = value", font_size=15, color=GREY_B).move_to(a.c2p(0.62, 0.8)).rotate(PI / 4)
        cols = {"2": ALLPAY, "3": FIRST, "4": PRICE, "10": SECOND}
        lines = VGroup(*[path(ax, vs, f["bids"][k], color=cols[k], width=3, smooth=False) for k in ("2", "3", "4",
                                                                                                    "10")])
        labs = VGroup(*[label(rf"n = {k}", font_size=16, color=cols[k]).next_to(a.c2p(1.0, (int(k) - 1) / int(k)),
                                                                               RIGHT, buff=0.1)
                        for k in ("2", "3", "4", "10")])
        side = VGroup(
            label(r"two bidders: \ bid half your value", font_size=22, color=ALLPAY),
            label(r"four: \ three quarters", font_size=22, color=PRICE),
            label(r"ten: \ nine tenths", font_size=22, color=SECOND),
            label(r"more rivals, \ less shading: \\ competition does the seller's work", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here are the equilibrium bids against values, for different numbers of bidders, with the dashed line "
            "where a bid would equal the value. <bookmark mark='a'/> With two bidders, you bid half your value. "
            "<bookmark mark='b'/> With four, three quarters. <bookmark mark='c'/> With ten, nine tenths. "
            "<bookmark mark='d'/> The more rivals there are, the less each one shades: the competition among bidders "
            "does the seller's work. A seller's first rule is to attract bidders."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), FadeIn(dl), FadeIn(tag))
            for k, (mk, i) in enumerate(zip("abc", (0, 2, 3))):
                vo.wait_until(mk)
                self.play(Create(lines[i]), FadeIn(labs[i]), FadeIn(side[k]))
                if mk == "a":
                    self.play(Create(lines[1]), FadeIn(labs[1]), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def meaning(self):
        rows = VGroup(
            MathTex(r"\beta(v) = \mathbb{E}\big[\,Y \;\big|\; Y < v\,\big]", font_size=46, color=E.ACCENT),
            label(r"$Y$: \ the highest of the rivals' values", font_size=24, color=GREY_A),
            label(r"bid what you would expect to pay in a second-price auction, \ if you won", font_size=26,
                  color=FIRST),
            label(r"Play it: \ the highest of three rivals' values, \ given it's below 70, \ averages 52.5",
                  font_size=24, color=YOU),
            label(r"true for any spread of private values, \ not just the even one", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        tag = published_tag(r"Vickrey (1961); \ Krishna, \emph{Auction Theory}, ch.\ 2", corner=DR, font_size=13)
        with self.voiceover(
            "There is a neater way to say what the equilibrium bid is. <bookmark mark='a'/> Call Y the highest of "
            "the rivals' values. <bookmark mark='b'/> Your bid is what you would expect to pay in a second-price "
            "auction, if you won it. <bookmark mark='c'/> In Play it, the highest of three rivals' values, given "
            "that it falls below your seventy, averages fifty-two and a half: exactly your best bid in sale A. "
            "<bookmark mark='d'/> And this holds for any spread of private values, not just the even one. Sale A "
            "and sale B are starting to look like the same thing in different clothes."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
