from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


class Thought(VoiceoverScene):
    def construct(self):
        self.card()
        self.whorf()
        self.blues()
        self.numbers()

    def card(self):
        card = chapter_card(11, r"Language and thought", r"Does the language you speak shape how you think?",
                            lit={1956: r"Whorf", 1969: r"Berlin \& Kay", 2007: r"Winawer et al.",
                                 2008: r"Frank et al."},
                            part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter eleven. Language and thought."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def whorf(self):
        head = heading(r"Whorf's question")
        rows = rows_of([
            (r"Benjamin Lee Whorf: \ speakers of different languages are led by their grammars to different views "
             r"of the world", WHITE),
            (r"the strong version: \ language determines thought, \ so some thoughts are unthinkable without the "
             r"words; \ almost no one holds it now", LOST),
            (r"the weak version: \ language nudges perception, \ memory and attention in measurable ways", STAT),
            (r"Berlin \& Kay, \ 1969: \ languages differ in how many basic colour words they have, \ but the words "
             r"are added in a broadly regular order: \ constraint, \ not chaos", MODEL),
        ], 12.6, 26, 0.36).move_to([0, -0.75, 0])
        # Berlin and Kay's order of basic colour terms (1969): stages I to VII
        stages = [("I", ["#F4F4F4", "#1A1A1A"]), ("II", ["#D33A2C"]), ("III", ["#3FA34D"]), ("IV", ["#F2C230"]),
                  ("V", ["#2E62C9"]), ("VI", ["#7A4A21"]), ("VII", ["#8A3FB5", "#F08DB5", "#F0922B", "#8C8C8C"])]
        seq = VGroup()
        for num_, cols_ in stages:
            sw = VGroup(*[Square(0.42, stroke_color=GREY_B, stroke_width=1, fill_color=c_, fill_opacity=1)
                          for c_ in cols_]).arrange(RIGHT, buff=0.06)
            seq.add(VGroup(sw, label(num_, font_size=20, color=GREY_A).next_to(sw, DOWN, buff=0.1)))
        seq.arrange(RIGHT, buff=0.45).move_to([0, 2.15, 0])
        arrows_ = VGroup(*[Arrow(seq[k].get_right(), seq[k + 1].get_left(), buff=0.06, color=GREY_B,
                                 stroke_width=2, max_tip_length_to_length_ratio=0.35) for k in range(len(seq) - 1)])
        sq = label(r"stages, \ simplified: \ III and IV come in either order", font_size=18, color=GREY_B).next_to(
            seq, DOWN, buff=0.15)
        tag = historical_tag(r"Whorf (1956, \ collected); \ Berlin \& Kay (1969)")
        with self.voiceover(
            "Does the language you speak shape how you think? <bookmark mark='a'/> Benjamin Lee Whorf, a fire "
            "inspector and amateur linguist, argued in the 1930s and 40s that speakers of different languages are "
            "led by their grammars to different views of the world. <bookmark mark='b'/> The strong version, that "
            "language determines thought so that some thoughts are unthinkable without the words, has almost no "
            "defenders now; chapter ten's patients think without language. <bookmark mark='c'/> The weak version, "
            "that language nudges perception, memory and attention, is testable. <bookmark mark='d'/> And there are "
            "limits on variety. Brent Berlin and Paul Kay found in 1969 that languages differ in how many basic "
            "colour words they have, but add them in a broadly regular order. Constraint, not chaos."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15), LaggedStart(*[FadeIn(g) for g in seq], lag_ratio=0.3),
                      FadeIn(arrows_), FadeIn(sq), run_time=3)
        self.clear_scene()

    def blues(self):
        head = heading(r"Russian blues")
        cols = [interpolate_color(ManimColor("#7FD3FF"), ManimColor("#123E9C"), a) for a in np.linspace(0, 1, 9)]
        strip = VGroup(*[Square(0.8, stroke_width=0, fill_color=c, fill_opacity=1) for c in cols]).arrange(
            RIGHT, buff=0.04).move_to([-2.6, 1.8, 0])
        brace_l = Brace(strip[:4], UP, color=SOUND)
        brace_r = Brace(strip[5:], UP, color=SOUND)
        tl = label(r"\emph{goluboy}", font_size=24, color=SOUND).next_to(brace_l, UP, buff=0.05)
        tr = label(r"\emph{siniy}", font_size=24, color=SOUND).next_to(brace_r, UP, buff=0.05)
        rows = rows_of([
            (r"Russian has two basic words for blue: \ \emph{goluboy}, \ lighter, \ and \emph{siniy}, \ darker", WHITE),
            (r"Winawer and colleagues, \ 2007: \ Russian speakers told two blues apart faster when they fell on "
             r"opposite sides of the boundary; \ English speakers did not", MODEL),
            (r"the advantage vanished when Russian speakers had to rehearse digits, \ a verbal load, \ but not a "
             r"spatial one: \ language working in real time", STAT),
            (r"several later studies did not find category effects of this kind, \ or found them shaped by the "
             r"stimuli: \ the Ledger calls it contested", LOST),
        ], 12.0, 26, 0.36).move_to([0, -1.4, 0])
        sl = label(r"colours illustrative", font_size=15, color=GREY_B).next_to(strip, RIGHT, buff=0.25)
        tag = published_tag(r"Winawer et al. (2007), \ \emph{PNAS}")
        with self.voiceover(
            "Here's a well-known test of the weak version. <bookmark mark='a'/> Russian has two basic words for "
            "blue: goluboy for lighter blues, siniy for darker ones. <bookmark mark='b'/> In 2007 Jonathan Winawer "
            "and colleagues found that Russian speakers told two blues apart faster when they fell on opposite sides "
            "of that boundary than when they fell on the same side. English speakers, looking at the same blues, "
            "showed no such advantage. <bookmark mark='c'/> And the advantage vanished when the Russian speakers had "
            "to rehearse a string of digits at the same time, a verbal load, but not when they had to remember a "
            "spatial pattern. Language seemed to be working in real time. <bookmark mark='d'/> Several later studies "
            "did not find category effects of this kind, or found them depended on how the colours were chosen. The "
            "Ledger calls the claim contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(brace_l), FadeIn(tl), FadeIn(brace_r), FadeIn(tr), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def numbers(self):
        head = heading(r"Numbers without number words")
        row1 = VGroup(*[Dot(radius=0.15, color=WORD) for _ in range(7)]).arrange(RIGHT, buff=0.2).move_to([-1.9, 1.9, 0])
        row2 = VGroup(*[Dot(radius=0.15, color=SOUND) for _ in range(7)]).arrange(RIGHT, buff=0.2).move_to(
            [-1.9, 1.2, 0])
        l1 = label(r"in view: \ match this line", font_size=21, color=GREY_A).next_to(row1, LEFT, buff=0.25)
        l2 = label(r"with this one", font_size=21, color=GREY_A).next_to(row2, LEFT, buff=0.25)
        hid = VGroup(*[Dot(radius=0.15, color=WORD) for _ in range(7)]).arrange(RIGHT, buff=0.2).move_to(
            [-1.9, -0.4, 0])
        cover = RoundedRectangle(corner_radius=0.1, width=hid.width + 0.4, height=0.6, stroke_color=GREY_B,
                                 fill_color=GREY_E, fill_opacity=1).move_to(hid)
        row3 = VGroup(*[Dot(radius=0.15, color=SOUND) for _ in range(6)]).arrange(RIGHT, buff=0.2)
        row3.move_to([-1.9, -1.1, 0]).align_to(hid, LEFT)
        l3 = label(r"hidden: \ seven \ldots", font_size=21, color=GREY_A).next_to(cover, LEFT, buff=0.25)
        l4 = label(r"\ldots matched from memory", font_size=21, color=GREY_A).next_to(row3, LEFT, buff=0.25)
        l4.align_to(l3, RIGHT)
        miss = label(r"six", font_size=24, color=LOST).next_to(row3, RIGHT, buff=0.35)
        sk = label(r"schematic of the task", font_size=18, color=GREY_B).move_to([-3.4, -2.0, 0])
        for m in (l1, l2, l3, l4):
            keep_in_frame(m)
        rows = rows_of([
            (r"the Pirah\~a of the Amazon have no words for exact numbers, \ only for small and larger amounts", WHITE),
            (r"Frank, \ Everett, \ Fedorenko \& Gibson, \ 2008: \ matching a line of objects one to one, \ in view, \ "
             r"they did well", MODEL),
            (r"when the set had to be remembered, \ or matched to something hidden, \ errors grew with the number", LOST),
            (r"number words look like a cognitive technology: \ a tool for holding exact quantities, \ not the "
             r"source of the idea of quantity", STAT),
        ], 5.4, 23, 0.36).move_to([3.9, 0.0, 0])
        tag = published_tag(r"Frank, \ Everett, \ Fedorenko \& Gibson (2008)")
        with self.voiceover(
            "Numbers give a sharper case. <bookmark mark='a'/> The Pirahã, who live along a river in the Amazon, "
            "have no words for exact numbers, only words for smaller and larger amounts. <bookmark mark='b'/> In "
            "2008 Michael Frank and colleagues asked Pirahã speakers to match a line of objects with a line of their "
            "own. With both lines in view, they did well. <bookmark mark='c'/> But when the set had to be remembered, "
            "or matched to one that was hidden, their errors grew with the number of objects. "
            "<bookmark mark='d'/> Number words look like a cognitive technology: a tool for holding exact "
            "quantities in mind, rather than the source of the idea of quantity itself. That is the weak version of "
            "Whorf, and here it holds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(row1), FadeIn(l1), FadeIn(sk))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(row2, lag_ratio=0.2), FadeIn(l2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(hid), FadeIn(l3), FadeIn(rows[2]))
            self.play(FadeIn(cover))
            self.play(FadeIn(row3, lag_ratio=0.2), FadeIn(l4))
            self.play(FadeIn(miss))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
