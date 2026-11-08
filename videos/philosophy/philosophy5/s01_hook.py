from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.strains()
        self.preview()
        self.objectives()

    def title(self):
        t = part_title(PART)
        two = VGroup(MathTex(r"\{\, 0,\ 1 \,\}", font_size=60, color=GREY_A),
                     MathTex(r"\longrightarrow", font_size=50, color=GREY_C),
                     MathTex(r"\{\, 0,\ \tfrac12,\ 1 \,\}", font_size=60, color=HALF),
                     MathTex(r"\longrightarrow", font_size=50, color=GREY_C),
                     MathTex(r"[0, 1]", font_size=60, color=OK)).arrange(RIGHT, buff=0.4).next_to(t, DOWN, buff=0.8)
        with self.voiceover(
            "Parts 2, 3 and 4 kept one rule fixed: every sentence is true or false, and nothing else. "
            "<bookmark mark='a'/>This part asks what happens when we let go of it. Three values, four, seven, or a "
            "whole continuum. <bookmark mark='b'/>It sounds like a technicality. It is not: the reasons for letting "
            "go come from the future, from paradox, from inconsistent data, from physics, and above all from a "
            "puzzle about a heap of sand that is two and a half thousand years old and still unsolved."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in two], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(two[2], color=HALF), Indicate(two[4], color=OK))
        self.clear_scene()

    def strains(self):
        head = label(r"Five places where two values strain", font_size=34, color=CONN).to_edge(UP, buff=0.45)
        rows = [(r"the future", r"`there will be a sea battle tomorrow': \ true \textit{now}?", r"Part 4"),
                (r"vagueness", r"`a man with 4{,}000 hairs is bald': \ true? \ false?", r"Chapters 10--13"),
                (r"paradox", r"`this sentence is false'", r"Part 8"),
                (r"inconsistent data", r"two sensors: \ `the door is open', \ `the door is not open'", r"Chapters 3, 6"),
                (r"physics", r"`the photon passes the filter': \ quantum propositions", r"Chapter 15")]
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 1.9 - 0.95 * i
            ra = label(a, font_size=28, color=GOAL)
            rb = label(b, font_size=24)
            rc = label(c, font_size=20, color=GREY_B)
            ra.move_to([-6.2 + ra.width / 2, y, 0])
            rb.move_to([-3.1 + rb.width / 2, y, 0])
            rc.move_to([6.4 - rc.width / 2, y - 0.32, 0])
            tab.add(VGroup(ra, rb, rc))
        with self.voiceover(
            "Here are the five pressures. <bookmark mark='a'/>The future: is 'there will be a sea battle tomorrow' "
            "already true today? Part 4 met Aristotle's worry. <bookmark mark='b'/>Vagueness: a man with four "
            "thousand hairs on his head. Is he bald? Neither answer seems right. <bookmark mark='c'/>Paradox: "
            "'this sentence is false', which is true if and only if it is false; Part 8 is devoted to it. "
            "<bookmark mark='d'/>Inconsistent data: two sensors disagree about whether a door is open, and a "
            "classical database that believes both believes everything. <bookmark mark='e'/>And physics: in the "
            "quantum world, propositions about where a particle is combine in ways that break a classical law."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def preview(self):
        d = load("sorites")
        n = 21
        heads = men_row([None] * n, width=12.0, r=0.2, y=0.6)
        ab = label(r"no hair: \ bald", font_size=22, color=OK).next_to(heads[0], DOWN, buff=0.35).align_to(
            heads[0], LEFT)
        bb = label(r"a full head: \ not bald", font_size=22, color=BAD).next_to(heads[-1], DOWN, buff=0.35).align_to(
            heads[-1], RIGHT)
        prem = label(r"and one hair never turns a bald man into a man who is not", font_size=26,
                     color=GREY_A).next_to(heads, DOWN, buff=1.2)
        res = label(rf"the Reasoner: \ {d['big']['premises']} premises for {d['big']['n'] + 1} men, \ "
                    r"classically inconsistent, \ and every one is needed", font_size=24, color=BAD).next_to(
            prem, DOWN, buff=0.45)
        wall_ = label(r"this part's brick in the Wall: \ the sorites", font_size=26, color=P.WALL).to_edge(DOWN,
                                                                                                 buff=0.4)
        with self.voiceover(
            "Here is the heap, in its bald form. <bookmark mark='a'/>Line up men by the number of hairs on their "
            "heads, from none to a full head. <bookmark mark='b'/>The first is bald, the last is not. "
            "<bookmark mark='c'/>And a single hair never makes the difference: if a man is bald, so is the man with "
            "one more hair. <bookmark mark='d'/>Each claim looks undeniable. Together, in classical logic, they are "
            f"inconsistent: the Reasoner checks all {d['big']['premises']} premises for {d['big']['n'] + 1} men and "
            "finds no way to make them all true. Yet drop any single one, and the rest are consistent. "
            "<bookmark mark='e'/>That is this part's brick in the Wall."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(h, scale=0.6) for h in heads], lag_ratio=0.06), run_time=2.5)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(heads[0].face.animate.set_stroke(OK).set_fill(OK, 0.3), FadeIn(ab),
                      heads[-1].face.animate.set_stroke(BAD).set_fill(BAD, 0.3), FadeIn(bb))
            vo.wait_until("c")
            self.play(FadeIn(prem))
            vo.wait_until("d")
            self.play(FadeIn(res))
            vo.wait_until("e")
            self.play(FadeIn(wall_))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"logical matrices: \ Łukasiewicz, Kleene, Bochvar; \ gaps (K3) and gluts (LP)",
            r"Belnap and Dunn's four values; \ the catuṣkoṭi; \ the Jaina seven predications",
            r"paraconsistency, \ relevance, \ and a preview of intuitionistic logic",
            r"degrees of truth: \ t-norms, \ and a fuzzy controller that stops a train",
            r"the sorites; \ supervaluations, degrees, a sharp unknowable line, \ and higher-order vagueness",
            r"linear logic as a logic of resources; \ quantum logic",
            r"what makes a consequence logical; \ one logic or many?",
        ], font_size=25)
        with self.voiceover(
            "So: <bookmark mark='a'/>first the machinery, tables with more than two values, and the two "
            "opposite ways of adding a third value: a gap or a glut. <bookmark mark='b'/>Then four values, which "
            "turn out to describe a computer that hears conflicting reports, and also a pattern of argument that is "
            "two thousand years old in India. <bookmark mark='c'/>Logics that tolerate contradiction, that demand "
            "relevance, and a first look at a logic of proof instead of truth. <bookmark mark='d'/>Degrees of truth, "
            "and a fuzzy controller we build that brings a train smoothly to a stop. <bookmark mark='e'/>Then the "
            "heap itself, and four theories of vagueness, computed side by side. <bookmark mark='f'/>Logics of "
            "resources and of quantum mechanics. <bookmark mark='g'/>And finally the question underneath it all: "
            "what makes an argument logically valid, and is there only one right logic?"
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
