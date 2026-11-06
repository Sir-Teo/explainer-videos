from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Email(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Almost common knowledge", r"Is very high mutual knowledge enough?", lit=(1989,),
                            part=PART)
        with self.voiceover("Chapter seven. Almost common knowledge."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.game()
        self.unravel()
        self.pbelief()

    def game(self):
        hc = history_card(1989, r"Ariel Rubinstein", r"`The Electronic Mail Game'", width=5.0,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"usually the enemy is strong: \ neither general should attack", font_size=23),
            label(r"sometimes it is weak, \ and only A learns this: \ both attacking wins $M$ each", font_size=23),
            label(r"attacking alone, \ or attacking the strong: \ lose $L$, \ with $L > M$", font_size=23,
                  color=BAD),
            label(r"if weak, \ A's computer emails B's; \ every email is confirmed automatically", font_size=23,
                  color=GOAL),
            label(r"each email is lost with chance $\varepsilon$, \ and then the exchange stops", font_size=23,
                  color=LOSS),
            label(r"a player's type: \ how many emails her computer sent", font_size=23,
                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, -0.5, 0])
        with self.voiceover(
            "Perhaps certainty is too much to ask. Surely a very high tower of mutual knowledge is enough? Ariel "
            "Rubinstein showed, in 1989, that it is not. <bookmark mark='a'/>Usually the enemy is strong, and "
            "neither general should attack. <bookmark mark='b'/>Sometimes it is weak, and only A learns which. Then "
            "attacking together wins M for each. <bookmark mark='c'/>Attacking alone, or attacking a strong enemy, "
            "loses L, which is worse than M is good. <bookmark mark='d'/>If the enemy is weak, A's computer emails "
            "B's computer, and every email that arrives is confirmed automatically, back and forth. "
            "<bookmark mark='e'/>Each email is lost with some small chance epsilon, and then the exchange stops. "
            "<bookmark mark='f'/>When it stops, each general sees only how many emails his own computer sent."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def unravel(self):
        d = load("email")
        head = label(r"The Reasoner iterates best responses", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        sub = label(rf"$\varepsilon = {d['eps']}$, \ $M = 2$, \ $L = 4$: \ types 0 to 8", font_size=22,
                    color=GREY_B).next_to(head, DOWN, buff=0.2)
        T = 8
        hist = d["history"]
        cell = 0.4
        grids = VGroup()
        for k, (a_set, b_set) in enumerate(hist[:9]):
            row = VGroup()
            for who, s_ in (("A", a_set), ("B", b_set)):
                for t in range(T + 1):
                    sq = Square(side_length=cell * 0.85, stroke_width=1, stroke_color=GREY_C,
                                fill_color=(OK if t in s_ else "#222"), fill_opacity=0.8 if t in s_ else 0.3)
                    sq.move_to([(-4.6 if who == "A" else 1.2) + t * cell, 1.45 - k * 0.4, 0])
                    row.add(sq)
            lab = label(rf"step {k}", font_size=17, color=GREY_B).move_to([-5.4, 1.45 - k * 0.4, 0])
            row.add(lab)
            grids.add(row)
        ha = label(r"A attacks, \ by type 0--8", font_size=20, color=AG["A"]).move_to([-4.6 + 4 * cell, 1.95, 0])
        hb = label(r"B attacks, \ by type 0--8", font_size=20, color=AG["B"]).move_to([1.2 + 4 * cell, 1.95, 0])
        foot = VGroup(label(r"each step, \ the lowest type that still attacks finds it too risky", font_size=21,
                            color=GREY_A),
                      label(r"the only equilibrium: \ never attack, \ even after a thousand emails", font_size=24,
                            color=BAD)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        assert d["final"] == [[], []]
        with self.voiceover(
            "Suppose both generals start from the obvious plan: attack whenever you know the enemy is weak. "
            "<bookmark mark='a'/>The Reasoner computes each type's best reply and repeats. <bookmark mark='b'/>Green "
            "squares are types that attack. <bookmark mark='c'/>A general whose computer sent nothing has received "
            "nothing, and does not attack. Then A of type one, who sent one email and heard nothing back, thinks it "
            "more likely that his own email was lost than that B's reply was; so he expects B not to attack, and "
            "stops. Then B of type one reasons the same way about A, and so on up the line. <bookmark mark='d'/>Step by step, the attack sets shrink to nothing. The only equilibrium is "
            "never to attack, even after a thousand emails have been exchanged, when each general knows that the "
            "other knows, a thousand levels deep. Almost common knowledge is not enough."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(ha), FadeIn(hb), FadeIn(grids[0]))
            vo.wait_until("b")
            self.play(Indicate(grids[0], color=OK, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            for g in grids[1:]:
                self.play(FadeIn(g), run_time=0.9)
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def pbelief(self):
        d = load("beliefs")
        head = label(r"What went wrong: \ common $p$-belief", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"Monderer and Samet (1989): \ coordination needs common $p$-belief, \ with $p$ near 1", font_size=23),
            label(r"`everyone believes it with probability $p$, \ believes that everyone does, \ \dots'", font_size=22,
                  color=GREY_A),
            label(rf"in the email game, \ every informed general gives probability \ ${d['p_fewer']:.3f}$",
                  font_size=23, color=GOAL),
            label(r"to his own last email having been lost, \ however many were sent", font_size=23, color=GOAL),
            label(rf"so the weak enemy is never common $p$-belief \ for $p$ above ${d['max_common_p']:.3f}$",
                  font_size=24, color=BAD),
            label(r"many messages build a high tower of knowledge, \ but always on a wobbly top storey", font_size=23,
                  color=OK)).arrange(DOWN, buff=0.28).move_to([0, -0.4, 0])
        with self.voiceover(
            "Dov Monderer and Dov Samet found the right diagnosis in the same year. <bookmark mark='a'/>Coordination "
            "does not need full common knowledge; it needs common p-belief, with p close to one: <bookmark mark='b'/>"
            "everyone believes the fact with probability at least p, believes that everyone believes it with that "
            "probability, and so on. <bookmark mark='c'/>The Reasoner computes what a general believes in the email "
            "game. Whatever his type, he gives probability just over a half, one over two minus epsilon, "
            "<bookmark mark='d'/>to his own last email having been lost, however many emails were sent. "
            "<bookmark mark='e'/>So the weak enemy is never common p-belief for p above about forty-seven percent. "
            "<bookmark mark='f'/>Many messages build a very high tower of knowledge, but its top storey always "
            "wobbles, and in strategic settings, the top storey is what matters."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

