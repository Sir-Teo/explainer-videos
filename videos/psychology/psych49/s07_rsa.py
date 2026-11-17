from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Rsa(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.matrices()
        self.scores()

    def card(self):
        card = chapter_card(6, r"Geometry", r"What is the shape of a representation?", lit=(), part=PART,
                            scale=("brain",), marr=("what",))
        with self.voiceover("Chapter six. Geometry."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def idea(self):
        head = heading(r"Compare distances, \ not voxels")
        rows = rows_of([
            (r"2008: \ Nikolaus Kriegeskorte, \ Marieke Mur and Peter Bandettini proposed representational similarity "
             r"analysis", WHITE),
            (r"for every pair of stimuli, \ how different are the region's patterns? \ the table of those distances "
             r"is the representational dissimilarity matrix", MODEL),
            (r"the same table can be made from a model, \ from behaviour (Part 22's similarity judgments), \ from "
             r"a monkey's neurons, \ or from a network's layer", PERSON),
            (r"compare the tables, \ and very different measurements meet: \ no voxel needs to match a neuron", GOOD),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Kriegeskorte et al.\ (2008)")
        with self.voiceover(
            "Geometry asks a different question: not where, but what shape. <bookmark mark='a'/> In 2008 Nikolaus "
            "Kriegeskorte, Marieke Mur and Peter Bandettini proposed representational similarity analysis. "
            "<bookmark mark='b'/> For every pair of stimuli, how different are the region's patterns? The table of "
            "those distances is the representational dissimilarity matrix. <bookmark mark='c'/> The same table can be "
            "made from a model, from behaviour, like Part 22's similarity judgments, from a monkey's neurons, or from "
            "a layer of a neural network. <bookmark mark='d'/> Compare the tables, and very different measurements "
            "meet. No voxel has to be matched to a neuron."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def matrices(self):
        d = load("rsa")
        head = heading(r"Three tables of distances")
        G = np.asarray(d["grand"], float)
        cat = np.asarray(d["cat"])
        size = np.asarray(d["size"])
        mc = (cat[:, None] != cat[None, :]).astype(float)
        ms = np.abs(size[:, None] - size[None, :]) / 2
        h = 3.2
        lo, hi = np.nanmin(G[G > 0]), np.nanmax(G)
        m1 = heat(np.nan_to_num(G), h, lo, hi, center=[-4.5, 0.6, 0], smooth=False)
        m2 = heat(mc, h, 0, 1, center=[0, 0.6, 0])
        m3 = heat(ms, h, 0, 1, center=[4.5, 0.6, 0])
        caps = VGroup(label(r"the region (mean of 12 people)", font_size=17, color=THRESH).next_to(m1, DOWN, buff=0.15),
                      label(r"model: \ category", font_size=17, color=MODEL).next_to(m2, DOWN, buff=0.15),
                      label(r"model: \ size", font_size=17, color=PERSON).next_to(m3, DOWN, buff=0.15))
        rows = rows_of([
            (r"24 stimuli in four categories of six; \ size varies within each category; \ dark means similar", WHITE),
            (r"the region's table shows four dark blocks: \ category, \ and inside each block a gradient: \ size", PERSON),
        ], 12.4, 20, 0.28).move_to([0, -2.75, 0])
        tag = psyche_tag(r"\texttt{neurodata.rsa}")
        with self.voiceover(
            "Psyche makes a region where the answer is known. <bookmark mark='a'/> Twenty-four stimuli in four "
            "categories of six, and a size that varies within each category. Each table is twenty-four by "
            "twenty-four, and dark means similar. <bookmark mark='b'/> The region's table, averaged over twelve "
            "people, shows four dark blocks, the categories, and inside each block a gradient, the size. The two "
            "model tables say what each idea predicts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(m1), FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(FadeIn(m2), FadeIn(m3), FadeIn(caps[1]), FadeIn(caps[2]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.wait(1.5)
        self.clear_scene()

    def scores(self):
        d = load("rsa")
        head = heading(r"How good is a model, \ and how good could it be?")
        A = axes([0.3, 2.7], [0, 1], x_length=4.0, y_length=3.0, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"Spearman $\rho$ with each person", center=[-3.8, 0.3, 0],
                 font_size=12)
        b = bars(A.ax, [1, 2], [d["r_category"], d["r_size"]], [MODEL, PERSON], width=0.6)
        band = Polygon(A.ax.c2p(0.3, d["ceiling_low"]), A.ax.c2p(2.7, d["ceiling_low"]), A.ax.c2p(2.7, d["ceiling_high"]),
                       A.ax.c2p(0.3, d["ceiling_high"]), stroke_width=0, fill_color=GREY_B, fill_opacity=0.35)
        names = VGroup(label(r"category", font_size=14, color=MODEL).next_to(A.ax.c2p(1, 0), DOWN, buff=0.1),
                       label(r"size", font_size=14, color=PERSON).next_to(A.ax.c2p(2, 0), DOWN, buff=0.1))
        rows = rows_of([
            (rf"the category model correlates {d['r_category']:.2f} with each person's table, \ the size model "
             rf"{d['r_size']:.2f}", MODEL),
            (rf"the grey band is the noise ceiling: \ how well the group's own table predicts each person, \ "
             rf"{d['ceiling_low']:.2f} to {d['ceiling_high']:.2f}", GREY_B),
            (r"no model can beat the ceiling; \ a model near it explains what the data can show", GOOD),
            (r"here neither reaches it: \ the region holds both, \ and a model of category and size together would "
             r"do better", YOU),
        ], 6.2, 19, 0.38).move_to([3.3, -0.1, 0])
        with self.voiceover(
            "So how good is each model, and how good could any model be? <bookmark mark='a'/> The category model "
            "correlates about zero point six four with each person's table, the size model about zero point four "
            "five. <bookmark mark='b'/> The grey band is the noise ceiling: how well the group's own table predicts "
            "each person, here about zero point nine. <bookmark mark='c'/> No model can beat that. A model near it "
            "explains everything the data can show. <bookmark mark='d'/> Here neither model reaches it, because the "
            "region holds both. A model of category and size together would do better."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(band))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
