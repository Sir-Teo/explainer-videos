from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (CCC, CCN, DATA, HEAD, KERN, NO, PART, WIN, YES, grid_table, load, window_axes)


class OurTcp(VoiceoverScene):
    def construct(self):
        self.card()
        self.traces()
        self.breakdown()
        self.ledger()

    def card(self):
        card = chapter_card(15, r"The novels, \ over our TCP", r"Where do the thirty-five seconds go?",
                            lit=(2026, 2026), extra=((2026, r"ledger row 14"),), part=PART)
        with self.voiceover("Chapter fifteen. The novels, over our TCP."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def traces(self):
        j = load("job")
        head = label(r"The first five seconds", font_size=36).to_edge(UP, buff=0.3)
        g = window_axes(5, x_length=10.0, y_length=4.4, step=1).move_to(DOWN * 0.3)
        trs = {c: g.line(j[c]["trace"], CCC[c], x_max=5) for c in ("reno", "cubic", "bbr")}
        p1 = g.hline(900, GREY_B, r"pipe")
        p2 = g.hline(1800, NO, r"pipe $+$ buffer")
        pipe, pl, full, fl = p1[0], p1[1], p2[0], p2[1]
        leg = VGroup(*[label(CCN[c], font_size=20, color=CCC[c]) for c in ("reno", "cubic", "bbr")]).arrange(
            RIGHT, buff=0.6).next_to(head, DOWN, buff=0.12)
        with self.voiceover(
            "Back to the hook. Our TCP fetches the twenty-five megabytes of novels from Frankfurt, over a hundred "
            "megabits a second, a hundred and eight milliseconds, a buffer of one pipe, and one random loss in a "
            "thousand. Here are the first five seconds. <bookmark mark='a'/> All three start with slow start, "
            "doubling each round trip: about ten round trips, one second, to reach the pipe. "
            "<bookmark mark='b'/> Reno and CUBIC are knocked down by the first random loss before they reach it, "
            "and Reno then crawls back at one packet per round trip. CUBIC's curve climbs faster, and is knocked "
            "down again. <bookmark mark='c'/> BBR's startup overshoots to nearly three pipes, overflowing the buffer "
            "and losing fifteen hundred packets of its own, which it resends without slowing; then it drains and "
            "sits on the pipe until the novels are done, at three point two seconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(pipe), Create(full), FadeIn(pl), FadeIn(fl), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(trs["reno"]), Create(trs["cubic"]), Create(trs["bbr"]), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(leg[0]), Indicate(leg[1]))
            vo.wait_until("c")
            self.play(Indicate(leg[2]))
        self.wait(0.4)
        self.clear_scene()

    def breakdown(self):
        j = load("job")
        head = label(r"Bytes, \ round trips, \ time", font_size=36).to_edge(UP, buff=0.3)
        rows = [[CCN[c], f"{j[c]['seconds']:.1f} s", f"{j[c]['round_trips']:.0f}", f"{j[c]['retx']:,}",
                 f"{j[c]['mbps']:.1f}", f"{j[c]['clean_seconds']:.2f} s"] for c in ("reno", "cubic", "bbr")]
        rows.append([r"the physics", f"{j['floor']:.2f} s", f"{j['floor'] / j['rtt']:.0f}", r"--",
                     f"{j['mbps'] * 1460 / 1500:.1f}", r"--"])
        tab = grid_table([r"", r"time", r"round trips", r"resent", r"Mb/s", r"with no loss"], rows,
                         widths=[2.2, 1.6, 1.9, 1.5, 1.4, 2.1], row_h=0.46, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for k, c in enumerate(("reno", "cubic", "bbr"), start=1):
            for i in range(6):
                tab.cells[k][i].set_color(CCC[c])
        lines = VGroup(
            wrapped_label(rf"{j['bytes']:,} bytes in {j['packets']:,} packets; \ the random losses: \ 13 "
                          r"\ (one in a thousand, \ by chance a few fewer)", 12.4, font_size=20, color=GREY_A),
            wrapped_label(r"\textbf{with no loss all three take 3.2 s}: \ slow start's dozen round trips, \ then the "
                          r"pipe; \ the 11$\times$ is entirely how each reads 13 random losses", 12.4, font_size=21,
                          color=WHITE),
            wrapped_label(r"Reno spends 320 round trips climbing back by one packet each; \ BBR spends 29 and resends "
                          r"1{,}600 packets it dropped itself", 12.4, font_size=21, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Here is the account. <bookmark mark='a'/> Twenty-five million bytes, seventeen thousand packets, of "
            "which thirteen are lost at random. <bookmark mark='b'/> Reno takes thirty-five seconds, three "
            "hundred and twenty round trips, and resends only thirteen packets. CUBIC takes twenty-four. BBR takes "
            "three point two, twenty-nine round trips, and resends sixteen hundred packets, almost all of them "
            "dropped by its own startup. The physics allows two point two. <bookmark mark='c'/> The last column is "
            "the key. On the same path with no random loss, all three take three point two seconds: a dozen round "
            "trips of slow start, then the pipe. The whole factor of eleven comes from how each algorithm "
            "interprets thirteen lost packets. Reno reads each as a full queue and halves; on a path where losses "
            "are noise, that is the wrong theory, and it costs thirty seconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k][:5])) for k in range(1, 5)], lag_ratio=0.3))
            self.play(FadeIn(lines[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(tab.cells[k][5]) for k in range(1, 5)], lag_ratio=0.2), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def ledger(self):
        j = load("job")
        led = j["ledger"]
        row = led[-1]
        head = label(r"Ledger row 14", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.3,
                           label_width=4.8).scale(0.88).move_to(UP * 0.9)
        notes = VGroup(
            label(rf"fetched over our TCP with CUBIC, \ Linux's default: \ {row['fetch_seconds']:.1f} s; \ then "
                  rf"counted under PebbleOS as in row 12: \ {row['count_seconds']:.1f} s", font_size=19, color=HEAD),
            label(rf"total {row['seconds']:.1f} s: \ the network is {row['fetch_seconds'] / row['seconds'] * 100:.0f}"
                  r"\% of the time; \ for the first time in the ledger, \ computing is not the bottleneck",
                  font_size=19, color=WHITE),
            label(rf"with BBR the fetch is {row['bbr_fetch_seconds']:.1f} s; \ with Reno, \ "
                  rf"{row['reno_fetch_seconds']:.1f} s", font_size=19, color=YES),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        for n in notes:
            if n.width > 12.8:
                n.width = 12.8
        with self.voiceover(
            "The ledger gets row fourteen. <bookmark mark='a'/> The novels, fetched from Frankfurt over our TCP "
            "with CUBIC, the default on Linux, in twenty-four seconds, then counted under PebbleOS, as in row "
            "twelve, in under three. <bookmark mark='b'/> Twenty-seven seconds in all, and ninety percent of it is "
            "the network. For the first time in this series, computing is not what limits the Job: distance is. "
            "<bookmark mark='c'/> With BBR the fetch takes three seconds; with Reno, thirty-five. The next parts "
            "spread the Job over many machines, and every one of them will pay this toll to talk to the others."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()


_ = (DATA, KERN, WIN, YES)
