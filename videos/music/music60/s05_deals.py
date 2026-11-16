from __future__ import annotations

import numpy as np

from videos.music.music60.common import *  # noqa: F403


class Deals(SoundScene):
    def construct(self):
        chapter(self, 4, r"Deals and recoupment", r"Why can an artist with a hundred million streams still owe the label?")
        self.terms()
        self.curve()
        self.kinds()
        self.careers()

    # ------------------------------------------------------------------
    def terms(self):
        items = [
            (r"an advance: \ money paid up front, \ to live on and to record with; \ not a loan, \ but repaid from royalties", WHITE),
            (r"a royalty: \ the artist's share of what the label receives, \ often 15 to 25\% for a new artist", WHITE),
            (r"recoupment: \ the advance and the recording costs are charged to the artist's account; \ royalties fill it before any is paid out", WHITE),
            (r"cross-collateralization: \ one album's debt is repaid from the next album's royalties", WHITE),
            (r"the label owns the recordings, \ often for the whole of the copyright's term", TUNE),
        ]
        rows_scene(self, r"a record deal", items,
                   "A record deal, in its classic form, has a few moving parts. <bookmark mark='b'/> An advance: money paid up "
                   "front to live on and to record with. It is not a loan, since ordinary nonreturnable advances are generally recouped from specified earnings rather than personally repayable, subject to contractual exceptions, "
                   "but it is repaid from royalties. <bookmark mark='c'/> A royalty: the artist's share of what the label receives, "
                   "often fifteen to twenty-five percent for a new artist. <bookmark mark='d'/> Recoupment: the advance and the "
                   "recording costs are charged to the artist's account, and royalties fill it before any are paid out. "
                   "<bookmark mark='e'/> Cross-collateralization: one album's debt is repaid from the next album's royalties. "
                   "<bookmark mark='f'/> And the label owns the recordings, often for the whole of the copyright's term.", marks="bcdef")

    # ------------------------------------------------------------------
    def curve(self):
        d = load("deals")
        s = np.array(d["streams"]) / 1e6
        bal = np.array(d["balance"]) / 1e3
        lab = np.array(d["label"]) / 1e3
        ind = np.array(d["indie"]) / 1e3
        ax = frame_axes(width=9.0, height=3.6, xlo=0, xhi=150, ylo=-200, yhi=500, center=DOWN * 0.4 + LEFT * 0.7)
        cb = curve(s, bal, ax.to, color=BLUE, width=3.5)
        cl = curve(s, np.clip(lab, -200, 500), ax.to, color=GREY_B, width=2.5)
        ci = curve(s, np.clip(ind, -200, 500), ax.to, color=TUNE, width=3)
        xt = VGroup(*[label(f"{v}M", font_size=14, color=GREY_A).next_to(ax.to(v, -200), DOWN, buff=0.1) for v in (0, 50, 100, 150)])
        yt = VGroup(*[label(rf"\${v}k", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (-200, 0, 200, 400)])
        need = d["need"] / 1e6
        key = VGroup(label(r"the artist's account, \ label deal", font_size=15, color=BLUE),
                     label(r"the label's position", font_size=15, color=GREY_B),
                     label(r"self-released: \ the artist's take", font_size=15, color=TUNE)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        n1 = label(rf"the label breaks even at {d['label_breakeven'] / 1e6:.0f}M streams", font_size=15, color=GREY_B).next_to(ax.to(d["label_breakeven"] / 1e6, 0), UP, buff=0.5)
        n2 = label(rf"the artist recoups at {need:.0f}M", font_size=15, color=BLUE).move_to(ax.to(120, -140))
        head = label(rf"a \${d['advance'] / 1e3:.0f}k advance and \${d['costs'] / 1e3:.0f}k of recording costs, \ an 18\% royalty", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Here is that arithmetic, stream by stream, at our simulated rate. A new artist gets a hundred-thousand-dollar advance, and the album costs fifty thousand to make; the royalty is eighteen percent. <bookmark mark='a'/> The artist's account starts a hundred and fifty thousand dollars down, and every stream credits eighteen percent of the label's share. It reaches zero only after {say(need)} million streams. <bookmark mark='b'/> The label, keeping eighty-two percent, has its money back after about {say(d['label_breakeven'] / 1000000.0)} million. Between those two numbers, this simplified label cash-flow model has recovered its stated costs while the artist royalty account remains unrecouped; other label costs and contractual terms are omitted, which is the answer to this chapter's question. <bookmark mark='c'/> Self-released, with a distributor taking fifteen percent, the artist earns from the first stream, but paid for the recording, the promotion and the risk themselves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt))
            vo.wait_until("a")
            self.play(Create(cb), FadeIn(key[0]), FadeIn(n2), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cl), FadeIn(key[1]), FadeIn(n1), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ci), FadeIn(key[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kinds(self):
        items = [
            (r"the 360 deal \ (from the 2000s): \ the label takes a share of touring, \ merchandise and sponsorship too", WHITE),
            (r"licence and distribution deals: \ the artist keeps the recordings; \ a smaller advance, \ a larger share", WHITE),
            (r"distributors for everyone: \ a flat fee or a percentage, \ no advance, \ and the artist may retain the master, subject to contracts and the rights of collaborators", WHITE),
            (r"and catalogues have become assets: \ old songs bought and sold, \ valued at many years of their royalties", WHITE),
            (r"the deal is a bet on uncertain success: \ who bears the risk, \ and who keeps the upside", TUNE),
        ]
        rows_scene(self, r"other deals", items,
                   "There are other shapes. <bookmark mark='b'/> The 360 deal, common since the 2000s, gives the label a share of "
                   "touring, merchandise and sponsorship as well. <bookmark mark='c'/> Licence and distribution deals leave the "
                   "artist owning the recordings, for a smaller advance and a larger share. <bookmark mark='d'/> And distributors "
                   "now serve anyone, for a flat fee or a percentage, with no advance, and the artist may retain the master, subject to contracts and the rights of collaborators. "
                   "<bookmark mark='e'/> Meanwhile catalogues of old songs are bought and sold as assets, valued at many years of "
                   "their royalties. <bookmark mark='f'/> Every deal is a bet on uncertain success, and the question is always who "
                   "bears the risk and who keeps the upside.", marks="bcdef")

    # ------------------------------------------------------------------
    def careers(self):
        items = [
            (r"recordings: \ streams, \ downloads, \ vinyl; \ for most musicians, \ a small part of their income", WHITE),
            (r"live: \ concerts and tours; \ for most working musicians, \ the largest part", WHITE),
            (r"songwriting and publishing: \ royalties, \ and synchronization fees for film, \ television and advertising", WHITE),
            (r"teaching, \ session work, \ composing to order, \ merchandise, \ fan subscriptions", WHITE),
            (r"most musicians combine several, \ and many hold other jobs too: \ a portfolio, \ not a salary", TUNE),
        ]
        rows_scene(self, r"how musicians are paid", items,
                   "Step back, and a musician's income has many sources. <bookmark mark='b'/> Recordings: streams, downloads and vinyl; for most musicians, a small part. <bookmark mark='c'/> Live performance: a major source for many working musicians; income composition varies strongly by occupation, country and survey. <bookmark mark='d'/> Songwriting and publishing: royalties, and synchronization fees for film, television and advertising. <bookmark mark='e'/> Teaching, session work, composing to order, merchandise, and fans who subscribe. <bookmark mark='f'/> Surveys of musicians find most combine several, and many hold other jobs too: a portfolio, not a salary.", marks="bcdef")
