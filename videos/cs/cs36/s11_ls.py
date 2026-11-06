from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, graph, grid_table, load, world)


class Ls(VoiceoverScene):
    def construct(self):
        self.card()
        self.flood()
        self.loops()

    def card(self):
        card = chapter_card(10, r"Link state", r"What if every router had the whole map?", lit=(1980, 1989),
                            extra=((1980, r"McQuillan et al.: \ new ARPANET routing"), (1989, r"OSPF")), part=PART)
        with self.voiceover("Chapter ten. Link state."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def flood(self):
        ls = load("ls")
        it = load("internet")
        head = label(r"Flood the map, \ then run Dijkstra", font_size=36).to_edge(UP, buff=0.3)
        w = world(it["cities"], it["links"], shift=UP * 0.5)
        lsa = VGroup(*[Dot(w.pos["lon"], radius=0.1, color=YES)])
        lines = VGroup(
            label(r"each router floods a \textbf{link-state advertisement}: \ my neighbours, \ my link costs, \ a "
                  r"sequence number", font_size=20, color=WHITE),
            label(rf"each router forwards a new one on every other link, \ once: \ London's reaches all "
                  rf"{ls['nodes']} routers in {ls['flood_hops']} hops, \ {ls['flood_sent']} messages", font_size=20,
                  color=YES),
            label(r"now every router holds the same map, \ and runs Dijkstra \ (Part 18) \ from itself: \ OSPF, \ "
                  r"IS-IS", font_size=20, color=HEAD),
            label(r"no counting to infinity: \ a failure is announced, \ not inferred", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The ARPANET abandoned distance vector in 1980 for a different idea. <bookmark mark='a'/> Each router "
            "describes only its own links, in a small message called a link-state advertisement, with a sequence "
            "number so that newer news replaces older. <bookmark mark='b'/> It floods the advertisement: every router "
            "that receives a new one passes it on over every other link, once. London's reaches all eight routers "
            "of our internet in three hops. <bookmark mark='c'/> Soon every router holds the same map of the whole "
            "network, and runs Dijkstra's algorithm from Part 18 to find its shortest paths. This is OSPF, and IS-IS, "
            "inside nearly every large network today. <bookmark mark='d'/> And a failure is simply announced. Nobody "
            "has to infer it from silence, so there is no counting to infinity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(lsa))
            vo.wait_until("b")
            order = [("lon", "ams"), ("lon", "par"), ("lon", "nyc"), ("ams", "fra"), ("par", "fra"), ("nyc", "sfo"),
                     ("fra", "sgp"), ("sfo", "tok")]
            for a, b in order:
                e = w.edges[tuple(sorted((a, b)))]
                self.play(e.animate.set_color(YES).set_stroke(width=4), run_time=0.25)
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def loops(self):
        ls = load("ls")
        it = load("internet")
        head = label(r"Until everyone has the news", font_size=36).to_edge(UP, buff=0.3)
        ring = ls["ring"]
        pos = {"lon": [-4.8, 1.2, 0], "ams": [-2.6, 1.9, 0], "fra": [-0.8, 0.6, 0], "par": [-3.2, -0.3, 0]}
        g = graph(pos, [("lon", "ams"), ("ams", "fra"), ("fra", "par"), ("par", "lon")], node_color=HEAD,
                  weights={("lon", "ams"): ring["lon"]["ams"], ("ams", "fra"): ring["ams"]["fra"],
                           ("fra", "par"): ring["fra"]["par"], ("par", "lon"): ring["par"]["lon"]}, r=0.38, font=17)
        cut = Cross(g.edges[("ams", "fra")], stroke_color=NO, stroke_width=4).scale(0.35)
        times = [r"Amsterdam updates at 50 ms", r"Frankfurt at 100 ms", r"Paris at 150 ms", r"London at 250 ms"]
        tl = VGroup(*[label(t, font_size=18, color=GREY_A) for t in times]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        tl.next_to(g, DOWN, buff=0.5).align_to(g, LEFT)
        fates = it["fate"]
        cols = {"delivered": YES, "looped": NO, "dropped": KERN}
        bar = VGroup(*[Rectangle(width=0.14, height=0.5, stroke_width=0, fill_color=cols[f["fate"]], fill_opacity=0.9)
                       for f in fates]).arrange(RIGHT, buff=0.02).move_to([3.4, 1.3, 0])
        bl = label(r"40 packets, \ London to Frankfurt, \ one every 10 ms, \ from the cut", font_size=17,
                   color=GREY_A).next_to(bar, UP, buff=0.15)
        n_d = sum(f["fate"] == "dropped" for f in fates)
        n_l = sum(f["fate"] == "looped" for f in fates)
        n_ok = sum(f["fate"] == "delivered" for f in fates)
        key = VGroup(label(rf"{n_d} dropped at the dead link", font_size=18, color=KERN),
                     label(rf"{n_l} caught in a loop, \ London $\leftrightarrow$ Amsterdam, \ until TTL ran out",
                           font_size=18, color=NO),
                     label(rf"{n_ok} delivered by the new route, \ via Paris", font_size=18, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(bar, DOWN, buff=0.3)
        lines = VGroup(
            label(r"routers recompute at different moments; \ in between, \ their tables can disagree", font_size=20,
                  color=WHITE),
            label(r"Amsterdam already sends Frankfurt's traffic via London; \ London still sends it via Amsterdam: \ "
                  r"a \textbf{microloop}", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Link state is not instantaneous either. <bookmark mark='a'/> In our internet, the cable from Amsterdam "
            "to Frankfurt fails. London has been reaching Frankfurt through Amsterdam. <bookmark mark='b'/> The news "
            "floods, and each router recomputes when it gets to it: Amsterdam first, London last, two hundred "
            "milliseconds later. <bookmark mark='c'/> In between, the tables disagree. Amsterdam now sends "
            "Frankfurt's traffic back to London, and London still sends it to Amsterdam: a loop. "
            "<bookmark mark='d'/> We sent forty packets from London to Frankfurt, one every ten milliseconds, from the "
            "moment of the cut. Five died at the dead link. Sixteen bounced between London and Amsterdam until their "
            "time to live ran out. Only when London updated did packets flow again, via Paris. Real networks shorten "
            "these windows by computing backup routes in advance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cut))
            vo.wait_until("b")
            self.play(FadeIn(tl), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]), Indicate(g.edges[("ams", "lon")], color=NO))
            vo.wait_until("d")
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(r) for r in bar], lag_ratio=0.05), run_time=2)
            self.play(FadeIn(key))
        self.wait(0.3)
        self.clear_scene()


_ = (DATA, grid_table)
