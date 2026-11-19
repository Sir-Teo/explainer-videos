from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.early()
        self.exploding()
        self.clearinghouse()
        self.today()
        self.question()
        self.title()
        self.objectives()

    def early(self):
        r = load("roth")["interns"]
        hc = history_card(r["two_years_before_by"], r"American hospitals and medical students", r"interns hired two "
                          r"years before they graduate", color=REJECT, width=11.2, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"each hospital wanted the best students, \ so it made offers a little earlier than the rest",
                  font_size=24),
            label(r"so the others went earlier still: \ the market unravelled", font_size=24, color=REJECT),
            label(r"a hospital hiring in the second year can't tell who is good; \ a student can't tell what they "
                  r"want", font_size=23, color=GREY_A),
            label(r"a student with an A in anatomy signs up for surgery, \ and learns a year later they faint at "
                  r"blood", font_size=23, color=GREY_A),
            label(rf"{r['schools_withhold_info']}: \ the medical schools stop sending grades and letters before a "
                  r"fixed date", font_size=24, color=HELD),
        ).arrange(DOWN, buff=0.36).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Roth, JPE 92(6) (1984); \ Roth, Nobel lecture (2012)", corner=DR, font_size=13)
        with self.voiceover(
            "By 1940, American hospitals were hiring their interns two years before the students graduated from "
            "medical school. <bookmark mark='a'/> Each hospital wanted the best students, so it made its offers a "
            "little earlier than the others. <bookmark mark='b'/> So the others went earlier still. Economists call "
            "it unravelling. <bookmark mark='c'/> A hospital hiring in a student's second year could not tell who "
            "would be good, and the student could not tell what they wanted. <bookmark mark='d'/> As Alvin Roth "
            "tells it, a student with an A in anatomy signs up to be a surgeon, and discovers a year later that they "
            "faint at the sight of blood. <bookmark mark='e'/> In 1945 the medical schools acted: they would send "
            "no grades and no letters before a fixed date."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, rr in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(rr, shift=UP * 0.1))
        self.clear_scene()

    def exploding(self):
        r = load("roth")["interns"]
        steps = VGroup(
            VGroup(label(r"1945", font_size=30, color=HELD), label(rf"offers stay open \\ {r['offer_days_1945']} days",
                                                                   font_size=22)).arrange(DOWN, buff=0.15),
            VGroup(label(r"1946", font_size=30, color=HELD), label(rf"offers stay open \\ {r['offer_days_1946']} days",
                                                                   font_size=22)).arrange(DOWN, buff=0.15),
            VGroup(label(r"by 1950", font_size=30, color=REJECT), label(r"twelve hours is \\ too long",
                                                                        font_size=22)).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=1.6).move_to(UP * 1.4)
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.25, color=GREY_B)
                          for i in range(2)])
        rows = VGroup(
            label(r"a student holds a third choice, \ and waits on a second choice's waiting list", font_size=23),
            label(r"while everyone waits, \ no waiting list moves: \ a chaotic last day", font_size=23,
                  color=GREY_A),
            label(r"so the deadline shrank, \ until offers came by telephone: \ yes or no, \ now", font_size=24,
                  color=REJECT),
            label(r"exploding offers: \ a market too congested to clear", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(steps, DOWN, buff=0.7)
        tag = published_tag(r"Roth, Nobel lecture (2012)", corner=DR, font_size=13)
        with self.voiceover(
            "It worked, and offers moved back to the final year. Then a new problem appeared. "
            "<bookmark mark='a'/> In 1945 the rule was that an offer stayed open for ten days. A student holding an "
            "offer from a third choice, and told by a second choice that an offer might come, would wait. "
            "<bookmark mark='b'/> With everyone waiting, no waiting list moved, and the tenth day was chaos. "
            "<bookmark mark='c'/> In 1946 the rule became eight days. By 1950 the hospitals thought twelve hours too "
            "long: offers came by telephone, to be answered on the spot. <bookmark mark='d'/> Exploding offers, in a "
            "market too congested to clear."
        ) as vo:
            self.play(FadeIn(steps[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[0]), FadeIn(steps[1]))
            self.play(GrowArrow(arrows[1]), FadeIn(steps[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def clearinghouse(self):
        hc = history_card(1952, r"the National Intern Matching Program", r"students rank hospitals; \ hospitals rank "
                          r"students; \ a procedure does the rest", color=STABLE, width=11.0, font_size=24
                          ).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"voluntary, \ yet within a few years nearly everyone went through it", font_size=24),
            label(r"run in the 1950s on card-sorting machines", font_size=23, color=GREY_A),
            label(r"1962: \ David Gale and Lloyd Shapley publish a puzzle about stable marriages", font_size=24,
                  color=PROPOSE),
            label(r"1984: \ Alvin Roth shows the hospitals had found the same algorithm, \ ten years earlier",
                  font_size=24, color=STABLE),
            label(r"2012: \ the Nobel prize, \ to Roth and Shapley", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.36).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Gale and Shapley, AMM 69(1) (1962); \ Roth, JPE 92(6) (1984)", corner=DR, font_size=13)
        with self.voiceover(
            "Then the doctors and hospitals did something remarkable. <bookmark mark='a'/> In 1952 they set up a "
            "clearinghouse. Students ranked the hospitals where they had interviewed, hospitals ranked the students, "
            "and a procedure did the rest. Joining was voluntary, yet within a few years nearly everyone went "
            "through it. <bookmark mark='b'/> In the 1950s it ran on card-sorting machines. <bookmark mark='c'/> In "
            "1962 two mathematicians, David Gale and Lloyd Shapley, published a puzzle about marriage: how to pair off "
            "men and women so that no two would rather be with each other. <bookmark mark='d'/> In 1984 Alvin Roth "
            "showed that the hospitals' procedure was Gale and Shapley's algorithm, found by trial and error ten "
            "years before the mathematicians. <bookmark mark='e'/> In 2012 Roth and Shapley shared the Nobel prize."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, rr in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(rr, shift=UP * 0.1))
        self.clear_scene()

    def today(self):
        rows = point_cards([
            (r"young doctors", r"tens of thousands of \\ residency places a year", STABLE),
            (r"school places", r"New York, \ Boston, \\ Denver, \ many more", SCHOOL),
            (r"kidneys", r"exchanges between pairs, \\ and long chains", KIDNEY),
            (r"university places", r"China's national \\ admissions", HELD),
            (r"refugees", r"placing families \\ where they'll find work", MECH),
            (r"never for money", r"prices are banned, \\ or simply don't work", REJECT),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
        head = label(r"markets where prices can't do the work", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Clearinghouses like it now run many markets. <bookmark mark='a'/> Tens of thousands of young doctors a "
            "year. Places at public schools, in New York, Boston, Denver and many other cities. Kidneys, swapped "
            "between patients and the donors who love them but cannot give to them. University places, across "
            "China. Homes for refugees. <bookmark mark='b'/> In every one, prices are banned, or simply cannot do "
            "the work: a school place, a kidney or a hospital job is not sold to the highest bidder."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards[:5]], lag_ratio=0.6), run_time=9)
            vo.wait_until("b")
            self.play(FadeIn(rows.cards[5], shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"can a rule make people want to tell the truth?", font_size=29, color=MECH),
            label(r"can it give an outcome nobody wants to break, \ with a pair who'd rather go off together?",
                  font_size=28, color=STABLE),
            label(r"and when the rules are wrong, \ what happens to a market?", font_size=29, color=REJECT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Part sixteen designed markets with prices. This part asks whether a market can be engineered when "
            "prices cannot do the work. <bookmark mark='a'/> Can a rule make it safe for people to say what they "
            "really want? <bookmark mark='b'/> Can it find an outcome nobody wants to break, with no pair who would "
            "rather go off together? <bookmark mark='c'/> And when the rules are wrong, what happens to a market?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, rr in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(rr, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = VGroup(*[islander(k, 0.9) for k in ("ana", "bo", "chidi", "dara")]).arrange(RIGHT, buff=0.35)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 17 \ $\cdot$ \ Markets by Design", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part seventeen: markets by design."):
            self.play(FadeIn(logo, shift=UP * 0.2), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IV \ $\cdot$ \ Failure and Design", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"rank three workshops under the Boston rule; \ mechanisms and the revelation principle",
            r"Vickrey, \ Clarke and Groves; \ Myerson and Satterthwaite's impossible bargain",
            r"stable matching, \ run on a board; \ who should propose; \ the residents' match",
            r"school choice; \ huts and kidneys; \ why markets fail to form; \ the assignment game",
            r"what a lottery reveals; \ a dial for schools; \ refugees and large markets",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Four. <bookmark mark='a'/> You'll rank three workshops under the rule Boston's "
            "schools once used, then meet mechanisms and the revelation principle. <bookmark mark='b'/> Vickrey, "
            "Clarke and Groves's way to make truth pay, and Myerson and Satterthwaite's proof that no bargain is "
            "perfect. <bookmark mark='c'/> Stable matching, run on a board; who should propose; and the redesign of "
            "the doctors' match. <bookmark mark='d'/> School choice; huts and kidneys; why markets fail to form; and "
            "matching with money. <bookmark mark='e'/> Then what a school lottery reveals, a dial for schools, and a "
            "frontier of refugees and very large markets."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, rr in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(rr, shift=RIGHT * 0.2))
        self.clear_scene()
