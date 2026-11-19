from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403


class Commitment(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Commitment and entry deterrence", r"Can a firm gain by tying its own hands, \ and can it keep "
             r"a rival out?", "Chapter seven. Commitment and entry deterrence.",
             lit={1934: r"von Stackelberg", 1980: r"Dixit's capacity"}, scale=("firm", "market"),
             horizon=("a year", "a decade"))
        self.leader()
        self.deter()
        self.regimes()
        self.taxonomy()

    def leader(self):
        b = load("boats")
        a_, bb, c = b["a"], b["b"], b["c"]
        qL = (a_ - c) / (2 * bb)
        qF = (a_ - c - bb * qL) / (2 * bb)
        P = a_ - bb * (qL + qF)
        piL, piF = (P - c) * qL, (P - c) * qF
        ax = plane([0, 92], [0, 92], center=LEFT * 3.2 + DOWN * 0.3, x_length=5.4, y_length=5.4,
                   xticks=[0, 30, 45, 90], yticks=[0, 22.5, 30, 45, 90], xlabel=r"Crusoe's boats",
                   ylabel=r"Dara's boats", font_size=16, xfmt=lambda v: fmt(v), yfmt=lambda v: fmt(v))
        a = ax.ax
        q = np.array(b["q1"])
        rep = np.array(b["reply"])
        rd = path(ax, q, rep, color=DARA, width=3.5, smooth=False)
        rdl = label(r"Dara's best reply", font_size=16, color=DARA).next_to(a.c2p(64, 14), UP, buff=0.2)
        cour = Dot(a.c2p(30, 30), radius=0.09, color=GREY_A)
        col = label(r"Cournot", font_size=15, color=GREY_A).next_to(cour, UR, buff=0.05)
        st = Dot(a.c2p(qL, qF), radius=0.1, color=LEADER)
        stl = label(r"Stackelberg", font_size=15, color=LEADER).next_to(st, UR, buff=0.05)
        side = VGroup(
            label(r"Heinrich von Stackelberg (1934): \\ one firm moves first, \ and the other knows it", font_size=21),
            label(r"Crusoe builds first, \ knowing Dara will reply: \\ he picks the best point on her reply curve",
                  font_size=21, color=LEADER),
            label(rf"Crusoe: \ {qL:.0f} boats, \ \${piL:,.1f}; \\ Dara: \ {qF:.1f} boats, \ \${piF:,.2f}".replace(
                ",", "{,}"), font_size=22, color=EQ),
            label(rf"price \${P:.1f}: \ lower than Cournot's \$40", font_size=21, color=COMPETE),
            label(r"moving first pays \ only if it can't be undone: \\ boats already built, \ not a promise",
                  font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"von Stackelberg, \emph{Marktform und Gleichgewicht} (1934); \ the numbers: \ Agora",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Cournot's yards choose at the same time. In 1934 the German economist Heinrich von Stackelberg asked "
            "what happens when one firm moves first. <bookmark mark='a'/> Suppose Crusoe builds his boats before "
            "Dara decides, and she can see them. <bookmark mark='b'/> Crusoe knows that Dara will reply along her "
            "best-reply curve, so he chooses the point on it that is best for him. <bookmark mark='c'/> He builds "
            "forty-five boats, the monopoly's number, and earns a thousand and twelve dollars and fifty cents. Dara's "
            "best reply is twenty-two and a half, earning about five hundred and six. Moving first is worth a "
            "hundred and twelve dollars and fifty cents to Crusoe, and costs Dara nearly four hundred. "
            "<bookmark mark='d'/> Buyers gain too: the price is thirty-two fifty, below Cournot's forty. "
            "<bookmark mark='e'/> But moving first pays only if it cannot be undone. Boats already built are a "
            "commitment. A promise to build them is not, because once Dara has built hers, Crusoe would rather "
            "build fewer."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(rd), FadeIn(rdl), FadeIn(cour), FadeIn(col))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(rd, color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(st, scale=1.5), FadeIn(stl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def deter(self):
        d = load("deter")
        p = d["params"]
        ks = np.array(d["ks"])
        prof = np.array(d["entrant_profit"])
        ax = plane([0, 60], [-80, 300], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[0, 20, 30, 36, 40, 60], yticks=[-50, 0, 100, 200, 300], xlabel=r"Crusoe's slips, \ built "
                   r"in advance", ylabel=r"Dara's profit if she enters, \ \$", font_size=16, xfmt=lambda v: fmt(v),
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        curve = path(ax, ks, prof, color=ENTRANT, width=3.5, smooth=False, xr=(0, 60))
        zero = DashedLine(a.c2p(0, 0), a.c2p(60, 0), color=GREY_B, stroke_width=1.5)
        band = Polygon(a.c2p(d["S"], -80), a.c2p(d["T"], -80), a.c2p(d["T"], 300), a.c2p(d["S"], 300),
                       stroke_width=0, fill_color=LEADER, fill_opacity=0.12)
        bl = label(r"credible threats", font_size=15, color=LEADER).move_to(a.c2p(30, 280))
        mdot = Dot(a.c2p(d["m"], float(np.interp(d["m"], ks, prof))), radius=0.08, color=WHITE)
        ml = label(r"monopoly's 30", font_size=15).next_to(mdot, UR, buff=0.05)
        ddot = Dot(a.c2p(d["deter_k"], 0), radius=0.1, color=EQ)
        dl = label(rf"{d['deter_k']:.0f}: \ Dara stays out", font_size=15, color=EQ).next_to(a.c2p(44, 0), UP,
                                                                                         buff=0.12)
        side = VGroup(
            label(rf"Avinash Dixit (1980): \ a slip costs \${p['r']:.0f} to build, \\ \${p['c']:.0f} to use; \ "
                  rf"Dara would pay \${p['F']:.0f} to set up", font_size=21),
            label(r"slips Crusoe has already built \\ cost him only \$10 a boat to use: \\ he will use them if Dara "
                  r"enters", font_size=21, color=LEADER),
            label(r"but only up to a point: \ capacity beyond 40 \\ he would leave idle, \ so it frightens nobody",
                  font_size=21, color=GREY_A),
            label(rf"at {d['deter_k']:.0f} slips Dara's profit is zero: \\ Crusoe earns \${d['pi_deter']:.0f}, \ "
                  rf"against \${d['pi_acc']:.0f} \\ if he lets her in", font_size=22, color=EQ),
            label(rf"six more slips than a monopolist needs: \\ \${d['pi_mono'] - d['pi_deter']:.0f} a year, \ "
                  r"spent on keeping Dara out", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Dixit, Economic Journal 90(357) (1980); \ the numbers: \ Agora", corner=DR, font_size=13)
        with self.voiceover(
            "Commitment can also keep a rival out. In 1980 Avinash Dixit studied an incumbent who can build "
            "capacity before anyone else arrives. <bookmark mark='a'/> On the Island, a boat slip costs thirty "
            "dollars to build and ten more to use; Crusoe is alone, and Dara is deciding whether to pay a hundred "
            "and forty-four dollars to set up a second yard. <bookmark mark='b'/> Slips Crusoe has already built "
            "cost him only ten dollars a boat to use, so if Dara enters he will use them: they make him tough. "
            "<bookmark mark='c'/> But only up to a point. Beyond forty slips, he would leave the extra ones idle "
            "rather than flood the market, so building them frightens nobody. Only capacities in the shaded range "
            "are credible threats. <bookmark mark='d'/> With thirty-six slips, Dara's best reply would earn her "
            "nothing, so she stays out, and Crusoe earns eight hundred and sixty-four dollars a year. If he let her "
            "in and led as Stackelberg did, he would earn four hundred and fifty. <bookmark mark='e'/> The "
            "deterrence costs him: a monopolist who feared nobody would build thirty slips and earn nine hundred. "
            "Six extra slips, thirty-six dollars a year, are what keeping Dara out is worth to him."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(zero), Create(curve))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(band), FadeIn(bl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(mdot), FadeIn(ml), FadeIn(ddot, scale=1.5), FadeIn(dl), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def regimes(self):
        d = load("deter")
        Fs = np.array(d["Fs"])
        reg = d["F_regime"]
        prof = np.array(d["F_profit"])
        colors = {"impossible": CARTEL, "accommodate": CARTEL, "deter": EQ, "blockaded": COMPETE}
        ax = plane([0, 410], [300, 950], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.4, y_length=4.4,
                   xticks=[0, 100, 225, 300, 400], yticks=[450, 600, 750, 900], xlabel=r"Dara's setup cost, \ \$",
                   ylabel=r"Crusoe's best profit, \ \$", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        dots = VGroup(*[Dot(a.c2p(F, p), radius=0.05, color=colors[r]) for F, p, r in zip(Fs, prof, reg)])
        side = VGroup(
            label(r"low setup cost: \ no credible capacity keeps Dara out; \\ Crusoe lets her in and leads",
                  font_size=21, color=CARTEL),
            label(r"middle: \ Crusoe builds extra slips to keep her out \\ (strategic deterrence)", font_size=21,
                  color=EQ),
            label(r"high: \ the monopoly's own 30 slips \\ already keep her out \ (blockaded entry)", font_size=21,
                  color=COMPETE),
            label(r"Joe Bain had named all three in 1956; \\ Dixit showed which threats are believable",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "How Crusoe should respond depends on how costly entry is for Dara. <bookmark mark='a'/> If her setup "
            "cost is low, no credible capacity keeps her out, and Crusoe does best to let her in and lead. "
            "<bookmark mark='b'/> In a middle range he builds extra slips to keep her out: strategic deterrence. "
            "<bookmark mark='c'/> And if her setup cost is high, the thirty slips a monopolist would build anyway are "
            "enough: entry is blockaded. <bookmark mark='d'/> Joe Bain had described all three cases in 1956. "
            "Dixit's contribution was to show which threats an entrant should believe."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]),
                      FadeIn(VGroup(*[d_ for d_, r in zip(dots, reg) if r in ("impossible", "accommodate")])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[d_ for d_, r in zip(dots, reg) if r == "deter"])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*[d_ for d_, r in zip(dots, reg) if r == "blockaded"])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def taxonomy(self):
        head = label(r"Fudenberg and Tirole's animals (1984)", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.45)
        cols = [r"to keep a rival out", r"to live with it: \\ quantities", r"to live with it: \\ prices"]
        rows = [r"investment makes \\ you tough", r"investment makes \\ you soft"]
        cells = [[(r"top dog: \\ overinvest", LEADER), (r"top dog: \\ overinvest", LEADER),
                  (r"puppy dog: \\ underinvest", COMPETE)],
                 [(r"lean and hungry: \\ underinvest", ENTRANT), (r"lean and hungry: \\ underinvest", ENTRANT),
                  (r"fat cat: \\ overinvest", CARTEL)]]
        grid = VGroup()
        W, H = 3.3, 1.35
        for i in range(2):
            for j in range(3):
                box = Rectangle(width=W, height=H, stroke_color=GREY_C, stroke_width=1.5).move_to(
                    RIGHT * (j - 0.6) * W + DOWN * (i - 0.1) * H)
                t, c = cells[i][j]
                grid.add(VGroup(box, label(t, font_size=22, color=c).move_to(box)))
        chead = VGroup(*[label(c, font_size=19, color=GREY_A).next_to(grid[j][0], UP, buff=0.15)
                         for j, c in enumerate(cols)])
        rhead = VGroup(*[label(r, font_size=19, color=GREY_A).next_to(grid[3 * i][0], LEFT, buff=0.2)
                         for i, r in enumerate(rows)])
        foot = VGroup(
            label(r"Crusoe's slips make him tough: \ top dog", font_size=22, color=LEADER),
            label(r"a loyalty scheme makes a firm reluctant to cut prices, \ so a rival can price higher too: \ "
                  r"fat cat", font_size=22, color=CARTEL),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Fudenberg and Tirole, AER 74(2) (1984); \ Tirole (1988), ch.\ 8", corner=DR, font_size=13)
        tab = VGroup(grid, chead, rhead).move_to(UP * 0.4)
        with self.voiceover(
            "In 1984 Drew Fudenberg and Jean Tirole sorted every such strategy into a zoo. <bookmark mark='a'/> Ask "
            "two questions about an investment made in advance: does it make you tough or soft toward your rival, "
            "and do you want the rival out, or are you living with it? <bookmark mark='b'/> To keep a rival out, "
            "be a top dog, investing more if it makes you tough, or show the lean and hungry look, investing less if "
            "investment would make you soft. <bookmark mark='c'/> Living with a rival in quantities, the same advice "
            "holds. But living with it in prices, the answer flips: be a puppy dog, small and unthreatening, or a "
            "fat cat, comfortable and slow to cut prices, because a rival who sees you won't fight will raise its "
            "own prices too. <bookmark mark='d'/> Crusoe's slips make him tough: he is a top dog. A loyalty scheme "
            "that rewards existing customers makes a firm reluctant to cut prices to win new ones; that softness "
            "invites rivals to price higher too, and makes the scheme a fat cat's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(chead), FadeIn(rhead),
                      FadeIn(VGroup(*[g[0] for g in grid])))
            vo.wait_until("b")
            self.play(FadeIn(grid[0][1]), FadeIn(grid[3][1]))
            vo.wait_until("c")
            self.play(FadeIn(grid[1][1]), FadeIn(grid[4][1]), FadeIn(grid[2][1]), FadeIn(grid[5][1]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        del tab
        self.clear_scene()
