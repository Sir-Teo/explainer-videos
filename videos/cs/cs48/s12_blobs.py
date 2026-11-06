from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs41.compute import load as load41
from videos.cs.cs45.compute import load as load45
from videos.cs.cs48.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, module_box,
                                   mono, tag_box)


def sci(x: float) -> str:
    """A probability as m x 10^e for Tex."""
    e = math.floor(math.log10(x))
    m = x / 10 ** e
    return rf"${m:.1f} \times 10^{{{e}}}$"


def arrow(a, b, color=GREY_B, buff=0.08, width=2.0):
    return Arrow(a, b, buff=buff, stroke_width=width, color=color, max_tip_length_to_length_ratio=0.12)


def strip(cuts, unit, y, x0, colors, names=None, insert=0):
    """A file drawn as a strip of chunks: `cuts` are chunk boundaries in bytes (units); an inserted sliver of
    `insert` units at the start is drawn in HEAD."""
    g = VGroup()
    if insert:
        g.add(Rectangle(width=insert * unit, height=0.42, stroke_width=0, fill_color=HEAD, fill_opacity=1).move_to(
            [x0 + insert * unit / 2, y, 0]))
    for k, (a, b) in enumerate(zip(cuts, cuts[1:])):
        r = Rectangle(width=(b - a) * unit, height=0.42, stroke_color=BG, stroke_width=2, fill_color=colors[k],
                      fill_opacity=0.65).move_to([x0 + (a + b) / 2 * unit, y, 0])
        cell = VGroup(r)
        if names:
            cell.add(label(names[k], font_size=17, color=WHITE).move_to(r))
        g.add(cell)
    return g


