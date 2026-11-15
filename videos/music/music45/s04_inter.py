from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403


class Inter(SoundScene):
    def construct(self):
        chapter(self, 3, r"Melodies hidden in melodies", r"Can a familiar tune vanish in plain hearing?")
        self.quiz()
        self.dowling()
        self.compound()
        self.hocket()
        self.bach()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("inter")
        c = clip("inter.three")
        card = listen_card(r"A well-known tune is hidden here, \ note by note between the notes of another line. \ "
                           r"Name it if you can; \ you will hear it twice, \ then once more, \ changed.", width=10.4)
        with self.voiceover(
            "A question for your ears. A well-known tune is hidden here, its notes alternating with the notes of another "
            "line. Name it if you can. You will hear it twice, and then once more, changed."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        keys = []
        cols = []
        for a, b in zip(d["tune"], d["distractor"]):
            keys += [a, b]
            cols += [GREY_B, GREY_B]
        r = keyroll(keys, width=11.0, height=2.0, lo=60, hi=80, colors=cols).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(r))
        st = d["starts"]
        ioi = d["ioi"]
        with self.listen(c) as snd:
            window(snd, r"a hidden tune", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k in ("same", "again"):
                flash(snd, r.notes, [st[k] + i * ioi for i in range(len(keys))], hot=WHITE, base=GREY_B)
            flash(snd, r.notes, [st["apart"] + i * ioi for i in range(len(keys))], hot=WHITE, base=GREY_B)
        for i, b in enumerate(r.notes):
            if i % 2 == 0:
                b.set_fill(TUNE, 1.0)
        ans = VGroup(label(r"Fr\`ere Jacques: \ gold, \ the tune; \ grey, \ the other line", font_size=21, color=TUNE),
                     label(rf"in the same register the two lines cross {d['crossings']} times in 16 notes; \ moved an octave and a half lower, \ never", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "It is Frère Jacques. In the same register the two lines cross "
            f"{say(d['crossings'])} times in sixteen notes, and most people cannot pick out the tune at all, even knowing it "
            "is there. The third time, the other line moved an octave and a half lower, and the tune stepped out at once."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dowling(self):
        items = [
            (r"W. Jay Dowling \ (1973): \ two familiar tunes interleaved, \ about eight notes a second", WHITE),
            (r"in the same register, \ listeners could not name them", WHITE),
            (r"separate them in pitch range, \ or in loudness or timbre, \ and both came out", WHITE),
            (r"but knowing which tune to listen for helped even when they overlapped: \ expectation steers grouping", TUNE),
            (r"Variation 45 uses timbre alone", GREY_A),
        ]
        rows_scene(self, r"interleaved melodies", items,
                   "This is W. Jay Dowling's experiment of 1973. <bookmark mark='b'/> He interleaved two familiar tunes at about "
                   "eight notes a second, <bookmark mark='c'/> and in the same register listeners could not name them. "
                   "<bookmark mark='d'/> Separate them in pitch range, or in loudness or timbre, and both came out. "
                   "<bookmark mark='e'/> But knowing which tune to listen for helped even when they overlapped: expectation "
                   "steers grouping. <bookmark mark='f'/> Variation 45, at the end of this part, uses timbre alone.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def compound(self):
        d = load("compound")
        c = clip("compound.two")
        line = d["line"]
        r = keyroll(line, width=10.0, height=2.0, lo=52, hi=75, colors=[TUNE if m < 70 else BLUE for m in line]).move_to(UP * 0.5)
        cells = VGroup(label(r"slow: \ one zig-zag line", font_size=20, color=WHITE), label(r"fast: \ two voices?", font_size=20, color=WHITE)).arrange(RIGHT, buff=2.0).to_edge(DOWN, buff=1.1)
        head = label(r"one line, \ two voices", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Streaming can also be used on purpose. Here is one line of ours that alternates between a moving lower part and "
            "a repeated high C. Hear it slowly, then fast."
        ):
            self.play(FadeIn(head), FadeIn(r), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"slow, \ then fast", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, ioi in zip(("slow", "fast"), d["iois"]):
                flash(snd, r.notes, [st[k] + i * ioi for i in range(len(line))] , hot=WHITE, base=GREY_A)
                flash(snd, r.notes, [st[k] + (i + len(line)) * ioi for i in range(len(line))], hot=WHITE, base=GREY_A)
            pulse(snd, cells[0], st["slow"], st["fast"] - 0.4, buff=0.1)
            pulse(snd, cells[1], st["fast"], c.duration, buff=0.1)
        with self.voiceover(
            "Slowly it is a single zig-zag line. Fast, it splits: a melody below and a high pedal note above, two voices "
            "from one instrument playing one note at a time."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bach(self):
        items = [
            (r"composers knew this long before the experiments: \ `implied polyphony', \ or compound melody", WHITE),
            (r"Bach's suites for solo cello and partitas for solo violin write two and three voices for one line", WHITE),
            (r"Baroque guitar and lute music, \ and Telemann's flute fantasias, \ do the same", WHITE),
            (r"the composer controls the split with leap size and speed, \ exactly van Noorden's two variables", TUNE),
            (r"and the trick can be reversed", GREY_A),
        ]
        rows_scene(self, r"implied polyphony", items,
                   "Composers knew this long before the experiments, and called it implied polyphony, or compound melody. "
                   "<bookmark mark='b'/> Bach's suites for solo cello and partitas for solo violin write two and three voices "
                   "for a single line. <bookmark mark='c'/> Baroque lute music and Telemann's fantasias for solo flute do the "
                   "same. <bookmark mark='d'/> The composer controls the split with leap size and speed, exactly van Noorden's "
                   "two variables. <bookmark mark='e'/> And the trick can be reversed.", marks="bcde")

    # ------------------------------------------------------------------
    def hocket(self):
        items = [
            (r"the reverse also works: \ two players alternating notes can make one melody", WHITE),
            (r"medieval hocket \ (Part 23) \ and the interlocking parts of Part 37's mbira and gamelan", WHITE),
            (r"for the parts to fuse into one line, \ they must share register and timbre, \ and leave no gaps", WHITE),
            (r"the same rules, \ read backwards: \ proximity binds what was played apart", TUNE),
            (r"chapter 4: \ sounds that arrive at the same moment", GREY_A),
        ]
        rows_scene(self, r"hocket: \ the trick reversed", items,
                   "The reverse works too. <bookmark mark='b'/> Two players alternating notes can make one melody: medieval "
                   "hocket, from Part 23, and the interlocking parts of Part 37's mbira and gamelan. <bookmark mark='c'/> For the "
                   "parts to fuse into one line they must share register and timbre, and leave no gaps. <bookmark mark='d'/> The "
                   "same rules, read backwards: proximity binds what was played apart. <bookmark mark='e'/> Chapter four turns to "
                   "sounds that arrive at the same moment.", marks="bcde")
