from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403

INK = {"RED": "#EF6F6C", "GREEN": "#5BD18B", "BLUE": "#7EC8F5", "YELLOW": "#F2C14E"}


class Control(VoiceoverScene):
    def construct(self):
        self.card()
        self.stroop_demo()
        self.stroop_model()
        self.monitoring()
        self.switching()

    def card(self):
        card = chapter_card(8, r"Control and conflict", r"Why is it hard to name the ink of a word?",
                            lit={1935: r"Stroop", 1974: r"Eriksen \& Eriksen", 2001: r"Botvinick et al."}, part=PART,
                            scale=("mind", "brain"), marr=("what", "how"))
        with self.voiceover("Chapter eight. Control and conflict."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def stroop_demo(self):
        p = archive.STROOP_1935.data
        head = heading(r"On you: \ name the ink, \ not the word")
        neutral = VGroup(*[label(r"XXXX", font_size=40, color=c) for c in ("#5BD18B", "#EF6F6C", "#7EC8F5",
                                                                             "#F2C14E", "#EF6F6C", "#7EC8F5")])
        conf = VGroup(*[label(w, font_size=40, color=INK[c]) for w, c in (("RED", "GREEN"), ("BLUE", "YELLOW"),
                                                                            ("GREEN", "RED"), ("YELLOW", "BLUE"),
                                                                            ("RED", "BLUE"), ("GREEN", "YELLOW"))])
        neutral.arrange_in_grid(rows=2, buff=(0.6, 0.35)).move_to([-3.4, 1.4, 0])
        conf.arrange_in_grid(rows=2, buff=(0.6, 0.35)).move_to([3.4, 1.4, 0])
        nl = label(r"name these inks", font_size=22, color=GREY_A).next_to(neutral, UP, buff=0.25)
        cl = label(r"now these", font_size=22, color=GREY_A).next_to(conf, UP, buff=0.25)
        rows = rows_of([
            (r"1935: \ John Ridley Stroop times people naming the inks of 100 items", WHITE),
            (rf"colour words in clashing inks took about {p['extra_seconds']:.0f} s longer than coloured squares: \ "
             rf"{p['extra_percent']:.0f}\% more", CONFLICT),
            (r"reading the words aloud, \ ignoring the ink, \ barely slowed at all", CUE),
            (r"MacLeod, \ 1991: \ over 700 studies; \ among the most reliable effects in psychology", DATA),
        ], 12.4, 26, 0.3).to_edge(DOWN, buff=0.75)
        tag = historical_tag(archive.STROOP_1935.cite)
        with self.voiceover(
            "Try naming the colours of the inks on the left, out loud if you can. <bookmark mark='a'/> Easy. Now the "
            "ones on the right: name the ink, not the word. <bookmark mark='b'/> You probably slowed down, and maybe "
            "started to say a word before catching it. In 1935 John Ridley Stroop timed people naming the ink "
            "colours of a hundred items. <bookmark mark='c'/> When the items were colour words printed in clashing "
            "inks, naming took about forty-seven seconds longer than for coloured squares, seventy-four percent "
            "more. <bookmark mark='d'/> When the task was reversed, read the word and ignore the ink, the ink barely "
            "mattered. <bookmark mark='e'/> By 1991 Colin MacLeod could review more than seven hundred studies of the "
            "effect. It is among the most reliable findings in all of psychology."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(neutral), FadeIn(nl))
            vo.wait_until("a")
            self.play(FadeIn(conf), FadeIn(cl))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def stroop_model(self):
        d = load("stroop")
        head = heading(r"Two pathways, \ one response")
        eq = MathTex(r"v", r"=", r"v_{\text{ink}}", r"\pm", r"(1 - c)\, v_{\text{word}}", font_size=40)
        eq[0].set_color(ATT)
        eq[2].set_color(CUE)
        eq[4].set_color(CONFLICT)
        eq.move_to([-3.4, 2.2, 0])
        rows = rows_of([
            (r"evidence for the ink's name accumulates to a bound: \ a diffusion, \ built in full in Part 25", WHITE),
            (r"the word pathway is faster and stronger; \ control $c$ damps it, \ not to zero", CONFLICT),
            (r"congruent: \ it helps; \ incongruent: \ it pushes the wrong way", ATT),
            (r"interference is larger than facilitation, \ because time goes as one over the drift", MODEL),
            (r"and it grows over the slow end of the distribution", GREY_A),
        ], 6.2, 24, 0.38).move_to([-3.3, -0.65, 0])
        A = axes([0, 3], [400, 800], x_length=4.4, y_length=2.1, xticks=[], yticks=[400, 600, 800],
                 ylabel=r"mean RT, \ ms", center=[3.6, 1.55, 0], font_size=16)
        ax = A.ax
        bars, labs = VGroup(), VGroup()
        for k, (cond, col) in enumerate([("congruent", GOOD), ("neutral", GREY_B), ("incongruent", BAD)]):
            for j, (task, alpha) in enumerate([("colour", 0.9), ("word", 0.35)]):
                v = d[f"{task}_{cond}"]
                x = k + 0.5 + (j - 0.5) * 0.36
                lo, hi = ax.c2p(x, 400), ax.c2p(x, v)
                bars.add(Rectangle(width=0.32, height=hi[1] - lo[1], stroke_width=0, fill_color=col,
                                   fill_opacity=alpha).move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
            labs.add(label(cond, font_size=16, color=col).next_to(ax.c2p(k + 0.5, 400), DOWN, buff=0.12))
        key = label(r"solid: \ name the ink; \ faint: \ read the word", font_size=16, color=GREY_A)
        key.next_to(ax.c2p(0, 800), RIGHT, buff=0.15).shift(DOWN * 0.12)
        B = axes([450, 1150], [0, 600], x_length=4.4, y_length=1.7, xticks=[500, 800, 1100], yticks=[0, 300, 600],
                 xlabel=r"RT quantile, \ ms", ylabel=r"incongruent $-$ congruent", center=[3.6, -1.75, 0], font_size=16)
        dc = VGroup(curve(B.ax, d["dx"], d["dy"], CONFLICT, 4), scatter(B.ax, d["dx"], d["dy"], CONFLICT, 0.06, 1))
        ptag = psyche_tag(r"\texttt{attention.stroop}: \ $v_{\text{ink}} = 2.5$, \ $v_{\text{word}} = 3$, \ $c = 0.6$")
        tag = published_tag(archive.STROOP_1935.cite)
        with self.voiceover(
            "A simple model captures the main facts. <bookmark mark='a'/> Naming the ink is a decision: evidence "
            "for each colour name accumulates until one reaches a bound, a diffusion; Part 25 builds that model in "
            "full. "
            "<bookmark mark='b'/> Two pathways feed it. The ink pathway is the one you're asked to use. The word "
            "pathway is faster and stronger, because reading is overlearned, and control can damp it but not shut it "
            "off. <bookmark mark='c'/> When word and ink agree, the word adds to the drift; when they clash, it "
            "subtracts. <bookmark mark='d'/> Because the time to a bound goes roughly as one over the drift, taking "
            "drift away costs more than adding it saves: interference is larger than facilitation, as in the data. "
            "Reverse the task, read the word, and the weak ink pathway barely moves anything. "
            "<bookmark mark='e'/> The model also predicts that interference grows across the response-time "
            "distribution, largest on the slowest trials, which is what delta plots of real Stroop data show."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "d":
                    self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1),
                              FadeIn(labs), FadeIn(key), FadeIn(ptag), run_time=2.0)
                if m == "e":
                    self.play(FadeIn(B), Create(dc), run_time=1.5)
        self.clear_scene()

    def monitoring(self):
        d = load("stroop")
        head = heading(r"Conflict calls for control")
        flank = VGroup(label(r"$>>>>>$", font_size=48, color=GOOD), label(r"$<<><<$", font_size=48, color=BAD))
        flank.arrange(DOWN, buff=0.3).move_to([-3.8, 1.6, 0])
        fl = wrapped_label(r"the flanker task: \ which way does the middle one point?", 4.2, 19, GREY_A)
        fl.next_to(flank, DOWN, buff=0.2)
        A = axes([0, 2], [0, 320], x_length=4.2, y_length=2.6, xticks=[], yticks=[0, 150, 300],
                 ylabel=r"incongruent $-$ congruent, \ ms", center=[3.4, 1.3, 0], font_size=16)
        ax = A.ax
        bars = VGroup()
        for k, (pc, col, name) in enumerate([("congruent", GREY_B, r"after a congruent trial"),
                                             ("incongruent", CONTROL, r"after an incongruent trial")]):
            v = d[f"seq_{pc}_incongruent"] - d[f"seq_{pc}_congruent"]
            lo, hi = ax.c2p(k + 0.5, 0), ax.c2p(k + 0.5, v)
            bars.add(VGroup(Rectangle(width=0.9, height=hi[1] - lo[1], stroke_width=0, fill_color=col,
                                      fill_opacity=0.85).move_to([lo[0], (lo[1] + hi[1]) / 2, 0]),
                            wrapped_label(name, 1.7, 16, col).next_to(lo, DOWN, buff=0.12),
                            label(rf"{v:.0f}", font_size=18, color=col).next_to(hi, UP, buff=0.06)))
        rows = rows_of([
            (r"1974: \ Eriksen and Eriksen: \ flanking letters that call for the other response slow you down", WHITE),
            (r"conflict: \ two responses active at once; \ the anterior cingulate cortex responds to it", CONFLICT),
            (r"Botvinick and colleagues, \ 2001: \ conflict is a signal to turn control up", CONTROL),
            (r"so interference is smaller right after an incongruent trial: \ the congruency sequence effect", MODEL),
        ], 12.4, 25, 0.28).to_edge(DOWN, buff=0.75)
        ptag = psyche_tag(r"\texttt{attention.stroop\_sequence}: \ control rises 0.25 after conflict, \ then relaxes")
        tag = historical_tag(archive.BOTVINICK_2001.cite)
        with self.voiceover(
            "Stroop has a cousin with no words in it. <bookmark mark='a'/> In 1974 Barbara and Charles Eriksen asked "
            "people to respond to a central letter flanked by others. Flankers that called for the other response "
            "slowed people down, though they were told to ignore them. Today the task is usually arrows. "
            "<bookmark mark='b'/> In both tasks, two responses are active at once: conflict. A region on the "
            "brain's midline, the anterior cingulate cortex, responds strongly on such trials. "
            "<bookmark mark='c'/> In 2001 Matthew Botvinick, Jonathan Cohen and colleagues proposed that the region "
            "monitors conflict, and that conflict is a signal to turn control up for what comes next. "
            "<bookmark mark='d'/> That predicts a sequence effect: right after a conflict trial, control is high, so "
            "the word or the flankers interfere less. Psyche, with control that rises after conflict and relaxes "
            "after, shows it, and so do people: it was first reported by Gabriele Gratton and colleagues in 1992. "
            "How much of it is control, and how much is memory for the previous trial's features, is still argued."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(flank), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(A), FadeIn(ptag), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.5), FadeIn(rows[3]),
                      run_time=2.0)
        self.clear_scene()

    def switching(self):
        d = load("switch")
        head = heading(r"Switching tasks costs time")
        seq = VGroup()
        for k, (t, col) in enumerate(zip("AABBAABB", [CUE, CUE, ATT, ATT] * 2)):
            sq = Square(0.62, color=col, stroke_width=3)
            seq.add(VGroup(sq, label(t, font_size=26, color=col).move_to(sq)))
        seq.arrange(RIGHT, buff=0.12).move_to([-3.2, 1.9, 0])
        sl = label(r"A: \ odd or even?  \ B: \ vowel or consonant?", font_size=19, color=GREY_A).next_to(seq, DOWN,
                                                                                                         buff=0.15)
        marks = VGroup(*[label(r"switch", font_size=16, color=BAD).next_to(seq[k], UP, buff=0.08) for k in (2, 4, 6)])
        A = axes([0, 1500], [0, 220], x_length=5.0, y_length=2.5, xticks=[0, 500, 1000, 1500], yticks=[0, 100, 200],
                 xlabel=r"time to prepare, \ ms", ylabel=r"switch cost, \ ms", center=[3.4, 1.1, 0], font_size=16)
        ax = A.ax
        c = curve(ax, d["rsi"], d["cost"], CONTROL, 4)
        res = DashedLine(ax.c2p(0, 80), ax.c2p(1500, 80), color=GREY_C, stroke_width=1.5)
        rl = label(r"the residual cost", font_size=17, color=GREY_B).next_to(ax.c2p(1500, 80), DOWN, buff=0.08).align_to(
            ax.c2p(1500, 80), RIGHT)
        rows = rows_of([
            (r"1995: \ Rogers and Monsell: \ predictable runs, \ AABB, \ two tasks on the same characters", WHITE),
            (r"the first trial after a switch is slower than a repeat", BAD),
            (r"time to prepare shrinks the cost: \ part of the switch can be done in advance", CONTROL),
            (r"part cannot: \ a residual cost that preparation never removes", GREY_A),
        ], 12.4, 25, 0.28).to_edge(DOWN, buff=0.75)
        ptag = psyche_tag(r"\texttt{attention.switch\_cost}: \ the pattern; \ the numbers are Psyche's")
        tag = historical_tag(archive.ROGERS_MONSELL_1995.cite)
        with self.voiceover(
            "Control also has to change tasks. <bookmark mark='a'/> In 1995 Robert Rogers and Stephen Monsell had "
            "people alternate between two tasks on the same displays, a digit and a letter: in one, judge whether the "
            "digit is odd or even, in the other whether the letter is a vowel, in predictable runs of two. "
            "<bookmark mark='b'/> The first trial after a switch was reliably slower than a repeat, even though "
            "people knew exactly when the switch was coming. <bookmark mark='c'/> Giving them more time before the "
            "switch shrank the cost: part of reconfiguring for the new task can be done in advance. "
            "<bookmark mark='d'/> But part could not. A residual cost remained however long they had, as if the last "
            "step of the switch only happens when the new stimulus arrives. The numbers here are Psyche's; the "
            "shape is theirs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(seq), FadeIn(sl), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(marks), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(res), FadeIn(rl), FadeIn(rows[3]))
        self.clear_scene()
