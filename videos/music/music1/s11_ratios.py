from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from videos.music.music1.common import (BAD, EAR, FREQ, GOOD, HIST, PART, RATIO, STR, TIME, TUNE, clip, load, say,
                                        window)

F_MAX = 1700.0
W = 11.6


def fx(hz: float) -> float:
    return -W / 2 + W * hz / F_MAX


class Combs(VGroup):
    """Two strings as two ladders of partials on one frequency axis: the lower string's below, the upper's above.
    Partials that meet are joined in green; ``.lower``, ``.upper``, ``.links``."""

    def __init__(self, row: dict, y: float = 0.0, **kw):
        super().__init__(**kw)
        axis = Line([-W / 2, y, 0], [W / 2, y, 0], color=GREY_D, stroke_width=1.5)
        self.lower, self.upper, self.links = VGroup(), VGroup(), VGroup()
        for n, f in enumerate(row["lower"], 1):
            t = Line([fx(f), y - 0.08, 0], [fx(f), y - 0.85, 0], color=STR, stroke_width=4)
            num = label(str(n), font_size=18, color=GREY_B).next_to(t, DOWN, buff=0.08)
            self.lower.add(VGroup(t, num))
        for m, f in enumerate(row["upper"], 1):
            t = Line([fx(f), y + 0.08, 0], [fx(f), y + 0.85, 0], color=TUNE, stroke_width=4)
            num = label(str(m), font_size=18, color=TUNE).next_to(t, UP, buff=0.08)
            self.upper.add(VGroup(t, num))
        for n, m in row["meets"]:
            if m <= len(row["upper"]):
                f = row["lower"][n - 1]
                self.links.add(Line([fx(f), y - 0.85, 0], [fx(f), y + 0.85, 0], color=GOOD, stroke_width=7))
        self.add(axis, self.lower, self.upper, self.links)
        self.axis = axis


