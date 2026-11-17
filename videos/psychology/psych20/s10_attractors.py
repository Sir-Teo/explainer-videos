from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Attractors(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.settle()
        self.capacity()

    def card(self):
        card = chapter_card(9, r"Memories as valleys", r"How can a network store a memory and complete it from a "
                            r"fragment?", lit={1949: r"Hebb", 1982: r"Hopfield", 1985: r"Amit et al.",
                                               2020: r"Ramsauer et al."},
                            part=PART, scale=("cell", "mind"), marr=("how", "where"))
        with self.voiceover("Chapter nine. Memories as valleys."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rule(self):
        head = heading(r"A Hopfield network")
        eq1 = MathTex(r"W_{ij} = \frac{1}{N} \sum_{\mu=1}^{P} \xi^{\mu}_i\, \xi^{\mu}_j, \quad W_{ii} = 0",
                      font_size=38, color=WORD)
        eq2 = MathTex(r"s_i \leftarrow \operatorname{sign}\Big(\sum_j W_{ij}\, s_j\Big)", font_size=38, color=MODEL)
        eq3 = MathTex(r"E(\mathbf{s}) = -\tfrac{1}{2} \sum_{i,j} W_{ij}\, s_i s_j", font_size=38, color=CTX)
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.4).move_to([-3.3, 0.5, 0])
        rows = rows_of([
            (r"$N$ units, \ each $+1$ or $-1$; \ every unit connected to every other, \ symmetrically", WHITE),
            (r"to store patterns $\xi^\mu$: \ Hebb's rule, \ strengthen the link between units that agree", WORD),
            (r"to recall: \ each unit in turn takes the sign of its input", MODEL),
            (r"each update can only lower the energy $E$, \ or leave it: \ the network must come to rest", CTX),
            (r"the stored patterns are valleys of $E$: \ start near one, \ and the network rolls into it", WORD),
        ], 6.2, 22, 0.3).move_to([3.5, -0.1, 0])
        tag = historical_tag(r"Hopfield (1982); \ Hebb (1949)")
        with self.voiceover(
            "The context model describes what memory does. How might neurons do it? In 1982 the physicist John "
            "Hopfield wrote down a network that stores memories and recalls them from fragments. "
            "<bookmark mark='a'/> It has N units, each either on or off, plus or minus one, and every unit is "
            "connected to every other, with the same weight in both directions. <bookmark mark='b'/> To store a set "
            "of patterns, use Hebb's rule from Part 5: strengthen the connection between two units whenever they "
            "agree in a pattern, and weaken it when they disagree. <bookmark mark='c'/> To recall, update the units "
            "one at a time: each takes the sign of the weighted input from the others. <bookmark mark='d'/> Hopfield "
            "showed that this rule can only lower a quantity he called the energy, or leave it unchanged. So the "
            "network can't wander forever; it has to come to rest. <bookmark mark='e'/> And the stored patterns sit "
            "at the bottoms of valleys of that energy. Start the network near one of them, and it rolls down into "
            "it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eq1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eq2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(eq3), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def settle(self):
        h = load("hopfield")
        head = heading(r"Recall by settling")
        overlap_all = [float(s_ @ h["target"]) / len(s_) for s_ in h["steps"]]
        last = next((k for k, m in enumerate(overlap_all) if m >= 0.999), len(overlap_all) - 1)
        steps = h["steps"][:min(len(overlap_all), last + 3)]  # until the ring is back, and two frames at rest
        energy = h["energy"][:len(steps)]
        pics = [grid_pattern(s_, size=0.27) for s_ in steps]
        for p in pics:
            p.move_to([-3.6, 0.2, 0])
        target = grid_pattern(h["target"], size=0.16).move_to([-0.6, 1.6, 0])
        tl = label(r"stored", font_size=19, color=GREY_B).next_to(target, DOWN, buff=0.12)
        cue_l = label(r"the cue: \ 30\% of units flipped", font_size=20, color=LOST).next_to(pics[0], DOWN, buff=0.2)
        A = axes([0, len(steps) - 1], [float(energy.min()) * 1.05, 0], x_length=4.2, y_length=2.4,
                 xticks=list(range(0, len(steps), 2)), yticks=[], xlabel=r"quarter sweeps", ylabel=r"energy",
                 center=[3.9, 1.35, 0], font_size=17)
        ax = A.ax
        overlap = [float(s_ @ h["target"]) / len(s_) for s_ in steps]
        rows = rows_of([
            (r"100 units, \ 8 patterns stored, \ one of them a ring", WHITE),
            (r"cue it with a corrupted ring: \ a third of the units wrong", LOST),
            (rf"each unit takes the sign of its input; \ the energy falls; \ the overlap with the ring goes "
             rf"from {overlap[0]:.2f} to {overlap[-1]:.2f}", MODEL),
            (r"content-addressable memory: \ part of a memory is the address of the whole", WORD),
        ], 6.4, 22, 0.28).move_to([3.4, -1.95, 0])
        ptag = psyche_tag(r"\texttt{memory}: \ Hebbian weights, \ asynchronous updates")
        with self.voiceover(
            "Here it is with a hundred units on a ten by ten grid, storing eight patterns. One of them is a ring; "
            "the other seven are random. <bookmark mark='a'/> Cue the network with the ring corrupted, a third of "
            "its units flipped. <bookmark mark='b'/> Now let it run. Each unit, in turn, takes the sign of its "
            "input. Watch the energy on the right fall with every sweep, and the picture clean itself up. "
            "<bookmark mark='c'/> Within one sweep through the units, the ring is back, and the energy stops falling. <bookmark mark='d'/> This is content-"
            "addressable memory. There's no address, no file name, no index card: a part of the memory is the cue "
            "that recovers the whole, just as a smell or a fragment of a tune brings back a scene. A computer looks "
            "memories up by where they are. A Hopfield network looks them up by what they contain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(target), FadeIn(tl), FadeIn(rows[0]), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(pics[0]), FadeIn(cue_l), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(A))
            cur = pics[0]
            for k in range(1, len(pics)):
                part = curve_in(ax, np.arange(k + 1), energy[:k + 1], CTX, 4)
                self.play(FadeOut(cur), FadeIn(pics[k]), FadeIn(part), run_time=0.45)
                cur = pics[k]
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(cur, color=WORD, scale_factor=1.03))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def capacity(self):
        h = load("hopfield")
        head = heading(r"Derived: \ how many memories fit?")
        eq = MathTex(r"h_i = \sum_j W_{ij}\, \xi^1_j", r"=", r"\xi^1_i", r"+",
                     r"\frac{1}{N}\sum_{\mu \ne 1} \xi^\mu_i \sum_{j} \xi^\mu_j \xi^1_j", font_size=36)
        eq[2].set_color(WORD)
        eq[4].set_color(LOST)
        eq.move_to([0, 2.25, 0])
        noi = label(r"crosstalk: \ variance about $P/N$", font_size=20, color=LOST).next_to(eq[4], DOWN, buff=0.2)
        sig = label(r"signal", font_size=20, color=WORD).next_to(eq[2], DOWN, buff=0.2)
        sig.set_y(min(sig.get_y(), eq.get_bottom()[1] - 0.12 - sig.height / 2))
        A = axes([0, 0.3], [0, 1], x_length=6.0, y_length=3.0, xticks=[0, 0.138, 0.2, 0.3], yticks=[0, 0.5, 1],
                 xlabel=r"patterns per unit, \ $P/N$", ylabel=r"recalled almost perfectly", center=[-2.7, -1.25, 0],
                 font_size=17, xfmt=lambda v: f"{v:.3f}".rstrip("0").rstrip(".") if v else "0",
                 yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        c = curve_in(ax, h["loads"], h["recalled"], MODEL, 4)
        mark = DashedLine(ax.c2p(0.138, 0), ax.c2p(0.138, 1), color=WORD, stroke_width=2)
        rows = rows_of([
            (r"the stored pattern pulls itself back; \ every other pattern adds noise", WHITE),
            (r"while $P \ll N$ the noise is small; \ errors begin as $P/N$ grows, \ and feed on each other", LOST),
            (r"Amit, \ Gutfreund and Sompolinsky, \ 1985: \ recall collapses near $P = 0.138\,N$", WORD),
            (r"200 units, \ cued with 10\% of units flipped: \ the collapse, \ computed", MODEL),
            (r"modern Hopfield networks store far more, \ and their update is the attention of a transformer \ "
             r"(\emph{AI, \ Built})", CUE),
        ], 5.8, 21, 0.28).move_to([3.6, -1.2, 0])
        ptag = psyche_tag(r"\texttt{memory.hopfield\_capacity}: \ $N = 200$, \ 40 trials per load")
        with self.voiceover(
            "How many memories can such a network hold? <bookmark mark='a'/> Set the network to a stored pattern "
            "and look at the input to one unit. It splits in two. The first part is the pattern itself, pulling the "
            "unit toward the right value. The second is crosstalk from every other stored pattern, and for random "
            "patterns it's noise whose variance is about P over N, the number of patterns per unit. "
            "<bookmark mark='b'/> With few patterns, the signal wins everywhere. As P over N grows, some units start "
            "to flip, and each flipped unit makes the noise worse for the others. <bookmark mark='c'/> Daniel Amit, "
            "Hanoch Gutfreund and Haim Sompolinsky worked out the limit exactly in 1985, with the tools of "
            "statistical physics. Recall collapses suddenly near 0.138 patterns per unit. <bookmark mark='d'/> "
            "Here's the collapse computed, in a network of two hundred units. <bookmark mark='e'/> The idea has had "
            "a second life. Modern Hopfield networks, with a sharper energy, store vastly more, and their update "
            "rule turns out to be the attention of a transformer. That story is told in AI, Built."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(sig), FadeIn(noi), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(A), Create(mark), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(c), FadeIn(rows[3]), FadeIn(ptag), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
