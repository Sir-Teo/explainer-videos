from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403

MAJORS = ["C", "G", "D", "A", "E", "B", "F♯", "D♭", "A♭", "E♭", "B♭", "F"]
MINORS = ["A", "E", "B", "F♯", "C♯", "G♯", "E♭", "B♭", "F", "C", "G", "D"]
DATA_NAME = {"C♯": "D♭", "G♯": "A♭"}            # the pathfinder names minor keys with flats
DIST_C = {0: TUNE, 1: "#7DD3FC", 2: "#F472B6"}


def key_circle(dist: dict, centre, R: float = 2.4, r: float = 1.55):
    g = VGroup()
    g.cells = {}
    for k in range(12):
        ang = 2 * np.pi * k / 12
        u = np.array([np.sin(ang), np.cos(ang), 0])
        for name, mode, rad, fs in ((MAJORS[k], "major", R, 24), (MINORS[k], "minor", r, 19)):
            dn = f"{DATA_NAME.get(name, name)} {mode}"
            dv = dist[dn]
            c_ = Circle(radius=0.32 if mode == "major" else 0.26, stroke_width=2, color=DIST_C[dv], fill_color=DIST_C[dv], fill_opacity=0.25).move_to(centre + rad * u)
            t = label(tex(name if mode == "major" else name.lower()), font_size=fs, color=WHITE).move_to(c_)
            cell = VGroup(c_, t)
            g.add(cell)
            g.cells[(name, mode)] = cell
    return g


def recolour(g, dist: dict):
    anims = []
    for (name, mode), cell in g.cells.items():
        dv = dist[f"{DATA_NAME.get(name, name)} {mode}"]
        anims.append(cell[0].animate.set_stroke(DIST_C[dv]).set_fill(DIST_C[dv], opacity=0.25))
    return anims


