from __future__ import annotations

from videos.psychology.psych3.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.quantity()
        self.habits()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ is it a quantity at all?", r"What has the field still not settled "
                            r"about its own numbers?", lit=(), part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter fourteen. The frontier: is it a quantity at all?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def quantity(self):
        head = heading(r"The committee's question, still open")
        left = VGroup(
            label(r"Stevens, 1946", font_size=38, color=SCALE["interval"]),
            wrapped_label(r"Measurement is assigning numbers by a rule. \ Then say which kind of scale you have.",
                          5.7, 31, WHITE),
            wrapped_label(r"what the field adopted", 5.7, 26, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        right = VGroup(
            label(r"Michell, 1997", font_size=38, color=ERRC),
            wrapped_label(r"That an attribute has quantitative structure is a hypothesis. \ A definition cannot "
                          r"make it true, and the hypothesis is almost never tested.", 5.7, 31, WHITE),
            wrapped_label(r"the objection, still unanswered", 5.7, 26, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        pair = VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 1.05, 0])
        hard = VGroup(
            label(r"Why it is rarely tested", font_size=34, color=P.ACCENT),
            wrapped_label(r"The test of chapter 2 needs the order of the cells exactly. \ Real data give it with "
                          r"error, and a noisy table breaks the conditions even when a scale exists.", 12.0, 29,
                          WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The committee of 1940 never got its answer, and the honest state of things is that it still hasn't. "
            "<bookmark mark='a'/> Stevens's move was to define the problem away: any rule for assigning numbers "
            "is measurement, and the only question is which kind. Psychology adopted that, and it has been in "
            "every methods textbook since. <bookmark mark='b'/> In the nineteen-nineties the psychologist Joel "
            "Michell argued that this was a wrong turn. Whether an attribute like ability or "
            "anxiety is a quantity, with real magnitudes that stand in ratios, is a claim about the world. A "
            "definition can't make it true. And the field, he said, simply stopped asking. "
            "<bookmark mark='c'/> The test exists; you saw it in chapter two. The trouble is that it needs the "
            "order of the cells exactly, and real data only give it with error. A noisy table can fail the test "
            "when a scale really is there, and pass when it isn't. How to run the test properly on data with "
            "error is unsolved, and it's this part's research problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(hard, shift=UP * 0.15))
        self.clear_scene()

    def habits(self):
        d = archive.FLAKE_FRIED_2020.data
        head = heading(r"What happens to measures on the way to print")
        unit, x0 = 6.0, -4.6
        cap = label(rf"of {d['scales_reviewed']} scales in a sample of one leading journal's studies, 2014:", font_size=29,
                    color=GREY_A).move_to([x0 - 1.0, 2.05, 0], aligned_edge=LEFT)
        rows = VGroup()
        for i, (share, text) in enumerate(((d["no_source"], r"gave no source for the scale"),
                                           (d["no_item_count"], r"did not say how many items it had"),
                                           (d["no_response_scale"], r"did not give the response scale"))):
            y = 1.25 - 0.75 * i
            back = Rectangle(width=unit, height=0.46, stroke_color=GREY_D, stroke_width=1.5).move_to(
                [x0 + unit / 2, y, 0])
            bar = Rectangle(width=unit * share, height=0.46, stroke_width=0, fill_color=ERRC, fill_opacity=0.85)
            bar.move_to([x0 + unit * share / 2, y, 0])
            num = label(rf"{100 * share:.0f}\%", font_size=36, color=ERRC).next_to(back, LEFT, buff=0.25)
            txt = label(text, font_size=28, color=WHITE).next_to(back, RIGHT, buff=0.3)
            rows.add(VGroup(num, VGroup(back, bar), txt))
        more = VGroup(
            label(rf"{100 * d['emotion_no_development']:.0f}\% of {d['emotion_instances']} measures of emotion: \ "
                  r"no reference to earlier work, and no account of how they were made", font_size=27, color=WHITE),
            label(rf"one laboratory measure of aggression: \ scored in more than {d['crtt_ways']} ways across "
                  rf"{d['crtt_publications']} papers", font_size=27, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.9, 0])
        src = published_tag(archive.FLAKE_FRIED_2020.cite)
        with self.voiceover(
            "The second open matter is less philosophical, and more embarrassing. Everything in this part "
            "assumed that a measure is a fixed thing: these items, this response scale, scored this way. "
            "<bookmark mark='a'/> In 2020 Jessica Flake and Eiko Fried collected what's known about how measures "
            f"are actually reported. In a sample of studies from one leading journal, {100 * d['no_source']:.0f} "
            f"per cent of the scales came with no source. <bookmark mark='b'/> "
            f"{100 * d['no_item_count']:.0f} per cent didn't say how many items they had. <bookmark mark='c'/> In "
            f"research on emotion, {100 * d['emotion_no_development']:.0f} per cent of the measures came with no "
            "reference to earlier work and no account of how they'd been made. <bookmark mark='d'/> And one "
            f"laboratory measure of aggression had been scored in more than {d['crtt_ways']} different ways. They "
            "called these questionable measurement practices. If you can choose your items and your scoring "
            "after seeing the data, a reliability coefficient describes a test that never existed until the "
            "analysis. We come back to that kind of flexibility in the next part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(cap), FadeIn(rows[0][1][0]), FadeIn(rows[0][0]), GrowFromEdge(rows[0][1][1], LEFT),
                      FadeIn(rows[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1][1][0]), FadeIn(rows[1][0]), GrowFromEdge(rows[1][1][1], LEFT), FadeIn(rows[1][2]))
            self.play(FadeIn(rows[2][1][0]), FadeIn(rows[2][0]), GrowFromEdge(rows[2][1][1], LEFT), FadeIn(rows[2][2]))
            vo.wait_until("c")
            self.play(FadeIn(more[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(more[1], shift=UP * 0.1))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"What is open")
        items = (
            (r"Are psychological attributes quantities?",
             r"The conditions an order must meet are known. \ A way of testing them on data with error is not "
             r"agreed."),
            (r"How many sources of error, and how large is each?",
             r"Generalizability theory splits error into items, days, judges and their mixtures. \ Most of "
             r"psychology seldom uses it."),
            (r"Can the field's measures be made fixed and comparable?",
             r"Proposals for reporting them exist. \ Whether they change practice is being watched now."),
        )
        rows = VGroup()
        for i, (q, a) in enumerate(items, 1):
            num = label(rf"{i}", font_size=52, color=P.ACCENT)
            body = VGroup(label(q, font_size=36, color=WHITE), wrapped_label(a, 11.6, 27, GREY_A))
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            rows.add(VGroup(num, body).arrange(RIGHT, buff=0.4, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(head, DOWN, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        star = VGroup(label(r"$\star$ \ Research problem", font_size=28, color=P.ACCENT),
                      wrapped_label(r"You have each person's answers to each item, with error. \ Devise a test of "
                                    r"whether an additive scale lies behind them that is fair to both answers: "
                                    r"it should fail when there is none, and pass when there is one.", 12.4, 27,
                                    WHITE))
        star.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        box = SurroundingRectangle(star, color=P.ACCENT, buff=0.22, corner_radius=0.12, stroke_width=2)
        sp = VGroup(box, star).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Three things are open. <bookmark mark='a'/> One. Are psychological attributes quantities? We know "
            "what an order has to satisfy. We don't have an agreed way to check it on real, noisy data. "
            "<bookmark mark='b'/> Two. How many kinds of error does a score contain, and how big is each? "
            "There's a framework for that, called generalizability theory, which splits error into items, days, "
            "judges and their combinations in one analysis. It's fifty years old, and most of psychology "
            "still seldom uses it. <bookmark mark='c'/> Three. Can psychology's measures be made into fixed "
            "things that two laboratories can share? Proposals for reporting them now exist. Whether practice "
            "follows is being watched as we speak. <bookmark mark='d'/> And the research problem is the first "
            "of those. Given people's answers to items, with error, devise a test for an additive scale that's "
            "fair in both directions."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(sp, shift=UP * 0.2))
        self.clear_scene()
