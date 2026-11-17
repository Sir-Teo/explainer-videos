from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


class Surprisal(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.example()
        self.fit()

    def card(self):
        card = chapter_card(5, r"The cost of a surprising word", r"Is reading time a measure of probability?",
                            lit={2001: r"Hale", 2008: r"Levy", 2013: r"Smith \& Levy"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter five. The cost of a surprising word."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def derive(self):
        head = heading(r"Derivation: \ surprisal")
        eqs = VGroup(
            MathTex(r"\text{cost}(w_t) \;\propto\; -\log P(w_t \mid w_1, \dots, w_{t-1})", font_size=38, color=STAT),
            MathTex(r"-\log P(w_t \mid w_{<t}) = D_{\mathrm{KL}}\big(P(T \mid w_{\le t}) \,\|\, "
                    r"P(T \mid w_{<t})\big)", font_size=34, color=MODEL),
        ).arrange(DOWN, buff=0.5).move_to([0, 1.6, 0])
        rows = rows_of([
            (r"Hale, \ 2001: \ the effort a word takes is its surprisal, \ how improbable it was given what came "
             r"before", WHITE),
            (r"Levy, \ 2008: \ if a reader keeps a probability over every analysis $T$ of the sentence so far, \ "
             r"surprisal is exactly how much that belief has to change", MODEL),
            (r"so one quantity covers garden paths, \ predictable words and everything between: \ a theory that "
             r"says reading time is linear in surprisal", STAT),
            (r"it can be tested on any text, \ with any language model, \ against any reading times", WORD),
        ], 12.6, 27, 0.38).move_to([0, -1.55, 0])
        tag = published_tag(r"Hale (2001); \ Levy (2008)")
        with self.voiceover(
            "Surprisal turns this into a theory. <bookmark mark='a'/> John Hale proposed in 2001 that the effort a "
            "word takes is its surprisal: minus the log of how probable it was, given everything that came before. "
            "<bookmark mark='b'/> Roger Levy showed in 2008 why that might be. Suppose a reader keeps a probability "
            "over every possible analysis of the sentence so far. When the next word arrives, the belief must be "
            "updated, and the size of the update, measured as a relative entropy, is exactly the word's surprisal. "
            "<bookmark mark='c'/> One quantity then covers garden paths, predictable words and everything in "
            "between, and the theory says reading time grows in proportion to it. <bookmark mark='d'/> Best of all, "
            "it can be tested on any text, with any language model, against any reading times."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def example(self):
        d = load("surprisal")
        head = heading(r"Ten stories, \ every word")
        words = [str(w) for w in d["ex_words"][:11]]
        surp = d["ex_surprisal"][:11]
        rt = d["ex_rt"][:11]
        A = axes([0, len(words)], [0, 22], x_length=11.0, y_length=1.9, xticks=[], yticks=[0, 10, 20],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"surprisal, \ bits", center=[0.3, 1.5, 0], font_size=15)
        B = axes([0, len(words)], [300, 420], x_length=11.0, y_length=1.9, xticks=[], yticks=[300, 350, 400],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"reading time, \ ms", center=[0.3, -1.2, 0], font_size=15)
        sb = VGroup(*[bars(A.ax, [k + 0.5], [s], STAT, 0.6) for k, s in enumerate(surp)])
        rb = VGroup(*[bars(B.ax, [k + 0.5], [r], WORD, 0.6) for k, r in enumerate(rt)])
        wl = VGroup(*[label(rf"\emph{{{w}}}", font_size=24).move_to([B.ax.c2p(k + 0.5, 300)[0], 0.15, 0])
                      for k, w in enumerate(words)])
        note = label(rf"Natural Stories, \ story 1; \ mean of about {d['readers_median']:.0f} readers per word; \ "
                     rf"surprisal from Psyche's trigram model of the novels", font_size=20, color=GREY_A
                     ).to_edge(DOWN, buff=0.65)
        ptag = psyche_tag(r"\texttt{language.KneserNey}; \ open data: \ Natural Stories")
        jw = words.index("journey")
        with self.voiceover(
            "Here is the start of the first story in the Natural Stories corpus: if you were to journey to the north "
            "of England. <bookmark mark='a'/> Above, each word's surprisal under Psyche's trigram model of the "
            f"novels. Journey is the surprising one, at {surp[jw]:.0f} bits; you and the are almost free. "
            "<bookmark mark='b'/> Below, the mean time readers spent on each word. Word by word it is noisy: reading "
            "times depend on length, on frequency, on where a reader's attention happens to be. "
            "<bookmark mark='c'/> To see the relation, we need all ten thousand words at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(wl), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in sb], lag_ratio=0.1), run_time=2)
            self.play(Indicate(wl[jw], color=STAT))
            vo.wait_until("b")
            self.play(FadeIn(B), LaggedStart(*[GrowFromEdge(b, DOWN) for b in rb], lag_ratio=0.1), run_time=2)
            vo.wait_until("c")
        self.clear_scene()

    def fit(self):
        d = load("surprisal")
        head = heading(r"Reading time against surprisal")
        A = axes([0, 20], [315, 365], x_length=5.6, y_length=3.6, xticks=[0, 5, 10, 15, 20], yticks=[320, 340, 360],
                 yfmt=lambda v: f"{v:.0f}", xlabel=r"surprisal of the word, \ bits", ylabel=r"mean reading time, \ ms",
                 center=[-3.2, 0.2, 0], font_size=16)
        cur = VGroup(curve(A.ax, d["bin_mid"], d["bin_rt"], WORD, 3), scatter(A.ax, d["bin_mid"], d["bin_rt"], WORD,
                                                                                 0.07, 1))
        nxt = VGroup(DashedVMobject(curve(A.ax, d["bin_mid"], d["bin_next"], STAT, 3), num_dashes=24),
                     scatter(A.ax, d["bin_mid"], d["bin_next"], STAT, 0.06, 1))
        key = legend([(WORD, r"time on the word itself"), (STAT, r"time on the \emph{next} word")],
                     font_size=17).move_to(A.ax.c2p(7, 360))
        coef = dict(zip([str(n) for n in d["names"]], d["coef"]))
        se = dict(zip([str(n) for n in d["names"]], d["se"]))
        rows = rows_of([
            (rf"{num(d['n_words'])} words in ten groups by surprisal: \ reading time rises steadily, \ about "
             rf"{d['bin_rt'][-1] - d['bin_rt'][0]:.0f} ms from the most to the least predictable tenth", WHITE),
            (r"but surprising words are also long and rare; \ fitted together with length and frequency, \ the "
             r"cost shows up on the \emph{next} word", STAT),
            (rf"{coef['prev_surprisal']:.1f} ms per bit on the following word \ "
             rf"(95\% interval $\pm${2 * se['prev_surprisal']:.1f}); "
             rf"\ {round(coef['surprisal'], 1) + 0.0:.1f} on the word itself", MODEL),
            (r"self-paced readers press on before a word is fully processed: \ spillover is the rule in this method",
             GREY_A),
        ], 5.8, 23, 0.36).move_to([3.6, 0.1, 0])
        ptag = psyche_tag(r"\texttt{language.rt\_regression}; \ open data: \ Natural Stories")
        with self.voiceover(
            "Here they are. <bookmark mark='a'/> All ten thousand words, sorted into ten groups by surprisal, from "
            "the most predictable tenth to the least. Mean reading time rises steadily, by about "
            f"{d['bin_rt'][-1] - d['bin_rt'][0]:.0f} milliseconds across the range. <bookmark mark='b'/> But "
            "surprising words also tend to be long and rare, which slows reading on its own. Fit everything "
            "together, and with length and frequency held fixed, the cost of surprise appears on the word after the "
            f"surprising one: {coef['prev_surprisal']:.1f} milliseconds per bit, very reliably, and nothing on the "
            "word itself. <bookmark mark='c'/> That's typical of self-paced reading, where people press for the next "
            "word before they have finished with this one. Eye-tracking studies see the cost sooner. "
            "<bookmark mark='d'/> Nathaniel Smith and Roger Levy found the relation is linear in surprisal across a "
            "range of probabilities spanning six orders of magnitude, as the theory says. A trigram model is crude, "
            "and still it captures something real about what readers expect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(Create(cur), FadeIn(key[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(nxt), FadeIn(key[1]), FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
        self.clear_scene()
