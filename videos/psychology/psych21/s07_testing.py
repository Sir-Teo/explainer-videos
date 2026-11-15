from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403

DELAY_TICKS = {0: r"5\,\text{min}", 2: r"2\,\text{d}", 7: r"1\,\text{wk}"}


def hist_bars(ax, values, edges, color, scale=1.0, opacity=0.6) -> VGroup:
    h, _ = np.histogram(values, edges, density=True)
    out = VGroup()
    for lo, hi, v in zip(edges[:-1], edges[1:], h * scale):
        a, b = ax.c2p(lo, 0), ax.c2p(hi, v)
        out.add(Rectangle(width=abs(b[0] - a[0]), height=max(abs(b[1] - a[1]), 1e-3), stroke_width=0,
                          fill_color=color, fill_opacity=opacity).move_to([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0]))
    return out


class Testing(VoiceoverScene):
    def construct(self):
        self.card()
        self.experiment()
        self.illusion()
        self.bifurcation()
        self.fit()

    def card(self):
        card = chapter_card(6, r"Testing", r"Is a test a measurement, \ or a way to learn?",
                            lit={1917: r"Gates", 2006: r"Roediger \& Karpicke", 2011: r"Kornell, \ Bjork \& Garcia"},
                            part=PART, scale=("mind", "person"), marr=("what", "how"))
        with self.voiceover("Chapter six. Testing."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def experiment(self):
        r = archive.ROEDIGER_KARPICKE_2006.data
        head = heading(r"Study it again, \ or test yourself?")
        x = np.array([0.0, 2.0, 7.0])
        A = axes([0, 7.5], [0.3, 0.9], x_length=6.0, y_length=3.4, xticks=[0, 2, 7], yticks=[0.3, 0.6, 0.9],
                 xfmt=lambda v: DELAY_TICKS[int(round(v))], yfmt=lambda v: f"{100 * v:.0f}\\%",
                 xlabel=r"delay before the final test", ylabel=r"idea units recalled", center=[-3.2, 0.1, 0],
                 font_size=18)
        g = VGroup(curve(A.ax, x, r["exp1_restudy"], CUE, 4), scatter(A.ax, x, r["exp1_restudy"], CUE, 0.09, 1.0),
                   curve(A.ax, x, r["exp1_test"], TRACE, 4), scatter(A.ax, x, r["exp1_test"], TRACE, 0.09, 1.0))
        key = legend([(CUE, r"read it again"), (TRACE, r"took a recall test")], font_size=21).move_to([-1.6, 1.9, 0])
        rows = rows_of([
            (rf"Roediger and Karpicke, \ 2006: \ {r['exp1_n']} students read a short prose passage, \ then either "
             r"read it again or wrote down all they could remember, \ with no feedback", WHITE),
            (r"five minutes later, \ re-reading wins", CUE),
            (r"two days and a week later, \ the test wins, \ by 14 points: \ the lines cross", TRACE),
            (r"the test did not only measure the memory: \ it changed it", MODEL),
        ], 6.0, 22, 0.3).move_to([3.6, 0.0, 0])
        tag = historical_tag(archive.ROEDIGER_KARPICKE_2006.cite)
        with self.voiceover(
            "We think of a test as a measurement, a thermometer for memory. In 2006 Henry Roediger and Jeffrey "
            "Karpicke showed that the thermometer changes the temperature. <bookmark mark='a'/> A hundred and "
            "twenty students read a short passage, about the sun or about sea otters. Then they either read it "
            "again, or wrote down everything they could remember, with no feedback on what they'd missed. "
            "<bookmark mark='b'/> Tested five minutes later, the students who had re-read did better, which is "
            "what anyone would expect: they had seen the whole passage twice. <bookmark mark='c'/> But two days "
            "later, and a week later, it was the other way round. The students who had been tested remembered "
            "fourteen points more. The lines cross. <bookmark mark='d'/> A test is not only a measurement of "
            "memory. Retrieving something is itself a powerful way to learn it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(g[0]), FadeIn(g[1]), Create(g[2]), FadeIn(g[3]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(g[3], color=TRACE))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def illusion(self):
        r = archive.ROEDIGER_KARPICKE_2006.data
        head = heading(r"The students did not know")
        conds = r["exp2_conditions"]
        A = axes([0, 3], [0, 1], x_length=4.6, y_length=3.0, xticks=[], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"recalled", center=[-4.3, 0.2, 0], font_size=18)
        five = bars(A.ax, np.arange(3) + 0.3, r["exp2_5min"], GREY_B, width=0.35)
        week = bars(A.ax, np.arange(3) + 0.7, r["exp2_week"], TRACE, width=0.35)
        names = VGroup(*[label(c, font_size=22, color=GREY_A).next_to(A.ax.c2p(i + 0.5, 0), DOWN, buff=0.12)
                         for i, c in enumerate(conds)])
        k1 = legend([(GREY_B, r"after 5 minutes"), (TRACE, r"after a week")], font_size=19)
        k1.arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.35)
        B = axes([0, 3], [0, 7], x_length=4.0, y_length=3.0, xticks=[], yticks=[1, 4, 7],
                 ylabel=r"predicted recall in a week \ (1 to 7)", center=[1.1, 0.2, 0], font_size=18)
        pb = bars(B.ax, np.arange(3) + 0.5, r["exp2_predicted"], FALSE, width=0.5)
        names2 = VGroup(*[label(c, font_size=22, color=GREY_A).next_to(B.ax.c2p(i + 0.5, 0), DOWN, buff=0.12)
                          for i, c in enumerate(conds)])
        rows = rows_of([
            (rf"{r['exp2_n']} students: \ four periods each, \ S = study the passage, \ T = recall it", GREY_A),
            (rf"after a week: \ {pct(r['exp2_week'][2])} for STTT, \ {pct(r['exp2_week'][0])} for SSSS, \ which "
             rf"had read it {r['exp2_reads'][0]:.0f} times", TRACE),
            (r"yet those who only studied predicted they would remember most", FALSE),
            (r"re-reading feels fluent, \ and fluency feels like learning", LOST),
        ], 3.6, 20, 0.3).move_to([5.1, 0.0, 0])
        tag = historical_tag(archive.ROEDIGER_KARPICKE_2006.cite)
        with self.voiceover(
            "Their second experiment pushed it further. <bookmark mark='a'/> A hundred and eighty students had four "
            "short periods with a passage. Some studied it four times; some studied three times and recalled once; "
            "some studied once and recalled it three times. <bookmark mark='b'/> Five minutes later, the more "
            f"studying, the better. A week later, the order flipped: {spct(r['exp2_week'][2])} for those who were "
            f"tested three times, {spct(r['exp2_week'][0])} for those who only studied, though they had read the "
            f"passage about {r['exp2_reads'][0]:.0f} times. <bookmark mark='c'/> Then the twist. Before the final "
            "test, everyone was asked how well they'd remember the passage in a week. Those who had only studied "
            "were the most confident. <bookmark mark='d'/> Re-reading makes a text feel fluent, and fluency feels "
            "like learning. It's a metacognitive illusion, and it's why students choose re-reading over testing "
            "themselves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(k1))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in five], lag_ratio=0.2))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in week], lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(B), FadeIn(names2), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in pb], lag_ratio=0.2),
                      FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bifurcation(self):
        d = load("testing")
        p = dict(zip(("restudy", "gain", "theta_test", "loss", "tau"), d["params"]))
        head = heading(r"Derivation: \ the bifurcation model")
        edges = np.linspace(-3.5, 6.5, 61)
        A = axes([-3.5, 6.5], [0, 0.55], x_length=6.4, y_length=1.8, xticks=[], yticks=[],
                 ylabel=r"re-read: \ everyone gains a little", center=[-2.9, 1.25, 0], font_size=18)
        B = axes([-3.5, 6.5], [0, 0.55], x_length=6.4, y_length=1.8, xticks=[], yticks=[],
                 ylabel=r"tested: \ the items recalled gain a lot, \ the rest nothing",
                 center=[-2.9, -1.35, 0], font_size=18)
        hA = hist_bars(A.ax, d["s_restudy"], edges, CUE)
        hB = hist_bars(B.ax, d["s_test"], edges, TRACE)
        th = DashedLine(B.ax.c2p(p["theta_test"] + p["gain"], 0), B.ax.c2p(p["theta_test"] + p["gain"], 0.55),
                        color=GREY_B)
        thl = label(r"recalled on the first test $\rightarrow$", font_size=18, color=GREY_B)
        thl.next_to(B.ax.c2p(p["theta_test"] + p["gain"], 0.47), LEFT, buff=0.1)
        rows = rows_of([
            (r"item strengths start out normal", GREY_A),
            (r"re-reading adds a little to every item", CUE),
            (r"a test retrieves the items above a threshold and adds a lot to those alone, \ with no feedback for "
             r"the rest", TRACE),
            (r"the distribution splits in two: \ \emph{bifurcates}", MODEL),
            (r"with a little forgetting, \ re-reading's gain to the weak items survives; \ with a lot, \ only the "
             r"tested items' large gain stays above the line", LOST),
        ], 5.4, 21, 0.3).move_to([4.0, 0.0, 0])
        tag = published_tag(r"Kornell, \ Bjork \& Garcia (2011)")
        with self.voiceover(
            "Why would the lines cross? Nate Kornell, Robert Bjork and Michael Garcia proposed a simple model in "
            "2011. <bookmark mark='a'/> Think of the items in a passage as having strengths, spread out like a bell "
            "curve. <bookmark mark='b'/> Re-reading adds a little strength to every item. "
            "<bookmark mark='c'/> A test is different. The items strong enough to be recalled get a large boost: "
            "retrieving them strengthens them much more than reading does. The items you fail to recall get nothing, "
            "because there's no feedback. <bookmark mark='d'/> So testing splits the distribution in two. It "
            "bifurcates. <bookmark mark='e'/> Now let time pass, and every strength falls. After five minutes, the "
            "re-read items are mostly still above the line, including the weak ones re-reading lifted. After a week, "
            "only items with a large margin survive, and those are the ones that were tested. One mechanism gives "
            "both halves of the crossover."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hA), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(hB), FadeIn(rows[2]), Create(th), FadeIn(thl))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def fit(self):
        d = load("testing")
        r = archive.ROEDIGER_KARPICKE_2006.data
        p = dict(zip(("restudy", "gain", "theta_test", "loss", "tau"), d["params"]))
        head = heading(r"The model, \ fitted to the first experiment")
        x = np.array([0.0, 2.0, 7.0])
        A = axes([0, 7.5], [0.3, 0.9], x_length=6.4, y_length=3.6, xticks=[0, 2, 7], yticks=[0.3, 0.6, 0.9],
                 xfmt=lambda v: DELAY_TICKS[int(round(v))], yfmt=lambda v: f"{100 * v:.0f}\\%",
                 xlabel=r"delay before the final test", ylabel=r"recalled", center=[-2.9, 0.0, 0], font_size=18)
        fx = d["fine_delays"]
        g = VGroup(curve(A.ax, fx, d["fine_restudy"], CUE, 3), curve(A.ax, fx, d["fine_test"], TRACE, 3),
                   scatter(A.ax, x, r["exp1_restudy"], CUE, 0.1, 1.0), scatter(A.ax, x, r["exp1_test"], TRACE, 0.1, 1.0))
        key = legend([(CUE, r"re-read: \ data and model"), (TRACE, r"tested: \ data and model")],
                     font_size=20).move_to([-1.6, 2.15, 0])
        rows = rows_of([
            (rf"five parameters, \ least squares on six points: \ the fit is close by construction", GREY_A),
            (rf"the check: \ the model says the first test should recall {pct(d['initial_test'])} of the items; \ "
             r"the students recalled about 70\% of the idea units", MODEL),
            (rf"re-reading adds {p['restudy']:.1f} \ (in units of the starting spread); \ a successful recall adds "
             rf"{p['gain']:.1f}", TRACE),
            (r"a prediction to test: \ give feedback after the test, \ so the failed items gain too, \ and "
             r"testing should win sooner", CUE),
        ], 5.6, 21, 0.3).move_to([3.9, 0.0, 0])
        ptag = psyche_tag(r"\texttt{memory.fit\_bifurcation}")
        with self.voiceover(
            "Here's the model fitted to Roediger and Karpicke's six points. <bookmark mark='a'/> It has five "
            "parameters, so fitting six points closely proves little by itself. <bookmark mark='b'/> The real "
            "check is a number it was not fitted to. The model says the first test should have recalled "
            f"{spct(d['initial_test'])} of the items. The students recalled about seventy percent of the passage's "
            "idea units. <bookmark mark='c'/> And the fitted gains are telling: a successful retrieval adds about "
            f"{p['gain'] / p['restudy']:.1f} times as much strength as reading the passage again. "
            "<bookmark mark='d'/> And it makes a prediction you could test: give feedback after the test, so the "
            "failed items gain too, and the bifurcation closes up. Then testing should beat re-reading even at short "
            "delays. That's one of this part's problems."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(key), FadeIn(ptag))
            self.play(Create(g[0]), Create(g[1]), FadeIn(g[2]), FadeIn(g[3]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
