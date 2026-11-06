from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono, words)


def disk(name, data, color, w=1.25):
    body = RoundedRectangle(width=w, height=2.6, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                            fill_color=BG, fill_opacity=1)
    nm = label(name, font_size=18, color=color).next_to(body, UP, buff=0.1)
    bytes_ = VGroup(*[mono(f"{b:02x}", 15, WHITE) for b in data[:6]]).arrange(DOWN, buff=0.12).move_to(body)
    return VGroup(body, nm, bytes_)


class Storage(VoiceoverScene):
    def construct(self):
        self.card()
        self.raid()
        self.cloud()
        self.fountain()

    def card(self):
        card = chapter_card(13, r"Codes for storage", r"How do data centres survive losing whole machines?",
                            lit=(1988, 2012), extra=((1988, r"RAID"), (2002, r"LT codes"), (2012, r"Azure LRC")),
                            part=PART)
        with self.voiceover("Chapter thirteen. Codes for storage."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def raid(self):
        s = load("storage")
        head = label(r"RAID-6: \ lose any two disks", font_size=34).to_edge(UP, buff=0.3)
        disks = VGroup(*[disk(f"D{i}", d, DATA) for i, d in enumerate(s["disks"])],
                       disk("P", s["P"], HEAD), disk("Q", s["Q"], LAM)).arrange(RIGHT, buff=0.22)
        disks.next_to(head, DOWN, buff=0.55)
        x, y = s["lost"]
        crosses = VGroup(*[Cross(disks[i][0], stroke_color=NO, stroke_width=6) for i in (x, y)])
        lines = VGroup(
            label(r"\textbf{P} = $D_0 \oplus D_1 \oplus \cdots \oplus D_5$, \ byte by byte: \ RAID-5 rebuilds any one "
                  r"lost disk", font_size=21, color=HEAD),
            label(r"\textbf{Q} = $\sum_i g^i D_i$ \ in $\mathrm{GF}(256)$: \ a second, \ independent equation",
                  font_size=21, color=LAM),
            label(rf"lose $D_{x}$ and $D_{y}$: \ two equations, \ two unknowns per byte, \ solved in the field", font_size=21,
                  color=NO),
            label(r"rebuilt, \ byte for byte: \ " + ("checked" if s["recovered"] else "failed"), font_size=21,
                  color=YES),
            label(r"a Reed--Solomon code with 2 check symbols, \ read sideways across the disks \ (Anvin's "
                  r"formulation, \ in Linux)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(disks, DOWN, buff=0.45)
        with self.voiceover(
            "Storage is the erasure channel: a dead disk is known to be dead. <bookmark mark='a'/> RAID-5 adds one "
            "disk holding the exclusive or of all the others, byte by byte, and so can rebuild any one that fails. "
            "<bookmark mark='b'/> RAID-6 adds a second check disk, a weighted sum in the field of chapter five, with "
            "a different power of g for each disk. <bookmark mark='c'/> If two disks die, each byte position gives "
            "two equations in two unknowns, and the field lets us solve them. <bookmark mark='d'/> We rebuilt both "
            "lost disks exactly. <bookmark mark='e'/> This is a Reed-Solomon code with two check symbols, read "
            "across the disks; Linux implements it this way, following Peter Anvin."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(dk) for dk in disks[:6]], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(disks[6]), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(disks[7]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Create(crosses), disks[x][2].animate.set_opacity(0.15), disks[y][2].animate.set_opacity(0.15),
                      FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeOut(crosses), disks[x][2].animate.set_opacity(1).set_color(YES),
                      disks[y][2].animate.set_opacity(1).set_color(YES), FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def cloud(self):
        head = label(r"Erasure codes in the data centre", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"3 replicas", r"3.0$\times$", r"any 2", r"1 block"],
                [r"Reed--Solomon (10, 4)", r"1.4$\times$", r"any 4", r"10 blocks"],
                [r"Azure LRC (12, 2, 2)", r"1.33$\times$", r"any 3, \ most 4", r"6 blocks"]]
        tab = grid_table([r"scheme", r"storage", r"lost blocks survived", r"read to repair one"], rows,
                         widths=[4.0, 2.0, 3.4, 3.2], row_h=0.5, font_size=21, mono_cols=(),
                         colors=[[WHITE, NO, YES, HEAD], [WHITE, YES, YES, NO], [WHITE, YES, YES, HEAD]])
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        lines = VGroup(
            label(r"replication is simple and fast to repair, \ but triples the disks", font_size=22, color=WHITE),
            label(r"RS(10,4): \ split into 10 pieces, \ add 4 checks: \ survives more failures with less than half "
                  r"the disks \ (Facebook's f4, \ HDFS)", font_size=22, color=YES),
            label(r"the price is \textbf{repair}: \ rebuilding one lost piece reads 10 others across the network",
                  font_size=22, color=NO),
            label(r"\textbf{local reconstruction codes} \ (Huang et al., \ 2012): \ extra parity per group of 6, \ so "
                  r"common repairs read 6", font_size=22, color=HEAD),
            label(r"the same trade-off is a research field: \ regenerating codes \ (Dimakis et al., \ 2010)",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "At data-centre scale, machines fail every day. <bookmark mark='a'/> The simple defence is three "
            "copies of everything, which triples the disks. <bookmark mark='b'/> A Reed-Solomon code that splits "
            "each block into ten pieces and adds four checks survives any four losses using only one point four "
            "times the space. Facebook's f4 warm storage and Hadoop's file system use exactly this. <bookmark "
            "mark='c'/> The price is repair: rebuilding one lost piece means reading ten others over the network. "
            "<bookmark mark='d'/> Microsoft's Azure storage adds a little more parity, one per local group of six, "
            "so the common single repair reads only six pieces. <bookmark mark='e'/> How little you must read to "
            "repair, for a given amount of storage, became a research field of its own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                if i < 2:
                    self.play(FadeIn(VGroup(*tab.cells[i + 1])), FadeIn(lines[i]))
                else:
                    self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def fountain(self):
        s = load("storage")
        head = label(r"Fountain codes: \ as many checks as you like", font_size=32).to_edge(UP, buff=0.35)
        rows = [[words(int(k)), words(int(v["median"])), f"{v['overhead'] * 100:.0f}\\%",
                 f"{words(v['min'])}--{words(v['max'])}"] for k, v in s["lt"].items()]
        tab = grid_table([r"source blocks $k$", r"received, \ median", r"overhead", r"range"], rows,
                         widths=[3.2, 3.2, 2.2, 3.0], row_h=0.48, font_size=21, mono_cols=(),
                         colors=[[WHITE, DATA, YES, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        lines = VGroup(
            label(r"\textbf{LT codes} \ (Luby, 2002): \ each output is the XOR of a random handful of source blocks",
                  font_size=22, color=WHITE),
            label(r"the sender never stops; \ a receiver collects \textbf{any} outputs, \ from anyone, \ in any order",
                  font_size=22, color=DATA),
            label(r"decoding peels: \ an output with one unknown reveals it; \ substitute; \ repeat", font_size=22,
                  color=HEAD),
            label(r"the robust soliton distribution keeps the peeling going: \ overhead falls as $k$ grows",
                  font_size=22, color=YES),
            label(r"Raptor codes \ (Shokrollahi) \ add a precode: \ broadcast video, \ 3GPP multimedia, \ satellite "
                  r"links", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "One more storage and broadcast trick. <bookmark mark='a'/> Michael Luby's LT codes, from 2002, make "
            "each output block the exclusive or of a random handful of source blocks. <bookmark mark='b'/> The "
            "sender can produce outputs forever, like a fountain, and a receiver just collects enough of them, "
            "from any source, in any order, whichever ones arrive. <bookmark mark='c'/> Decoding peels: any output "
            "with a single unknown source reveals it, which is substituted everywhere, and the process repeats. "
            "<bookmark mark='d'/> With Luby's robust soliton distribution of degrees, we needed about thirty percent "
            "extra blocks for a hundred source blocks, eighteen percent for a thousand, and nine percent for ten "
            "thousand. <bookmark mark='e'/> Amin Shokrollahi's Raptor codes add a precode and bring the overhead to a "
            "few percent; they carry broadcast video and multimedia in mobile networks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
