from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"Two things fill the mind with ever new and increasing admiration and awe, \ the more often "
                       r"and steadily we reflect upon them: \ the starry heavens above me and the moral law within me.",
                       r"Immanuel Kant", r"\textit{Critique of Practical Reason} \ (1788)", width=9.6,
                       font_size=28).next_to(t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 34 showed that rational self-interest, left to itself, can leave everyone worse off, and asked "
            "which rules a society should choose. This part asks what makes any choice right. "
            "<bookmark mark='a'/>Immanuel Kant wrote that two things fill the mind with ever new admiration and awe: "
            "the starry heavens above, and the moral law within. <bookmark mark='b'/>Normative ethics tries to say "
            "what that law is. Three great theories answer, and each can be made precise enough to compute."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=DUTY, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        d = load("tetrad")
        sv = d["survey"]
        assert (sv["virtue ethics"], sv["deontology"], sv["consequentialism"]) == (0.370, 0.321, 0.306)
        head = label(r"Three questions, \ three theories", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"what is good?", r"consequentialism: \ the right act makes things go best \ (Bentham, \ Mill, \ "
                                   r"Sidgwick)", GOOD),
                (r"what is right?", r"deontology: \ some acts are required or forbidden whatever the consequences \ "
                                    r"(Kant, \ Ross)", DUTY),
                (r"how should I be?", r"virtue ethics: \ act as a person of good character would \ (Aristotle, \ "
                                      r"Confucius, \ Mencius)", VIRT)]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.4)
        bars = VGroup()
        for k, (n, col) in enumerate((("virtue ethics", VIRT), ("deontology", DUTY), ("consequentialism", GOOD))):
            w = 8.0 * sv[n]
            b = Rectangle(width=w, height=0.34, stroke_width=0, fill_color=col, fill_opacity=0.7)
            b.move_to([-3.0 + w / 2, -1.9 - 0.5 * k, 0])
            bars.add(VGroup(b, label(f"{n}: \\ {100 * sv[n]:.1f}\\%", font_size=17, color=col).next_to(b, RIGHT,
                                                                                                    buff=0.15)))
        cap = label(r"PhilPapers Survey 2020: \ normative ethics, \ accept or lean toward", font_size=16,
                    color=GREY_A).next_to(bars, UP, buff=0.15).align_to(bars, LEFT)
        with self.voiceover(
            "Three questions run through the part. <bookmark mark='a'/>What is good? Consequentialists say the right "
            "act is the one that makes things go best. <bookmark mark='b'/>What is right? Deontologists say some acts "
            "are required or forbidden whatever their consequences. <bookmark mark='c'/>And how should I be? Virtue "
            "ethicists say act as a person of good character would. <bookmark mark='d'/>In the PhilPapers survey of "
            "2020, philosophers split almost evenly: thirty seven percent virtue ethics, thirty two deontology, "
            "thirty one consequentialism. Each theory has cases it gets wrong, and that is this part's brick in "
            "the Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(cap), LaggedStart(*[GrowFromEdge(b[0], LEFT) for b in bars], lag_ratio=0.2),
                      *[FadeIn(b[1]) for b in bars])
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Bentham's ledger; \ Mill; \ Sidgwick; \ rules against calculation, \ simulated",
            r"theories of welfare; \ the experience machine",
            r"Harsanyi's theorem: \ nonlinear welfare functions broken, \ computed",
            r"equality, \ priority, \ maximin; \ the utility monster; \ Singer's pond, \ priced",
            r"Kant's formulas; \ a world of promises in which lying defeats itself; \ consent",
            r"universalizability tested; \ the murderer at the door",
            r"doing and allowing; \ the paradox of deontology \ (the Wall); \ the trolley Price List",
            r"Scanlon and Taurek; \ virtue and particularism; \ care; \ moral uncertainty",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Bentham's felicific calculus, built as a ledger, Mill and Sidgwick, and a "
            "simulation of when rules beat calculation. "
            "<bookmark mark='b'/>What is good for a person, and Nozick's experience machine. <bookmark mark='c'/>Harsanyi's "
            "theorem, which turns two mild axioms into utilitarianism, with its escape routes checked. "
            "<bookmark mark='d'/>Equality, priority and maximin, Nozick's utility monster, and Peter Singer's drowning "
            "child, with the demands of impartiality priced. <bookmark mark='e'/>Kant, "
            "a toy world of promises in which a universal lie destroys itself, and the formula of humanity as a "
            "test of consent. <bookmark mark='f'/>The test "
            "applied to famous maxims, including the ones it gets wrong, and the murderer at the door. "
            "<bookmark mark='g'/>Doing and allowing, the paradox of deontology, this part's brick in the Wall, and "
            "the trolley problem with its Price List. <bookmark mark='h'/>Scanlon's contractualism and whether the "
            "numbers count, virtue and the holism of reasons, the ethics of care, and what to do when you are unsure "
            "which theory is true."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
