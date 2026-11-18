from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403


class Devices(VoiceoverScene):
    def construct(self):
        card(self, 11, r"How we will know", r"What will the series build, \ and how will it keep itself honest?",
             "Chapter eleven. How we will know.", scale=("market", "nation"), horizon=("a decade",))
        self.agora()
        self.island_()
        self.facts_()
        self.dials_()
        self.tags()

    # ------------------------------------------------------------------
    def agora(self):
        mods = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.85, corner_radius=0.1, stroke_color=E.AGORA,
                                                stroke_width=2, fill_color=E.AGORA, fill_opacity=0.12),
                               label(n, font_size=24, color=WHITE), label(w, font_size=17, color=GREY_A))
                        for n, w in ((r"market", r"cards, schedules, double auctions"),
                                     (r"crusoe", r"frontiers, the margin, Ricardo"),
                                     (r"signals", r"Hayek's tin"))])
        for m in mods:
            m[1].move_to(m[0].get_center() + UP * 0.14)
            m[2].move_to(m[0].get_center() + DOWN * 0.2)
        mods.arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        future = VGroup(*[RoundedRectangle(width=1.0, height=0.5, corner_radius=0.08, stroke_color=GREY_D,
                                           stroke_width=1.5) for _ in range(12)]).arrange(RIGHT, buff=0.12)
        future.next_to(mods, DOWN, buff=0.5)
        fl = label(r"one more mechanism in each part: \ games, auctions, banks, a central bank, a hundred thousand "
                   r"households", font_size=22, color=GREY_B).next_to(future, DOWN, buff=0.2)
        head = VGroup(label(r"Agora", font_size=54, color=E.AGORA), label(r"the economy the series builds, \ in code",
                                                                          font_size=26, color=GREY_A))
        head.arrange(DOWN, buff=0.15).to_edge(UP, buff=0.5)
        rule = label(r"each piece checked against something it did not compute itself", font_size=24,
                     color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The series builds an economy, in code, one mechanism at a time. It's called Agora, the Greek word for "
            "the gathering place that became the market. <bookmark mark='a'/> So far it has three modules: the "
            "market of the pit, the islanders' frontiers and Ricardo's trade, and Hayek's tin market. "
            "<bookmark mark='b'/> Each part adds another: games, auctions, a bank that can be run on, a central "
            "bank, a hundred thousand households with different incomes. <bookmark mark='c'/> And every piece is "
            "checked against something it didn't compute itself: a formula, a second method, a published table."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in mods], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(future, lag_ratio=0.1), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.clear_scene()

    def island_(self):
        isl = island_shape(6.0, 3.0).move_to([-3.2, 0.2, 0])
        cast = VGroup(*[islander(k, 0.6, name=True, font_size=16) for k in island.CAST]).arrange(RIGHT, buff=0.3)
        cast.move_to(isl.get_center())
        head = VGroup(label(r"The Island", font_size=48, color=E.ISLAND),
                      label(r"Agora, run as one world with a cast", font_size=24, color=GREY_A))
        head.arrange(DOWN, buff=0.12).to_corner(UL, buff=0.45)
        ax = axes([0, 10], [1.0, 3.5], x_length=4.6, y_length=3.0, xticks=[0, 5, 10], yticks=[1, 2, 3],
                  xlabel=r"quantity", font_size=16, center=[3.6, -0.2, 0])
        pit = load("pit")
        truth = step_curve(ax.ax, pit["steps"]["demand"], E.TRUTH, 3)
        truth = DashedVMobject(truth, num_dashes=40)
        rng = np.random.default_rng(3)
        est = VGroup(*[Dot(ax.ax.c2p(q, 3.4 - 0.2 * q + rng.normal(0, 0.15)), radius=0.05, color=WHITE)
                       for q in np.linspace(0.5, 9.5, 14)])
        tl = label(r"the truth, planted: \ known", font_size=20, color=E.TRUTH).next_to(ax.ax, UP, buff=0.15)
        el = label(r"a method's estimate: \ graded", font_size=20, color=WHITE).next_to(tl, DOWN, buff=0.05)
        tag = illustrative_tag(r"illustrative: how the Island grades a method (Part 4 does it with real runs)",
                               font_size=17)
        with self.voiceover(
            "Agora runs as one world, with a cast that persists from part to part: the Island. Crusoe and Friday "
            "are here already. In Part two a village comes ashore and opens a fish market. Later it gets a bank, a "
            "central bank, and a second island with its own money. <bookmark mark='a'/> The point of the Island is "
            "this. In the real economy the truth is hidden: nobody knows the true demand curve for anything. On the "
            "Island the truth is planted, and known. So when the series tries a method for measuring something, it "
            "can grade the method against the truth, and show you where it fails. Everything from the Island is "
            "labelled simulated."
        ) as vo:
            self.play(FadeIn(head), FadeIn(isl), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cast], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(tag))
            self.play(Create(truth), FadeIn(tl))
            self.play(LaggedStart(*[FadeIn(e, scale=0.5) for e in est], lag_ratio=0.1), FadeIn(el))
        self.clear_scene()

    def facts_(self):
        groups = facts.GROUPS
        counts = {g: sum(1 for f in facts.FACTS if f.group == g) for g in groups}
        items = [(g, rf"{counts[g]} facts", E.ACCENT if g in ("markets", "growth") else GREY_B) for g in groups]
        pc = point_cards(items, width=12.4, cols=4, font_size=22).move_to(DOWN * 0.2)
        head = VGroup(label(r"The Facts", font_size=48, color=E.ACCENT),
                      label(rf"{len(facts.FACTS)} regularities any account of an economy has to reproduce",
                            font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.5)
        cols = label(r"three columns each: \ your guess \ \textperiodcentered \ the data \ \textperiodcentered \ "
                     r"Agora", font_size=24, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"The Facts. There are {len(facts.FACTS)} of them, fixed for the whole series: regularities that any "
            "account of an economy has to reproduce, from Engel's law about food budgets to the shape of a "
            "recession and the gravity of trade. <bookmark mark='a'/> You've seen two today: double auctions "
            "converge, and income was flat for millennia before it rose. <bookmark mark='b'/> Each fact gets your "
            "guess first, then the data, then what Agora does. In the last part, Agora sits the whole list, and "
            "the scorecard shows what the economy we built can and cannot do."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in pc.cards], lag_ratio=0.15), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(cols))
        self.clear_scene()

    def dials_(self):
        rows = dials.board()
        b = dial_board(rows[:12], cols=6, radius=0.5, font_size=15).to_edge(UP, buff=1.3)
        head = VGroup(label(r"The Dials", font_size=48, color=E.ACCENT),
                      label(rf"{len(dials.DIALS)} numbers economics runs on, \ each with its estimates, \ how each "
                            r"was identified, \ and the date it was checked", font_size=22, color=GREY_A))
        head.arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        legend_ = VGroup(*[VGroup(Dot(radius=0.06, color=c), label(k, font_size=16, color=c)).arrange(RIGHT, buff=0.08)
                           for k, c in list(DESIGN_COLOR.items())[:8]]).arrange(RIGHT, buff=0.3)
        legend_.next_to(b, DOWN, buff=0.4)
        ll = label(r"each estimate, a tick, \ in the colour of its design", font_size=20, color=GREY_B).next_to(
            legend_, DOWN, buff=0.15)
        with self.voiceover(
            "The Dials, named after Hayek's engineer watching the hands of a few dials. Economics runs on a few "
            "dozen key numbers: how much people cut back when a price rises, how much of a windfall they spend, how "
            "many jobs a minimum wage costs or doesn't, what a tax raises. <bookmark mark='a'/> Each one is a dial, "
            "empty today, with the part that first measures it. <bookmark mark='b'/> When a dial is filled, every "
            "estimate on it is a tick, coloured by how it was found: a randomized trial, a natural experiment, a "
            "structural model, a calibration. And the dial says how far the estimates agree, and when it was last "
            "checked. <bookmark mark='c'/> One more device: once a part, a dated prediction gets scored against what "
            "happened. You saw the first today. Right calls and wrong calls are both shown."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in b], lag_ratio=0.08), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(legend_), FadeIn(ll))
        self.clear_scene()

    def tags(self):
        rows = VGroup(*[VGroup(t, label(d, font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.5) for t, d in (
            (note(r"data: \ the source, and the date it was retrieved", font_size=26, color=E.SOURCE),
             r"from the Data Room"),
            (note(r"published: \ the paper or the book", font_size=26, color=E.SOURCE), r"cited"),
            (note(r"computed: \ Agora", font_size=26, color=E.AGORA), r"the model"),
            (note(r"simulated: \ the Island", font_size=26, color=E.ISLAND), r"a world we made"),
            (note(r"illustrative \ or \ schematic", font_size=26, color=GREY_B), r"made up, and said so"),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.2)
        head = heading(r"Every number on screen says where it came from")
        with self.voiceover(
            "And every number on screen says where it came from. <bookmark mark='a'/> Data carry their source and "
            "the date they were retrieved. Published results are cited. Agora's numbers say computed, the Island's "
            "say simulated, and anything made up for an example says so. If a part freezes its data on a date, the "
            "date is on screen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.4), run_time=3)
        self.clear_scene()
