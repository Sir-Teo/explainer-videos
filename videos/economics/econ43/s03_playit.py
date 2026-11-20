from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ two mergers among five brands", r"Which merger would raise prices more?",
             "Chapter two. Play it: two mergers among five brands.", lit={2010: r"Farrell and Shapiro"},
             scale=("industry",), horizon=("a year",))
        self.ask()
        self.reveal()
        self.why()

    def brand_boxes(self, G, scale=1.0):
        P = TRUTH["playit"]
        boxes = VGroup()
        sh = G["shares_inside"]
        for j, (nm, g) in enumerate(zip(P["names"], P["nests"])):
            h = 1.2 + 6.0 * sh[j]
            box = RoundedRectangle(width=1.75, height=h, corner_radius=0.1, stroke_color=NEST[g], stroke_width=2.4,
                                   fill_color=NEST[g], fill_opacity=0.22)
            t = label(nm, font_size=17, color=WHITE).move_to(box.get_top() + DOWN * 0.3)
            s = label(rf"{100 * sh[j]:.0f}\% of sales", font_size=15, color=GREY_A).next_to(t, DOWN, buff=0.12)
            p = label(rf"\${G['p0'][j]:.2f}", font_size=17, color=PRICE).next_to(s, DOWN, buff=0.12)
            boxes.add(VGroup(box, t, s, p))
        boxes.arrange(RIGHT, buff=0.32, aligned_edge=DOWN).scale(scale)
        nests = VGroup()
        for g, nm in enumerate((r"sweet", r"nutty", r"bran")):
            mem = VGroup(*[boxes[j] for j in range(5) if P["nests"][j] == g])
            br = Brace(mem, DOWN, color=NEST[g], buff=0.1)
            nests.add(VGroup(br, label(nm, font_size=18, color=NEST[g]).next_to(br, DOWN, buff=0.08)))
        return boxes, nests

    def ask(self):
        G = load("playit")
        P = TRUTH["playit"]
        boxes, nests = self.brand_boxes(G)
        VGroup(boxes, nests).move_to(UP * 0.45)
        x, y = G["x"], G["y"]
        n = P["names"]
        opts = VGroup(
            label(rf"X: \ {n[3]} + {n[4]}: \ the Herfindahl index rises {x['dhhi']:,.0f}", font_size=22,
                  color=NEST[2]),
            label(rf"Y: \ {n[0]} + {n[2]}: \ the Herfindahl index rises {y['dhhi']:,.0f}", font_size=22,
                  color=NEST[0]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        head = label(r"Your turn: \ which merger raises the merging brands' prices more?", font_size=27,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        ring = countdown().scale(0.6).next_to(opts, RIGHT, buff=0.6)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Your turn. The Island's cereal market has five brands, each made by a different firm. "
            "<bookmark mark='a'/> Two are sweet, Sun Flakes and Honey Puffs. One is nutty, Nut Clusters. And two "
            "are bran cereals, Bran Buds and Bran Twigs, which taste almost the same. <bookmark mark='b'/> Each box "
            "shows the brand's share of sales and its price. Two mergers are proposed. <bookmark mark='c'/> Merger "
            "X joins the two bran cereals. Together they have about a quarter of sales, and the usual measure of "
            f"concentration, the Herfindahl index, rises by {x['dhhi']:,.0f} points. <bookmark mark='d'/> Merger Y "
            "joins the two largest brands, Sun Flakes and Nut Clusters, with almost sixty percent of sales; the "
            f"index rises by {y['dhhi']:,.0f}. Which merger would raise the merging brands' prices more? Pause, and "
            "choose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(b[:2]) for b in boxes], lag_ratio=0.2),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(nb) for nb in nests], lag_ratio=0.4), run_time=1.5)
            vo.wait_until("b")
            self.play(*[FadeIn(b[2:]) for b in boxes])
            vo.wait_until("c")
            self.play(FadeIn(opts[0]), Indicate(VGroup(boxes[3], boxes[4]), color=WHITE, scale_factor=1.04))
            vo.wait_until("d")
            self.play(FadeIn(opts[1]), Indicate(VGroup(boxes[0], boxes[2]), color=WHITE, scale_factor=1.04),
                      FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.keep = (head, boxes, nests, opts, tag)

    def reveal(self):
        G = load("playit")
        head, boxes, nests, opts, tag = self.keep
        x, y = G["x"], G["y"]
        hl = SurroundingRectangle(opts[0], color=GAIN, buff=0.1)
        ups = VGroup()
        for j in range(5):
            dx = x["dp"][j]
            if dx > 0.005:
                ups.add(label(rf"+{100 * dx:.0f}\%", font_size=22, color=LOSS).next_to(boxes[j], UP, buff=0.1))
        res = VGroup(
            label(rf"X: \ the bran cereals' prices rise {100 * x['merged']:.0f}\%; \ shoppers lose "
                  rf"{100 * abs(x['dcs_pct']):.1f}\% of their surplus", font_size=21, color=NEST[2]),
            label(rf"Y: \ the two largest rise {100 * y['merged']:.1f}\%; \ shoppers lose "
                  rf"{100 * abs(y['dcs_pct']):.1f}\%", font_size=21, color=NEST[0]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The answer is X, and not by a little. <bookmark mark='a'/> After merger X the two bran cereals' prices "
            f"rise by about {say_pct(x['merged'], 0)}. <bookmark mark='b'/> After merger Y the two largest brands' "
            f"prices rise by only {say_pct(y['merged'], 1)}. Shoppers lose {say_pct(abs(x['dcs_pct']), 1)} of what "
            f"they gain from the market under X, and {say_pct(abs(y['dcs_pct']), 1)} under Y. The merger that barely "
            "moves the concentration index does more than twice the harm."
        ) as vo:
            self.play(Create(hl))
            vo.wait_until("a")
            self.play(FadeOut(opts), FadeOut(hl), FadeIn(res[0]), FadeIn(ups, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(res[1]))
        self.clear_scene()

    def why(self):
        G = load("playit")
        P = TRUTH["playit"]
        n = P["names"]
        D = np.array(G["diversion"])
        rows = VGroup(
            label(rf"raise {n[3]}'s price: \ {100 * D[3][4]:.0f}\% of the shoppers it loses \\ buy {n[4]} instead",
                  font_size=21, color=NEST[2]),
            label(rf"raise {n[0]}'s price: \ only {100 * D[0][2]:.0f}\% of its lost shoppers \\ buy {n[2]}",
                  font_size=21, color=NEST[0]),
            label(r"a merger raises prices when the merging products are close substitutes: \\ the diversion "
                  r"ratio, \ not the market share, \ does the work", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.4)
        head = label(r"why: \ diversion", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"to know the diversion ratios you must know demand: \ the next chapters estimate it",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Farrell and Shapiro (2010); \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Why? Think about what stops a firm from raising its price: shoppers leave. <bookmark mark='a'/> When "
            f"Bran Buds raises its price, about {say_pct(D[3][4], 0)} of the shoppers it loses buy Bran Twigs "
            "instead. Once the two are one firm, those shoppers are no longer lost, so the higher price pays. "
            f"<bookmark mark='b'/> When Sun Flakes raises its price, only {say_pct(D[0][2], 0)} of its lost "
            "shoppers buy Nut Clusters; most go elsewhere or stop buying cereal. <bookmark mark='c'/> The fraction "
            "of lost sales that goes to the merger partner is called the diversion ratio, and it, not the market "
            "share, decides how much a merger raises prices. <bookmark mark='d'/> But diversion ratios are facts "
            "about demand, and nobody publishes them. The next chapters are about estimating them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
