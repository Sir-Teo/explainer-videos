from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Information(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Information in biology", r"Is the genetic code really a code?", lit=(1953, 2000),
                            part=PART)
        with self.voiceover("Chapter ten. Information in biology."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.code()
        self.debate()
        self.parity()

    def code(self):
        d = load("code")
        head = label(r"The genetic code, \ counted", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        deg = d["degeneracy"]
        items = list(deg.items())
        ax = Axes(x_range=[0, len(items), 1], y_range=[0, 6.5, 1], x_length=7.0, y_length=3.0,
                  axis_config={"color": GREY_B, "font_size": 16}, y_axis_config={"include_numbers": True},
                  x_axis_config={"include_ticks": False}).move_to([-2.6, 0.4, 0])
        bars = VGroup()
        labs = VGroup()
        for i, (aa, k) in enumerate(items):
            col = BAD if aa == "*" else GENE
            r = Rectangle(width=ax.x_axis.unit_size * 0.75, height=ax.y_axis.unit_size * k, stroke_width=0,
                          fill_color=col, fill_opacity=0.7).move_to(ax.c2p(i + 0.5, k / 2))
            bars.add(r)
            labs.add(label(r"stop" if aa == "*" else aa, font_size=13, color=col).next_to(r, DOWN, buff=0.08))
        al = label(r"codons per amino acid", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1)
        side = stack([(r"64 codons \ $\to$ \ 20 amino acids and stop", WHITE),
                      (r"capacity: \ $\log_2 64 = 6$ bits per codon", GREY_A),
                      (r"entropy of the output \ (codons uniform): \ " + f"{d['entropy']:.2f}" + r" bits", GENE),
                      (r"redundancy: \ " + f"{d['redundancy']:.2f}" + r" bits per codon", ORG),
                      (r"single-base mutations that change nothing: \ " + f"{100 * d['silent_share']:.0f}" + r"\%", OK),
                      (r"at the third position: \ " + f"{100 * d['third_position_silent']:.0f}" + r"\%", OK),
                      (r"a code that buffers errors \ (Freeland and Hurst, \ 1998)", GOAL)], font_size=19,
                     aligned_edge=LEFT, width=5.0).move_to([4.4, -0.3, 0])
        with self.voiceover(
            "The genetic code maps three-letter words of DNA to amino acids. <bookmark mark='a'/>Sixty-four codons "
            "map to twenty amino acids and a stop signal, so most amino acids have several codons: leucine, serine "
            "and arginine have six each; methionine and tryptophan have one. <bookmark mark='b'/>A codon has a "
            "capacity of six bits. The amino-acid output, if codons were used equally, has an entropy of about four "
            "point two bits, so nearly two bits per codon are redundancy. <bookmark mark='c'/>The redundancy is "
            "structured. The Reasoner tries every single-letter mutation of every codon: about a quarter change "
            "nothing, and at the third letter two thirds are silent. <bookmark mark='d'/>Stephen Freeland and "
            "Laurence Hurst found the standard code better at buffering errors than nearly all of a million random "
            "alternatives."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(al))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(labs),
                      FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
            vo.wait_until("d")
            self.play(FadeIn(side[6]))
        self.clear_scene()

    def debate(self):
        head = label(r"A code, \ or a metaphor?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Shannon information", r"any reliable correlation carries it: \ smoke carries information about fire; \ "
                                     r"so does every cause about its effect", GREY_A),
            (r"the parity problem", r"in that sense environments carry information about phenotypes as much as genes "
                                    r"do", BAD),
            (r"Maynard Smith \ (2000)", r"genes carry \textit{semantic} information: \ the code is arbitrary, \ like a "
                                        r"language, \ and was shaped by selection to signal", GENE),
            (r"teleosemantics", r"information as what a signal was selected to indicate \ (Millikan; \ Shea)", ORG),
            (r"Godfrey-Smith", r"the code is real for the narrow step from codon to amino acid; \ beyond it the talk "
                               r"is metaphor", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Is the genetic code a code in the sense that language is? <bookmark mark='a'/>In Shannon's sense, "
            "any reliable correlation carries information: smoke carries information about fire. "
            "<bookmark mark='b'/>But then environments carry information about the organism as much as genes do, "
            "which undercuts the special status of genes. <bookmark mark='c'/>John Maynard Smith argued that genes "
            "carry semantic information: the mapping from codon to amino acid is arbitrary, like the link between a "
            "word and its meaning, and was shaped by selection to do its job. <bookmark mark='d'/>Teleosemantics, "
            "from Ruth Millikan and Nicholas Shea, makes information a matter of what a signal was selected to "
            "indicate. <bookmark mark='e'/>Peter Godfrey-Smith's verdict: there is a genuine code for the narrow step "
            "from codon to amino acid; beyond that, talk of genetic programs and blueprints is metaphor."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def parity(self):
        d = load("parity")
        head = label(r"The parity thesis, \ in bits", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        g = VGroup(Circle(radius=0.38, color=GENE, fill_opacity=0.3), MathTex(r"G", font_size=30, color=GENE))
        e = VGroup(Circle(radius=0.38, color=ORG, fill_opacity=0.3), MathTex(r"E", font_size=30, color=ORG))
        p = VGroup(Circle(radius=0.42, color=GOAL, fill_opacity=0.3), MathTex(r"P", font_size=30, color=GOAL))
        g.move_to([-5.4, 1.2, 0])
        e.move_to([-5.4, -0.6, 0])
        p.move_to([-3.2, 0.3, 0])
        ag = Arrow(g.get_right(), p.get_left(), buff=0.08, color=GENE, stroke_width=3)
        ae = Arrow(e.get_right(), p.get_left(), buff=0.08, color=ORG, stroke_width=3)
        gl = label(r"gene", font_size=16, color=GENE).next_to(g, UP, buff=0.1)
        el = label(r"diet", font_size=16, color=ORG).next_to(e, DOWN, buff=0.1)
        rule = label(r"tall $\iff G = 1$ and $E = 1$", font_size=17, color=GOAL).next_to(p, DOWN, buff=0.3)
        mi = MathTex(r"I(X; P) = \sum_{x, p} \Pr(x, p) \log_2 \frac{\Pr(x, p)}{\Pr(x) \Pr(p)}", font_size=30).move_to(
            [2.8, 1.8, 0])
        hd = [r"\text{background}", r"I(G; P)", r"I(E; P)"]
        rows = []
        for k, lab in (("both vary", r"both vary"), ("diet fixed", r"everyone well fed"),
                       ("gene fixed", r"everyone has the gene")):
            v = d[k]
            rows.append([MathTex(r"\text{" + lab + "}", font_size=22),
                         MathTex(f"{v['gene']:.2f}", font_size=24, color=GENE),
                         MathTex(f"{v['diet']:.2f}", font_size=24, color=ORG)])
        grid = ValueGrid(hd, rows, col_w=[3.8, 1.5, 1.5], cell_h=0.55, font_size=20).move_to([2.8, 0.0, 0])
        lab = label(r"bits", font_size=15, color=GREY_A).next_to(grid, RIGHT, buff=0.15)
        rows2 = stack([(r"symmetric causes, \ symmetric information", WHITE),
                       (r"which cause `carries the information' depends on what the background holds fixed", GOAL),
                       (r"Griffiths and Gray: \ Shannon information cannot single out the genes", BAD)],
                      font_size=19, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Reasoner can make the parity problem exact. <bookmark mark='a'/>A toy organism grows tall only if it "
            "has a certain gene and a good diet. <bookmark mark='b'/>Mutual information measures, in bits, how much "
            "knowing a cause reduces uncertainty about the phenotype. <bookmark mark='c'/>If genes and diets both "
            "vary, each carries the same zero point three one bits: the two causes are perfectly symmetric. "
            "<bookmark mark='d'/>If everyone is well fed, all the variation in height comes from the gene, which "
            "now carries a full bit, and diet carries none. <bookmark mark='e'/>If everyone has the gene, the "
            "situation reverses. <bookmark mark='f'/>So which cause carries the information depends on what the "
            "background holds fixed, not on whether the cause is a gene. That is Paul Griffiths and Russell Gray's "
            "parity thesis: if genes are special, it must be in a semantic sense, like Maynard Smith's, not Shannon's."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(e), FadeIn(p), GrowArrow(ag), GrowArrow(ae), FadeIn(gl), FadeIn(el),
                      FadeIn(rule))
            vo.wait_until("b")
            self.play(Write(mi), FadeIn(grid.head), Create(grid.rule), FadeIn(lab))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[0])), FadeIn(rows2[0]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*grid.cell[1])), Indicate(ag, color=GENE))
            vo.wait_until("e")
            self.play(FadeIn(VGroup(*grid.cell[2])), Indicate(ae, color=ORG))
            vo.wait_until("f")
            self.play(FadeIn(rows2[1]), FadeIn(rows2[2]))
        self.clear_scene()
