from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.salmon()
        self.explained()
        self.the_chain()
        self.objectives()

    def salmon(self):
        head = heading(r"2009: \ a salmon in a brain scanner")
        sc = scanner(4.4).move_to([-4.1, -0.3, 0])
        f = fish(2.1).move_to(sc.bore.get_center())
        spot = VGroup(*[Square(side_length=0.09, stroke_width=0, fill_color=THRESH, fill_opacity=1).move_to(
            f.get_center() + f.head + np.array([dx, dy, 0])) for dx, dy in ((0, 0), (0.09, 0), (0, 0.09))])
        rows = rows_of([
            (r"one Atlantic salmon, \ not alive", WHITE),
            (r"shown photographs of people; \ asked what each person was feeling", WHITE),
            (r"analysed the usual way: \ a test in every voxel, \ ``active'' at $p < 0.001$", GREY_A),
            (r"result: \ a cluster of active voxels in the salmon's brain", THRESH),
        ], 6.2, 31).move_to([3.4, -0.2, 0])
        keep_in_frame(rows)
        src = published_tag(archive.BENNETT_2009.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "In 2009 a group of researchers in the United States put a salmon in a brain scanner. "
            "<bookmark mark='a'/> An Atlantic salmon, and, as their report takes care to say, not alive at "
            "the time. <bookmark mark='b'/> They showed the fish a series of photographs of people in "
            "social situations, and asked it to work out what emotion each person was feeling. "
            "<bookmark mark='c'/> Then they analysed the scans the way a good share of published studies "
            "did. Cut the image into small cubes, called voxels. Run a statistical test in every one. Call "
            "a voxel active if it passes at one in a thousand. <bookmark mark='d'/> And there it was. A "
            "small cluster of active voxels, in the brain of a dead fish, apparently thinking about human "
            "feelings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(sc))
            vo.wait_until("a")
            self.play(FadeIn(f, shift=RIGHT * 0.3), FadeIn(rows[0], shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(spot, scale=3.0), FadeIn(rows[3], shift=UP * 0.1))
            self.play(Indicate(spot, color=WHITE, scale_factor=1.6))
        self.clear_scene()

    def explained(self):
        s = load("salmon")
        head = heading(r"The fish was a statistics lesson")
        g = np.random.default_rng(8)
        n = 40
        grid = VGroup(*[Square(side_length=0.13, stroke_width=0, fill_color=NOISE,
                               fill_opacity=0.32) for _ in range(n * 25)]).arrange_in_grid(rows=25, buff=0.03)
        grid.move_to([-3.6, -0.1, 0])
        lucky = [int(k) for k in g.choice(n * 25, 1, replace=False)]
        cap = label(r"1{,}000 tests on noise: \ on average, one passes", font_size=26, color=GREY_A)
        cap.next_to(grid, DOWN, buff=0.2)
        rows = rows_of([
            (r"one test at $p < 0.001$: \ a false alarm once in a thousand", WHITE),
            (rf"1{{,}}000 tests: \ a {pct(s['chance_at'][0])} chance of at least one", THRESH),
            (r"a brain image: \ tens of thousands of tests, \ so false alarms are certain", THRESH),
            (r"with the standard corrections, \ the salmon's activity vanished", MODEL),
        ], 6.0, 31).move_to([3.5, -0.2, 0])
        keep_in_frame(rows)
        src = published_tag(archive.BENNETT_2009.cite)
        tag = note(r"the grid: schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The fish hadn't come back to life, and the scanner wasn't broken. The salmon was a statistics "
            "lesson, and you already know the statistics, from Part 4. <bookmark mark='a'/> A test at one "
            "in a thousand gives a false alarm one time in a thousand. That sounds safe. "
            "<bookmark mark='b'/> But run a thousand tests on pure noise, and the chance that at least one "
            f"of them passes is {100 * s['chance_at'][0]:.0f} percent. <bookmark mark='c'/> A brain image "
            "isn't a thousand tests. It's tens of thousands. Some voxels will pass by chance, in any "
            "brain, alive or dead. <bookmark mark='d'/> The researchers then applied the standard "
            "corrections for the number of tests, and the salmon's activity vanished. Their point wasn't "
            "about fish. By the count they cite, something like a quarter of the brain-imaging papers in the main "
            "journals at the time were still reporting results without that correction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(grid, lag_ratio=0.002), FadeIn(cap), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[grid[k].animate.set_fill(THRESH, opacity=1.0) for k in lucky], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(*[grid[k].animate.set_fill(NOISE, opacity=0.32) for k in lucky], FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def the_chain(self):
        head = heading(r"Between a thought and a coloured blob")
        top = chain([r"neurons fire", r"currents at synapses", r"blood flow changes", r"the magnet's signal"],
                    [SPIKE, EEGC, BLOOD, BLOOD], width=12.8, font_size=30, height=1.15).move_to([0, 1.75, 0])
        low = chain([r"a statistical model", r"a threshold", r"a coloured map", r"a statement about a mind"],
                    [MODEL, THRESH, DATA, P.ACCENT], width=12.8, font_size=30, height=1.15).move_to([0, 0.15, 0])
        boxes = [*top.boxes, *low.boxes]
        links = [*top.arrows, None, *low.arrows]
        notes = rows_of([
            (r"A scan looks like a photograph of thinking. \ It is the end of a chain, \ and each link rests "
             r"on an assumption.", WHITE),
            (r"The last step is the largest, \ and the picture does not show it.", THRESH),
            (r"This part walks the chain, \ so that you can see where it holds and where it has broken.",
             P.ACCENT),
        ], 12.6, 31, 0.25).move_to([0, -2.2, 0])
        with self.voiceover(
            "A brain scan in a newspaper looks like a photograph of someone thinking. It isn't a "
            "photograph. <bookmark mark='a'/> It's the last link of a chain. Neurons fire. Currents flow "
            "at their synapses. A few seconds later, the blood supply to that patch of tissue changes. "
            "That changes a magnetic signal. The signal is fitted with a statistical model, the fit is "
            "passed through a threshold, and what survives is painted onto a picture of a brain. "
            "<bookmark mark='b'/> Every one of those links rests on an assumption. And then there's one "
            "more step, the largest, which the picture doesn't show: from the coloured map to a statement "
            "about a mind. <bookmark mark='c'/> Part 7 read the brain through damage. This part reads it "
            "through instruments. We'll walk the chain link by link, so that you can see where it holds, "
            "and where, more than once, it has broken."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("a")
            for i in range(7):
                self.play(FadeIn(boxes[i], shift=RIGHT * 0.1), *([GrowArrow(links[i - 1])] if i and links[i - 1] else []),
                          run_time=1.6)
            vo.wait_until("b")
            self.play(GrowArrow(links[6]), FadeIn(boxes[7], shift=RIGHT * 0.1), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2], shift=UP * 0.1))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 8", font_size=34, color=GREY_B), label(r"Reading the Brain", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"one neuron's tuning curve; \ why the scalp shows only cells that act together",
            r"averaging: \ a signal pulled out of noise at a rate of $\sqrt{n}$",
            r"MRI in five minutes, \ and the slow echo in the blood that fMRI measures",
            r"the linear model of an experiment, \ and a hundred thousand tests",
            r"three ways a map misleads: \ thresholds, circular selection, reading it backwards",
            r"what scans have settled, \ what is sold, \ and how many people a study needs",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part eight: reading the brain. <bookmark mark='a'/> We'll listen to one neuron, and see why an "
            "electrode on the scalp can hear only cells that act together. <bookmark mark='b'/> We'll pull "
            "a signal out of noise by averaging, and compute how fast that works. <bookmark mark='c'/> "
            "We'll do magnetic resonance imaging in five minutes, and meet the slow echo in the blood that "
            "a functional scan really measures. <bookmark mark='d'/> We'll build the linear model that "
            "turns an experiment into a map, and face the hundred thousand tests inside it. "
            "<bookmark mark='e'/> We'll see three ways a map misleads: the threshold, choosing voxels by "
            "the answer, and reading the map backwards. <bookmark mark='f'/> And we'll end with what scans "
            "have settled, what's being sold, and how many people a brain study needs."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark_, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
