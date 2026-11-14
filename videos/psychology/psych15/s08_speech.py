from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


def formants(ax, f2_start, f2_end, color, f1=(300, 700), f2_steady=None):
    """A schematic spectrogram of a consonant-vowel syllable: F1 rising, F2 moving from its start to the vowel."""
    f2s = f2_steady if f2_steady is not None else f2_end
    g = VGroup(
        Line(ax.c2p(0, f1[0]), ax.c2p(40, f1[1]), color=color, stroke_width=10),
        Line(ax.c2p(40, f1[1]), ax.c2p(250, f1[1]), color=color, stroke_width=10),
        Line(ax.c2p(0, f2_start), ax.c2p(40, f2s), color=color, stroke_width=10),
        Line(ax.c2p(40, f2s), ax.c2p(250, f2s), color=color, stroke_width=10),
    )
    return g


class Speech(VoiceoverScene):
    def construct(self):
        self.card()
        self.invariance()
        self.categories()
        self.refined()
        self.mcgurk()
        self.people()

    def card(self):
        card = chapter_card(7, r"Speech", r"How does a stream of sound become words?",
                            lit={1957: r"Liberman", 1976: r"McGurk"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter seven. Speech."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def invariance(self):
        head = heading(r"No fixed sound for a consonant")
        A1 = axes([0, 250], [0, 3000], x_length=3.6, y_length=3.0, xticks=[0, 250], yticks=[0, 1000, 2000, 3000],
                  xlabel=r"ms", ylabel=r"Hz", center=[-4.4, 0.4, 0])
        A2 = axes([0, 250], [0, 3000], x_length=3.6, y_length=3.0, xticks=[0, 250], yticks=[0, 1000, 2000, 3000],
                  xlabel=r"ms", center=[-0.4, 0.4, 0])
        di = formants(A1.ax, 2200, 2600, SOUND, f1=(250, 300))
        du = formants(A2.ax, 1200, 700, PLACE, f1=(250, 300))
        l1 = label(r"``di''", font_size=30, color=SOUND).next_to(A1, UP, buff=0.1)
        l2 = label(r"``du''", font_size=30, color=PLACE).next_to(A2, UP, buff=0.1)
        rows = rows_of([
            (r"the bands are formants: \ the resonances of the mouth", WHITE),
            (r"the /d/ in ``di'' starts with a rising second formant; \ in ``du'', \ a falling one", PLACE),
            (r"yet both are heard as the same /d/: \ no acoustic invariant", BAD),
            (r"Liberman and colleagues, \ Haskins Laboratories, \ 1950s and 1960s", GREY_A),
        ], 4.4, 25, 0.32).move_to([4.6, 0.0, 0])
        keep_in_frame(rows)
        tag = note(r"schematic formant patterns, \ after the Haskins pattern playback").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Speech seems to arrive as a string of separate sounds, like letters. It doesn't. "
            "<bookmark mark='a'/> These are schematic spectrograms: time across, frequency up. The dark bands are "
            "formants, the resonances of the mouth and throat. <bookmark mark='b'/> In the syllable dee, the second "
            "formant starts with a rise. In doo, it starts with a fall. <bookmark mark='c'/> Yet both are heard as "
            "the same d. There is no fixed piece of sound that is the d: what you hear depends on the vowel that "
            "follows. <bookmark mark='d'/> Alvin Liberman and his colleagues at Haskins Laboratories found this in the "
            "nineteen-fifties, by painting spectrograms by hand and turning them back into sound with a machine they "
            "called the pattern playback."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A1), FadeIn(A2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(di), Create(du), FadeIn(l1), FadeIn(l2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def categories(self):
        d = load("speech")
        head = heading(r"Categorical perception")
        A = axes([1, 14], [0, 1], x_length=7.2, y_length=4.2, xticks=[1, 4, 7, 10, 13], yticks=[0, 0.5, 1],
                 xlabel=r"step along a continuum from /b/ to /d/", ylabel=r"proportion", center=[-2.4, -0.3, 0])
        ax = A.ax
        ident = curve(ax, d["steps"], d["ident"], SOUND, stroke_width=4)
        abx = curve(ax, d["abx_x"], d["abx"], PLACE, stroke_width=4)
        dots = scatter(ax, d["abx_x"], d["abx"], PLACE, radius=0.06)
        leg = legend([(SOUND, r"heard as /d/"), (PLACE, r"ABX correct, \ two steps apart")], font_size=20)
        leg.move_to(ax.c2p(4.2, 0.85))
        rows = rows_of([
            (r"a continuum of synthetic syllables, \ changing in equal acoustic steps", WHITE),
            (r"identification flips sharply at a boundary", SOUND),
            (r"discrimination predicted from labels alone: \ $\tfrac12[1 + (p_A - p_B)^2]$", PLACE),
            (r"near chance within a category, \ a peak at the boundary: \ found in 1957", TIMING),
        ], 4.6, 25, 0.32).move_to([4.6, -0.2, 0])
        keep_in_frame(rows)
        tag = VGroup(psyche_tag(r"computed: \ a logistic boundary and the label model"),
                     published_tag(archive.LIBERMAN_1957.cite, corner=DL))
        with self.voiceover(
            "Liberman's group then asked how people hear a continuum of such sounds. <bookmark mark='a'/> They made "
            "syllables that change in equal acoustic steps from b, through d, to g. <bookmark mark='b'/> Asked to name "
            "them, listeners don't drift gradually from b to d. They switch sharply at a boundary. "
            "<bookmark mark='c'/> Then the key test, from 1957: discrimination. In an ABX trial you hear two different "
            "steps and then one of them again, and say which it matched. If listeners could compare only their labels, "
            "the chance of being right would be a half plus a half times the square of the difference in labelling "
            "probabilities. That's this curve. <bookmark mark='d'/> And that's roughly what they found: near chance "
            "within a category, a peak at the boundary. People seemed to hear speech in categories, and to be deaf to "
            "differences inside them. It became known as categorical perception."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ident), FadeIn(leg[0]), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(abx), FadeIn(dots), FadeIn(leg[1]), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def refined(self):
        head = heading(r"The story, \ and the record")
        rows = rows_of([
            (r"the peak at the boundary is robust, \ and found in many languages", TIMING),
            (r"but ``deaf within a category'' is too strong", BAD),
            (r"2002: \ McMurray, \ Tanenhaus and Aslin track the eyes as people hear words", WHITE),
            (r"looks to the competing word rise smoothly as the sound nears the boundary: \ the detail is heard and used", SOUND),
            (r"categories shape what we report; \ they do not erase what we hear", PRIOR),
        ], 12.6, 29, 0.4).move_to([0, -0.1, 0])
        tag = published_tag(archive.MCMURRAY_2002.cite)
        with self.voiceover(
            "This is a case where the finding held and the story didn't. <bookmark mark='a'/> The peak in "
            "discrimination at the boundary is robust and has been found in many languages. "
            "<bookmark mark='b'/> But the idea that listeners are deaf to differences within a category is too "
            "strong. <bookmark mark='c'/> In 2002, Bob McMurray, Michael Tanenhaus and Richard Aslin tracked people's "
            "eyes as they heard words, with pictures of the possible words on a screen. <bookmark mark='d'/> As a "
            "sound moved closer to the category boundary, though still clearly inside the category, people looked "
            "more and more at the picture of the competing word. The fine detail was heard, and used. "
            "<bookmark mark='e'/> Categories shape what people report; they don't erase what people hear. The Ledger "
            "will record this one as story and record."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def mcgurk(self):
        d = load("speech")
        head = heading(r"The McGurk effect, \ as cue combination")
        axis = NumberLine(x_range=[-0.5, 2.5, 1], length=8.0, include_numbers=False, color=GREY_B).move_to([-1.6, 1.0, 0])
        labs = VGroup(*[label(t, font_size=30, color=WHITE).next_to(axis.n2p(k), DOWN, buff=0.25)
                        for k, t in enumerate((r"/b/", r"/d/", r"/g/"))])
        ends = VGroup(label(r"lips", font_size=20, color=GREY_B).next_to(labs[0], DOWN, buff=0.2),
                      label(r"back of the mouth", font_size=20, color=GREY_B).next_to(labs[2], DOWN, buff=0.2))
        where = VGroup(ends, label(r"place of articulation", font_size=20, color=GREY_B).next_to(ends, DOWN, buff=0.12))
        aud = Dot(axis.n2p(0), color=SOUND, radius=0.12)
        vis = Dot(axis.n2p(2), color=VISION, radius=0.12)
        al = label(r"the voice: \ ba", font_size=22, color=SOUND).next_to(aud, UP, buff=0.2)
        vl = label(r"the lips: \ ga", font_size=22, color=VISION).next_to(vis, UP, buff=0.2)
        fused = Dot(axis.n2p(1), color=TIMING, radius=0.14)
        fl = label(r"heard: \ da", font_size=24, color=TIMING).next_to(fused, UP, buff=0.2)
        t = d["typical"]
        rows = rows_of([
            (r"1976: \ McGurk and MacDonald dub a voice saying ba onto lips saying ga", WHITE),
            (r"98\% of adults reported da, \ or a blend: \ a sound in neither the voice nor the face", TIMING),
            (rf"Part 14's rule: \ weight each cue by its reliability; \ the estimate lands between, \ at /d/ ({pct(t[1])} in the model)", PRIOR),
            (r"with eyes closed, \ the voice says ba again", GREY_A),
        ], 12.6, 26, 0.24).to_edge(DOWN, buff=0.75)
        tag = VGroup(published_tag(archive.MCGURK_1976.cite, corner=DL),
                     psyche_tag(r"computed: \ \texttt{hearing.mcgurk}, \ equal reliabilities"))
        with self.voiceover(
            "Speech isn't only heard. <bookmark mark='a'/> In 1976, Harry McGurk and John MacDonald dubbed a voice "
            "saying ba onto a film of lips saying ga. <bookmark mark='b'/> Ninety-eight percent of the adults they "
            "tested reported hearing da, or a blend: a syllable in neither the voice nor the face. "
            "<bookmark mark='c'/> Line the consonants up by where the mouth closes, from the lips to the back of the "
            "mouth: b, d, g. The voice says the front; the lips say the back. Weight each by its reliability, Part "
            "14's rule, and the estimate lands between them, on d. In Psyche, with the two cues equally reliable, nearly "
            "nine trials in ten come out as d. <bookmark mark='d'/> And the effect is in the combining, not the ears: "
            "close your eyes and the same voice says ba again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(labs), FadeIn(where), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(aud), FadeIn(al), FadeIn(vis), FadeIn(vl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(TransformFromCopy(VGroup(aud, vis), fused), FadeIn(fl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def people(self):
        d = load("speech")
        head = heading(r"Not everyone hears it")
        edges = np.linspace(0, 1, 11)
        counts, _ = np.histogram(d["fused"], bins=edges)
        A = axes([0, 1], [0, max(counts) * 1.15], x_length=6.6, y_length=4.0, xticks=[0, 0.5, 1], xfmt=lambda v: pct(v),
                 yticks=[], xlabel=r"share of trials heard as da", ylabel=r"listeners", center=[-2.8, -0.3, 0])
        ax = A.ax
        bars = VGroup(*[Rectangle(width=ax.c2p(edges[k + 1], 0)[0] - ax.c2p(edges[k], 0)[0] - 0.04,
                                  height=ax.c2p(0, c)[1] - ax.c2p(0, 0)[1] + 1e-3, stroke_width=0, fill_color=TIMING,
                                  fill_opacity=0.8).move_to(ax.c2p((edges[k] + edges[k + 1]) / 2, c / 2))
                        for k, c in enumerate(counts)])
        rows = rows_of([
            (r"2015: \ Mallick, \ Magnotti and Beauchamp: \ from 0\% to 100\% across people, \ stable a year later", WHITE),
            (r"Psyche's simulated listeners differ in how far they trust the lips: \ the same spread", MODEL),
            (rf"the model also answers ga too often \ ({pct(d['mean_g'])}): \ real listeners rarely report the lips alone", BAD),
            (r"better models first ask whether the voice and face belong together: \ causal inference", PRIOR),
        ], 4.8, 25, 0.32).move_to([4.4, -0.2, 0])
        keep_in_frame(rows)
        tag = VGroup(simulated_tag(r"simulated: \ 300 listeners, \ 400 trials each"),
                     published_tag(archive.MALLICK_2015.cite, corner=DL))
        with self.voiceover(
            "The original ninety-eight percent turned out to be unusual. <bookmark mark='a'/> In 2015, Debshila "
            "Mallick, John Magnotti and Michael Beauchamp measured the illusion in many people with many recordings. "
            "Some people never experienced it; some experienced it on every trial; most were in between, and each "
            "person's rate was stable when they were tested again a year later. <bookmark mark='b'/> Psyche's "
            "simulated listeners differ in how much they trust lips relative to voices, and give the same kind of "
            "spread. <bookmark mark='c'/> But the simple model has a flaw worth seeing: it answers ga, what the lips "
            "alone said, far too often. Real listeners rarely do. <bookmark mark='d'/> Better models add a first step: "
            "deciding whether the voice and the face come from the same event at all, and combining only if they do. "
            "It's called causal inference, and it's where cue combination is going."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
