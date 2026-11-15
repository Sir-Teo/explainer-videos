from __future__ import annotations

import numpy as np

from videos.music.music53.common import *  # noqa: F403


def byte_cells(hexs, colors, size=0.62, font=17):
    g = VGroup()
    for h, c in zip(hexs, colors):
        g.add(VGroup(Square(side_length=size, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.15), label(h, font_size=font, color=WHITE)).arrange(ORIGIN))
    return g.arrange(RIGHT, buff=0.06)


class Bytes(SoundScene):
    def construct(self):
        chapter(self, 3, r"MIDI, \ byte by byte", r"What exactly goes down the cable?")
        self.wire()
        self.message()
        self.keypress()
        self.running()
        self.smear()
        self.others()

    # ------------------------------------------------------------------
    def wire(self):
        bits = [0] + [int(b) for b in format(0x90, "08b")[::-1]] + [1]
        cells = VGroup(*[VGroup(Rectangle(width=0.62, height=0.62, stroke_color=GREY_B, stroke_width=1.5, fill_color=(EAR if i in (0, 9) else TUNE), fill_opacity=0.15 + 0.5 * b),
                               label(str(b), font_size=18, color=WHITE)).arrange(ORIGIN) for i, b in enumerate(bits)]).arrange(RIGHT, buff=0.05).move_to(UP * 0.8)
        tags = VGroup(label(r"start", font_size=14, color=EAR).next_to(cells[0], DOWN, buff=0.15), label(r"eight data bits, \ lowest first", font_size=14, color=TUNE).next_to(cells[1:9], DOWN, buff=0.15),
                      label(r"stop", font_size=14, color=EAR).next_to(cells[9], DOWN, buff=0.15))
        notes = VGroup(label(r"31,250 bits a second \ (a 1 MHz clock divided by 32): \ ten bits a byte, \ 320 microseconds", font_size=18, color=WHITE),
                       label(r"a current loop through an opto-isolator: \ no ground shared, \ no hum between instruments", font_size=18, color=GREY_A),
                       label(r"one direction per cable: \ out, \ in, \ and thru to chain the next instrument", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"one byte on the wire", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Start with the wire. <bookmark mark='a'/> MIDI is a serial line: each byte is sent as a start bit, eight data bits "
            "lowest first, and a stop bit. <bookmark mark='b'/> At thirty-one thousand two hundred and fifty bits a second, a "
            "speed chosen because it is a one-megahertz clock divided by thirty-two, a byte takes three hundred and twenty "
            "microseconds. The signal is a current loop through an opto-isolator, so instruments share no ground and no hum; "
            "and each cable carries one direction, out, in, or thru to chain the next instrument."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(cells, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(tags))
            vo.wait_until("b")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def message(self):
        msg = byte_cells(["90", "3C", "64"], [EAR, TUNE, BLUE], size=0.9, font=24).move_to(UP * 1.2)
        tl = VGroup(label(r"status: \ note on, \ channel 1", font_size=16, color=EAR).next_to(msg[0], DOWN, buff=0.3),
                    label(r"key 60: \ middle C", font_size=16, color=TUNE).next_to(msg[1], DOWN, buff=0.3).shift(DOWN * 0.45),
                    label(r"velocity 100", font_size=16, color=BLUE).next_to(msg[2], DOWN, buff=0.3))
        rows = VGroup(label(r"a status byte has its top bit set \ (128 to 255); \ a data byte does not \ (0 to 127): \ seven bits, \ 128 values", font_size=18, color=WHITE),
                      label(r"the status's high four bits are the kind: \ 9 note on, \ 8 note off, \ B controller, \ E pitch bend, \ C program", font_size=18, color=GREY_A),
                      label(r"its low four bits are the channel: \ sixteen instruments on one cable", font_size=18, color=GREY_A),
                      label(r"MIDI says which key and how hard, \ never what it sounds like: \ a score, \ not a sound", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        head = label(r"one note, \ three bytes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A note is three bytes. <bookmark mark='a'/> Hexadecimal nine zero: note on, channel one. Three C: key sixty, middle "
            "C. Six four: velocity one hundred, how hard. <bookmark mark='b'/> The rule that makes the stream readable: a status "
            "byte has its top bit set, a data byte does not, so data has seven bits and a hundred and twenty-eight values. "
            "<bookmark mark='c'/> The status byte's high half is the kind of message, nine for note on, eight for off, B for a "
            "controller, E for pitch bend; its low half is the channel, so sixteen instruments share one cable. "
            "<bookmark mark='d'/> And notice what is missing: MIDI says which key and how hard, never what it sounds like. It is "
            "a score, not a sound."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(msg, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(msg), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def running(self):
        d = load("bytes")
        p = d["plain_hex"].split()
        r = d["running_hex"].split()

        def colors(hs):
            return [EAR if int(h, 16) & 0x80 else TUNE for h in hs]
        a = byte_cells(p, colors(p), size=0.5, font=14).move_to(UP * 1.0)
        b = byte_cells(r, colors(r), size=0.5, font=14).move_to(DOWN * 0.6)
        la = label(rf"plain: \ every message has its status \ ({d['plain_bytes']} bytes for the phrase)", font_size=17, color=WHITE).next_to(a, UP, buff=0.25)
        lb = label(rf"running status: \ a repeated status is left out, \ and a note-off is sent as note-on at velocity 0 \ ({d['running_bytes']} bytes)", font_size=17, color=TUNE).next_to(b, UP, buff=0.25)
        key = label(r"pink: \ status bytes; \ gold: \ data", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.6)
        head = label(r"the Tune's first phrase on the wire", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        save = 100 * (1 - d["running_bytes"] / d["plain_bytes"])
        with self.voiceover(
            f"The Tune's first phrase is {say(d['messages'])} messages, a note on and a note off for each note. <bookmark mark='a'/> "
            f"Sent plainly that is {say(d['plain_bytes'])} bytes. <bookmark mark='b'/> But a receiver can remember the last "
            "status: if the next message has the same one, it is left out, running status. And a note off can be sent as a note "
            f"on with velocity zero to keep the status the same. The phrase shrinks to {say(d['running_bytes'])} bytes, "
            f"{say(save)} per cent less, and our decoder reads it back exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def smear(self):
        d = load("bytes")
        n = d["sizes"]
        lp = line_plot([d["spread"]["plain"], d["spread"]["running"]], width=7.0, height=3.4, ylo=0, yhi=16, colors=[EAR, TUNE],
                       yticks=(0, 5, 10, 15), ylabel=r"last note arrives, \ ms", size=16).move_to(LEFT * 1.2 + DOWN * 0.2)
        xt = VGroup(*[label(str(k), font_size=14, color=GREY_A).next_to(lp.to(k - 1, 0), DOWN, buff=0.1) for k in (1, 4, 8, 12, 16)])
        xl = label(r"notes in the chord", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        key = VGroup(label(r"plain", font_size=17, color=EAR), label(r"running status", font_size=17, color=TUNE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(lp, RIGHT, buff=0.5)
        note = label(r"for comparison: \ sound travels 3.4 m in 10 ms; \ a drummer and a bassist a few metres apart live with this", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"how long a chord takes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "So how long does a chord take? <bookmark mark='a'/> Each note adds three bytes plainly, two with running status: "
            f"sixteen notes take {say(d['spread']['plain'][-1], 1)} milliseconds plainly and {say(d['spread']['running'][-1], 1)} "
            "with running status. <bookmark mark='b'/> For comparison, sound travels three and a half metres in ten "
            "milliseconds: a drummer and a bassist a few metres apart live with that every night. A chord is safe; but a dense "
            "passage with controllers moving on several channels can fill the cable, and then everything waits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lp[0]), FadeIn(lp[2:]), FadeIn(xt), FadeIn(xl), FadeIn(ghost(lp.lines, 0.3)))
            vo.wait_until("a")
            self.play(Create(lp.lines[0]), Create(lp.lines[1]), FadeIn(key), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def others(self):
        items = [
            (r"controllers: \ B0 cc value: \ the mod wheel is 1, \ volume 7, \ the sustain pedal 64", WHITE),
            (r"pitch bend: \ two data bytes make 14 bits, \ 16,384 steps, \ 8192 at rest", WHITE),
            (r"program change: \ choose one of 128 sounds; \ General MIDI \ (1991) \ fixed which: \ 1 is a piano, \ 41 a violin", WHITE),
            (r"system messages: \ a clock 24 times a beat to keep machines in step, \ and system exclusive for anything else", WHITE),
            (r"in all, \ a handful of message types; \ the rest is convention", TUNE),
        ]
        rows_scene(self, r"the other messages", items,
                   "A few more messages complete the language. <bookmark mark='b'/> Controllers: B, the controller number, the "
                   "value. The modulation wheel is one, volume seven, the sustain pedal sixty-four. <bookmark mark='c'/> Pitch bend "
                   "uses two data bytes for fourteen bits, sixteen thousand three hundred and eighty-four steps, with eight thousand "
                   "one hundred and ninety-two at rest. <bookmark mark='d'/> Program change chooses one of a hundred and twenty-eight "
                   "sounds, and General MIDI, in 1991, fixed which: one is a piano, forty-one a violin. <bookmark mark='e'/> System "
                   "messages send a clock twenty-four times a beat to keep machines in step, and system exclusive carries anything "
                   "else. <bookmark mark='f'/> In all, a handful of message types; the rest is convention.", marks="bcdef")

    # ------------------------------------------------------------------
    def keypress(self):
        items = [
            (r"a key closes two contacts, \ one early in its travel and one at the bottom", WHITE),
            (r"the time between them measures how fast it moved: \ a few milliseconds is loud, \ tens of milliseconds soft", WHITE),
            (r"the keyboard's processor scans every key many times a millisecond and turns that time into a velocity, \ 1 to 127", WHITE),
            (r"then three bytes leave the five-pin socket", WHITE),
            (r"the velocity is a measurement of a gesture: \ how the receiving instrument uses it is up to the instrument", TUNE),
        ]
        rows_scene(self, r"inside a keyboard", items,
                   "Where do the three bytes come from? <bookmark mark='b'/> Each key closes two contacts, one early in its travel "
                   "and one at the bottom. <bookmark mark='c'/> The time between them measures how fast the key moved: a few "
                   "milliseconds is loud, tens of milliseconds soft. <bookmark mark='d'/> The keyboard's processor scans every key many times a "
                   "millisecond and turns that time into a velocity from one to a hundred and twenty-seven, <bookmark mark='e'/> "
                   "and three bytes leave the socket. <bookmark mark='f'/> The velocity is a measurement of a gesture; what the "
                   "receiving instrument does with it is up to the instrument.", marks="bcdef")
