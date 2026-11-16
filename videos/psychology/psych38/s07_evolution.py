from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


class Evolution(VoiceoverScene):
    def construct(self):
        self.card()
        self.conformity()
        self.prestige()
        self.faithful()
        self.tasmania()

    def card(self):
        card = chapter_card(6, r"Culture as inheritance", r"Can culture be written as equations?",
                            lit={1985: r"Boyd \& Richerson", 2004: r"Henrich", 2005: r"Horner \& Whiten",
                                 2016: r"Vaesen et al."},
                            part=PART, scale=("group", "culture"), marr=("what", "how"))
        with self.voiceover("Chapter six. Culture as inheritance."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def conformity(self):
        d = load("conform")
        head = heading(r"Copy the majority")
        A = axes([0, 1], [-0.03, 0.03], x_length=4.2, y_length=2.1, xticks=[0, 0.5, 1], yticks=[-0.02, 0, 0.02],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:+.2f}" if v else "0", xlabel=r"share with the variant, "
                 r"\ $p$", ylabel=r"change per generation", center=[-4.0, 1.35, 0], font_size=13)
        step = curve(A.ax, d["step_p"], d["step_dp"], MODEL, stroke_width=4)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1, 0), color=GREY_D)
        B = axes([0, 40], [0, 1], x_length=4.2, y_length=1.7, xticks=[0, 20, 40], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"generation", ylabel=r"share",
                 center=[-4.0, -2.35, 0], font_size=13)
        gens = np.arange(41)
        paths = VGroup(*[curve(B.ax, gens, d[f"sim_{k}"], c, stroke_width=3) for k, c in
                         enumerate((WEST, WEST, WORLD, WORLD))])
        eq = MathTex(r"\Delta p = D\,p\,(1-p)\,(2p-1)", font_size=34, color=MODEL).move_to([3.2, 2.0, 0])
        rows = rows_of([
            (r"Boyd and Richerson, \ 1985: \ cultural traits passed on by learning, \ with biases in whom and what "
             r"is copied", WHITE),
            (r"conformist bias: \ a learner who samples three people adopts the majority's variant a little more "
             r"often than its share; \ with strength $D$, \ the share $p$ moves by the amount above", MODEL),
            (r"Psyche: \ 200 learners, \ $D = 0.3$; \ a variant starting at 45\% vanishes, \ one at 55\% takes "
             r"over: \ groups become uniform inside and different from each other", WORLD),
        ], 6.0, 19, 0.36).move_to([3.3, -0.9, 0])
        tag = psyche_tag(r"\texttt{culture.conformist\_sim}; \ Boyd \& Richerson (1985)")
        with self.voiceover(
            "If culture is learned from others, it's a second system of inheritance, and it can be modelled like "
            "genes. <bookmark mark='a'/> In 1985 Robert Boyd and Peter Richerson wrote down the mathematics, with "
            "biases in whom and what people copy. <bookmark mark='b'/> Take conformist bias. A learner who samples "
            "three people adopts the majority's variant a little more often than its share. With a bias of strength "
            "D, the share p moves by D p, one minus p, two p minus one, each generation. Below a half it shrinks; "
            "above a half it grows. <bookmark mark='c'/> In Psyche, two hundred learners with D of point three. A "
            "variant that starts at forty-five percent vanishes. One that starts at fifty-five takes over. "
            "Conformity makes groups uniform inside and different from each other, which is what cultures look "
            "like."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(eq), Create(step))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(B), *[Create(p) for p in paths], run_time=3.0)
        self.clear_scene()

    def prestige(self):
        d = load("prestige")
        head = heading(r"Copy the successful")
        A = axes([0, 30], [0, 1], x_length=5.0, y_length=3.2, xticks=[0, 10, 20, 30], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"generation",
                 ylabel=r"share with the useless marker", center=[-3.4, -0.2, 0], font_size=14)
        gens = np.arange(len(d["share"]))
        line = curve(A.ax, gens, d["share"], WORLD, stroke_width=4)
        n_over = int((np.asarray(d["finals"]) > 0.5).sum())
        rows = rows_of([
            (r"prestige bias: \ learners copy the most successful of a few people they observe", WHITE),
            (r"Psyche: \ a useless marker, \ a style of dress, \ starts in 10\% of people, \ mostly the skilled", WORLD),
            (rf"it rides along with skill: \ in the median of 21 runs it reaches {pct(d['share'][-1])} after 30 "
             rf"generations, \ and passes half in {n_over} of the 21", MODEL),
            (r"why fashions follow celebrities, \ and why a successful group's customs spread with its "
             r"techniques", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{culture.prestige\_sim}")
        with self.voiceover(
            "A second bias is prestige. <bookmark mark='a'/> Learners copy the most successful of the few people "
            "they observe. <bookmark mark='b'/> In Psyche, a useless marker, say a style of dress, starts in ten "
            "percent of the population, mostly among the skilled. <bookmark mark='c'/> It does nothing, but it rides "
            f"along with skill. In the median of twenty-one runs it reaches {spct(d['share'][-1])} after thirty "
            f"generations, and it passes half in {n_over} runs of the twenty-one. <bookmark mark='d'/> It's why "
            "fashions follow celebrities, and why a successful group's customs spread along with its techniques."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(line), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def faithful(self):
        head = heading(r"Copy faithfully")

        def box(opaque: bool):
            b = Rectangle(width=1.8, height=1.3, stroke_color=GREY_B, fill_color="#1A1F28" if opaque else "#14181F",
                          fill_opacity=1 if opaque else 0.3)
            bolt = Rectangle(width=0.7, height=0.1, color=PERSON, fill_opacity=1, stroke_width=0).move_to(
                b.get_top() + DOWN * 0.15)
            door = Rectangle(width=0.4, height=0.5, stroke_color=GOOD, fill_opacity=0).move_to(
                b.get_right() + LEFT * 0.3)
            food = Dot(b.get_center() + RIGHT * 0.3 + DOWN * 0.25, radius=0.1, color=GOOD)
            inner = VGroup(food) if not opaque else VGroup()
            return VGroup(b, bolt, door, inner)

        opaque = box(True).move_to([-4.8, 1.0, 0])
        clear = box(False).move_to([-2.2, 1.0, 0])
        lo = label(r"opaque box", font_size=16, color=GREY_A).next_to(opaque, DOWN, buff=0.2)
        lc = label(r"transparent box", font_size=16, color=GREY_A).next_to(clear, DOWN, buff=0.2)
        steps = VGroup(word_chip(r"1. \ tap the bolt on top", color=PERSON, font_size=16, width=3.4),
                       word_chip(r"2. \ open the door, \ take the reward", color=GOOD, font_size=16, width=3.4))
        steps.arrange(DOWN, buff=0.2).move_to([-3.5, -1.4, 0])
        useless = label(r"useless, \ as the transparent box shows", font_size=14, color=AUTH).next_to(steps[0], RIGHT,
                                                                                                buff=0.1)
        rows = rows_of([
            (r"Horner and Whiten, \ 2005: \ a demonstrator does an unnecessary action, \ then the useful one", WHITE),
            (r"with a transparent box, \ young chimpanzees skipped the useless action; \ children copied it", PERSON),
            (r"overimitation: \ San children in the Kalahari did it too (Nielsen and Tomaselli, \ 2010); \ Aka "
             r"forager children in the Congo Basin did it at one of the lowest rates recorded (Berl and Hewlett, \ "
             r"2015)",
             WORLD),
            (r"found wherever it has been tested, \ in varying amounts: \ faithful copying of what you do not "
             r"understand is how a skill too complex to reinvent can be inherited", GOOD),
        ], 6.0, 19, 0.34).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Horner \& Whiten (2005); \ Nielsen \& Tomaselli (2010); \ Berl \& Hewlett (2015)")
        with self.voiceover(
            "Cumulative culture also needs faithful copying. <bookmark mark='a'/> In 2005 Victoria Horner and Andrew "
            "Whiten showed young chimpanzees and children a puzzle box. A demonstrator first tapped a bolt on top, "
            "which did nothing, and then opened a door to get a reward. <bookmark mark='b'/> When the box was "
            "transparent, so that the tapping was plainly useless, the chimpanzees skipped it. The children copied "
            "it. <bookmark mark='c'/> It's called overimitation. San children in the Kalahari did it too. Aka "
            "forager children in the Congo Basin did it at one of the lowest rates ever recorded. <bookmark mark='d'/> It's "
            "been found wherever it's been tested, in varying amounts. Copying what you don't understand sounds "
            "foolish, but it's how a skill too complex to reinvent can be inherited."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(opaque), FadeIn(clear), FadeIn(lo), FadeIn(lc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(steps))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(useless), Indicate(clear[1], color=AUTH))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def tasmania(self):
        d = load("tasmania")
        head = heading(r"Population size and lost skills")
        A = axes([0, 60], [0, 100], x_length=5.0, y_length=2.6, xticks=[0, 20, 40, 60], yticks=[0, 50, 100],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"generation",
                 ylabel=r"best skill", center=[-3.4, 0.6, 0], font_size=14)
        gens = np.arange(61)
        cols = {20: AUTH, 50: GREY_A, 200: GOOD}
        lines = VGroup(*[curve(A.ax, gens, np.minimum(d[f"path_{n}"], 100), cols[n], stroke_width=4) for n in
                         (20, 50, 200)])
        nudge = {20: DOWN * 0.14, 50: UP * 0.14, 200: ORIGIN}
        names = VGroup(*[label(rf"$N = {n}$", font_size=16, color=cols[n]).next_to(
            A.ax.c2p(60, min(float(d[f"path_{n}"][-1]), 100)), RIGHT, buff=0.1).shift(nudge[n]) for n in (20, 50, 200)])
        eq = MathTex(r"\Delta \bar z = \beta(\gamma + \ln N) - \alpha", font_size=30, color=MODEL)
        eq.move_to([-3.4, -2.2, 0])
        rows = rows_of([
            (r"Henrich, \ 2004: \ each learner copies the most skilled person of the last generation, \ and lands "
             r"on average $\alpha$ below, \ with luck of spread $\beta$", WHITE),
            (rf"the best of $N$ copies gains $\beta(\gamma + \ln N) - \alpha$: \ below about "
             rf"{d['critical']:.0f} people a skill decays, \ above it, \ it improves", MODEL),
            (r"his case: \ Tasmania, \ cut off by rising seas about 10{,}000 years ago, \ whose toolkit seems to have "
             r"shrunk", WORLD),
            (r"Vaesen and colleagues, \ 2016: \ the models need restrictive assumptions, \ and among hunter-gatherers "
             r"toolkit complexity tracks environment better than population; \ contested", AUTH),
        ], 6.0, 19, 0.34).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{culture.tasmania}; \ Henrich (2004); \ Vaesen et al.\ (2016)")
        with self.voiceover(
            "The third model asks why skills accumulate, and why they're sometimes lost. <bookmark mark='a'/> In "
            "2004 Joseph Henrich supposed that each learner copies the most skilled person of the last generation, "
            "and lands on average a little below, alpha, with some luck, beta. <bookmark mark='b'/> The best of N "
            "such copies gains beta times gamma plus log N, minus alpha. Below a critical population, here about "
            f"{d['critical']:.0f} people, a skill decays. Above it, it improves. You can watch it: twenty learners "
            "lose the skill, two hundred build on it. <bookmark mark='c'/> His case was Tasmania, cut off from "
            "Australia by rising seas about ten thousand years ago, whose toolkit seems to have shrunk. "
            "<bookmark mark='d'/> In 2016 Krist Vaesen and colleagues argued that the models need restrictive "
            "assumptions, and that among hunter-gatherers, toolkit complexity tracks the environment better than "
            "population. Henrich and colleagues replied. It's contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(eq), *[Create(l_) for l_ in lines], FadeIn(names), run_time=3.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