class Ratios(SoundScene):
    def construct(self):
        self.card()
        self.octave()
        self.others()
        self.beats()
        self.answer()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"Why the ratios?", r"What do two strings share when their lengths are 2 to 1, or 3 to 2?",
                            lit=(-530, 1863), part=PART, links=("instrument", "ear"))
        with self.voiceover("Chapter ten. Why the ratios?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def play_pair(self, key: str, combs: Combs, text: str):
        """Lower string, upper string, both.  Each partial's line lights when its string is plucked and fades at
        the rate that partial dies away in the sound (the decay times measured in chapter nine)."""
        c = clip(f"coincide.{key}")
        row = load("coincide")["rows"][key]
        tab = load("overtones")["table"]
        slope, base = np.polyfit([r["hz"] ** 2 for r in tab], [6.91 / r["t60"] for r in tab], 1)
        t_hi, t_both = c.events["hi"], c.events["both"]

        def ringer(hz, onsets, silent=None):
            rate = base + slope * hz * hz

            def fn(m, t):
                if silent and silent[0] <= t < silent[1]:
                    level = None
                else:
                    on = [o for o in onsets if o <= t]
                    level = float(np.exp(-rate * (t - on[-1]))) if on else None
                line = m[0] if len(m.submobjects) else m
                line.set_stroke(opacity=0.12 if level is None else 0.25 + 0.75 * level)
                if len(m.submobjects):
                    m[1].set_opacity(0.3 if level is None else 1.0)
            return fn

        with self.listen(c) as snd:
            window(snd, text, detail=r"two strings, \ left and right", tag_corner=DR)
            for tick, hz in zip(combs.lower, row["lower"]):
                snd.drive(tick, ringer(hz, (0.0, t_both), silent=(t_hi, t_both)))
            for tick, hz in zip(combs.upper, row["upper"]):
                snd.drive(tick, ringer(hz, (t_hi, t_both), silent=(0.0, t_hi)))
            snd.wait_until("both")
            if len(combs.links):
                self.add(combs.links)
                for link, (n, _) in zip(combs.links, [nm for nm in row["meets"] if nm[1] <= len(row["upper"])]):
                    snd.drive(link, ringer(row["lower"][n - 1], (t_both,)))
        for part in (combs.lower, combs.upper):
            for tick in part:
                tick[0].set_stroke(opacity=1.0)
                tick[1].set_opacity(1.0)
        combs.links.set_stroke(opacity=1.0)

    # ------------------------------------------------------------------
    def octave(self):
        d = load("coincide")
        row = d["rows"]["octave"]
        combs = Combs(row, y=-0.4)
        combs.links.set_opacity(0)
        names = VGroup(label(r"the lower string's partials", font_size=26, color=STR).next_to(combs.lower, DOWN, buff=0.3),
                       label(r"the upper string's partials", font_size=26, color=TUNE).next_to(combs.upper, UP, buff=0.3))
        ax = label(r"frequency $\rightarrow$", font_size=22, color=GREY_B).next_to(combs.axis, RIGHT, buff=0.1).shift(DOWN * 1.5 + LEFT * 1.2)
        title = VGroup(MathTex(r"2 : 1", font_size=54, color=RATIO), label(r"the octave", font_size=34)).arrange(RIGHT, buff=0.4)
        title.to_edge(UP, buff=0.5)
        with self.voiceover(
            "Pythagoras had lengths and ratios. We have something he did not: we know that every string is a ladder "
            "of partials at one, two, three, four times its fundamental. <bookmark mark='a'/> So put two strings on "
            "one frequency axis. The lower string's ladder below the line, <bookmark mark='b'/> the upper string's "
            "above it. Start with the octave, where the upper string is twice as high."
        ) as vo:
            self.play(FadeIn(title), Create(combs.axis), FadeIn(ax), FadeIn(combs.lower[0]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in combs.lower[1:]], lag_ratio=0.25), run_time=4.4)
            vo.wait_until("a")
            self.play(FadeIn(names[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in combs.upper], lag_ratio=0.06), FadeIn(names[1]),
                      run_time=1.5)
        combs.links.set_opacity(1)
        self.remove(combs.links)
        self.play_pair("octave", combs, r"lower, \ upper, \ both")
        with self.voiceover(
            "Every partial of the upper string lands exactly on a partial of the lower one. "
            f"<bookmark mark='a'/> {say(row['count'])} of the lower string's first twelve are doubled, and the upper "
            "string brings nothing that was not already there. That is why an octave does not sound like two notes. "
            "It sounds like the same note, coloured differently, and it is why men and women singing a tune "
            "together an octave apart believe they are singing the same thing."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(combs.links, color=GOOD, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def others(self):
        d = load("coincide")
        table_head = VGroup(label(r"interval", font_size=24, color=GREY_B), label(r"ratio", font_size=24, color=GREY_B),
                            label(r"partials that meet, \ of the first 12", font_size=24, color=GREY_B))
        tx = [-5.2, -3.3, 0.2]
        for h, x in zip(table_head, tx):
            h.move_to([x, 3.4, 0])
        self.add(table_head)
        oc = d["rows"]["octave"]
        rows = VGroup()

        def trow(i, name, row):
            p, q = row["ratio"]
            r = VGroup(label(name, font_size=28), MathTex(rf"{p} : {q}", font_size=34, color=RATIO),
                       VGroup(*[Square(0.2, stroke_width=0, fill_color=GOOD, fill_opacity=0.95)
                                for _ in range(row["count"])]).arrange(RIGHT, buff=0.08)
                       if row["count"] else label(r"none", font_size=28, color=BAD))
            for cell, x in zip(r, tx):
                cell.move_to([x, 2.85 - 0.5 * i, 0])
            r[2].align_to([tx[2] - 1.7, 0, 0], LEFT)
            return r

        rows.add(trow(0, r"octave", oc))
        self.add(rows[0])
        spoken = {
            "fifth": ("Now the fifth, three to two. <bookmark mark='a'/> The upper string's second partial meets the "
                      "lower string's third. Its fourth meets the sixth. Every second one finds a partner."),
            "fourth": ("The fourth, four to three. <bookmark mark='a'/> Fewer meetings: the third partial of the "
                       "upper string with the fourth of the lower, and so on up."),
            "tritone": ("And for contrast, the interval the legend's weights really gave: half an octave, the "
                        "tritone. As a ratio it is something like forty-five to thirty-two. <bookmark mark='a'/> "
                        "Nothing meets."),
        }
        current = None
        for i, (key, name) in enumerate((("fifth", r"fifth"), ("fourth", r"fourth"), ("tritone", r"tritone")), 1):
            row = d["rows"][key]
            combs = Combs(row, y=-0.9)
            combs.links.set_opacity(0)
            with self.voiceover(spoken[key]) as vo:
                anims = [FadeIn(combs)]
                if current is not None:
                    anims.append(FadeOut(current))
                self.play(*anims, run_time=0.8)
                vo.wait_until("a")
            combs.links.set_opacity(1)
            self.remove(combs.links)
            self.play_pair(key, combs, r"lower, \ upper, \ both")
            r = trow(i, name, row)
            self.play(FadeIn(r), run_time=0.5)
            rows.add(r)
            current = combs
        miss = d["rows"]["tritone"]["near_misses"][0]
        a = current.lower[miss["n"] - 1]
        b = current.upper[miss["m"] - 1]
        ring_ = SurroundingRectangle(VGroup(a[0], b[0]), color=BAD, buff=0.1, stroke_width=3)
        tag = label(rf"{miss['cents']:.0f} cents apart", font_size=26, color=BAD).next_to(ring_, UP, buff=0.4)
        with self.voiceover(
            "Worse than nothing, in fact. <bookmark mark='a'/> Look at the seventh partial of the lower string and "
            f"the fifth of the upper. They miss each other by {say(miss['cents'])} cents: too far apart to be the "
            "same, too close to be heard as two. What happens then is the last thing we need."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ring_), FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beats(self):
        d = load("coincide")
        m = d["mistuned"]
        c = clip("coincide.beats")
        t_pair, t_bad, t_pure = (c.events[k] for k in ("pair", "mistuned", "pure"))
        dur = 3.0
        tt = np.linspace(0, dur, 400)
        env = np.abs(np.cos(np.pi * m["beat_hz"] * tt))
        band = Lens([-5.6, 1.5, 0], [5.6, 1.5, 0], amp=0.9, color=FREQ, opacity=0.5, shape=env, n=400)
        head = Line([-5.6, 0.5, 0], [-5.6, 2.5, 0], color=WHITE, stroke_width=2)
        cap = VGroup(label(rf"two pure tones, \ {m['hz'][0]:.1f} and {m['hz'][1]:.1f} hertz", font_size=26, color=FREQ),
                     label(rf"their sum swells and fades {m['beat_hz']:.1f} times a second", font_size=26, color=GREY_A)
                     ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)
        fifth = d["rows"]["fifth"]
        combs = Combs(fifth, y=-1.9).scale(0.9)
        combs.links.set_opacity(0)
        pair = VGroup(combs.lower[2][0], combs.upper[1][0])
        with self.voiceover(
            "Two tones that nearly agree do not sound like two tones. They sound like one tone that swells and "
            "fades. <bookmark mark='a'/> The two waves drift in and out of step, adding when they are together and "
            "cancelling when they are opposed. These are called beats, and the number of beats per second is simply "
            f"the difference between the two frequencies. <bookmark mark='b'/> Here is a fifth mistuned by "
            f"{say(m['cents'])} cents, a difference you would never notice in a single note. First just the two "
            "partials that ought to meet. Then both strings, mistuned. Then both strings, tuned true."
        ) as vo:
            self.play(FadeIn(cap[0]), FadeIn(band))
            vo.wait_until("a")
            self.play(FadeIn(cap[1]))
            vo.wait_until("b")
            self.play(FadeIn(combs))
        measured = d["band"]
        rate = measured["rate"]
        heard = {k: np.array(measured["env"][k]) for k in ("mistuned", "pure")}

        def band_of(key, color):
            return Lens([-5.6, 1.5, 0], [5.6, 1.5, 0], amp=1.15, color=color, opacity=0.5, shape=heard[key], n=400)

        def sweep(snd, t0, seconds):
            h = Line([-5.6, 0.5, 0], [-5.6, 2.5, 0], color=WHITE, stroke_width=2)
            snd.show(h)
            snd.drive(h, lambda mob, t: mob.set_x(-5.6 + 11.2 * float(np.clip((t - t0) / seconds, 0, 1))))
            return h

        cap2 = VGroup(label(rf"both strings: \ the band round {m['hz'][0]:.0f} hertz", font_size=26, color=FREQ),
                      label(r"filtered out of the sound you are hearing", font_size=26, color=GREY_A)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)
        with self.listen(c) as snd:
            window(snd, r"the pair, \ the mistuned fifth, \ the true fifth")
            head = sweep(snd, t_pair, dur)
            pair.set_color(BAD)
            snd.wait_until("mistuned")
            self.remove(head, band, *cap)
            bad = band_of("mistuned", BAD)
            self.add(bad, cap2)
            head = sweep(snd, t_bad, measured["seconds"])

            def throb(mob, t):
                i = int(np.clip((t - t_bad) * rate, 0, len(heard["mistuned"]) - 1))
                mob.set_stroke(opacity=1.0 if t >= t_pure else 0.2 + 0.8 * min(1.0, heard["mistuned"][i] / 0.57))

            snd.drive(pair, throb)
            verdict = label(r"mistuned: \ the third partial of one fights the second of the other", font_size=26,
                            color=BAD).next_to(combs, UP, buff=0.3)
            snd.show(verdict)
            snd.wait_until("pure")
            self.remove(verdict, head, bad)
            pair.set_color(GOOD)
            good = band_of("pure", GOOD)
            self.add(good)
            sweep(snd, t_pure, measured["seconds"])
            ok = label(r"in tune: \ the same frequency, \ no beats", font_size=26, color=GOOD).next_to(combs, UP, buff=0.3)
            self.add(ok)
        with self.voiceover(
            "That slow throb is how instruments are tuned. You do not judge the note; you listen for the beats and "
            "slow them down until they stop. <bookmark mark='a'/> And the picture was not a cartoon. It is the band "
            "where those two partials sit, filtered out of the sound you heard, and in the mistuned fifth it swells "
            f"{say(measured['beat_hz_measured'], 1)} times a second: the difference of the two frequencies."
        ) as vo:
            self.play(Indicate(pair, color=GOOD, scale_factor=1.2))
            vo.wait_until("a")
            self.play(FadeOut(good), FadeIn(bad), FadeOut(ok), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def answer(self):
        claim = theorem_card(
            r"A first answer to Pythagoras",
            r"When two harmonic sounds stand in a simple ratio, \ many of their partials coincide, \ and "
            r"coinciding partials do not beat. \ Away from the simple ratios, \ partials nearly coincide, \ and the "
            r"sound throbs or grates.", who=r"after Hermann von Helmholtz, \ 1863", color=GOOD, width=10.4, font_size=28,
            kind=r"Proposal").to_edge(UP, buff=0.45)
        gaps = VGroup(
            label(r"what it leaves out", font_size=28, color=GREY_B),
            label(r"It needs harmonic partials. \ Bells and drums do not have them. \quad $\rightarrow$ Parts 5 and 9",
                  font_size=26, color=WHITE),
            label(r"It says where the beats are, \ not why smoothness should please. \ The ear is missing. \quad "
                  r"$\rightarrow$ Part 4", font_size=26, color=WHITE),
            label(r"Not every culture prefers the smooth intervals. \quad $\rightarrow$ Part 5", font_size=26, color=WHITE),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 1.6)
        with self.voiceover(
            "So here is a first answer to the question we started with, and it is essentially the one Hermann von "
            "Helmholtz gave in 1863. <bookmark mark='a'/> Strings in simple ratios share partials. Shared partials "
            "cannot beat. Move away from the simple ratios and the partials only nearly agree, and the sound throbs "
            "or grates. The simpler the ratio, the more is shared."
        ) as vo:
            fifth = Combs(load("coincide")["rows"]["fifth"], y=-1.6)
            self.play(FadeIn(fifth), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(claim, shift=DOWN * 0.2))
        self.play(FadeOut(fifth), run_time=0.4)
        with self.voiceover(
            "It is a good answer, and it is not the whole one. <bookmark mark='a'/> It depends on the partials being "
            "harmonic, which is true of strings and pipes and false of bells and drums. <bookmark mark='b'/> It tells "
            "us where the beats are, but not why an ear should care: there is no listener in it yet. "
            "<bookmark mark='c'/> And not every culture agrees that smooth is better. Each of those gaps is a later "
            "part of this series. For now, one more debt. Our string so far has been ideal, and no real string is."
        ) as vo:
            self.play(FadeIn(gaps[0]))
            for mark, g in zip("abc", gaps[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(g, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
