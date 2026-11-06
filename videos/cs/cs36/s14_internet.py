from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, HEAD, KERN, LAM, NAMES, NO, PART, YES, grid_table, load, world)


class Internet(VoiceoverScene):
    def construct(self):
        self.card()
        self.matrix()
        self.load()
        self.failure()

    def card(self):
        card = chapter_card(13, r"Our internet", r"Does it all work together?", lit=(1983,),
                            extra=((1983, r"the flag day"),), part=PART)
        with self.voiceover("Chapter thirteen. Our internet."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def matrix(self):
        it = load("internet")
        head = label(r"Four Pebbles, \ eight routers, \ ten cables", font_size=34).to_edge(UP, buff=0.3)
        w = world(it["cities"], it["links"], shift=UP * 0.6, scale=0.95)
        hosts = {h: v[1] for h, v in it["hosts"].items()}
        hl = VGroup(*[label(rf"\textbf{{{h.replace('pebble', 'P')}}}", font_size=16, color=YES).next_to(
            w.dots[c], DOWN + LEFT * 0.4, buff=0.05) for h, c in hosts.items()])
        names = ["pebble1", "pebble2", "pebble3", "pebble4"]
        rows = []
        for a in names:
            row = [rf"{a} \ ({NAMES[hosts[a]]})"]
            for b in names:
                if a == b:
                    row.append("--")
                else:
                    k = f"{min(a, b)}-{max(a, b)}"
                    row.append(f"{it['matrix'][k]['ms']:.1f}")
            rows.append(row)
        tab = grid_table([r"ping, \ ms"] + [n.replace("pebble", "P") for n in names], rows,
                         widths=[3.6, 1.2, 1.2, 1.2, 1.2], row_h=0.36, font_size=17, mono_cols=())
        tab.to_edge(DOWN, buff=0.4).set_x(-2.4)
        lines = VGroup(
            wrapped_label(r"routes by link state, \ costs by delay; \ forwarding by longest prefix; \ TTL, \ ICMP", 5.0, font_size=18,
                  color=WHITE),
            wrapped_label(r"Frankfurt to Tokyo goes east, \ via Singapore: \ 160 ms; \ London to Tokyo, \ 167", 5.0, font_size=18,
                  color=HEAD),
            wrapped_label(r"every number is a sum of cable lengths over $2c/3$, \ plus microseconds of queueing", 5.0, font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(tab, RIGHT, buff=0.5).align_to(tab, UP)
        with self.voiceover(
            "Now the whole stack at once. <bookmark mark='a'/> Our internet has eight routers in eight cities, ten "
            "cables of realistic length, and four Pebbles attached to it. Routers flood link state, compute shortest "
            "paths by delay, and forward every packet by longest-prefix match, decrementing its time to live. "
            "<bookmark mark='b'/> Pinging every pair: Frankfurt to London, seven milliseconds; San Francisco to "
            "Tokyo, eighty-one; Frankfurt to Tokyo goes east through Singapore, a hundred and sixty. "
            "<bookmark mark='c'/> Each number is the length of the cables divided by the speed of light in glass, "
            "plus a few microseconds of transmission and queueing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w), FadeIn(hl))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def load(self):
        q = load("queueing")
        head = label(r"Delay under load", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{r['rho']:.0%}".replace("%", r"\%"), f"{r['mean_ms']:.2f}", f"{r['p99_ms']:.2f}",
                 f"{r['wait_ms'] * 1000:.0f}", f"{r['pk_ms'] * 1000:.0f}"] for r in q["rows"]]
        tab = grid_table([r"link busy", r"ping, \ mean ms", r"99th percentile", r"queueing, \ $\mu$s",
                          r"Pollaczek--Khinchine"], rows, widths=[1.8, 2.0, 2.2, 2.0, 2.8], row_h=0.38, font_size=18,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        for r in range(1, len(rows) + 1):
            tab.cells[r][3].set_color(YES)
            tab.cells[r][4].set_color(HEAD)
            tab.cells[r][2].set_color(NO)
        eq = MathTex(r"W = \frac{\rho\,S}{2(1 - \rho)}", font_size=34, color=HEAD).next_to(tab, DOWN, buff=0.3)
        lines = VGroup(
            label(rf"a 100 Mb/s link carrying 1{{,}}500-byte packets at random, \ and 400 pings across it", font_size=19,
                  color=WHITE),
            label(r"queueing follows the formula of Part 31: \ small until the link is busy, \ then without bound as "
                  r"$\rho \to 1$", font_size=19, color=HEAD),
            label(r"the tail grows faster than the mean: \ at 95\%, \ one ping in a hundred waits 4.5 ms in the queue",
                  font_size=19, color=NO),
            label(r"\textbf{bufferbloat}: \ huge router buffers turn this into seconds; \ the next part's congestion "
                  r"control decides how full they get", font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Propagation is fixed, but queueing is not. <bookmark mark='a'/> We loaded a hundred-megabit link in our "
            "internet with random full-sized packets and sent four hundred pings across it. <bookmark mark='b'/> At "
            "low load the pings barely notice. As the link gets busy, the time spent waiting grows like rho over one "
            "minus rho, the Pollaczek-Khinchine formula of Part 31, and the measured waits follow it. "
            "<bookmark mark='c'/> The tail grows faster still: at ninety-five percent load, one ping in a hundred "
            "spends four and a half milliseconds in the queue. <bookmark mark='d'/> Real routers with huge buffers "
            "can turn this into seconds, a problem called bufferbloat, and how full those buffers get is decided by "
            "the congestion control of the next part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(eq), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def failure(self):
        it = load("internet")
        head = label(r"Cut a cable", font_size=36).to_edge(UP, buff=0.3)
        w = world(it["cities"], it["links"], shift=UP * 0.6, scale=0.95)
        bp = [x for x in it["before"]["path"] if x in it["cities"]]
        ap = [x for x in it["after"]["path"] if x in it["cities"]]
        before = VGroup(*[Line(w.pos[a], w.pos[b], color=DATA, stroke_width=5) for a, b in zip(bp, bp[1:])])
        after = VGroup(*[Line(w.pos[a], w.pos[b], color=YES, stroke_width=5) for a, b in zip(ap, ap[1:])])
        cut = Cross(w.edges[("ams", "fra")], stroke_color=NO, stroke_width=5).scale(0.5)
        lines = VGroup(
            label(rf"London to Frankfurt: \ {it['before']['ms']:.2f} ms via Amsterdam; \ after the cut, \ "
                  rf"{it['after']['ms']:.2f} ms via Paris", font_size=20, color=YES),
            label(r"in between: \ 5 packets dropped at the dead link, \ 16 looping until their TTL expired, \ then "
                  r"delivery resumed", font_size=20, color=NO),
            label(r"every mechanism of this part, \ at once: \ link-state flooding, \ Dijkstra, \ LPM, \ TTL, \ and "
                  r"the transient loop of chapter 10", font_size=20, color=HEAD),
            label(r"the network repaired itself, \ with nobody in charge: \ Baran's design goal, \ met", font_size=20,
                  color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And then we cut a cable. <bookmark mark='a'/> Traffic from London to Frankfurt had gone through "
            "Amsterdam, in seven milliseconds. After the cut, and after the routers reconverge, it goes through "
            "Paris, in eight. <bookmark mark='b'/> In between, as in chapter ten, five packets died at the dead link "
            "and sixteen looped until their time to live ran out. <bookmark mark='c'/> Every mechanism of this part "
            "took part: flooding, Dijkstra, longest-prefix match, the time to live that ended the loop. "
            "<bookmark mark='d'/> And nobody was in charge. The network found its own way around the damage, which is "
            "exactly what Paul Baran designed it to do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w), FadeIn(before))
            vo.wait_until("a")
            self.play(Create(cut))
            self.play(FadeOut(before), FadeIn(after), FadeIn(lines[0]))
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()


_ = (KERN,)
