from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


class Production(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.latency()
        self.protocols()

    def card(self):
        card = chapter_card(5, r"Production systems", r"Can a list of if-then rules think?",
                            lit={1972: r"Newell \& Simon", 1980: r"Ericsson \& Simon", 1993: r"Anderson"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter five. Production systems."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rules(self):
        head = heading(r"Thinking as rules that fire")
        rules = [
            (r"IF \ the goal is to move disc $d$ to peg $g$ \ AND \ a smaller disc is in the way", SEARCH,
             r"THEN \ push a subgoal: \ move the smaller discs to the other peg"),
            (r"IF \ the goal is to move disc $d$ to peg $g$ \ AND \ nothing is in the way", MODEL,
             r"THEN \ move $d$ to $g$, \ and pop the goal"),
            (r"IF \ the goal is done", GREY_A, r"THEN \ return to the goal beneath it on the stack"),
        ]
        rows = VGroup()
        for cond, col, act in rules:
            rows.add(VGroup(label(cond, font_size=25, color=col), label(act, font_size=25, color=WHITE)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=0.5).set_y(1.0)
        goals = [(r"move disc 3 to C", GREY_A), (r"move disc 2 to B", SEARCH), (r"move disc 1 to C", MODEL)]
        stack = VGroup()
        for k, (g, c) in enumerate(goals):
            b = RoundedRectangle(corner_radius=0.08, width=3.0, height=0.55, stroke_color=c, stroke_width=2,
                                 fill_color=c, fill_opacity=0.12).move_to([4.7, 0.0 + 0.65 * k, 0])
            stack.add(VGroup(b, label(g, font_size=21, color=c).move_to(b)))
        st = label(r"the goal stack, \ three discs", font_size=20, color=GREY_B).next_to(stack, UP, buff=0.2)
        base = Line([3.1, -0.35, 0], [6.3, -0.35, 0], color=GREY_B, stroke_width=2)
        push = wrapped_label(r"pushed when a smaller disc is in the way; \ the top one acts first", 3.4, 18,
                             GREY_B).next_to(base, DOWN, buff=0.15)
        notes = rows_of([
            (r"a production system: \ a working memory of goals and facts, \ and rules that match it; \ one rule "
             r"fires at a time", WHITE),
            (r"ACT-R \ (Anderson, \ 1993 to now): \ declarative and procedural memory, \ one rule fires in about "
             r"50 ms; \ models predict times, \ errors, \ and brain activity", LOGIC),
        ], 12.6, 24, 0.32).to_edge(DOWN, buff=0.9)
        tag = published_tag(r"Newell \& Simon (1972); \ Anderson (1993)")
        with self.voiceover(
            "Newell and Simon's programs were written as productions: if-then rules that watch a working memory "
            "and fire when their conditions match. <bookmark mark='a'/> Here's a whole strategy for the tower in "
            "three rules. If the goal is to move a disc and a smaller disc is in the way, push a subgoal: move the "
            "smaller discs to the other peg. If nothing is in the way, move the disc and drop the goal. And when a "
            "goal is done, go back to the one beneath it. <bookmark mark='b'/> A production system is just that: a "
            "memory of goals and facts, and rules that fire one at a time. <bookmark mark='c'/> John Anderson's ACT-R "
            "grew from this idea into a theory of the whole mind, with a declarative memory, a procedural memory, and "
            "rules that fire about every fifty milliseconds. Its models predict times, errors, and even brain "
            "activity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(st), FadeIn(base), FadeIn(stack[0]))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=1.0),
                      LaggedStart(FadeIn(stack[1], shift=DOWN * 0.2), FadeIn(stack[2], shift=DOWN * 0.2),
                                  FadeIn(push), lag_ratio=1.0), run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.clear_scene()

    def latency(self):
        d = load("hanoi")
        head = heading(r"Where the rules predict a pause")
        lat = d["latency4"]
        A = axes([0, 16], [0, 6], x_length=7.4, y_length=3.0, xticks=[1, 5, 9, 13, 15], yticks=[0, 2, 4, 6],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"move", ylabel=r"time, \ arbitrary units",
                 center=[-2.3, 0.6, 0], font_size=16)
        bs = VGroup(*[bars(A.ax, [k + 1], [v], SEARCH if v > 1.01 else GREY_B, 0.7) for k, v in enumerate(lat)])
        big = int(np.argmax(lat))
        assert big == 0 and lat[8] > lat[4] > 1  # first move longest; then move 9; then moves 5 and 13
        rows = rows_of([
            (r"four discs, \ fifteen moves: \ each move costs one unit, \ each subgoal set up before it, \ one and "
             r"a half more", WHITE),
            (r"long pauses before move 1, \ then 9, \ then 5 and 13: \ where a new tower of subgoals is built", SEARCH),
            (r"Anderson \& Douglass, \ 2001: \ people's move times on fifteen-move problems depended on setting and "
             r"retrieving goals, \ retrieval most of all", DATA),
        ], 4.6, 23, 0.36).move_to([4.4, 0.3, 0])
        tag = psyche_tag(r"\texttt{reason.goal\_stack\_solver}; \ Anderson \& Douglass (2001)")
        with self.voiceover(
            "Rules like these make a prediction about time. <bookmark mark='a'/> Suppose each move costs one unit "
            "of time, and each subgoal set up before it costs one and a half more. With four discs, Psyche's goal "
            "stack solves the tower in fifteen moves. <bookmark mark='b'/> The pauses aren't even. The longest comes "
            "before the first move, where the whole tower of subgoals is built, then before the ninth, then before "
            "the fifth and the thirteenth. <bookmark mark='c'/> In 2001 John Anderson and Scott Douglass found that "
            "people's move times on fifteen-move problems depended on setting up and retrieving goals, retrieval "
            "most of all. The structure of the plan shows up in the clock."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bs], lag_ratio=0.15), FadeIn(rows[0]),
                      run_time=3)
            vo.wait_until("b")
            self.play(Indicate(bs[0], color=WHITE), Indicate(bs[8], color=WHITE), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def protocols(self):
        head = heading(r"Thinking aloud as data")
        quote = VGroup(
            label(r"``\ldots the big one has to go to C, \ so the little one", font_size=28, color=CONTENT),
            label(r"has to get out of the way first, \ to B? \ No, \ to C\ldots''", font_size=28, color=CONTENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0, 1.8, 0])
        ql = label(r"an illustration of a think-aloud protocol, \ not a recorded one", font_size=19, color=GREY_B
                   ).next_to(quote, DOWN, buff=0.15)
        rows = rows_of([
            (r"Ericsson \& Simon, \ 1980 and 1993: \ ask people only to say what they are attending to, \ and "
             r"thinking aloud barely changes the thinking", WHITE),
            (r"ask them to explain why, \ and it does: \ it slows them, \ and changes what they do", LOST),
            (r"a protocol shows the sequence of states a solver visits, \ which a model must then reproduce", MODEL),
            (r"what it cannot show: \ processes too fast or too automatic to put into words", GREY_A),
        ], 12.6, 25, 0.34).move_to([0, -1.3, 0])
        tag = published_tag(r"Ericsson \& Simon (1980, \ 1993)")
        with self.voiceover(
            "How do you check that a model searches the way a person does? Ask the person to think aloud. "
            "<bookmark mark='a'/> In 1980 Anders Ericsson and Herbert Simon argued that if people are asked only to "
            "say what they're attending to, speaking barely changes the thinking. <bookmark mark='b'/> Ask them to "
            "explain why they're doing it, and it does: they slow down, and change what they do. "
            "<bookmark mark='c'/> A protocol gives the sequence of states a solver passes through, and a model must "
            "reproduce it. <bookmark mark='d'/> What a protocol can't show are the processes too fast or too "
            "automatic to put into words, which, as the next chapter shows, may be where the hardest problems are "
            "solved."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(quote), FadeIn(ql))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
