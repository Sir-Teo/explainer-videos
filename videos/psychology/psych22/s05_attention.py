from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403
from explainer.psychology.psyche import concepts as K


def curves_axes(center, x_length=5.6, y_length=3.4, font_size=17):
    return axes([1, 16], [0, 0.6], x_length=x_length, y_length=y_length, xticks=[1, 4, 8, 12, 16],
                yticks=[0, 0.3, 0.6], yfmt=lambda v: f"{v:.1f}", xlabel=r"block of 16 trials",
                ylabel=r"probability of error", center=center, font_size=font_size)


class Attention(VoiceoverScene):
    def construct(self):
        self.card()
        self.problems()
        self.data()
        self.failures()
        self.alcove()
        self.fit()

    def card(self):
        card = chapter_card(4, r"Six problems, \ and attention that learns", r"Which categories are hard to learn, "
                            r"and why?", lit={1961: r"Shepard, \ Hovland \& Jenkins", 1992: r"Kruschke",
                                              1994: r"Nosofsky et al."},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter four. Six problems, and attention that learns."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def problems(self):
        head = heading(r"Shepard, \ Hovland and Jenkins, \ 1961")
        cubes = VGroup()
        for t in range(1, 7):
            k = t - 1
            org = np.array([-6.0 + 2.25 * (k % 6), 0.6, 0])
            cube = shj_cube(K.SHJ_TYPES[t], org, size=1.05, radius=0.11)
            cubes.add(VGroup(cube, label(rf"Type {ROMAN[k]}", font_size=24, color=TYPE_COL[k]).next_to(cube, UP,
                                                                                                    buff=0.2)))
        rows = rows_of([
            (r"eight objects that vary in three binary ways: \ size, \ colour, \ shape; \ four go in each category",
             WHITE),
            (r"Type I: \ one dimension decides. \ Type II: \ two dimensions, \ exclusive or. \ Type IV: \ a family "
             r"resemblance. \ Type VI: \ every dimension, \ no regularity", GREY_A),
            (r"the corners of a cube: \ the colour is the category", CAT_A),
        ], 12.4, 24, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(r"Shepard, \ Hovland \& Jenkins (1961)")
        with self.voiceover(
            "In 1961 Roger Shepard, Carl Hovland and Herbert Jenkins found the cleanest test of all. "
            "<bookmark mark='a'/> Take eight objects that vary in three binary ways: big or small, black or white, "
            "square or triangle. Split them four and four into two categories. There are only six essentially "
            "different ways to do it. <bookmark mark='b'/> In Type I one dimension decides: all the big ones. In "
            "Type II two dimensions matter, as an exclusive or, and the third is irrelevant. Type IV is a family "
            "resemblance: members share most features with a prototype. And Type VI has no regularity at all: every "
            "dimension matters, and each object is its own rule. <bookmark mark='c'/> Drawn as the corners of a "
            "cube, the colour of each corner is its category."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cubes], lag_ratio=0.25), FadeIn(rows[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def data(self):
        d = load("shj")
        head = heading(r"How hard each one is: \ the open data")
        A = curves_axes([-2.6, 0.2, 0], x_length=6.6, y_length=3.8)
        b = d["blocks"]
        g = VGroup(*[curve(A.ax, b, d["observed"][k], TYPE_COL[k], 4) for k in range(6)])
        key = legend([(TYPE_COL[k], rf"Type {ROMAN[k]}") for k in range(6)], font_size=20).move_to([2.3, 1.1, 0])
        rows = rows_of([
            (r"Nosofsky, \ Gluck, \ Palmeri, \ McKinley and Glauthier, \ 1994: \ 40 learners per problem, \ "
             r"feedback on every trial", WHITE),
            (r"the order: \ I, \ then II, \ then III, \ IV and V together, \ then VI", MODEL),
            (r"II before IV is the surprise: \ IV has a prototype, \ II does not", LOST),
        ], 4.0, 21, 0.3).move_to([5.0, -0.8, 0])
        ptag = psyche_tag(r"open data: \ catlearn's \texttt{nosof94}")
        with self.voiceover(
            "Here are the learning curves, from a replication by Nosofsky and colleagues in 1994, with forty learners "
            "on each problem, packaged as open data. <bookmark mark='a'/> Type I is learnt almost at once. Then Type "
            "II. Then III, IV and V, close together. Then Type VI, by far the slowest. That order matches the "
            "original 1961 study. <bookmark mark='b'/> And it's a puzzle for prototypes. Type IV has a perfect "
            "family resemblance structure: every member is closer to its own prototype. Type II has no prototype at "
            "all: its categories' averages are identical. Yet II is easier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag), FadeIn(rows[0]))
            self.play(LaggedStart(*[Create(x) for x in g], lag_ratio=0.2), FadeIn(key), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), Indicate(key[1]), Indicate(key[3]))
        self.clear_scene()

    def failures(self):
        d = load("shj")
        head = heading(r"Two models that get it wrong")
        b = d["blocks"]
        A = curves_axes([-3.5, 0.1, 0], x_length=5.4, y_length=3.2)
        B = curves_axes([3.0, 0.1, 0], x_length=5.4, y_length=3.2)
        ga = VGroup(*[curve(A.ax, b, d["delta"][k], TYPE_COL[k], 3) for k in range(6)])
        gb = VGroup(*[curve(B.ax, b, d["noattn"][k], TYPE_COL[k], 3) for k in range(6)])
        ta = label(r"a prototype network \ (the delta rule)", font_size=22, color=PROTO).next_to(A, UP, buff=0.1)
        tb = label(r"exemplars, \ attention fixed", font_size=22, color=EXEMPLAR).next_to(B, UP, buff=0.1)
        key = legend([(TYPE_COL[k], rf"{ROMAN[k]}") for k in range(6)], font_size=18).arrange(RIGHT, buff=0.35)
        key.move_to([0, 2.75, 0])
        noat = d["noattn"].mean(1)
        rows = rows_of([
            (r"the prototype network learns I and IV, \ part of III and V, \ and nothing of II and VI: \ no straight "
             r"boundary separates them", PROTO),
            (rf"exemplars with fixed attention, \ fitted: \ II comes out harder than III and IV "
             rf"({noat[1]:.2f} against {noat[2]:.2f}): \ the wrong order", EXEMPLAR),
        ], 12.4, 22, 0.25).to_edge(DOWN, buff=0.65)
        ptag = psyche_tag(r"\texttt{concepts.delta\_rule\_network}, \ \texttt{concepts.fit\_alcove\_shj}")
        with self.voiceover(
            "Two simple models fail. <bookmark mark='a'/> A prototype network, the dimensions wired straight to the "
            "categories and trained by the delta rule of Part 16, can learn only categories that a straight "
            "boundary separates. It learns I and IV, only part of III and V, and stays at chance on II and VI. <bookmark mark='b'/> An "
            "exemplar model with attention fixed, spread equally over the three dimensions, does learn everything. "
            "Fitted as well as it can be to the data, it gets the order wrong: Type II comes out harder than III and "
            "IV. With equal attention, the irrelevant third dimension of Type II keeps getting in the way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(ta), FadeIn(tb), FadeIn(key), FadeIn(ptag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in ga], lag_ratio=0.15), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in gb], lag_ratio=0.15), FadeIn(rows[1]))
        self.clear_scene()

    def alcove(self):
        head = heading(r"Derivation: \ ALCOVE")
        eqs = VGroup(
            MathTex(r"a_j = \exp\Big(-c \sum_i \alpha_i\, |h_{ji} - x_i|\Big)", font_size=34, color=EXEMPLAR),
            MathTex(r"o_k = \sum_j w_{kj}\, a_j \qquad P(k) = \frac{e^{\phi o_k}}{\sum_K e^{\phi o_K}}", font_size=34,
                    color=MODEL),
            MathTex(r"\Delta w_{kj} = \lambda_w\, (t_k - o_k)\, a_j", font_size=34, color=CAT_A),
            MathTex(r"\Delta \alpha_i = -\lambda_\alpha \sum_j \Big[\sum_k (t_k - o_k)\, w_{kj}\Big] a_j\, c\, "
                    r"|h_{ji} - x_i|", font_size=32, color=PROTO),
        ).arrange(DOWN, buff=0.35).move_to([-2.6, 0.1, 0])
        rows = rows_of([
            (r"one hidden unit per stored example: \ the GCM's similarity", EXEMPLAR),
            (r"category outputs, \ and Luce's rule", MODEL),
            (r"association weights learnt by the delta rule", CAT_A),
            (r"and attention learnt too: \ gradient descent on the error shifts attention to the dimensions that "
             r"reduce it", PROTO),
        ], 4.4, 21, 0.32).move_to([4.6, 0.1, 0])
        tag = published_tag(r"Kruschke (1992)")
        with self.voiceover(
            "John Kruschke's ALCOVE, in 1992, put the two together: Parts 16 and 18 meeting in one network. "
            "<bookmark mark='a'/> There is one hidden unit for every stored example, and its activation is the GCM's "
            "similarity, with attention strengths alpha on each dimension. <bookmark mark='b'/> The category outputs "
            "sum over the examples, and Luce's rule makes the choice. <bookmark mark='c'/> After each trial, the "
            "association weights learn by the delta rule. <bookmark mark='d'/> And the attention strengths learn too, "
            "by gradient descent on the same error: attention shifts to the dimensions whose differences reduce the "
            "error, and away from the ones that only get in the way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, e, r in zip("abcd", eqs, rows):
                vo.wait_until(m)
                self.play(Write(e), FadeIn(r))
        self.clear_scene()

    def fit(self):
        d = load("shj")
        head = heading(r"ALCOVE, \ fitted to the six curves")
        b = d["blocks"]
        A = curves_axes([-3.7, 0.25, 0], x_length=5.0, y_length=3.2)
        obs = VGroup(*[scatter(A.ax, b, d["observed"][k], TYPE_COL[k], 0.05, 0.9) for k in range(6)])
        fit = VGroup(*[curve(A.ax, b, d["alcove"][k], TYPE_COL[k], 3) for k in range(6)])
        key = legend([(TYPE_COL[k], rf"{ROMAN[k]}") for k in range(6)], font_size=18).arrange(RIGHT, buff=0.3)
        key.next_to(A, UP, buff=0.15)
        bars_ = VGroup()
        for i, t in enumerate((1, 2, 6)):
            att = d[f"attention{t}"]
            Bx = axes([0, 3], [0, 1.2], x_length=1.6, y_length=1.4, xticks=[], yticks=[],
                      center=[1.0 + 2.0 * i, 1.2, 0], font_size=14)
            bb = bars(Bx.ax, [0.5, 1.5, 2.5], att, TYPE_COL[t - 1], width=0.6)
            bars_.add(VGroup(Bx, bb, label(rf"Type {ROMAN[t - 1]}", font_size=18, color=TYPE_COL[t - 1]).next_to(
                Bx, UP, buff=0.05)))
        al = label(r"attention to the three dimensions, \ at the end", font_size=19, color=PROTO).next_to(bars_, UP,
                                                                                                    buff=0.15)
        al.set_x(bars_.get_x())
        m = d["alcove"].mean(1)
        o = d["observed"].mean(1)
        p = d["alcove_params"]
        rows = rows_of([
            (rf"four numbers fitted to all 96 points \ ($c = {p[0]:.1f}$, \ $\phi = {p[1]:.1f}$, \ "
             rf"$\lambda_w = {p[2]:.2f}$, \ $\lambda_\alpha = {p[3]:.2f}$)", GREY_A),
            (rf"now II beats III to V \ ({m[1]:.2f} against {m[2]:.2f}): \ attention leaves the irrelevant dimension",
             MODEL),
            (rf"but at these values VI is learnt about as fast as III to V \ ({m[5]:.2f}; \ people: {o[5]:.2f}): \ "
             r"the model's known weak point", LOST),
        ], 6.4, 20, 0.28).move_to([3.1, -1.6, 0])
        ptag = psyche_tag(r"\texttt{concepts.alcove}: \ 20 random orders per problem")
        with self.voiceover(
            "Here's ALCOVE fitted to all ninety-six points, four numbers for six curves. "
            "<bookmark mark='a'/> The order now comes out right at the start: Type I, then II, then III, IV and V. "
            f"Type II's mean error is {m[1]:.2f} against {m[2]:.2f} for Type III. <bookmark mark='b'/> The reason is "
            "in the attention it ends with. On Type I, all attention goes to the one dimension that decides. On Type "
            "II, to the two that matter, and the third is ignored. On Type VI it stays spread over all three, "
            "because all three are needed. <bookmark mark='c'/> It isn't perfect. At these fitted values it learns "
            f"Type VI about as fast as III to V, with mean error {m[5]:.2f}, where people's was {o[5]:.2f}: the most "
            "difficult problem is where this version struggles. Still, the main lesson stands: to learn a category "
            "you must learn what to attend to, and exemplars plus learnt attention capture that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(key), FadeIn(ptag), FadeIn(obs), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in fit], lag_ratio=0.15), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(al), LaggedStart(*[FadeIn(x) for x in bars_], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
