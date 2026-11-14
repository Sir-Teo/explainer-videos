from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403

KIND_C = {"passing": TUNE, "neighbour": BLUE, "suspension": EAR, "cambiata": "#A3E635", "anticipation": GREY_B, "free": RED}


class Dissonance(SoundScene):
    def construct(self):
        chapter(self, 4, r"Palestrina's style as rules", r"When may two voices clash?", extra=((1927, r"Jeppesen's \textit{The Style of Palestrina and the Dissonance}"),))
        self.kinds()
        self.counted()
        self.quiz()

    # ------------------------------------------------------------------
    def kinds(self):
        d = load("kinds")
        c = clip("kinds.four")
        cells = VGroup()
        rolls = {}
        for k in ("passing", "neighbour", "suspension", "cambiata"):
            u, l = d["demos"][k]
            g = voices_roll([u, l], width=2.6, height=1.9, colors=[KIND_C[k], GREY_A], lo=53, hi=76, bar_h=0.12)
            rolls[k] = g
            cells.add(VGroup(label(k, font_size=24, color=KIND_C[k]), g).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=0.55).move_to(UP * 0.5)
        rows_ = VGroup(*[label(t, font_size=21, color=c_) for t, c_ in (
            (r"passing and neighbour notes: \ on a weak beat, \ approached and left by step", WHITE),
            (r"the suspension: \ a consonance held while the bass moves, \ then falling by step", EAR),
            (r"the cambiata: \ down a step to a dissonance, \ then down a third", WHITE))]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Palestrina's music became a textbook. In 1725 Johann Joseph Fux built his Gradus ad Parnassum, Part 16's "
            "species, on it, and in the 1920s the Danish scholar Knud Jeppesen showed exactly how it treats dissonance. A "
            "dissonance is allowed in only a few ways. <bookmark mark='a'/> A passing note, on a weak beat, stepping "
            "through; a neighbour, stepping away and back. <bookmark mark='b'/> A suspension: a note consonant when it "
            "is struck, held while the bass moves under it into a dissonance, then falling by step to a consonance. "
            "<bookmark mark='c'/> And a stock figure called the cambiata, down a step to a dissonance and then down a "
            "third. Here are the four, two voices each."
        ) as vo:
            self.play(FadeIn(cells))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
        with self.listen(c) as snd:
            window(snd, r"passing, \ neighbour, \ suspension, \ cambiata", detail=r"two synthetic voices", kind="synthesized", corner=UL, tag_corner=UR)
            for k, cell in zip(("passing", "neighbour", "suspension", "cambiata"), cells):
                st = d["starts"][k]
                flash_voices(snd, rolls[k], d["demos"][k], st, d["unit"], colors=[KIND_C[k], GREY_A])
                end = st + 12 * d["unit"] + 0.3
                pulse(snd, cell[0], st, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counted(self):
        d = load("dissonance")
        g = d["groups"]["Palestrina"]
        sh = g["shares"]
        order = ["passing", "suspension", "neighbour", "cambiata", "anticipation", "free"]
        bars = columns([100 * sh[k] for k in order], order, width=8.4, height=2.8, color=TUNE, fmt="{:.1f}", font_size=19)
        bars.move_to(LEFT * 1.6 + DOWN * 0.3)
        t = label(rf"all {g['total']:,} dissonances against the bass in Palestrina's {g['pieces']:,} movements, \ in 100s".replace(",", "{,}"), font_size=20, color=GREY_A).to_edge(UP, buff=0.6)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (rf"free: \ {100 * sh['free']:.1f} in 100", RED),
            (rf"half the movements: \ under {100 * d['palestrina_free_quantiles'][1]:.0f} in 100", WHITE),
            (r"some `free' ones are the program's: \ figures it does not know, \ encoding slips", GREY_A))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 3.9))
        side.move_to(RIGHT * 5.0 + DOWN * 0.2)
        with self.voiceover(
            f"Now count. A program finds every dissonance against the bass in all {say(g['pieces'])} movements, "
            f"{say(g['total'])} of them, and classifies each by how it is approached and left. <bookmark mark='a'/> "
            f"{say(round(100 * sh['passing']))} in a hundred are passing notes, {say(round(100 * sh['suspension']))} "
            f"suspensions, {say(round(100 * sh['neighbour']))} neighbours, and a handful cambiatas and anticipations. "
            f"<bookmark mark='b'/> Only {100 * sh['free']:.1f} in a hundred fit none of the rules, <bookmark mark='c'/> and "
            f"in half the movements the share is below {say(round(100 * d['palestrina_free_quantiles'][1]))} in a hundred. "
            "<bookmark mark='d'/> Some of those few are not Palestrina's at all but the program's: figures it was not "
            "told about, and slips in the encoding. A style can be a set of rules followed ninety-seven times in a "
            "hundred, and that is what Jeppesen meant."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("kinds")
        c = clip("kinds.prepared")
        q = d["quiz"]
        card = listen_card(r"The same cadence twice: \ a seventh against the bass resolving down. \ In one, \ the seventh is held over from a consonance \ "
                           r"(prepared); \ in the other, \ it is struck from a leap. \ Which one is prepared, \ A or B?", width=10.6)
        with self.voiceover(
            "Your turn. The same small cadence twice: a seventh against the bass, falling to a sixth. In one the seventh "
            "is prepared, held over from a consonance; in the other it is struck, arrived at by a leap. Which one is "
            "prepared, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll(q["A"], width=4.6, height=2.0, colors=[TUNE, GREY_A], lo=53, hi=76, bar_h=0.14).move_to(LEFT * 3.2 + DOWN * 0.2)
        gB = voices_roll(q["B"], width=4.6, height=2.0, colors=[TUNE, GREY_A], lo=53, hi=76, bar_h=0.14).move_to(RIGHT * 3.2 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.35)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.35)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"two synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, q["A"], d["quiz_starts"]["A"], q["unit"], colors=[TUNE, GREY_A])
            flash_voices(snd, gB, q["B"], d["quiz_starts"]["B"], q["unit"], colors=[TUNE, GREY_A])
            pulse(snd, la, d["quiz_starts"]["A"], d["quiz_starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["quiz_starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"struck from a leap: \ free", font_size=22, color=RED).next_to(gA, DOWN, buff=0.35),
                     label(r"held over: \ a suspension", font_size=22, color=EAR).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "B is prepared. The upper voice sings C over A, a consonance, and simply stays while the bass moves to D "
            "beneath it: now it is a seventh, and it falls to B, a sixth. In A the same seventh arrives by a leap, with "
            "no preparation. In Palestrina, B happens tens of thousands of times; A almost never. Keep A in mind for "
            "chapter nine."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
