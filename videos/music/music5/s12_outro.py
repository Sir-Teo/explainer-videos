from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune")
        v = load("variation")
        s = load("stretched")
        c = clip("tune.variation5")
        wide = s["wide"]
        head = VGroup(label(r"Variation 5", font_size=48, color=TUNE),
                      label(r"a tune for a bent tone", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.4)
        base, unit = LEFT * 5.6 + UP * 0.1, 8.4 / 12.0
        axis = Line(base, base + RIGHT * 8.8, color=GREY_C, stroke_width=2)
        mult_bent = np.arange(1, 8) ** np.log2(wide)
        mult_plain = np.arange(1, 8).astype(float)
        fifth = d["fifth"]

        def lines(mult, ratio, col):
            return VGroup(*[Line(base + RIGHT * unit * m * ratio, base + RIGHT * unit * m * ratio + UP * 1.5 * 0.88 ** k, color=col, stroke_width=5)
                            for k, m in enumerate(mult) if m * ratio < 12.4])

        low = lines(mult_bent, 1.0, AIR)
        up = lines(mult_bent, fifth, TUNE)
        low_p = lines(mult_plain, 1.0, AIR)
        up_p = lines(mult_plain, fifth, TUNE)
        al = label(r"the partials of the two voices", font_size=22, color=GREY_B).next_to(axis, DOWN, buff=0.15)
        meter = Meter(width=0.55, height=2.2, color=ROUGH).move_to(RIGHT * 4.9 + UP * 0.9)
        ml = label(r"roughness", font_size=22, color=ROUGH).next_to(meter, DOWN, buff=0.15)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built a way of "
            "moving consonance, so here is the Tune in the bent tone, on a scale that has been stretched to "
            "match it. <bookmark mark='a'/> Two phrases alone. Then two phrases with a second voice above the "
            f"melody, at the bent tone's own fifth, which is {say(d['fifth_cents'])} cents: half a semitone "
            "wider than a real one. For this timbre it is smooth. <bookmark mark='b'/> Then, for one phrase, "
            "exactly the same notes with ordinary partials. And then the bent tone again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(axis), FadeIn(al), FadeIn(low), FadeIn(meter), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(up))
        up.set_stroke(opacity=0)
        self.add(low_p, up_p)
        low_p.set_stroke(opacity=0)
        up_p.set_stroke(opacity=0)
        top = d["rough_plain"] * 1.25
        words, phrase, k_in = None, -1, 0
        mode = label(r"the bent tone, \ alone", font_size=30, color=AIR).move_to(DOWN * 1.35)
        self.add(mode)
        captions = {2: (r"the bent tone, \ in its own fifths", TUNE), 4: (r"the same notes, \ with ordinary partials", ROUGH), 5: (r"the bent tone again", TUNE)}
        with self.listen(c) as snd:
            window(snd, r"Variation 5", kind="synthesized", detail=r"stretched partials; \ ordinary ones in phrase 5", tag_corner=DR)
            for k, nt in enumerate(c.notes):
                snd.wait_until(f"n{k}")
                if nt["phrase"] != phrase:
                    phrase, k_in = nt["phrase"], 0
                    ns = [m["name"] for m in c.notes if m["phrase"] == phrase]
                    new = VGroup(*[label(t, font_size=40, color=GREY_D) for t in ns]).arrange(RIGHT, buff=0.7).move_to(DOWN * 2.35)
                    if words is not None:
                        self.remove(words)
                    words = new
                    self.add(words)
                    if phrase in captions:
                        self.remove(mode)
                        mode = label(captions[phrase][0], font_size=30, color=captions[phrase][1]).move_to(DOWN * 1.35)
                        self.add(mode)
                kind = nt["kind"]
                low.set_stroke(opacity=0 if kind == "plain" else 1)
                up.set_stroke(opacity=1 if kind == "bent" else 0)
                low_p.set_stroke(opacity=1 if kind == "plain" else 0)
                up_p.set_stroke(opacity=1 if kind == "plain" else 0)
                r = {"alone": 0.02, "bent": d["rough_bent"] / top, "plain": d["rough_plain"] / top}[kind]
                t0 = nt["t"]
                snd.drive(meter, lambda m, t, r=r, t0=t0: m.set_level(r * (0.85 + 0.15 * np.cos(9 * (t - t0)))))
                words[k_in].set_color(captions.get(phrase, (None, AIR))[1] if phrase >= 2 else AIR)
                k_in += 1
        rows = rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}]
        led = variations_ledger(rows, highlight=(len(rows) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row five of the ledger. {say(v['seconds'])} seconds. In Monochord's sum, the fifth phrase, with "
            f"ordinary partials, is {say(d['times'], 1)} times as rough as the same notes in the bent tone. The "
            "intervals did not change. The partials did."
        ):
            self.play(FadeOut(words), FadeOut(mode), FadeOut(al), FadeOut(ml), FadeOut(meter), FadeOut(low_p), FadeOut(up_p),
                      VGroup(axis, low, up).animate.scale(0.5).move_to(UP * 2.0), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"theories of number rank the intervals well, \ and fail on a fifth five cents wide",
            r"two close tones beat at the difference of their frequencies; \ fast beats are roughness",
            r"roughness is greatest a quarter of a band apart, \ and for pure tones knows no ratios",
            r"add it over all pairs of partials: \ the valleys are the just ratios, \ and they move with the timbre",
            r"partials that fit one series fuse into one pitch: \ that tells major from minor",
            r"the preference itself is learned: \ membrane, \ nerve, \ and listener",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The theories of number put the intervals in nearly the right order, and are "
            "defeated by a fifth that is five cents wide. <bookmark mark='a'/> Two close tones beat at the "
            "difference of their frequencies, and beats too fast to follow are heard as roughness. "
            "<bookmark mark='b'/> Roughness is greatest a quarter of a critical band apart, and for pure tones "
            "it knows nothing about ratios. <bookmark mark='c'/> Add it up over all the partials of two notes, "
            "and the valleys of the curve are the just ratios. Change the partials, and the valleys move. "
            "<bookmark mark='d'/> Partials that fit one harmonic series fuse into a single pitch, and that is "
            "what tells a major chord from a minor one. <bookmark mark='e'/> And the preference for consonance "
            "is learned. Three layers: the membrane, the nerve, and the listener."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, r in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Compute Euler's number for the minor seventh 16 : 9 and for the `harmonic seventh' 7 : 4. \ Which does his formula prefer? \ "
            r"Which sits in a valley of this part's roughness curve?",
            r"Two notes have harmonic partials and stand in the ratio $p : q$ in lowest terms. \ Show that partial $m$ of the upper coincides with "
            r"partial $n$ of the lower exactly when $m$ is a multiple of $q$ and $n$ the same multiple of $p$. \ What fraction of the upper note's partials coincide?",
            r"\textbf{Ear.} \ The lab plays one interval twice: \ once in an ordinary tone, \ once in a tone whose partials were stretched. \ "
            r"Say which version is smoother, \ and so whether the interval is an octave or a stretched octave.",
            r"\textbf{Build.} \ Compute the dissonance curve of a tone with partials at 1, \ 2.76, \ 5.40 and 8.93 (a bar struck at its middle), \ "
            r"and list its valleys. \ Build a five-note scale from them and play the Tune on it.",
            r"$\bigstar$ \ Fit weights for roughness, \ harmonicity and familiarity to published ratings of the twelve intervals, \ "
            r"and predict the rating of every triad. \ Where is the fit worst, \ and what would a fourth term have to measure?",
        ], font_size=23)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, "
            "marked with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"beats, \ and valleys that can be a little off", [6]),
            (r"inharmonic partials and their scales", [7, 9, 36, 52]),
            (r"the fundamental bass; \ chords and inversions", [13, 18]),
            (r"consonance and dissonance in motion", [16, 17, 19]),
            (r"what is learned: \ expectation, \ and other musics", [34, 46, 47]),
            (r"roughness as a measure of sound", [41, 56]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? At once, in Part 6: every tuning system is a way of sharing out beats, "
            "and it only works because the valleys can be a little off. Inharmonic partials return with stiff "
            "strings, with bells, with the gamelan, and in synthesis. The fundamental bass becomes the theory of "
            "chords. The handling of dissonance, how it is prepared and where it must go, is the whole craft of "
            "counterpoint. And what is learned returns when we study expectation, and the musics of the world."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"piano tuners", r"count beats between partials, \ and stretch the octaves to suit each instrument's strings"),
            (r"orchestrators and arrangers", r"space chords wide in the bass, \ where the ear's bands are wide and close notes grind"),
            (r"synthesizer and bell designers", r"choose the partials and the scale together, \ so that the intervals played are valleys"),
            (r"mixing engineers", r"two instruments rough against each other are fighting for the same band: \ retune, \ or move one"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A piano tuner counts beats between partials for a living, and stretches each "
            "instrument's octaves to suit its strings. An arranger spaces chords wide in the bass, where the "
            "ear's bands are wide and close notes grind. A designer of bells or of synthesizer sounds chooses "
            "the partials and the scale together. And a mixing engineer knows that two parts which sound rough "
            "together are competing for the same bands of the ear."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"H. von Helmholtz, \ \textit{On the Sensations of Tone} \ (1863; tr.\ Ellis), \ part II",
             r"W. A. Sethares, \ \textit{Tuning, Timbre, Spectrum, Scale} \ (2nd ed., 2005)",
             r"D. Deutsch (ed.), \ \textit{The Psychology of Music} \ (3rd ed., 2013), \ ch.\ 4",
             r"J. Tenney, \ \textit{A History of `Consonance' and `Dissonance'} \ (1988)"],
            [r"L. Euler, \ \textit{Tentamen novae theoriae musicae} \ (1739)",
             r"R. Plomp and W. J. M. Levelt, \ ``Tonal consonance and critical bandwidth'', \ \textit{JASA} 38 (1965)",
             r"W. A. Sethares, \ ``Local consonance and the relationship between timbre and scale'', \ \textit{JASA} 94 (1993)",
             r"J. H. McDermott, A. J. Lehr and A. J. Oxenham, \ ``Individual differences reveal the basis of consonance'', \ \textit{Curr. Biol.} 20 (2010)",
             r"J. H. McDermott et al., \ ``Indifference to dissonance in native Amazonians'', \ \textit{Nature} 535 (2016)",
             r"P. M. C. Harrison and M. T. Pearce, \ ``Simultaneous consonance in music perception and composition'', \ \textit{Psychol. Rev.} 127 (2020)",
             r"R. Marjieh et al., \ ``Timbral effects on consonance'', \ \textit{Nature Commun.} 15 (2024)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        d = load("nextpart")
        c = clip("next.comma")
        circle = Circle(radius=1.7, color=GREY_C, stroke_width=2).move_to(LEFT * 3.4 + UP * 0.3)
        names = ("C", "G", "D", "A", "E", "B", r"F$\sharp$", r"C$\sharp$", r"G$\sharp$", r"D$\sharp$", r"A$\sharp$", r"E$\sharp$")
        pts = [circle.get_center() + 1.7 * np.array([np.sin(TAU * k / 12 * 1.0163), np.cos(TAU * k / 12 * 1.0163), 0]) for k in range(13)]
        dots = VGroup(*[Dot(p, radius=0.07, color=TUNE) for p in pts[:12]])
        labs = VGroup(*[label(n, font_size=22, color=GREY_A).move_to(circle.get_center() + 2.1 * (p - circle.get_center()) / 1.7) for n, p in zip(names, pts)])
        last = Dot(pts[12], radius=0.09, color=BAD)
        gap = label(r"twelve pure fifths \\ do not close the circle", font_size=24, color=BAD).next_to(circle, DOWN, buff=0.55)
        bx = boxes((r"C", r"the C twelve fifths on", r"both"), buff=0.3, width=2.3, height=1.1, font_size=22).move_to(RIGHT * 3.3 + UP * 1.3)
        with self.voiceover(
            "One last sound. Start on C and go up by a pure fifth, three to two. Then another, and another, "
            "folding back down by octaves whenever you go too high. <bookmark mark='a'/> After twelve fifths you "
            "have visited every note on the keyboard, and you are back at C. Here is the C you started from, the "
            "C you arrived at, and then the two together."
        ) as vo:
            self.play(Create(circle), FadeIn(dots[0]), FadeIn(labs[0]))
            self.play(LaggedStart(*[FadeIn(VGroup(a, b)) for a, b in zip(dots[1:], labs[1:])], lag_ratio=0.25), run_time=max(vo.until("a"), 2.0))
            self.play(FadeIn(last), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"C; \ the C twelve fifths later; \ both", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for ev, b, dur in zip(("c", "c_again", "both"), bx, (1.6, 1.6, 3.2)):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + dur)
        nxt = VGroup(label(r"Part 6", font_size=34, color=GREY_B), label(r"Tuning", font_size=54, color=TUNE)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.3 + DOWN * 2.2)
        facts = label(rf"they differ by {d['cents']:.1f} cents, \\ and beat {d['beat']:.1f} times a second", font_size=26, color=BAD).next_to(bx, DOWN, buff=0.35)
        with self.voiceover(
            f"They are not the same note. They differ by {say(d['cents'], 1)} cents, about a quarter of a "
            "semitone, and together they beat. <bookmark mark='a'/> Twelve pure fifths overshoot seven octaves. "
            "The circle does not close, and no arithmetic will ever make it close, because no power of three is "
            "a power of two. So the purest intervals this part has found cannot all be had at once. Every "
            "keyboard, every fretted instrument, every choir has to decide where to hide the error. "
            "<bookmark mark='b'/> That decision is Part 6: Tuning."
        ) as vo:
            self.play(FadeIn(facts))
            vo.wait_until("a")
            self.play(FadeIn(gap))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
