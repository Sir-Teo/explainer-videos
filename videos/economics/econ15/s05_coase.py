from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403

CATTLE = "#E8C07D"
CROP = "#7BD88F"


class Coase(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Coase: \ the cattle and the corn", r"If the people involved can bargain, \ does it matter who "
             r"is liable?", "Chapter four. Coase: the cattle and the corn.",
             lit={1879: r"Sturges v. Bridgman", 1960: r"Coase", 1991: r"the Nobel"}, scale=("person", "market"),
             horizon=("a year",))
        self.table()
        self.bargain()
        self.costs()

    def table(self):
        c = load("coase")
        b = c["base"]
        tb = c["table"]
        heads = [r"steers", r"crop lost, \\ tons", r"lost by the \\ last steer", r"the last steer's \\ value to the "
                 r"rancher"]
        xs = [-4.6, -2.2, 0.3, 3.0]
        head = VGroup(*[label(h, font_size=19, color=GREY_B).move_to(RIGHT * x + UP * 2.35) for h, x in zip(heads, xs)])
        rule = Line(LEFT * 5.6 + UP * 1.8, RIGHT * 4.4 + UP * 1.8, color=GREY_C, stroke_width=1.5)
        rows = VGroup()
        for i, (n, lost, ml, v) in enumerate(zip(tb["steers"], tb["crop_loss_tons"], tb["marginal_loss"],
                                                 b["values"])):
            y = 1.3 - 0.62 * i
            vt = (r"$-$" if v < 0 else "") + rf"\${abs(v):.2f}"
            rows.add(VGroup(
                label(f"{n}", font_size=24, color=CATTLE).move_to(RIGHT * xs[0] + UP * y),
                label(f"{lost}", font_size=24, color=CROP).move_to(RIGHT * xs[1] + UP * y),
                label(rf"\${ml}", font_size=24, color=SOCIAL).move_to(RIGHT * xs[2] + UP * y),
                label(vt, font_size=24, color=CATTLE).move_to(RIGHT * xs[3] + UP * y)))
        frame = SurroundingRectangle(rows[1], color=E.ACCENT, stroke_width=3, buff=0.12)
        notes = VGroup(
            label(r"Coase's table: \ the crop sells at \$1 a ton, \ a fence costs \$9 a year", font_size=20,
                  color=GREY_A),
            label(r"the rancher's values are Agora's: \ Coase gives none", font_size=18, color=GREY_B),
        ).arrange(DOWN, buff=0.12).next_to(rows, DOWN, buff=0.4)
        side = VGroup(
            label(r"left alone, \\ the rancher keeps 3", font_size=21, color=CATTLE),
            label(r"the third steer is worth \$1.50 \\ and eats \$3 of corn", font_size=21, color=SOCIAL),
            label(r"the best herd \\ for the two together: \ 2", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.3)
        tag = published_tag(r"Coase, JLE 3 (1960), p.\ 3", corner=DR, font_size=13)
        with self.voiceover(
            "The second remedy came from Ronald Coase, in 1960, in what became one of the most cited papers in "
            "economics. Coase began with a cattle rancher whose steers stray onto a farmer's land and eat the crop. "
            "<bookmark mark='a'/> Here is Coase's own table. One steer destroys a ton of crop a year; two, three tons; "
            "three, six; four, ten. The crop sells at a dollar a ton, and fencing the farm would cost nine dollars a "
            "year. Coase didn't say what the steers are worth to the rancher, so Agora supplies the last column. "
            "<bookmark mark='b'/> Left alone, the rancher keeps three steers, since a fourth would be worth "
            "nothing. <bookmark mark='c'/> But the third steer is worth a dollar fifty to the rancher and eats three "
            "dollars of corn. <bookmark mark='d'/> For the two of them together, the best herd is two."
        ) as vo:
            self.play(FadeIn(head), Create(rule), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), FadeIn(notes), run_time=3)
            for mk, r in zip("bcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
                if mk == "d":
                    self.play(Create(frame))
        self.clear_scene()

    def bargain(self):
        c = load("coase")
        b = c["base"]
        lo, hi = b["payment_range"]
        cols = VGroup(
            VGroup(label(r"if the rancher is liable", font_size=26, color=CATTLE),
                   label(r"the rancher pays for the corn the steers eat", font_size=21),
                   label(r"the third steer costs the rancher \$3 \\ and is worth \$1.50: \ it is sold", font_size=21,
                         color=SOCIAL),
                   label(r"the herd: \ 2", font_size=26, color=E.ACCENT)).arrange(DOWN, buff=0.3),
            VGroup(label(r"if the rancher is not liable", font_size=26, color=CROP),
                   label(r"the farmer can pay the rancher to keep fewer", font_size=21),
                   label(rf"the farmer would pay up to \$3 to lose the third steer; \\ the rancher takes anything over "
                         rf"\${lo:.2f}", font_size=21, color=SOCIAL),
                   label(r"the herd: \ 2", font_size=26, color=E.ACCENT)).arrange(DOWN, buff=0.3),
        ).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(UP * 0.7)
        div = Line(UP * 2.3, DOWN * 1.0, color=GREY_C, stroke_width=1.5).move_to(cols.get_center())
        foot = VGroup(
            label(r"either way, \ the steer goes: \ the rule decides only who pays whom", font_size=24,
                  color=E.ACCENT),
            label(r"the Coase theorem: \ if bargaining is free, \ the outcome doesn't depend on who has the right",
                  font_size=22, color=GREY_A),
            label(r"and the problem is reciprocal: \ the steers harm the corn, \ but stopping them harms the rancher",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Coase, JLE 3 (1960), pp.\ 6--7", corner=DR, font_size=13)
        with self.voiceover(
            "Now ask who should be liable for the corn. <bookmark mark='a'/> Suppose the law makes the rancher pay "
            "for the crop the steers destroy. The third steer then costs the rancher three dollars in damages, and "
            "is worth a dollar fifty, so it is sold: the herd is two. <bookmark mark='b'/> Now suppose the rancher is "
            "not liable. Coase's point is that the farmer can pay the rancher to keep fewer steers. The farmer would pay up to "
            "three dollars to be rid of the third, and the rancher would accept anything over a dollar fifty. They strike "
            "a bargain, and the herd is two again. <bookmark mark='c'/> Either way the third steer goes. The law "
            "decides only who pays whom. <bookmark mark='d'/> That is the Coase theorem, as others named it: if "
            "bargaining costs nothing, the efficient outcome happens whoever holds the right. "
            "<bookmark mark='e'/> And Coase added that the problem is reciprocal. The steers harm the corn, but "
            "stopping the steers harms the rancher. The question is not who is to blame, but which harm is larger."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cols[0][0]), FadeIn(cols[1][0]), Create(div))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in cols[0][1:]], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in cols[1][1:]], lag_ratio=0.5), run_time=2.5)
            for mk, r in zip("cde", foot):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def costs(self):
        c = load("coase")
        runs = c["runs"]
        rows = VGroup(
            label(r"but bargaining is rarely free: \ finding each other, \ agreeing, \ enforcing", font_size=24),
            label(rf"in Agora, \ the bargain gains the two of them \${runs['0']['gain_from_bargain']:.2f}", font_size=24,
                  color=CROP),
            label(rf"let it cost \$2 to strike: \ with the rancher liable, \ the herd is still "
                  rf"{runs['2']['liable']}; \ with the rancher not liable, \ it stays {runs['2']['not_liable']}",
                  font_size=23, color=SOCIAL),
            label(r"when bargaining is costly, \ who holds the right decides what happens", font_size=25,
                  color=E.ACCENT),
            label(r"Coase's own conclusion: \ the law should place rights where bargaining would put them",
                  font_size=23, color=GREY_A),
            label(r"a few neighbours can bargain; \ a million people downwind of a power station cannot", font_size=23,
                  color=SMOKE),
        ).arrange(DOWN, buff=0.34).move_to(UP * 0.1)
        hc = label(r"Sturges v.\ Bridgman, \ 1879: \ a confectioner's pestles and a doctor's consulting room",
                   font_size=20, color=GREY_B).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Coase, JLE 3 (1960); \ the numbers: \ Agora", corner=DR, font_size=13)
        with self.voiceover(
            "The theorem is usually misread as a claim that the law doesn't matter. Coase meant the opposite. "
            "<bookmark mark='a'/> Bargaining is rarely free: the parties must find each other, agree, and enforce "
            "what they agreed. <bookmark mark='b'/> In Agora's version, the bargain over the third steer gains the "
            "two of them a dollar fifty. <bookmark mark='c'/> Suppose striking it costs two dollars. With the rancher "
            "liable, no bargain is needed, and the herd is two. With the rancher not liable, the bargain isn't worth "
            "striking, and the herd stays at three. <bookmark mark='d'/> Once bargaining is costly, who holds the "
            "right decides what happens. <bookmark mark='e'/> Coase's conclusion was that the law should place "
            "rights where the parties would have bargained them to. Coase's cases came from English law, like Sturges "
            "against Bridgman in 1879, a confectioner whose pestles shook a doctor's consulting room next door. "
            "<bookmark mark='f'/> A few neighbours can bargain. A million people downwind of a power station cannot, "
            "and that is where Pigou comes back."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
                if mk == "e":
                    self.play(FadeIn(hc))
        self.clear_scene()
