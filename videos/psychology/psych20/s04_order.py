from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403

EXAMPLE = (16, 15, 14, 1, 2, 9)  # a made-up recall sequence for the worked lag-CRP


class Order(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.peers()
        self.persons()
        self.long_term()

    def card(self):
        card = chapter_card(3, r"One word leads to the next", r"In what order do memories come back?",
                            lit={1974: r"Bjork \& Whitten", 1977: r"Baddeley \& Hitch", 1996: r"Kahana",
                                 2014: r"Healey \& Kahana"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter three. One word leads to the next."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def derive(self):
        head = heading(r"Derived: \ the lag-conditional response probability")
        cells = VGroup(*[Square(side_length=0.62, stroke_color=GREY_C, stroke_width=2) for _ in range(16)])
        cells.arrange(RIGHT, buff=0.08).move_to([0, 2.15, 0])
        pos = VGroup(*[label(str(i + 1), font_size=18, color=GREY_B).move_to(c) for i, c in enumerate(cells)])
        seq = VGroup(*[label(str(p), font_size=30, color=WORD) for p in EXAMPLE]).arrange(RIGHT, buff=0.55)
        seq.move_to([0, 1.0, 0])
        arrows = VGroup()
        lags = []
        for a, b in zip(EXAMPLE, EXAMPLE[1:]):
            lags.append(b - a)
        lag_l = VGroup(*[label(rf"{l:+d}", font_size=20, color=CUE).move_to(
            (seq[i].get_center() + seq[i + 1].get_center()) / 2 + DOWN * 0.42) for i, l in enumerate(lags)])
        eq = MathTex(r"\text{CRP}(\ell)", r"=", r"\frac{\#\,\text{transitions of lag } \ell}"
                     r"{\#\,\text{times lag } \ell \text{ was possible}}", font_size=38).move_to([0, -0.35, 0])
        eq[0].set_color(CUE)
        rows = rows_of([
            (r"lag = the next word's position minus this one's; \ $+1$ is the next word in the list", CUE),
            (r"divide by the chances: \ after recalling 15, \ the lag $+1$ word (16) was already used, \ so lag $+1$ was "
             r"not possible", WHITE),
            (r"without the denominator, \ words in the middle would look more ``contiguous'' just because they have "
             r"more neighbours", LOST),
        ], 12.6, 23, 0.24).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Serial position tells you which words come back. The order they come back in tells you more. "
            "<bookmark mark='a'/> Here is one made-up recall: sixteen, fifteen, fourteen, then one, two, then nine. "
            "<bookmark mark='b'/> Each step from one recall to the next has a lag: the position of the next word "
            "minus the position of this one. Fifteen after sixteen is a lag of minus one; two after one, plus one. "
            "<bookmark mark='c'/> Michael Kahana's measure, the lag-conditional response probability, counts how "
            "often each lag was taken, and divides by how often it could have been taken: the lag must lead to a "
            "word that exists and hasn't been recalled yet. <bookmark mark='d'/> That denominator matters. After "
            "recalling fifteen, a lag of plus one would lead to sixteen, which was already used, so it doesn't "
            "count as a chance. <bookmark mark='e'/> Without it, any analysis would find that words in the middle of "
            "a list are followed by their neighbours, simply because they have more of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(pos))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in seq], lag_ratio=0.3),
                      *[cells[p - 1].animate.set_fill(WORD, 0.35) for p in EXAMPLE], run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lag_l], lag_ratio=0.3), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(Write(eq))
            vo.wait_until("d")
            self.play(Indicate(seq[1], color=CUE), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def peers(self):
        d = load("peers")
        head = heading(r"Contiguity, \ and it leans forward")
        A = lag_axes([-2.4, 0.3, 0], x_length=7.4, y_length=3.8)
        ax = A.ax
        c = crp_curves(ax, d["lags"], d["crp"], DATA)
        i1, im1 = list(d["lags"]).index(1), list(d["lags"]).index(-1)
        fwd = label(rf"$+1$: \ {d['crp'][i1]:.2f}", font_size=22, color=WORD).next_to(
            ax.c2p(1, d["crp"][i1]), RIGHT, buff=0.15)
        bwd = label(rf"$-1$: \ {d['crp'][im1]:.2f}", font_size=22, color=CTX).next_to(
            ax.c2p(-1, d["crp"][im1]), LEFT, buff=0.15)
        rows = rows_of([
            (r"after recalling a word, \ the next recall is very likely its neighbour in the list", WORD),
            (r"forward neighbours more than backward ones", CTX),
            (r"words studied seconds apart, \ with nothing to link them but time", GREY_A),
        ], 4.6, 22, 0.3).move_to([4.7, 0.3, 0])
        tag = published_tag(r"open data: \ PEERS (Kahana lab), \ as packaged with psifr")
        with self.voiceover(
            "Here is the lag-conditional response probability for the three and a half thousand lists. "
            "<bookmark mark='a'/> It's a sharp peak. Of all the words still available, the next one recalled is most "
            "likely to be a neighbour of the one just recalled. <bookmark mark='b'/> And the peak leans forward: "
            f"plus one has a probability of {d['crp'][i1]:.2f}, minus one {d['crp'][im1]:.2f}. Having recalled the "
            "word you studied at some moment, you tend to recall next the word you studied just after it. "
            "<bookmark mark='c'/> Remember that these are unrelated words in a random order. Neighbours share "
            "nothing but a moment in time, and still each one brings back the next. This is the temporal contiguity "
            "effect, and it's the second law of free recall."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            self.play(Create(c), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(fwd), FadeIn(bwd), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def persons(self):
        p = load("persons")
        head = heading(rf"Not an average: \ {p['n']} people, \ one at a time")
        A = axes([0, 0.7], [0, 0.7], x_length=4.6, y_length=4.6, xticks=[0, 0.2, 0.4, 0.6], yticks=[0, 0.2, 0.4, 0.6],
                 xlabel=r"CRP at lag $-1$", ylabel=r"CRP at lag $+1$", center=[-3.6, -0.1, 0], font_size=18,
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}")
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(0.7, 0.7), color=GREY_B, stroke_width=2)
        dots = scatter(ax, p["bwd"], p["fwd"], DATA, radius=0.055, opacity=0.85)
        rows = rows_of([
            (rf"each dot is one person's lag-CRP, \ forward against backward", WHITE),
            (rf"{pct(p['share_forward'])} of people lean forward: \ above the diagonal", WORD),
            (rf"{pct(p['share_recency'])} show recency, \ {pct(p['share_primacy'])} primacy, \ against their own "
             r"middle", DATA),
            (r"Healey and Kahana, \ 2014: \ the serial-position and contiguity curves are found in almost every "
             r"person, \ while how people \emph{start} recall varies", GREY_A),
            (r"a law, \ not an artefact of averaging different strategies", MODEL),
        ], 7.0, 23, 0.3).move_to([3.2, -0.1, 0])
        tag = published_tag(r"open data: \ PEERS; \ Healey \& Kahana (2014)")
        with self.voiceover(
            "An average curve can hide people who do something quite different, so it's worth looking at people one "
            f"at a time. <bookmark mark='a'/> Each dot is one of the {p['n']} participants: their own probability "
            "of a lag of plus one, against their own lag of minus one. <bookmark mark='b'/> "
            f"{spct(p['share_forward'])} of them lie above the diagonal, leaning forward. "
            f"<bookmark mark='c'/> And {spct(p['share_recency'])} recall the last word more "
            "often than their own middle words. <bookmark mark='d'/> Using all of PEERS, Kahana and Karl Healey made "
            "this test systematically in 2014. How people begin their recall varies: some start from the end, some "
            "from the beginning, some a few words back. But the serial-position curve and the contiguity curve "
            "appeared, recognisably, in almost every person. <bookmark mark='e'/> These are laws of the system, "
            "not a blend of strategies."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(diag), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def long_term(self):
        head = heading(r"Recency that refuses to die")
        strip = trial_strip([
            (r"a word", label(r"HORSE", font_size=28, color=WORD), r"1 s"),
            (r"arithmetic", label(r"7 + 4 + 9 = ?", font_size=26, color=GREY_B), r"seconds"),
            (r"a word", label(r"RIVER", font_size=28, color=WORD), r"1 s"),
            (r"arithmetic", label(r"3 + 8 + 2 = ?", font_size=26, color=GREY_B), r"seconds"),
            (r"... then recall", label(r"?", font_size=34, color=YOU), ""),
        ], frame_w=2.25, frame_h=1.1, font_size=18).move_to([0, 1.95, 0])
        rows = rows_of([
            (r"Bjork and Whitten, \ 1974: \ distraction after every word, \ the last one included", WHITE),
            (r"no short-term store survives that much arithmetic, \ and yet recency comes back", WORD),
            (r"what matters is the ratio: \ the gap between words against the time since the last one", CTX),
            (r"Baddeley and Hitch, \ 1977: \ rugby players recall the season's last games best, \ counted in games, "
             r"\ not weeks", CTX),
            (r"Howard and Kahana, \ 1999: \ contiguity survives the distraction too", CUE),
            (r"one mechanism, \ on every time scale: \ the next three chapters look for it", MODEL),
        ], 12.6, 24, 0.27).move_to([0, -1.25, 0])
        tag = historical_tag(r"Bjork \& Whitten (1974); \ Baddeley \& Hitch (1977); \ Howard \& Kahana (1999)")
        with self.voiceover(
            "Now the result the two-store story can't explain. <bookmark mark='a'/> In 1974 Robert Bjork and William "
            "Whitten filled the gap after every word with arithmetic, including after the last, so that by the time "
            "recall began even the last word had been pushed out of any short-term store. <bookmark mark='b'/> On "
            "the two-store story, recency should have been gone, as it was for Glanzer and Cunitz. And yet recency came back: the last words were again "
            "recalled best. <bookmark mark='c'/> What matters is not the delay itself but its ratio to the spacing "
            "of the list. Spread the words out and a long delay barely matters; it's the last items' place relative "
            "to the rest that counts. <bookmark mark='d'/> The same holds on the scale of months. Baddeley and Hitch "
            "asked rugby players to name the teams they had played that season. They remembered the most recent "
            "games best, and the decline was set by the number of games in between, not by the weeks. "
            "<bookmark mark='e'/> Marc Howard and Kahana showed in 1999 that contiguity survives the arithmetic "
            "too: words separated by seconds of arithmetic still bring back their neighbours. <bookmark mark='f'/> Recency "
            "and contiguity, at the scale of seconds and of seasons, with no short-term store to explain them. They "
            "call for one mechanism that works on every time scale, and the next chapters look for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(strip), FadeIn(tag))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
