from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, module_box, mono,
                                   tag_box)


def packet(parts, size=15, h=0.5):
    """A packet drawn as a row of header fields: parts are (text, colour)."""
    return VGroup(*[tag_box(t, color=c, size=size, h=h) for t, c in parts]).arrange(RIGHT, buff=0.04)


class Network(VoiceoverScene):
    def construct(self):
        self.card()
        self.vpc()
        self.overlay()
        self.balance()
        self.egress()

    def card(self):
        card = chapter_card(9, r"Cloud networking", r"How do a million private networks share one set of wires?",
                            lit=(2009, 2016), extra=((2009, r"Amazon VPC"),
                                                     (2016, r"Maglev: \ load balancing in software")), part=PART)
        with self.voiceover("Chapter nine. Cloud networking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def vpc(self):
        head = label(r"A private network, \ rented", font_size=36).to_edge(UP, buff=0.3)
        vpc = RoundedRectangle(width=7.6, height=4.7, corner_radius=0.15, stroke_color=DATA, stroke_width=2)
        vpc.move_to([-2.7, 0.2, 0])
        vl = mono("VPC 10.0.0.0/16", size=18, color=DATA).next_to(vpc.get_corner(UL), DR, buff=0.18)
        subnets, insts, sgs = VGroup(), VGroup(), VGroup()
        for j, (z, xs) in enumerate((("a", -4.6), ("b", -0.8))):
            sn = RoundedRectangle(width=3.4, height=3.3, corner_radius=0.1, stroke_color=GREY_B, stroke_width=1.5)
            sn.move_to([xs, -0.15, 0])
            t = VGroup(mono(f"subnet 10.0.{j + 1}.0/24", size=16, color=GREY_A),
                       label(rf"zone {z}", font_size=18, color=GREY_B)).arrange(DOWN, buff=0.08)
            t.next_to(sn.get_top(), DOWN, buff=0.15)
            vms = VGroup(*[tag_box(f"10.0.{j + 1}.{5 + i}", color=YES, size=17, w=2.0, h=0.5)
                           for i in range(2)]).arrange(DOWN, buff=0.4).next_to(t, DOWN, buff=0.4)
            for v in vms:
                sgs.add(DashedVMobject(Rectangle(width=v.width + 0.22, height=v.height + 0.18, color=KERN,
                                                 stroke_width=1.5), num_dashes=40).move_to(v))
            subnets.add(VGroup(sn, t))
            insts.add(vms)
        igw = tag_box("internet gateway", color=HEAD, size=16).move_to([vpc.get_right()[0], 2.0, 0])
        net = label(r"the internet", font_size=19, color=HEAD).next_to(igw, RIGHT, buff=0.7)
        net_a = Arrow(igw.get_right(), net.get_left(), buff=0.08, stroke_width=2, color=HEAD,
                      max_tip_length_to_length_ratio=0.25)
        rt_t = label(r"route table", font_size=19, color=WHITE)
        rt = code_block(["destination    target", "10.0.0.0/16    local", "0.0.0.0/0      gateway"], size=15)
        sg_t = label(r"security group", font_size=19, color=KERN)
        sg = code_block(["allow tcp 443 from anywhere", "replies allowed back"], size=15)
        side = VGroup(VGroup(rt_t, rt).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
                      VGroup(sg_t, sg).arrange(DOWN, aligned_edge=LEFT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.45)
        side.next_to(vpc, RIGHT, buff=0.55).align_to(vpc, DOWN).shift(UP * 0.3)
        line = wrapped_label(r"none of these wires exists: \ two tenants can both use 10.0.1.5 on the same "
                             r"physical network, \ and never see each other's packets", 12.4, font_size=19,
                             color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Every tenant in the warehouse wants what looks like its own private network. "
            "<bookmark mark='a'/> A virtual private cloud gives it one: an address range of its choosing, here "
            "ten dot zero dot zero dot zero slash sixteen in Part 36's notation, cut into subnets, one in each "
            "zone. <bookmark mark='b'/> A route table decides where packets go: anything inside the range stays "
            "local, and everything else goes to a gateway to the internet. <bookmark mark='c'/> Security groups "
            "are firewalls attached to each machine's virtual network card. They are stateful, so the reply to an "
            "allowed connection is allowed back. <bookmark mark='d'/> None of these wires exists. Two tenants can "
            "both choose ten dot zero dot one dot five, on the same physical network, and never see each other's "
            "packets. How?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(vpc), FadeIn(vl))
            self.play(LaggedStart(*[FadeIn(s) for s in subnets], lag_ratio=0.4), FadeIn(insts))
            vo.wait_until("b")
            self.play(FadeIn(igw), GrowArrow(net_a), FadeIn(net), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(sgs), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(line))
        self.wait(0.4)
        self.clear_scene()

    def overlay(self):
        head = label(r"Packets inside packets", font_size=36).to_edge(UP, buff=0.3)
        hosts = VGroup()
        for x, addr, vm in ((-4.6, "192.168.7.21", "10.0.1.5"), (4.6, "192.168.9.40", "10.0.2.7")):
            box = RoundedRectangle(width=3.6, height=2.05, corner_radius=0.12, stroke_color=GREY_B, stroke_width=1.5)
            box.move_to([x, 1.45, 0])
            t = mono(f"host {addr}", size=15, color=GREY_A).next_to(box.get_top(), DOWN, buff=0.12)
            v = tag_box(f"VM {vm}, tenant 7", color=YES, size=15).next_to(t, DOWN, buff=0.17)
            sw = tag_box("virtual switch", color=KERN, size=15).next_to(v, DOWN, buff=0.17)
            hosts.add(VGroup(box, t, v, sw))
        fabric = Line(hosts[0][0].get_right(), hosts[1][0].get_right() * [-1, 1, 1] + [0, 0, 0], color=GREY_C,
                      stroke_width=3)
        fabric.put_start_and_end_on(hosts[0][0].get_right() + DOWN * 0.6, hosts[1][0].get_left() + DOWN * 0.6)
        fl = label(r"the physical network", font_size=16, color=GREY_B).next_to(fabric, DOWN, buff=0.1)
        mapping = VGroup(label(r"mapping, \ kept by the control plane", font_size=17, color=KERN),
                         mono("tenant 7: 10.0.2.7 -> 192.168.9.40", size=14, color=KERN)).arrange(DOWN, buff=0.1)
        mapping.move_to([0, 1.9, 0])
        inner = packet([("IP 10.0.1.5 -> 10.0.2.7", YES), ("data", GREY_B)])
        outer = packet([("IP 192.168.7.21 -> 192.168.9.40", DATA), ("UDP 4789", GREY_A), ("VXLAN: net 7", LAM)])
        whole = VGroup(outer, inner.copy()).arrange(RIGHT, buff=0.04).move_to([0, -0.75, 0])
        inner.move_to(whole[1])
        outer.move_to(whole[0])
        b_in = Brace(inner, DOWN, buff=0.06, color=YES)
        b_out = Brace(outer, DOWN, buff=0.06, color=DATA)
        l_in = label(r"the tenant's packet", font_size=18, color=YES).next_to(b_in, DOWN, buff=0.06)
        l_out = label(r"added by the host, \ for the physical network", font_size=18, color=DATA).next_to(
            b_out, DOWN, buff=0.06)
        dot = Dot(fabric.get_start(), radius=0.1, color=LAM)
        lines = VGroup(
            wrapped_label(r"VXLAN \ (RFC 7348, \ 2014): \ an 8-byte header with a 24-bit network number, \ about 16 "
                          r"million networks; \ with the outer headers, \ 50 bytes a packet", 12.4, font_size=19,
                          color=LAM),
            wrapped_label(r"Amazon runs this on its own Nitro cards; \ Google in software on every host \ "
                          r"(Andromeda, \ 2018)", 12.4, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The answer is encapsulation, Part 36's idea of a packet carried inside another. "
            "<bookmark mark='a'/> A virtual machine sends an ordinary packet, from ten dot zero dot one dot five to "
            "ten dot zero dot two dot seven. Those addresses mean nothing to the physical network. "
            "<bookmark mark='b'/> The host's virtual switch looks up where that destination lives: for this "
            "tenant, it is a virtual machine on another physical host. <bookmark mark='c'/> So it wraps the "
            "packet in a new one, addressed to that host, with a small header naming the tenant's network. In the "
            "VXLAN standard of 2014 that header is eight bytes, with a twenty-four-bit network number, room for "
            "about sixteen million networks. <bookmark mark='d'/> The receiving host unwraps it and hands it to "
            "the right tenant's machine. Every packet carries about fifty extra bytes, which is why such networks "
            "often allow slightly smaller packets. <bookmark mark='e'/> The mapping is the control plane, kept "
            "true by controllers like chapter four's. Amazon runs the data path on its own network cards; Google "
            "in software on every host."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hosts), Create(fabric), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(inner, shift=UP * 0.2), Create(b_in), FadeIn(l_in))
            vo.wait_until("b")
            self.play(FadeIn(mapping), Indicate(hosts[0][3], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(outer, shift=RIGHT * 0.3), Create(b_out), FadeIn(l_out))
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(dot))
            self.play(dot.animate.move_to(fabric.get_end()), run_time=1.5)
            self.play(FadeOut(dot), FadeOut(outer), FadeOut(b_out), FadeOut(l_out), FadeOut(b_in), FadeOut(l_in))
            self.play(inner.animate.next_to(hosts[1][0], DOWN, buff=0.25).align_to(hosts[1][0], RIGHT),
                      Indicate(hosts[1][2], color=WHITE))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def balance(self):
        head = label(r"One address, \ many machines", font_size=36).to_edge(UP, buff=0.3)
        # left: a managed load balancer in front of backends, one failing its health check
        lb = module_box(r"load balancer", KERN, w=2.4, h=0.6, font=19).move_to([-4.0, 1.6, 0])
        lba = mono("203.0.113.10", size=15, color=KERN).next_to(lb, UP, buff=0.12)
        backs = VGroup(*[module_box(rf"backend {i + 1}", DATA, w=1.35, h=0.5, font=16) for i in range(4)])
        backs.arrange(RIGHT, buff=0.18).move_to([-4.0, -0.1, 0])
        links = VGroup(*[Line(lb.get_bottom(), b.get_top(), color=GREY_B, stroke_width=2) for b in backs])
        bad = 2
        xb = Cross(backs[bad], stroke_color=NO, stroke_width=4)
        hc = label(r"fails its health check: \ no new connections", font_size=16, color=NO).next_to(backs, DOWN,
                                                                                                    buff=0.15)
        hl = label(r"one name in front; \ layer 4 by connection, \ or layer 7 by request", font_size=16,
                   color=GREY_A).next_to(hc, DOWN, buff=0.15)
        # right: anycast, the same address announced from three sites (illustrative)
        sites = [(1.5, 1.6), (5.8, 1.3), (3.6, -0.7)]
        sg = VGroup()
        for k, (x, y) in enumerate(sites):
            sq = Square(side_length=0.5, stroke_color=HEAD, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
            inner_sq = Square(side_length=0.5, stroke_width=0, fill_color=HEAD, fill_opacity=0.3).move_to(sq)
            sl = label(rf"site {'ABC'[k]}", font_size=17, color=HEAD).next_to(sq, UP, buff=0.08)
            sl.add_background_rectangle(color=BG, opacity=1, buff=0.04)
            sg.add(VGroup(sq, inner_sq, sl))
        ann = mono("all announce 192.0.2.1", size=15, color=HEAD).move_to([3.7, 2.45, 0])
        rng = random.Random(2)
        clients, routes = VGroup(), VGroup()
        cols = (DATA, LAM, YES)
        for _ in range(14):
            x, y = rng.uniform(0.6, 6.6), rng.uniform(-1.4, 2.0)
            k = min(range(3), key=lambda i: math.dist((x, y), sites[i]))
            if math.dist((x, y), sites[k]) < 0.8:
                continue
            c = Dot([x, y, 0], radius=0.07, color=cols[k])
            clients.add(c)
            routes.add(Line(c.get_center(), sg[k][0].get_center(), color=cols[k], stroke_width=1.5,
                            stroke_opacity=0.7))
        il = label(r"each client reaches the nearest site \ (illustrative)", font_size=16, color=GREY_B).move_to(
            [3.6, -1.75, 0])
        lines = VGroup(
            wrapped_label(r"Maglev \ (Eisenbud et al., \ Google, \ 2016): \ balancing in software on ordinary "
                          r"machines, \ hashing each connection so its packets keep reaching one backend", 12.4,
                          font_size=19, color=KERN),
            wrapped_label(r"anycast: \ one address announced by BGP from many places; \ DNS root servers and content "
                          r"delivery networks work this way \ (Part 48 builds the rest)", 12.4, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A service needs one address in front of many machines. <bookmark mark='a'/> A managed load balancer "
            "is that address. It spreads connections across healthy backends, checks each one's health, and stops "
            "sending new work to any that fail. It can balance by connection, at layer four, or read each HTTP "
            "request, at layer seven. <bookmark mark='b'/> Google's Maglev, described in 2016, does this in "
            "software on ordinary machines, hashing each connection so that its packets keep reaching the same "
            "backend even as balancers come and go. <bookmark mark='c'/> To go global, clouds use anycast. The "
            "same address is announced, through BGP, from many sites at once, and the internet's routers carry "
            "each client to whichever is nearest by their routing. The DNS root servers and content delivery "
            "networks work this way, and Part 48 builds the rest."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lb), FadeIn(lba), Create(links), FadeIn(backs), FadeIn(hl))
            self.play(Create(xb), links[bad].animate.set_stroke(NO, opacity=0.25), FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(sg), FadeIn(ann))
            self.play(FadeIn(clients), Create(routes), FadeIn(il), run_time=2)
            self.bring_to_front(sg)
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def egress(self):
        j = load("job")
        pr = j["prices"]
        out, store = pr["egress per GB"], pr["s3 standard per GB-month"]
        novels = j["bytes"] / 1e9 * out
        head = label(r"Data in is free; \ data out is not", font_size=36).to_edge(UP, buff=0.3)
        region = RoundedRectangle(width=4.2, height=3.0, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2)
        region.move_to([-3.0, 0.7, 0])
        rl = label(r"a region", font_size=18, color=GREY_B).next_to(region.get_top(), DOWN, buff=0.12)
        zones = VGroup(module_box(r"zone a", DATA, w=1.5, h=0.9, font=17),
                       module_box(r"zone b", DATA, w=1.5, h=0.9, font=17)).arrange(RIGHT, buff=0.7).move_to(
            region.get_center() + DOWN * 0.15)
        cross = DoubleArrow(zones[0].get_right(), zones[1].get_left(), buff=0.05, color=HEAD, stroke_width=2.5,
                            tip_length=0.15)
        cl = label(r"billed too", font_size=16, color=HEAD).next_to(cross, DOWN, buff=0.5)
        a_in = Arrow([-6.8, 1.6, 0], [region.get_left()[0], 1.6, 0], buff=0.05, color=YES, stroke_width=3)
        l_in = label(r"in: \ free", font_size=18, color=YES).next_to(a_in, UP, buff=0.08)
        a_out = Arrow([region.get_right()[0], 1.6, 0], [region.get_right()[0] + 1.6, 1.6, 0], buff=0.05, color=NO,
                      stroke_width=3)
        l_out = label(rf"out: \ \${out:.2f}/GB", font_size=18, color=NO).next_to(a_out, UP, buff=0.08)
        # right: storing a gigabyte for a month against sending it out once
        sc = 4.2 / out
        bx = 1.6
        b1 = Rectangle(width=store * sc, height=0.45, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
        b2 = Rectangle(width=out * sc, height=0.45, stroke_width=0, fill_color=NO, fill_opacity=0.85)
        b1.move_to([bx + b1.width / 2, 0.55, 0])
        b2.move_to([bx + b2.width / 2, -0.55, 0])
        t1 = label(rf"store 1 GB for a month: \ \${store:.3f}", font_size=18, color=DATA).next_to(b1, UP, buff=0.08)
        t1.align_to(b1, LEFT)
        t2 = label(rf"send 1 GB out once: \ \${out:.2f}", font_size=18, color=NO).next_to(b2, UP, buff=0.08)
        t2.align_to(b2, LEFT)
        ratio = label(rf"one download costs {out / store:.1f} months of storage", font_size=19,
                      color=HEAD).next_to(b2, DOWN, buff=0.25).align_to(b2, LEFT)
        tb = label(rf"a terabyte out: \ about \${out * 1000:.0f}, \ before volume discounts", font_size=18,
                   color=GREY_A).next_to(region, DOWN, buff=0.3)
        nov = label(rf"our thirty novels, \ {j['bytes'] / 1e6:.0f} MB: \ about {100 * novels:.2f} cents a download",
                    font_size=18, color=GREY_A).next_to(tb, DOWN, buff=0.15).align_to(tb, LEFT)
        lines = VGroup(
            wrapped_label(r"data has gravity: \ computation moves to the data, \ caches near users absorb repeated "
                          r"downloads \ (Part 48), \ and the cost of leaving keeps customers in", 12.4, font_size=19,
                          color=WHITE),
            label(rf"{pr['date']}", font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Finally, the line on the bill that surprises people. <bookmark mark='a'/> Moving data into a cloud is "
            "free. Moving it out to the internet, at Amazon's 2024 list price, costs nine cents a gigabyte, about "
            "ninety dollars a terabyte before volume discounts. Traffic between zones is billed too. "
            "<bookmark mark='b'/> Compare storing it, at two point three cents a gigabyte a month. Sending an "
            "object out once costs as much as keeping it for nearly four months. <bookmark mark='c'/> Our thirty "
            "novels, twenty-five megabytes, would cost about a fifth of a cent to download: harmless for one "
            "reader, not for millions. <bookmark mark='d'/> So data has gravity. Computation moves to where the "
            "data is, caches near the users absorb repeated downloads, as Part 48 will show, and the cost of "
            "leaving is one reason customers stay."
        ) as vo:
            self.play(FadeIn(head), Create(region), FadeIn(rl), FadeIn(zones))
            vo.wait_until("a")
            self.play(GrowArrow(a_in), FadeIn(l_in))
            self.play(GrowArrow(a_out), FadeIn(l_out), FadeIn(tb))
            self.play(GrowFromCenter(cross), FadeIn(cl))
            vo.wait_until("b")
            self.play(GrowFromEdge(b1, LEFT), FadeIn(t1))
            self.play(GrowFromEdge(b2, LEFT), FadeIn(t2))
            self.play(FadeIn(ratio))
            vo.wait_until("c")
            self.play(FadeIn(nov))
            vo.wait_until("d")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()


_ = (BG,)
