from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n) -> str:
    """A whole number as a speaker says it (British: 'one hundred and twenty-eight')."""
    n = int(round(n))
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + say(n % 1000))


def say1(x: float) -> str:
    """A number with one decimal, spoken: 'six point seven'."""
    whole, tenth = divmod(int(round(10 * x)), 10)
    return say(whole) + ("" if tenth == 0 else " point " + _ONES[tenth])


def page(blocks, width=3.3):
    """A paper drawn as a page of labelled blocks; ``blocks`` is [(text, height)].  Each block has a heading stripe
    (``block[1]``) and a body (``block[0]``) that the passes light separately."""
    g = VGroup()
    for t, h in blocks:
        body = Rectangle(width=width - 0.3, height=h, stroke_width=0, fill_color=GREY_B, fill_opacity=0.12)
        stripe = Rectangle(width=width - 0.3, height=0.07, stroke_width=0, fill_color=GREY_B,
                           fill_opacity=0.35).align_to(body, UP)
        txt = label(t, font_size=16, color=GREY_B)
        if txt.width > width - 0.45:
            txt.width = width - 0.45
        g.add(VGroup(body, stripe, txt.move_to(body)))
    g.arrange(DOWN, buff=0.06)
    frame = Rectangle(width=width, height=g.height + 0.3, stroke_color=GREY_B, stroke_width=1.6, fill_color=BG,
                      fill_opacity=1).move_to(g)
    return VGroup(frame, g)


