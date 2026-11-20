from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403

EVENTS = (
    (-600, r"Lydia: \ the first coins, \\ of gold and silver alloy", MONEY),
    (1024, r"Song China: \ the state issues \\ paper notes, \ \emph{jiaozi}", COCO),
    (1660, r"London: \ goldsmiths' receipts \\ circulate as notes", BANK),
    (1694, r"the Bank of England", CB),
    (1821, r"Britain on gold, \\ by law", MONEY),
    (1944, r"Bretton Woods: \ dollars \\ convertible into gold", MONEY),
    (1971, r"15 August: \ the gold \\ window closes", PRICE),
)


class Paper(VoiceoverScene):
    def construct(self):
        card(self, 4, r"From coin to paper", r"How did money stop being made of something valuable?",
             "Chapter four. From coin to paper.", lit={1024: r"jiaozi", 1694: r"Bank of England", 1971: r"Nixon"},
             scale=("nation", "world"), horizon=("a century",))
        self.timeline()
        self.lessons()

    def timeline(self):
        def x_of(year):
            # a compressed axis: before 1000 squeezed, after it linear
            if year < 1000:
                return -6.2 + (year + 700) / 1700 * 1.2
            return -5.0 + (year - 1000) / 1030 * 11.0
        axis = Line([-6.4, -0.2, 0], [6.4, -0.2, 0], color=GREY_B, stroke_width=3)
        ticks = VGroup()
        for y in (-600, 1000, 1200, 1400, 1600, 1800, 2000):
            t = Line([x_of(y), -0.32, 0], [x_of(y), -0.08, 0], color=GREY_B, stroke_width=2)
            ticks.add(VGroup(t, label(f"{abs(y)}" + (" BC" if y < 0 else ""), font_size=15,
                                      color=GREY_B).next_to(t, DOWN, buff=0.08)))
        marks = VGroup()
        for k, (y, txt, c) in enumerate(EVENTS):
            up = k % 2 == 0
            d = Dot([x_of(y), -0.2, 0], radius=0.08, color=c)
            lab = label(txt, font_size=17, color=c)
            lab.move_to([x_of(y), -0.2 + (1.5 if up else -1.6) + (0.55 * (k % 4 == 0) if up else -0.4 * (k % 4 == 3)),
                         0])
            stem = Line(d.get_center(), lab.get_bottom() if up else lab.get_top(), color=c, stroke_width=1.5)
            marks.add(VGroup(d, stem, lab))
        tag = published_tag(r"histories of money: \ von Glahn, \emph{Fountain of Fortune} (1996); \ Eichengreen, "
                            r"\emph{Globalizing Capital} (2019)", corner=DR, font_size=12)
        with self.voiceover(
            "Money has been made of less and less. <bookmark mark='a'/> The first coins were struck in Lydia, in what "
            "is now Turkey, about two thousand six hundred years ago, from an alloy of gold and silver: valuable "
            "metal, stamped to show its weight. <bookmark mark='b'/> In Sichuan, in the eleventh century, iron coins "
            "were so heavy that merchants began issuing paper receipts for them, and in 1024 the Song government "
            "took over the issue: the first official paper money. Without enough coin behind it, it later lost "
            "much of its value. <bookmark mark='c'/> In seventeenth-century London, goldsmiths took deposits of gold "
            "and gave receipts, and the receipts began to circulate as money; the goldsmiths noticed that not "
            "everyone came back for their gold at once, and lent some of it out. <bookmark mark='d'/> The Bank of "
            "England was founded in 1694. <bookmark mark='e'/> Britain's pound was tied to gold by law after the "
            "Napoleonic wars, and by the 1870s most trading nations were on gold. <bookmark mark='f'/> After the "
            "Second World War, at Bretton Woods, other currencies were tied to the dollar, and dollars held by "
            "central banks could be turned into gold. <bookmark mark='g'/> On 15 August 1971, President Nixon "
            "closed that window. Since then the world's main currencies have been backed by nothing but the "
            "expectation that they will be accepted."
        ) as vo:
            self.play(Create(axis), FadeIn(ticks), FadeIn(tag), run_time=1.2)
            for mk, m in zip("abcdefg", marks):
                vo.wait_until(mk)
                self.play(GrowFromCenter(m[0]), Create(m[1]), FadeIn(m[2]))
        self.clear_scene()

    def lessons(self):
        rows = VGroup(
            label(r"commodity money: \ worth something in itself; \ its supply depends on mines", font_size=24,
                  color=MONEY),
            label(r"convertible paper: \ a promise to pay commodity money; \ safe while people trust the promise",
                  font_size=24, color=BANK),
            label(r"fiat money: \ a promise of nothing; \ accepted because others accept it \ (chapter 3)",
                  font_size=24, color=CB),
            label(r"each step saves resources, \ and makes the quantity of money a choice", font_size=25,
                  color=E.ACCENT),
            label(r"which raises this part's other question: \ what happens when there is too much of it?",
                  font_size=22, color=PRICE),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "Three kinds of money, then. <bookmark mark='a'/> Commodity money is worth something in itself, so its "
            "supply depends on mines and luck. <bookmark mark='b'/> Convertible paper is a promise to pay the "
            "commodity, safe as long as people trust the promise. <bookmark mark='c'/> And fiat money is a promise "
            "of nothing at all: it is accepted because others accept it, the equilibrium of chapter three. "
            "<bookmark mark='d'/> Each step saves the resources tied up in metal, and each makes the quantity of "
            "money a decision. <bookmark mark='e'/> Which raises the question: what happens when someone decides "
            "there should be much more of it?"
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
