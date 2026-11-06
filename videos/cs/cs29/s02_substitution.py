from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (DATA, HEAD, NO, PART, YES, fit_right, letter_bars, load, mono)

A2Z = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def letter_row(s, color=WHITE, font=22, dx=0.42):
    g = VGroup(*[mono(c, font, color) for c in s])
    for i, m in enumerate(g):
        m.move_to([dx * i, 0, 0])
    return g.center()


class Substitution(VoiceoverScene):
    def construct(self):
        self.card()
        self.keys()
        self.counting()
        self.climbing()

    def card(self):
        card = chapter_card(1, r"Substitution and frequency analysis", r"Can you read a cipher without the key?",
                            lit=(1843,), extra=((1843, r"Poe's \textit{The Gold-Bug}"),), part=PART)
        with self.voiceover("Chapter one. Substitution, and frequency analysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def keys(self):
        s = load("subst")
        head = label(r"Replace every letter", font_size=34).to_edge(UP, buff=0.3)
        top = letter_row(A2Z, GREY_A).next_to(head, DOWN, buff=0.6)
        caesar = letter_row(A2Z[3:] + A2Z[:3], DATA).next_to(top, DOWN, buff=0.25)
        key = letter_row(s["key"], HEAD).move_to(caesar)
        tag1 = label(r"Caesar", font_size=20, color=DATA).next_to(caesar, LEFT, buff=0.25)
        tag2 = label(r"a key", font_size=20, color=HEAD).next_to(key, LEFT, buff=0.25)
        arrows = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.04, stroke_width=1.5, color=GREY_D,
                                max_tip_length_to_length_ratio=0.3) for a, b in zip(top, caesar)])
        pt = letter_row(s["plain"][:26], WHITE, 20).next_to(key, DOWN, buff=0.7)
        ct = letter_row(s["cipher"][:26], HEAD, 20).next_to(pt, DOWN, buff=0.2)
        years = 4.03e26 / 1e9 / 3.156e7
        lines = VGroup(
            label(r"Caesar: \ shift every letter by 3: \ only 26 keys, \ so try them all", font_size=22, color=DATA),
            label(r"a \textbf{substitution}: \ any rearrangement of the alphabet: \ $26! \approx 4 \times 10^{26}$ "
                  r"keys", font_size=22, color=HEAD),
            label(rf"at a billion keys a second, \ trying them all takes {years / 1e9:.0f} billion years", font_size=22,
                  color=WHITE),
            label(r"and yet a page of text gives the key away", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The oldest ciphers replace each letter by another. <bookmark mark='a'/> Caesar shifted every letter "
            "three places along the alphabet. There are only twenty-six shifts, so anyone who suspects a shift can "
            "simply try them all. <bookmark mark='b'/> A substitution cipher allows any rearrangement of the "
            "alphabet as the key. Here is one, and the opening of Moby-Dick under it. <bookmark mark='c'/> There "
            "are twenty-six factorial keys, about four times ten to the twenty-six. Trying a billion a second would "
            "take thirteen billion years, about the age of the universe. <bookmark mark='d'/> A large key space is "
            "necessary, but it is not enough. This cipher falls in seconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(caesar), FadeIn(tag1), Create(arrows), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(ReplacementTransform(caesar, key), ReplacementTransform(tag1, tag2), FadeIn(lines[1]))
            self.play(FadeIn(pt), FadeIn(ct))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def counting(self):
        s = load("subst")
        head = label(r"al-Kindi's method: \ count", font_size=34).to_edge(UP, buff=0.3)
        cb = letter_bars(s["cipher_freq"], width=5.6, height=2.2, color=HEAD)
        eb = letter_bars(s["english"], width=5.6, height=2.2, color=DATA)
        VGroup(cb, eb).arrange(RIGHT, buff=0.8).next_to(head, DOWN, buff=1.0)
        ct = label(r"the ciphertext \ (600 letters)", font_size=20, color=HEAD).next_to(cb, UP, buff=0.25)
        et = label(r"English", font_size=20, color=DATA).next_to(eb, UP, buff=0.25)
        topc = max(s["cipher_freq"], key=s["cipher_freq"].get)
        hb = cb.bars[A2Z.index(topc)]
        he = eb.bars[A2Z.index("E")]
        ring = VGroup(SurroundingRectangle(hb, color=YES, buff=0.05), SurroundingRectangle(he, color=YES, buff=0.05))
        lines = VGroup(
            label(r"al-Kindi \ (c.\ 850, \ Baghdad): \ \textit{On Deciphering Cryptographic Messages}", font_size=22,
                  color=WHITE),
            label(rf"the commonest ciphertext letter, \ {topc} \ ({100 * s['cipher_freq'][topc]:.1f}\%), \ is "
                  rf"probably E \ ({100 * s['english']['E']:.1f}\%)", font_size=22, color=YES),
            label(r"matching letters by rank gives a first guess: \ \texttt{" + s["start"][:30] + r"}", font_size=22,
                  color=HEAD),
            label(r"wrong in most places, \ but a start: \ the rest is search", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The method was written down in Baghdad in the ninth century by the philosopher al-Kindi, in a "
            "manuscript on deciphering cryptographic messages. <bookmark mark='a'/> Count how often each letter "
            "appears in the ciphertext, and compare with how often letters appear in the language. A substitution "
            "moves the bars around, but cannot change their heights. <bookmark mark='b'/> Here the commonest "
            "ciphertext letter is W, at almost thirteen percent, and the commonest English letter is E, at almost "
            "thirteen percent. W is probably E. <bookmark mark='c'/> Matching every letter by rank gives a first "
            "guess at the key. <bookmark mark='d'/> It is wrong in most places, because six hundred letters do not "
            "rank the rarer letters reliably. But it is a start, and the rest is search."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cb), FadeIn(ct), FadeIn(eb), FadeIn(et), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(ring), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def climbing(self):
        s = load("subst")
        head = label(r"Climbing toward English", font_size=34).to_edge(UP, buff=0.3)
        tr = s["trace"]
        shown = [tr[i] for i in sorted({0, 2, 4, 6, 8, 9, 10, 11, 12, len(tr) - 1})]
        lo, hi = tr[0][1], tr[-1][1]
        rows = VGroup()
        for step, score, text in shown:
            frac = (score - lo) / (hi - lo)
            bar = Rectangle(width=0.05 + 2.4 * frac, height=0.26, stroke_width=0, fill_color=YES,
                            fill_opacity=0.35 + 0.6 * frac)
            t = mono(text[:44], 19, interpolate_color(ManimColor(GREY_B), ManimColor(WHITE), frac))
            n = mono(f"{step:>2}", 17, GREY_C)
            sc = mono(f"{score:.0f}", 17, GREY_A)
            row = VGroup(n, t, sc, bar).arrange(RIGHT, buff=0.3)
            bar.align_to(sc, LEFT).shift(RIGHT * 0.9)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        for r in rows:
            r[3].next_to(r[2], RIGHT, buff=0.3)
        hdr = VGroup(label(r"step", font_size=16, color=GREY_C).next_to(rows[0][0], UP, buff=0.15),
                     label(r"score", font_size=16, color=GREY_C).next_to(rows[0][2], UP, buff=0.15))
        f = s["finals"]
        lines = VGroup(
            label(r"score: \ how English the text looks, \ from counts of four-letter runs in six million letters of "
                  r"other novels", font_size=21, color=WHITE),
            label(r"swap two letters of the key; \ keep the swap if the score improves; \ repeat", font_size=21,
                  color=DATA),
            label(rf"restart 1 stuck at {f[0]:.0f}; \ restarts 2--6 all reach {max(f):.0f}: \ the true key",
                  font_size=21, color=HEAD),
            label(rf"600 letters, \ {100 * s['accuracy']:.0f}\% correct, \ in {s['seconds']:.1f} seconds",
                  font_size=23, color=YES),
        ).arrange(DOWN, buff=0.17).to_edge(DOWN, buff=0.3)
        fit_right(rows)
        with self.voiceover(
            "To search, we need a way to score a guess. <bookmark mark='a'/> We count every run of four letters in "
            "six million letters of other novels, and score a candidate text by how likely its own runs are. "
            "English scores high; gibberish scores low. <bookmark mark='b'/> Then climb: swap two letters of the "
            "key, and keep the swap if the score improves. Watch the text sharpen. Common short words appear first, "
            "then longer ones, and then: Call me Ishmael. Some years ago, never mind how long precisely. <bookmark "
            "mark='c'/> A climb can get stuck on a false peak, as our first attempt did, so we restart a few times "
            "from jiggled starting keys; the other five all reached the same, higher score. <bookmark mark='d'/> "
            "Six hundred letters, every one correct, in a few seconds of Python. Edgar Allan Poe knew this in "
            "1843: a substitution cipher hides nothing from someone willing to count."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows[1:]], lag_ratio=0.5), run_time=5.0)
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]), rows[-1].animate.set_color(YES))
        self.wait(0.3)
        self.clear_scene()
