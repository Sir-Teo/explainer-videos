from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Systems(VoiceoverScene):
    def construct(self):
        self.card()
        self.bat()
        self.story_()
        self.one_process()

    def card(self):
        card = chapter_card(11, r"Two systems?", r"Is there a fast mind and a slow one?",
                            lit={2000: r"Stanovich \& West", 2005: r"Frederick", 2011: r"Kahneman",
                                 2013: r"Evans \& Stanovich"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter eleven. Two systems?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def bat(self):
        stage = demo_stage(12.4, 4.6, center=[0, 0.4, 0])
        q = wrapped_label(r"A bat and a ball cost \$1.10 in total. \ The bat costs \$1.00 more than the ball. \ How "
                          r"much does the ball cost?", 11.0, 30, WHITE).move_to([0, 0.9, 0])
        fast = label(r"the answer that comes first: \ 10 cents", font_size=27, color=HEUR).move_to([0, -0.3, 0])
        check = MathTex(r"b + (b + 1.00) = 1.10 \;\Rightarrow\; b = 0.05", font_size=38, color=NORM).move_to(
            [0, -1.2, 0])
        foot = wrapped_label(r"Frederick, \ 2005: \ the Cognitive Reflection Test; \ many students at selective "
                             r"universities gave the intuitive answer", 12.0, 23, GREY_A).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "One more on you. <bookmark mark='a'/> A bat and a ball cost a dollar ten in total. The bat costs a "
            "dollar more than the ball. How much does the ball cost?"
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(q))
        self.wait(3.0)
        with self.voiceover(
            "If ten cents came to mind, you're in large company. <bookmark mark='a'/> But then the bat would cost a "
            "dollar ten, and the two together a dollar twenty. The ball costs five cents. <bookmark mark='b'/> Shane "
            "Frederick made this the first item of his Cognitive Reflection Test in 2005, and found the intuitive "
            "answer common even among students at highly selective universities. Getting it right means noticing "
            "the first answer, and checking it."
        ) as vo:
            self.play(FadeIn(fast))
            vo.wait_until("a")
            self.play(Write(check))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def story_(self):
        head = heading(r"System 1 and System 2")
        s1 = VGroup(label(r"System 1", font_size=30, color=HEUR),
                    wrapped_label(r"fast, \ automatic, \ effortless, \ associative; \ the answer that comes", 4.8, 23,
                                  WHITE)).arrange(DOWN, buff=0.2)
        s2 = VGroup(label(r"System 2", font_size=30, color=NORM),
                    wrapped_label(r"slow, \ deliberate, \ effortful, \ rule-based; \ the check, \ when it runs", 4.8,
                                  23, WHITE)).arrange(DOWN, buff=0.2)
        VGroup(s1, s2).arrange(RIGHT, buff=1.5).move_to([0, 1.3, 0])
        rows = rows_of([
            (r"Stanovich and West, \ 2000, \ named them; \ Kahneman's \emph{Thinking, \ Fast and Slow}, \ 2011, "
             r"\ made them famous", WHITE),
            (r"default-interventionist: \ System 1 proposes, \ System 2 sometimes intervenes \ (Evans and Stanovich, "
             r"\ 2013)", MODEL),
            (r"the evidence: \ time pressure and memory load push answers toward the intuitive; \ some people, \ "
             r"and some moods, \ check more", GREY_A),
            (r"the critics: \ the lists of features do not line up; \ one process with a quick default may do as "
             r"well \ (Keren and Schul, \ 2009; \ Kruglanski and Gigerenzer, \ 2011)", LOSS),
        ], 12.0, 23, 0.3).move_to([0, -1.5, 0])
        tag = published_tag(r"Stanovich \& West (2000); \ Evans \& Stanovich (2013); \ Kruglanski \& Gigerenzer "
                            r"(2011)")
        with self.voiceover(
            "The bat and the ball is the poster child of a popular idea. <bookmark mark='a'/> Two kinds of "
            "thinking: System 1, fast, automatic, effortless and associative, which produces the answer that comes; "
            "and System 2, slow, deliberate and effortful, which checks it, when it runs. Keith Stanovich and "
            "Richard West named them in 2000, and Kahneman's book Thinking, Fast and Slow made them famous in "
            "2011. <bookmark mark='b'/> In the most developed version, from Jonathan Evans and Stanovich, System 1 "
            "proposes a default and System 2 sometimes intervenes. <bookmark mark='c'/> There's evidence for the "
            "pattern: time pressure and a load on working memory push answers toward the intuitive one, and some "
            "people check more than others. <bookmark mark='d'/> And there are critics. The features said to go "
            "together, fast with automatic with associative, often come apart. And a single process that starts "
            "near a quick default may produce the same signatures. Gideon Keren and Yaacov Schul made the case in "
            "2009, and Arie Kruglanski and Gigerenzer in 2011."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(s1), FadeIn(s2), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def one_process(self):
        d = load("systems")
        head = heading(r"One process, \ two systems' signature")
        A = axes([-0.5, 4.5], [0, 1], x_length=5.6, y_length=3.8, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"share of answers that are the checked one",
                 center=[-3.3, -0.2, 0], font_size=16)
        xs = np.arange(5)
        bs = bars(A.ax, xs, d["p_reflective"], NORM, width=0.6)
        names = VGroup(*[label(rf"{m:.2f} s", font_size=16, color=GREY_A).next_to(A.ax.c2p(x, 0), DOWN, buff=0.15)
                         for x, m in zip(xs, d["rt_mid"])])
        xl = label(r"fifths of the response times, \ fastest to slowest \ (median of each)", font_size=17,
                   color=GREY_A).next_to(names, DOWN, buff=0.15)
        rows = rows_of([
            (r"Psyche's diffusion model from Part 25, \ started a quarter of the way up, \ near the intuitive "
             r"answer, \ with the evidence favouring the checked one", MODEL),
            (rf"the fastest fifth: \ {100 * d['fast_intuitive']:.0f}\% intuitive; \ the slowest: \ "
             rf"{100 * d['slow_reflective']:.0f}\% checked", NORM),
            (r"fast answers intuitive, \ slow answers reflective, \ time pressure favouring intuition: \ all from one "
             r"accumulator with a biased start", HEUR),
            (r"so the signature alone does not prove two systems; \ the architecture is still argued over", LOSS),
        ], 5.6, 22, 0.3).move_to([3.5, 0.0, 0])
        tag = psyche_tag(rf"\texttt{{decide.simulate}}: \ $v = {d['v']}$, \ $a = {d['a']}$, \ start $= {d['w']}a$; "
                         r"\ 40{,}000 trials")
        with self.voiceover(
            "Psyche can make the critics' point concrete. <bookmark mark='a'/> Take the diffusion model from the "
            "last part, a single accumulator. Start it a quarter of the way up, near the bound for the intuitive "
            "answer, and let the evidence drift, on average, toward the checked answer. <bookmark mark='b'/> Now "
            "sort its responses by time. In the fastest fifth, "
            f"{100 * d['fast_intuitive']:.0f} percent of answers are the intuitive one. In the slowest fifth, "
            f"{100 * d['slow_reflective']:.0f} percent are the checked one. <bookmark mark='c'/> Fast answers "
            "intuitive, slow answers reflective, and anything that hurries the process favours intuition: the "
            "classic signature of two systems, produced by one. <bookmark mark='d'/> That doesn't settle the "
            "question; it shows that this signature alone can't. Whether the mind has two systems, or one with a "
            "quick default, is still argued over."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bs], lag_ratio=0.3), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
