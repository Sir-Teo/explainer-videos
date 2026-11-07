from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.napkin()
        self.result()
        self.ledger()

    def card(self):
        card = chapter_card(12, r"The Job at a million books a day", r"What does the series' program cost at scale?",
                            lit=(1965, 2006), extra=((1965, r"Moore's observation"),
                                                     (2006, r"computing rented by the hour")), part=PART)
        with self.voiceover("Chapter twelve. The Job at a million books a day."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def napkin(self):
        j = load("job")
        head = label(r"The napkin", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"books uploaded", r"1,000,000 a day", rf"{j['uploads_per_s']:.1f} a second"],
                [r"reads of results", r"20 per upload", rf"{j['reads_per_s']:.0f} a second"],
                [r"cache hits on reads", rf"{100 * j['cache_hit']:.0f}\%", r"served in a millisecond"],
                [r"work at a 3$\times$ peak", r"uploads $+$ missed reads", rf"{j['peak_work_rps']:.0f} a second"],
                [r"workers at 60\% busy", r"80 ms per book", rf"{j['servers']} workers"],
                [r"storage", r"600 kB per book \ (text $+$ results)", rf"{j['storage_tb_per_year']:.0f} TB a year"]]
        tab = grid_table([r"quantity", r"assumption", r"result"], rows, widths=[3.8, 4.4, 3.4], row_h=0.55,
                         font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        for r in range(1, len(rows) + 1):
            tab.cells[r][2].set_color(HEAD)
        note_ = note(r"assumptions illustrative; \ the 80 ms is Part 48's model of one count", font_size=16).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Scale the Job up to a million books a day. <bookmark mark='a'/> A million uploads a day is about "
            "eleven and a half a second. <bookmark mark='b'/> If each book's results are read twenty times, that is "
            "about two hundred and thirty reads a second, and with a cache answering sixty percent of them, most cost "
            "nothing. <bookmark mark='c'/> At an evening peak of three times the mean, the workers must count about "
            f"{j['peak_work_rps']:.0f} books a second. At eighty milliseconds a book, and keeping them sixty percent "
            f"busy so the queue stays short, that is {j['servers']} workers. <bookmark mark='d'/> And storing the text "
            f"and its results, at six hundred kilobytes a book, grows by about {j['storage_tb_per_year']:.0f} terabytes "
            "a year."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[2])), FadeIn(VGroup(*tab.cells[3])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[4])), FadeIn(VGroup(*tab.cells[5])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[6])))
        self.wait(0.4)
        self.clear_scene()

    def result(self):
        j = load("job")
        head = label(r"The simulated peak hour", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup()
        for t, v, c in ((r"median response", rf"{j['p50_ms']:.0f} ms", DATA), (r"99th percentile", rf"{j['p99_ms']:.0f} ms",
                                                                                NO),
                        (r"workers", rf"{j['servers']}", HEAD), (r"a month of workers", rf"\${j['monthly_dollars']:,.0f}",
                                                                  YES),
                        (r"per book counted", rf"\${j['dollars_per_book'] * 100:.4f} cents".replace(r"\$", ""), KERN)):
            frame = RoundedRectangle(width=3.8, height=1.8, corner_radius=0.15, stroke_color=c, stroke_width=2,
                                     fill_color=BG, fill_opacity=1)
            g = VGroup(label(v, font_size=34, color=c), label(t, font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2)
            g.move_to(frame)
            tiles.add(VGroup(frame, g))
        tiles[:3].arrange(RIGHT, buff=0.3)
        tiles[3:].arrange(RIGHT, buff=0.3)
        VGroup(tiles[:3], tiles[3:]).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.5)
        foot = wrapped_label(r"workers at Part 45's on-demand list price \ (m5.large, \ 2024); \ storage, \ network and "
                             r"people not included", 12.4, font_size=18, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Then we simulated an hour at the peak. <bookmark mark='a'/> The median count that reaches a worker finishes in about "
            f"{j['p50_ms']:.0f} milliseconds, and the ninety-ninth percentile in about {j['p99_ms']:.0f}: the long tail "
            "of an exponential service time, not of queueing, because the workers are only sixty percent busy. "
            f"<bookmark mark='b'/> {j['servers']} workers rented at Part 45's list price cost about "
            f"{j['monthly_dollars']:,.0f} dollars a month, which is about a hundredth of a cent per book. "
            "<bookmark mark='c'/> Storage, the network and above all the people who run it would cost more. But the "
            "counting itself, the thing this series has been optimizing since Part 6, is now almost free."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tiles[0]), FadeIn(tiles[1]))
            vo.wait_until("b")
            self.play(FadeIn(tiles[2]), FadeIn(tiles[3]), FadeIn(tiles[4]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def ledger(self):
        j = load("job")
        led = j["ledger"]
        row = led[-1]
        head = label(r"Ledger row 18", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.26,
                           label_width=4.8).scale(0.82).move_to(UP * 0.7)
        notes = VGroup(
            label(rf"the thirty novels as thirty requests in parallel: \ about {row['seconds']:.2f} s, \ "
                  rf"{row['dollars'] * 100:.3f} cents", font_size=19, color=HEAD),
            label(r"from Part 6's 281 seconds on one Pebble to a third of a second on a service", font_size=19,
                  color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        for n in notes:
            if n.width > 12.8:
                n.width = 12.8
        with self.voiceover(
            "The ledger gets row eighteen. <bookmark mark='a'/> On this service the thirty novels are thirty "
            "requests running in parallel, and the slowest of thirty counts sets the time: about a third of a "
            f"second, for about {row['dollars'] * 1000:.0f} thousandths of a dollar. <bookmark mark='b'/> Part 6's single Pebble took two hundred "
            "and eighty seconds. Every layer of the series in between, pipelines, caches, compilers, algorithms, "
            "networks and services, is somewhere in that factor."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM)
