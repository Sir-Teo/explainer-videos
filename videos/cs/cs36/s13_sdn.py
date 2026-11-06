from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (CODE, DATA, HEAD, KERN, LAM, NO, PART, YES, box, grid_table, load, mono)


class Sdn(VoiceoverScene):
    def construct(self):
        self.card()
        self.split()
        self.fabrics()
        self.pipeline()

    def card(self):
        card = chapter_card(12, r"Software-defined networks", r"What if the network were a program?", lit=(2008, 2014),
                            extra=((2008, r"OpenFlow"), (2014, r"P4")), part=PART)
        with self.voiceover("Chapter twelve. Software-defined networks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def split(self):
        head = label(r"Separate the brain from the muscle", font_size=36).to_edge(UP, buff=0.3)
        ctrl = box(5.0, 0.8, r"\text{controller: \ the whole map, \ in software}", YES, font_size=20).move_to([0, 1.8, 0])
        sw = VGroup(*[box(1.8, 0.7, rf"\text{{switch {k}}}", HEAD, font_size=18) for k in range(1, 5)]).arrange(
            RIGHT, buff=0.5).move_to([0, -0.2, 0])
        arrows = VGroup(*[Arrow(ctrl.get_bottom(), s.get_top(), buff=0.08, color=GREY_B, stroke_width=1.8) for s in sw])
        links = VGroup(*[Line(sw[i].get_right(), sw[i + 1].get_left(), color=GREY_C) for i in range(3)])
        lines = VGroup(
            label(r"classic routers run their routing protocol \textit{and} forward, \ each in its own box",
                  font_size=20, color=WHITE),
            label(r"\textbf{SDN}: \ switches only forward, \ by match-action tables; \ a central controller computes "
                  r"and installs the tables \ (OpenFlow, \ 2008)", font_size=20, color=YES),
            label(r"Google's B4 \ (2013) \ runs its data-centre WAN this way at nearly full utilisation", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Everything so far has had each router compute its own routes and forward its own packets. "
            "<bookmark mark='a'/> Software-defined networking pulls those apart. <bookmark mark='b'/> The switches "
            "only forward, by looking packets up in tables of match and action. A controller, a program on ordinary "
            "servers with a view of the whole network, computes what every table should hold and installs it. That "
            "was OpenFlow, from Stanford in 2008. <bookmark mark='c'/> Google's private backbone between its data "
            "centres runs this way, driving its links close to full, because a program with the whole picture can "
            "place traffic far better than independent routers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sw), FadeIn(links), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(ctrl), *[GrowArrow(a) for a in arrows], FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def fabrics(self):
        e = load("ecmp")
        head = label(r"Data-centre fabrics: \ many equal paths", font_size=34).to_edge(UP, buff=0.3)
        ft = e["fat_tree"]
        core = VGroup(*[Dot(radius=0.08, color=YES) for _ in range(4)]).arrange(RIGHT, buff=0.55).move_to([-3.3, 2.0, 0])
        agg = VGroup(*[Dot(radius=0.08, color=HEAD) for _ in range(8)]).arrange(RIGHT, buff=0.3).move_to([-3.3, 1.0, 0])
        edge = VGroup(*[Dot(radius=0.08, color=DATA) for _ in range(8)]).arrange(RIGHT, buff=0.3).move_to([-3.3, 0.0, 0])
        hosts = VGroup(*[Dot(radius=0.05, color=GREY_B) for _ in range(16)]).arrange(RIGHT, buff=0.12).move_to([-3.3, -0.8, 0])
        wires = VGroup()
        for p in range(4):
            for a in range(2):
                ai = 2 * p + a
                for c in range(2):
                    wires.add(Line(agg[ai].get_center(), core[2 * a + c].get_center(), color=GREY_D, stroke_width=1))
                for ed in range(2):
                    wires.add(Line(agg[ai].get_center(), edge[2 * p + ed].get_center(), color=GREY_D, stroke_width=1))
        for i in range(16):
            wires.add(Line(edge[i // 2].get_center(), hosts[i].get_center(), color=GREY_D, stroke_width=0.8))
        fl = label(rf"a $k = 4$ fat tree: \ {ft['hosts']} hosts, \ {ft['switches']} identical switches, \ "
                   rf"{ft['paths_between_pods']} equal paths between pods", font_size=17, color=GREY_A).next_to(hosts, DOWN,
                                                                                                         buff=0.2)
        rows = [[str(r["paths"]), str(r["flows"]), f"{r['equal']:.2f}", f"{r['pareto']:.2f}"] for r in e["rows"]]
        tab = grid_table([r"paths", r"flows", r"busiest path / mean, \ equal flows", r"heavy-tailed flows"], rows,
                         widths=[1.1, 1.1, 3.4, 2.4], row_h=0.38, font_size=17, mono_cols=())
        tab.move_to([3.4, 1.0, 0])
        for r in range(1, len(rows) + 1):
            tab.cells[r][3].set_color(NO)
        lines = VGroup(
            label(r"Clos networks of cheap identical switches \ (Al-Fares et al., 2008) \ give every pair of hosts many "
                  r"shortest paths", font_size=19, color=WHITE),
            label(r"\textbf{ECMP}: \ hash each flow's addresses and ports to pick a path, \ so a flow's packets stay in "
                  r"order", font_size=19, color=HEAD),
            label(r"but hashing is balls into bins \ (Part 20): \ the busiest path carries 1.5--2 times the mean, \ and "
                  r"a few elephant flows make it 2--5", font_size=19, color=NO),
            label(r"responses: \ split flows into \textit{flowlets} at pauses, \ spray packets and reorder at the end, \ "
                  r"or let a controller place the elephants", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Inside a data centre the network looks different again. <bookmark mark='a'/> Instead of a few huge "
            "routers, thousands of small identical switches are wired in layers, a Clos network, so that between any "
            "two racks there are many equally short paths. A four-port fat tree already gives four between every pair "
            "of pods. <bookmark mark='b'/> Switches spread traffic over the paths by hashing each flow's addresses and "
            "ports, equal-cost multipath, so that one flow's packets follow one path and stay in order. "
            "<bookmark mark='c'/> But hashing is the balls-into-bins game of Part 20. With equal flows, the busiest "
            "path carries one and a half to two times its share. Real flows are heavy-tailed, and a few elephants "
            "make it two to five times. <bookmark mark='d'/> So fabrics split flows at natural pauses, spray packets "
            "and reorder them at the receiver, or let a controller with the whole picture place the elephants."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(wires), FadeIn(core), FadeIn(agg), FadeIn(edge), FadeIn(hosts), FadeIn(fl), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def pipeline(self):
        s = load("sdn")
        head = label(r"A programmable pipeline", font_size=36).to_edge(UP, buff=0.3)
        stages = VGroup(*[box(1.9, 0.75, rf"\text{{{t}}}", c, font_size=18) for t, c in (
            ("parse", GREY_B), ("ACL (ternary)", NO), ("route (LPM)", HEAD), ("QoS (exact)", LAM), ("TTL", KERN),
            ("deparse", GREY_B))]).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.5)
        arrows = VGroup(*[Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=0.04, color=GREY_B,
                                stroke_width=1.5, max_tip_length_to_length_ratio=0.3) for i in range(5)])
        rows = []
        for p in s["packets"]:
            fate = f"port {p['port']}" if p["port"] is not None else "dropped"
            steps = ", ".join(f"{t[0]}:{t[1][0] if isinstance(t[1], list) else t[1]}" for t in p["trace"])
            rows.append([p["dst"], str(p["ttl"]), str(p["dscp"]), fate, steps])
        tab = grid_table([r"destination", r"TTL", r"DSCP", r"result", r"what each table did"], rows,
                         widths=[2.0, 0.8, 1.0, 1.4, 7.4], row_h=0.42, font_size=17, mono_cols=(0, 4))
        tab.next_to(stages, DOWN, buff=0.6).set_x(0)
        for r, p in enumerate(s["packets"], start=1):
            tab.cells[r][3].set_color(YES if p["port"] is not None else NO)
        lines = VGroup(
            label(r"\textbf{P4} \ (2014): \ the programmer declares the headers, \ the tables and the actions; \ the "
                  r"chip implements them at line rate", font_size=20, color=YES),
            label(r"a new protocol no longer waits years for new silicon: \ it is a recompile", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The next step made the switches themselves programmable. <bookmark mark='a'/> In P4, a language from "
            "2014, the programmer declares the packet's headers, a sequence of tables, and their actions, and a "
            "compiler maps them onto the switch chip, which still runs at line rate. Here is a small one, written "
            "with our instruments: parse, an access list, a longest-prefix route, a quality-of-service counter, "
            "the time to live. <bookmark mark='b'/> Four packets through it. One forwarded on port three; a voice "
            "packet counted and forwarded; one blocked by the access list; one whose time to live ran out. "
            "<bookmark mark='c'/> A new protocol used to need new chips, years away. Now it is a recompile."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in stages], lag_ratio=0.2), *[GrowArrow(a) for a in arrows],
                      FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()


_ = (CODE, DATA, mono)
