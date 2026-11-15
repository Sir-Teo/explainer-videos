from __future__ import annotations

import numpy as np

from videos.music.music63.common import *  # noqa: F403


class Recordings(SoundScene):
    def construct(self):
        chapter(self, 4, r"Recordings, \ not songs", r"Does a fingerprint know the song, \ or only the recording?")
        self.fresh()
        self.speed()
        self.sampled()
        self.hum()
        self.meaning()

    # ------------------------------------------------------------------
    def fresh(self):
        d = load("falsematch")
        c = clip("unknown.one")
        top = d["fresh_top"]
        note = VGroup(label(r"the Tune, \ on Part 38's piano, \ at a tempo no earlier part used", font_size=20, color=WHITE),
                      label(rf"best match: \ {top[0]['track'].split('/')[1]} \ ({top[0]['votes']} votes); \ pure noise: \ at most {max(d['noise_top_votes'])}; \ a true excerpt: \ {min(d['true_votes'])} or more", font_size=18, color=EAR)).arrange(DOWN, buff=0.4).move_to(DOWN * 0.6)
        head = label(r"a new recording of an old song", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is the Tune, the song this whole series is built on, rendered afresh on the piano at a tempo no earlier part used. The library holds dozens of recordings of this song. Does the fingerprinter know it?"):
            self.play(FadeIn(head), FadeIn(note[0]))
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ new", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, note[0], 0.0, c.duration, rate=5.0, color=GREY_B, buff=0.15)
        with self.voiceover(
            f"Not as a recording. Its best guess, {top[0]['track'].split('/')[1].replace('tune.variation', 'Variation ')}, "
            f"collects {say(top[0]['votes'])} votes: more than chance, which never gave pure noise more than "
            f"{say(max(d['noise_top_votes']))}, because a few notes and chords sound alike in both; but a tenth of the "
            f"{say(min(d['true_votes']))} or more that a true excerpt collects. A fingerprint identifies a recording, its exact "
            "peaks at their exact times. A new performance of the same song, at another tempo, has other peaks entirely."
        ):
            self.play(FadeIn(note[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        items = [
            (r"fingerprints answer `which recording?': \ exact, \ fast, \ and blind to the song", WHITE),
            (r"`which song?' \ needs Part 62's cover matching: \ chroma, \ any key, \ any tempo; \ slower and less sure", WHITE),
            (r"`songs like this?' \ needs features of sound and style: \ the next chapters", WHITE),
            (r"Content ID can tell a re-upload from a cover: \ the rights in each are different \ (Part 60)", WHITE),
            (r"three questions, \ three kinds of similarity: \ the same signal, \ the same composition, \ the same taste", TUNE),
        ]
        rows_scene(self, r"three kinds of sameness", items,
                   "This is a feature, not a flaw. <bookmark mark='b'/> Fingerprints answer which recording: exactly, fast, and "
                   "blind to the song. <bookmark mark='c'/> Which song needs Part 62's cover matching, by chroma in any key and at "
                   "any tempo: slower, and less sure. <bookmark mark='d'/> Songs like this one needs features of sound and style, the "
                   "subject of the next chapters. <bookmark mark='e'/> And the difference matters for money: a re-upload and a cover "
                   "carry different rights, as Part 60 explained. <bookmark mark='f'/> Three questions, three kinds of similarity: "
                   "the same signal, the same composition, the same taste.", marks="bcdef")

    # ------------------------------------------------------------------
    def speed(self):
        d = load("speed")
        c = clip("speed.two")
        card = listen_card(r"The same five seconds, \ as stored, \ then played 4\% fast. \ Will the fingerprint still name it?", width=9.0)
        with self.voiceover("Your turn. The same five seconds of a Variation, first as the library stores it, then played four per cent fast, as a radio station sometimes does. Will the fingerprint still name it?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"as stored", r"4\% fast"], width=3.2, height=0.9, buff=1.2, size=20).move_to(UP * 0.8)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"4\% fast", kind="physical model", detail=r"a Variation from Part 5", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["stored"], st["fast"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["fast"], c.duration, buff=0.08)
        self.clear_scene()
        pct = np.array(d["percent"])
        rates = np.array(d["rates"])
        ax = frame_axes(width=8.0, height=2.8, xlo=0, xhi=8.4, ylo=0, yhi=1, center=DOWN * 0.7 + LEFT * 0.8)
        cv = curve(pct, rates, ax.to, color=EAR, width=3)
        dots = VGroup(*[Dot(ax.to(x, y), radius=0.06, color=EAR) for x, y in zip(pct, rates)])
        ticks = VGroup(*[label(f"{x:g}\\%", font_size=14, color=GREY_A).move_to(ax.to(x, 0) + DOWN * 0.25) for x in pct])
        yl = label(rf"share of {d['n']} queries named", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        res = label(rf"4\% fast: \ {d['votes_fast']} votes, \ for the wrong clip; \ as stored: \ {d['votes_stored']}", font_size=19, color=EAR).to_edge(UP, buff=0.5)
        why = label(r"every peak moves up in frequency and closer in time: \ the hashes change, \ though the tune does not", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"It does not. Played as stored, the right clip gets {say(d['votes_stored'])} votes; four per cent fast, the best "
            f"any clip gets is {say(d['votes_fast'])}, and it is the wrong one. <bookmark mark='a'/> Across all the Variations: "
            f"half a per cent fast still works {say(round(100 * rates[1]))} per cent of the time, one per cent "
            f"{say(round(100 * rates[2]))}, two per cent {say(round(100 * rates[3]))}. Every peak moves up in frequency and closer "
            "in time, so the hashes change, though no listener would call it a different song. Fingerprints that survive "
            "speed changes exist, built on ratios of frequencies and of times, at some cost in speed."
        ) as vo:
            self.play(FadeIn(res))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(ticks), FadeIn(yl), Create(cv), FadeIn(dots), FadeIn(why), run_time=1.5)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sampled(self):
        d = load("sampled")
        c = clip("sampled.two")
        boxes = choice_boxes([r"the sample alone", r"the sample, \ 12 dB under another track"], width=4.2, height=0.9, buff=0.8, size=18).move_to(UP * 1.2)
        head = label(r"finding a sample", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("A harder search, the one a rights service must make: find a recording used as a sample inside another track. Hear five seconds of Variation 3, then the same five seconds twelve decibels under Variation 10."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a sample, \ buried", kind="physical model", detail=r"Variations 3 and 10", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["sample"], st["track"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["track"], c.duration, buff=0.08)
        lv = np.array(d["levels"], float)
        r = np.array(d["sample_found"])
        ax = frame_axes(width=6.5, height=2.2, xlo=-19, xhi=1, ylo=0, yhi=1, center=DOWN * 1.6 + LEFT * 0.6)
        cv = curve(lv, r, ax.to, color=TUNE, width=3)
        dots = VGroup(*[Dot(ax.to(x, y), radius=0.06, color=TUNE) for x, y in zip(lv, r)])
        ticks = VGroup(*[label(f"{int(x)} dB", font_size=13, color=GREY_A).move_to(ax.to(x, 0) + DOWN * 0.22) for x in lv])
        yl = label(rf"share of {d['n']} samples found", font_size=13, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        top = d["demo"][0]
        with self.voiceover(
            f"The search names Variation 10, with {say(top['votes'])} votes, and its copies elsewhere in the series; Variation 3 "
            "is not among the top five. <bookmark mark='a'/> Across all the Variations, a sample level with the track on top is "
            f"found {say(round(100 * r[0]))} per cent of the time; six decibels down, {say(round(100 * r[1]))}; twelve down, "
            f"{say(round(100 * r[2]))}; eighteen down, {say(round(100 * r[3]))}. The louder track's peaks bury the sample's. "
            "Quiet samples are the hard case for anyone who polices them."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(ticks), FadeIn(yl), Create(cv), FadeIn(dots), run_time=1.4)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hum(self):
        d = load("hum")
        c = clip("hum.one")
        head = label(r"search by melody", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        lead = label(r"the Tune's opening, \ sung slower, \ three semitones up, \ a little out of tune", font_size=19, color=WHITE).move_to(UP * 1.6)
        with self.voiceover("To find the song rather than the recording, search by melody. Here is a hummed query: the Tune's opening, sung slower, three semitones higher, and a little out of tune."):
            self.play(FadeIn(head), FadeIn(lead))
        box = choice_boxes([r"the query"], width=3.0, height=0.8, size=18).move_to(UP * 0.6)
        self.play(FadeIn(box))
        with self.listen(c) as snd:
            window(snd, r"a hummed query", kind="synthesized", detail=r"the Tune, \ sung", corner=DL, tag_corner=DR)
            pulse(snd, box, 0.0, c.duration, buff=0.06)
        self.clear_scene()
        q = np.array(d["contour"])
        r = np.array(d["tune_ref"])
        q = q - np.median(q)
        r = r - np.median(r)
        ax1 = frame_axes(width=5.2, height=2.2, xlo=0, xhi=len(q), ylo=-8, yhi=8, center=LEFT * 3.4 + UP * 0.9)
        ax2 = frame_axes(width=5.2, height=2.2, xlo=0, xhi=len(r), ylo=-8, yhi=8, center=RIGHT * 3.0 + UP * 0.9)
        c1 = curve(np.arange(len(q)), q, ax1.to, color=EAR, width=2.5)
        c2 = curve(np.arange(len(r)), r, ax2.to, color=TUNE, width=2.5)
        l1 = label(r"the query's pitch, \ by Part 61's YIN \ (semitones from its median)", font_size=14, color=EAR).next_to(ax1, UP, buff=0.12)
        l2 = label(r"the Tune as written, \ at its own tempo", font_size=14, color=TUNE).next_to(ax2, UP, buff=0.12)
        ranked = d["ranked"]
        dist = d["dist"]
        tab = VGroup(*[label(rf"{i + 1}. \ {k}: \ {dist[k]:.2f}", font_size=17, color=TUNE if k == "the Tune" else GREY_A) for i, k in enumerate(ranked[:4])]).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(DOWN * 1.9 + LEFT * 2.5)
        fp = d["fingerprint"][0]
        side = label(rf"the fingerprint's best: \ {fp['votes']} votes, \ for Variation {fp['track'].split('variation')[-1]}: \ no match", font_size=16, color=EAR).move_to(DOWN * 1.9 + RIGHT * 3.0)
        with self.voiceover(
            f"The fingerprint finds nothing: its best guess collects {say(fp['votes'])} votes, where a true match collects "
            "hundreds. <bookmark mark='a'/> A melody search instead tracks the query's pitch, with Part 61's YIN, and centres "
            "it so that the key does not matter. <bookmark mark='b'/> Then it compares that contour with each melody it knows, "
            f"by time warping, which forgives the tempo. <bookmark mark='c'/> Among {say(d['n'])} melodies, the Tune comes first, "
            f"with a warping cost of {say(dist['the Tune'], 2)}, half the runner-up's {say(dist[ranked[1]], 2)}. Services that "
            "search by humming rest on the same idea, with millions of melodies and faster indexes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(ax1), Create(c1), FadeIn(l1), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(ax2), Create(c2), FadeIn(l2), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(side))
        self.wait(0.6)
        self.clear_scene()
