from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs41.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, commit_dot, grid_table, load, mono)


class Merge(VoiceoverScene):
    def construct(self):
        self.card()
        self.bases()
        self.painting()
        self.editgraph()
        self.threeway()
        self.resolution()
        self.rewrite()
        self.bisect()

    def card(self):
        card = chapter_card(2, r"Merging and bisecting", r"How do two lines of work become one?",
                            lit=(1986, 2021), extra=((1986, r"Myers: \ the O(ND) diff"),
                                                     (2021, r"git's ort merge")), part=PART)
        with self.voiceover("Chapter two. Merging and bisecting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def bases(self):
        b = load("bases")
        cc = b["criss_cross"]
        head = label(r"Where did the branches part?", font_size=36).to_edge(UP, buff=0.3)
        pos = {0: [-5.0, 0.3], 1: [-3.2, 1.3], 2: [-3.2, -0.7], 3: [-1.0, 1.3], 4: [-1.0, -0.7], 5: [1.0, 1.3],
               6: [1.0, -0.7]}
        dots = {i: commit_dot(YES if i in cc["bases"] else (HEAD if i in (5, 6) else DATA)).move_to([*p, 0])
                for i, p in pos.items()}
        names = VGroup(*[label(f"{i}", font_size=16, color=WHITE).next_to(d, UP if pos[i][1] > 0 else DOWN,
                                                                       buff=0.08) for i, d in dots.items()])
        edges = VGroup(*[Arrow(dots[c].get_center(), dots[p].get_center(), buff=0.18, stroke_width=2,
                               color=GREY_B, max_tip_length_to_length_ratio=0.12)
                         for c, ps in enumerate(cc["parents"]) for p in ps])
        notes = VGroup(
            wrapped_label(r"a \textbf{merge base} of two commits is a best common ancestor: \ an ancestor of both "
                          r"that is not an ancestor of another common ancestor", 5.4, font_size=19, color=WHITE),
            wrapped_label(rf"for commits 5 and 6 there are two: \ {cc['bases'][0]} and {cc['bases'][1]}, \ because "
                          r"each branch merged the other \ (a criss-cross)", 5.4, font_size=19, color=YES),
            wrapped_label(r"git's recursive strategy merges the merge bases first, \ into a virtual ancestor, \ then "
                          r"merges against that; \ its successor \textbf{ort} \ (2021) \ does the same, \ faster", 5.4,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, 0.2, 0])
        with self.voiceover(
            "History is a directed acyclic graph: every commit points to its parents. To merge two branches, git "
            "first finds where they diverged. <bookmark mark='a'/> A merge base is a best common ancestor: a commit "
            "that both branches contain and that is not an ancestor of another such commit, the lowest common "
            "ancestor of Part 18 generalized to graphs. <bookmark mark='b'/> Usually there is one. But in this "
            "history each branch merged the other, a criss-cross, and commits five and six have two merge bases, "
            "one and two, neither better than the other. <bookmark mark='c'/> Git's recursive strategy merges the "
            "two bases first into a virtual ancestor, and merges against that. Its replacement since 2021, called "
            "ort, does the same, many times faster."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(d) for d in dots.values()], FadeIn(names), Create(edges))
            for mk, n in zip("abc", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.wait(0.4)
        self.clear_scene()

    def threeway(self):
        m = load("merge")
        head = label(r"Three-way merge", font_size=36).to_edge(UP, buff=0.3)

        def col(title, lines, color, hi=()):
            body = code_block(lines, size=15)
            for i in hi:
                body[i].set_color(color)
            t = label(title, font_size=19, color=color)
            return VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        base = col(r"base", m["base"], GREY_A)
        ours = col(r"ours", m["ours"], DATA, hi=(1,))
        theirs = col(r"theirs", m["theirs"], LAM, hi=(3,))
        cols = VGroup(base, ours, theirs).arrange(RIGHT, buff=0.5, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        merged = col(r"merged: \ each side's change kept", m["clean"], YES, hi=(1, 3))
        clash = col(r"if theirs had changed line 2 too: \ a conflict", m["conflicted"], NO, hi=(1, 2, 3, 4, 5))
        VGroup(merged, clash).arrange(RIGHT, buff=0.8, aligned_edge=UP).next_to(cols, DOWN, buff=0.55)
        note = wrapped_label(r"diff base with each side \ (Myers, Part 21); \ a region changed on one side takes that "
                             r"side; \ changed identically on both, \ either; \ changed differently, \ a conflict for "
                             r"a person", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "With a merge base in hand, the merge itself compares three versions. <bookmark mark='a'/> Here a base, "
            "and two branches: ours lower-cased the words; theirs changed twenty to ten. <bookmark mark='b'/> Diff "
            "the base against each side, with Myers' algorithm from Part 21. A region changed on only one side takes "
            "that side's version; a region changed identically on both takes it once. Our merge keeps both changes, "
            "and no person is needed. <bookmark mark='c'/> But if theirs had also rewritten line two, differently, "
            "no rule can choose, and git writes both versions between conflict markers for a person to resolve. "
            "Without the base, a two-way comparison could not tell which side changed anything at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols))
            vo.wait_until("b")
            self.play(FadeIn(merged), FadeIn(note))
            vo.wait_until("c")
            self.play(FadeIn(clash))
        self.wait(0.4)
        self.clear_scene()

    def rewrite(self):
        head = label(r"Rebase, \ cherry-pick", font_size=36).to_edge(UP, buff=0.3)
        y1, y2 = 1.2, -0.2
        main = VGroup(*[commit_dot(DATA).move_to([-5.5 + i * 1.2, y1, 0]) for i in range(4)])
        feat = VGroup(*[commit_dot(LAM).move_to([-3.7 + i * 1.2, y2, 0]) for i in range(2)])
        l1 = VGroup(*[Line(main[i].get_center(), main[i + 1].get_center(), color=GREY_C) for i in range(3)])
        l2 = VGroup(Line(main[1].get_center(), feat[0].get_center(), color=GREY_C),
                    Line(feat[0].get_center(), feat[1].get_center(), color=GREY_C))
        merge_dot = commit_dot(HEAD).move_to([-0.6, y1, 0])
        lm = VGroup(Line(main[3].get_center(), merge_dot.get_center(), color=GREY_C),
                    Line(feat[1].get_center(), merge_dot.get_center(), color=GREY_C))
        ml = label(r"merge: \ a commit with two parents; \ history as it happened", font_size=18,
                   color=HEAD).next_to(merge_dot, RIGHT, buff=0.2)
        rb = VGroup(*[commit_dot(YES).move_to([-0.6 + i * 1.2, -1.9, 0]) for i in range(2)])
        rbl = VGroup(Line(main[3].get_center(), rb[0].get_center(), color=GREY_C),
                     Line(rb[0].get_center(), rb[1].get_center(), color=GREY_C))
        rl = wrapped_label(r"rebase: \ the same diffs replayed on the new tip; \ new commits, \ new names, \ a "
                           r"straight line", 5.6, font_size=18, color=YES).next_to(rb, RIGHT, buff=0.25)
        lines = VGroup(
            wrapped_label(r"\textbf{cherry-pick} applies one commit's diff somewhere else, \ as a new commit", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"rewriting changes names, \ so never rebase commits others already have: \ their "
                          r"histories would contain the old names", 12.4, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "There are two ways to bring a branch up to date. <bookmark mark='a'/> A merge commit has two parents and "
            "records history as it happened, branches and all. <bookmark mark='b'/> A rebase instead replays each "
            "of the branch's diffs on top of the new main line, making new commits with new names, and gives a "
            "straight history. <bookmark mark='c'/> Cherry-pick applies a single commit's diff elsewhere. Because "
            "rewriting changes names, the one rule is never to rebase commits that other people already have: their "
            "copies of history would refer to commits that, in yours, no longer exist."
        ) as vo:
            self.play(FadeIn(head), FadeIn(main), Create(l1), FadeIn(feat), Create(l2))
            vo.wait_until("a")
            self.play(FadeIn(merge_dot), Create(lm), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(rb), Create(rbl), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def bisect(self):
        b = load("bisect")
        ex = b["example"]
        head = label(r"Bisect: \ binary search over history", font_size=36).to_edge(UP, buff=0.3)
        x0, w = -6.0, 12.0
        bar = Rectangle(width=w, height=0.3, stroke_color=GREY_C, stroke_width=1).move_to([0, 2.0, 0])
        good = label(r"good", font_size=16, color=YES).next_to(bar, LEFT, buff=0.1)
        bad = label(r"bad", font_size=16, color=NO).next_to(bar, RIGHT, buff=0.1)
        marks = VGroup()
        shown = []
        for k, t in enumerate(ex["tested"]):
            x = x0 + t / 1000 * w
            tick = Line([x, 1.82, 0], [x, 2.18, 0], color=NO if t >= ex["first_bad"] else YES, stroke_width=3)
            if all(abs(x - s0) > 0.3 for s0 in shown):      # later tests crowd together: label the first few only
                shown.append(x)
                marks.add(VGroup(tick, label(f"{k + 1}", font_size=14, color=GREY_A).move_to([x, 2.38, 0])))
            else:
                marks.add(tick)
        found = label(rf"commit {ex['first_bad']} of 1{{,}}000 introduced the bug: \ found in {ex['steps']} tests",
                      font_size=21, color=HEAD).next_to(bar, DOWN, buff=0.5)
        rows = [[f"{r['commits']:,}", f"{r['steps']}"] for r in b["rows"]]
        tab = grid_table([r"commits in the range", r"tests needed"], rows, widths=[3.2, 2.4], row_h=0.4,
                         font_size=19, mono_cols=())
        tab.next_to(found, DOWN, buff=0.4).set_x(-2.6)
        note = wrapped_label(r"$\lceil \log_2 n \rceil$: \ Part 16's binary search; \ \texttt{git bisect run} "
                             r"automates it with any script that can say good or bad; \ merges make it subtler, \ "
                             r"since history is a graph, \ not a line", 5.0, font_size=19, color=WHITE).next_to(
            tab, RIGHT, buff=0.6)
        with self.voiceover(
            "History also answers the question every developer eventually asks: when did this break? "
            "<bookmark mark='a'/> Mark one old commit good and the current one bad. Git checks out the commit "
            "halfway between; you test it and say good or bad; the range halves. <bookmark mark='b'/> In a "
            "thousand commits, the one that introduced the bug is found in ten tests. <bookmark mark='c'/> It is "
            "Part 16's binary search: a million commits need twenty. Given a script that decides good or bad, git "
            "bisect runs the whole search by itself. With merges, history is a graph rather than a line, and git "
            "picks the commit that splits the remaining candidates most evenly."
        ) as vo:
            self.play(FadeIn(head), Create(bar), FadeIn(good), FadeIn(bad))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(mk) for mk in marks], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(found))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def editgraph(self):
        e = load("editgraph")
        a, b = e["a"], e["b"]
        head = label(r"Diff as a shortest path", font_size=36).to_edge(UP, buff=0.3)
        cell = 0.62
        x0, y0 = -6.2, 2.0
        grid = VGroup()
        for i in range(len(a) + 1):
            grid.add(Line([x0 + i * cell, y0, 0], [x0 + i * cell, y0 - len(b) * cell, 0], color=GREY_D,
                          stroke_width=1))
        for j in range(len(b) + 1):
            grid.add(Line([x0, y0 - j * cell, 0], [x0 + len(a) * cell, y0 - j * cell, 0], color=GREY_D,
                          stroke_width=1))
        diag = VGroup()
        for i, ca in enumerate(a):
            for j, cb in enumerate(b):
                if ca == cb:
                    diag.add(Line([x0 + i * cell, y0 - j * cell, 0], [x0 + (i + 1) * cell, y0 - (j + 1) * cell, 0],
                                  color=GREY_B, stroke_width=1.5))
        la = VGroup(*[mono(ch, size=18, color=DATA).move_to([x0 + (i + 0.5) * cell, y0 + 0.25, 0])
                      for i, ch in enumerate(a)])
        lb = VGroup(*[mono(ch, size=18, color=LAM).move_to([x0 - 0.25, y0 - (j + 0.5) * cell, 0])
                      for j, ch in enumerate(b)])
        path = VMobject(color=YES, stroke_width=5).set_points_as_corners(
            [[x0 + x * cell, y0 - y * cell, 0] for x, y in e["path"]])
        notes = VGroup(
            wrapped_label(r"walk from the top left to the bottom right: \ right deletes a letter of the old text, \ "
                          r"down inserts one of the new, \ a diagonal keeps a letter they share", 5.6, font_size=20,
                          color=WHITE),
            wrapped_label(rf"the fewest non-diagonal steps is the edit distance: \ $D = {e['D']}$ here, \ keeping "
                          rf"{e['lcs']} letters", 5.6, font_size=20, color=YES),
            wrapped_label(r"Myers \ (1986) \ finds it in $O(ND)$ by extending the furthest-reaching path with "
                          r"$d$ edits, \ for $d = 0, 1, 2, \dots$ \ --- \ fast when files differ a little, \ which is "
                          r"always", 5.6, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "Every merge rests on a diff, and Part 21 showed what a diff is: a shortest path. "
            "<bookmark mark='a'/> Lay the old text along the top and the new down the side. Moving right deletes a "
            "letter of the old; moving down inserts a letter of the new; and where the letters match, a diagonal "
            "keeps it, for free. <bookmark mark='b'/> The shortest edit script is the path with fewest horizontal and "
            "vertical steps. For Eugene Myers' own example it needs five edits and keeps four letters. "
            "<bookmark mark='c'/> His algorithm of 1986 explores paths in order of how many edits they use, keeping "
            "only the furthest point each can reach, so its time grows with the size of the difference rather than "
            "the size of the files. Since versions of a file usually differ a little, that is exactly the case that "
            "matters."
        ) as vo:
            self.play(FadeIn(head), Create(grid), FadeIn(la), FadeIn(lb))
            vo.wait_until("a")
            self.play(Create(diag), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(path), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def painting(self):
        head = label(r"Finding the merge base", font_size=36).to_edge(UP, buff=0.3)
        # a small history: main c0..c5 (tip A), a branch d1..d3 from c2 (tip B); dates order the walk
        pos = {"c0": (-6.0, 1.0), "c1": (-4.8, 1.0), "c2": (-3.6, 1.0), "c3": (-2.4, 1.0), "c4": (-1.2, 1.0),
               "c5": (1.2, 1.0), "d1": (-1.8, -0.2), "d2": (-0.6, -0.2), "d3": (0.6, -0.2)}
        parents = {"c1": ["c0"], "c2": ["c1"], "c3": ["c2"], "c4": ["c3"], "c5": ["c4"], "d1": ["c2"],
                   "d2": ["d1"], "d3": ["d2"]}
        date = {"c0": 0, "c1": 1, "c2": 2, "c3": 3, "c4": 4, "c5": 6, "d1": 3.5, "d2": 4.5, "d3": 5.5}
        dots = {k: Dot([x, y, 0], radius=0.17, color=GREY_D) for k, (x, y) in pos.items()}
        edges = VGroup(*[Line(dots[c].get_center(), dots[q].get_center(), color=GREY_C, stroke_width=2)
                         for c, ps in parents.items() for q in ps])
        tips = VGroup(label(r"A", font_size=22, color=DATA).next_to(dots["c5"], UP, buff=0.12),
                      label(r"B", font_size=22, color=LAM).next_to(dots["d3"], DOWN, buff=0.12))
        # the walk, computed: a queue ordered newest first; paint flags A, B, stale
        paint = {"c5": {"A"}, "d3": {"B"}}
        queue = ["c5", "d3"]
        steps, result = [], None
        while queue and any("stale" not in paint[q] for q in queue):
            queue.sort(key=lambda k: -date[k])
            cur = queue.pop(0)
            flags = paint[cur]
            if {"A", "B"} <= flags and "stale" not in flags:
                result = cur
                flags = flags | {"stale"}
            for q in parents.get(cur, []):
                new = paint.setdefault(q, set()) | flags
                paint[q] = new
                if q not in queue:
                    queue.append(q)
            steps.append((cur, {k: set(v) for k, v in paint.items()}))

        def col(fl):
            if "stale" in fl:
                return GREY_B
            if {"A", "B"} <= fl:
                return YES
            return DATA if "A" in fl else (LAM if "B" in fl else GREY_D)
        lines = VGroup(
            wrapped_label(r"walk back from both commits at once, \ newest first, \ painting each commit with the "
                          r"side or sides that reach it", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"a commit painted by \textit{both} is a common ancestor; \ paint its ancestors "
                          r"``stale'' so that they are not reported too; \ stop when only stale commits remain", 12.4,
                          font_size=20, color=YES),
            wrapped_label(r"the cost is the commits since the branches parted, \ not the whole history; \ "
                          r"\textbf{commit-graph} files with generation numbers \ (2018) \ let git stop even "
                          r"earlier", 12.4, font_size=20, color=HEAD),
            wrapped_label(r"the same search answers \texttt{git log A..B} \ (what B has that A lacks) \ and decides "
                          r"whether a push is a fast-forward", 12.4, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        legend = VGroup(*[VGroup(Dot(radius=0.09, color=c), label(t, font_size=16, color=c)).arrange(RIGHT, buff=0.1)
                          for t, c in ((r"reached from A", DATA), (r"from B", LAM), (r"from both", YES),
                                       (r"stale", GREY_B))]).arrange(RIGHT, buff=0.45).move_to([0, 2.15, 0])
        ring = Circle(radius=0.3, color=YES, stroke_width=4, fill_opacity=0)
        with self.voiceover(
            "How does git find merge bases quickly in a history of millions of commits? <bookmark mark='a'/> It walks "
            "backwards from both commits at once, newest first, painting each commit it reaches with the side or "
            "sides that reached it. <bookmark mark='b'/> A commit painted by both sides is a common ancestor. Its own "
            "ancestors are painted stale, so they will not be reported as well, and the walk stops when only stale "
            "commits are left. <bookmark mark='c'/> The cost depends on how far the branches have drifted, not on the "
            "length of history, and since 2018 a commit-graph file storing generation numbers lets git stop "
            "earlier still. <bookmark mark='d'/> The same walk answers which commits one branch has that another "
            "lacks, and whether a push only moves a branch forward."
        ) as vo:
            self.play(FadeIn(head), Create(edges), *[FadeIn(d) for d in dots.values()], FadeIn(tips), FadeIn(legend))
            self.play(dots["c5"].animate.set_color(DATA), dots["d3"].animate.set_color(LAM))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            for cur, pt in steps:
                self.play(Indicate(dots[cur], scale_factor=1.3, color=WHITE), run_time=0.45)
                self.play(*[dots[k].animate.set_color(col(f)) for k, f in pt.items()], run_time=0.45)
            vo.wait_until("b")
            ring.move_to(dots[result])
            self.play(FadeIn(lines[1]), Create(ring))
            for mk, l in zip("cd", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def resolution(self):
        head = label(r"Resolving conflicts", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"a conflict is a question only a person, \ or a test, \ can answer: \ which combination "
                          r"of the two intentions is right?", 12.4, font_size=23, color=WHITE),
            wrapped_label(r"\textbf{rerere} \ (``reuse recorded resolution''): \ git remembers how you resolved a "
                          r"conflict, \ keyed by a hash of its two sides, \ and replays the answer when the same "
                          r"conflict reappears", 12.4, font_size=23, color=YES),
            wrapped_label(r"after resolving, \ build and test the merge: \ a merge without textual conflicts can "
                          r"still be wrong, \ which is Chapter 8's frontier", 12.4, font_size=23, color=NO),
            wrapped_label(r"the cheapest conflict is the one that never happens: \ small changes, \ merged often "
                          r"\ (Chapter 6)", 12.4, font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "When a merge does conflict, someone has to decide. <bookmark mark='a'/> A conflict is a question only a "
            "person, or a test, can answer: which combination of two intentions is correct? "
            "<bookmark mark='b'/> Git can at least avoid asking twice. Its rerere feature, reuse recorded resolution, "
            "remembers how you resolved a conflict, keyed by a hash of its two sides, and replays the answer when "
            "the same conflict comes back, as it does when a branch is rebased repeatedly. "
            "<bookmark mark='c'/> After resolving, build and test the result: a merge with no textual conflict can "
            "still be wrong, as the frontier chapter will show. <bookmark mark='d'/> And the cheapest conflict is the "
            "one that never happens, because changes were small and merged often."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, math)
