from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Twins(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_kinds()
        self.clouds()
        self.falconer()
        self.diagram()

    def card(self):
        card = chapter_card(3, r"The logic of twins", r"What do two kinds of twins let you subtract?",
                            lit={1875: r"Galton's twins"}, part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter three. The logic of twins."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two_kinds(self):
        head = heading(r"Two kinds of twins")
        mz = VGroup(twin_pair(MZC, True, 1.25), label(r"identical", font_size=36, color=MZC),
                    label(r"one egg, split", font_size=29, color=GREY_A)).arrange(DOWN, buff=0.14).move_to([-4.6, 1.0, 0])
        dz = VGroup(twin_pair(DZC, False, 1.25), label(r"fraternal", font_size=36, color=DZC),
                    label(r"two eggs", font_size=29, color=GREY_A)).arrange(DOWN, buff=0.14).move_to([-1.0, 1.0, 0])
        cells = [(r"genes that differ between people, shared", r"all", r"half, on average", GENE),
                 (r"born together, raised in one home", r"yes", r"yes", HOME)]
        table = VGroup()
        for i, (what, a, b, col) in enumerate(cells):
            y = -1.25 - 0.85 * i
            table.add(VGroup(wrapped_label(what, 4.6, 29, col).move_to([4.2, y, 0]),
                             label(a, font_size=34, color=MZC).move_to([-4.6, y, 0]),
                             label(b, font_size=34, color=DZC).move_to([-1.0, y, 0])))
        end = wrapped_label(r"If identical twins are more alike than fraternal twins, \ the extra likeness should come "
                            r"from the extra genes they share.", 5.2, 31, P.ACCENT).move_to([4.2, 1.3, 0])
        keep_in_frame(end)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Nature runs the experiment for us. There are two kinds of twins. <bookmark mark='a'/> "
            "Identical twins come from one fertilized egg that split in two. They have the same genes. "
            "<bookmark mark='b'/> Fraternal twins come from two eggs. Genetically they're ordinary "
            "brothers and sisters. Of the genes that differ between people, they share, on average, half. "
            "<bookmark mark='c'/> And both kinds are born at the same time and grow up in the same home. "
            "<bookmark mark='d'/> So here's the logic. If identical twins are more alike than fraternal "
            "twins, the extra likeness should come from the extra genes they share. The comparison was "
            "first made in the nineteen-twenties, and it's been made thousands of times since."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(mz[0]), FadeIn(dz[0]))
            vo.wait_until("a")
            self.play(FadeIn(mz[1]), FadeIn(mz[2]), FadeIn(table[0][0]), FadeIn(table[0][1]))
            vo.wait_until("b")
            self.play(FadeIn(dz[1]), FadeIn(dz[2]), FadeIn(table[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(table[1]))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def clouds(self):
        d = load("twins")
        head = heading(r"Three hundred pairs of each kind, \ from the Pool")
        panels = []
        for x0, key, name, col in ((-4.2, "mz", r"identical pairs", MZC), (1.1, "dz", r"fraternal pairs", DZC)):
            A = axes([-3, 3], [-3, 3], x_length=3.9, y_length=3.9, xticks=[], yticks=[], xlabel=r"one twin",
                     ylabel=r"the other twin", center=[x0, -0.35, 0])
            pts = scatter(A.ax, d[key][:, 0], d[key][:, 1], col, radius=0.035, opacity=0.65)
            title = label(name, font_size=32, color=col).next_to(A, UP, buff=0.12)
            r = label(rf"$r = {r2(d[f'r_{key}_shown'])}$", font_size=34, color=col).next_to(A.ax.c2p(-3, 3), DR, buff=0.12)
            panels.append(VGroup(A, pts, title, r))
        bar = share_bar([d["a2"], d["c2"], d["e2"]], [GENE, HOME, OWN], width=3.3, height=0.55, names=[r"A", r"C", r"E"],
                        font_size=28).move_to([5.1, 0.5, 0])
        bl = wrapped_label(r"planted in the registry: \ half genes, \ a fifth the shared home, \ the rest everything else",
                           3.5, 28, GREY_A).next_to(bar, UP, buff=0.2)
        end = wrapped_label(r"The method lives in the gap between the two clouds.", 3.5, 30, P.ACCENT).move_to([5.1, -1.7, 0])
        keep_in_frame(VGroup(bar, bl, end))
        tag = simulated_tag(r"simulated: the Pool's twin registry")
        with self.voiceover(
            "Here are three hundred pairs of each kind from the Pool's twin registry, for a trait where "
            "we've planted the truth. Half the variation comes from genes, a fifth from the shared home, "
            "and the rest from everything else. <bookmark mark='a'/> Each dot is a pair. One twin across, "
            f"the other up. Identical pairs: a correlation of {d['r_mz_shown']:.2f}. "
            f"<bookmark mark='b'/> Fraternal pairs: {d['r_dz_shown']:.2f}. A looser cloud. "
            "<bookmark mark='c'/> The whole method lives in the gap between those two clouds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(bar), FadeIn(bl), FadeIn(panels[0][0]), FadeIn(panels[0][2]))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][1], lag_ratio=0.003), FadeIn(panels[0][3]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][2]), FadeIn(panels[1][1], lag_ratio=0.003), FadeIn(panels[1][3]),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def falconer(self):
        d = load("twins")
        head = heading(r"Four lines of algebra")
        lines = VGroup(
            VGroup(label(r"identical twins share all of A and all of C:", font_size=31, color=MZC),
                   label(r"$r_{\!I} = a^2 + c^2$", font_size=40, color=MZC)),
            VGroup(label(r"fraternal twins share half of A and all of C:", font_size=31, color=DZC),
                   label(r"$r_{\!F} = \tfrac12 a^2 + c^2$", font_size=40, color=DZC)),
            VGroup(label(r"subtract, and double:", font_size=31, color=GENE),
                   label(r"$a^2 = 2\,(r_{\!I} - r_{\!F})$", font_size=40, color=GENE)),
            VGroup(label(r"and the other two shares:", font_size=31, color=WHITE),
                   label(r"$c^2 = 2\,r_{\!F} - r_{\!I}, \qquad e^2 = 1 - r_{\!I}$", font_size=38, color=WHITE)),
        )
        for ln in lines:
            ln.arrange(RIGHT, buff=0.5)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.85, 0])
        for ln in lines:
            ln[1].align_to(lines[1][1], LEFT)
        keep_in_frame(lines)
        res = rows_of([
            (rf"on the registry, in a large sample: \ $2\,({d['r_mz']:.2f} - {d['r_dz']:.2f}) = {d['est_h2']:.2f}$ "
             rf"\ (planted ${d['a2']:.1f}$)", GENE),
            (rf"shared home: \ ${d['est_c2']:.2f}$ \ (planted ${d['c2']:.1f}$); \ \ the rest: \ ${d['est_e2']:.2f}$ "
             rf"\ (planted ${d['e2']:.1f}$)", HOME),
        ], 12.4, 31, 0.18).to_edge(DOWN, buff=0.8)
        tag = simulated_tag(r"simulated: the Pool's twin registry, 200{,}000 pairs of each kind")
        with self.voiceover(
            "Now the algebra, which takes four lines. Call the three shares a squared, c squared and e "
            "squared. <bookmark mark='a'/> Identical twins share all of A and all of C. So their "
            "correlation is a squared plus c squared. <bookmark mark='b'/> Fraternal twins share half of "
            "A and all of C: half of a squared, plus c squared. <bookmark mark='c'/> Subtract. The c "
            "squareds cancel, and what's left is half of a squared. So the heritability is twice the "
            "difference between the two correlations. <bookmark mark='d'/> The shared home is what's left "
            "of the fraternal correlation, and E is whatever makes even identical twins differ. "
            f"<bookmark mark='e'/> On the registry, in a large sample: two times {d['r_mz']:.2f} minus "
            f"{d['r_dz']:.2f} is {d['est_h2']:.2f}. We planted {d['a2']:.1f}. The shared home comes out "
            f"at {d['est_c2']:.2f}, and the rest at {d['est_e2']:.2f}. This is called Falconer's formula. "
            "You can do it on a napkin, and that's part of why it's been applied to almost every trait "
            "you can name."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(lines[0][0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[0][1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
        self.clear_scene()

    def diagram(self):
        d = load("twins")
        bm = archive.BOUCHARD_MCGUE_1981.data
        head = heading(r"The same four lines as a picture: \ a path diagram")
        pd = path_diagram(8.6).move_to([-2.4, 0.35, 0])
        keep_in_frame(pd)
        rows = rows_of([
            (r"squares: \ what is measured. \ \ circles: \ causes nobody sees", WHITE),
            (r"curved lines: \ how alike the twins' causes are. \ Homes: 1. \ Genes: 1 or a half", GREY_A),
            (r"it is a model: \ it predicts the two correlations, \ and it can fail", P.ACCENT),
        ], 4.3, 29, 0.28).move_to([4.75, 0.75, 0])
        keep_in_frame(rows)
        bar = share_bar([d["classic_h2"], d["classic_c2"], d["classic_e2"]], [GENE, HOME, OWN], width=7.4, height=0.55,
                        names=[rf"genes ${d['classic_h2']:.2f}$", rf"home ${d['classic_c2']:.2f}$", rf"${d['classic_e2']:.2f}$"],
                        font_size=27).move_to([-2.6, -2.75, 0])
        bl = label(rf"{bm['studies']} studies of test scores: \ identical ${d['classic_r_mz']:.2f}$, \ fraternal "
                   rf"${d['classic_r_dz']:.2f}$", font_size=29, color=DATA).next_to(bar, UP, buff=0.14)
        keep_in_frame(VGroup(bar, bl))
        src = published_tag(archive.BOUCHARD_MCGUE_1981.cite)
        with self.voiceover(
            "Here are the same four lines as a picture, and it's the first of a kind you'll see throughout "
            "the series. <bookmark mark='a'/> Squares are things we measure: each twin's score. Circles "
            "are causes nobody sees: A, C and E for each twin. Arrows say what causes what. "
            "<bookmark mark='b'/> The curved lines say how alike the two twins' causes are. Their homes: "
            "the same, so one. Their genes: one for identical twins, a half for fraternal twins. Their E's "
            "aren't joined at all. That's what E means. <bookmark mark='c'/> A picture like this is a "
            "model. It predicts the two correlations, it can be fitted to data, and it can fail. It's "
            "called a path diagram, and from Part 44 on they get much bigger. <bookmark mark='d'/> Now "
            f"some classic data. A review of {bm['studies']} studies of intelligence-test scores put the "
            f"correlation for identical twins raised together at {d['classic_r_mz']:.2f}, and for "
            f"fraternal twins at {d['classic_r_dz']:.2f}. The formula turns that into "
            f"{d['classic_h2']:.2f} for genes, {d['classic_c2']:.2f} for the shared home, and "
            f"{d['classic_e2']:.2f} for the rest. Before we believe it, let's find out when the formula "
            "tells the truth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(pd.twins))
            vo.wait_until("a")
            self.play(FadeIn(pd.latents, lag_ratio=0.1), FadeIn(pd.arrows, lag_ratio=0.1), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(pd.links[1]), FadeIn(pd.link_labels[1]), run_time=1.0)
            self.play(Create(pd.links[0]), FadeIn(pd.link_labels[0]), FadeIn(rows[1]), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(bl), FadeIn(bar))
        self.clear_scene()
