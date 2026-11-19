from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403

REP = "#7BD88F"


class Online(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Online markets: \ feedback as a fix", r"Can strangers trade things they can't inspect, \ "
             r"if every buyer leaves a review?", "Chapter twelve. Online markets: feedback as a fix.",
             lit={2010: r"Cabral and Hortaçsu"}, scale=("person", "market", "world"), horizon=("a day", "a year"))
        self.bayes()
        self.ebay()

    def bayes(self):
        r = load("reputation")
        price = np.array(r["price"])
        fb = r["feedback"]
        n = len(price)
        ax = plane([-0.5, n - 0.5], [50, 105], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[0, 4, 8, 12, 16], yticks=[60, 70, 80, 90, 100], xlabel=r"reviews so far",
                   ylabel=r"what a buyer will pay, \ \$", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        line = path(ax, np.arange(n), price, color=REP, width=3.2, smooth=False)
        dots = VGroup(*[Dot(a.c2p(k + 1, price[k + 1]), radius=0.06, color=REP if f else LOSS)
                        for k, f in enumerate(fb)])
        k = r["bad_at"]
        bad = Dot(a.c2p(k, price[k]), radius=0.11, color=LOSS)
        side = VGroup(
            label(r"a new seller: \ honest with chance 0.6; \\ an honest seller's sale goes well 95\% of the time, \\ a "
                  r"cheat's 60\%", font_size=20),
            label(r"a boat from an honest seller is worth \$100, \\ from a cheat \$40: \ buyers pay the expected value",
                  font_size=20, color=GREY_A),
            label(rf"three good reviews: \ \${r['start']:.0f} rises to \${r['before_bad']:.2f}", font_size=21, color=REP),
            label(rf"one bad review: \ \${r['after_bad']:.2f}", font_size=22, color=LOSS),
            label(rf"twelve more good ones to climb back, \\ to \${r['end']:.2f}: \ a reputation is slow to build, \\ "
                  r"quick to lose", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Online markets run on strangers. Reviews are their answer to Akerlof. <bookmark mark='a'/> Picture a new "
            "seller on the Island's market, who is honest with a chance of six in ten. An honest seller's sale goes "
            "well ninety-five times in a hundred, a cheat's only sixty. <bookmark mark='b'/> A boat from an honest "
            "seller is worth a hundred dollars, from a cheat forty, and buyers pay the expected value, given "
            "everything the reviews have told them. <bookmark mark='c'/> Three good reviews raise what buyers will "
            "pay from seventy-six dollars to about ninety-one, by Bayes's rule. <bookmark mark='d'/> Then one bad "
            "review, and the price drops to about sixty-six: a bad sale is far likelier from a cheat. "
            "<bookmark mark='e'/> It takes twelve more good reviews to climb back near a hundred. Reputations are slow "
            "to build and quick to lose, which is exactly what gives an honest seller a reason to stay honest."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(dots), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(bad, scale=1.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def ebay(self):
        papers = load("reputation")["papers"]
        rows = VGroup(
            label(r"Lu\'is Cabral and Ali Horta\c{c}su (2010), \ eBay's sellers:", font_size=24),
            label(r"after a seller's first negative feedback, \ weekly sales growth turned sharply negative",
                  font_size=23, color=LOSS),
            label(r"and further negatives arrived faster: \ a damaged reputation is worth less to protect",
                  font_size=23, color=GREY_A),
            label(r"the catch: \ nearly all feedback is positive, \ and reviews can be bought or faked", font_size=23,
                  color=HOLD),
            label(r"platforms now screen too: \ verified purchases, \ guarantees, \ and holding the money until the "
                  r"buyer is happy", font_size=23, color=SIGNAL),
            label(r"how platforms design trust: \ Part 61", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).move_to(UP * 0.1)
        tag = published_tag(r"Cabral and Horta\c{c}su, J.\ Industrial Economics 58(1) (2010)", corner=DR, font_size=13)
        del papers
        with self.voiceover(
            "Real platforms behave much like this. <bookmark mark='a'/> Luis Cabral and Ali Hortacsu followed sellers "
            "on eBay. <bookmark mark='b'/> After a seller's first negative feedback, the growth of their weekly sales "
            "turned sharply negative. <bookmark mark='c'/> And further negative feedback then arrived faster than the "
            "first, as if a damaged reputation were worth less effort to protect. <bookmark mark='d'/> The catch is "
            "that nearly all feedback is positive, so buyers learn less from it than they might, and reviews can be "
            "bought or faked. <bookmark mark='e'/> So platforms now screen as well: they verify purchases, offer their "
            "own guarantees, and hold the buyer's money until the buyer is satisfied. <bookmark mark='f'/> How "
            "platforms design trust is part of Part sixty-one."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
