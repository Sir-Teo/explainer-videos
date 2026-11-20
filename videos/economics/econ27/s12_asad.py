from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class ASAD(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Aggregate demand and supply", r"How do output and the price level settle together?",
             "Chapter ten. Aggregate demand and supply.", lit={1955: r"Samuelson's synthesis"}, scale=("nation",),
             horizon=("a year", "a decade"))
        self.curves()
        self.shocks()
        self.synthesis()

    def _axes(self):
        return plane([1200, 1700], [0.6, 1.6], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=4.8,
                     xticks=[1200, 1300, 1400, 1500, 1600, 1700], yticks=[0.6, 0.8, 1.0, 1.2, 1.4, 1.6],
                     xlabel=r"output $Y$", ylabel=r"price level $P$", xfmt=lambda v: f"{v:.0f}",
                     yfmt=lambda v: f"{v:.1f}", font_size=15)

    def curves(self):
        A = load("asad")
        ax = self._axes()
        ad = path(ax, A["ad0"], A["P"], color=SPEND, width=4, smooth=False)
        as_ = path(ax, A["as0"], A["P"], color=OUTPUT, width=4, smooth=False)
        lr = seg(ax, A["Ystar"], 0.6, A["Ystar"], 1.6, color=GREY_B, width=2, dashed=True)
        e = A["e0"]
        d = dot(ax, e["Y"], e["P"], color=WHITE, r=0.08)
        side = VGroup(
            label(r"AD: \ IS--LM's output at each price level; \\ lower prices, \ more real money, \\ lower rates, "
                  r"\ more spending", font_size=19, color=SPEND),
            label(r"below a price level of about 0.75 \\ it turns vertical: \ the trap, \\ where cheaper money "
                  r"does nothing", font_size=19, color=PRICE),
            label(r"AS: \ with wages sticky, \\ firms produce more when prices rise", font_size=19, color=OUTPUT),
            label(rf"dashed: \ potential output, \ {A['Ystar']:.0f}, \\ where AS ends up once wages adjust",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "I S and L M hold prices fixed. To let them move, draw two new curves. <bookmark mark='a'/> Aggregate "
            "demand gives I S L M's output at each price level. A lower price level means more real money, a lower "
            "interest rate and more investment, so demand slopes down. <bookmark mark='b'/> But notice its bottom: "
            "below a price level of about three quarters, the interest rate is already at zero, and cheaper money "
            "buys nothing more. Demand turns vertical. In a trap, falling prices do not help. "
            "<bookmark mark='c'/> Aggregate supply: with money wages sticky, a higher price level lowers real "
            "wages, and firms hire and produce more. <bookmark mark='d'/> The dashed line is potential output, "
            f"{A['Ystar']:,.0f}, where supply ends up once wages have had time to adjust. Today the curves cross "
            "very close to it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(ad), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(as_), FadeIn(side[2]), run_time=1.2)
            vo.wait_until("d")
            self.play(Create(lr), GrowFromCenter(d), FadeIn(side[3]))
        self.clear_scene()

    def shocks(self):
        A = load("asad")
        ax = self._axes()
        ad0 = path(ax, A["ad0"], A["P"], color=SPEND, width=3, smooth=False)
        ad1 = path(ax, A["ad1"], A["P"], color=PRICE, width=4, smooth=False)
        as0 = path(ax, A["as0"], A["P"], color=OUTPUT, width=3, smooth=False)
        as1 = path(ax, A["as1"], A["P"], color=INVEST, width=4, smooth=False)
        e0, dm, sp = A["e0"], A["demand"], A["supply"]
        d0 = dot(ax, e0["Y"], e0["P"], color=WHITE, r=0.07)
        d1 = dot(ax, dm["Y"], dm["P"], color=PRICE, r=0.09)
        d2 = dot(ax, sp["Y"], sp["P"], color=INVEST, r=0.09)
        side = VGroup(
            label(rf"a demand shock: \ money falls by {-A['dM']:.0f}", font_size=20, color=PRICE),
            label(rf"output {e0['Y']:.0f} $\to$ {dm['Y']:.0f}; \\ prices {e0['P']:.2f} $\to$ {dm['P']:.2f}: "
                  r"\\ both fall", font_size=20, color=PRICE),
            label(rf"a supply shock: \ costs rise by {100 * A['cost']:.0f}\%", font_size=20, color=INVEST),
            label(rf"output {e0['Y']:.0f} $\to$ {sp['Y']:.0f}; \\ prices {e0['P']:.2f} $\to$ {sp['P']:.2f}: "
                  r"\\ opposite ways", font_size=20, color=INVEST),
            label(r"the sign of the price change \\ tells you which shock it was", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Two kinds of shock. <bookmark mark='a'/> A demand shock first: the money supply falls by "
            f"{-A['dM']:.0f}, as it did in America after 1929. Aggregate demand moves left. "
            f"<bookmark mark='b'/> Output falls, from {e0['Y']:,.0f} to {dm['Y']:,.0f}, and prices fall too, from "
            f"{e0['P']:.2f} to {dm['P']:.2f}: both down together, as in the 1930s. "
            "<bookmark mark='c'/> Now a supply shock instead: costs rise by fifteen percent, as when oil prices "
            "jumped in the 1970s. Aggregate supply moves up. <bookmark mark='d'/> Output falls by about as much, "
            f"to {sp['Y']:,.0f}, but prices rise, to {sp['P']:.2f}. <bookmark mark='e'/> So the sign of the price "
            "change tells you which kind of shock hit. A demand slump brings deflation; a supply slump brings "
            "stagflation, and the policies that fight one make the other worse."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ad0), Create(as0), GrowFromCenter(d0), run_time=1.2)
            vo.wait_until("a")
            self.play(Create(ad1), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(GrowFromCenter(d1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(as1), FadeIn(side[2]), run_time=1.2)
            vo.wait_until("d")
            self.play(GrowFromCenter(d2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def synthesis(self):
        A = load("asad")
        P = np.array(A["P"])
        ad1 = np.array(A["ad1"])
        k = int(np.argmin(np.abs(ad1 - A["Ystar"])))
        p_long = float(P[k])
        rows = VGroup(
            label(r"the neoclassical synthesis", font_size=28, color=E.ACCENT),
            label(r"in the short run, \ wages and prices are sticky: \ Keynes is right, \ demand sets output",
                  font_size=23, color=SPEND),
            label(rf"in the long run, \ wages adjust: \ output returns to {A['Ystar']:.0f} and only prices have "
                  rf"changed \ (to {p_long:.2f} after the money shock)", font_size=22, color=OUTPUT),
            label(r"so policy can shorten the short run; \ it cannot raise the long run", font_size=23,
                  color=GOV),
            label(r"Samuelson's textbook, \ from the 1955 edition: \ the doctrine of a generation", font_size=21,
                  color=GREY_A),
            label(r"unless the short run is long, \ or never ends: \ Keynes, \ ``in the long run we are all dead''",
                  font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Samuelson, \emph{Economics} (3rd ed., 1955); \ Keynes, \emph{A Tract on Monetary "
                            r"Reform} (1923)", corner=DR, font_size=12)
        with self.voiceover(
            "This picture became a peace treaty. <bookmark mark='a'/> In the short run, wages and prices are "
            "sticky, so Keynes is right: demand sets output, and policy can help. <bookmark mark='b'/> In the long "
            f"run, wages adjust, output returns to its potential of {A['Ystar']:,.0f}, and only prices have "
            f"changed: after the money shock, the price level ends near {p_long:.2f}. The classics are right about "
            "the long run. <bookmark mark='c'/> So policy can shorten a slump, but it cannot raise what the economy "
            "can produce. <bookmark mark='d'/> Paul Samuelson called it the neoclassical synthesis, in his textbook "
            "from the 1955 edition, and it was the doctrine of a generation. <bookmark mark='e'/> Its weak point "
            "is the length of the short run. Keynes had written, in 1923, that the long run is a misleading guide "
            "to current affairs: in the long run we are all dead."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
