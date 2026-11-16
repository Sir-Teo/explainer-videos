from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Thresholds(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.permutation()
        self.clusters()
        self.byrule()

    def card(self):
        card = chapter_card(4, r"Thresholds at depth", r"When is a blob more than noise?", lit=(), part=PART,
                            scale=("brain",), marr=("how",))
        with self.voiceover("Chapter four. Thresholds at depth."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rules(self):
        d = load("thresholds")
        head = heading(r"Four rules, \ one map")
        mask = np.asarray(d["mask"], bool)
        truth = np.asarray(d["truth"])
        h = 2.6
        xs = [-4.95, -1.65, 1.65, 4.95]
        maps = Group(*[hits_map(np.asarray(d[k], bool), mask, truth, h, center=[x, 0.9, 0])
                       for k, x in zip(("unc", "fdr", "clus", "perm"), xs)])
        names = [r"$p < 0.001$ \ per voxel", r"false discovery rate 5\%", r"clusters, \ $p < 0.01$ to form",
                 r"permutation, \ maximum $t$"]
        caps = VGroup(*[VGroup(label(n, font_size=16, color=WHITE),
                               label(rf"{int(np.sum(np.asarray(d[k])))} voxels", font_size=15, color=THRESH))
                        .arrange(DOWN, buff=0.06).next_to(m, DOWN, buff=0.12)
                        for n, k, m in zip(names, ("unc", "fdr", "clus", "perm"), maps)])
        rows = rows_of([
            (r"Part 8 met the rules; \ here they are on one group map, \ gold where they are right and red where they "
             r"are wrong", WHITE),
            (r"per-voxel thresholds control each test, \ not the map; \ the false discovery rate controls the share "
             r"of declared voxels that are false", MODEL),
            (r"cluster rules ask whether a blob is bigger than noise makes blobs; \ permutation asks what the largest "
             r"$t$ would be if nothing were there", PERSON),
        ], 12.4, 19, 0.26).move_to([0, -2.6, 0])
        tag = psyche_tag(r"\texttt{neurodata.run\_pipeline}, \ 4-voxel smoothing")
        with self.voiceover(
            "Part 8 met the thresholding rules. Here are four of them on one group map: gold where they're right, red "
            "where they're wrong. <bookmark mark='a'/> A per-voxel threshold controls each test, not the map. The "
            "false discovery rate controls the share of the declared voxels that are false. <bookmark mark='b'/> "
            "Cluster rules ask whether a blob is bigger than noise makes blobs. And permutation asks what the largest "
            "t would be if nothing were there. Same data, four maps, and none of them finds every planted voxel."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(maps), FadeIn(caps), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.wait(1.0)
        self.clear_scene()

    def permutation(self):
        head = heading(r"Permutation: \ let the data make the null")
        steps = rows_of([
            (r"1. \ \ with no effect, \ each person's contrast map is as likely to be flipped in sign as not", SYMP),
            (r"2. \ \ so flip the signs of a random subset of people, \ and recompute the whole $t$ map", MODEL),
            (r"3. \ \ record the largest $t$, \ or the largest cluster, \ anywhere in the brain", PERSON),
            (r"4. \ \ do it thousands of times; \ the 95th percentile of those maxima is the threshold", GOOD),
        ], 12.4, 22, 0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"no assumption about the shape of the noise's spatial correlation: \ the brain's own "
                             r"noise sets the bar (Nichols and Holmes, \ 2002)", 12.0, 20, YOU).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Permutation lets the data make its own null. <bookmark mark='a'/> If there's no effect, each person's "
            "contrast map is as likely to point up as down. <bookmark mark='b'/> So flip the signs of a random "
            "subset of people, and recompute the whole t map. <bookmark mark='c'/> Record the largest t, or the "
            "largest cluster, anywhere in the brain. <bookmark mark='d'/> Do it thousands of times, and the "
            "ninety-fifth percentile of those maxima is the threshold. No assumption about how the noise is "
            "correlated in space is needed. The brain's own noise sets the bar."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", steps):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(foot))
        self.clear_scene()

    def clusters(self):
        d = load("clusterfwe")
        head = heading(r"Cluster failure, \ simulated")
        A = axes([0.3, 4.7], [0, 0.16], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 0.05, 0.1, 0.15],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"null studies with a cluster", center=[-3.4, 0.3, 0],
                 font_size=12)
        vals = [d["lenient_parametric"], d["lenient_permutation"], d["strict_parametric"], d["strict_permutation"]]
        b = bars(A.ax, [1, 2, 3, 4], vals, [AUTH, GOOD, AUTH, GOOD], width=0.6)
        five = DashedLine(A.ax.c2p(0.3, 0.05), A.ax.c2p(4.7, 0.05), color=GREY_B, stroke_width=1.5)
        names = VGroup(*[wrapped_label(t, 1.1, 11, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, (t, c) in
                         enumerate(((r"$p<0.01$, \ Gaussian", AUTH), (r"$p<0.01$, \ permutation", GOOD),
                                    (r"$p<0.001$, \ Gaussian", AUTH), (r"$p<0.001$, \ permutation", GOOD)))])
        rows = rows_of([
            (rf"{d['sets']} group studies of pure noise whose spatial correlation has a long tail, \ as real noise does",
             WHITE),
            (rf"cluster sizes calibrated on Gaussian noise, \ formed at $p < 0.01$: \ a cluster in "
             rf"{100 * d['lenient_parametric']:.1f}\% of studies, \ against the promised 5\%", AUTH),
            (rf"at $p < 0.001$, \ {100 * d['strict_parametric']:.1f}\%; \ permutation holds both near 5\%", GOOD),
            (r"Eklund, \ Nichols and Knutsson found far larger excesses in real resting-state data in 2016", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{neurodata.cluster\_fwe}, \ 200 permutations each")
        tag2 = published_tag(r"Eklund et al.\ (2016)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Now the failure that shook the field. <bookmark mark='a'/> Psyche makes two hundred group studies of pure "
            "noise, whose spatial correlation has a long tail, as real noise does. <bookmark mark='b'/> Calibrate "
            "cluster sizes on Gaussian noise and form clusters at one in a hundred, and a cluster appears in about "
            "one study in eight, against the promised one in twenty. <bookmark mark='c'/> At one in a thousand it's "
            "close to the promise, and permutation holds both near five percent. <bookmark mark='d'/> In 2016 Anders "
            "Eklund, Thomas Nichols and Hans Knutsson ran null analyses on real resting-state data in common software, "
            "and found far larger excesses at the lenient threshold. That's in the Ledger."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(names), FadeIn(five))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]), FadeIn(b[2]), FadeIn(b[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def byrule(self):
        d = load("multiverse")
        head = heading(r"The threshold is a fork too")
        M = np.asarray(d["by_threshold"])
        names = [r"$p<0.001$", r"$p<0.005$, \ 10 voxels", r"FDR 5\%", r"cluster $p<0.01$", r"cluster $p<0.001$",
                 r"permutation"]
        hm = VGroup()
        cell = 0.62
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                v = float(M[i, j])
                sq = Square(cell, stroke_width=1, stroke_color=BLACK, fill_opacity=1,
                            fill_color=interpolate_color(ManimColor("#14181F"), ManimColor(THRESH), v))
                sq.move_to([j * cell, -i * cell, 0])
                hm.add(VGroup(sq, label(f"{100 * v:.0f}", font_size=14, color=BLACK if v > 0.55 else WHITE).move_to(sq)))
        hm.move_to([-2.2, 0.2, 0])
        rl = VGroup(*[label(n, font_size=14, color=GREY_A).next_to(hm[i * M.shape[1]], LEFT, buff=0.12)
                      for i, n in enumerate(names)])
        cl = VGroup(*[label(rf"H{j + 1}", font_size=14, color=GREY_A).next_to(hm[j], UP, buff=0.1)
                      for j in range(M.shape[1])])
        rows = rows_of([
            (r"percent of pipelines saying yes, \ by threshold rule, \ for the five questions", WHITE),
            (r"for the empty region and the smallest effect, \ every rule agrees: \ no", GOOD),
            (r"for the middle effects, \ the rule alone moves the answer: \ from none to a third of pipelines for one, \ from two fifths to two thirds for the other", AUTH),
            (r"a threshold is a decision about errors; \ choose it before the data, \ and say which", YOU),
        ], 4.6, 19, 0.38).move_to([4.3, -0.1, 0])
        with self.voiceover(
            "And the threshold is a fork. <bookmark mark='a'/> Here's the share of pipelines saying yes, by "
            "threshold rule, for the five questions. <bookmark mark='b'/> For the empty region and the smallest "
            "effect, every rule agrees: no. <bookmark mark='c'/> For the middle effects, the rule alone moves the "
            "answer: from none to a third of the pipelines for one, and from two fifths to two thirds for the other. <bookmark mark='d'/> A threshold is a decision about which "
            "errors to risk. Choose it before the data, and say which."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hm), FadeIn(rl), FadeIn(cl))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
