from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono, words)


class Recursion(VoiceoverScene):
    def construct(self):
        self.card()
        self.quines()
        self.theorem()

    def card(self):
        card = chapter_card(4, r"Programs that know their own code", r"Can a program print itself?", lit=(1938,),
                            extra=((1938, r"Kleene's recursion theorem"),), part=PART)
        with self.voiceover("Chapter four. Programs that know their own code."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def quines(self):
        q = load("quines")
        head = label(r"Quines", font_size=34).to_edge(UP, buff=0.3)
        py = VGroup(*[mono(ln, 20, LAM) for ln in q["python"].strip().splitlines()]).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=0.08)
        pyl = label(r"Python: \ the string is the program's template; \\ \%r prints it quoted", font_size=19,
                    color=LAM).next_to(py, DOWN, buff=0.15)
        g1 = VGroup(py, pyl).to_edge(UP, buff=1.1).to_edge(LEFT, buff=0.7)
        lines = q["pebble_head"][-4:] + q["pebble_data"] + ["    ..."] + q["pebble_tail"][:8]
        pb = VGroup(*[mono(ln if ln else " ", 14, DATA) for ln in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        if pb.width > 6.0:
            pb.width = 6.0
        pb.to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        pbl = label(rf"the Pebble language: \ {q['pebble_lines']} lines, \ {words(q['pebble_len'])} characters; \\ "
                    rf"{q['data_lines']} assignments store the rest of the program as numbers", font_size=19,
                    color=DATA).next_to(pb, DOWN, buff=0.15)
        notes = VGroup(
            label(r"the recipe: \ \textbf{A} = data describing \textbf{B}; \ \textbf{B} = print A's data as code, \ "
                  r"then print it as text", font_size=21, color=WHITE),
            label(rf"run on the emulator: \ {words(q['pebble_steps'])} instructions, \ and the output equals the source, "
                  r"\ byte for byte", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Can a program print its own source? The obvious attempt fails: a print statement must contain its own "
            "text, which contains the print statement, forever. <bookmark mark='a'/> The trick is to split the "
            "program in two. Here in Python, the string s is a template of the whole program, with a hole. The "
            "print statement fills the hole with the string itself, quoted. <bookmark mark='b'/> Our Pebble "
            "language has no string formatting, so its quine is longer: seven hundred and fifty-nine lines. Most of "
            "them store the rest of the program as numbers, one character each. <bookmark mark='c'/> The tail then "
            "prints the head from that data, then prints each assignment statement, then prints the tail. Part A "
            "describes part B; part B prints A twice, once as code and once as the text it encodes. <bookmark "
            "mark='d'/> We ran it on the emulator: ninety-nine thousand instructions, and the output is the source, "
            "byte for byte."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g1))
            vo.wait_until("b")
            self.play(FadeIn(pb), FadeIn(pbl))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def theorem(self):
        head = label(r"Kleene's recursion theorem", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('acceptable effective numbering: every TOTAL computable index transformer $t$ has $\\varphi_e=\\varphi_{t(e)}$',
                  font_size=22, color=HEAD),
            label('construct a program with an embedded self-description; no general source-introspection facility', font_size=22,
                  color=WHITE),
            label(r"the quine is the case $t$ = ``print this text''", font_size=22, color=LAM),
            label(r"\textbf{halting, again}: \ suppose $H$ decides halting. \ Write $R$: \ get my own code; \ ask $H$ "
                  r"whether I halt; \ do the opposite", font_size=22, color=NO),
            label(r"no diagonal table needed: \ self-reference is a \textbf{programming technique}", font_size=22,
                  color=YES),
            label(r"the same trick: \ Thompson's trojan compiler \ (Part 55), \ self-replicating viruses, \ "
                  r"G\"odel's sentence \ (chapter 8)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Kleene's recursion theorem makes self-reference precise. <bookmark mark='a'/> In an acceptable effective numbering of programs, every TOTAL computable transformation of program indices has an index whose program computes the same partial function as its transform. <bookmark mark='b'/> This constructs programs with an embedded description of themselves. It does not provide arbitrary source introspection to every existing program. <bookmark mark='c'/> Printing a supplied description gives the quine construction. <bookmark mark='d'/> If H decided halting, construct R with its own description embedded, ask H whether R halts, and do the opposite. H must be wrong. <bookmark mark='e'/> The construction packages the diagonal argument as a programming technique. <bookmark mark='f'/> Related self-reference appears in Gödel sentences and Thompson's compiler construction in Part 55."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
