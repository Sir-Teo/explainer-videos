from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Program(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Hilbert's program", r"Can mathematics prove its own reliability?", lit=(1928,),
                            part=PART)
        with self.voiceover("Chapter one. Hilbert's program."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.formalism()
        self.miu()
        self.invariant()

    def formalism(self):
        hc = history_card(1928, r"Hilbert \& Ackermann", r"\textit{Grundzüge der theoretischen Logik}: \ the "
                          r"\textit{Entscheidungsproblem}", width=6.6, color=HIST).to_corner(UL, buff=0.35)
        dc = definition_card(r"formal system", r"an alphabet, \ some axioms (strings), \ and rules that turn "
                             r"strings into strings; \ a \textit{proof} is a finite list of strings, \ each an axiom "
                             r"or made from earlier ones by a rule", width=9.6, font_size=25, color=P.CLAIM).move_to(
            [0, 0.3, 0])
        two = VGroup(
            VGroup(label(r"mathematics", font_size=28, color=GOAL),
                   label(r"a game of symbols, \ played by rules, \ meaning set aside", font_size=24,
                         color=GREY_A)).arrange(DOWN, buff=0.15),
            VGroup(label(r"metamathematics", font_size=28, color=PROV),
                   label(r"facts \textit{about} the game, \ proved by finite, \ concrete reasoning", font_size=24,
                         color=GREY_A)).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Hilbert's answer to the paradoxes of Part 6 was a program, worked out with Paul Bernays and Wilhelm "
            "Ackermann through the 1920s. <bookmark mark='a'/>Write all of mathematics as a formal system: an "
            "alphabet, some axioms, and rules for turning strings into strings. A proof is then a finite list of "
            "strings, checkable by a clerk, or a machine. <bookmark mark='b'/>Mathematics itself becomes a game of "
            "symbols, played without regard to meaning. <bookmark mark='c'/>And facts about the game, such as "
            "that no proof ends in zero equals one, are to be proved by finite, concrete reasoning that even a "
            "sceptic of the infinite would accept. That is metamathematics."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(dc))
            vo.wait_until("b")
            self.play(FadeIn(two[0]))
            vo.wait_until("c")
            self.play(FadeIn(two[1]))
        self.clear_scene()

    def miu(self):
        d = load("miu")
        rules = VGroup(
            label(r"axiom: \ \texttt{MI}", font_size=26, color=GOAL),
            label(r"1. \ \texttt{x I} $\to$ \texttt{x IU}", font_size=24),
            label(r"2. \ \texttt{M x} $\to$ \texttt{M x x}", font_size=24),
            label(r"3. \ \texttt{III} $\to$ \texttt{U}", font_size=24),
            label(r"4. \ \texttt{UU} $\to$ nothing", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rules.to_corner(UL, buff=0.5)
        head = label(r"Hofstadter's MIU system \ (1979)", font_size=30, color=CONN).to_edge(UP, buff=0.4).shift(
            RIGHT * 1.6)
        levels = [list(lv) for lv in d["levels"][:4]]
        for k in range(1, len(levels)):
            prev = levels[k - 1]

            def key(s_, prev=prev):
                for i, p_ in enumerate(prev):
                    for t, r in A.miu_successors(p_):
                        if t == s_:
                            return (i, r)
                return (len(prev), 0)
            levels[k].sort(key=key)
        nodes = {}
        layer = VGroup()
        for k, lv in enumerate(levels):
            y = 1.9 - 1.35 * k
            n = len(lv)
            xs = np.linspace(-0.6 - 1.0 * (n - 1), -0.6 + 1.0 * (n - 1), n) * (1.35 if k == 3 else 1.6) / 1.6 + 2.0
            for s, x in zip(lv, xs):
                m = Tex(r"\texttt{" + s + "}", font_size=24 if k < 3 else 20, color=WHITE)
                bg = SurroundingRectangle(m, buff=0.08, corner_radius=0.06, stroke_color=GREY_C, stroke_width=1.2,
                                          fill_color="#151A24", fill_opacity=1)
                nodes[s] = VGroup(bg, m).move_to([x, y, 0])
                layer.add(nodes[s])
        edges = VGroup()
        for k in range(1, len(levels)):
            for s in levels[k]:
                for p in levels[k - 1]:
                    hit = [r for t, r in A.miu_successors(p) if t == s]
                    if hit:
                        a, b = nodes[p].get_bottom(), nodes[s].get_top()
                        ln = Line(a, b, buff=0.05, color=GREY_B, stroke_width=1.6)
                        tag = MathTex(str(hit[0]), font_size=18, color=NUM).move_to(ln.point_from_proportion(0.5) +
                                                                                    LEFT * 0.14)
                        edges.add(VGroup(ln, tag))
                        break
        q = label(r"is \texttt{MU} a theorem?", font_size=30, color=SELF).to_edge(DOWN, buff=0.9)
        search = label(rf"the Reasoner: \ {d['count7']} theorems within seven steps, \ none of them \texttt{{MU}}",
                       font_size=24, color=GREY_A).next_to(q, DOWN, buff=0.2)
        assert not d["mu"]
        with self.voiceover(
            "Here is a formal system small enough to play by hand, from Douglas Hofstadter's book of 1979, "
            "Gödel, Escher, Bach. <bookmark mark='a'/>The alphabet is M, I and U. There is one axiom, MI, and "
            "four rules. Add U after a final I. Double everything after the M. Replace three I's by a U. Delete "
            "two U's. <bookmark mark='b'/>Applying the rules builds a tree of theorems: MII, MIU, MIIII, and so on. "
            "<bookmark mark='c'/>The puzzle: is MU a theorem? <bookmark mark='d'/>The Reasoner can search. Within "
            "seven steps it finds more than seventeen hundred theorems, and no MU. But a search, however long, can never show "
            "that MU will not turn up at step eight, or step eight million."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rules], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            for k in range(len(levels)):
                new = [nodes[s] for s in levels[k]]
                es = [e for e in edges if any(np.allclose(e[0].get_end(), nodes[s].get_top(), atol=0.1)
                                              for s in levels[k])]
                self.play(*[Create(e[0]) for e in es], *[FadeIn(e[1]) for e in es],
                          *[FadeIn(m, shift=DOWN * 0.1) for m in new], run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(search))
        self.clear_scene()

    def invariant(self):
        head = label(r"An argument \textit{about} the system", font_size=32, color=PROV).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"count the I's, \ modulo 3", font_size=28, color=GOAL),
            label(r"the axiom \texttt{MI} has one: \ $1 \not\equiv 0$", font_size=26),
            label(r"rule 2 doubles the count: \ $1 \to 2 \to 1 \to 2 \dots$ \ never 0 (mod 3)", font_size=26),
            label(r"rule 3 removes three: \ the remainder is unchanged; \ rules 1 and 4 add or remove no I's",
                  font_size=26),
            label(r"\texttt{MU} has none: \ $0 \equiv 0$", font_size=26, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.5, 0])
        concl = label(r"so \texttt{MU} is not a theorem: \ proved from outside, \ by reasoning about the rules",
                      font_size=28, color=OK).to_edge(DOWN, buff=1.2)
        dream = label(r"Hilbert's hope: \ the same for mathematics; \ an invariant shows no proof ends in "
                      r"$0 = 1$", font_size=26, color=PROV).next_to(concl, DOWN, buff=0.3)
        with self.voiceover(
            "So step outside the system. <bookmark mark='a'/>Count the I's, and look at the remainder when you "
            "divide by three. The axiom has one I. <bookmark mark='b'/>Doubling turns a remainder of one into two, "
            "and two into one, never zero. Replacing three I's by a U leaves the remainder alone, and the other "
            "rules add or remove no I's at all. <bookmark mark='c'/>MU has no I's, a remainder of zero. So MU is "
            "not a theorem. <bookmark mark='d'/>The proof is not a derivation inside MIU. It is a short, finite "
            "argument about MIU. <bookmark mark='e'/>That was Hilbert's hope for all of mathematics: an invariant "
            "of the same kind, proving by finite means that no proof in the system ends in zero equals one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(concl))
            vo.wait_until("e")
            self.play(FadeIn(dream))
        self.clear_scene()
