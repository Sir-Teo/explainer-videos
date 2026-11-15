from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403

GAMES = (("board games", ("competition", "winning and losing", "skill", "luck")),
         ("card games", ("competition", "winning and losing", "luck", "skill")),
         ("patience", ("skill", "luck", "a single player")),
         ("ball games", ("competition", "skill", "the body")),
         ("ring-a-ring-o'-roses", ("amusement", "the body")))
FEATURE_COL = {"competition": CAT_A, "winning and losing": PROTO, "skill": MODEL, "luck": CAT_B,
               "a single player": EXEMPLAR, "the body": "#FFB86B", "amusement": GREY_B}


class Definitions(VoiceoverScene):
    def construct(self):
        self.card()
        self.classical()
        self.games()
        self.resemblance()
        self.fuzzy()

    def card(self):
        card = chapter_card(1, r"No definition", r"Is a concept a list of necessary and sufficient features?",
                            lit={1953: r"Wittgenstein", 1975: r"Rosch \& Mervis", 1978: r"McCloskey \& Glucksberg",
                                 1998: r"Hampton"},
                            part=PART, scale=("mind", "culture"), marr=("what",))
        with self.voiceover("Chapter one. No definition."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def classical(self):
        head = heading(r"The classical view")
        eq = MathTex(r"\text{bachelor}", r"\;=\;", r"\text{unmarried}", r"\;\wedge\;", r"\text{adult}", r"\;\wedge\;",
                     r"\text{male}", font_size=46).move_to([0, 1.7, 0])
        eq[0].set_color(CAT_A)
        rows = rows_of([
            (r"a concept is a definition: \ features each necessary, \ and together sufficient", WHITE),
            (r"then membership is all or none, \ every member is equally a member, \ and the boundary is sharp",
             CAT_A),
            (r"it is how logic, \ law and mathematics define their terms, \ and it was the default for two thousand "
             r"years", GREY_A),
            (r"but try it on \emph{bird}, \ or \emph{game}, \ or \emph{furniture}: \ every feature you list has "
             r"exceptions", LOST),
        ], 12.0, 27, 0.36).move_to([0, -0.9, 0])
        with self.voiceover(
            "The oldest answer is the classical view, going back to Aristotle. <bookmark mark='a'/> A concept is a "
            "definition: a list of features, each necessary, and together sufficient. A bachelor is an unmarried "
            "adult male. <bookmark mark='b'/> If that's right, membership is all or none, every member is equally a "
            "member, and the boundary is sharp. <bookmark mark='c'/> It's how logic, law and mathematics define "
            "their terms, and for two thousand years it was assumed to be how minds hold concepts too. "
            "<bookmark mark='d'/> But try it on bird. Flies? Not the penguin. Sings? Not the ostrich. Every feature "
            "you list has exceptions, and the ones without exceptions, like has feathers, don't tell you why a robin "
            "is a better bird than a penguin."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def games(self):
        head = heading(r"Wittgenstein's games")
        rows = VGroup()
        for name, feats in GAMES:
            chips = VGroup(*[word_chip(f, color=FEATURE_COL[f], font_size=19) for f in feats]).arrange(RIGHT, buff=0.15)
            rows.add(VGroup(label(name, font_size=24, color=WHITE), chips))
        for r in rows:
            r[0].move_to([-4.6, 0, 0])
            r[1].next_to([-3.0, 0, 0], RIGHT, buff=0)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, 0.6, 0])
        for r in rows:
            r[1].set_x(r[1].get_width() / 2 - 2.6)
            r[0].set_x(-4.7)
        quote = rows_of([
            (r"``Don't say: \ there \emph{must} be something common... \ but \emph{look} and see.'' \ "
             r"No feature runs through all of them: \ a network of overlapping similarities", WHITE),
            (r"Wittgenstein called it \emph{family resemblance}: \ like the build, \ the eyes, \ the gait of the members "
             r"of a family, \ overlapping and criss-crossing", PROTO),
        ], 12.4, 24, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(r"Wittgenstein (1953), \ \emph{Philosophical Investigations}, \ \S 66--67")
        with self.voiceover(
            "In the 1940s Ludwig Wittgenstein set a challenge. <bookmark mark='a'/> Consider the things we call "
            "games: board games, card games, patience, ball games, ring-a-ring-o'-roses. What is common to them all? "
            "Competition? Not patience. Winning and losing? Not ring-a-ring-o'-roses. Skill, luck? Sometimes. "
            "<bookmark mark='b'/> Don't say there must be something common, he wrote: look and see. What you find is "
            "a network of similarities, overlapping and criss-crossing, with no single thread running through. "
            "<bookmark mark='c'/> He called it family resemblance: like the build, the eyes, the way of walking of "
            "the members of a family. No feature is shared by everyone, and yet you can tell who belongs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.4), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(quote[0]))
            vo.wait_until("c")
            self.play(FadeIn(quote[1]))
        self.clear_scene()

    def resemblance(self):
        d = load("birds")
        head = heading(r"Family resemblance predicts typicality")
        names = [str(n) for n in d["names"]]
        F = d["F"]
        feats = [str(f) for f in d["features"]]
        cell = 0.36
        grid = VGroup()
        for i, n in enumerate(names):
            for j in range(len(feats)):
                grid.add(Square(cell * 0.9, stroke_width=0, fill_color=CAT_A if F[i, j] else "#1E2430",
                                fill_opacity=1).move_to([j * cell, -i * cell, 0]))
        grid.move_to([-3.1, -0.3, 0])
        rl = VGroup(*[label(n, font_size=18, color=GREY_A).next_to(grid[i * len(feats)], LEFT, buff=0.15)
                      for i, n in enumerate(names)])
        cl = VGroup(*[label(f, font_size=15, color=GREY_B).rotate(PI / 3).next_to(grid[j], UP, buff=0.08,
                                                                                    aligned_edge=LEFT)
                      for j, f in enumerate(feats)])
        fr = d["fr"]
        bar_w = 2.2
        frb = VGroup()
        for i, v in enumerate(fr):
            y = grid[i * len(feats)].get_y()
            frb.add(Rectangle(width=bar_w * v / fr.max(), height=cell * 0.7, stroke_width=0, fill_color=PROTO,
                              fill_opacity=0.85).move_to([grid.get_right()[0] + 0.4 + bar_w * v / fr.max() / 2, y, 0]))
            frb.add(label(f"{v:.0f}", font_size=16, color=GREY_A).move_to([grid.get_right()[0] + 0.55 + bar_w * v / fr.max()
                                                                           + 0.2, y, 0]))
        frl = label(r"family resemblance", font_size=20, color=PROTO).next_to(frb, UP, buff=0.2)
        rows = rows_of([
            (r"for each bird: \ count, \ over its features, \ how many other birds share them", PROTO),
            (r"Rosch and Mervis, \ 1975: \ with people's own feature lists, \ the members sharing most were the ones "
             r"rated most typical", WHITE),
            (r"the robin shares the most, \ the penguin and ostrich the least: \ typicality without a definition", MODEL),
        ], 3.3, 19, 0.3).move_to([5.0, -0.4, 0])
        ptag = psyche_tag(r"Psyche's bird table: \ features by common knowledge, \ an illustration")
        with self.voiceover(
            "In 1975 Eleanor Rosch and Carolyn Mervis turned family resemblance into a number. "
            "<bookmark mark='a'/> Here is a small table of birds and their features. For each bird, go through its "
            "features and count how many of the other birds share each one. That sum is its family resemblance. "
            "<bookmark mark='b'/> Rosch and Mervis did this with features that people themselves listed for members "
            "of everyday categories, and found that the members sharing the most features with the rest were the ones "
            "people rated most typical. <bookmark mark='c'/> In our table the robin and the sparrow share the most, "
            "and the penguin and the ostrich the least. Typicality comes out of the structure of the category, with "
            "no definition anywhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(grid), FadeIn(rl), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(frl), LaggedStart(*[FadeIn(b) for b in frb], lag_ratio=0.05),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def fuzzy(self):
        head = heading(r"Fuzzy boundaries")
        A = axes([1, 7], [0, 1], x_length=6.0, y_length=3.2, xticks=[1, 4, 7], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"rated typicality \ (1 = poor, \ 7 = excellent)",
                 ylabel=r"share saying ``yes, \ a member''", center=[-3.2, 0.1, 0], font_size=18)
        x = np.linspace(1, 7, 100)
        sig = 1 / (1 + np.exp(-(x - 3.2) * 2.0))
        c = curve(A.ax, x, sig, PROTO, 4)
        band = Rectangle(width=abs(A.ax.c2p(4.0, 0)[0] - A.ax.c2p(2.4, 0)[0]),
                         height=abs(A.ax.c2p(0, 1)[1] - A.ax.c2p(0, 0)[1]), stroke_width=0, fill_color=LOST,
                         fill_opacity=0.15).move_to(A.ax.c2p(3.2, 0.5))
        bl = wrapped_label(r"borderline: \ disagreement, \ and changes of mind", 2.4, 18, LOST)
        bl.move_to(A.ax.c2p(5.6, 0.3))
        sl = label(r"schematic", font_size=16, color=GREY_B).next_to(A, DOWN, buff=0.05).align_to(A, RIGHT)
        rows = rows_of([
            (r"McCloskey and Glucksberg, \ 1978: \ clear members and clear non-members, \ and in between a band where "
             r"people disagree, \ and change their own minds", WHITE),
            (r"Hampton, \ 1998: \ the chance of a \emph{yes} rises smoothly with an item's similarity to the category, "
             r"\ like a threshold on a noisy judgement", PROTO),
            (r"so membership is graded, \ and the grade is similarity: \ a judgement of how close, \ not a check of "
             r"a definition", MODEL),
        ], 5.8, 21, 0.3).move_to([3.6, 0.1, 0])
        tag = historical_tag(r"McCloskey \& Glucksberg (1978); \ Hampton (1998)")
        with self.voiceover(
            "And the boundaries are fuzzy. <bookmark mark='a'/> McCloskey and Glucksberg found clear members, clear "
            "non-members, and in between a band of items where people disagreed with each other, and, asked again, "
            "with themselves. <bookmark mark='b'/> James Hampton reanalysed their data in 1998. The chance that a "
            "person says yes, it's a member, rises smoothly with how similar the item is to the category, like a "
            "threshold applied to a noisy judgement. The curve here is a schematic of that shape. "
            "<bookmark mark='c'/> So membership is graded, and the grade is similarity. Which raises the next "
            "question: similarity to what?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(sl))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(band), FadeIn(bl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
