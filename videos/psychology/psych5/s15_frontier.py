from __future__ import annotations

from videos.psychology.psych5.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.gidon()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ how much is one neuron?", r"What is still not known about the "
                            r"smallest part?", lit={2020: r"graded spikes in human dendrites"}, part=PART,
                            scale=("neuron", "circuit"), marr=("what",))
        with self.voiceover(
            "Chapter fourteen. The frontier: how much is one neuron?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def gidon(self):
        d = archive.GIDON_2020.data
        head = heading(r"2020: \ a dendritic signal that shrinks when pushed harder")
        import numpy as np

        A = axes([0, 3], [0, 1.15], x_length=5.6, y_length=3.3, xticks=[1, 2, 3], yticks=[], xlabel=r"strength of the "
                 r"input (1 = threshold)", ylabel=r"size of the response", center=[-3.5, -0.6, 0], font_size=20)
        ax = A.ax
        x = np.linspace(0, 3, 200)
        ordinary = np.where(x >= 1, 1.0, 0.0)
        graded = np.where(x >= 1, np.exp(-(x - 1) / 0.6), 0.0)
        l1 = curve(ax, x, ordinary, LEAK, stroke_width=3)
        l2 = curve(ax, x, graded, THRESH, stroke_width=4)
        l1_l = label(r"the axon's signal: \ all or none", font_size=22, color=LEAK).move_to(ax.c2p(2.1, 1.08))
        l2_l = label(r"the dendritic spike reported", font_size=22, color=THRESH).move_to(ax.c2p(2.25, 0.6))
        side = VGroup(
            wrapped_label(r"In slices of human cortex, removed in surgery, some dendrites of the upper layers "
                          r"gave calcium spikes that were largest for an input just at threshold and smaller "
                          r"for stronger ones.", 6.0, 26, WHITE),
            wrapped_label(r"A branch like that responds to ``one input, but not both''. \ In the authors' models "
                          r"it computes the table of chapter 11 by itself.", 6.0, 26, MODEL),
            wrapped_label(r"The limits: \ tissue outside the body; \ and whether other species have the same "
                          r"spikes is not known.", 6.0, 26, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.4, 0])
        keep_in_frame(side)
        src = published_tag(archive.GIDON_2020.cite)
        tag = note(r"schematic curves, not the paper's data").to_corner(DR, buff=0.2)
        with self.voiceover(
            "How much one neuron computes is an open question, and it moved recently. <bookmark mark='a'/> In "
            "2020 a group in Berlin recorded from the dendrites of neurons in human cortex, in slices of "
            "tissue that had been removed during surgery for epilepsy or tumours. In the upper layers they "
            "found a dendritic spike carried by calcium that did something no textbook spike does. "
            "<bookmark mark='b'/> The axon's signal is all or none: at threshold it appears at full size, "
            "and stays that size. <bookmark mark='c'/> This one was largest for an input just at threshold, "
            "and smaller for stronger inputs. <bookmark mark='d'/> Think what a branch like that computes. "
            "One input: a big response. Two inputs together: too strong, a small one. That's one but not "
            "both, the very table that a simple adding cell can't produce. In the authors' models a single "
            "dendrite does it. <bookmark mark='e'/> The cautions are theirs as well as ours. The tissue was "
            "outside the body. And almost nothing comparable has been recorded in other species, so nobody "
            "can yet say whether this is special to us. But it's a reminder that the Ledger's verdict on "
            "Hodgkin and Huxley was about one membrane, not about what neurons can do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(A))
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(l1_l), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(l2), FadeIn(l2_l), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[1], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        qs = VGroup(
            wrapped_label(r"1. \ How many numbers does it take to describe one neuron? \ Four equations for an "
                          r"axon; \ for a cortical cell with its dendrites, models run to thousands of "
                          r"compartments, and may still fall short.", 12.2, 28, WHITE),
            wrapped_label(r"2. \ Rate or timing? \ When does the exact moment of a spike carry information that "
                          r"a count does not?", 12.2, 28, WHITE),
            wrapped_label(r"3. \ What are the other cells for? \ Glia are as numerous as neurons, and they "
                          r"signal, slowly, with calcium.", 12.2, 28, WHITE),
            wrapped_label(r"4. \ Does the mind need this level at all? \ Which facts about thinking would be "
                          r"different if the membrane were different?", 12.2, 28, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.35, 0])
        star = wrapped_label(r"$\star$ \ Research problem: \ find the smallest change to the integrate-and-fire "
                             r"neuron that lets one cell compute ``one but not both'', and say what measurement "
                             r"on a real cell would show it.", 12.2, 27, P.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Four open questions. <bookmark mark='a'/> One. How many numbers does it take to describe a "
            "neuron? For the squid's axon, four equations. For a cortical cell with its whole dendritic "
            "tree, detailed models use thousands of compartments, and it isn't settled what the right "
            "simplification is. <bookmark mark='b'/> Two. Rate or timing? We said the strength of a stimulus "
            "is carried by the rate. In some systems the exact moment of a spike clearly matters too. How "
            "general that is, nobody knows. <bookmark mark='c'/> Three. Neurons aren't the only cells in the "
            "brain. Glial cells are roughly as numerous, and they signal to each other and to neurons, on a "
            "slower clock. What they contribute to computation is wide open. <bookmark mark='d'/> Four, and "
            "it's the one a psychologist should care about most. Does the mind need this level? If you "
            "changed the membrane and kept the input-output behaviour of every cell, would anything about "
            "thinking change? That's a question about what explains what, and it runs through the whole "
            "series. <bookmark mark='e'/> And the research problem. Find the smallest change to the "
            "integrate-and-fire neuron that lets a single cell compute one but not both. Then say what you'd "
            "measure on a real cell to find out whether it does."
        ) as vo:
            self.play(FadeIn(head))
            for mark, q in zip("abcd", qs):
                vo.wait_until(mark)
                self.play(FadeIn(q, shift=UP * 0.12))
            vo.wait_until("e")
            self.play(FadeIn(star, shift=UP * 0.15))
        self.clear_scene()
