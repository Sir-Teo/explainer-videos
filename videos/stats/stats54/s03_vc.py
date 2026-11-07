from __future__ import annotations

from videos.stats.stats54.common import *  # noqa: F403


class VC(VoiceoverScene):
    def construct(self):
        self.card()
        self.symmetrization()
        self.bound()
        self.lower()
        self.sauer_proof()
        self.examples()
        self.realvalued()
        self.board()
        self.lesson()

    def card(self):
        card = chapter_card(2, r"VC bounds", r"From counting labellings to a guarantee", lit=(1971,), part=PART)
        with self.voiceover("Chapter two. VC bounds: from counting labellings to a guarantee."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def symmetrization(self):
        rows = [
            cmath(r"\text{a ghost sample } X'_{1:n}", r":", r"\sup_h |R_n(h) - R(h)| \lesssim \sup_h |R_n(h) - R'_n(h)|", font_size=30),
            cmath(r"\text{on } 2n \text{ points}", r":", r"\mathcal H \text{ acts through at most } \Pi_{\mathcal H}(2n) \text{ labellings}", font_size=32),
            cmath(r"\text{union bound}", r":", r"\Pi_{\mathcal H}(2n)\, e^{-nt^2/8}", font_size=36),
            cmath(r"\Pi_{\mathcal H}(n)", r"\le", r"(en/d)^d \ (1\le d\le n);\quad 2^n\ (d>n)", font_size=36),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"symmetrization"), why(r"the growth function"), why(r"finitely many, \ now"), why(r"polynomial in $n$")]
        heading = label('A ghost sample makes counting patterns useful for probability bounds', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The ghost sample controls deviation through a probability symmetrization inequality, with constants and a small-deviation condition; the first row is a schematic, not a pathwise comparison. <bookmark mark='b'/> Conditional on the combined two n observations, only finitely many binary loss patterns matter. <bookmark mark='c'/> A union bound, together with random swaps, then gives the growth-function tail bound. <bookmark mark='d'/> Sauer and Shelah bound the growth function by the sum of binomial coefficients up to d. For one at most d at most n, this is bounded by e n over d to the d; when d exceeds n use two to the n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bound(self):
        rows = [
            cmath(r"\sup_h |R_n(h) - R(h)|", r"\le", r"\sqrt{\frac{8\big(d\log(2en/d) + \log(4/\delta)\big)}{n}}", font_size=36),
            cmath(r"\text{rate}", r":", r"\sqrt{d\log n / n}; \ \text{the log removable by chaining (Part 48)}", font_size=32),
            cmath(r"\text{distribution-free}", r":", r"\text{the same for every } P", font_size=36),
            cmath(r"\text{the price}", r":", r"\text{loose, \ since most } P \text{ are not the worst case}", font_size=34),
        ]
        rows[0][-1].set_color(BOUNDC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"Vapnik (1998)"), why(r"Talagrand; \ Dudley"), why(r"the strength"), why(r"and the weakness")]
        heading = label('A binary VC class admits a distribution-free probability bound', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The result: with probability one minus delta, the uniform deviation is at most the root of "
            "eight times d log of two e n over d plus log four over delta, over n. <bookmark mark='b'/> Its rate is the root "
            "of d log n over n, and Part forty-eight's chaining removes the log. <bookmark mark='c'/> Its great strength is "
            "that it holds for every distribution. <bookmark mark='d'/> Its weakness is the same thing: most distributions "
            "are not the worst case, so it is usually loose, as chapter one's chart showed."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lower(self):
        rows = [
            cmath(r"\text{a lower bound}", r":", r"\text{for every learner, \ some } P \text{ with VC-dimension-}d\ \mathcal H", font_size=32),
            cmath(r"E R(\hat h) - \inf_{\mathcal H} R", r"\ge", r"c\min\{1,\sqrt{d/n}\}: \ \text{agnostic},\ d\ge2", font_size=36),
            cmath(r"\text{realizable}", r":", r"\ge c\min\{1,d/n\},\ d\ge2", font_size=36),
            cmath(r"\text{so}", r":", r"\text{VC dimension is the right measure, \ up to logs}", font_size=34),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Ehrenfeucht et al. (1989)"), why(r"Part 50's method"), why(r"shattered sets as hypercubes"), why(r"matching bounds")]
        heading = label('Worst-case rates are capped by the bounded risk scale', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Matching lower bounds describe the worst distribution for each learner, not the risk on every distribution. Take a binary class with VC dimension at least two. <bookmark mark='b'/> In the agnostic case, the expected excess risk can be at least a constant times the minimum of one and root d over n. <bookmark mark='c'/> In the realizable case the analogous rate is the minimum of one and d over n. Shattered sets provide hard instances, using Part fifty's lower-bound methods. <bookmark mark='d'/> Thus VC dimension characterizes distribution-free sample complexity, with logarithmic qualifications for particular upper bounds."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sauer_proof(self):
        rows = [
            cmath(r"\text{fix a point } x_n", r":", r"\mathcal H|_{x_{1:n}} \to \mathcal H|_{x_{1:n-1}}: \ \text{some labellings merge in pairs}", font_size=32),
            cmath(r"|\mathcal H|_{x_{1:n}}|", r"=", r"|\mathcal H'| + |\mathcal H''|: \ \mathcal H'' = \text{the pairs, \ both labels of } x_n", font_size=32),
            cmath(r"\mathrm{VC}(\mathcal H'')", r"\le", r"d - 1: \ \text{any set it shatters, \ plus } x_n, \text{ is shattered by } \mathcal H", font_size=32),
            cmath(r"\text{induction}", r":", r"\Pi(n) \le \textstyle\sum_{i \le d}\binom{n-1}{i} + \sum_{i \le d-1}\binom{n-1}{i} = \sum_{i \le d}\binom{n}{i}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(BOUNDC)
        whys = [why(r"remove one point"), why(r"a counting identity"), why(r"the key step"), why(r"Pascal's rule")]
        heading = label('Counting merged pairs proves the Sauer--Shelah inequality', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Why does the growth function turn polynomial? Here is the proof of the Sauer–Shelah lemma, by induction on n. Forget the last point: labellings of the n points that differ only at that point merge in pairs. <bookmark mark='b'/> So the count of labellings of n points is the count on n minus one points, plus the number of merged pairs, those patterns that extend both ways. <bookmark mark='c'/> The class of merged pairs has VC dimension at most d minus one: if it shattered a set, then that set plus the last point would be shattered by the original class, impossible for a set of size d plus one. <bookmark mark='d'/> Apply the induction to both terms, and Pascal's rule for binomial coefficients assembles the sum of n choose i for i up to d: at most e n over d to the power d."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def examples(self):
        rows = [[r"class", r"VC dimension"],
                [r"thresholds on $\mathbb R$", r"1"], [r"intervals", r"2"], [r"half-planes in $\mathbb R^2$", r"3"],
                [r"half-spaces in $\mathbb R^p$", r"$p + 1$"], [r"axis-aligned rectangles", r"4"],
                [r"$\{\mathrm{sign}(\sin(\omega x))\}$", r"$\infty$, \ one parameter"],
                [r"neural networks, \ $W$ weights", r"architecture-dependent; \ ReLU upper bound $O(WL\log W)$"]]
        tab = table_rows(rows, font_size=26, col_buff=0.9, row_buff=0.32, colors=[GREY_B] + [CLASSC] * 5 + [BADC, TESTC])
        tab.move_to([0, 0.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Some VC dimensions. Thresholds on the line, one; intervals, two; half-planes, three, as in the hook; half-spaces in p dimensions, p plus one; axis-aligned rectangles, four. <bookmark mark='b'/> The VC dimension is not the number of parameters: the one-parameter class of sine waves has infinite VC dimension, because a high enough frequency can fit any labelling of suitably placed points. <bookmark mark='c'/> And neural-network VC bounds depend on depth and activation as well as weight count. For certain ReLU architectures, an upper bound is of order W L log W. Such worst-case capacity can greatly exceed the sample size."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[:6]))
            vo.wait_until("b")
            self.play(FadeIn(tab[6]))
            vo.wait_until("c")
            self.play(FadeIn(tab[7]))
        self.clear_scene()

    def realvalued(self):
        rows = [
            cmath(r"\text{real-valued classes}", r":", r"\text{pseudo-dimension, \ fat-shattering dimension at scale } \gamma", font_size=32),
            cmath(r"\text{covering numbers}", r":", r"\log N(\varepsilon, \mathcal F, L_2(P_n)) \lesssim d\log(1/\varepsilon)", font_size=34),
            cmath(r"\text{Dudley}", r":", r"\mathfrak R_n \lesssim \frac{1}{\sqrt n}\int_0^1 \sqrt{\log N(\varepsilon)}\, d\varepsilon", font_size=34),
            cmath(r"\text{the unifying idea}", r":", r"\text{capacity} = \text{how many distinct functions at each resolution}", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Pollard; \ Alon et al. (1997)"), why(r"Haussler (1995)"), why(r"Part 51's chaining"), why(r"entropy, \ again")]
        heading = label('Bounded real-valued classes need scale-sensitive capacity measures', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> For classes of real-valued functions, such as regression rules, the VC dimension is replaced by its scale-sensitive cousins, David Pollard's pseudo-dimension and the fat-shattering dimension. <bookmark mark='b'/> They bound covering numbers in the empirical L-two metric, as David Haussler showed. <bookmark mark='c'/> And Dudley's entropy integral from Part fifty-one turns covering numbers into a Rademacher bound. <bookmark mark='d'/> The unifying idea of all these measures: capacity is the number of genuinely different functions the class contains at each resolution."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("training error", "union bound", "holdout")
        d = load("board")
        a = [x["achieved"] for x in d["rows"]]
        show_board(self, rows,
                   f"<bookmark mark='a'/> On the Coverage Board, a selection problem: a thousand classifiers, in a constructed fixed class with independent Bernoulli error coordinates, each with true error just under a half, two hundred training points, and we keep the one with the lowest training error. The usual Wald interval around its training error covers its true error {100 * a[0]:.0f} percent of the time: selection makes the training error hopelessly optimistic. <bookmark mark='b'/> Hoeffding's interval with a union bound over the thousand classifiers, of half-width {say(d['union_half'], 2)}, covers {100 * a[1]:.1f} percent, conservatively. <bookmark mark='c'/> And a plain Wald interval on two hundred fresh holdout points covers {100 * a[2]:.0f} percent. Independence removes selection bias, but the Wald interval still has approximate rather than exact finite-sample coverage.",
                   [("a", [0]), ("b", [1]), ("c", [2])])

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"Selection bias, uniform guarantees and independent validation", font_size=36, color=WHITE),
            label(r"an error estimated on the data used to choose is biased, \ often badly", font_size=26, color=BADC),
            label(r"uniform bounds pay for the whole class, \ and are honest", font_size=26, color=BOUNDC),
            label(r"independent holdout removes selection; \ Wald coverage is approximate", font_size=26, color=GOODC),
            label(r"cross-validation sits between: \ Part 28's subject", font_size=26, color=CLASSC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What the Board says. <bookmark mark='b'/> An error estimated on the same data used to choose the rule is biased, often badly. <bookmark mark='c'/> A uniform bound pays for the size of the whole class, and is honest. <bookmark mark='d'/> An independent holdout removes selection bias; its interval method still determines coverage and width. <bookmark mark='e'/> Cross-validation, Part twenty-eight's subject, sits in between."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
