from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403
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
        c = clip("tune.variation32")
        head = VGroup(label(r"Variation 32", font_size=48, color=TUNE), label(r"the Tune, \ by the shortest paths", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)

        def row(key, col):
            nm = VGroup(*[label(tex_triad(n), font_size=28, color=col) for n in d[key]["chain"]]).arrange(RIGHT, buff=0.55)
            sz = VGroup(*[label(f"{s:.0f}", font_size=17, color=GREY_A).move_to((nm[i].get_center() + nm[i + 1].get_center()) / 2 + DOWN * 0.45)
                          for i, s in enumerate(d[key]["sizes"])])
            return VGroup(nm, sz)
        r1 = row("plain", TUNE)
        r2 = row("far", EAR)
        l1 = label(rf"chords of C major: \ {d['plain']['total']:.0f} semitones", font_size=20, color=TUNE)
        l2 = label(rf"chords outside it: \ {d['far']['total']:.0f} semitones", font_size=20, color=EAR)
        g = VGroup(VGroup(l1, r1).arrange(DOWN, buff=0.25), VGroup(l2, r2).arrange(DOWN, buff=0.25)).arrange(DOWN, buff=0.7).move_to(DOWN * 0.3)
        with self.voiceover(
            f"Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> This time a program harmonizes the Tune's first two phrases twice, one triad every two beats, each containing the melody note sampled at that two-beat boundary, with C major supplied at both endpoints, minimizing total pitch-class voice-leading cost. First it may use only the chords of C major; it finds C, C, A minor, C, F, A minor, D minor, C. The second search permits chromatic triads and C major but excludes the other diatonic triads; it finds A major, F minor and G minor, and the whole path costs only {say(round(d['far']['total'] - d['plain']['total']))} semitones more. Distant chords, reached by short steps."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"Variation 32", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            u = d["unit"]
            for key, r in (("plain", r1), ("far", r2)):
                for i in range(len(r[0])):
                    pulse(snd, r[0][i], d["starts"][key] + 2 * i * u, d["starts"][key] + (2 * i + 2) * u - 0.05, buff=0.08)
        self.play(FadeOut(g))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirty-two of the ledger: {say(v['seconds'])} seconds; the measurement is the rerouted path and the two "
            "totals of voice leading."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        b = load("bach")
        card = objectives_card([
            r"a chord is a point; \ folding by octave and permutation curves the space",
            r"two notes: \ a M\"obius strip; \ three: \ a triangle in a twisted prism",
            r"voice-leading size: \ the smallest total of semitones, \ in any norm",
            r"nearly even chords reach their transpositions by one or two semitones",
            r"OPTIC names the objects; \ Fourier magnitudes name their qualities",
            rf"Bach's upper voices take the shortest path {100 * b['upper']['minimal_share']:.0f} times in 100",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A chord is a point, and folding by octave and permutation curves the space. <bookmark mark='a'/> Two-note chords live on a Möbius strip, three-note chords in a twisted prism around a triangle. <bookmark mark='b'/> A voice leading has a size, the smallest total of semitones. <bookmark mark='c'/> Nearly even chords, the triads, the seventh chords and the diatonic scale, reach their own transpositions by one or two semitones. <bookmark mark='d'/> Five symmetries name music theory's objects, and Fourier magnitudes their qualities. <bookmark mark='e'/> And in this corpus and beat-sampling scheme, Bach's upper voices match the pitch-class minimum about two times in three."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Find the smallest voice leading from C major to A$\flat$ minor, \ and from C$^7$ to F$\sharp^7$.",
            r"Prove that the excess of any voice leading over the minimal one between the same chords is even.",
            r"\textbf{Ear.} \ The lab plays pairs of progressions; \ one in each pair is the minimal voice leading. \ Find it.",
            r"\textbf{Build.} \ Draw the M\"obius strip of two-note chords in 19-note equal temperament, \ and place its thirds.",
            r"$\bigstar$ \ Does voice-leading size predict how smooth a progression sounds?",
        ], font_size=22)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"the mathematics of scales and rhythms", [33]),
            (r"jazz voicings and their voice leading", [39]),
            (r"orchestration and spacing", [41]),
            (r"chords recognized and generated by machine", [62, 65]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in the mathematics of scales and rhythms. In jazz voicings. In orchestration, "
            "where spacing and register return. And in machines that recognize and generate chords."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"arrangers", r"voice chords so each part moves by a step"),
            (r"jazz pianists", r"keep guide tones and move them by semitones"),
            (r"film composers", r"slide between distant chords by small moves"),
            (r"software", r"voice-leads chord symbols automatically, \ by shortest paths"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Arrangers voice chords so every part moves by a step. Jazz pianists keep the guide tones and "
            "move them by semitones. Film composers slide between distant chords by small moves. And notation and "
            "accompaniment software voices chord symbols automatically, by shortest paths."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"D. Tymoczko, \ \textit{A Geometry of Music} \ (2011)",
             r"E. Amiot, \ \textit{Music Through Fourier Space} \ (2016)",
             r"D. Huron, \ \textit{Voice Leading: \ The Science behind a Musical Art} \ (2016)",
             r"R. Cohn, \ \textit{Audacious Euphony} \ (2012)"],
            [r"D. Tymoczko, \ `The geometry of musical chords', \ \textit{Science} \ (2006)",
             r"C. Callender, \ I. Quinn, \ D. Tymoczko, \ `Generalized voice-leading spaces', \ \textit{Science} \ (2008)",
             r"I. Quinn, \ `General equal-tempered harmony', \ \textit{Perspectives of New Music} \ (2006--07)",
             r"D. Lewin, \ `Re: \ Intervallic relations between two collections of notes', \ \textit{JMT} \ (1959)"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what if the same mathematics described rhythms, \ and scales, \ at once?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act V: \ after tonality", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"Nearly even sets of notes made the scales.", font_size=24, color=WHITE).move_to(UP * 1.7)
        lead.scale_to_fit_width(min(lead.width, 12.5))
        nxt = VGroup(label(r"Part 33", font_size=32, color=GREY_B), label(r"The Mathematics of Rhythm and Scale", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Nearly even sets of notes made the scales. <bookmark mark='a'/> What if the same mathematics describes rhythms "
            "too, nearly even sets of beats? <bookmark mark='b'/> Next time. Part 33: The Mathematics of Rhythm and Scale."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
