from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, region)
from videos.cs.cs12.s03_regex import mod3_diagram

POS = {"S": (-5.6, 0.6), "0": (-2.6, 0.6), "1": (0.8, 0.6), "2": (4.2, 0.6), "F": (-2.6, -1.6)}


def gnfa(edges):
    nodes = {k: POS[k] for k in POS if any(k in (a, b) for a, b, _ in edges) or k in ("S", "F")}
    es = []
    for a, b, lab in edges:
        if a == b:
            es.append((a, b, lab, UP if a != "2" else RIGHT))
        elif (b, a) in [(x, y) for x, y, _ in edges]:
            es.append((a, b, lab, 0.5))
        else:
            es.append((a, b, lab, 0))
    return StateDiagram(nodes, es, radius=0.42, font_size=24, edge_font=19, accept=("F",))


def edges_of(d):
    out = []
    for k, v in d.items():
        a, b = k.split("->")
        out.append((a, b, v if v else "ε"))
    return out


class Kleene(VoiceoverScene):
    def construct(self):
        self.card()
        self.eliminate()
        self.closure()

    def card(self):
        card = chapter_card(5, r"Kleene's theorem", r"Can every automaton be written as a regular expression?",
                            lit=(1956,), extra=((1956, r"Kleene: \ the theorem published"),), part=PART)
        with self.voiceover("Chapter five. Kleene's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def eliminate(self):
        k = load("kleene")
        head = label(r"From automaton back to expression: \ remove states", font_size=34).to_edge(UP, buff=0.3)
        start = [("S", "0", "ε"), ("0", "F", "ε"), ("0", "0", "0"), ("0", "1", "1"), ("1", "0", "1"), ("1", "2", "0"),
                 ("2", "1", "0"), ("2", "2", "1")]
        d0 = gnfa(start)
        rule = VGroup(label(r"to remove $q$: \ for every path $p \to q \to r$, \ add", font_size=21, color=GREY_A),
                      MathTex(r"p \xrightarrow{\;R_{pq}\,(R_{qq})^*\,R_{qr}\;} r", font_size=34, color=HEAD)).arrange(
            RIGHT, buff=0.3).to_edge(DOWN, buff=1.2)
        steps = k["steps"]
        notes = [label(r"remove 2: \ the path $1 \to 2 \to 1$ becomes a loop \texttt{01*0} on 1", font_size=21,
                       color=GREY_A),
                 label(r"remove 1: \ the path $0 \to 1 \to 0$ becomes \texttt{1(01*0)*1}", font_size=21,
                       color=GREY_A),
                 label(r"remove 0: \ its loop becomes a star", font_size=21, color=GREY_A)]
        res = VGroup(Text(k["regex"][1:-1] if k["regex"].startswith("((") else k["regex"],
                          font="DejaVu Sans Mono", font_size=30, color=YES),
                     label(rf"checked against the DFA on every number from 1 to 4,095: \ "
                           rf"{'all agree' if k['checked'] else 'disagree'}", font_size=19, color=GREY_B)).arrange(
            DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover("Now the last side of the triangle: from any automaton, a regular expression. <bookmark mark='a'/> Take the divisible-by-three machine, and add a new start state and a new accepting state, joined by epsilon arrows. Let arrows carry whole regular expressions, not just symbols. <bookmark mark='b'/> Now remove the original states one at a time. To remove a state q, every path that went through it, from p into q and out to r, is replaced by one arrow from p to r, labelled: the way in, then q's loop any number of times, then the way out. <bookmark mark='c'/> Remove state two: the trip from one to two and back becomes a loop on one, zero, one star, zero. <bookmark mark='d'/> Remove state one: the trip from zero to one and back becomes one, then that loop starred, then one. <bookmark mark='e'/> Remove state zero: its loop becomes a star, and what is left is a single arrow carrying a single expression. <bookmark mark='f'/> That is where the strange expression of chapter two came from, and we checked it against the machine on every number up to four thousand and ninety-five.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(d0), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(rule))
            cur = d0
            for mk, st, note_ in zip('cde', steps, notes):
                vo.wait_until(mk)
                nxt = gnfa(edges_of(st['edges']))
                note_.next_to(head, DOWN, buff=0.25)
                self.play(Indicate(cur.node[str(st['removed'])], color=NO), FadeIn(note_))
                self.play(FadeOut(cur), FadeIn(nxt), run_time=1.2)
                self.play(FadeOut(note_))
                cur = nxt
            vo.wait_until('f')
            self.play(FadeOut(rule), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def closure(self):
        head = label(r"Regular languages are closed under \dots", font_size=34).to_edge(UP, buff=0.3)
        items = VGroup(
            label(r"union, \ concatenation, \ star: \ by definition", font_size=22, color=GREY_A),
            label("complement: swap accepting / rejecting in a complete DFA over the chosen alphabet", font_size=22, color=DATA),
            label(r"intersection: \ run two DFAs side by side; \ a state is a \textit{pair} of states", font_size=22,
                  color=CTRL),
            label(r"so ``not divisible by 3'' and ``divisible by 3 \textit{and} ending in 1'' are regular too",
                  font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.45)
        sd = mod3_diagram().scale(0.7).to_edge(DOWN, buff=0.7)
        flip = [sd.node[n].circle.animate.set_stroke(YES if n != "0" else CTRL) for n in "012"]
        cap = label(r"not divisible by 3: \ accept in 1 or 2", font_size=19, color=DATA).next_to(sd, UP, buff=0.15)
        use = label(r"and every question about them can be answered by machine: \ is the language empty? \ "
                    r"are two expressions equal?", font_size=20, color=HEAD).to_edge(DOWN, buff=0.25)
        with self.voiceover("Automata make closure properties constructive. <bookmark mark='a'/> Union, concatenation and star preserve regularity. <bookmark mark='b'/> For complement, first use a complete deterministic machine over the chosen alphabet, including a rejecting sink when necessary, then exchange accepting and rejecting states. <bookmark mark='c'/> For intersection, track a pair of machine states over a common alphabet and accept only when both components accept. <bookmark mark='d'/> The corresponding expression can be awkward to write by hand, even though the automaton construction is straightforward. <bookmark mark='e'/> Equivalence is decidable too: compare acceptance throughout the reachable product, or minimize complete DFAs and compare them up to renaming. A finite set of test strings alone would not decide equivalence.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(items[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(items[1]), FadeIn(sd))
            self.play(*flip, FadeIn(cap))
            vo.wait_until('c')
            self.play(FadeIn(items[2]))
            vo.wait_until('d')
            self.play(FadeIn(items[3]))
            vo.wait_until('e')
            self.play(FadeOut(sd), FadeOut(cap), FadeIn(use))
        self.wait(0.3)
        self.clear_scene()