class Blobs(VoiceoverScene):
    def construct(self):
        self.card()
        self.split()
        self.durable()
        self.chunks()
        self.signed()
        self.edge()

    def card(self):
        card = chapter_card(11, r"Blobs and the edge", r"Where do the big bytes live, \ and how do they travel?",
                            lit=(2001, 2006), extra=((2001, r"LBFS: \ content-defined chunks"),
                                                     (2006, r"Amazon S3")), part=PART)
        with self.voiceover("Chapter eleven. Blobs and the edge."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ metadata here, bytes there
    def split(self):
        head = label(r"Metadata here, \ bytes there", font_size=36).to_edge(UP, buff=0.3)
        client = module_box(r"client", DATA, w=1.7, h=0.65, font=19).move_to([-5.6, 0.9, 0])
        api = module_box(r"API", KERN, w=1.5, h=0.65, font=19).move_to([-2.6, 0.9, 0])
        db = module_box(r"metadata database", LAM, w=2.7, h=0.65, font=19).move_to([0.9, 2.0, 0])
        store = module_box(r"object store", YES, w=2.7, h=0.65, font=19).move_to([0.9, -0.2, 0])
        row = code_block(["book_id  4817", "sha256   9f2c...e1", "blob     books/9f2c...e1", "status   ready"],
                         size=16).next_to(db, RIGHT, buff=0.45)
        rowbox = SurroundingRectangle(row, buff=0.12, color=LAM, stroke_width=1.5, corner_radius=0.08)
        objs = VGroup(*[tag_box(t, YES, size=16) for t in ("books/9f2c...e1", "books/a03b...77", "books/...")])
        objs.arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(store, RIGHT, buff=0.45)
        a1 = arrow(client.get_right(), api.get_left())
        a2 = arrow(api.get_right(), db.get_left(), color=LAM)
        a3 = arrow(api.get_right(), store.get_left(), color=YES)
        book = VGroup(Rectangle(width=0.32, height=0.42, stroke_width=0, fill_color=DATA, fill_opacity=0.9),
                      label(r"book", font_size=16, color=DATA).shift(UP * 0.38)).move_to(client.get_top() + UP * 0.45)
        rowdot = Dot(api.get_center(), radius=0.08, color=LAM)
        notes = VGroup(
            wrapped_label(r"a blob is big, \ opaque, \ written once and read many times: \ in a database row it "
                          r"would ride along in every backup, \ replica and cache", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"an \textbf{object store} maps flat keys to immutable objects, \ written and read whole "
                          r"over HTTP \ (Amazon S3, \ 2006, \ and its imitators)", 12.4, font_size=20, color=YES),
            wrapped_label(r"two systems must now agree: \ write the bytes first, \ the row second; \ at worst an "
                          r"orphaned blob, \ which a sweeper deletes \ (Part 43's ordering of side effects)", 12.4,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        foot = note(r"illustrative", font_size=16).to_corner(DR, buff=0.12)
        with self.voiceover(
            "The Job takes books, and books are blobs: big, opaque, written once and read many times. <bookmark "
            "mark='a'/> In database rows, they would ride along in every backup, replica and cache. <bookmark "
            "mark='b'/> Instead the database keeps a small row describing the book: its hash, and a key. <bookmark "
            "mark='c'/> The bytes go to an object store, a flat map from keys to immutable objects, read and written "
            "whole over HTTP: Amazon's S3 since 2006, and its imitators. <bookmark mark='d'/> Two systems must now "
            "agree, so write the bytes first and the row second. A row never points at nothing; at worst a blob is "
            "orphaned, and a sweeper deletes it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(client), FadeIn(api), FadeIn(db), FadeIn(store), GrowArrow(a1),
                      FadeIn(foot))
            self.play(FadeIn(book))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), book.animate.move_to(api.get_top() + UP * 0.45))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(rowdot))
            self.play(rowdot.animate.move_to(db.get_center()), FadeIn(row), Create(rowbox))
            self.remove(rowdot)
            vo.wait_until("c")
            self.play(GrowArrow(a3), book.animate.move_to(store.get_center()), FadeIn(notes[1]))
            self.play(FadeOut(book), LaggedStart(*[FadeIn(o, shift=RIGHT * 0.1) for o in objs], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]), Circumscribe(objs[0], color=HEAD), Circumscribe(row[2], color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ durability: copies against erasure codes
    def durable(self):
        sch = {s["name"]: s for s in load45("durability")["schemes"]}
        head = label(r"Bytes that are not lost", font_size=36).to_edge(UP, buff=0.3)
        n_data, n_par = 10, 4
        sq, gap = 0.4, 0.12
        obj = Rectangle(width=n_data * (sq + gap) - gap, height=sq, stroke_width=0, fill_color=DATA,
                        fill_opacity=0.85)
        obj.move_to([-2.9, 2.35, 0])
        objl = label(r"one object", font_size=18, color=DATA).next_to(obj, LEFT, buff=0.15)
        frags = VGroup(*[Square(side_length=sq, stroke_width=0, fill_color=DATA if i < n_data else LAM,
                                fill_opacity=0.85) for i in range(n_data + n_par)]).arrange(RIGHT, buff=gap)
        frags.move_to([-2.9, 1.25, 0])
        data_part = frags[:n_data].copy().move_to(obj)
        disks = VGroup(*[RoundedRectangle(width=sq + 0.06, height=0.62, corner_radius=0.06, stroke_color=GREY_B,
                                          stroke_width=1.3).move_to(f.get_center() + DOWN * 0.08) for f in frags])
        dl = label(r"14 disks, \ in different racks", font_size=17, color=GREY_A).next_to(disks, DOWN, buff=0.15)
        fl = VGroup(label(r"10 data fragments", font_size=17, color=DATA),
                    label(r"4 parity", font_size=17, color=LAM)).arrange(RIGHT, buff=1.6).next_to(frags, UP, buff=0.2)
        fl[0].align_to(frags[0], LEFT)
        fl[1].align_to(frags[n_data], LEFT)
        lost = [1, 6, 9, 12]
        crosses = VGroup(*[Cross(disks[i], stroke_color=NO, stroke_width=4, scale_factor=0.8) for i in lost])
        order = ["one copy", "three copies", "RS(10, 4)"]
        names = {"one copy": r"one copy", "three copies": r"three copies", "RS(10, 4)": r"10 data $+$ 4 parity"}
        rows = [[names[o], rf"{sch[o]['overhead']:.1f}$\times$", sci(sch[o]["p_loss_year"])] for o in order]
        tab = grid_table([r"stored as", r"space", r"chance of losing it in a year"], rows, widths=[2.8, 1.3, 3.6],
                         row_h=0.5, font_size=20, colors=[[WHITE, GREY_A, NO], [WHITE, NO, YES], [WHITE, YES, YES]],
                         mono_cols=())
        tab.move_to([-2.6, -1.75, 0])
        notes = VGroup(
            wrapped_label(r"three full copies survive two lost disks, \ for three times the space", 4.3,
                          font_size=19, color=WHITE),
            wrapped_label(r"\textbf{erasure coding}: \ a Reed--Solomon code \ (1960) \ computes 4 parity fragments "
                          r"so that \textit{any} 10 of the 14 rebuild the object", 4.3, font_size=19, color=LAM),
            wrapped_label(r"lose any four disks: \ nothing is lost; \ a fifth before repair, \ and it is", 4.3,
                          font_size=19, color=YES),
            wrapped_label(r"Part 45's model: \ 2\% of disks fail a year, \ a day to repair; \ racks fail together, "
                          r"\ so fragments are spread across them", 4.3, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, 0.15, 0])
        with self.voiceover(
            "An object store's whole promise is that bytes are not lost. <bookmark mark='a'/> Three full copies "
            "survive two failed disks, for three times the space. <bookmark mark='b'/> Erasure coding does better. "
            "Cut the object into ten fragments and compute four more with a Reed-Solomon code, so that any ten of the"
            " fourteen rebuild it. <bookmark mark='c'/> Lose any four disks, and nothing is lost. <bookmark "
            "mark='d'/> Part 45's model, with two percent of disks failing a year and a day to repair, gives the "
            "chance of losing an object in a year. Three copies: about four in ten billion. Ten plus four: about four"
            " and a half in a hundred trillion, in less than half the space."
        ) as vo:
            self.play(FadeIn(head), FadeIn(obj), FadeIn(objl))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("b")
            self.add(data_part)
            self.remove(obj)
            self.play(FadeIn(disks), FadeIn(dl), Transform(data_part, frags[:n_data]), FadeIn(fl[0]),
                      FadeOut(objl))
            self.play(LaggedStart(*[GrowFromCenter(f) for f in frags[n_data:]], lag_ratio=0.2), FadeIn(fl[1]),
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in crosses], lag_ratio=0.3),
                      *[data_part[i].animate.set_opacity(0.15) for i in lost if i < n_data],
                      *[frags[i].animate.set_opacity(0.15) for i in lost if i >= n_data], FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ chunks and content addresses
    def chunks(self):
        obj = load41("objects")
        readme = obj["git"]["blobs"]["README.md"]
        same = obj["ours"]["blobs"]["README.md"] == readme
        head = label(r"Chunks named by their contents", font_size=36).to_edge(UP, buff=0.3)
        L, unit, x0 = 48, 0.14, -6.5
        fixed = list(range(0, L + 1, 6))
        cdc = [0, 7, 13, 22, 27, 35, 41, 48]                             # illustrative content-chosen cuts
        names = "ABCDEFGH"
        t1 = label(r"cut every 6 bytes", font_size=19, color=GREY_A).move_to([x0, 2.35, 0], aligned_edge=LEFT)
        f0 = strip(fixed, unit, 1.85, x0, [DATA] * 8, names)
        f1 = strip([c + 1 for c in fixed[:-1]] + [L + 1], unit, 1.25, x0, [NO] * 8,
                   [n + "'" for n in names], insert=1)
        t2 = label(r"cut where the content says", font_size=19, color=GREY_A).move_to([x0, 0.45, 0],
                                                                                    aligned_edge=LEFT)
        c0 = strip(cdc, unit, -0.05, x0, [DATA] * 7, names[:7])
        c1 = strip([1] + [c + 1 for c in cdc[1:]], unit, -0.65, x0, [NO] + [YES] * 6,
                   [names[0] + "'"] + list(names[1:7]), insert=1)
        ins = VGroup(label(r"one byte inserted", font_size=16, color=HEAD).next_to(f1, LEFT, buff=0.1))
        ins.next_to(f1[0], DOWN, buff=0.08).align_to(f1, LEFT)
        ins2 = ins.copy().next_to(c1[0], DOWN, buff=0.08).align_to(c1, LEFT)
        r1 = label(r"every chunk changes", font_size=18, color=NO).next_to(f1, RIGHT, buff=0.2)
        r2 = label(r"one chunk changes", font_size=18, color=YES).next_to(c1, RIGHT, buff=0.2)
        addr = VGroup(mono("README.md", size=17, color=GREY_A), mono("->", size=17, color=GREY_B),
                      mono(readme[:16] + "...", size=17, color=YES)).arrange(RIGHT, buff=0.2)
        addr_l = label(rf"Part 41: \ a file's name is the hash of its bytes; \ ours and real git's agree: \ "
                       rf"{'yes' if same else 'no'}", font_size=18, color=WHITE)
        addr_g = VGroup(addr_l, addr).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([x0, -2.05, 0],
                                                                                        aligned_edge=LEFT)
        notes = VGroup(
            wrapped_label(r"\textbf{multipart upload}: \ pieces sent in parallel, \ a failed piece retried alone, "
                          r"\ one final call stitches the object", 4.0, font_size=19, color=WHITE),
            wrapped_label(r"name each chunk by its hash: \ identical chunks are stored once, \ and every download "
                          r"can be checked", 4.0, font_size=19, color=YES),
            wrapped_label(r"\textbf{content-defined chunking}: \ cut wherever a rolling hash of the last few dozen "
                          r"bytes matches a pattern \ (LBFS, \ 2001); \ cuts move with the content", 4.0,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.75, 0.3, 0])
        foot = note(r"chunk boundaries illustrative", font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Big files travel in pieces. <bookmark mark='a'/> A multipart upload sends pieces in parallel, retries "
            "only a piece that failed, and stitches them together at the end. <bookmark mark='b'/> Name each piece by"
            " the hash of its bytes, as Part 41's git names every object: identical pieces are stored once, and every"
            " download can be checked. <bookmark mark='c'/> But where do the cuts go? Cut every six bytes, and one "
            "byte inserted at the start shifts every boundary: every piece changes. <bookmark mark='d'/> "
            "Content-defined chunking cuts wherever a rolling hash of the last few dozen bytes matches a pattern, as "
            "the low-bandwidth file system did in 2001. Now an insertion changes only the piece it lands in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t1), FadeIn(f0), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(addr_g))
            vo.wait_until("c")
            self.play(FadeIn(f1), FadeIn(ins), FadeIn(r1))
            vo.wait_until("d")
            self.play(FadeIn(t2), FadeIn(c0), FadeIn(notes[2]))
            self.play(FadeIn(c1), FadeIn(ins2), FadeIn(r2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ signed URLs
    def signed(self):
        head = label(r"Signed URLs", font_size=36).to_edge(UP, buff=0.3)
        client = module_box(r"client", DATA, w=1.7, h=0.65, font=19).move_to([-5.4, 0.6, 0])
        api = module_box(r"API \ (holds the key)", KERN, w=2.6, h=0.65, font=19).move_to([-1.4, 2.0, 0])
        store = module_box(r"object store \ (holds the key)", YES, w=3.2, h=0.65, font=19).move_to([-1.4, -0.8, 0])
        a1 = arrow(client.get_top() + RIGHT * 0.2, api.get_left() + DOWN * 0.1)
        a2 = arrow(api.get_left() + UP * 0.15, client.get_top() + LEFT * 0.3, color=KERN)
        a3 = arrow(client.get_bottom(), store.get_left(), color=DATA, width=4)
        l1 = label(r"1. \ may I upload book 4817?", font_size=17, color=GREY_A).next_to(a1.get_center(), DR,
                                                                                         buff=0.05)
        l2 = label(r"2. \ a signed URL", font_size=17, color=KERN).next_to(a2.get_center(), UL, buff=0.15)
        l3 = label(r"3. \ the bytes, \ directly", font_size=17, color=DATA).next_to(a3.get_center(), DL, buff=0.1)
        parts = [("https://store.example/books/9f2c", GREY_A), ("?expires=1793000600", HEAD),
                 ("&sig=7d1e04a9...", LAM)]
        url = VGroup(*[mono(t, size=17, color=c) for t, c in parts]).arrange(RIGHT, buff=0.02)
        url.move_to([0, -2.0, 0])
        url_l = label(r"the URL: \ which object, \ until when, \ and proof that the API said so", font_size=18,
                      color=WHITE).next_to(url, DOWN, buff=0.15)
        code = code_block([
            "# the API signs",
            "msg = 'PUT /books/9f2c 1793000600'",
            "sig = hmac(key, msg)",
            "",
            "# the store checks",
            "ok = hmac(key, request) == sig",
            "ok = ok and now() < expires",
        ], size=16).move_to([4.15, 1.45, 0])
        notes = VGroup(
            wrapped_label(r"change the object or the expiry and the signature fails; \ the application servers never "
                          r"touch a byte", 4.6, font_size=19, color=YES),
            wrapped_label(r"the URL is a capability: \ whoever holds it may use it until it expires, \ so keep "
                          r"expiries short", 4.6, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(code, DOWN, buff=0.4).align_to(code, LEFT)
        foot = note(r"illustrative; \ S3's real scheme is AWS Signature Version 4", font_size=16).to_edge(
            DOWN, buff=0.12)
        with self.voiceover(
            "Who carries the bytes? Not the application servers, if we can help it. <bookmark mark='a'/> The client "
            "asks the API for permission to upload. The API holds a secret key, and returns a URL naming the object "
            "and an expiry time, signed with a keyed hash, an HMAC, of exactly those. <bookmark mark='b'/> The client"
            " sends the bytes straight to the store, which shares the key and checks the signature. Change the object"
            " or the expiry and it fails; after the expiry, the request is refused. <bookmark mark='c'/> Downloads "
            "work the same way. But the link is a capability: whoever holds it may use it, so keep expiries short."
        ) as vo:
            self.play(FadeIn(head), FadeIn(client), FadeIn(api), FadeIn(store), FadeIn(foot))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1))
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(code[:3]))
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in url], lag_ratio=0.4), FadeIn(url_l))
            vo.wait_until("b")
            self.play(GrowArrow(a3), FadeIn(l3), FadeIn(code[3:]))
            self.play(Indicate(store, color=YES), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ cache keys at the edge
    def edge(self):
        head = label(r"Cache keys at the edge", font_size=36).to_edge(UP, buff=0.3)
        reqs = ["/books/9f2c.txt?utm_source=mail", "/books/9f2c.txt?utm_source=feed", "/books/9f2c.txt?sig=a81..."]
        rq = VGroup(*[mono(r, size=16, color=DATA) for r in reqs]).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        rq.move_to([-4.0, 1.3, 0])
        edge = module_box(r"CDN edge", KERN, w=1.8, h=1.6, font=20).move_to([0.2, 1.3, 0])
        origin = module_box(r"origin", GREY_B, w=1.6, h=0.7, font=19).move_to([5.6, 1.3, 0])
        ins = VGroup(*[arrow(r.get_right(), edge.get_left() + UP * (0.4 - 0.4 * k)) for k, r in enumerate(rq)])
        keys_bad = VGroup(*[label(rf"key {k + 1}: \ miss", font_size=17, color=NO) for k in range(3)]).arrange(
            DOWN, buff=0.18).next_to(edge, RIGHT, buff=0.35)
        keys_good = VGroup(label(r"one key: \ 1 miss, \ 2 hits", font_size=17, color=YES)).next_to(
            edge, RIGHT, buff=0.35)
        to_origin = VGroup(*[arrow(keys_bad.get_right() + UP * (0.35 - 0.35 * k), origin.get_left(), color=NO)
                             for k in range(3)])
        to_origin1 = arrow(keys_good.get_right(), origin.get_left(), color=YES)
        hdr = code_block(["Vary: Accept-Encoding", "Cache-Control: public,", "    max-age=31536000, immutable"],
                         size=17)
        notes = VGroup(
            wrapped_label(r"the key is what the edge treats as the same request: \ by default, \ the whole URL", 5.6,
                          font_size=19, color=WHITE),
            wrapped_label(r"normalise it: \ drop parameters that do not change the bytes, \ sort the rest, \ check "
                          r"a signature at the edge but leave it out of the key", 5.6, font_size=19, color=YES),
            wrapped_label(r"\texttt{Vary} adds headers to the key: \ by encoding, \ a few versions; \ by user "
                          r"agent, \ thousands", 5.6, font_size=19, color=HEAD),
            wrapped_label(r"best: \ the content hash in the URL; \ those bytes never change, \ so cache them for a "
                          r"year \ (Part 42), \ and a new version is a new name", 5.6, font_size=19, color=LAM),
        )
        notes[0].next_to(edge, DOWN, buff=0.35).set_x(3.8)
        VGroup(notes[1], notes[2], notes[3]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(
            notes[0], DOWN, buff=0.25).align_to(notes[0], LEFT)
        hdr.next_to(rq, DOWN, buff=1.0).align_to(rq, LEFT)
        hl = label(r"one year, \ in seconds", font_size=17, color=GREY_A).next_to(hdr, DOWN, buff=0.15).align_to(
            hdr, LEFT)
        foot = note(r"illustrative", font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Downloads go through the content delivery network of Parts 42 and 45, and an edge cache is only as good "
            "as its key. <bookmark mark='a'/> By default the key is the whole URL. Add a tracking parameter or a "
            "signature, and three requests for the same book are three keys and three misses at the origin. <bookmark"
            " mark='b'/> So normalise the key: drop parameters that do not change the bytes, and check signatures at "
            "the edge but leave them out of the key. One miss, two hits. <bookmark mark='c'/> A Vary header adds "
            "request headers to the key: by encoding, a few versions; by user agent, thousands. <bookmark mark='d'/> "
            "Better, put the content hash in the URL. Those bytes never change, so the edge may keep them for a year,"
            " and a new version is a new name."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rq), FadeIn(edge), FadeIn(origin), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in ins], lag_ratio=0.3), FadeIn(notes[0]))
            self.play(FadeIn(keys_bad), LaggedStart(*[GrowArrow(a) for a in to_origin], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeOut(to_origin), ReplacementTransform(keys_bad, keys_good), GrowArrow(to_origin1),
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(hdr[0]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(hdr[1:]), FadeIn(hl), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD, LAM, grid_table)
