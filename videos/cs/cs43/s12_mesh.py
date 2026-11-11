from __future__ import annotations

import base64
import json

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, module_box, mono,
                                   tag_box)


def unb64(s: str) -> str:
    """One part of a JWT, decoded (base64url without padding)."""
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4)).decode()


def compact(obj) -> str:
    return json.dumps(obj, separators=(",", ":"))


class Mesh(VoiceoverScene):
    def construct(self):
        self.card()
        self.discovery()
        self.balance()
        self.sidecar()
        self.oauth()
        self.jwt()
        self.macaroons()

    def card(self):
        card = chapter_card(11, r"Finding, routing and trusting services", r"Which server, \ and who is asking?",
                            lit=(2012, 2014), extra=((2012, r"OAuth 2.0 \ (RFC 6749)"),
                                                     (2014, r"Birgisson et al.: \ macaroons")), part=PART)
        with self.voiceover("Chapter eleven. Finding, routing and trusting services."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def discovery(self):
        head = label(r"Finding a service", font_size=36).to_edge(UP, buff=0.3)
        client = module_box(r"client", DATA, w=1.6, h=0.6, font=19).move_to([-5.7, 1.0, 0])
        rows = VGroup(*[mono(f"orders  10.0.1.{k}:8080", size=16, color=WHITE) for k in (4, 7, 9)]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.14)
        marks = VGroup(*[mono("healthy", size=15, color=YES).next_to(r, RIGHT, buff=0.25) for r in rows])
        body = VGroup(rows, marks)
        reg = RoundedRectangle(width=body.width + 0.6, height=body.height + 0.5, corner_radius=0.12,
                               stroke_color=KERN, stroke_width=2).move_to([-1.3, 1.0, 0])
        body.move_to(reg)
        rt = label(r"registry", font_size=19, color=KERN).next_to(reg, UP, buff=0.1)
        inst = VGroup(*[module_box(rf"orders \ 10.0.1.{k}", HEAD, w=2.4, h=0.5, font=17) for k in (4, 7, 9)])
        inst.arrange(DOWN, buff=0.35).move_to([4.6, 1.0, 0])
        beats = VGroup(*[DashedLine(m.get_left(), [reg.get_right()[0], r.get_y(), 0], color=GREY_B, stroke_width=1.5,
                                    dash_length=0.08) for m, r in zip(inst, rows)])
        bl = label(r"health checks", font_size=16, color=GREY_B).next_to(beats[0], UP, buff=0.08)
        ask = Arrow(client.get_right() + UP * 0.12, reg.get_left() + UP * 0.12, buff=0.05, color=DATA,
                    stroke_width=2, max_tip_length_to_length_ratio=0.1)
        ans = Arrow(reg.get_left() + DOWN * 0.12, client.get_right() + DOWN * 0.12, buff=0.05, color=YES,
                    stroke_width=2, max_tip_length_to_length_ratio=0.1)
        al = label(r"where is orders?", font_size=16, color=DATA).next_to(ask, UP, buff=0.08)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(reg, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(r"instances register as they start and are checked while they run; \ a client asks for "
                          r"the healthy ones \ (Consul, \ etcd, \ ZooKeeper, \ Kubernetes)", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"the plainest registry is DNS: \ a name for the service, \ an address per instance; \ "
                          r"but cached answers are slow to forget a server that has died", 12.4, font_size=20,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Before a client can call a service, it must find one of its servers. <bookmark mark='a'/> Each instance "
            "registers as it starts, and the registry keeps checking that it is healthy. <bookmark mark='b'/> A "
            "client asks for the current healthy addresses. <bookmark mark='c'/> An instance that stops answering its"
            " health checks is dropped, and requests stop going to it. <bookmark mark='d'/> The plainest registry is "
            "DNS: a name for the service, an address per instance. But answers are cached, so DNS is slow to forget a"
            " dead server."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(inst), Create(reg), FadeIn(rt), FadeIn(ill))
            self.play(Create(beats), FadeIn(bl), FadeIn(rows), FadeIn(marks), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(client), GrowArrow(ask), FadeIn(al))
            self.play(GrowArrow(ans))
            vo.wait_until("c")
            self.play(inst[1][0].animate.set_stroke(NO).set_fill(NO, opacity=0.3), beats[1].animate.set_color(NO))
            self.play(Transform(marks[1], mono("dropped", size=15, color=NO).move_to(marks[1], aligned_edge=LEFT)),
                      rows[1].animate.set_opacity(0.35))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def balance(self):
        bal = load("balance")
        P = bal["policies"]
        head = label(r"The power of two choices", font_size=36).to_edge(UP, buff=0.3)
        heights = [3, 1, 4, 2, 5, 1, 3, 2]                  # illustrative queue lengths
        cell, x0, yb = 0.32, -6.3, -0.2
        queues = VGroup()
        for i, h in enumerate(heights):
            col = VGroup(*[Square(cell - 0.04, stroke_width=0, fill_color=DATA, fill_opacity=0.7).move_to(
                [x0 + i * 0.55, yb + (j + 0.5) * cell, 0]) for j in range(h)])
            queues.add(col)
        base = Line([x0 - 0.3, yb, 0], [x0 + 7 * 0.55 + 0.3, yb, 0], color=GREY_C, stroke_width=1.5)
        ql = label(r"queues at 8 servers \ (illustrative)", font_size=17, color=GREY_A).next_to(base, DOWN, buff=0.15)
        ql.align_to(base, LEFT)

        def probe(a, b):
            ra = SurroundingRectangle(VGroup(queues[a], Dot([x0 + a * 0.55, yb, 0], radius=0.01)), color=HEAD,
                                      buff=0.06)
            rb = SurroundingRectangle(VGroup(queues[b], Dot([x0 + b * 0.55, yb, 0], radius=0.01)), color=HEAD,
                                      buff=0.06)
            k = a if heights[a] <= heights[b] else b
            sq = Square(cell - 0.04, stroke_width=0, fill_color=HEAD, fill_opacity=1).move_to(
                [x0 + k * 0.55, yb + (heights[k] + 0.5) * cell + 1.2, 0])
            self.play(Create(ra), Create(rb), FadeIn(sq), run_time=0.6)
            self.play(sq.animate.shift(DOWN * 1.2), run_time=0.6)
            heights[k] += 1
            queues[k].add(sq)
            self.play(FadeOut(ra), FadeOut(rb), run_time=0.3)
        order = [("random", r"random", NO), ("round robin", r"round robin", KERN),
                 ("two choices", r"two choices", YES), ("least loaded", r"least loaded", DATA)]
        rows = [[n, f"{P[k]['mean']:.1f}", f"{P[k]['p99']:.1f}"] for k, n, _ in order]
        tab = grid_table([r"policy", r"mean", r"99th percentile"], rows, widths=[2.6, 1.4, 2.4], row_h=0.48,
                         font_size=20, mono_cols=())
        tab.move_to([3.3, 1.2, 0])
        for i, (_, _, c) in enumerate(order, 1):
            tab.cells[i][0].set_color(c)
        tt = label(rf"{bal['servers']} servers at {bal['load'] * 100:.0f}\% load: \ time in system, \ in service "
                   r"times \ (computed)", font_size=17, color=GREY_A).next_to(tab, UP, buff=0.2)
        hl = SurroundingRectangle(VGroup(*tab.cells[3]), color=YES, buff=0.08)
        bound = VGroup(
            label(r"one random choice: \ fullest of $n$ bins $\approx \dfrac{\ln n}{\ln \ln n}$", font_size=22,
                  color=NO),
            label(r"two choices: \ $\approx \dfrac{\ln \ln n}{\ln 2}$", font_size=22, color=YES),
        ).arrange(RIGHT, buff=0.9).move_to([0, -1.75, 0])
        note = wrapped_label(r"Azar, \ Broder, \ Karlin and Upfal \ (1994): \ a second choice is an exponential "
                             r"improvement; \ a third adds only a constant factor \ (Part 20's balls into bins)",
                             12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Which server should take each request? <bookmark mark='a'/> Choosing at random, some queues grow long by"
            " bad luck. The power of two choices asks two random servers how busy they are and picks the less loaded."
            " <bookmark mark='b'/> With fifty servers at ninety percent load, random choice gives a mean of ten "
            "service times and a ninety-ninth percentile of forty-nine; round robin roughly halves the mean "
            "and cuts the tail to twenty-one; two choices brings "
            "them to two point six and nine. <bookmark mark='c'/> Part 20's balls into bins explains why: with one "
            "random choice the fullest of n bins holds about log n over log log n; with two, about log log n. Azar, "
            "Broder, Karlin and Upfal proved it in 1994."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(queues), FadeIn(ql))
            vo.wait_until("a")
            probe(2, 5)
            probe(0, 4)
            probe(6, 3)
            vo.wait_until("b")
            self.play(FadeIn(tt), FadeIn(tab))
            self.play(Create(hl))
            vo.wait_until("c")
            self.play(FadeIn(bound[0]))
            self.play(FadeIn(bound[1]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def sidecar(self):
        head = label(r"Sidecars and the service mesh", font_size=36).to_edge(UP, buff=0.3)

        def pod(app, color, x):
            a = module_box(app, color, w=1.9, h=0.6, font=19)
            s = module_box(r"sidecar", KERN, w=1.9, h=0.6, font=19)
            g = VGroup(a, s).arrange(DOWN, buff=0.35).move_to([x, 0.55, 0])
            frame = DashedVMobject(RoundedRectangle(width=2.5, height=g.height + 0.5, corner_radius=0.15,
                                                    color=GREY_B, stroke_width=1.5), num_dashes=40).move_to(g)
            link = Line(a.get_bottom(), s.get_top(), color=GREY_B, stroke_width=2)
            return VGroup(frame, a, s, link)
        pa = pod(r"orders", HEAD, -5.1)
        pb = pod(r"payments", YES, 5.1)
        wire = Line(pa[2].get_right(), pb[2].get_left(), color=YES, stroke_width=3)
        lock = label(r"mutual TLS", font_size=18, color=YES).next_to(wire, DOWN, buff=0.12)
        feats = VGroup(*[tag_box(t, KERN, size=15) for t in ("retries", "timeouts", "circuit breaker", "mTLS")])
        feats.arrange(RIGHT, buff=0.2).next_to(wire, UP, buff=0.25)
        cp = module_box(r"control plane \ (Istio, \ Linkerd)", LAM, w=4.4, h=0.6, font=19).move_to([0, 2.45, 0])
        cpl = VGroup(*[DashedLine(cp.get_left() if p is pa else cp.get_right(), p[0].get_top(), color=LAM,
                                  stroke_width=1.5, dash_length=0.08) for p in (pa, pb)])
        cpt = label(r"configuration and certificates", font_size=16, color=LAM).next_to(cp, DOWN, buff=0.1)
        dot = Dot(radius=0.09, color=HEAD).move_to(pa[1])
        path = [pa[2].get_center(), pb[2].get_center(), pb[1].get_center()]
        spiffe = VGroup(mono("spiffe://shop.example/ns/prod/sa/orders", size=16, color=YES),
                        label(r"a workload identity \ (SPIFFE), \ written into the certificate", font_size=18,
                              color=GREY_A)).arrange(DOWN, buff=0.1).move_to([0, -1.35, 0])
        notes = VGroup(
            wrapped_label(r"every call passes through a local proxy \ (Envoy); \ the policy that chapters 5 and 8 "
                          r"asked of every client lives in one place, \ for every language", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"mutual TLS \ (Part 30, \ with certificates on both sides): \ the server learns which "
                          r"service is calling, \ not just that the line is encrypted", 12.4, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Every service needs retries, timeouts and encryption. <bookmark mark='a'/> A service mesh takes them out"
            " of the application: beside each service runs a sidecar proxy, such as Envoy, and every call goes "
            "through it. <bookmark mark='b'/> The sidecar retries with backoff, enforces timeouts, and opens a "
            "circuit breaker to stop calling a server that keeps failing. <bookmark mark='c'/> Between sidecars runs "
            "mutual TLS, Part 30's handshake with certificates on both sides, so the server learns which service is "
            "calling; SPIFFE names each workload. <bookmark mark='d'/> A control plane, such as Istio or Linkerd, "
            "hands out configuration and certificates."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa[0]), FadeIn(pa[1]), FadeIn(pb[0]), FadeIn(pb[1]))
            vo.wait_until("a")
            self.play(FadeIn(pa[2]), FadeIn(pb[2]), Create(pa[3]), Create(pb[3]), Create(wire), FadeIn(notes[0]))
            self.add(dot)
            for p in path:
                self.play(dot.animate.move_to(p), run_time=0.7)
            self.play(FadeOut(dot, scale=0.5), run_time=0.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f) for f in feats[:3]], lag_ratio=0.4), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(feats[3]), FadeIn(lock), FadeIn(notes[1]))
            self.play(FadeIn(spiffe))
            vo.wait_until("d")
            self.play(FadeIn(cp), Create(cpl), FadeIn(cpt))
        self.wait(0.4)
        self.clear_scene()

    def oauth(self):
        head = label(r"OAuth 2.0: \ the authorization-code flow", font_size=36).to_edge(UP, buff=0.3)
        who = [(r"browser", GREY_A), (r"client app", DATA), (r"authorization server", HEAD),
               (r"resource server", YES)]
        xs = [-5.3, -1.75, 1.75, 5.3]
        heads = VGroup(*[module_box(n, c, w=3.0, h=0.5, font=18).move_to([x, 2.45, 0]) for (n, c), x in zip(who, xs)])
        y_end = -1.55
        lines = VGroup(*[DashedLine([x, 2.18, 0], [x, y_end, 0], color=GREY_D, stroke_width=1.5, dash_length=0.08)
                         for x in xs])
        msgs = [(1, 0, r"go to \texttt{/authorize}, \ with $H(v)$", DATA),
                (0, 2, r"the user logs in and consents", GREY_A),
                (2, 0, r"back to the app, \ with a \textbf{code}", HEAD),
                (0, 1, r"the code", GREY_A),
                (1, 2, r"code $+$ verifier $v$", DATA),
                (2, 1, r"access token $+$ refresh token", HEAD),
                (1, 3, r"\texttt{Authorization: Bearer} access token", DATA),
                (3, 1, r"the user's data", YES)]
        arrows = VGroup()
        y = 1.75
        for a, b, t, c in msgs:
            ar = Arrow([xs[a], y, 0], [xs[b], y, 0], buff=0.04, color=c, stroke_width=2.2,
                       max_tip_length_to_length_ratio=0.16 / abs(xs[b] - xs[a]))
            tl = label(t, font_size=16, color=c).next_to(ar, UP, buff=0.04)
            num = label(f"{len(arrows) + 1}", font_size=16, color=GREY_B).next_to(ar.get_start(), LEFT if b > a
                                                                                  else RIGHT, buff=0.08)
            arrows.add(VGroup(ar, tl, num))
            y -= 0.44
        notes = VGroup(
            wrapped_label(r"\textbf{PKCE} \ (RFC 7636): \ the app keeps a random verifier $v$ and first sends only "
                          r"its hash $H(v)$; \ a code stolen on the way is useless without $v$", 12.4, font_size=19,
                          color=DATA),
            wrapped_label(r"the access token is short-lived; \ the refresh token gets a new one without asking the "
                          r"user again \ --- \ and the app never sees the password", 12.4, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Services must also know who is calling. OAuth 2.0, RFC 6749, lets a user grant an app limited access "
            "without sharing a password. <bookmark mark='a'/> The app sends the browser to the authorization server, "
            "<bookmark mark='b'/> where the user logs in and consents. <bookmark mark='c'/> The server sends the "
            "browser back with a short-lived code, <bookmark mark='d'/> and the app exchanges it for an access token "
            "and a refresh token. With PKCE, the app first sent only the hash of a secret, and reveals the secret "
            "now, so a stolen code is useless. <bookmark mark='e'/> The access token rides on each call to the "
            "resource server, and the refresh token renews it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(heads), Create(lines))
            for mk, idx in (("a", (0,)), ("b", (1,)), ("c", (2, 3)), ("d", (4, 5)), ("e", (6, 7))):
                vo.wait_until(mk)
                for i in idx:
                    self.play(GrowArrow(arrows[i][0]), FadeIn(arrows[i][1]), FadeIn(arrows[i][2]), run_time=0.7)
                if mk == "d":
                    self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def jwt(self):
        J = load("jwt")
        hh, hp, hs = J["honest"].split(".")
        fh, fp, fs = J["forged"].split(".")
        head = label(r"JWTs, \ and \texttt{alg: none}", font_size=36).to_edge(UP, buff=0.3)

        def short(s, n=10):
            return s[:n] + "…" if len(s) > n else s
        cols = (DATA, LAM, HEAD)
        dec = VGroup(mono(unb64(hh), size=15, color=DATA), mono(unb64(hp), size=15, color=LAM),
                     label(r"HMAC-SHA256 \ (key, \ header.payload)", font_size=17, color=HEAD))
        dec.arrange(RIGHT, buff=0.6).move_to([0, 1.55, 0])
        if dec.width > 13.2:
            dec.width = 13.2
        parts = VGroup(mono(short(hh), size=17, color=DATA), mono(".", size=22, color=WHITE),
                       mono(short(hp), size=17, color=LAM), mono(".", size=22, color=WHITE),
                       mono(short(hs), size=17, color=HEAD))
        for i, j in ((0, 0), (2, 1), (4, 2)):
            parts[i].next_to(dec[j], UP, buff=0.45)
        for i in (1, 3):
            parts[i].move_to((parts[i - 1].get_right() + parts[i + 1].get_left()) / 2).align_to(parts[0], DOWN)
        ties = VGroup(*[DashedLine(parts[2 * i].get_bottom(), dec[i].get_top(), color=c, stroke_width=1.2,
                                   dash_length=0.06) for i, c in enumerate(cols)])
        names = [r"header", r"payload \ (claims)", r"signature"]
        nl = VGroup(*[label(n, font_size=16, color=c).next_to(d, DOWN, buff=0.1) for n, c, d in zip(names, cols, dec)])

        def verdict(v):
            if v is None:
                return r"rejects", GREY_A
            return (rf"accepts: \ role {v['role']}", NO if v["role"] == "admin" else YES)
        tokens = {"honest": (hh, hp, hs), "payload edited": (hh, fp, hs), "alg: none": (fh, fp, fs)}
        rows, colors = [], []
        for r in J["rows"]:
            h, p, s = tokens[r["token"]]
            alg = json.loads(unb64(h))["alg"]
            role = json.loads(unb64(p))["role"]
            nv, nc = verdict(r["naive"])
            pv, pc = verdict(r["pinned"])
            rows.append([r["token"].replace("alg: none", r"\texttt{alg: none}"), alg, role,
                         short(s, 8) if s else r"(empty)", nv, pv])
            colors.append([WHITE, WHITE, NO if role == "admin" else WHITE, WHITE, nc, pc])
        tab = grid_table([r"token", r"alg", r"role", r"signature", r"trusts the header", r"pins HS256"], rows,
                         widths=[2.6, 1.3, 1.2, 2.2, 2.8, 2.6], row_h=0.5, font_size=19, colors=colors,
                         mono_cols=(1, 2, 3))
        tab.move_to([0, -0.85, 0])
        cells = [VGroup(*tab.cells[i][:4]) for i in range(len(rows) + 1)]
        nverd = VGroup(*[tab.cells[i][4] for i in range(1, len(rows) + 1)])
        pverd = VGroup(*[tab.cells[i][5] for i in range(1, len(rows) + 1)])
        note = wrapped_label(r"RFC 8725 \ (2020): \ the verifier, \ not the token, \ chooses the algorithm "
                             r"\ (computed with our two verifiers)", 12.4, font_size=19,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Access tokens are often JSON Web Tokens, RFC 7519. <bookmark mark='a'/> Three base64 parts joined by "
            "dots: a header naming the algorithm, a payload of claims, here ada with the role reader, and a signature"
            " over both. <bookmark mark='b'/> Our first verifier does whatever the header says. Edit the payload to "
            "say admin, and the signature fails. <bookmark mark='c'/> But set the algorithm to none, which the "
            "standard allows for unsecured tokens, drop the signature, and that verifier accepts a token claiming "
            "admin. <bookmark mark='d'/> The fix, in RFC 8725, is for the server to pin the algorithm it expects. Our"
            " pinned verifier rejects both forgeries."
        ) as vo:
            self.play(FadeIn(head), FadeIn(parts))
            vo.wait_until("a")
            self.play(Create(ties), FadeIn(dec), FadeIn(nl))
            vo.wait_until("b")
            self.play(FadeIn(cells[0]), FadeIn(tab.cells[0][4]), FadeIn(tab.cells[0][5]), Create(tab.rule),
                      FadeIn(cells[1]), FadeIn(cells[2]))
            self.play(FadeIn(nverd[0]), FadeIn(nverd[1]))
            vo.wait_until("c")
            self.play(FadeIn(cells[3]))
            self.play(FadeIn(nverd[2]), Circumscribe(nverd[2], color=NO))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(v) for v in pverd], lag_ratio=0.4), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def macaroons(self):
        head = label(r"Capabilities and macaroons", font_size=36).to_edge(UP, buff=0.3)
        chain = [(r"identifier", r"$\sigma_0 = \mathrm{HMAC}(k, \mathrm{id})$", HEAD),
                 (r"\texttt{service = photos}", r"$\sigma_1 = \mathrm{HMAC}(\sigma_0, c_1)$", DATA),
                 (r"\texttt{op = read}", r"$\sigma_2 = \mathrm{HMAC}(\sigma_1, c_2)$", DATA),
                 (r"\texttt{before 2026-12-01}", r"$\sigma_3 = \mathrm{HMAC}(\sigma_2, c_3)$", LAM)]
        boxes = VGroup()
        for cav, sig, c in chain:
            top = label(cav, font_size=18, color=c)
            bot = label(sig, font_size=18, color=WHITE)
            g = VGroup(top, bot).arrange(DOWN, buff=0.18)
            r = RoundedRectangle(width=3.0, height=1.2, corner_radius=0.1, stroke_color=c, stroke_width=2,
                                 fill_color=BG, fill_opacity=1).move_to(g)
            boxes.add(VGroup(r, g))
        boxes.arrange(RIGHT, buff=0.3).move_to([0, 1.3, 0])
        arr = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.02, color=GREY_B, stroke_width=2,
                             max_tip_length_to_length_ratio=0.4) for i in range(3)])
        who = VGroup(label(r"the issuer, \ with secret key $k$", font_size=17, color=HEAD).next_to(boxes[0], UP,
                                                                                                 buff=0.15),
                     label(r"any holder, \ without $k$: \ attenuate", font_size=17, color=LAM).next_to(
                         VGroup(boxes[2], boxes[3]), UP, buff=0.15))
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(boxes, DOWN, buff=0.12).align_to(boxes, RIGHT)
        lines = VGroup(
            wrapped_label(r"a bearer token is a \textbf{capability}: \ holding it is the permission", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"adding a caveat needs only the last signature; \ removing one would mean inverting "
                          r"HMAC, \ so a token can only be weakened", 12.4, font_size=20, color=LAM),
            wrapped_label(r"the issuer recomputes the chain from $k$ and checks every caveat \ (Birgisson et al., "
                          r"\ 2014); \ Part 55 builds trust this way", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A bearer token is a capability: whoever holds it may use it. Macaroons, from Birgisson and colleagues in"
            " 2014, are capabilities any holder can weaken. <bookmark mark='a'/> The issuer signs an identifier with "
            "its secret key. <bookmark mark='b'/> Each caveat, such as only photos, only reading, only until "
            "December, is signed with the previous signature, so a holder can narrow a token without the key; "
            "removing a caveat would mean undoing a hash. <bookmark mark='c'/> The issuer recomputes the chain and "
            "checks every caveat. Part 55 returns to them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), FadeIn(who[0]), FadeIn(ill))
            vo.wait_until("b")
            for i in (1, 2, 3):
                self.play(GrowArrow(arr[i - 1]), FadeIn(boxes[i], shift=LEFT * 0.2), run_time=0.7)
            self.play(FadeIn(who[1]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]), *[Indicate(b[0], color=YES, scale_factor=1.03) for b in boxes])
        self.wait(0.4)
        self.clear_scene()


_ = (BG,)
