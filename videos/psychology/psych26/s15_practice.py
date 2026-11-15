from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.defaults()
        self.pensions()
        self.risk()

    def card(self):
        card = chapter_card(14, r"In practice: \ defaults, \ pensions and risk", r"Where does the psychology of "
                            r"choice change outcomes?",
                            lit={1988: r"Levin \& Gaeth", 2003: r"Johnson \& Goldstein", 2004: r"Thaler \& Benartzi"},
                            part=PART, scale=("mind", "society"), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: defaults, pensions and risk."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def defaults(self):
        head = heading(r"The power of the default")
        A = axes([-0.5, 1.5], [0, 100], x_length=4.4, y_length=3.6, xticks=None, yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"effective consent to organ donation",
                 center=[-3.6, -0.3, 0], font_size=16)
        b = VGroup(bars(A.ax, [0], [12.0], LOSS, width=0.6), bars(A.ax, [1], [99.98], GAIN, width=0.6))
        names = VGroup(label(r"Germany: \ opt in", font_size=18, color=LOSS).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       label(r"Austria: \ opt out", font_size=18, color=GAIN).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                      buff=0.15))
        vals = VGroup(label(r"12\%", font_size=20).next_to(A.ax.c2p(0, 12), UP, buff=0.08),
                      label(r"99.98\%", font_size=20).next_to(A.ax.c2p(1, 99.98), UP, buff=0.08))
        rows = rows_of([
            (r"Johnson and Goldstein, \ 2003: \ neighbours with similar cultures, \ different defaults", WHITE),
            (r"why defaults work: \ inertia, \ an implied recommendation, \ and the reference point they set, \ "
             r"so that leaving feels like a loss", MODEL),
            (r"consent is not donation: \ actual donation rates differ much less, \ since families and hospitals "
             r"decide too", LOSS),
            (r"framing in labels: \ beef described as 75\% lean is rated better than beef described as 25\% fat "
             r"\ (Levin and Gaeth, \ 1988)", RISKY),
        ], 6.2, 22, 0.3).move_to([3.2, -0.1, 0])
        tag = published_tag(r"Johnson \& Goldstein (2003); \ Levin \& Gaeth (1988)")
        with self.voiceover(
            "The ideas of this part have left the laboratory. The most powerful is the default. "
            "<bookmark mark='a'/> In 2003 Eric Johnson and Daniel Goldstein compared European countries' consent "
            "to organ donation. In Germany, where you must opt in, about twelve percent had consented. In "
            "neighbouring Austria, where you must opt out, nearly everyone counted as a donor. "
            "<bookmark mark='b'/> Defaults work through inertia, through the recommendation they seem to imply, and "
            "through the reference point they set: once a default is yours, leaving it feels like a loss. "
            "<bookmark mark='c'/> A caution: consent isn't donation. Families and hospitals decide too, and actual "
            "donation rates differ far less than these bars. <bookmark mark='d'/> Framing works in labels as well. "
            "Irwin Levin and Gary Gaeth found in 1988 that beef described as seventy-five percent lean was rated "
            "better, even after tasting, than the same beef described as twenty-five percent fat."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(b), FadeIn(vals), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def pensions(self):
        head = heading(r"Save More Tomorrow")
        A = axes([0, 4], [0, 15], x_length=5.0, y_length=3.4, xticks=[0, 1, 2, 3, 4], yticks=[0, 5, 10, 15],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}\\%", xlabel=r"pay rises since joining",
                 ylabel=r"share of pay saved", center=[-3.5, -0.3, 0], font_size=16)
        steps = curve(A.ax, [0, 0, 1, 1, 2, 2, 3, 3, 4], [3.5, 3.5, 6.5, 6.5, 9.4, 9.4, 11.6, 11.6, 13.6], TIME, 4)
        start = label(r"3.5\%", font_size=20, color=TIME).next_to(A.ax.c2p(0, 3.5), UR, buff=0.08)
        end = label(r"13.6\%", font_size=20, color=TIME).next_to(A.ax.c2p(4, 13.6), UL, buff=0.08)
        rows = rows_of([
            (r"Thaler and Benartzi, \ 2004: \ commit now to save more \emph{later}, \ out of future pay rises", WHITE),
            (r"present bias: \ the cost falls on a future self; \ loss aversion: \ take-home pay never falls; \ "
             r"inertia: \ once in, \ people stay in", MODEL),
            (r"in the first company, \ savings rates of those who joined rose from 3.5\% to 13.6\% over four pay "
             r"rises", TIME),
            (r"automatic enrolment, \ the same idea as a default, \ is now law in several countries", GAIN),
        ], 5.6, 22, 0.3).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Thaler \& Benartzi (2004)")
        with self.voiceover(
            "Pensions are where present bias and loss aversion cost the most. <bookmark mark='a'/> In 2004 Richard "
            "Thaler and Shlomo Benartzi reported a plan called Save More Tomorrow. Employees committed now to save "
            "more later, out of future pay rises. <bookmark mark='b'/> It turns three biases to advantage. The "
            "cost falls on a future self, whom a present-biased person is happy to commit. Take-home pay never "
            "falls, so there's no loss to feel. And inertia keeps people in. <bookmark mark='c'/> In the first "
            "company to use it, the saving rate of those who joined rose from three and a half percent to over "
            "thirteen percent across four pay rises. These are the participants, who chose to join, not a "
            "randomized comparison. <bookmark mark='d'/> Automatic enrolment in pensions, the same idea as a "
            "default, is now law in several countries; Part 55 looks at how such policies are evaluated."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(steps), FadeIn(start), FadeIn(end), FadeIn(rows[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def risk(self):
        d = load("bayes")
        head = heading(r"Communicating risk")
        left = VGroup(label(r"relative risk", font_size=26, color=LOSS),
                      label(r"``doubles your risk''", font_size=30, color=WHITE),
                      label(r"``halves your risk''", font_size=30, color=WHITE)).arrange(DOWN, buff=0.3)
        right = VGroup(label(r"absolute risk", font_size=26, color=GAIN),
                       label(r"from 1 in 7{,}000 to 2 in 7{,}000", font_size=26, color=WHITE),
                       label(r"from 2 in 1{,}000 to 1 in 1{,}000", font_size=26, color=WHITE)).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=1.6).move_to([0, 1.4, 0])
        rows = rows_of([
            (r"the same change can sound alarming or trivial; \ relative risks without baselines mislead patients "
             r"and doctors alike", WHITE),
            (r"the 1995 pill scare in Britain: \ a doubling from a tiny baseline, \ reported as a doubling, \ was "
             r"followed by a rise in unwanted pregnancies and abortions", LOSS),
            (rf"natural frequencies and icon arrays help: \ 8 of the 103 women who test positive have cancer, \ "
             rf"about {100 * d['mam']:.0f}\%", NORM),
            (r"medical guidelines now ask for absolute risks, \ in frequencies, \ with the same denominator", GAIN),
        ], 12.0, 23, 0.3).move_to([0, -1.6, 0])
        tag = published_tag(r"Gigerenzer et al.\ (2007); \ Furedi (1999)")
        with self.voiceover(
            "Last, risk communication, where framing can do harm. <bookmark mark='a'/> A drug that halves your "
            "risk, or a risk that doubles: the same change can be from two in a thousand to one in a thousand, or "
            "from one in seven thousand to two. Relative risks without their baselines mislead patients and "
            "doctors alike. <bookmark mark='b'/> In 1995 British doctors were warned that some contraceptive pills "
            "doubled the risk of a rare kind of blood clot. The baseline was tiny, but the doubling made the "
            "headlines, many women stopped taking the pill, and unwanted pregnancies and abortions rose the next "
            "year. <bookmark mark='c'/> The tools from this part help: natural frequencies and pictures of a "
            "hundred or a thousand people, like the screening tree from chapter seven. "
            "<bookmark mark='d'/> Medical guidelines now ask for absolute risks, in frequencies, with the same "
            "denominator throughout, which Gerd Gigerenzer and colleagues have campaigned for since the 1990s."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(left), FadeIn(right))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
