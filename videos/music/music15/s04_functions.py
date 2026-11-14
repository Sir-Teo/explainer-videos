from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Functions(SoundScene):
    def construct(self):
        chapter(self, 3, r"Three jobs", r"What do the chords of a key do?", extra=((1893, r"Riemann's three functions"),))
        self.table()
        self.listen_three()
        self.harmonize()

    # ------------------------------------------------------------------
    def table(self):
        d = load("functions")
        rows = d["rows"]
        cells = VGroup()
        for k, r in enumerate(rows):
            col = FUNC_C[r["function"]]
            notes = VGroup(*[label(str(x), font_size=28, color=WHITE if x in (1, 3, 5) else EAR) for x in r["degrees"]]).arrange(UP, buff=0.12)
            cells.add(VGroup(label(tex(r["roman"]), font_size=36, color=col), notes).arrange(UP, buff=0.3))
        cells.arrange(RIGHT, buff=0.75, aligned_edge=DOWN).scale(1.35).move_to(UP * 0.4)
        legend = VGroup(label(r"white: \ degrees 1, \ 3, \ 5, \ which rest", font_size=24, color=WHITE), label(r"pink: \ degrees 2, \ 4, \ 6, \ 7, \ which lean", font_size=24, color=EAR)).arrange(RIGHT, buff=0.9).to_edge(UP, buff=0.5)
        jobs = VGroup(label(r"tonic: \ rest", font_size=30, color=TONIC_C), label(r"predominant: \ leave", font_size=30, color=PRE_C), label(r"dominant: \ pull back", font_size=30, color=DOM_C)).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.8)
        g = d["goes"]
        with self.voiceover(
            "Part 13 built a triad on every degree of the scale. In a key, those seven chords are not "
            "seven equal colours. Part 14 showed that degrees one, three and five are where melodies "
            "rest, and that two, four, six and seven lean toward them. <bookmark mark='a'/> So sort the "
            "chords by what they contain. The chord on one is all resting notes. <bookmark mark='b'/> The "
            f"chord on five holds seven and two, which both lean on one: seven rises to it "
            f"{say(100 * g['7']['p'])} times in a hundred. <bookmark mark='c'/> The chord on four holds "
            "four and six, which lean on three and five. Between them, four and five carry every "
            "leaning note of the scale."
        ) as vo:
            self.play(FadeIn(legend), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(cells[0], color=TONIC_C, scale_factor=1.1))
            vo.wait_until("b")
            self.play(Indicate(cells[4], color=DOM_C, scale_factor=1.1))
            vo.wait_until("c")
            self.play(Indicate(cells[3], color=PRE_C, scale_factor=1.1))
        with self.voiceover(
            "In 1893 Hugo Riemann gave these three roles names, and they are still used. The tonic is "
            "rest. <bookmark mark='a'/> The dominant, five, is the pull back to rest; the chord on seven "
            "does the same job. <bookmark mark='b'/> The predominant, four or two, is the step away that "
            "prepares the dominant. The other chords borrow a role: six and three stand in for the "
            "tonic. Seven chords, three jobs; and the usual order is rest, leave, pull, rest."
        ) as vo:
            self.play(FadeIn(jobs[0]))
            vo.wait_until("a")
            self.play(FadeIn(jobs[2]))
            vo.wait_until("b")
            self.play(FadeIn(jobs[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen_three(self):
        d = load("functions")
        c = clip("functions.three")
        pr = d["progressions"]
        kb = keys(41, 77, width=10.0, height=1.4).move_to(DOWN * 1.2)
        fn = {"I": "tonic", "IV": "predominant", "ii": "predominant", "V": "dominant", "V7": "dominant"}
        rows = VGroup(*[chips(pr[k]["names"], colors=[FUNC_C[fn[n]] for n in pr[k]["names"]], font_size=34, buff=0.7) for k in "abc"]).arrange(RIGHT, buff=1.3).move_to(UP * 1.6)
        tags = VGroup(*[label(t, font_size=22, color=GREY_B).next_to(rows[k], UP, buff=0.25) for k, t in enumerate((r"rest, \ leave, \ pull, \ rest", r"the same jobs, \ another chord", r"pull and leave exchanged"))])
        with self.voiceover(
            "Listen to the jobs. First: one, four, five, one. Then with the chord on two doing the "
            "work of four, and a seventh on the dominant. Then with the middle two exchanged: one, "
            "five, four, one."
        ):
            self.play(FadeIn(rows), FadeIn(tags), FadeIn(kb))
        allch = [ch for k in "abc" for ch in pr[k]["chords"]]
        allt = [t for k in "abc" for t in d["times"][k]]
        with self.listen(c) as snd:
            window(snd, r"three progressions", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, allch, allt, end=c.duration)
            for i, k in enumerate("abc"):
                for j in range(4):
                    end = d["times"][k][j + 1] if j < 3 else (d["starts"]["abc"[i + 1]] - 0.3 if i < 2 else c.duration)
                    pulse(snd, rows[i][j], d["times"][k][j], end, buff=0.08)
        kb.clear()
        with self.voiceover(
            "The first two say the same sentence in slightly different words. The third is not wrong; "
            "it is another grammar. Five falling to four is rare in Mozart, and everywhere in blues and "
            "rock. Which order sounds like home depends on which music you have counted. That will be "
            "the theme of the frontier chapter."
        ):
            self.play(Indicate(rows[2], color=WHITE, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def harmonize(self):
        d = load("more")["harmonize"]
        c = clip("functions.tune")
        r = roll([m - 72 for m in d["melody"]], d["beats"], width=10.5, height=1.6, lo=-1, hi=10, lines=(0,), phrase_ends=(7,), color=TUNE).move_to(UP * 2.1)
        fn = {"I": "tonic", "IV": "predominant", "V7": "dominant"}
        ch = VGroup(*[label(tex(n).replace("7", "$^7$"), font_size=32, color=FUNC_C[fn[n]]) for n in d["prog"]])
        on = np.concatenate([[0.0], np.cumsum(d["beats"])])
        for j, x in enumerate(ch):
            x.move_to([r.x(2 * j + 1.0), r.get_bottom()[1] - 0.4, 0])
        kb = keys(41, 84, width=10.0, height=1.2).move_to(DOWN * 1.3)
        mem = d["members"]
        note = label(rf"each note of the scale is in three of the seven chords: \ the first degree in {', '.join(mem['1'])}", font_size=24, color=GREY_B).next_to(kb, UP, buff=0.3)
        with self.voiceover(
            "Now the practical use. A melody note does not tell you its chord: each note of the scale "
            "belongs to three of the seven triads. The first degree is in the chords on one, on four "
            "and on six. So to put chords under a tune, you choose by job. Start at rest; leave before "
            "the end of the phrase; pull back with the dominant; land on the tonic. Here is the Tune's "
            "first phrase alone, and then two phrases with a chord to every two beats."
        ):
            self.play(FadeIn(r), FadeIn(kb), FadeIn(note))
            self.play(LaggedStart(*[FadeIn(x) for x in ch], lag_ratio=0.3), run_time=3.0)
        with self.listen(c) as snd:
            window(snd, r"alone; \ then with chords", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, r, d["alone_times"] + [999] * 7, hot=WHITE, base=TUNE)
            light_chords(snd, kb, d["chords"], d["chord_times"], end=c.duration, color=BLUE, melody=d["melody"][:7] + d["melody"], melody_times=d["alone_times"] + d["melody_times"], melody_color=GOLD)
            flash(snd, list(ch), d["chord_times"], hot=WHITE, base=GREY_B, fade=0.5, hold=0.7)
        kb.clear()
        for j, x in enumerate(ch):
            x.set_color(FUNC_C[fn[d["prog"][j]]])
        with self.voiceover(
            "Three chords, and the tune stands on a floor. Notice the end of each phrase. The first "
            "stops on the tonic chord with the fifth degree in the melody: at rest, but open. The second "
            "goes dominant, tonic, with the melody stepping down to one: closed. That is the difference "
            "between a comma and a full stop, and the next chapter gives it names."
        ):
            self.play(Indicate(ch[3], color=TONIC_C), Indicate(VGroup(ch[6], ch[7]), color=DOM_C))
        self.wait(0.4)
        self.clear_scene()
