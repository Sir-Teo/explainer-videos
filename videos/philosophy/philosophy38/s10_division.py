from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Division(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Fair division", r"How do you divide a cake so that no one envies anyone?", lit=(1948, 2016), part=PART)
        with self.voiceover("Chapter nine. Fair division."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.cut_choose()
        self.selfridge()
        self.history()
        self.rent()
        self.matching()
        self.stability()
        self.notions()

    # the cake is [0, 1], drawn from X0 to X1
    X0, X1 = -5.4, 5.6

    def xc(self, t):
        return self.X0 + (self.X1 - self.X0) * t

    def lane(self, dens, base, scale, color, name):
        g = VGroup()
        for k, h in enumerate(dens):
            if h <= 0:
                continue
            r = Rectangle(width=(self.X1 - self.X0) / len(dens), height=h * scale, stroke_width=1, stroke_color=color,
                          fill_color=color, fill_opacity=0.45)
            r.move_to([self.xc((k + 0.5) / len(dens)), base + h * scale / 2, 0])
            g.add(r)
        g.add(Line([self.X0, base, 0], [self.X1, base, 0], color=GREY_C, stroke_width=1.5))
        g.add(label(name, font_size=21, color=color).move_to([self.X0 - 0.75, base + 0.25, 0]))
        return g

    def slab(self, a, b, color, y=-2.75, h=0.42, opacity=0.85):
        return Rectangle(width=max(0.01, (b - a) * (self.X1 - self.X0)), height=h, stroke_width=1.2, stroke_color=WHITE,
                         fill_color=color, fill_opacity=opacity).move_to([self.xc((a + b) / 2), y, 0])

    def cut(self, t, top, bottom=-3.0, color=WHITE):
        return DashedLine([self.xc(t), bottom, 0], [self.xc(t), top, 0], color=color, stroke_width=3, dash_length=0.08)

    def cut_choose(self):
        d = load("cake")["cut_choose"]
        sc = load("cake")["sc"]
        assert d["cut"] == 0.1667 and d["chooser_values"] == [0.0333, 0.9667] and d["chooser_takes"] == "right"
        head = label(r"I cut, \ you choose", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ana = self.lane(sc["densities"][0], 0.55, 0.42, FAIR, r"Ana")
        ben = self.lane(sc["densities"][1], -1.75, 0.42, MKT, r"Ben")
        whole = self.slab(0, 1, GREY_D)
        knife = self.cut(d["cut"], 2.0)
        av = label(r"Ana: \ $\tfrac12 \ \big| \ \tfrac12$", font_size=22, color=FAIR).move_to([self.xc(0.45), 1.85, 0])
        bv = label(rf"Ben: \ ${d['chooser_values'][0]:.2f} \ \big| \ {d['chooser_values'][1]:.2f}$", font_size=22,
                   color=MKT).move_to([self.xc(0.45), -0.15, 0])
        left, right = self.slab(0, d["cut"], FAIR), self.slab(d["cut"], 1, MKT)
        note = label(r"each gets at least half, \ by her own measure: \ no envy", font_size=22,
                     color=GOAL).move_to([0.2, -3.5, 0])
        with self.voiceover(
            "Fair division starts with the oldest procedure there is: one cuts, the other chooses. <bookmark "
            "mark='a'/>Here is a cake, the interval from zero to one, and two people who value its parts differently. "
            "Ana loves the left end, where the chocolate is; Ben loves the middle. Each one's values add up to one. "
            "<bookmark mark='b'/>Ana cuts where the two sides are worth exactly a half to her: at one sixth, since "
            "the left end is so rich. <bookmark mark='c'/>Ben compares. The left piece is worth about three "
            "hundredths to him, the right piece about ninety seven hundredths. He takes the right. <bookmark "
            "mark='d'/>Neither envies the other. Ana has exactly half by her own measure, whatever Ben does; Ben has "
            "at least half by his. The cutter's guarantee comes from cutting, and the chooser's from choosing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(whole), FadeIn(ana), FadeIn(ben))
            vo.wait_until("b")
            self.play(Create(knife), FadeIn(av))
            vo.wait_until("c")
            self.play(FadeIn(bv))
            vo.wait_until("d")
            self.play(FadeIn(left), FadeIn(right), FadeIn(note))
        self.clear_scene()

    def selfridge(self):
        d = load("cake")["sc"]
        assert d["first_cuts"] == [0.1111, 0.2667] and d["trim"] == 0.3611 and d["fav_of_2"] == 2
        assert d["picks"] == {"3": 1, "2": 2, "1": 0} and d["trimmed_taker"] == 1 and d["cutter"] == 2
        assert d["trim_cuts"] == [0.5741, 0.787] and d["envy_free"]
        head = label(r"Envy-free for three \ (Selfridge; \ Conway, \ c. \ 1960)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        cols, names = [FAIR, MKT, COM], [r"Ana", r"Ben", r"Cy"]
        lanes = [self.lane(d["densities"][i], b, 0.3, cols[i], names[i]) for i, b in zip(range(3), (1.25, -0.05, -1.35))]
        c1, c2 = d["first_cuts"]
        cuts1 = VGroup(self.cut(c1, 2.3, color=FAIR), self.cut(c2, 2.3, color=FAIR))
        whole = VGroup(self.slab(0, c1, GREY_D), self.slab(c1, c2, GREY_D), self.slab(c2, 1, GREY_D))
        t = d["trim"]
        trim = self.cut(t, 2.3, color=MKT)
        trimmings = self.slab(t, 1, GREY_B, y=-3.35, h=0.3, opacity=0.5)
        first = VGroup(self.slab(0, c1, FAIR), self.slab(c1, c2, COM), self.slab(c2, t, MKT))
        t1, t2 = d["trim_cuts"]
        cuts2 = VGroup(self.cut(t1, 2.3, color=COM), self.cut(t2, 2.3, color=COM))
        b = d["bundles"]
        second = VGroup(*[self.slab(*b[str(i)][1], cols[i]) for i in range(3)])
        steps = [r"1. \ Ana cuts three pieces equal for her", r"2. \ Ben trims his favourite to tie his second",
                 r"3. \ Cy, \ Ben, \ Ana choose; \ Ben must take the trimmed piece",
                 r"4. \ Cy cuts the trimmings; \ Ben, \ Ana, \ Cy choose"]
        sl = [label(s, font_size=20, color=GREY_A).move_to([0.1, 2.75 - 0.0, 0]) for s in steps]
        for s in sl:
            s.next_to(head, DOWN, buff=0.12)
        with self.voiceover(
            "For three people, an envy-free procedure eluded mathematicians until about 1960, when John Selfridge and "
            "John Conway independently found this one. <bookmark mark='a'/>Ana, Ben and Cy; Cy values the cake "
            "evenly. <bookmark mark='b'/>Ana cuts three pieces equal by her own measure: at one ninth, and at just "
            "over a quarter. <bookmark mark='c'/>Ben trims his favourite, the big right piece, until it ties with his "
            "second best, and the trimmings are set aside. <bookmark mark='d'/>Now Cy chooses first, and takes the "
            "middle piece. Ben must take the trimmed piece if it is left, and it is. Ana takes the last, which is "
            "worth a third to her, as all three were. <bookmark mark='e'/>Then the trimmings. Since Ben took the "
            "trimmed piece, Cy cuts the trimmings into three, equal by his measure, and they choose in the order Ben, "
            "Ana, Cy."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(x) for x in lanes], FadeIn(whole))
            vo.wait_until("b")
            self.play(FadeIn(sl[0]), Create(cuts1))
            vo.wait_until("c")
            self.play(FadeOut(sl[0]), FadeIn(sl[1]), Create(trim))
            self.play(TransformFromCopy(whole[2], trimmings))
            vo.wait_until("d")
            self.play(FadeOut(sl[1]), FadeIn(sl[2]), FadeOut(whole[0]), FadeOut(whole[1]), FadeOut(whole[2]),
                      FadeIn(first[1]))
            self.play(FadeIn(first[2]))
            self.play(FadeIn(first[0]))
            vo.wait_until("e")
            self.play(FadeOut(sl[2]), FadeIn(sl[3]), Create(cuts2))
            self.play(FadeOut(trimmings), LaggedStart(*[FadeIn(second[i]) for i in (1, 0, 2)], lag_ratio=0.5))
        self.clear_scene()
        worth = d["worth"]
        head = label(r"What each thinks each bundle is worth", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"", r"\text{Ana's bundle}", r"\text{Ben's bundle}", r"\text{Cy's bundle}"]
        cells = [[label(rf"by {names[i]}'s measure", font_size=20, color=cols[i])] +
                 [label(f"{worth[i][j]:.3f}", font_size=22, color=GOAL if i == j else WHITE) for j in range(3)]
                 for i in range(3)]
        grid = ValueGrid(hd, cells, col_w=[3.4, 2.4, 2.4, 2.4], cell_h=0.7, font_size=20).move_to([0, 0.7, 0])
        boxes = VGroup(*[SurroundingRectangle(grid.cell[i][i + 1], color=GOAL, buff=0.1) for i in range(3)])
        foot = stack([(r"every row's largest entry is on the diagonal: \ no one envies anyone", GOAL),
                      (r"each bundle is two pieces: \ a share of the first cut, \ and a share of the trimmings", GREY_A)],
                     font_size=21, buff=0.2).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The Reasoner then computes what each person thinks each bundle is worth. <bookmark mark='a'/>By Ana's "
            "measure, her own bundle is worth about forty six hundredths, the others twenty and thirty four. By "
            "Ben's, his own is worth half, the others thirty seven and thirteen. By Cy's, his own is worth thirty "
            "seven hundredths, the others thirty two and thirty one. <bookmark mark='b'/>Every row's largest entry is "
            "on the diagonal. No one envies anyone, which is exactly what the procedure guarantees, whatever the "
            "three valuations are."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i])) for i in range(3)], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(Create(boxes), FadeIn(foot))
        self.clear_scene()

    def rent(self):
        d = load("rent")
        assert d["assign"] == [0, 1, 2] and d["prices"] == [1330.0, 935.0, 735.0]
        assert d["utility"] == [170.0, 165.0, 165.0] and d["min_utility"] == 165.0 and d["total_value"] == 3500.0
        V, p = d["values"], d["prices"]
        names, cols = [r"Ana", r"Ben", r"Cy"], [FAIR, MKT, COM]
        head = label(r"Splitting the rent \ (Gal, \ Mash, \ Procaccia and Zick, \ 2016)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        hd = [r"", r"\text{room 1}", r"\text{room 2}", r"\text{room 3}", r"\text{own surplus}",
              r"\text{best other}"]
        cells = []
        for i in range(3):
            other = max(V[i][r] - p[r] for r in range(3) if r != i)
            cells.append([label(names[i], font_size=21, color=cols[i])] +
                         [label(f"\\${V[i][r]:,.0f}", font_size=20) for r in range(3)] +
                         [label(f"\\${d['utility'][i]:,.0f}", font_size=20, color=GOAL),
                          label(f"\\${other:,.0f}" if other >= 0 else f"$-$\\${-other:,.0f}", font_size=20,
                                color=GREY_A)])
        cells.append([label(r"rent", font_size=20, color=MKT)] +
                     [label(f"\\${x:,.0f}", font_size=20, color=MKT) for x in p] +
                     [label(r"", font_size=20), label(r"", font_size=20)])
        grid = ValueGrid(hd, cells, col_w=[1.4, 1.8, 1.8, 1.8, 2.2, 2.2], cell_h=0.62, font_size=19).move_to([0, 0.9, 0])
        boxes = VGroup(*[SurroundingRectangle(grid.cell[i][i + 1], color=cols[i], buff=0.08) for i in range(3)])
        foot = stack([(r"values sum to the \$3,000 rent; \ assign rooms to maximize total value: \ \$3,500", GREY_A),
                      (r"prices sum to the rent; \ no one prefers another room at its price", FAIR),
                      (r"among envy-free prices, \ maximize the least surplus: \ \$165", GOAL)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The same ideas now divide real rent. <bookmark mark='a'/>Three housemates share a three bedroom flat "
            "whose rent is three thousand dollars. Each says what each room is worth to them, with values adding up "
            "to the rent. <bookmark mark='b'/>First, assign rooms to maximize the total value. The Reasoner tries all "
            "six assignments: Ana gets room one, Ben room two, Cy room three, worth three and a half thousand in all. "
            "Only such an assignment can be envy-free. <bookmark mark='c'/>Then choose prices adding up to the rent, "
            "so that no one would rather have another's room at its price. Many price vectors pass. Among them, pick "
            "the one that makes the worst-off housemate as well off as possible: rents of thirteen hundred and "
            "thirty, nine hundred and thirty five, and seven hundred and thirty five. <bookmark mark='d'/>Each "
            "housemate's surplus is at least a hundred and sixty five, and each one's best alternative is worse. This "
            "is the rule of Gal, Mash, Procaccia and Zick, of 2016, and it runs on the website Spliddit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for i in range(3) for c in grid.cell[i][:4]], FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(Create(boxes))
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[3]], FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[i][j]) for i in range(3) for j in (4, 5)], FadeIn(foot[2]))
        self.clear_scene()

    def history(self):
        head = label(r"From Steinhaus to Aziz--Mackenzie", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Steinhaus \ (1948)", r"the problem for $n$ people; \ Banach and Knaster's last diminisher guarantees each a proportional share", HIST),
                (r"Dubins--Spanier \ (1961)", r"the moving knife: \ the first to call stop takes the piece", FAIR),
                (r"Brams--Taylor \ (1995)", r"a finite envy-free procedure for any $n$, \ but with no bound on its steps", MKT),
                (r"Aziz--Mackenzie \ (2016)", r"the first bounded one: \ at most $n^{n^{n^{n^{n^{n}}}}}$ queries; \ at least order $n^2$ are needed \ (Procaccia, \ 2009)", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The mathematics began in occupied Poland. <bookmark mark='a'/>Hugo Steinhaus, in 1948, posed the problem "
            "for any number of people, and reported Stefan Banach and Bronisław Knaster's last diminisher procedure, "
            "which guarantees everyone a proportional share. <bookmark mark='b'/>Lester Dubins and Edwin Spanier's "
            "moving knife, of 1961: a knife sweeps slowly across the cake, and the first to call stop takes the "
            "piece. <bookmark mark='c'/>Steven Brams and Alan Taylor found a finite envy-free procedure for any "
            "number of people in 1995, but its number of steps has no bound. <bookmark mark='d'/>Haris Aziz and Simon "
            "Mackenzie gave the first bounded one in 2016, and its bound is a tower of six n's. Ariel Procaccia had "
            "shown in 2009 that at least on the order of n squared steps are needed."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def notions(self):
        head = label(r"What fair means, \ formally", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"proportional", r"each gets at least $1/n$ by her own measure", FAIR),
                (r"envy-free", r"no one prefers another's share: \ stronger, \ for three or more", GOAL),
                (r"equitable; \ efficient", r"equal values by each one's own measure; \ no division better for some, \ worse for none", LIB),
                (r"indivisible goods", r"one diamond, \ two heirs: \ EF1, \ envy-free up to one good \ (Lipton et al., \ 2004); \ max Nash welfare gives EF1 and efficiency \ (Caragiannis et al., \ 2016)", MKT),
                (r"Budish \ (2011)", r"approximate CEEI allocates courses at Wharton: \ Dworkin's auction, \ in production", COM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Fair division has its own vocabulary. <bookmark mark='a'/>A division is proportional if each person gets "
            "at least one nth by her own measure. <bookmark mark='b'/>It is envy-free if no one prefers another's "
            "share; for two people the two ideas coincide, and for more, envy-freeness is stronger. <bookmark "
            "mark='c'/>It is equitable if each gets the same value by her own measure, and efficient if no other "
            "division is better for some and worse for none. <bookmark mark='d'/>With indivisible goods, "
            "envy-freeness can be impossible: one diamond, two heirs. Its relaxation, envy-free up to one good, can "
            "always be met, and the division that maximizes the product of utilities, the maximum Nash welfare, "
            "achieves it together with efficiency. <bookmark mark='e'/>Eric Budish's approximate competitive "
            "equilibrium from equal incomes, of 2011, allocates courses at the Wharton School: Dworkin's auction, in "
            "production."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def matching(self):
        d = load("match")
        assert d["student_match"] == [2, 3, 1, 0] and len(d["rounds"]) == 5
        assert [r["held"] for r in d["rounds"]] == [[3, 1, None, 0], [3, 2, None, 0], [3, 2, None, 0],
                                                    [3, 2, None, 1], [3, 2, 0, 1]]
        st, sc = [r"Ana", r"Ben", r"Cy", r"Dee"], [r"W", r"X", r"Y", r"Z"]
        cols = [FAIR, MKT, COM, LIB]
        head = label(r"Deferred acceptance \ (Gale and Shapley, \ 1962)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sp = VGroup(*[label(rf"{st[i]}: \ $" + r" \succ ".join(sc[j] for j in d["student_prefs"][i]) + "$",
                            font_size=20, color=cols[i]) for i in range(4)]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        cp = VGroup(*[label(rf"{sc[j]}: \ " + r" $\succ$ ".join(st[i] for i in d["school_priority"][j]),
                            font_size=20, color=GREY_A) for j in range(4)]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        sp_t = label(r"students rank schools", font_size=20, color=CONN)
        cp_t = label(r"schools rank students", font_size=20, color=CONN)
        VGroup(sp_t, sp).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([-3.4, 1.65, 0])
        VGroup(cp_t, cp).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([3.3, 1.65, 0])
        hd = [r"\text{school}"] + [rf"\text{{round {k + 1}}}" for k in range(5)]
        cells = []
        for j in range(4):
            row = [label(sc[j], font_size=20, color=GREY_A)]
            for k, r in enumerate(d["rounds"]):
                h = r["held"][j]
                new = str(j) in r["proposals"] and h in r["proposals"][str(j)]
                row.append(label(st[h] if h is not None else r"--", font_size=19,
                                 color=(cols[h] if new else GREY_B) if h is not None else GREY_D))
            cells.append(row)
        grid = ValueGrid(hd, cells, col_w=[1.4] + [1.6] * 5, cell_h=0.46, font_size=18).move_to([0, -1.6, 0])
        foot = label(r"held, \ not accepted: \ a school trades up whenever a better applicant arrives", font_size=20,
                     color=GOAL).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Some goods cannot be divided or priced: places in schools, kidneys, medical residencies. For these, the "
            "Reasoner builds David Gale and Lloyd Shapley's deferred acceptance algorithm, of 1962. <bookmark "
            "mark='a'/>Four students rank four schools, each with one seat. <bookmark mark='b'/>Each school ranks the "
            "students, by its priorities. <bookmark mark='c'/>In the first round, every student applies to her "
            "favourite school. Each school holds its best applicant so far and rejects the rest; nothing is final. "
            "<bookmark mark='d'/>Rejected students apply to their next choice, and schools trade up whenever a better "
            "applicant arrives: in round two, Cy displaces Ben at school X; in round four, Ben displaces Ana at Z. "
            "<bookmark mark='e'/>After five rounds everyone holds a seat: Ana at Y, Ben at Z, Cy at X, Dee at W."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sp_t), FadeIn(sp))
            vo.wait_until("b")
            self.play(FadeIn(cp_t), FadeIn(cp))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(grid.cell[j][0]) for j in range(4)])
            self.play(*[FadeIn(grid.cell[j][1]) for j in range(4)])
            vo.wait_until("d")
            for k in range(2, 5):
                self.play(*[FadeIn(grid.cell[j][k]) for j in range(4)], run_time=0.6)
            vo.wait_until("e")
            self.play(*[FadeIn(grid.cell[j][5]) for j in range(4)], FadeIn(foot))
        self.clear_scene()

    def stability(self):
        d = load("match")
        assert d["matchings"] == 24 and len(d["stable"]) == 3
        assert d["student_ranks"] == [2, 3, 2, 1] and d["school_side_ranks"] == [3, 4, 4, 1]
        assert d["student_optimal"] and d["worst_for_students"]
        st, sc = [r"Ana", r"Ben", r"Cy", r"Dee"], [r"W", r"X", r"Y", r"Z"]
        cols = [FAIR, MKT, COM, LIB]
        nth = {1: r"1st", 2: r"2nd", 3: r"3rd", 4: r"4th"}
        head = label(r"Stable matchings: \ all 24 checked", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{stable matching}"] + [rf"\text{{{s}}}" for s in st]
        cells = []
        for m, rk in zip(d["stable"], d["stable_ranks"]):
            tag = (r"students propose" if m == d["student_match"] else
                   r"schools propose" if m == d["school_match"] else r"in between")
            cells.append([label(tag, font_size=19, color=GOAL if m == d["student_match"] else GREY_A)] +
                         [label(rf"{sc[m[i]]} \ ({nth[rk[i]]})", font_size=19, color=cols[i]) for i in range(4)])
        grid = ValueGrid(hd, cells, col_w=[3.2, 1.9, 1.9, 1.9, 1.9], cell_h=0.6, font_size=19).move_to([0, 1.2, 0])
        foot = stack([(r"stable: \ no student and school both prefer each other to what they got", GREY_A),
                      (r"students propose: \ the best stable matching for every student at once", GOAL),
                      (r"and no student can gain by misreporting \ (Dubins--Freedman, \ 1981; \ Roth, \ 1982)", LIB),
                      (r"New York \ (2003), \ Boston \ (2005): \ Abdulkadiroğlu, \ Pathak and Roth; \ Nobel prize, \ "
                       r"Roth and Shapley \ (2012)", MKT)],
                     font_size=20, buff=0.2).move_to([0, -1.75, 0])
        with self.voiceover(
            "Is the result fair? <bookmark mark='a'/>A matching is stable if no student and school would both rather "
            "have each other than what they got: there is no blocking pair, and so no justified envy. The Reasoner "
            "checks all twenty four matchings, and exactly three are stable. <bookmark mark='b'/>Gale and Shapley "
            "proved that deferred acceptance always finds a stable matching, and that when the students propose, it "
            "is the best stable matching for every student at once. Here the students get their second, third, second "
            "and first choices; when the schools propose instead, they get their third, fourth, fourth and first. "
            "<bookmark mark='c'/>Proposing students also cannot gain by misreporting their preferences. <bookmark "
            "mark='d'/>New York City has assigned high school places this way since 2003, and Boston since 2005, with "
            "designs by Atila Abdulkadiroğlu, Parag Pathak and Alvin Roth; Roth and Shapley shared the Nobel prize in "
            "economics in 2012."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i])) for i in range(3)], lag_ratio=0.4), FadeIn(foot[0]))
            vo.wait_until("b")
            i = d["stable"].index(d["student_match"])
            self.play(Create(SurroundingRectangle(VGroup(*grid.cell[i]), color=GOAL, buff=0.08)), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot[3]))
        self.clear_scene()
