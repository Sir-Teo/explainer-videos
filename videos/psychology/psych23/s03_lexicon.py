from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


class Lexicon(VoiceoverScene):
    def construct(self):
        self.card()
        self.frequency()
        self.cohort()

    def card(self):
        card = chapter_card(2, r"The mental lexicon", r"How fast can you find a word among forty thousand?",
                            lit={1971: r"Meyer \& Schvaneveldt", 1978: r"Marslen-Wilson \& Welsh",
                                 2021: r"Futrell et al."},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter two. The mental lexicon."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def frequency(self):
        d = load("lexicon")
        s = load("surprisal")
        head = heading(r"Common words are read faster")
        A = axes([0.5, 5.6], [300, 400], x_length=4.6, y_length=3.2, xticks=[1, 2, 3, 4, 5], yticks=[300, 350, 400],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"frequency in the novels", ylabel=r"reading time, \ ms", center=[-4.0, 0.1, 0], font_size=16)
        B = axes([1, 12], [300, 400], x_length=4.0, y_length=3.2, xticks=[2, 4, 6, 8, 10, 12], yticks=[300, 350, 400],
                 yfmt=lambda v: f"{v:.0f}", xlabel=r"length, \ letters", ylabel=r"", center=[1.0, 0.1, 0],
                 font_size=16)
        f = VGroup(curve(A.ax, d["freq_mid"], d["freq_rt"], WORD, 3), scatter(A.ax, d["freq_mid"], d["freq_rt"], WORD,
                                                                                0.06, 1))
        ok = ~np.isnan(d["len_rt"])
        L = VGroup(curve(B.ax, d["len"][ok], d["len_rt"][ok], SOUND, 3),
                   scatter(B.ax, d["len"][ok], d["len_rt"][ok], SOUND, 0.06, 1))
        coef = dict(zip([str(n) for n in s["names"]], s["coef"]))
        rows = rows_of([
            (rf"Natural Stories: \ {num(s['n_words'])} words of ten stories, \ each read one word at a time by "
             rf"about {s['readers_median']:.0f} people", WHITE),
            (rf"each tenfold rise in frequency saves about {-coef['logfreq']:.0f} ms, \ with length held fixed", WORD),
            (rf"each extra letter costs about {coef['length']:.1f} ms", SOUND),
            (r"in lexical decision the frequency effect is far larger: \ looking a word up is the slow part of "
             r"reading it", MODEL),
        ], 3.6, 21, 0.33).move_to([5.1, 0.0, 0])
        ptag = psyche_tag(r"open data: \ Natural Stories \ (Futrell et al.); \ \texttt{language.rt\_regression}")
        with self.voiceover(
            "Somewhere you store tens of thousands of words, and you find each one in a fraction of a second. "
            "<bookmark mark='a'/> Here is one measure of how. The Natural Stories corpus is ten short stories, ten "
            "thousand words, each shown one word at a time to readers who press a key for the next. Each word was "
            f"read by about {s['readers_median']:.0f} people. <bookmark mark='b'/> Common words are read faster. "
            f"Holding length fixed, each tenfold rise in a word's frequency saves about {-coef['logfreq']:.0f} "
            "milliseconds. <bookmark mark='c'/> Longer words take longer, a few milliseconds a letter. "
            "<bookmark mark='d'/> In lexical decision, where people judge whether a string is a word, the frequency "
            "effect is much larger. Looking a word up is a large part of reading it, and frequent words are found "
            "faster, as if the lexicon were sorted by use."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(f), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(L), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def cohort(self):
        d = load("lexicon")
        head = heading(r"Spoken words: \ the cohort")
        word = "trespass"
        sizes = d["cohort_" + word]
        assert sizes[0] > 1000 and sizes[2] == 54 and sizes[4] == 2, sizes  # the narration reads these out
        A = axes([0.5, len(word) + 0.5], [0, 4], x_length=6.0, y_length=3.2, xticks=[], yticks=[0, 1, 2, 3, 4],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", ylabel=r"words still possible", center=[-2.9, 0.2, 0],
                 font_size=16)
        bs = VGroup(*[bars(A.ax, [k + 1], [np.log10(v)], SOUND if v > 2 else MODEL, 0.6) for k, v in enumerate(sizes)])
        letters = VGroup(*[label(rf"\emph{{{word[:k + 1]}}}", font_size=17, color=WORD).next_to(A.ax.c2p(k + 1, 0),
                                                                                             DOWN, buff=0.15)
                           for k in range(len(word))])
        for k, lab_ in enumerate(letters):
            lab_.shift(DOWN * 0.22 * (k % 2))
        nums = VGroup(*[label(f"{v:,}", font_size=16).next_to(A.ax.c2p(k + 1, np.log10(v)), UP, buff=0.06)
                        for k, v in enumerate(sizes)])
        rows = rows_of([
            (r"Marslen-Wilson, \ 1978: \ as a word arrives, \ every word that fits its start is activated at once: "
             r"\ the cohort", WHITE),
            (rf"letters standing in for sounds, \ among {num(d['lexicon_size'])} words: \ \emph{{trespass}} is "
             rf"down to its own forms by its fifth letter", SOUND),
            (r"people often recognize a word before it ends, \ around this \emph{uniqueness point}", MODEL),
            (r"TRACE \ (McClelland \& Elman, \ 1986) \ does it with competing units and feedback, \ as the next "
             r"chapter's model does for print", STAT),
        ], 5.2, 22, 0.33).move_to([3.9, 0.1, 0])
        ptag = psyche_tag(r"\texttt{language.cohort} \ (letters as a stand-in for speech sounds)")
        with self.voiceover(
            "Speech brings a different problem: a spoken word arrives over time, one sound after another. "
            "<bookmark mark='a'/> William Marslen-Wilson proposed in 1978 that as a word begins, every word that "
            "fits its start is activated at once: the cohort. Each new sound throws out the words that no longer "
            "fit. <bookmark mark='b'/> Here letters stand in for sounds, in a lexicon of thirty thousand words. After "
            "t, more than a thousand candidates. After t r e, fifty-four. By the fifth letter only trespass and its "
            "own forms are left. <bookmark mark='c'/> People often recognize a spoken word before it has finished, "
            "around this uniqueness point. <bookmark mark='d'/> The TRACE model does this with competing units and "
            "feedback between levels, the same idea as the model of reading in the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(l_), FadeIn(n_))
                                    for b, l_, n_ in zip(bs, letters, nums)], lag_ratio=0.3), FadeIn(rows[1]),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
