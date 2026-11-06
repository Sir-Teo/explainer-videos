from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.learned()
        self.predict()
        self.metastable()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ design as a science", r"Can a design be predicted, \ not just argued?",
                            lit=(2018, 2021), extra=((2018, r"learned index structures"),
                                                     (2021, r"metastable failures")), part=PART)
        with self.voiceover("Chapter fifteen, the frontier. Can a design be predicted, and not just argued for?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def learned(self):
        L = load("learned")
        head = label(r"An index that learns the data", font_size=36).to_edge(UP, buff=0.3)
        # schematic: a staircase of keys and a few line segments fitted to it
        x0, y0 = -6.0, -1.9
        import random
        rng = random.Random(2)
        pts, t = [], 0.0
        for k in range(60):
            t += rng.expovariate(1.0) * (4 if 20 <= k < 30 else 1)
            pts.append((t, k))
        tmax = pts[-1][0]
        dots = VGroup(*[Dot([x0 + p[0] / tmax * 5.6, y0 + p[1] / 60 * 3.6, 0], radius=0.04, color=DATA) for p in pts])
        segs = VGroup(Line([x0, y0, 0], [x0 + pts[20][0] / tmax * 5.6, y0 + 20 / 60 * 3.6, 0], color=HEAD,
                           stroke_width=3),
                      Line([x0 + pts[20][0] / tmax * 5.6, y0 + 20 / 60 * 3.6, 0],
                           [x0 + pts[30][0] / tmax * 5.6, y0 + 30 / 60 * 3.6, 0], color=HEAD, stroke_width=3),
                      Line([x0 + pts[30][0] / tmax * 5.6, y0 + 30 / 60 * 3.6, 0],
                           [x0 + pts[59][0] / tmax * 5.6, y0 + 59 / 60 * 3.6, 0], color=HEAD, stroke_width=3))
        axl = VGroup(label(r"key", font_size=16, color=GREY_B).move_to([x0 + 2.8, y0 - 0.3, 0]),
                     label(r"position", font_size=16, color=GREY_B).rotate(PI / 2).move_to([x0 - 0.3, y0 + 1.8, 0]))
        sch = note(r"schematic", font_size=15).next_to(dots, UP, buff=0.1)
        rows = [[f"{r['eps']}", f"{r['segments']:,}", f"{r['bytes'] / 1000:.1f} kB", f"{r['search_steps']}"]
                for r in L["rows"]]
        rows.append([r"B+ tree", f"{L['btree_inner_nodes']}", f"{L['btree_inner_bytes'] / 1000:.0f} kB",
                     f"{L['btree_steps']}"])
        tab = grid_table([r"max error", r"segments", r"model size", r"comparisons"], rows,
                         widths=[1.8, 1.8, 1.9, 1.9], row_h=0.45, font_size=18, mono_cols=())
        tab.to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        for cell in tab.cells[-1]:
            cell.set_color(GREY_A)
        foot = wrapped_label(rf"{L['keys']:,} bursty timestamps; \ Kraska et al., \ ``The case for learned index "
                             r"structures'' \ (2018); \ the PGM-index \ (Ferragina and Vinciguerra, \ 2020) \ with "
                             r"guarantees", 12.4, font_size=18, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "An index maps a key to a position. A B-tree does it with a hierarchy of sorted pages, knowing nothing "
            "about the keys. <bookmark mark='a'/> But the map from key to position is a function, and a function "
            "can be learned. Fit a few straight lines to it, each guaranteed to predict a position within a fixed "
            "error, and finish with a short binary search. <bookmark mark='b'/> On a million bursty timestamps, "
            f"an error bound of 32 needs {L['rows'][1]['segments']} segments, about "
            f"{L['rows'][1]['bytes'] / 1000:.0f} kilobytes, and seven comparisons; the B-tree's inner nodes take "
            f"about {L['btree_inner_bytes'] / 1000:.0f} kilobytes and some {L['btree_steps']} comparisons. "
            "<bookmark mark='c'/> Tim Kraska and colleagues made the case for learned indexes in 2018; the "
            "PGM-index of Paolo Ferragina and Giorgio Vinciguerra added worst-case guarantees. Learned structures "
            "for updates, multiple dimensions and shifting data remain open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots), FadeIn(axl), FadeIn(sch))
            vo.wait_until("a")
            self.play(Create(segs), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        head = label(r"Predicting a system before building it", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"queueing networks", r"Jackson networks and mean-value analysis predict throughput and waits of a "
                 r"whole design from service times \ (Part 31): \ exact for idealized systems", HEAD),
            tile(r"simulation", r"discrete-event models like this part's load test: \ any detail, \ but only the "
                 r"scenarios you think to simulate", DATA),
            tile(r"learned performance models", r"models trained on traces predict tail latency and tune "
                 r"configurations; \ accurate inside the data, \ unreliable outside it", LAM),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"open: \ predicting tail latency, \ not just means, \ for a design that does not exist "
                             r"yet, \ with bounds on the error", 12.4, font_size=20, color=NO).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Design reviews are still mostly arguments. Three tools try to turn them into predictions. "
            "<bookmark mark='a'/> Queueing networks, Part 31's mathematics extended to many connected queues, "
            "predict throughput and waiting times from service times alone, exactly for idealized systems. "
            "<bookmark mark='b'/> Simulation, like this part's load test, can include any detail, but only covers "
            "the scenarios someone thought to simulate. <bookmark mark='c'/> And learned models trained on traces "
            "predict latency and tune configurations, accurately inside their data and unreliably outside it. "
            "<bookmark mark='d'/> Predicting the tail, not just the mean, of a system that does not exist yet, with "
            "a bound on the error, is open."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def metastable(self):
        head = label(r"Failures that sustain themselves", font_size=36).to_edge(UP, buff=0.3)
        states = [(r"stable", YES, [-4.5, 0.6]), (r"vulnerable", HEAD, [0.0, 0.6]), (r"metastable failure", NO,
                                                                                     [4.5, 0.6])]
        boxes = VGroup()
        for t, c, p in states:
            r = RoundedRectangle(width=3.2, height=1.0, corner_radius=0.15, stroke_color=c, stroke_width=2.5,
                                 fill_color=BG, fill_opacity=1).move_to([*p, 0])
            boxes.add(VGroup(r, label(t, font_size=21, color=c).move_to(r)))
        a1 = Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.1, color=GREY_B, stroke_width=2)
        a2 = Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.1, color=NO, stroke_width=2)
        loop = CurvedArrow(boxes[2].get_bottom() + LEFT * 0.6, boxes[2].get_bottom() + RIGHT * 0.6, angle=2.5,
                           color=NO, stroke_width=2)
        l1 = label(r"load rises", font_size=16, color=GREY_B).next_to(a1, UP, buff=0.08)
        l2 = label(r"a trigger: \ a blip, \ a cold cache", font_size=16, color=NO).next_to(a2, UP, buff=0.08)
        l3 = label(r"retries, \ timeouts, \ cache misses feed it", font_size=16, color=NO).next_to(loop, DOWN,
                                                                                               buff=0.1)
        lines = VGroup(
            wrapped_label(r"Bronson et al. \ (2021): \ a class of outages where the trigger ends but the failure does "
                          r"not, \ because the system's own work keeps it overloaded \ (Part 43's retry storm)", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"open: \ detecting vulnerability before the trigger, \ and designs proven not to have a "
                          r"bad stable state", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Some failures sustain themselves. <bookmark mark='a'/> A system runs stably, and as load rises it "
            "becomes vulnerable without anyone noticing. <bookmark mark='b'/> Then a trigger, a brief network blip, "
            "or a cache that restarts cold, pushes it into overload. <bookmark mark='c'/> The trigger ends, but the "
            "overload does not: timeouts cause retries, retries cause more timeouts, misses keep the cache cold. "
            "Nathan Bronson and colleagues named these metastable failures in 2021; Part 43's retry storm was one. "
            "<bookmark mark='d'/> Detecting vulnerability before the trigger, and proving that a design has no bad "
            "stable state, are open problems."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), GrowArrow(a1), FadeIn(l1), FadeIn(boxes[1]))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(boxes[2]))
            vo.wait_until("c")
            self.play(Create(loop), FadeIn(l3), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Learned structures that update}: \ learned indexes with guarantees under "
                          r"inserts, \ deletes and shifting data.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Predicting tails}: \ tail latency of an unbuilt design, \ with error "
                          r"bounds.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Metastability}: \ detecting vulnerable states before a trigger arrives.",
                          12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Optimal caching online}: \ admission and eviction near Belady's optimum on "
                          r"real, \ changing traffic.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ a cache admission policy with a provable "
                             r"competitive ratio against the best static set on Zipf traffic whose popularity drifts",
                             12.4, font_size=23, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Learned indexes that keep their guarantees as data is inserted, "
            "deleted and shifts. <bookmark mark='b'/> Predicting the tail latency of a design before it is built, "
            "with bounds on the error. <bookmark mark='c'/> Detecting the vulnerable states that precede metastable "
            "failures. <bookmark mark='d'/> And caches that admit and evict close to the optimum on real traffic "
            "that keeps changing. <bookmark mark='e'/> This part's research problem asks for a cache admission "
            "policy with a provable competitive ratio against the best fixed set of items, when popularity follows "
            "Zipf's law but drifts over time."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
