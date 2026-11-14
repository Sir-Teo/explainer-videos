from __future__ import annotations

import numpy as np

from videos.music.music10.common import *  # noqa: F403


def human(n: float) -> str:
    if n >= 1e6:
        return rf"{n / 1e6:.1f} MB"
    if n >= 1e3:
        return rf"{n / 1e3:.0f} kB" if n >= 1e4 else rf"{n / 1e3:.1f} kB"
    return rf"{n:.0f} bytes"


def bar_rows(rows, per_decade: float = 1.3, step: float = 0.56, font_size: int = 26, x0: float = -2.6) -> VGroup:
    """Horizontal bars on a logarithmic axis: ``rows`` are (name, bytes, colour)."""
    g = VGroup()
    g.rows = []
    for k, (name, n, col) in enumerate(rows):
        y = -k * step
        w = per_decade * np.log10(n)
        bar = Rectangle(width=w, height=step * 0.62, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([x0 + w / 2, y, 0])
        nm = label(name, font_size=font_size, color=GREY_A).next_to(bar, LEFT, buff=0.2)
        val = label(human(n), font_size=font_size, color=col).next_to(bar, RIGHT, buff=0.15)
        r = VGroup(bar, nm, val)
        g.add(r)
        g.rows.append(r)
    ticks = VGroup()
    for p in range(1, 8):
        x = x0 + per_decade * p
        ticks.add(Line([x, step * 0.5, 0], [x, -(len(rows) - 0.5) * step, 0], color=GREY_D, stroke_width=1))
    g.add_to_back(ticks)
    return g


class Bits(SoundScene):
    def construct(self):
        chapter(self, 9, r"How many bits?", r"How much of the music is on the page?")
        self.sizes()
        self.count()
        self.quiz()
        self.rules()

    # ------------------------------------------------------------------
    def sizes(self):
        d = load("bits")
        s, a = d["sizes"], d["audio"]
        rows = [(r"gongche, \ as text", s["gongche"], TUNE), (r"jianpu, \ as text", s["jianpu"], TUNE), (r"MIDI", s["MIDI"], TUNE), (r"MEI", s["MEI"], TUNE), (r"MusicXML", s["MusicXML"], TUNE),
                (r"sound: \ Opus", a["Opus"], AIR), (r"sound: \ MP3", a["MP3"], AIR), (r"sound: \ lossless (FLAC)", a["FLAC"], AIR), (r"sound: \ as on a CD", a["WAV"], AIR)]
        bars = bar_rows(rows).move_to(DOWN * 0.3)
        bars.shift(LEFT * bars.get_center()[0])
        head = label(r"one tune, \ forty-two notes: \ how many bytes?", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"each grid line is ten times the one before", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now let us count. One tune, forty-two notes. How many bytes does it take? <bookmark mark='a'/> "
            f"Written as text, in gongche or in jianpu, about {say(round(s['jianpu'], -1))}. As a MIDI "
            f"file, {say(s['MIDI'])}. As MusicXML, more than five thousand, because XML spells everything "
            f"out. <bookmark mark='b'/> And as sound? The Tune played once on our piano lasts "
            f"{say(d['seconds'])} seconds. Stored the way a compact disc stores sound, that is "
            f"{say(a['WAV'] / 1e6, 1)} million bytes. Packed without any loss, {say(round(a['FLAC'] / 1e3, -1))} "
            f"thousand. As an MP3, {say(round(a['MP3'] / 1e3, -1))} thousand. The axis here is logarithmic: "
            "every grid line is ten times the one before it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars[0]), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in bars.rows[:5]], lag_ratio=0.5), run_time=6.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in bars.rows[5:][::-1]], lag_ratio=0.6), run_time=7.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("bits")
        ratio = round(d["ratio"], -3)
        lines = VGroup(
            MathTex(r"42 \text{ notes} \times (\underbrace{3}_{\text{one of 6 pitches}} + \underbrace{1}_{\text{one of 2 lengths}}) \text{ bits} = " + str(d["plain_bits"]) + r" \text{ bits}", font_size=36),
            MathTex(r"\text{three phrases, used as } A\,A'\,B\,B\,A\,A': \quad 3 \times 7 \times 4 + 6 \times 2 = " + str(d["structured_bits"]) + r" \text{ bits}", font_size=36),
            MathTex(rf"\text{{the sound: }} {d['seconds']:.1f} \text{{ s}} \times 48{{,}}000 \times 16 \text{{ bits}} = {d['audio_bits'] / 1e6:.1f} \text{{ million bits}}", font_size=36, color=AIR),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(UP * 1.2)
        big = VGroup(label(r"sound : page \ $\approx$", font_size=36, color=GREY_A), label(r"{:,.0f} : 1".format(ratio).replace(",", "{,}"), font_size=56, color=TUNE)).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.7)
        cmp_ = label(rf"MP3 : CD sound \ $\approx$ \ 1 : {d['audio']['WAV'] / d['audio']['MP3']:.0f}; \ \ Opus \ 1 : {d['audio']['WAV'] / d['audio']['Opus']:.0f}", font_size=28, color=AIR).next_to(big, DOWN, buff=0.45)
        with self.voiceover(
            "Those are files, with their overheads. How few bits would do? The Tune uses six different "
            "pitches, which takes three bits, and two lengths, which takes one. Four bits a note, "
            f"forty-two notes: {say(d['plain_bits'])} bits. Twenty-one bytes. <bookmark mark='a'/> And the "
            "Tune repeats itself. It has only three different phrases, used in the order A, A, B, B, A, A. "
            f"Describe it that way and {say(d['structured_bits'])} bits are enough. <bookmark mark='b'/> "
            f"The sound, at forty-eight thousand samples a second and sixteen bits a sample, is "
            f"{say(d['audio_bits'] / 1e6, 1)} million bits. <bookmark mark='c'/> So the sound holds about "
            f"{say(ratio / 1000)} thousand times as many bits as the page. Compare the best that audio "
            "engineering can do. <bookmark mark='d'/> An MP3 shrinks this sound six times; a modern codec, "
            "sixteen. A score shrinks it a hundred thousand times. No algorithm does that. The score gets "
            "away with it because its decoder is a trained musician with an instrument. And that tells "
            "you where the other bits are. They are not on the page. The player supplies them."
        ) as vo:
            self.play(FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]))
            vo.wait_until("c")
            self.play(FadeIn(big))
            vo.wait_until("d")
            self.play(FadeIn(cmp_))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("bits")
        c = clip("bits.pair")
        st = Staff(phrase_score(0, 4), width=11.6, space=0.2, show_time=False).move_to(UP * 1.6)
        self.st = st
        card = listen_card(r"The same fourteen notes, \ twice. \ One is a machine playing the page exactly. \ Which?", width=9.6).move_to(DOWN * 1.2)
        with self.voiceover("How much does the player supply? Here are the same fourteen notes, twice. One of the two is a machine playing the page exactly as written. Which?"):
            self.play(FadeIn(st), FadeIn(card))
        self.wait(1.0)
        bx = boxes(("A", "B"), buff=1.2, width=2.4, height=1.2, font_size=48).move_to(DOWN * 1.3)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], snd.time_of("A"), snd.time_of("B") - 1.0)
            pulse(snd, bx[1], snd.time_of("B"), c.duration)
            light(snd, [n.ink for n in st.notes] * 2, d["times"]["A"] + d["times"]["B"], end=c.duration)
            for t in d["times"]["A"] + d["times"]["B"]:
                snd.wait_until(t)
                self.play(bx[0 if t < snd.time_of("B") - 0.5 else 1][1].animate(rate_func=there_and_back).scale(1.12), run_time=0.2)
        self.play(FadeOut(bx))

    # ------------------------------------------------------------------
    def rules(self):
        d = load("bits")
        st = self.st
        xs = [n.head.get_x() for n in st.notes]
        y_ms, y_db = -0.6, -2.3
        base_ms = Line([xs[0] - 0.4, y_ms, 0], [xs[-1] + 0.4, y_ms, 0], color=GREY_C, stroke_width=1.5)
        base_db = Line([xs[0] - 0.4, y_db, 0], [xs[-1] + 0.4, y_db, 0], color=GREY_C, stroke_width=1.5)
        ms_bars = VGroup(*[Rectangle(width=0.3, height=max(abs(v) * 0.011, 0.02), stroke_width=0, fill_color=TIME, fill_opacity=0.9).move_to([x, y_ms + v * 0.0055, 0]) for x, v in zip(xs, d["ms"])])
        db_bars = VGroup(*[Rectangle(width=0.3, height=max(abs(v) * 0.14, 0.02), stroke_width=0, fill_color=LEVEL, fill_opacity=0.9).move_to([x, y_db + v * 0.07, 0]) for x, v in zip(xs, d["db"])])
        l_ms = VGroup(label(r"late", font_size=20, color=TIME), label(r"early", font_size=20, color=TIME)).arrange(DOWN, buff=0.5).next_to(base_ms, LEFT, buff=0.15)
        l_db = VGroup(label(r"louder", font_size=20, color=LEVEL), label(r"softer", font_size=20, color=LEVEL)).arrange(DOWN, buff=0.5).next_to(base_db, LEFT, buff=0.15)
        facts = VGroup(label(rf"up to {d['largest_ms']:.0f} ms off the beat", font_size=24, color=TIME).next_to(base_ms, RIGHT, buff=-3.2).shift(UP * 0.75),
                       label(rf"a range of {d['db_range']:.0f} dB", font_size=24, color=LEVEL).next_to(base_db, RIGHT, buff=-2.4).shift(UP * 0.75))
        with self.voiceover(
            "B was the machine. A was the same page played by four rules that researchers have measured "
            "in real performances. Each phrase speeds up into its middle and relaxes at its end. The "
            "faster, the louder. The ending slows the way a runner comes to a stop. And a repeated note "
            "is separated from the one before. <bookmark mark='a'/> Here is how far A strayed from the "
            f"page. Against a steady beat its notes come up to {say(d['largest_ms'])} milliseconds early "
            f"or late. <bookmark mark='b'/> Their levels range over {say(d['db_range'])} decibels. And the "
            f"last note is held {say(d['last_ratio'], 1)} times its written length. None of this is on "
            "the page. <bookmark mark='c'/> To write it down, for every note when exactly, how long "
            f"exactly, and how loud, takes about nineteen more bits a note: {say(d['perf_bits'])} bits, "
            "five times what the notes themselves took. That is what a piano roll or a MIDI file of a "
            f"performance holds. And it is still about {say(round(d['audio_bits'] / (d['perf_bits'] + d['plain_bits']), -3) / 1000)} "
            "thousand times smaller than the sound. The rest of the bits are the piano and the room, "
            "which was Act One."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(base_ms), FadeIn(l_ms), LaggedStart(*[GrowFromEdge(b, DOWN if v > 0 else UP) for b, v in zip(ms_bars, d["ms"])], lag_ratio=0.1), FadeIn(facts[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(base_db), FadeIn(l_db), LaggedStart(*[GrowFromEdge(b, DOWN if v > 0 else UP) for b, v in zip(db_bars, d["db"])], lag_ratio=0.1), FadeIn(facts[1]), run_time=2.5)
            vo.wait_until("c")
            total = label(rf"the performance: \ about {d['perf_bits']} more bits; \ \ the page: \ {d['plain_bits']}; \ \ the sound: \ {d['audio_bits'] / 1e6:.1f} million", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.3)
            self.play(FadeIn(total))
        self.wait(0.4)
        self.clear_scene()
