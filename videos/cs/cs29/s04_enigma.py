from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (DATA, HEAD, LAM, NO, PART, YES, flow_box, load, mono)


class Enigma(VoiceoverScene):
    def construct(self):
        self.card()
        self.machine()
        self.rejewski()
        self.cribs()

    def card(self):
        card = chapter_card(3, r"Enigma", r"How do you break a machine with $10^{20}$ keys?",
                            lit=(1932, 1940), extra=((1918, r"Scherbius's patent"), (1932, r"Rejewski"),
                                                     (1940, r"Turing's Bombe")), part=PART)
        with self.voiceover("Chapter three. Enigma."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def machine(self):
        e = load("enigma")
        head = label(r"A substitution that changes with every key", font_size=34).to_edge(UP, buff=0.3)
        names = [(r"keys \\ and lamps", GREY_B), (r"plugboard", HEAD), (r"rotor 3", DATA), (r"rotor 2", DATA),
                 (r"rotor 1", DATA), (r"reflector", LAM)]
        boxes = VGroup(*[flow_box(t, c, w=1.45, h=1.6, font=19) for t, c in names]).arrange(RIGHT, buff=0.4)
        boxes.next_to(head, DOWN, buff=0.6)
        y_out, y_back = boxes.get_y() + 0.45, boxes.get_y() - 0.45
        go = VGroup(*[Arrow([a.get_right()[0], y_out, 0], [b.get_left()[0], y_out, 0], buff=0.02, stroke_width=3,
                            color=YES, max_tip_length_to_length_ratio=0.3) for a, b in zip(boxes, boxes[1:])])
        back = VGroup(*[Arrow([b.get_left()[0], y_back, 0], [a.get_right()[0], y_back, 0], buff=0.02, stroke_width=3,
                              color=NO, max_tip_length_to_length_ratio=0.3) for a, b in zip(boxes, boxes[1:])])
        pos = [mono(c, 22, WHITE).next_to(boxes[2 + i], DOWN, buff=0.15) for i, c in enumerate("ALB")]
        posg = VGroup(*pos)
        step = mono("B", 22, YES).move_to(pos[0])
        msg = mono(e["msg"], 20, WHITE)
        cip = mono(e["cipher"], 20, DATA)
        pair = VGroup(msg, cip).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(boxes, DOWN, buff=0.6)
        lines = VGroup(
            label(r"each rotor is a fixed wiring: \ a permutation of 26 letters; \ the rightmost steps on every key",
                  font_size=21, color=DATA),
            label(r"the reflector sends the current back: \ so encrypting twice decrypts, \ and \textbf{no letter "
                  r"ever becomes itself}", font_size=21, color=LAM),
            label(r"plugboard: \ 10 cables swap 20 letters: \ 150{,}738{,}274{,}937{,}250 ways", font_size=21,
                  color=HEAD),
            label(r"60 rotor orders $\times$ $26^3$ positions $\times$ plugboards: \ $1.59 \times 10^{20}$ daily "
                  r"keys", font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Enigma, patented by Arthur Scherbius in 1918 and used by every branch of the German military, mechanised "
            "Vigenère's idea. <bookmark mark='a'/> Pressing a key sends a current through a plugboard, then through "
            "three rotors, each a fixed wiring of the twenty-six letters: a permutation. <bookmark mark='b'/> A "
            "reflector sends it back through the rotors and plugboard to light a lamp. Before each letter the right "
            "rotor steps, and now and then the others, so every letter is enciphered by a different permutation. "
            "<bookmark mark='c'/> Our simulation passes the standard test, and enciphers a weather report. The "
            "reflector has two consequences: enciphering the ciphertext again gives back the message, and no letter "
            "is ever enciphered as itself. Look down the columns: never the same letter. <bookmark mark='d'/> The "
            "plugboard's ten cables could be placed in a hundred and fifty million million ways. <bookmark mark='e'/> "
            "With the choice and order of three rotors from five and their starting positions, an operator chose "
            "each day among a hundred and fifty-nine billion billion keys."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(posg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in go], lag_ratio=0.3), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in back[::-1]], lag_ratio=0.3))
            self.play(Transform(pos[0], step))
            vo.wait_until("c")
            self.play(FadeIn(pair), FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def rejewski(self):
        e = load("enigma")
        head = label(r"Rejewski's theorem \ (1932)", font_size=34).to_edge(UP, buff=0.3)
        lines_top = VGroup(
            label(r"each message began with its 3-letter key, \ enciphered \textbf{twice}: \ letters 1 and 4 hide "
                  r"the same letter", font_size=21, color=WHITE),
            label(r"so from a day's messages, \ the product $A_1 A_4$ of two of the day's permutations is known",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).next_to(head, DOWN, buff=0.35)

        def cyc_row(cs, color):
            g = VGroup(*[VGroup(mono(c, 20, color), label(rf"length {len(c)}", font_size=15, color=GREY_B))
                         .arrange(DOWN, buff=0.06) for c in cs]).arrange(RIGHT, buff=0.6)
            return g
        r1 = cyc_row(e["cycles_noplug"], DATA)
        r2 = cyc_row(e["cycles_plug"], HEAD)
        t1 = label(r"no plugboard", font_size=18, color=DATA)
        t2 = label(r"10 cables", font_size=18, color=HEAD)
        grid = VGroup(VGroup(t1, r1).arrange(RIGHT, buff=0.4), VGroup(t2, r2).arrange(RIGHT, buff=0.4)).arrange(
            DOWN, buff=0.35, aligned_edge=RIGHT).next_to(lines_top, DOWN, buff=0.4)
        ch = e["char_noplug"]
        cs = r"; \ ".join("(" + ", ".join(str(x) for x in c) + ")" for c in ch)
        oth = r"; \ ".join("(" + ", ".join(str(x) for x in c) + ")" for c in e["char_other"])
        lines = VGroup(
            label(r"the letters change, \ the cycle lengths do not: \ $A_i = S R_i S$, \ so $A_1 A_4 = S \,(R_1 R_4)"
                  r"\, S$ \ and conjugating keeps every cycle's length", font_size=21, color=YES),
            label(rf"the day's \textbf{{characteristic}} \ (from $A_1A_4$, $A_2A_5$, $A_3A_6$): \ {cs}", font_size=21,
                  color=WHITE),
            label(rf"another rotor setting: \ {oth}", font_size=21, color=GREY_A),
            label(r"so the Poles catalogued all 105{,}456 rotor settings \ (6 orders $\times$ 17{,}576 positions) "
                  r"once, \ and looked each day up", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The first break came from mathematics. Marian Rejewski, a young Polish mathematician, worked on Enigma "
            "in 1932. <bookmark mark='a'/> Operators began each message with a three-letter message key, enciphered "
            "twice for safety. So the first and fourth letters were the same letter under two different "
            "permutations, and from a day's worth of messages Rejewski could reconstruct the product of the two: a "
            "permutation of the alphabet. <bookmark mark='b'/> Here is that product for one setting of our "
            "simulated rotors, written as cycles: A goes to I, I to D, and so on, two cycles of thirteen. Now add "
            "ten plugboard cables. The letters in the cycles change completely; the lengths of the cycles do not. "
            "<bookmark mark='c'/> That is a theorem from group theory: the plugboard S is applied on the way in and "
            "on the way out, so it conjugates the product, and conjugation renames letters without changing the "
            "shape of the cycles. <bookmark mark='d'/> So the cycle lengths, the day's characteristic, depend only "
            "on the rotors. A different setting gives a different shape. <bookmark mark='e'/> The Poles built a "
            "device to catalogue the characteristic of every rotor setting, a hundred thousand of them, and then "
            "found each day's setting by looking it up, ignoring the plugboard's hundred and fifty million million "
            "possibilities entirely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines_top[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines_top[1]))
            vo.wait_until("b")
            self.play(FadeIn(grid[0]))
            self.play(FadeIn(grid[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]), FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def cribs(self):
        e = load("enigma")
        head = label(r"Cribs, \ and a machine to test them", font_size=34).to_edge(UP, buff=0.3)
        ct, crib = e["cipher"], "WETTERBERICHT"
        dx = 0.42
        crow = VGroup(*[mono(c, 22, DATA).move_to([dx * i, 0, 0]) for i, c in enumerate(ct)]).center()
        crow.next_to(head, DOWN, buff=0.8)
        ok = []
        rows = VGroup()
        for o in range(len(ct) - len(crib) + 1):
            bad = [i for i, c in enumerate(crib) if ct[o + i] == c]
            if not bad:
                ok.append(o)
            r = VGroup(*[mono(c, 22, NO if i in bad else WHITE).move_to(crow[o + i].get_center() + DOWN * 0.55)
                         for i, c in enumerate(crib)])
            rows.add(r)
        tag = label(r"cipher", font_size=18, color=DATA).next_to(crow, LEFT, buff=0.3)
        ctag = label(r"crib", font_size=18, color=WHITE).next_to(rows[0], LEFT, buff=0.3).align_to(tag, RIGHT)
        bad_count = len(rows) - len(ok)
        lines = VGroup(
            label(r"a \textbf{crib}: \ words the message probably contains: \ \texttt{WETTERBERICHT}, \ weather "
                  r"report", font_size=21, color=WHITE),
            label(r"slide it along: \ wherever a letter would encipher to \textbf{itself}, \ that position is "
                  r"impossible \ (red)", font_size=21, color=NO),
            label(rf"{bad_count} of {len(rows)} positions ruled out \ (possible: \ "
                  + ", ".join(str(o) for o in ok) + ")", font_size=21, color=HEAD),
            label(r"Turing's \textbf{Bombe} \ (1940): \ test a crib against every rotor setting, \ discarding "
                  r"contradictions electrically", font_size=21, color=YES),
            label(r"by 1945: \ over 200 Bombes; \ Colossus, \ the first electronic computer, \ broke the Lorenz "
                  r"cipher", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 1939, weeks before the war, the Poles gave everything they had to the British and French. At "
            "Bletchley Park the work moved from mathematics to machinery. <bookmark mark='a'/> The British relied on "
            "cribs: words a message probably contained. Weather stations sent weather reports, in a fixed format, "
            "every day. <bookmark mark='b'/> To place a crib, slide it along the ciphertext. Wherever a crib letter "
            "lines up with the same ciphertext letter, that position is impossible, because Enigma never enciphers a "
            "letter as itself. <bookmark mark='c'/> On our message, nine of the fifteen positions are ruled out at "
            "once. <bookmark mark='d'/> Alan Turing, with Gordon Welchman, designed the Bombe: an electrical machine "
            "that took a placed crib and ran through rotor settings, rejecting every one that led to a "
            "contradiction. <bookmark mark='e'/> By the end of the war over two hundred Bombes were running, and the "
            "Colossus machines, the first programmable electronic computers, were breaking a different German "
            "cipher, the Lorenz teleprinter. The reflector's elegant symmetry was the machine's weakness."
        ) as vo:
            self.play(FadeIn(head), FadeIn(crow), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            cur = rows[0].copy()
            self.play(FadeIn(cur), FadeIn(ctag), FadeIn(lines[1]))
            for r in rows[1:]:
                self.play(Transform(cur, r), run_time=0.45)
            vo.wait_until("c")
            okm = VGroup(*[SurroundingRectangle(crow[o], color=YES, buff=0.05) for o in ok])
            self.play(FadeIn(lines[2]), Create(okm))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()
