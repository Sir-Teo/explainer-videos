from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Position(VoiceoverScene):
    def construct(self):
        self.card()
        self.your_sheet()
        self.peers()
        self.two_stores()

    def card(self):
        card = chapter_card(2, r"First and last", r"Which words survive a list, \ and why those?",
                            lit={1962: r"Murdock", 1966: r"Glanzer \& Cunitz", 1971: r"Rundus", 2014: r"PEERS"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter two. First and last."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def your_sheet(self):
        head = heading(r"Score your sheet")
        chips = VGroup(*[word_chip(w, font_size=22, width=1.55) for w in WORDS]).arrange_in_grid(2, 8, buff=0.16)
        chips.move_to([0, 1.7, 0])
        nums = VGroup(*[label(str(i + 1), font_size=16, color=GREY_B).next_to(ch, UP, buff=0.06)
                        for i, ch in enumerate(chips)])
        first = SurroundingRectangle(VGroup(*chips[0:4]), color=MODEL, buff=0.08)
        last = SurroundingRectangle(VGroup(*chips[12:16]), color=WORD, buff=0.08)
        rows = rows_of([
            (r"tick each word you wrote; \ count how many of the first four, \ the middle eight, \ the last four", WHITE),
            (r"most people: \ more of the first four than the middle, \ and most of all of the last four", WORD),
            (r"and look at the first word you wrote: \ for nearly half of people it is one of the last few", CUE),
        ], 12.4, 26, 0.32).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Take out your sheet. Here is the list again, in the order you saw it. <bookmark mark='a'/> Tick each "
            "word you wrote down, and count three things: how many of the first four you got, how many of the middle "
            "eight, and how many of the last four. <bookmark mark='b'/> If you're like most people, you got more of "
            "the first four than of the middle, and more of the last four than of anything. "
            "<bookmark mark='c'/> Now look at the first word you wrote. For nearly half of people it's the very last "
            "word of the list, and for most of the rest it's one of the last few. Your recall started where the list "
            "ended."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.05), FadeIn(nums))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(first), Create(last), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(chips[15], color=WORD), FadeIn(rows[2]))
        self.clear_scene()

    def peers(self):
        d = load("peers")
        head = heading(r"Serial position, \ measured on 3,528 lists")
        A = position_axes([-3.0, 0.35, 0], x_length=6.6, y_length=3.5)
        ax = A.ax
        x = np.arange(1, 17)
        spc_ = curve_in(ax, x, d["spc"], DATA, 4)
        dots = scatter(ax, x, d["spc"], DATA, radius=0.07, opacity=1.0)
        B = position_axes([3.9, 0.35, 0], x_length=4.4, y_length=3.5, ymax=0.6, ylabel=r"recalled first")
        bx = B.ax
        pf = bars(bx, x, d["pfr"], CUE, width=0.7)
        prim = label(r"primacy", font_size=22, color=MODEL).next_to(ax.c2p(2.0, d["spc"][0]), UP, buff=0.25)
        rec = label(r"recency", font_size=22, color=WORD).next_to(ax.c2p(15.0, d["spc"][-1]), UP, buff=0.25)
        mid = label(r"the middle", font_size=22, color=GREY_B).next_to(ax.c2p(8.5, d["spc"][8]), DOWN, buff=0.35)
        rows = rows_of([
            (rf"PEERS, \ the Penn study of encoding and retrieval: \ {d['n_subjects']} people, \ "
             rf"{num(d['n_lists'])} lists of 16 words, \ recall straight after the last word", WHITE),
            (rf"position 1: \ {pct(d['spc'][0])}; \ the middle: \ about {pct(np.mean(d['spc'][6:10]))}; \ "
             rf"position 16: \ {pct(d['spc'][-1])}; \ the last word starts {pct(d['pfr'][-1])} of recalls", DATA),
        ], 12.6, 23, 0.22).to_edge(DOWN, buff=0.85)
        tag = published_tag(r"open data: \ PEERS (Kahana lab), \ as packaged with psifr")
        with self.voiceover(
            "In 1962 Bennet Murdock gave people lists of ten to forty words at one or two seconds a word, and drew "
            "the probability of recalling each word against its position in the list. <bookmark mark='a'/> The "
            "same curve, measured today in open data. These are three thousand five hundred lists of sixteen words, "
            f"recalled by {d['n_subjects']} people in the Kahana lab's Penn Electrophysiology of Encoding and "
            "Retrieval Study. <bookmark mark='b'/> The curve has three parts. The first word is recalled more often "
            "than the middle ones: that's primacy. <bookmark mark='c'/> The middle is a long flat stretch. "
            "<bookmark mark='d'/> And the last few are recalled best of all: recency. <bookmark mark='e'/> On the "
            "right, the word people recalled first. It's overwhelmingly the last one, and almost never a word from "
            "the middle. Murdock found that lengthening the list lowers the middle but leaves the last half-dozen "
            "positions almost untouched."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(spc_), FadeIn(dots), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(prim))
            vo.wait_until("c")
            self.play(FadeIn(mid))
            vo.wait_until("d")
            self.play(FadeIn(rec), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(B), LaggedStart(*[GrowFromEdge(b, DOWN) for b in pf], lag_ratio=0.05), run_time=2.0)
        self.clear_scene()

    def two_stores(self):
        d = load("peers")
        head = heading(r"Two ends, \ two causes?")
        A = position_axes([-3.3, 0.6, 0], x_length=6.0, y_length=3.2)
        ax = A.ax
        x = np.arange(1, 17)
        c = curve_in(ax, x, d["spc"], DATA, 4)
        recz = Rectangle(width=abs(ax.c2p(16.4, 0)[0] - ax.c2p(12.6, 0)[0]), height=A.ax.height,
                         stroke_width=0, fill_color=WORD, fill_opacity=0.18)
        recz.move_to([(ax.c2p(12.6, 0)[0] + ax.c2p(16.4, 0)[0]) / 2, ax.get_center()[1], 0])
        primz = Rectangle(width=abs(ax.c2p(4.4, 0)[0] - ax.c2p(0.8, 0)[0]), height=A.ax.height,
                          stroke_width=0, fill_color=MODEL, fill_opacity=0.18)
        primz.move_to([(ax.c2p(0.8, 0)[0] + ax.c2p(4.4, 0)[0]) / 2, ax.get_center()[1], 0])
        rows = rows_of([
            (r"Glanzer and Cunitz, \ 1966: \ 30 seconds of counting before recall", WHITE),
            (r"recency vanishes; \ primacy and the middle are untouched", WORD),
            (r"slower presentation raises the early and middle words, \ not the last", MODEL),
            (r"Rundus, \ 1971: \ people who rehearse aloud say the early words most often", MODEL),
            (r"the reading of the day: \ the last words are still in a short-term store; \ the first got extra "
             r"rehearsal into a long-term one", CTX),
            (r"hold on to that reading: \ the next chapter breaks it", LOST),
        ], 5.8, 22, 0.24).move_to([3.7, -0.1, 0])
        tag = historical_tag(r"Glanzer \& Cunitz (1966); \ Rundus (1971)")
        with self.voiceover(
            "Why are the two ends special? The answer of the 1960s was that they have different causes. "
            "<bookmark mark='a'/> In 1966 Murray Glanzer and Anita Cunitz had people count aloud for thirty seconds "
            "between the last word and recall. <bookmark mark='b'/> Recency vanished. The first and middle words "
            "were recalled as well as ever. <bookmark mark='c'/> And presenting the words more slowly helped the "
            "early and middle part of the curve, but not its end. Two manipulations, each touching one end and not "
            "the other: a dissociation, the logic of Part 7. <bookmark mark='d'/> Dewey Rundus then asked people to "
            "rehearse aloud while they studied, and found that the early words were rehearsed more often than any "
            "others, and the number of rehearsals tracked primacy. <bookmark mark='e'/> So the textbook story was "
            "two stores. The last few words are still in the short-term store of Part 19 when recall begins, and "
            "spill out first. The first few got extra rehearsal, which moved them into long-term memory. "
            "<bookmark mark='f'/> It's a tidy story. The next chapter shows a result that it cannot explain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(c), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(recz), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(primz), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()
