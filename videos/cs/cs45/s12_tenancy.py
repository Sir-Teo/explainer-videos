from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, mono, tag_box


def cell(color, w=0.34, h=0.34, opacity=0.85):
    return Rectangle(width=w, height=h, stroke_color=GREY_D, stroke_width=1, fill_color=color, fill_opacity=opacity)


class Tenancy(WatchScene):
    def construct(self):
        self.card()
        self.neighbours()
        self.sidechannel()
        self.domains()
        self.placement()

    def card(self):
        self.chapter(11, r"Neighbours, \ regions and failure domains", r"Who shares your machine, \ and what fails with it?", lit=(2009, 2020), extra=((2009, r"Ristenpart et al.: \ co-residence in a cloud"), (2020, r"Schrems II")), part=PART, said="Chapter eleven. Neighbours, regions and failure domains.")

    def neighbours(self):
        head = label(r"Noisy neighbours", font_size=36).to_edge(UP, buff=0.3)
        cores = VGroup()
        for i, c in enumerate((DATA, DATA, LAM, LAM)):
            r = RoundedRectangle(width=1.2, height=0.55, corner_radius=0.08, stroke_color=c, stroke_width=2,
                                 fill_color=c, fill_opacity=0.15)
            cores.add(VGroup(r, mono(f"core {i}", size=15, color=WHITE).move_to(r)))
        cores.arrange(RIGHT, buff=0.3)
        l2 = VGroup()
        for b in cores:
            r = Rectangle(width=1.2, height=0.3, stroke_color=GREY_C, stroke_width=1).next_to(b, DOWN, buff=0.08)
            l2.add(VGroup(r, mono("L1, L2", size=13, color=GREY_B).move_to(r)))
        ways, sets = 16, 3
        llc = VGroup(*[cell(DATA if w < 11 else LAM) for s in range(sets) for w in range(ways)])
        llc.arrange_in_grid(rows=sets, cols=ways, buff=0.0).next_to(l2, DOWN, buff=0.45)
        llc_t = label(r"shared last-level cache: \ 16 ways", font_size=18, color=GREY_A).next_to(llc, DOWN, buff=0.18)
        bus = Rectangle(width=llc.width, height=0.32, stroke_color=GREY_C, stroke_width=1.5).next_to(
            llc_t, DOWN, buff=0.25)
        bus_t = label(r"memory bus, \ to DRAM", font_size=18, color=GREY_A).next_to(bus, DOWN, buff=0.1)
        fill_a = Rectangle(width=bus.width * 0.25, height=0.3, stroke_width=0, fill_color=DATA, fill_opacity=0.8)
        fill_a.align_to(bus, LEFT).set_y(bus.get_y())
        fill_b = Rectangle(width=bus.width * 0.1, height=0.3, stroke_width=0, fill_color=LAM, fill_opacity=0.8)
        fill_b.next_to(fill_a, RIGHT, buff=0)
        chip = VGroup(cores, l2, llc, llc_t, bus, bus_t, fill_a, fill_b).scale(1.12).move_to([-3.3, -0.55, 0])
        tl = VGroup(label(r"tenant A", font_size=19, color=DATA).next_to(VGroup(cores[0], cores[1]), UP, buff=0.12),
                    label(r"tenant B", font_size=19, color=LAM).next_to(VGroup(cores[2], cores[3]), UP, buff=0.12))
        frame = SurroundingRectangle(VGroup(chip, tl), buff=0.2, color=GREY_C, stroke_width=1.5, corner_radius=0.1)
        gauge_t = label(r"tenant A's time per request", font_size=19, color=WHITE)
        g_base = Line(ORIGIN, RIGHT * 4.6, color=GREY_C, stroke_width=1.5)
        VGroup(gauge_t, g_base).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.9, 1.7, 0])

        def bar(w, col):
            return Rectangle(width=w, height=0.35, stroke_width=0, fill_color=col, fill_opacity=0.85).next_to(
                g_base, UP, buff=0.02).align_to(g_base, LEFT)
        g = bar(1.2, YES)
        illus = label(r"illustrative", font_size=16, color=GREY_B).next_to(g_base, DOWN, buff=0.1).align_to(
            g_base, LEFT)
        notes = VGroup(
            wrapped_label(r"the hypervisor divides cores and memory, \ but by default not the cache or the memory "
                          r"bus \ (Part 9's misses, \ caused by someone else)", 4.8, font_size=19, color=NO),
            wrapped_label(r"Intel's \textbf{Cache Allocation Technology} gives each tenant its own ways; \ "
                          r"\textbf{Memory Bandwidth Allocation} throttles its share of the bus", 4.8, font_size=19,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(illus, DOWN, buff=0.45).align_to(g_base, LEFT)
        fence = DashedLine(llc.get_corner(UL) + RIGHT * llc.width / 2 + UP * 0.15,
                           llc.get_corner(DL) + RIGHT * llc.width / 2 + DOWN * 0.04, color=HEAD, stroke_width=3)
        with self.voiceover(
            "A virtual machine gets its own cores and memory, but not everything on the chip is divided. <bookmark "
            "mark='a'/> Here two tenants share one processor. Each has two cores with private caches; the last-level "
            "cache and the memory bus are shared, and tenant A's working set fits. <bookmark mark='b'/> Then tenant B "
            "streams through gigabytes. Its lines push A's out of the shared cache, Part 9's misses return, and A "
            "slows down although A changed nothing: a noisy neighbour. <bookmark mark='c'/> Newer processors can "
            "divide these too. Intel's cache allocation technology gives each tenant its own ways of the cache, and "
            "memory bandwidth allocation limits its share of the bus."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(cores), FadeIn(l2), FadeIn(tl), FadeIn(llc_t),
                      FadeIn(bus), FadeIn(bus_t), FadeIn(gauge_t), Create(g_base), FadeIn(illus))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in llc], lag_ratio=0.02), GrowFromEdge(fill_a, LEFT),
                      GrowFromEdge(fill_b, LEFT), GrowFromEdge(g, LEFT), run_time=1.5)
            vo.wait_until("b")
            evict = [c for k, c in enumerate(llc) if k % ways < 11 and (k * 7) % 5 != 0]
            fill_b2 = Rectangle(width=bus.width * 0.72, height=0.3, stroke_width=0, fill_color=LAM,
                                fill_opacity=0.8).next_to(fill_a, RIGHT, buff=0)
            self.play(LaggedStart(*[c.animate.set_fill(LAM) for c in evict], lag_ratio=0.08),
                      Transform(fill_b, fill_b2), Transform(g, bar(4.2, NO)), FadeIn(notes[0]), run_time=3)
            vo.wait_until("c")
            self.play(Create(fence))
            self.play(*[c.animate.set_fill(DATA if k % ways < ways // 2 else LAM) for k, c in enumerate(llc)],
                      Transform(g, bar(1.6, YES)), FadeIn(notes[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()


    def sidechannel(self):
        self.ask(r"Two tenants share a processor's cache. \\ Can one learn the other's AES key?", [r"no", r"yes"], 1,
                 say="Two tenants' virtual machines share one processor's cache. Can one learn the other's AES key?",
                 reveal="Yes, by prime and probe: timing which cache sets the victim touched.")
        head = label(r"Side channels: \ prime and probe", font_size=36).to_edge(UP, buff=0.3)
        nsets, nways = 4, 8
        grid = VGroup(*[cell(GREY_E, w=0.45, h=0.45) for _ in range(nsets * nways)])
        grid.arrange_in_grid(rows=nsets, cols=nways, buff=0.04).move_to([-4.1, 0.3, 0])
        rows = [VGroup(*grid[s * nways:(s + 1) * nways]) for s in range(nsets)]
        names = VGroup(*[label(rf"set {s}", font_size=18, color=GREY_A).next_to(r, LEFT, buff=0.15)
                         for s, r in enumerate(rows)])
        gt = label(r"a shared cache, \ four of its sets", font_size=19, color=GREY_A).next_to(grid, UP, buff=0.25)
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.85),
                                 label(t, font_size=17, color=c)).arrange(RIGHT, buff=0.1)
                          for t, c in ((r"attacker's lines", NO), (r"victim's line", DATA))]).arrange(RIGHT, buff=0.4)
        legend.next_to(grid, DOWN, buff=0.3)
        secret = 2
        probe_t = label(r"time to reload", font_size=18, color=HEAD).next_to(grid, RIGHT, buff=0.35).align_to(
            gt, DOWN)
        probes = VGroup(*[Rectangle(width=1.5 if s == secret else 0.45, height=0.32, stroke_width=0,
                                    fill_color=NO if s == secret else YES, fill_opacity=0.85)
                          .next_to(rows[s], RIGHT, buff=0.35) for s in range(nsets)])
        for p in probes:
            p.align_to(probe_t, LEFT)
        slow = label(r"slow: \ a miss", font_size=17, color=NO).next_to(probes[secret], RIGHT, buff=0.12)
        illus = label(r"illustrative", font_size=16, color=GREY_B).next_to(legend, DOWN, buff=0.15)
        steps = VGroup(
            wrapped_label(r"1. \ \textbf{prime}: \ fill every set with your own lines", 4.3, font_size=19,
                          color=NO),
            wrapped_label(r"2. \ the victim runs; \ a lookup that depends on its secret evicts one line", 4.6,
                          font_size=19, color=DATA),
            wrapped_label(r"3. \ \textbf{probe}: \ time each of your lines again; \ the slow set is the one the "
                          r"victim used", 4.3, font_size=19, color=HEAD),
            wrapped_label(r"Osvik, Shamir and Tromer \ (2006) \ read AES keys this way; \ Ristenpart et al. \ "
                          r"(2009) \ placed VMs beside a target in EC2; \ defences: \ no shared cores, \ "
                          r"partitioned caches, \ constant-time code", 4.3, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, -0.1, 0])
        victim_cell = grid[secret * nways + 5]
        with self.voiceover(
            "A shared cache also leaks. <bookmark mark='a'/> In prime and probe, the attacker fills every set of the "
            "cache with its own lines. <bookmark mark='b'/> Then the victim runs. A table lookup at an address that "
            "depends on a secret evicts one of the attacker's lines. <bookmark mark='c'/> The attacker times reading "
            "its lines again: one set is slow, so it knows where the victim looked. <bookmark mark='d'/> In 2006 Dag "
            "Arne Osvik, Adi Shamir and Eran Tromer recovered AES keys this way, and in 2009 Thomas Ristenpart and "
            "colleagues showed how to place a virtual machine beside a chosen target in Amazon's cloud. Defences keep "
            "tenants off shared cores, partition caches, and use code whose memory accesses do not depend on secrets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(names), FadeIn(gt), FadeIn(legend), FadeIn(illus))
            vo.wait_until("a")
            self.play(LaggedStart(*[c.animate.set_fill(NO, 0.85) for c in grid], lag_ratio=0.03), FadeIn(steps[0]),
                      run_time=2)
            vo.wait_until("b")
            self.play(Indicate(rows[secret], color=DATA, scale_factor=1.03), FadeIn(steps[1]))
            self.play(victim_cell.animate.set_fill(DATA, 0.95))
            vo.wait_until("c")
            self.play(FadeIn(probe_t), FadeIn(steps[2]))
            self.play(LaggedStart(*[GrowFromEdge(p, LEFT) for p in probes], lag_ratio=0.4), run_time=2)
            self.play(FadeIn(slow), Indicate(names[secret], color=NO))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
        self.wait(0.4)
        self.clear_scene()

    def domains(self):
        head = label(r"Regions, \ zones, \ racks", font_size=36).to_edge(UP, buff=0.3)
        zones = VGroup()
        racks = []
        for z in range(3):
            rs = VGroup()
            for r in range(3):
                hosts = VGroup(*[Square(0.26, stroke_color=GREY_B, stroke_width=1, fill_color=GREY_D,
                                        fill_opacity=0.9) for _ in range(5)]).arrange(DOWN, buff=0.1)
                frame = SurroundingRectangle(hosts, buff=0.1, color=GREY_B, stroke_width=1.5)
                rs.add(VGroup(frame, hosts))
            rs.arrange(RIGHT, buff=0.22)
            racks.append(rs)
            zf = RoundedRectangle(width=rs.width + 0.5, height=rs.height + 0.9, corner_radius=0.12,
                                  stroke_color=DATA, stroke_width=2)
            zt = label(rf"zone {'abc'[z]}", font_size=19, color=DATA).next_to(zf.get_top(), DOWN, buff=0.12)
            rs.move_to(zf).shift(DOWN * 0.18)
            zones.add(VGroup(zf, zt, rs))
        zones.arrange(RIGHT, buff=0.3)
        region = RoundedRectangle(width=zones.width + 0.5, height=zones.height + 0.95, corner_radius=0.15,
                                  stroke_color=HEAD, stroke_width=2.5)
        rt = label(r"a region: \ a metropolitan area", font_size=20, color=HEAD).next_to(region.get_top(), DOWN,
                                                                                         buff=0.15)
        zones.move_to(region).shift(DOWN * 0.22)
        VGroup(region, rt, zones).move_to([-2.6, -0.35, 0])
        notes = VGroup(
            wrapped_label(r"AWS: \ zones are separate buildings with their own power and networking, \ many "
                          r"kilometres apart but within 100 km of each other", 3.9, font_size=19, color=DATA),
            wrapped_label(r"a \textbf{failure domain}: \ everything that fails together", 3.9, font_size=19,
                          color=WHITE),
            wrapped_label(r"host: \ a disk, \ a power supply, \ a kernel panic", 3.9, font_size=19, color=GREY_A),
            wrapped_label(r"rack: \ one power feed, \ one top-of-rack switch", 3.9, font_size=19, color=KERN),
            wrapped_label(r"zone: \ a building's power or cooling", 3.9, font_size=19, color=NO),
            wrapped_label(r"region: \ rare but real; \ Amazon S3 in Northern Virginia, \ February 2017, \ after "
                          r"a mistyped command", 3.9, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.75, -0.2, 0])
        host = racks[0][1][1][2]
        rack = racks[1][2]
        zone = zones[2]
        with self.voiceover(
            "Clouds are built around failures that come together. <bookmark mark='a'/> A region is a metropolitan "
            "area with several availability zones. Amazon describes its zones as separate buildings with their own "
            "power and networking, many kilometres apart but within a hundred kilometres of each other: far enough "
            "not to fail together, near enough to replicate synchronously. <bookmark mark='b'/> Each level is a "
            "failure domain, a set of things that fail together. <bookmark mark='c'/> A host loses a disk, or panics. "
            "<bookmark mark='d'/> A rack shares a power feed and a switch. <bookmark mark='e'/> A zone can lose power "
            "or cooling. <bookmark mark='f'/> And in February 2017 a mistyped command took Amazon S3 in Northern "
            "Virginia down for about four hours."
        ) as vo:
            self.play(FadeIn(head), FadeIn(region), FadeIn(rt))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(z) for z in zones], lag_ratio=0.3), FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(host.animate.set_fill(NO, 1), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(rack[0].animate.set_stroke(KERN, 3), *[h.animate.set_fill(KERN, 1) for h in rack[1]],
                      FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(zone[0].animate.set_stroke(NO, 3), *[h.animate.set_fill(NO, 1) for r in zone[2] for h in r[1]],
                      FadeIn(notes[4]))
            vo.wait_until("f")
            self.play(region.animate.set_stroke(HEAD, 5), FadeIn(notes[5]))
            self.play(Indicate(rt, color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def placement(self):
        c = load("correlated")
        rs = next(r for r in load("durability")["schemes"] if r["name"] == "RS(10, 4)")
        n, k, nr = rs["n"], rs["k"], c["racks"]
        per = n // nr
        head = label(r"Placement for availability", font_size=36).to_edge(UP, buff=0.3)
        racks = VGroup()
        for r in range(nr):
            frags = VGroup(*[cell(YES, w=0.5, h=0.3) for _ in range(per)]).arrange(DOWN, buff=0.08)
            fr = SurroundingRectangle(frags, buff=0.12, color=GREY_B, stroke_width=1.5)
            racks.add(VGroup(fr, frags, label(rf"rack {r + 1}", font_size=16, color=GREY_A).next_to(fr, DOWN,
                                                                                                    buff=0.08)))
        racks.arrange(RIGHT, buff=0.3).move_to([-3.0, 1.55, 0])
        rt = label(rf"RS({k}, {n - k}): \ any {k} of {n} fragments rebuild the object \ (chapter 8)", font_size=19,
                   color=WHITE).next_to(racks, UP, buff=0.2).align_to(racks, LEFT)
        status = VGroup()
        for d in range(1, c["need_down_together"] + 1):
            left = n - per * d
            ok = left >= k
            status.add(label(rf"{d} rack{'s' if d > 1 else ''} down: \ {left} left" +
                             (r" \ --- \ enough" if ok else r" \ --- \ lost"), font_size=19, color=YES if ok else NO))
        status.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(racks, RIGHT, buff=0.5).align_to(racks, UP)
        one = wrapped_label(rf"all {n} in one rack: \ the first rack failure loses it", 3.6, font_size=19,
                            color=NO).next_to(status, DOWN, buff=0.2).align_to(status, LEFT)

        def quorum(split, title):
            zs = VGroup()
            for m in split:
                dots = VGroup(*[Dot(radius=0.13, color=DATA) for _ in range(m)]).arrange(RIGHT, buff=0.18)
                zf = RoundedRectangle(width=1.5, height=0.7, corner_radius=0.1, stroke_color=GREY_B, stroke_width=1.5)
                dots.move_to(zf)
                zs.add(VGroup(zf, dots))
            zs.arrange(RIGHT, buff=0.25)
            t = label(title, font_size=19, color=WHITE).next_to(zs, UP, buff=0.15)
            return VGroup(t, zs)
        qa = quorum((2, 2, 1), r"five Raft replicas, \ three zones")
        qb = quorum((3, 2), r"five Raft replicas, \ two zones")
        VGroup(qa, qb).arrange(RIGHT, buff=1.2, aligned_edge=DOWN).move_to([-0.3, -1.25, 0])
        ra = label(r"lose any zone: \ $\geq 3$ of 5 remain, \ a majority", font_size=19, color=YES).next_to(
            qa, DOWN, buff=0.2)
        rb = label(r"lose the larger: \ 2 of 5, \ no majority", font_size=19, color=NO).next_to(qb, DOWN, buff=0.2)
        foot = wrapped_label(r"schedulers state this as \textbf{spread constraints} \ (anti-affinity), \ which pull "
                             r"against chapter 5's packing: \ packing wants machines full, \ spreading wants replicas "
                             r"apart \ (Part 50)", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.3)

        def down(rack):
            return [rack[0].animate.set_stroke(NO, 3), *[f.animate.set_fill(NO, 0.3) for f in rack[1]]]
        with self.voiceover(
            "Placement turns failure domains into availability. <bookmark mark='a'/> Chapter eight's code cuts an "
            "object into fourteen fragments, any ten of which rebuild it. Put two in each of seven racks. <bookmark "
            "mark='b'/> One rack fails: twelve remain. A second: ten, still enough. Only a third rack down at once "
            "loses the object; with all fourteen in one rack, the first would. <bookmark mark='c'/> The same rule "
            "protects Part 38's Raft. Five replicas spread two, two and one across three zones survive the loss of "
            "any zone: three of five is still a majority. <bookmark mark='d'/> Spread three and two across two zones, "
            "and losing the larger leaves two: no majority. <bookmark mark='e'/> Schedulers call this a spread "
            "constraint; it pulls against chapter five's packing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rt))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in racks], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("b")
            for d, s in enumerate(status):
                self.play(*down(racks[[1, 4, 6][d]]), FadeIn(s), run_time=0.9)
            self.play(FadeIn(one))
            vo.wait_until("c")
            self.play(FadeIn(qa))
            self.play(qa[1][0][0].animate.set_stroke(NO, 3), qa[1][0][1].animate.set_color(NO), FadeIn(ra))
            vo.wait_until("d")
            self.play(FadeIn(qb))
            self.play(qb[1][0][0].animate.set_stroke(NO, 3), qb[1][0][1].animate.set_color(NO), FadeIn(rb))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()



_ = (BG, KERN, mono)
