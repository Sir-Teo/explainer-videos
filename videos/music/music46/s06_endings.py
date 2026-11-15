from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403

EC = {"expected": TUNE, "delayed": BLUE, "denied": EAR}


class Endings(SoundScene):
    def construct(self):
        chapter(self, 5, r"Three endings", r"What does delay do to an ending?")
        self.hear()
        self.drawn()
        self.again()
        self.qualia()
        self.devices()
        self.susp()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("endings")
        c = clip("endings.three")
        rows_ = VGroup()
        for k in ("expected", "delayed", "denied"):
            notes = d[k]["notes"]
            mel, t = [], 0.0
            for m, b in notes:
                mel.append([60 + m, t, b])
                t += b
            r = mroll(mel, width=8.6, height=0.9, lo=55, hi=68, color=EC[k], total=16, bar_h=0.13)
            rows_.add(VGroup(label(k, font_size=21, color=EC[k]), r).arrange(RIGHT, buff=0.5))
        rows_.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 0.1)
        head = label(r"the Tune's last phrase, \ three ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are the three endings this part will give the Tune. Expected: down to C over the tonic. Delayed: down "
            "to A over A minor, the deceptive turn, then round again to C. Denied: up to F sharp over D, and stop."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        st = d["starts"]
        beat = d["beat"]
        with self.listen(c) as snd:
            window(snd, r"three endings", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            for i, k in enumerate(("expected", "delayed", "denied")):
                ts, t = [], 0.0
                for m, b in d[k]["notes"]:
                    ts.append(st[k] + t * beat)
                    t += b
                flash(snd, rows_[i][1].notes, ts, hot=WHITE, base=EC[k])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drawn(self):
        d = load("endings")
        rows_ = VGroup()
        for k in ("expected", "delayed", "denied"):
            ic = d[k]["ic"]
            g = bits_plot(ic, width=0.75 * len(ic), height=1.2, top=11.0, color=EC[k])
            nums = VGroup(*[label(rf"{v:.1f}", font_size=12, color=WHITE).next_to(g[i + 1], UP, buff=0.05) for i, v in enumerate(ic)])
            rows_.add(VGroup(label(k, font_size=20, color=EC[k]), VGroup(g, nums)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN))
        rows_.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(DOWN * 0.1)
        e = d["expected"]["ic"][-1]
        dl = d["delayed"]["ic"]
        de = d["denied"]["ic"][-1]
        head = label(r"surprise, \ note by note, \ in bits", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The listener's surprise for each note. <bookmark mark='a'/> Expected: the last C costs "
            f"{say(e, 1)} bits. <bookmark mark='b'/> Delayed: the deceptive A costs {say(dl[6], 1)} bits, a real jolt; "
            f"but when C finally comes it costs only {say(dl[-1], 1)}, less than in the plain ending. Delay made the "
            "resolution more certain, and arguably more satisfying: Meyer's point, in numbers. <bookmark mark='c'/> "
            f"Denied: F sharp costs {say(de, 1)} bits, and nothing comes after to repair it."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def devices(self):
        items = [
            (r"the deceptive cadence: \ V to vi instead of V to I \ (Part 18)", WHITE),
            (r"the suspension and the appoggiatura: \ the right note arrives late, \ after a dissonance \ (Part 16)", WHITE),
            (r"the long dominant pedal before a recapitulation \ (Part 21): \ wanting, \ prolonged", WHITE),
            (r"the anticipatory build and drop of dance music \ (Part 40): \ the same device, \ engineered", TUNE),
            (r"chapter 6: \ what the brain does at a wrong chord", GREY_A),
        ]
        rows_scene(self, r"devices of delay", items,
                   "Composers have many devices of delay. <bookmark mark='b'/> The deceptive cadence, five to six instead of five "
                   "to one, from Part 18. <bookmark mark='c'/> The suspension and the appoggiatura, where the right note arrives "
                   "late, after a dissonance, from Part 16. <bookmark mark='d'/> The long dominant pedal before a "
                   "recapitulation, Part 21's: wanting, prolonged. <bookmark mark='e'/> And the build and drop of dance music, "
                   "Part 40's, the same device engineered. <bookmark mark='f'/> Chapter six asks what the brain does at a wrong "
                   "chord.", marks="bcdef")

    # ------------------------------------------------------------------
    def again(self):
        d = load("again")
        c = clip("again.three")
        cells = VGroup(*[VGroup(label(rf"time {i + 1}", font_size=20, color=WHITE), label(rf"F$\sharp$: \ {v:.1f} bits", font_size=19, color=EAR)).arrange(DOWN, buff=0.2) for i, v in enumerate(d["ic"])]).arrange(RIGHT, buff=1.4).move_to(UP * 0.3)
        head = label(r"the denied ending, \ three times running", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover("What if the denial is repeated? Hear the denied ending three times running."):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"denied, \ three times", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            third = c.duration / 3
            for i in range(3):
                pulse(snd, cells[i], i * third, (i + 1) * third, buff=0.1)
        v = d["ic"]
        with self.voiceover(
            f"The listener's surprise at F sharp falls from {say(v[0], 1)} bits to {say(v[1], 1)} and then {say(v[2], 1)}: "
            "the short-term model learns the piece's own rule. Repeat a surprise and it becomes a feature of the style, "
            "which is how many musical languages grow."
        ):
            self.play(Indicate(cells[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def susp(self):
        d = load("susp")
        c = clip("susp.two")
        cells = VGroup(label(r"I \ IV \ V \ I", font_size=24, color=TUNE), label(r"I \ IV \ V$^{4-3}$ \ V \ I: \ a suspension", font_size=24, color=BLUE)).arrange(RIGHT, buff=1.4).move_to(UP * 0.3)
        head = label(r"a delay inside one chord", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is the smallest delay of all. A plain cadence; then the same with a suspension, the C held over from the "
            "previous chord into the dominant, clashing, before it falls to B."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"plain, \ then suspended", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["plain"], st["suspended"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["suspended"], c.duration, buff=0.1)
        with self.voiceover("One held note, one beat of wanting, and the cadence lands harder."):
            self.play(Indicate(cells[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def qualia(self):
        items = [
            (r"Huron asked listeners to describe how scale degrees feel at the end of a phrase", WHITE),
            (r"the tonic: \ stable, \ home, \ finished; \ the fifth: \ strong but open", WHITE),
            (r"the leading note: \ unstable, \ yearning, \ pointing upward; \ the raised fourth: \ strange, \ lifting", WHITE),
            (r"the feelings track the statistics: \ the more often a degree is followed by a particular note, \ the more it seems to lean", TUNE),
            (r"the `tendencies' of Meyer and of Part 15, \ heard as qualities", GREY_A),
        ]
        rows_scene(self, r"how scale degrees feel", items,
                   "Huron also asked listeners to describe how each scale degree feels at the end of a phrase. "
                   "<bookmark mark='b'/> The tonic: stable, home, finished. The fifth: strong, but open. <bookmark mark='c'/> The "
                   "leading note: unstable, yearning, pointing upward. The raised fourth: strange, lifting. "
                   "<bookmark mark='d'/> The feelings track the statistics: the more reliably a degree is followed by one "
                   "particular note, the more it seems to lean towards it. <bookmark mark='e'/> These are Meyer's tendencies, and "
                   "Part 15's, heard as qualities.", marks="bcde")
