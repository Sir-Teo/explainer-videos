from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, big, grid_table, load, mono, words)

POS = {0: (-5.6, 0.0), 1: (-3.8, 1.2), 2: (-2.0, 2.0), 8: (-0.2, 2.0), 9: (1.6, 2.0), 6: (-2.0, 0.6),
       7: (-0.2, 0.6), 3: (-3.8, -1.2), 4: (-2.0, -1.2), 5: (-0.2, -1.2)}


class AhoCorasick(VoiceoverScene):
    def construct(self):
        self.card()
        self.trie()
        self.measured()

    def card(self):
        card = chapter_card(5, r"Many patterns at once", r"How do you look for a thousand words in one pass?",
                            lit=(1975,), extra=((1975, r"Aho--Corasick"),), part=PART)
        with self.voiceover("Chapter five. Many patterns at once."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def trie(self):
        d = load("ac")["tiny_trie"]
        head = label(r"A trie of the patterns, \ with failure links", font_size=34).to_edge(UP, buff=0.35)
        pats = label(r"patterns: \ \texttt{he}, \ \texttt{she}, \ \texttt{his}, \ \texttt{hers}", font_size=22,
                     color=GREY_A).next_to(head, DOWN, buff=0.2)
        nodes = {}
        for s, (x, y) in POS.items():
            out = d["out"][s]
            col = YES if out else DATA
            c = Circle(radius=0.28, color=col, stroke_width=2.5 if out else 2).move_to([x, y - 0.5, 0])
            nodes[s] = VGroup(c, mono(str(s), 16, WHITE).move_to(c))
        edges = VGroup()
        for s, ch, t in d["edges"]:
            a = Arrow(nodes[s].get_center(), nodes[t].get_center(), buff=0.3, stroke_width=2.2, color=DATA,
                      max_tip_length_to_length_ratio=0.12)
            edges.add(VGroup(a, mono(ch, 16, DATA).move_to(a.get_center() + UP * 0.18)))
        fails = VGroup()
        for s, f in enumerate(d["fail"]):
            if s and f:
                arc = CurvedArrow(nodes[s].get_center() + DOWN * 0.28, nodes[f].get_center() + DOWN * 0.28,
                                  angle=-0.6, color=HEAD, stroke_width=1.8, tip_length=0.14)
                fails.add(arc)
        outs = VGroup()
        for s, o in enumerate(d["out"]):
            if o:
                outs.add(label(r", ".join(rf"\texttt{{{w}}}" for w in o), font_size=17, color=YES).next_to(
                    nodes[s], UP, buff=0.08))
        side = VGroup(
            label(r"follow the trie while characters match", font_size=20, color=DATA),
            label(r"on a mismatch, \ follow the \textbf{failure link}: \\ the longest proper suffix still in the "
                  r"trie", font_size=20, color=HEAD),
            label(r"each state lists every pattern ending there: \\ at \texttt{she}, \ \texttt{he} too", font_size=20,
                  color=YES),
            label(r"KMP's failure function, \\ generalized from a line to a tree", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        side.move_to([4.4, -1.8, 0])
        if side.get_right()[0] > 6.9:
            side.shift(LEFT * (side.get_right()[0] - 6.9))
        with self.voiceover(
            "Often we want many patterns at once: every virus signature, every banned word, every name in a list. "
            "Running one search per pattern reads the text again and again. <bookmark mark='a'/> In 1975 Alfred Aho "
            "and Margaret Corasick put all the patterns into one trie, a tree of their prefixes. <bookmark "
            "mark='b'/> Reading the text, we walk down the trie while characters match. On a mismatch, we follow a "
            "failure link to the longest proper suffix of what we've read that is still in the trie: from s h, "
            "the link goes to h. <bookmark mark='c'/> And each state lists every pattern that ends there: reaching "
            "s h e reports she, and also he. <bookmark mark='d'/> This is Knuth, Morris and Pratt's failure "
            "function, generalized from a line to a tree, and it reads the text exactly once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pats))
            vo.wait_until("a")
            self.play(*[FadeIn(n) for n in nodes.values()], LaggedStart(*[Create(e) for e in edges], lag_ratio=0.1))
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(f) for f in fails], lag_ratio=0.3), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(outs), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("ac")
        head = label(rf"{d['patterns']} character names, \ one pass over the corpus", font_size=32).to_edge(UP,
                                                                                                    buff=0.35)
        stats = VGroup(
            label(rf"trie: \ {d['states']} states", font_size=22, color=DATA),
            label(rf"one pass: \ {big(d['steps'])} steps \ ({d['seconds']:.1f} s in Python)", font_size=22, color=YES),
            label(rf"one search per name: \ {big(d['separate_reads'])} characters read", font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT, buff=0.8).shift(UP * 0.6)
        top = d["top"][:10]
        vmax = top[0][1]
        bars = VGroup()
        for k, (w, c) in enumerate(top):
            b = Rectangle(width=3.8 * c / vmax, height=0.3, stroke_width=0, fill_color=LAM, fill_opacity=0.85)
            b.move_to([1.6 + b.width / 2, 2.0 - k * 0.42, 0])
            bars.add(VGroup(b, mono(w, 16, WHITE).next_to(b, LEFT, buff=0.15).align_to([1.5, 0, 0], RIGHT),
                            mono(words(c), 14, GREY_A).next_to(b, RIGHT, buff=0.1)))
        note_ = label(r"substrings, \ not words: \ \texttt{Jo} also counts \texttt{John} and \texttt{Joe}", font_size=19,
                      color=GREY_B).next_to(bars, DOWN, buff=0.3).align_to(bars, LEFT)
        uses = label(r"in practice: \ \texttt{fgrep} with many patterns, \ antivirus signatures, \ intrusion detection "
                     r"(Snort), \ tokenizers' vocabularies", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            f"We built the automaton for {d['patterns']} character names from the novels: Elizabeth, Ahab, "
            f"Queequeg, Holmes, Raskolnikov and the rest. <bookmark mark='a'/> The trie has {d['states']} states. "
            "One pass over the corpus took twenty-five million steps. <bookmark mark='b'/> Searching for each name "
            "separately would read the text forty-five times, more than a billion characters. <bookmark "
            "mark='c'/> These are substring counts, so Jo also counts John and Joe; a real tool would add word "
            "boundaries. <bookmark mark='d'/> The same automaton runs inside grep with many patterns, antivirus "
            "scanners and network intrusion detectors."
        ) as vo:
            self.play(FadeIn(head), FadeIn(stats[0]))
            vo.wait_until("a")
            self.play(FadeIn(stats[1]), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(stats[2]))
            vo.wait_until("c")
            self.play(FadeIn(note_))
            vo.wait_until("d")
            self.play(FadeIn(uses))
        self.wait(0.3)
        self.clear_scene()
