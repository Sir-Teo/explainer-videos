from __future__ import annotations

import numpy as np

from videos.stats.stats19.common import *  # noqa: F403


def box(text, sub, col, pos, w=2.6):
    t = label(text, font_size=20, color=col)
    s = label(sub, font_size=16, color=GREY_B)
    inner = VGroup(t, s).arrange(DOWN, buff=0.08)
    r = RoundedRectangle(width=max(w, inner.width + 0.3), height=inner.height + 0.3, corner_radius=0.1, stroke_color=col,
                         stroke_width=2, fill_color="#0B0F17", fill_opacity=0.95).move_to(pos)
    inner.move_to(r)
    return VGroup(r, inner)


class Trees(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.diagram()
        self.partition()
        self.prune()
        self.cv_size()
        self.pros_cons()

    def card(self):
        card = chapter_card(6, r"Trees", r"Twenty questions, \ asked by the data", part=PART)
        with self.voiceover("Chapter six. Trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\text{split}", r":", r"x_j \le t \text{ or not, \ choosing } j, t \text{ to purify the two halves}", font_size=28),
            cmath(r"\text{impurity}", r":", r"\text{squared error, \ or Gini } 2p(1 - p)", font_size=30),
            cmath(r"\text{recurse}", r":", r"\text{split each half again, \ until the leaves are small}", font_size=30),
            cmath(r"\text{predict}", r":", r"\text{the average (or majority) in the leaf}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"try every variable and every cut"), why(r"Breiman, \ Friedman, \ Olshen \& Stone (1984): \ CART"),
                why(r"greedy: \ the best split now, \ not the best tree"), why(r"a piecewise-constant rule")]
        with self.voiceover(
            "A tree asks a sequence of yes-or-no questions. <bookmark mark='a'/> At each step it considers every variable and "
            "every cut point, and picks the split that makes the two halves most homogeneous. <bookmark mark='b'/> "
            "Homogeneity is measured by squared error for a number, or by the Gini index for a class. The method, CART, was "
            "set out by Leo Breiman, Jerome Friedman, Richard Olshen and Charles Stone in 1984. <bookmark mark='c'/> Then it "
            "splits each half the same way, and so on: a greedy search, choosing the best split at each step rather than the "
            "best tree overall. <bookmark mark='d'/> A new case runs down the questions to a leaf, and gets the leaf's average "
            "or majority."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def diagram(self):
        d = load("tree")["small"]
        t1 = 10 ** d["threshold"]
        t2 = 10 ** d["right"]["threshold"]
        root = box(r"all 2,000 adults", rf"Blue {100 * d['value']:.1f}\%", GREY_A, [0, 2.4, 0])
        q1 = label(rf"income $\le$ {t1:.1f}k?", font_size=20, color=OBS).move_to([0, 1.55, 0])
        left = box(rf"{d['left']['n']} adults", rf"Blue {100 * d['left']['value']:.1f}\%", RED, [-3.4, 0.6, 0])
        right = box(rf"{d['right']['n']} adults", rf"Blue {100 * d['right']['value']:.1f}\%", GREY_A, [3.0, 0.6, 0])
        q2 = label(rf"income $\le$ {t2:.1f}k?", font_size=20, color=OBS).move_to([3.0, -0.6, 0])
        rl = box(rf"{d['right']['left']['n']} adults", rf"Blue {100 * d['right']['left']['value']:.1f}\%", RED, [1.2, -1.3, 0])
        rr = box(rf"{d['right']['right']['n']} adults", rf"Blue {100 * d['right']['right']['value']:.1f}\%", BLUE, [4.8, -1.3, 0])
        lines = VGroup(Line(root.get_bottom(), left.get_top(), color=GREY_C), Line(root.get_bottom(), right.get_top(), color=GREY_C),
                       Line(right.get_bottom(), rl.get_top(), color=GREY_C), Line(right.get_bottom(), rr.get_top(), color=GREY_C))
        yes = VGroup(label(r"yes", font_size=16, color=GREY_B).move_to([-1.8, 1.6, 0]), label(r"no", font_size=16, color=GREY_B).move_to([1.6, 1.6, 0]))
        foot = fit_rows(VGroup(
            label(r"income, \ again and again: \ age never earns a split this early", font_size=22),
            label(r"leaves: \ Red, \ Red, \ Blue \ (majority rule)", font_size=22, color=GREY_A),
        ), 12.4, 0.2, [0, -2.8, 0])
        tag = simulated_tag(r"2,000 adults; \ the World's vote", corner=UR)
        with self.voiceover(
            "<bookmark mark='a'/> A small tree for the World's vote, grown from two thousand adults' income and age. Overall, "
            "thirty-nine percent vote Blue. <bookmark mark='b'/> The best first question is whether income is above thirty-one "
            "thousand. <bookmark mark='c'/> Below it, only a quarter vote Blue. <bookmark mark='d'/> Above it, forty-seven "
            "percent, and the next best question splits again on income, at seventy-six thousand: <bookmark mark='e'/> forty-three "
            "percent below, sixty-three above. <bookmark mark='f'/> Income dominates; age never earns a split this early. Read "
            "with majority rule, the leaves say Red, Red, Blue: only the richest group is predicted to vote Blue."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(root))
            vo.wait_until("b")
            self.play(FadeIn(q1))
            vo.wait_until("c")
            self.play(Create(lines[0]), FadeIn(left), FadeIn(yes[0]))
            vo.wait_until("d")
            self.play(Create(lines[1]), FadeIn(right), FadeIn(yes[1]), FadeIn(q2))
            vo.wait_until("e")
            self.play(Create(lines[2]), Create(lines[3]), FadeIn(rl), FadeIn(rr))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def partition(self):
        d = load("tree")
        s = d["small"]
        X, v = np.asarray(d["sample_x"]), np.asarray(d["sample_v"])
        A = axes([0.6, 2.6], [18, 95], x_length=8.0, y_length=4.4, xlabel=r"income, \ thousands \ (log scale)", ylabel=r"age",
                 xticks=[1, 1.5, 2, 2.5], yticks=[20, 40, 60, 80], center=[-1.4, 0.3, 0], xfmt=lambda u: f"{10 ** u:.0f}")
        ax = A.ax
        t1, t2 = s["threshold"], s["right"]["threshold"]
        regs = VGroup(
            Rectangle(width=ax.c2p(t1, 0)[0] - ax.c2p(0.6, 0)[0], height=ax.c2p(0, 95)[1] - ax.c2p(0, 18)[1], stroke_width=0,
                      fill_color=RED, fill_opacity=0.2).move_to(ax.c2p(0.6, 18), aligned_edge=DL),
            Rectangle(width=ax.c2p(t2, 0)[0] - ax.c2p(t1, 0)[0], height=ax.c2p(0, 95)[1] - ax.c2p(0, 18)[1], stroke_width=0,
                      fill_color=RED, fill_opacity=0.12).move_to(ax.c2p(t1, 18), aligned_edge=DL),
            Rectangle(width=ax.c2p(2.6, 0)[0] - ax.c2p(t2, 0)[0], height=ax.c2p(0, 95)[1] - ax.c2p(0, 18)[1], stroke_width=0,
                      fill_color=BLUE, fill_opacity=0.22).move_to(ax.c2p(t2, 18), aligned_edge=DL))
        cuts = VGroup(*[DashedLine(ax.c2p(t, 18), ax.c2p(t, 95), color=OBS, stroke_width=2.5) for t in (t1, t2)])
        dots = VGroup(*[Dot(ax.c2p(min(max(a, 0.62), 2.58), b), radius=0.035, color=BLUE if c else RED) for (a, b), c in zip(X, v)])
        rows = fit_rows(VGroup(
            label(r"a tree cuts the plane into boxes", font_size=22),
            label(r"splits are parallel to the axes", font_size=22, color=OBS),
            label(r"each box gets one prediction", font_size=22),
            label(r"deeper trees: \ smaller boxes, \ interactions", font_size=22, color=GREY_A),
        ), 4.0, 0.4, [4.9, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the plane of income and age, the tree is a set of boxes. <bookmark mark='b'/> Every split "
            "is a cut parallel to an axis, here two cuts on income. <bookmark mark='c'/> Each box gets a single prediction. "
            "<bookmark mark='d'/> A deeper tree cuts the boxes again, perhaps by age within an income band, and so captures "
            "interactions without anyone specifying them: the effect of age can differ between rich and poor."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(regs), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(Create(cuts), FadeIn(rows[1]))
                else:
                    self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def prune(self):
        rows = [
            cmath(r"\text{grow big}", r":", r"\text{until leaves have 20 adults: \ 35 leaves}", font_size=30),
            cmath(r"R_\alpha(T)", r"=", r"\text{error}(T) + \alpha\,|T|", font_size=32),
            cmath(r"\text{weakest link}", r":", r"\text{collapse the split that buys least per leaf}", font_size=30),
            cmath(r"\alpha", r":", r"\text{chosen by cross-validation}", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"stopping early can miss a good later split"), why(r"cost-complexity: \ a penalty per leaf"),
                why(r"a nested sequence of subtrees"), why(r"chapter three, \ again")]
        with self.voiceover(
            "How big should the tree be? <bookmark mark='a'/> CART's answer is to grow it large, here until the leaves hold "
            "about twenty adults, thirty-five leaves in all, because a split that looks useless can enable a useful one below "
            "it. <bookmark mark='b'/> Then prune, by penalizing size: the error plus alpha times the number of leaves. "
            "<bookmark mark='c'/> As alpha grows, the splits that buy the least improvement per leaf are collapsed first, the "
            "weakest links, giving a nested sequence of smaller and smaller trees. <bookmark mark='d'/> Cross-validation picks "
            "alpha, and so the size."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cv_size(self):
        d = load("tree")
        sz = np.asarray(d["sizes"], float)
        cv = np.asarray(d["cv"])
        A = axes([0, 25], [0.34, 0.41], x_length=8.4, y_length=4.2, xlabel=r"leaves", ylabel=r"10-fold CV misclassification",
                 xticks=[1, 5, 10, 15, 20, 25], yticks=[0.35, 0.37, 0.39, 0.41], center=[-1.4, 0.3, 0])
        ax = A.ax
        c = polyline(ax, sz, cv, CVC, 3.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=CVC) for a, b in zip(sz, cv)])
        base = DashedLine(ax.c2p(0, d["base"]), ax.c2p(25, d["base"]), color=GREY_B, stroke_width=2)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{CV's choice}}: {d['best']}\ \text{{leaves}}", font_size=26, color=CVC),
            MathTex(rf"\text{{test error}}: {100 * d['test_pruned']:.1f}\%\ \text{{pruned}},\ {100 * d['test_full']:.1f}\%\ \text{{full}}", font_size=24),
            MathTex(rf"\text{{always Red}}: {100 * d['base']:.1f}\%", font_size=24, color=GREY_B),
            label(r"the vote is mostly unpredictable from income and age", font_size=20, color=RES),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The cross-validated error for each pruned size: one leaf, a single guess for everyone, is "
            "worst; the minimum is at four leaves, and larger trees slowly get worse. <bookmark mark='b'/> On a thousand "
            "held-out adults, the pruned tree misclassifies thirty-five point nine percent, and the full thirty-five-leaf tree "
            "thirty-eight point five. <bookmark mark='c'/> Predicting Red for everyone would misclassify thirty-seven point six. "
            "<bookmark mark='d'/> So the tree helps only a little, which is the truth: in the World, income and age shift the "
            "odds of voting Blue, but most of the vote is individual. A good learner is honest about how little can be "
            "predicted; the unpruned tree, worse than guessing, is not."
        ) as vo:
            self.play(FadeIn(A), Create(base))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(dots), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def pros_cons(self):
        rows = fit_rows(VGroup(
            label(r"trees: \ readable, \ handle any kind of variable, \ find interactions", font_size=24, color=HIT),
            label(r"but unstable: \ a slightly different sample, \ a different tree", font_size=24, color=RES),
            label(r"high variance: \ chapter two's problem", font_size=24),
            label(r"the cure: \ average many trees \ (bagging, \ random forests, \ boosting)", font_size=24, color=OBS),
            label(r"Breiman (1996, \ 2001); \ Friedman (2001): \ Parts 54 and 64", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Trees are readable, handle any kind of variable without transformation, and find "
            "interactions on their own. <bookmark mark='b'/> But they're unstable: change a few observations and the first "
            "split may move, and everything below it. <bookmark mark='c'/> That's chapter two's variance problem in its purest "
            "form. <bookmark mark='d'/> The cure is to average many trees, grown on bootstrap resamples or on reweighted data: "
            "bagging, random forests and boosting. <bookmark mark='e'/> Breiman's random forests of 2001 and Friedman's gradient "
            "boosting of the same year are among the most accurate off-the-shelf predictors there are; Parts 54 and 64 take "
            "them up."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
