from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


def hand(cards, color=WHITE, w=0.36, h=0.5, font_size=20):
    g = VGroup()
    for c in cards:
        r = RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color=color, stroke_width=2,
                             fill_color="#0B0F17", fill_opacity=1)
        g.add(VGroup(r, label(str(c), font_size=font_size, color=color).move_to(r)))
    return g.arrange(RIGHT, buff=0.06)


class Russian(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"A secret told in public", r"Can two people share a secret in front of a third?",
                            lit=(), part=PART)
        with self.voiceover("Chapter ten. A secret told in public."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.setup_()
        self.solution()

    def setup_(self):
        d = load("russian")
        head = label(r"The Russian cards problem", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        who = label(r"Moscow Mathematical Olympiad, \ 2000; \ van Ditmarsch (2003)", font_size=21,
                    color=GREY_B).next_to(head, DOWN, buff=0.15)
        ha = VGroup(hand([0, 1, 2], AG["a"]), label(r"Ann", font_size=22, color=AG["a"])).arrange(DOWN, buff=0.15)
        hb = VGroup(hand([3, 4, 5], AG["b"]), label(r"Bob", font_size=22, color=AG["b"])).arrange(DOWN, buff=0.15)
        hc = VGroup(hand([6], AG["c"]), label(r"Cath", font_size=22, color=AG["c"])).arrange(DOWN, buff=0.15)
        hands = VGroup(ha, hb, hc).arrange(RIGHT, buff=1.6).move_to([0, 1.1, 0])
        rows = VGroup(
            label(r"seven cards: \ Ann and Bob get three each, \ Cath gets one; \ everyone knows this", font_size=22),
            label(rf"{d['all_deals']} possible deals; \ each sees only her own hand", font_size=22, color=GREY_A),
            label(r"Ann and Bob must learn each other's hands, \ by public announcements only", font_size=22,
                  color=GOAL),
            label(r"and Cath, \ who hears everything, \ must not learn of any card who holds it", font_size=22,
                  color=BAD)).arrange(DOWN, buff=0.22).move_to([0, -1.3, 0])
        naive = label(r"`I hold 0, 1, 2': \ Bob learns, \ but so does Cath", font_size=21, color=GREY_B).to_edge(
            DOWN, buff=0.3)
        assert not d["naive"]["outright"]["cath_learns_nothing"]
        with self.voiceover(
            "Here is a puzzle that looks impossible after the last chapters, set at a Moscow mathematical olympiad "
            "in 2000 and analysed by Hans van Ditmarsch. <bookmark mark='a'/>Seven cards, numbered zero to six. Ann "
            "and Bob draw three each; Cath gets the last one. Everyone knows the procedure, and each sees only her "
            "own hand. <bookmark mark='b'/>There are a hundred and forty possible deals. <bookmark mark='c'/>Ann and "
            "Bob want to learn each other's hands, but they can only speak in public, <bookmark mark='d'/>and Cath, "
            "who hears everything, must not learn, of any single card, who holds it. <bookmark mark='e'/>Ann cannot "
            "just say her hand: Cath would learn everything. Is there anything Ann can say that tells Bob all, and "
            "Cath nothing?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(hands), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(naive))
        self.clear_scene()

    def solution(self):
        d = load("russian")
        head = label(r"Ann's announcement: \ seven hands, \ one of them hers", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        hs = VGroup(*[hand(h, COMMON if h == [0, 1, 2] else WHITE, w=0.32, h=0.44, font_size=18)
                      for h in d["hands"]]).arrange_in_grid(rows=2, buff=(0.45, 0.3)).move_to([0, 1.6, 0])
        fano = label(r"the lines of the Fano plane: \ any two hands share exactly one card", font_size=20,
                     color=GREY_B).next_to(hs, DOWN, buff=0.2)
        rows = VGroup(
            VGroup(label(r"Bob, \ holding 3, 4, 5, \ finds exactly one hand avoiding his cards", font_size=22),
                   mark(d["bob_learns"], 26)).arrange(RIGHT, buff=0.3),
            VGroup(label(rf"the Reasoner checks all {d['deals']} deals consistent with the announcement: \ Bob "
                         r"always learns", font_size=21, color=GREY_A), mark(d["bob_learns"], 24)).arrange(
                RIGHT, buff=0.3),
            VGroup(label(rf"Cath, \ holding {d['cath_card']}, \ still sees {len(d['cath_view'])} hands: \ every card "
                         r"is in some, \ and missing from others", font_size=21), mark(d["cath_learns_nothing"], 24)
                   ).arrange(RIGHT, buff=0.3),
            label(r"then Bob announces: \ `Cath holds 6'. \ Ann learns Bob's hand; \ Cath learns nothing new",
                  font_size=22, color=OK),
            label(r"a secret shared in public, \ by knowing exactly what the eavesdropper can and cannot infer",
                  font_size=23, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -1.4, 0])
        with self.voiceover(
            "There is. <bookmark mark='a'/>Ann announces: my hand is one of these seven. Her real hand is among them, "
            "and the seven are the lines of the Fano plane, the smallest projective plane: any two of them share "
            "exactly one card. <bookmark mark='b'/>Bob, holding three, four, five, looks for the hands that avoid all "
            "his cards, and finds exactly one: zero one two. <bookmark mark='c'/>The Reasoner checks every one of the "
            "twenty-eight deals consistent with Ann's announcement: in all of them, Bob learns Ann's hand. "
            "<bookmark mark='d'/>Cath, holding six, can rule out the three hands containing six, and is left with "
            "four. Every card other than six appears in some of those and is missing from others, so for no card "
            "does she learn who holds it; again the Reasoner checks every deal. <bookmark mark='e'/>Then Bob "
            "announces Cath's card, which Cath already knew. Now Ann knows Bob's hand, and Cath has learned nothing. "
            "<bookmark mark='f'/>A secret has been shared in public, by reasoning exactly about what the eavesdropper "
            "can and cannot infer. Epistemic logic has become a tool for designing protocols."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h) for h in hs], lag_ratio=0.15), FadeIn(fano))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
