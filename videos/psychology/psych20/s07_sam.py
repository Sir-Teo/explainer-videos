from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Sam(VoiceoverScene):
    def construct(self):
        self.card()
        self.buffer()
        self.search()
        self.curves()

    def card(self):
        card = chapter_card(6, r"Searching associative memory", r"Can a rehearsal buffer explain both ends?",
                            lit={1968: r"Atkinson \& Shiffrin", 1980: r"Raaijmakers \& Shiffrin", 1981: r"SAM"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter six. Searching associative memory."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def buffer(self):
        head = heading(r"SAM, \ part 1: \ a buffer that writes to long-term memory")
        slots = VGroup(*[RoundedRectangle(corner_radius=0.1, width=1.9, height=0.75, stroke_color=CTX,
                                          stroke_width=3) for _ in range(4)]).arrange(RIGHT, buff=0.25)
        slots.move_to([0, 1.9, 0])
        bl = label(r"the rehearsal buffer: \ room for $r = 4$", font_size=22, color=CTX).next_to(slots, UP, buff=0.2)
        rng = np.random.default_rng(3)
        buf: list[int] = []
        frames = []
        for i in range(7):
            if len(buf) == 4:
                buf.pop(int(rng.integers(4)))
            buf.append(i)
            frames.append(list(buf))
        rows = rows_of([
            (r"each new word enters the buffer; \ when it is full, \ a random word leaves", CTX),
            (r"every step a word spends in the buffer strengthens its link to the list's context, \ by $a$", WORD),
            (r"and its link to every other word in the buffer with it, \ by $b$", SAM),
            (r"early words wait longer before the buffer fills, \ so they gain more strength: \ primacy", MODEL),
            (r"the last words are still in the buffer when recall starts: \ recency", WORD),
        ], 12.4, 25, 0.28).move_to([0, -1.25, 0])
        tag = historical_tag(r"Raaijmakers \& Shiffrin (1981)")
        ptag = psyche_tag(r"\texttt{memory.sam\_simulate}: \ $r = 4$, \ $a = b = 0.1$")
        with self.voiceover(
            "The first great model of the search grew straight out of the two-store story. Jeroen Raaijmakers and "
            "Richard Shiffrin called it the search of associative memory, SAM, in 1981. <bookmark mark='a'/> At "
            "study, words pass through a rehearsal buffer with room for about four. Each new word enters; when the "
            "buffer is full, a word chosen at random leaves to make room. <bookmark mark='b'/> Every moment a word "
            "spends in the buffer strengthens its association to the context of the list, <bookmark mark='c'/> and "
            "to every other word sharing the buffer with it. <bookmark mark='d'/> The first words have the buffer "
            "to themselves for a while before it fills, so they stay longest and grow strongest: that's primacy, "
            "Rundus's extra rehearsal, as a mechanism. <bookmark mark='e'/> And the last words are still in the "
            "buffer at the end, ready to be reported first: recency."
        ) as vo:
            self.play(FadeIn(head), FadeIn(slots), FadeIn(bl), FadeIn(tag), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            shown = VGroup()
            for f in frames:
                new = VGroup(*[label(WORDS[w], font_size=22, color=WORD).move_to(slots[k]) for k, w in enumerate(f)])
                self.play(FadeOut(shown), FadeIn(new), run_time=0.5)
                shown = new
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def search(self):
        head = heading(r"SAM, \ part 2: \ sample, \ recover, \ stop")
        eq1 = MathTex(r"P(\text{sample } i) = \frac{S(C, i)\, S(j, i)}{\sum_k S(C, k)\, S(j, k)}", font_size=38,
                      color=SAM)
        eq2 = MathTex(r"P(\text{recover } i) = 1 - e^{-[S(C, i) + S(j, i)]}", font_size=38, color=WORD)
        eqs = VGroup(eq1, eq2).arrange(DOWN, buff=0.4).move_to([0, 1.6, 0])
        rows = rows_of([
            (r"first, \ report what is still in the buffer", CTX),
            (r"then search: \ the cues are the list context $C$ and the last word recalled, \ $j$", CUE),
            (r"sample a word in proportion to its combined strength; \ recover it, \ or fail", SAM),
            (r"after too many failures in a row, \ stop", LOST),
            (r"one model gives serial position, \ the order of recall, \ and when people give up", MODEL),
        ], 12.4, 25, 0.28).move_to([0, -1.5, 0])
        with self.voiceover(
            "At test, SAM first reports whatever is still in the buffer. <bookmark mark='a'/> Then it searches "
            "long-term memory, using two cues at once: the context of the list, and the word it has just "
            "recalled. <bookmark mark='b'/> A word is sampled with a probability proportional to the product of its "
            "strengths to the two cues, <bookmark mark='c'/> and once sampled it is recovered, or not, with a "
            "probability that grows with the same strengths. <bookmark mark='d'/> After a run of failures, the "
            "search stops. <bookmark mark='e'/> It's a beautiful machine. With a handful of parameters it gives the "
            "serial-position curve, a reason why one word leads to the next, and a reason why people stop."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Write(eq1), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Write(eq2))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def curves(self):
        s, d = load("sam"), load("peers")
        head = heading(r"SAM against the data")
        A = position_axes([-3.4, 0.75, 0], x_length=5.6, y_length=3.0)
        ax = A.ax
        x = np.arange(1, 17)
        cd = curve_in(ax, x, d["spc"], DATA, 4)
        cs = curve_in(ax, x, s["spc"], SAM, 4)
        B = lag_axes([3.4, 0.75, 0], x_length=5.6, y_length=3.0)
        bx = B.ax
        kd = crp_curves(bx, d["lags"], d["crp"], DATA)
        ks = crp_curves(bx, s["lags"], s["crp"], SAM)
        key = legend([(DATA, r"PEERS"), (SAM, r"SAM, \ simulated")], font_size=19).move_to(ax.c2p(8.5, 0.2))
        i1, im1 = list(s["lags"]).index(1), list(s["lags"]).index(-1)
        rows = rows_of([
            (r"primacy and recency: \ yes, \ with the buffer doing both", SAM),
            (rf"contiguity: \ yes; \ but SAM's is symmetric, \ $+1$: \ {s['crp'][i1]:.2f}, \ $-1$: \ "
             rf"{s['crp'][im1]:.2f}: \ two words in the buffer together are linked both ways", LOST),
            (r"and Bjork and Whitten's long-term recency: \ arithmetic after every word empties the buffer, \ so "
             r"SAM predicts none", LOST),
        ], 12.6, 23, 0.26).to_edge(DOWN, buff=0.85)
        ptag = psyche_tag(r"\texttt{memory.sam\_simulate}: \ 4,000 lists, \ parameters set by hand, \ not fitted")
        with self.voiceover(
            "Let's run it, with parameters set by hand, on four thousand lists of sixteen words. "
            "<bookmark mark='a'/> It produces primacy and recency, both from the buffer, and a flat middle. "
            "<bookmark mark='b'/> It produces contiguity too: words that shared the buffer are linked, so one leads "
            "to the next. But look at the shape. SAM's links are made by being in the buffer together, and that is "
            "a symmetric relation. Its curve is as high at minus one as at plus one. People's is not. "
            "<bookmark mark='c'/> And remember Bjork and Whitten. Arithmetic after every word means the buffer is "
            "always emptied, so SAM predicts that recency should vanish, and that contiguity should vanish with it. "
            "Neither does. Something other than a buffer is producing them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(key), Create(cd), Create(kd), FadeIn(ptag))
            vo.wait_until("a")
            self.play(Create(cs), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ks), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