class Paths(SoundScene):
    def construct(self):
        chapter(self, 9, r"The shortest way to any key", r"How many chords does it take to get from C to anywhere?")
        self.graph()
        self.search()
        self.counts()

    # ------------------------------------------------------------------
    def graph(self):
        d = load("paths")
        centre = LEFT * 3.0 + DOWN * 0.2
        g = key_circle(d["pivots"], centre)
        legend = VGroup(*[VGroup(Dot(radius=0.1, color=DIST_C[v]), label(t, font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15)
                          for v, t in ((0, r"home"), (1, r"one step"), (2, r"two steps"))]).arrange(RIGHT, buff=0.4).next_to(g, DOWN, buff=0.35)
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"24 keys; \ a step joins two keys \ if one chord can belong to both", WHITE),
            (r"breadth-first search from C: \ the fewest steps to every key", WHITE),
            (r"Part 15's pivot chords only: \ half the keys need two steps", WHITE),
            (r"add the doors: \ the German sixth, \ the diminished seventh, \ the Neapolitan", EAR),
            (r"now almost every key is one chord away", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.6))
        rows_.move_to(RIGHT * 3.4 + DOWN * 0.1)
        with self.voiceover(
            "How far is any key from C, counted in chords? Turn the question into a program. "
            "<bookmark mark='a'/> Put the twenty-four keys on Part 15's circle, majors outside, minors inside, and "
            "join two keys by a step if a single chord can belong to both. <bookmark mark='b'/> Then search outward "
            "from C, breadth first, and record the fewest steps to every key. <bookmark mark='c'/> With only Part 15's "
            "pivot chords, triads shared by both keys, the neighbours of C are one step away, and the far side of the "
            "circle takes two. <bookmark mark='d'/> Now add this part's doors: the German sixth heard as a dominant "
            "seventh, the diminished seventh respelled, the Neapolitan heard as a chord of a new key. "
            "<bookmark mark='e'/> Almost every key is now a single chord away."
        ) as vo:
            self.play(FadeIn(g), FadeIn(legend))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(rows_[3]))
            self.play(*recolour(g, d["chromatic"]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(rows_[4]))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def search(self):
        from explainer.music.monochord import chromatic as X
        d = load("paths")
        n_edges = sum(len(X.edges(k, False)) for k in X.KEYS)
        layers = {s_: [k for k, v in d["pivots"].items() if v == s_] for s_ in (0, 1, 2)}
        cols = VGroup()
        for s_, title in ((0, r"0 steps"), (1, r"1 step"), (2, r"2 steps")):
            ks = layers[s_]
            items = VGroup(*[label(tex(k.replace(" major", "").replace(" minor", "m")), font_size=28, color=DIST_C[s_]) for k in ks])
            items.arrange_in_grid(cols=3 if len(ks) > 1 else 1, buff=(0.45, 0.28))
            cols.add(VGroup(label(title, font_size=30, color=GREY_A), items).arrange(DOWN, buff=0.4))
        cols.arrange(RIGHT, buff=1.1, aligned_edge=UP).to_edge(UP, buff=0.5)
        arrows = VGroup(Arrow(cols[0].get_right(), cols[1].get_left(), buff=0.15, color=GREY_B, stroke_width=3),
                        Arrow(cols[1].get_right(), cols[2].get_left(), buff=0.15, color=GREY_B, stroke_width=3))
        rows_ = VGroup(*[label(t_, font_size=26, color=c_) for t_, c_ in (
            (r"a queue: \ first in, \ first out", WHITE),
            (r"take a key out; \ add its unseen neighbours, \ each with a distance and a parent", WHITE),
            (r"keys leave in the order found: \ nearest first, \ so the first route found is a shortest one", WHITE),
            (rf"{n_edges} connections looked at, \ each once from either end", TUNE))]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "How does the search work? <bookmark mark='a'/> Keep a queue of keys, first in, first out, and start it "
            "with C major. <bookmark mark='b'/> Take the first key out; list every key one chord away that has not been "
            "seen yet; give each a distance one more than the key it came from, remember that parent, and put it at "
            f"the back of the queue. <bookmark mark='c'/> From C, that finds {say(len(layers[1]))} keys at one step. Then "
            f"each of those is taken out in turn, and finds the remaining {say(len(layers[2]))} at two. Because keys leave "
            "the queue in the order they were found, nearest first, the first route to reach a key is a shortest one; "
            "following the parents back gives the route. <bookmark mark='d'/> Each connection between keys is looked at "
            f"once in each direction: {say(n_edges)} of them with pivot chords. This is breadth-first search, and it "
            "finds shortest routes in any network whose steps all cost the same."
        ) as vo:
            self.play(FadeIn(cols[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[0]), FadeIn(cols[1]), FadeIn(rows_[2]))
            self.play(GrowArrow(arrows[1]), FadeIn(cols[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("paths")
        cnt = {k: [sum(1 for v in d[k].values() if v == s) for s in (1, 2)] for k in ("pivots", "chromatic")}
        ch = columns([cnt["pivots"][0], cnt["pivots"][1], cnt["chromatic"][0], cnt["chromatic"][1]],
                     [r"1 step", r"2 steps", r"1 step", r"2 steps"], width=6.4, height=2.6, color=WEAK, hot=(2,), hot_color=TUNE, fmt="{:.0f}", font_size=22).move_to(LEFT * 3.0 + DOWN * 0.5)
        tags = VGroup(label(r"pivot chords", font_size=22, color=GREY_A), label(r"with the doors", font_size=22, color=TUNE)).arrange(RIGHT, buff=1.6).next_to(ch, UP, buff=0.35)
        r1 = d["routes_pivots"]["F♯ major"]
        r2 = d["routes"]["F♯ major"]
        route = VGroup(label(r"C major to F$\sharp$ major:", font_size=26, color=WHITE),
                       label(tex(" → ".join([r1[0][0]] + [b for a, b, how in r1])) + r" \ (pivots)", font_size=22, color=GREY_A),
                       label(tex(" → ".join([r2[0][0]] + [b for a, b, how in r2])), font_size=22, color=TUNE),
                       label(r"by " + r2[0][2], font_size=22, color=TUNE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.6 + DOWN * 0.2)
        with self.voiceover(
            f"Count them. With pivot chords alone, {say(cnt['pivots'][0])} keys are one step from C and "
            f"{say(cnt['pivots'][1])} need two. <bookmark mark='a'/> With the doors, {say(cnt['chromatic'][0])} are "
            f"one step away, and only {say(cnt['chromatic'][1])} need two. <bookmark mark='b'/> Take F sharp major, "
            "the key furthest from C on the circle, with six sharps. With pivots, the shortest route goes through E "
            "minor. With the doors, the diminished seventh of C, respelled, lands there directly. This is what "
            "chromatic harmony bought: the whole map of keys within reach of a single chord."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(tags))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(route))
        self.wait(0.4)
        self.clear_scene()
