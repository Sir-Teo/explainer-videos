from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.aisle()
        self.puzzle()
        self.question()
        self.title()
        self.objectives()

    def shelves(self, shares, colors, rng):
        """Three shelves of 30 boxes, coloured in proportion to the shares, in a shuffled order."""
        n = 90
        counts = [int(round(n * s / 100)) for s in shares]
        counts.append(n - sum(counts))
        kinds = np.repeat(np.arange(len(counts)), counts)
        rng.shuffle(kinds)
        boxes = VGroup()
        for k in kinds:
            h = rng.uniform(0.55, 0.8)
            col = (list(colors) + [GREY_D])[k]
            r = Rectangle(width=0.32, height=h, stroke_color=BLACK, stroke_width=1.0, fill_color=col,
                          fill_opacity=0.9)
            r.kind = int(k)
            boxes.add(r)
        rows = VGroup()
        for s in range(3):
            row = VGroup(*boxes[30 * s:30 * (s + 1)]).arrange(RIGHT, buff=0.04, aligned_edge=DOWN)
            board = Rectangle(width=row.width + 0.3, height=0.07, stroke_width=0, fill_color=GREY_B,
                              fill_opacity=0.8).next_to(row, DOWN, buff=0.0)
            rows.add(VGroup(row, board))
        rows.arrange(DOWN, buff=0.35)
        return boxes, rows

    def aisle(self):
        F = tables.CEREAL_FTC.data
        rng = np.random.default_rng(43)
        boxes, rows = self.shelves((F["kellogg"], F["gm"], F["gf"]), FIRM[:3], rng)
        rows.scale(0.92).move_to(LEFT * 1.6 + DOWN * 0.2)
        side = VGroup(
            label(r"America's cereal, \ 1980: \\ each box, \ about 1\% \\ of sales", font_size=19, color=WHITE),
            label(rf"Kellogg: \ about {F['kellogg']}\%", font_size=20, color=FIRM[0]),
            label(rf"General Mills: \ about {F['gm']}\%", font_size=20, color=FIRM[1]),
            label(rf"General Foods \ (Post): \\ about {F['gf']}\%", font_size=20, color=FIRM[2]),
            label(r"1972: \ the FTC alleges \\ a `shared monopoly'; \\ 1981: \ dismissed", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.CEREAL_FTC.tag + r"; \ shares as reported in 1980", corner=DR, font_size=11)
        with self.voiceover(
            "Walk down the cereal aisle of an American supermarket and you see dozens of brands, from flakes to "
            "puffs to clusters, in every colour. <bookmark mark='a'/> But look at who makes them. Around 1980, "
            f"Kellogg sold about {F['kellogg']} percent of all the cereal Americans bought, "
            f"<bookmark mark='b'/> General Mills about {F['gm']} percent, <bookmark mark='c'/> and General Foods, the "
            f"maker of Post, about {F['gf']} percent. <bookmark mark='d'/> In 1972 the Federal Trade Commission "
            "charged the biggest makers with sharing a monopoly: no explicit agreement, but prices kept high and "
            "rivals kept out by a flood of new brands. After nearly a decade of hearings, a judge dismissed the case "
            "in 1981, finding collusion unproved."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3), FadeIn(side[0]), FadeIn(tag),
                      run_time=2.0)
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                grp = [b for b in boxes if b.kind == k]
                self.play(FadeIn(side[k + 1]), *[b.animate.shift(UP * 0.12) for b in grp], run_time=0.8)
                self.play(*[b.animate.shift(DOWN * 0.12) for b in grp], run_time=0.4)
            vo.wait_until("d")
            self.play(FadeIn(side[4], shift=UP * 0.1))
        self.clear_scene()

    def puzzle(self):
        R = load("cereal")
        cards = point_cards([
            (r"high margins", rf"on the Island's aisle, \\ about {100 * R['true_avg']:.0f}\% of each price \\ is "
                              r"margin over \\ marginal cost", PRICE),
            (r"collusion?", r"firms agree, \\ openly or tacitly, \\ not to compete", LOSS),
            (r"or differentiation?", r"each brand a little \\ monopoly: \ no box \\ is a perfect \\ substitute",
             DEMAND),
            (r"the catch", r"nobody outside \\ the firms sees \\ their costs", HOLD),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"a puzzle with no costs in sight", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.NEVO_2001.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "The puzzle did not go away. <bookmark mark='a'/> Cereal makers earn large margins: on the Island's own "
            f"cereal aisle, which this part builds, about {say_pct(R['true_avg'], 0)} of each price is margin over "
            "the cost of making one more box. <bookmark mark='b'/> Is that collusion, firms agreeing, openly or "
            "tacitly, not to compete? <bookmark mark='c'/> Or is it differentiation: every brand a little "
            "monopoly, because no box is a perfect substitute for another, and each firm owning many brands that "
            "it prices together? <bookmark mark='d'/> The catch is that nobody outside the firms can see their "
            "costs. In 2001 Aviv Nevo answered the question without them. He estimated how shoppers substitute "
            "between brands, worked out what margins competition alone would produce, and found them close to "
            "the margins observed: no collusion was needed. His method came from a 1995 paper on cars, by Steven "
            "Berry, James Levinsohn and Ariel Pakes, famous for being hard to read. This part reads it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 36, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"does concentration mean market power, \ or efficiency?", font_size=26, color=LOSS),
            label(r"how do you estimate demand for hundreds of products?", font_size=26, color=DEMAND),
            label(r"from demand to markups, \ mergers and new goods", font_size=26, color=PRICE),
            label(r"from production data, \ and from counting firms in towns", font_size=26, color=THEORY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "So this part asks how you can tell whether a market is competitive when you cannot see anyone's "
            "costs. <bookmark mark='a'/> Does a concentrated industry mean market power, or just efficient firms "
            "that grew large? <bookmark mark='b'/> How do you estimate demand for hundreds of related products, "
            "with their prices tangled up in qualities you cannot measure? <bookmark mark='c'/> How do you go from "
            "demand to markups, to the effects of a merger, to the value of a new product? "
            "<bookmark mark='d'/> And what can production data, or a simple count of firms in towns of different "
            "sizes, reveal?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1947, 2027], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, PROFIT, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 43 \ $\cdot$ \ Measuring Market Power", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part forty-three: measuring market power."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IX \ $\cdot$ \ The Fields", font_size=40, color=E.ACCENT)
        sub = label(r"each part: \ one field of economics, \ its tools, \ and its open questions", font_size=24,
                    color=GREY_A).next_to(head, DOWN, buff=0.4)
        obj = objectives_card([
            r"structure, \ conduct, \ performance; \ a merger game; \ conduct identified",
            r"demand for differentiated products: \ logit, \ nests, \ random coefficients derived",
            r"BLP on the Island and on real cars; \ markups; \ Nevo's cereals; \ mergers and new goods",
            r"production functions; \ markups from production data; \ entry thresholds",
            r"two dials; \ merger review in practice; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This is the first part of Act Nine, the fields: each part takes one field of economics, its tools and "
            "its open questions, beginning with industrial organization. Here is the plan. <bookmark mark='a'/> "
            "The old way of reading market power from concentration, a game about two mergers, and how conduct can "
            "be identified. <bookmark mark='b'/> Demand for differentiated products, from the logit to random "
            "coefficients, derived. <bookmark mark='c'/> The estimator run on the Island's cars and on the real ones, "
            "then markups, Nevo's cereals, mergers and new goods. <bookmark mark='d'/> Production functions, "
            "markups from production data, and entry. <bookmark mark='e'/> Two dials, merger review in practice, "
            "and the frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeOut(sub), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