def abstract(width: float):
    """An invented abstract, for illustration: its lines, with the claim split into phrases (``lines[3]`` and
    ``lines[4]`` are groups of phrases)."""
    size = 21

    def phrases(*ps):
        return Tex(*ps, font_size=size, color=WHITE)
    title = label(r"\textbf{Skim: \ faster word counting}", font_size=24, color=HEAD)
    lines = VGroup(
        label(r"Word counting is a core step in text analytics.", font_size=size, color=WHITE),
        label(r"Existing counters spend most of their time hashing.", font_size=size, color=WHITE),
        label(r"We present Skim, \ which hashes each word only once.", font_size=size, color=WHITE),
        phrases(r"On thirty novels,", r"\ Skim is", r"\ 2.1 times faster", r"\ than the standard counter."),
        phrases(r"It needs", r"\ little extra memory."),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    g = VGroup(title, lines).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    if g.width > width:
        g.width = width
    ill = note(r"illustrative: \ an invented paper", font_size=16)
    return g, title, lines, ill


T = load("timing")
TIMES = np.asarray(T["times"])
RUN_SPREAD = 100 * (TIMES.max() / TIMES.min() - 1)
B = load("bias")
ENV_SPREAD = 100 * B["env_spread"]


class Reading(VoiceoverScene):
    def construct(self):
        self.card()
        self.passes()
        self.five_cs()
        self.unsaid()
        self.third()
        self.review()

    def card(self):
        card = chapter_card(6, r"Reading and reviewing", r"How do you read a paper, \ and judge one?",
                            lit=(1990, 2007), extra=((1990, r"Smith: \ the task of the referee"),
                                                     (2007, r"Keshav: \ how to read a paper")), part=PART)
        with self.voiceover("Chapter six. Reading and reviewing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def passes(self):
        head = label(r"Three passes \ (Keshav, \ 2007)", font_size=36).to_edge(UP, buff=0.3)
        blocks = [(r"title, \ authors", 0.32), (r"abstract", 0.39), (r"1 \ introduction", 0.57),
                  (r"2 \ design", 0.55), (r"figure", 0.48), (r"3 \ proofs, \ details", 0.55),
                  (r"4 \ evaluation", 0.55), (r"5 \ conclusion", 0.32), (r"references", 0.34)]
        # which pass first reads each block: 1, 2 or 3 (headings are read in the first pass)
        when = [1, 1, 1, 2, 2, 3, 2, 1, 1]
        pages = VGroup(*[page(blocks, width=3.7) for _ in range(3)]).arrange(RIGHT, buff=0.75).next_to(head, DOWN, buff=0.3)
        cols = (HEAD, DATA, YES)
        caps = VGroup()
        for i, (t, how, c) in enumerate((
                (r"first pass: \ 5 to 10 minutes", r"title, \ abstract, \ introduction, \ headings, \ conclusion; "
                 r"\ a glance at the references", HEAD),
                (r"second pass: \ up to an hour", r"everything but the proofs; \ the figures with care; \ mark the "
                 r"references to read", DATA),
                (r"third pass: \ hours", r"all of it: \ re-create the work, \ assumption by assumption", YES))):
            cap = VGroup(label(t, font_size=21, color=c), wrapped_label(how, 3.9, font_size=19, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1)
            cap.next_to(pages[i], DOWN, buff=0.18).align_to(pages[i], LEFT)
            caps.add(cap)

        def light(pg, k, color):
            anims = []
            for b, w in zip(pg[1], when):
                anims.append(b[1].animate.set_fill(color, opacity=0.9))
                if w <= k:
                    anims.append(b[0].animate.set_fill(color, opacity=0.35))
                    anims.append(b[2].animate.set_color(WHITE))
            return anims
        with self.voiceover(
            "In 2007 Srinivasan Keshav published a short note called How to Read a Paper. Its advice is to read "
            "in three passes. <bookmark mark='a'/> The first takes five to ten minutes: the title, the abstract and "
            "the introduction; the section headings, but not what is under them; the conclusion; and a glance at "
            "the references. That is enough to decide whether to go on. <bookmark mark='b'/> The second pass takes "
            "up to an hour. Read everything except the proofs and the fine details, and read the figures with "
            "care: are the axes labelled, are there error bars, does each figure show what the text claims? Mark "
            "the references you have not read. <bookmark mark='c'/> The third pass is for a paper you must "
            "understand completely, or review. Keshav's instruction is to re-create the work: make the same "
            "assumptions as the authors, rebuild it, and compare. For a beginner, that can take many hours."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pages))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(*light(pages[k], k + 1, cols[k]), FadeIn(caps[k]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def five_cs(self):
        head = label(r"After the first pass: \ the five Cs", font_size=36).to_edge(UP, buff=0.3)
        g, title, lines, ill = abstract(6.0)
        frame = SurroundingRectangle(g, buff=0.3, color=GREY_C, stroke_width=1.5, corner_radius=0.1)
        left = VGroup(frame, g).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3)
        ill.next_to(frame, DOWN, buff=0.12).align_to(frame, LEFT)
        cs = [(r"Category", r"what kind of paper? \ a systems paper: \ a new design, \ measured", HEAD),
              (r"Context", r"what does it build on? \ hash tables \ (Part 17); \ the related work, \ not yet read",
               DATA),
              (r"Correctness", r"do the assumptions look valid? \ from an abstract, \ not yet clear", KERN),
              (r"Contributions", r"what is new? \ one design, \ one speedup", YES),
              (r"Clarity", r"is it well written? \ short, \ but vague in places", LAM)]
        rows = VGroup()
        for t, a, c in cs:
            rows.add(VGroup(label(t, font_size=24, color=c), wrapped_label(a, 5.6, font_size=20, color=WHITE)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(left, RIGHT, buff=0.45)
        rows.set_y(-0.25)
        with self.voiceover(
            "The first pass ends with five questions, which Keshav calls the five Cs. Here is an abstract to try "
            "them on. It is invented, for illustration. <bookmark mark='a'/> Category: what kind of paper is "
            "this? A systems paper: a new design, measured. <bookmark mark='b'/> Context: which other papers and "
            "which theory does it build on? Hash tables, from Part 17, and a related-work section we have not yet "
            "read. <bookmark mark='c'/> Correctness: do the assumptions appear to be valid? From an abstract, you "
            "cannot yet tell. <bookmark mark='d'/> Contributions: what does it add? One design and one speedup. "
            "<bookmark mark='e'/> Clarity: is it well written? Short, but vague in places. After five minutes you "
            "know whether to read on, and what to read for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(title), FadeIn(ill))
            self.play(LaggedStart(*[FadeIn(ln) for ln in lines], lag_ratio=0.3), run_time=2)
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=LEFT * 0.15))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unsaid(self):
        head = label(r"Finding what is not said", font_size=36).to_edge(UP, buff=0.3)
        g, title, lines, ill = abstract(11.0)
        g.scale(1.15)
        g.next_to(head, DOWN, buff=0.3).set_x(-0.6)
        ill.next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        targets = [(lines[3][0], DATA), (lines[3][2], HEAD), (lines[3][3], KERN), (lines[4][1], NO)]
        unders = VGroup(*[Line(m.get_corner(DL) + DOWN * 0.07, m.get_corner(DR) + DOWN * 0.07, color=c,
                               stroke_width=3) for m, c in targets])
        texts = [
            (r"which texts? \ thirty novels are one sample of text, \ not all of it \ (chapter 4)", DATA),
            (rf"how many runs, \ what interval? \ our Job's {len(TIMES)} runs spread {RUN_SPREAD:.0f}\%; \ "
             r"averaged how? \ (chapter 3)", HEAD),
            (rf"which baseline, \ tuned by whom, \ on which machine? \ an unused variable moved our medians "
             rf"{ENV_SPREAD:.1f}\% \ (chapter 2)", KERN),
            (r"how much is little? \ an adjective stands where a number belongs", NO),
            (r"missing entirely: \ limitations, \ threats to validity, \ the code", LAM),
        ]
        cards = VGroup()
        for t, c in texts:
            body = wrapped_label(t, 2.25, font_size=19, color=WHITE)
            r = RoundedRectangle(width=2.55, height=2.7, corner_radius=0.1, stroke_color=c, stroke_width=2,
                                 fill_color=c, fill_opacity=0.08)
            body.move_to(r).align_to(r, UP).shift(DOWN * 0.18)
            cards.add(VGroup(r, body))
        cards.arrange(RIGHT, buff=0.1).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In the second pass, look for what is not said. Read the claim again, phrase by phrase, and ask what "
            "you would need in order to believe it. <bookmark mark='a'/> On thirty novels: which texts? Thirty "
            "novels are one sample of text, and chapter four showed how benchmarks fail. <bookmark mark='b'/> Two "
            "point one times faster: from how many runs, with what interval? Our own Job, run "
            f"{say(len(TIMES))} times on the same text, spread by {say(RUN_SPREAD)} percent. And if there were "
            "several inputs, how was the speedup averaged? <bookmark mark='c'/> Than the standard counter: which "
            "one, tuned by whom, on which machine? In chapter two, an unused environment variable moved our "
            f"medians by {say1(ENV_SPREAD)} percent. <bookmark mark='d'/> Little extra memory: how much is little? "
            "An adjective stands where a number belongs. <bookmark mark='e'/> And notice what is missing "
            "entirely: limitations, threats to validity, the code. When a paper names no weakness of its own, the "
            "reviewer has to find them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ill))
            for mk, u, cd in zip("abcd", unders, cards):
                vo.wait_until(mk)
                self.play(Create(u), FadeIn(cd, shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(cards[4], shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def third(self):
        head = label(r"The third pass: \ re-create the work", font_size=36).to_edge(UP, buff=0.3)
        blocks = [(r"Mytkowicz, \ Diwan, \ Hauswirth, \ Sweeney", 0.34), (r"ASPLOS 2009", 0.28),
                  (r"link order and environment size \\ bias measurements", 0.7), (r"experiments", 0.6),
                  (r"remedy: \ setup randomization", 0.5)]
        paper = page(blocks, width=4.0)
        for b in paper[1]:
            b[0].set_fill(DATA, opacity=0.25)
            b[2].set_color(WHITE)
        paper.to_edge(LEFT, buff=0.5).shift(DOWN * 0.1)
        ours = VGroup(
            label(r"our rebuild \ (chapter 2)", font_size=22, color=YES),
            wrapped_label(rf"one C program, \ {len(B['env'])} environment sizes $\times$ {B['reps']} runs, \ "
                          rf"{len(B['link'])} link orders", 3.6, font_size=18, color=WHITE),
            wrapped_label(rf"medians spread {ENV_SPREAD:.1f}\%: \ within the noise", 3.6, font_size=18,
                          color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        oframe = SurroundingRectangle(ours, buff=0.3, color=YES, stroke_width=1.8, corner_radius=0.1)
        right = VGroup(oframe, ours).to_edge(RIGHT, buff=0.5).match_y(paper)
        qs = VGroup(
            label(r"which program?", font_size=21, color=WHITE),
            label(r"which machine, \ how loaded?", font_size=21, color=WHITE),
            label(r"how many sizes, \ how many runs?", font_size=21, color=WHITE),
            label(r"does the stack start at the same \\ address on every run?", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.4).move_to([(paper.get_right()[0] + right.get_left()[0]) / 2, paper.get_y(), 0])
        a1 = CurvedArrow(paper.get_top() + UP * 0.1, right.get_top() + UP * 0.1, angle=-PI / 6, color=GREY_C,
                         stroke_width=2, tip_length=0.18)
        a1l = label(r"rebuild it", font_size=19, color=GREY_A).next_to(a1, UP, buff=0.05)
        ans = label(r"here: \ no, \ randomized", font_size=21, color=NO).next_to(qs[3], DOWN, buff=0.15)
        foot = wrapped_label(r"the rebuild did not refute the paper: \ it found the paper's own remedy, \ setup "
                             r"randomization, \ already switched on", 12.4, font_size=21, color=WHITE).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "The third pass is the hardest, and the one that teaches most. <bookmark mark='a'/> This part made one "
            "in chapter two, on the 2009 paper by Todd Mytkowicz, Amer Diwan, Matthias Hauswirth and Peter Sweeney: "
            "that link order and the size of the environment bias measurements. <bookmark mark='b'/> Rebuilding "
            "forces every unstated choice into the open. Which program? Which machine, and how busy? How many "
            "sizes, and how many runs? <bookmark mark='c'/> We had to answer each one ourselves, and we found an "
            f"answer: {say(len(B['env']))} sizes, {say(B['reps'])} runs each, a spread of {say1(ENV_SPREAD)} "
            "percent, within the noise. <bookmark mark='d'/> And one question the reading alone would never have "
            "raised: does the stack start at the same address on every run? On this machine it does not. "
            "<bookmark mark='e'/> So the rebuild did not refute the paper. It found the paper's own remedy, setup "
            "randomization, already switched on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(paper))
            vo.wait_until("a")
            self.play(Indicate(paper[1][2], color=DATA))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(q, shift=RIGHT * 0.2) for q in qs[:3]], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(a1), FadeIn(a1l), FadeIn(right))
            vo.wait_until("d")
            self.play(FadeIn(qs[3], shift=RIGHT * 0.2))
            self.play(FadeIn(ans))
            vo.wait_until("e")
            self.play(FadeIn(foot), Indicate(paper[1][4], color=YES))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def review(self):
        head = label(r"Writing a review", font_size=36).to_edge(UP, buff=0.3)
        fields = [
            (r"summary", r"in your own words: \ Skim hashes each word once, \ and reports a 2.1-fold speedup on "
                         r"thirty novels", GREY_A),
            (r"strengths", r"a simple idea; \ a claim that is easy to check", YES),
            (r"weaknesses", r"one benchmark, \ no intervals, \ an unnamed baseline, \ memory not measured: \ "
                            r"\textit{each could be fixed, \ and the review says how}", NO),
            (r"questions", r"how many runs, \ on which machine? \ will the code be released?", DATA),
            (r"verdict", r"not yet: \ accept with intervals, \ a second benchmark and a named baseline; \ "
                         r"confidence: \ high", HEAD),
        ]
        rows = VGroup()
        for t, body, c in fields:
            rows.add(VGroup(label(t, font_size=24, color=c), wrapped_label(body, 9.4, font_size=21, color=WHITE)))
        for r in rows:
            r[0].move_to([-6.6, 0, 0], aligned_edge=LEFT)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.62).next_to(head, DOWN, buff=0.6)
        for r in rows:
            r[0].set_x(-6.6 + r[0].width / 2)
            r[1].set_x(-3.7 + r[1].width / 2).align_to(r[0], UP)
        rules = VGroup(*[Line([-6.6, r.get_bottom()[1] - 0.2, 0], [6.6, r.get_bottom()[1] - 0.2, 0], color=GREY_D,
                              stroke_width=1) for r in rows[:-1]])
        ill = note(r"illustrative: \ a review of the invented paper", font_size=16).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Reviewing is reading with a duty attached. Most review forms ask for the same few things. "
            "<bookmark mark='a'/> First a summary, in your own words, so that the authors can see you understood "
            "them. <bookmark mark='b'/> Then the strengths: say what is good, and mean it. <bookmark mark='c'/> "
            "Then the weaknesses, and here the craft is to separate what is fatal from what can be fixed, and for "
            "each fixable flaw, to say what would fix it. Judge the paper that was submitted, not the one you "
            "would have written. <bookmark mark='d'/> Then questions the authors can answer. <bookmark mark='e'/> "
            "And a verdict, with your confidence in it. A review is confidential, and it is written to a person: "
            "specific, courteous and checkable. Alan Jay Smith's guide for referees, The Task of the Referee, "
            "from 1990, is still worth reading."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            for mk, r, i in zip("abcde", rows, range(5)):
                vo.wait_until(mk)
                anims = [FadeIn(r[0], shift=RIGHT * 0.15), FadeIn(r[1])]
                if i:
                    anims.append(Create(rules[i - 1]))
                self.play(*anims)
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, YES)
