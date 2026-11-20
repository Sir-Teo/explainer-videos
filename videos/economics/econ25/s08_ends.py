from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403

CASES = (("Austria", r"1922", r"League of Nations loan; \\ a new central bank"),
         ("Germany", r"November 1923", r"the Rentenmark; \\ no more credit to the state"),
         ("Hungary", r"1924", r"League of Nations loan; \\ a balanced budget"),
         ("Poland", r"1924", r"tax reform; \\ an independent bank"))


class Ends(VoiceoverScene):
    def construct(self):
        card(self, 7, r"How four big inflations ended", r"Can a hyperinflation be stopped overnight?",
             "Chapter seven. How four big inflations ended.", lit={1982: r"Sargent", 1986: r"Wicker"},
             scale=("nation",), horizon=("a month", "a year"))
        self.four()
        self.lesson()
        self.model()

    def four(self):
        cards = VGroup()
        for name, when, how in CASES:
            box = RoundedRectangle(width=2.9, height=2.6, corner_radius=0.15, stroke_color=PRICE, stroke_width=2)
            body = VGroup(label(name, font_size=26, color=WHITE), label(when, font_size=21, color=E.ACCENT),
                          label(how, font_size=17, color=GREY_A)).arrange(DOWN, buff=0.22).move_to(box)
            cards.add(VGroup(box, body))
        cards.arrange(RIGHT, buff=0.3).move_to(UP * 0.6)
        rows = VGroup(
            label(r"after the First World War: \ deficits, \ reparations, \ and central banks that lent to the state",
                  font_size=21, color=GREY_A),
            label(r"each ended within weeks, \ when the government stopped financing itself by printing",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(cards, DOWN, buff=0.5)
        tag = published_tag(r"Sargent, \ ``The Ends of Four Big Inflations'', \ in Hall (ed.), \emph{Inflation: "
                            r"Causes and Effects} (NBER, 1982): \ 41--98", corner=DR, font_size=12)
        with self.voiceover(
            "In 1982 Thomas Sargent studied four of the hyperinflations that followed the First World War. "
            "<bookmark mark='a'/> Austria, Germany, Hungary and Poland had run large deficits, some burdened by "
            "reparations, and their central banks had financed them by printing. <bookmark mark='b'/> Austria "
            "stabilized in 1922, with a loan arranged by the League of Nations and a new central bank. "
            "<bookmark mark='c'/> Germany in November 1923, with a new currency and an end to central bank credit for "
            "the government. <bookmark mark='d'/> Hungary in 1924, again with a League loan and a balanced budget. "
            "<bookmark mark='e'/> And Poland in 1924, with tax reform. <bookmark mark='f'/> In each, prices stopped "
            "rising within weeks, at the moment the government credibly stopped paying its way with the printing "
            "press."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, c in zip("bcde", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def lesson(self):
        rows = VGroup(
            label(r"Sargent's reading: \ a change of \emph{regime}, \ not a slow squeeze", font_size=26,
                  color=E.ACCENT),
            label(r"people believed the new rules: \ budgets balanced, \ the bank forbidden to lend to the state",
                  font_size=22, color=GREY_A),
            label(r"so expected inflation collapsed, \ and with it the cost of holding money", font_size=22,
                  color=MONEY),
            label(r"people rebuilt the money balances they had fled: \ the quantity of money could grow \\ while "
                  r"prices held still", font_size=22, color=MONEY),
            label(r"his critics: \ the ends were less painless than his account suggests \ (Wicker, \ 1986)",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Sargent (1982); \ Wicker (1986)", corner=DR, font_size=12)
        with self.voiceover(
            "Sargent's reading was that these were changes of regime, not slow squeezes. "
            "<bookmark mark='a'/> People believed the new rules, because they were written into law and backed by "
            "outside lenders: budgets would balance, and the central bank could no longer lend to the state. "
            "<bookmark mark='b'/> So expected inflation collapsed at once, and with it the cost of holding money. "
            "<bookmark mark='c'/> People wanted their money balances back, so the quantity of money could keep "
            "growing for a while after the stabilization without pushing prices up: Cagan's demand, running in "
            "reverse. <bookmark mark='d'/> Critics, among them Elmus Wicker, have argued that the stabilizations "
            "were less painless than Sargent's account suggests. The lesson that survived is about credibility."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def model(self):
        d = load("deficit")
        T = len(d["slow"]["path"])
        ax = plane([0, d["months"]], [0, 0.6], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=4.8,
                   xticks=[0, 12, 24, 36, 48, 60], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], xlabel=r"months",
                   ylabel=r"inflation, \ a month", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=16)
        lo, hi = d["slow"]["steady"]
        s_lo = seg(ax, 0, lo, d["months"], lo, color=MONEY, width=2, dashed=True)
        s_hi = seg(ax, 0, hi, d["months"], hi, color=PRICE, width=2, dashed=True)
        slow = path(ax, list(range(T)), d["slow"]["path"], color=MONEY, width=4, yr=(0, 0.6))
        fast = path(ax, list(range(len(d["fast"]["path"]))), d["fast"]["path"], color=PRICE, width=4, yr=(0, 0.6),
                    smooth=False)
        big = path(ax, list(range(len(d["big"]["path"]))), d["big"]["path"], color=BANK, width=4, yr=(0, 0.6),
                   smooth=False)
        side = VGroup(
            label(rf"a deficit of {100 * d['deficit']:.0f}\% of real balances, \\ paid by printing", font_size=20,
                  color=GREY_A),
            label(rf"two steady states: \\ {100 * lo:.1f}\% \ and \ {100 * hi:.0f}\% a month", font_size=20,
                  color=WHITE),
            label(r"slow expectations: \\ settles at the low one", font_size=20, color=MONEY),
            label(r"fast expectations: \\ it runs away", font_size=20, color=PRICE),
            label(r"a deficit beyond the most \\ printing can ever raise: \\ no steady state", font_size=20,
                  color=BANK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Agora shows why the fiscal regime is the key. Suppose a government runs a deficit worth "
            f"{100 * d['deficit']:.0f} percent of the real balances people would hold at zero inflation, every month, "
            "and pays it by printing. <bookmark mark='a'/> Two inflation rates raise exactly that much: a low one, "
            f"{100 * lo:.1f} percent a month, and a high one, {100 * hi:.0f} percent, on the far side of the Laffer "
            "peak. <bookmark mark='b'/> If people's expectations adapt slowly, the economy settles at the low one. "
            "<bookmark mark='c'/> If they adapt fast, as they do once people have lived through inflation, there is "
            "no stopping: inflation runs away. <bookmark mark='d'/> And a deficit larger than the most the "
            "inflation tax can ever raise has no steady state at all. Printing faster cannot close it; only "
            "closing the deficit can. That is what the four stabilizations did."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(s_lo), Create(s_hi), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(slow), FadeIn(side[2]), run_time=2)
            vo.wait_until("c")
            self.play(Create(fast), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(big), FadeIn(side[4]), run_time=1.5)
        self.clear_scene()
