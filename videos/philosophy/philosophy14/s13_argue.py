from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403

TRIAL = {"P1": r"P1: \ the witness saw him", "D1": r"D1: \ she was drunk", "P2": r"P2: \ her blood test was clean",
         "D2": r"D2: \ the test was contaminated", "P3": r"P3: \ the lab log shows no contamination",
         "D3": r"D3: \ the log was altered"}


class Argue(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Arguments that attack", r"Which arguments survive their attackers?", lit=(1995,),
                            part=PART)
        with self.voiceover("Chapter twelve. Arguments that attack."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.semantics()
        self.small()
        self.trial()
        self.uses()

    def semantics(self):
        hc = history_card(1995, r"Phan Minh Dung", r"`On the Acceptability of Arguments'", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = stack([
            (r"forget what arguments say: \ keep only who attacks whom", WHITE),
            (r"conflict-free: \ no member attacks another", GREY_A),
            (r"admissible: \ conflict-free, \ and defends each member against every attacker", BEL),
            (r"grounded: \ accept the unattacked, \ reject what they attack, \ repeat", OK),
            (r"preferred: \ maximal admissible; \ \ stable: \ attacks everything outside", NEW),
            (r"Dung: \ default logic, \ logic programming \ and $n$-person games are all instances", GOAL),
        ], font_size=23, buff=0.3, width=12.4, aligned_edge=LEFT).next_to(hc, DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "In 1995 Phan Minh Dung made a radical abstraction. <bookmark mark='a'/>Forget what the arguments say; keep "
            "only which argument attacks which. <bookmark mark='b'/>A set of arguments is conflict-free if none of them "
            "attacks another. <bookmark mark='c'/>It is admissible if, in addition, it defends each of its members: "
            "every attacker of a member is attacked by some member. <bookmark mark='d'/>The grounded extension is the "
            "cautious answer: accept the unattacked arguments, reject what they attack, and repeat until nothing "
            "changes. <bookmark mark='e'/>The preferred extensions are the bold answers, the maximal admissible sets; "
            "a stable extension attacks everything outside it. <bookmark mark='f'/>Dung showed that default logic, "
            "logic programming, and the solutions of n-person games are all instances of this one structure."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def small(self):
        d = load("argue")
        head = label(r"Three small frameworks", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        specs = [("reinstatement", {"a": [-5.6, 0.6], "b": [-4.2, 0.6], "c": [-2.8, 0.6]}, r"reinstatement"),
                 ("mutual attack", {"a": [-0.7, 0.6], "b": [0.7, 0.6]}, r"mutual attack"),
                 ("odd cycle", {"a": [4.2, 1.3], "b": [5.4, -0.1], "c": [3.0, -0.1]}, r"odd cycle")]
        graphs, notes = VGroup(), VGroup()
        for key, pos, name in specs:
            ex = d[key]
            g = ArgGraph(ex["args"], ex["attacks"], {k: v + [0] for k, v in pos.items()}, radius=0.36)
            t = label(name, font_size=23, color=BEL).next_to(g, UP, buff=0.35)
            grounded = r"\{" + r",".join(ex["grounded"]) + r"\}" if ex["grounded"] else r"\varnothing"
            pref = r",\ ".join(r"\{" + r",".join(s) + r"\}" if s else r"\varnothing" for s in ex["preferred"])
            stab = r",\ ".join(r"\{" + r",".join(s) + r"\}" for s in ex["stable"]) if ex["stable"] else r"\text{none}"
            n = VGroup(MathTex(r"\text{grounded: }" + grounded, font_size=22),
                       MathTex(r"\text{preferred: }" + pref, font_size=22),
                       MathTex(r"\text{stable: }" + stab, font_size=22)).arrange(DOWN, buff=0.12)
            n.next_to(g, DOWN, buff=0.45)
            graphs.add(VGroup(t, g))
            notes.add(n)
        legend = VGroup(*[VGroup(Circle(radius=0.12, color=c, fill_color=c, fill_opacity=0.3, stroke_width=3),
                                 label(t, font_size=20, color=c)).arrange(RIGHT, buff=0.12)
                          for c, t in ((IN_C, r"in"), (OUT_C, r"out"), (UND_C, r"undecided"))]).arrange(
            RIGHT, buff=0.6).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Three small frameworks show the semantics at work. <bookmark mark='a'/>Reinstatement: c attacks b, which "
            "attacks a. c is unattacked, so it is in; b is out; and a, defended by c, is back in. "
            "<bookmark mark='b'/>Mutual attack: a and b attack each other. The cautious grounded extension accepts "
            "neither, and leaves both undecided. The bold preferred semantics offers two answers, a or b, just like "
            "the two extensions of the Nixon diamond. <bookmark mark='c'/>An odd cycle: a attacks b, b attacks c, c "
            "attacks a. No argument can be defended, the only preferred extension is empty, and there is no stable "
            "extension at all, a paradox in miniature."
        ) as vo:
            self.play(FadeIn(head), FadeIn(legend))
            for mk, (key, _, _), g, n in zip("abc", specs, graphs, notes):
                vo.wait_until(mk)
                self.play(FadeIn(g))
                self.play(*graphs_label(g[1], d[key]["labelling"]), FadeIn(n))
        self.clear_scene()

    def trial(self):
        d = load("argue")
        head = label(r"A trial, \ argued", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pos = {"P1": [-4.8, 1.2, 0], "D1": [-2.4, 1.2, 0], "P2": [0.0, 1.2, 0], "D2": [2.4, 1.2, 0],
               "P3": [4.8, 1.2, 0], "D3": [4.8, -1.2, 0]}
        ex = d["trial"]
        g = ArgGraph(ex["args"], ex["attacks"], {k: pos[k] for k in ex["args"]}, radius=0.42, font_size=22)
        above = {"D1", "P3"}

        def tag(a, node):
            t = label(TRIAL[a], font_size=17, color=GREY_A)
            if t.width > 2.3:
                t.width = 2.3
            return t.next_to(node, UP if a in above else DOWN, buff=0.15)
        tags = VGroup(*[tag(a, g.node[a]) for a in ex["args"]])
        ex2 = d["trial, disputed"]
        g2 = ArgGraph(ex2["args"], ex2["attacks"], pos, radius=0.42, font_size=22)
        tag_d3 = tag("D3", g2.node["D3"])
        r1 = label(r"grounded: \ P3, P2, P1 in; \ D2, D1 out: \ the witness stands", font_size=23,
                   color=OK).to_edge(DOWN, buff=1.0)
        r2 = label(r"add D3, \ which P3 and D3 dispute: \ grounded is empty; \ two preferred extensions", font_size=23,
                   color=BAD).to_edge(DOWN, buff=1.0)
        r3 = label(r"a skeptical court acquits; \ a credulous one could go either way", font_size=21,
                   color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is a trial. <bookmark mark='a'/>The prosecution: a witness saw him. The defence: she was drunk. The "
            "prosecution: her blood test was clean. The defence: the test was contaminated. The prosecution: the lab's "
            "log shows no contamination. <bookmark mark='b'/>The grounded semantics labels the chain: the log is "
            "unattacked, so in; contamination out; the blood test in; drunkenness out; and the witness stands. "
            "<bookmark mark='c'/>Now the defence claims the log was altered, and the prosecution disputes that in turn: "
            "a mutual attack. The grounded extension is now empty, and there are two preferred extensions, one for "
            "each side. <bookmark mark='d'/>A skeptical court, which accepts only what every extension accepts, "
            "acquits; a credulous one could go either way. Burdens of proof decide such ties in real law."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for a in ex["args"]:
                self.play(FadeIn(g.node[a]), FadeIn(tags[ex["args"].index(a)]), run_time=0.5)
            self.play(*[GrowArrow(x) for x in g.arrows])
            vo.wait_until("b")
            self.play(*g.label_anims(ex["labelling"]), FadeIn(r1))
            vo.wait_until("c")
            self.play(FadeOut(g), FadeOut(r1), FadeIn(g2), FadeIn(tag_d3))
            self.play(*g2.label_anims(ex2["labelling"]), FadeIn(r2))
            vo.wait_until("d")
            self.play(FadeIn(r3))
        self.clear_scene()

    def uses(self):
        head = label(r"Arguments at work", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"law: \ ASPIC$^+$ \ (Prakken, \ 2010), \ Carneades: \ structured arguments, \ burdens of proof", WHITE),
            (r"medicine and policy: \ decision support that shows its reasons and their rebuttals", WHITE),
            (r"multi-agent negotiation: \ agents trade arguments, \ not just offers", WHITE),
            (r"argument mining: \ finding claims and attacks in text; \ IBM's Project Debater \ (2019)", WHITE),
            (r"large language models: \ debate between models as a check on their answers", NEW),
            (r"the same question each time: \ which arguments survive their attackers?", GOAL),
        ], font_size=23, buff=0.32, width=12.4).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Argumentation frameworks are used well beyond philosophy. <bookmark mark='a'/>In law, systems such as "
            "Henry Prakken's ASPIC plus and Carneades model structured arguments and burdens of proof. "
            "<bookmark mark='b'/>In medicine and policy, decision support that shows its reasons and the rebuttals to "
            "them. <bookmark mark='c'/>In negotiation between software agents, which trade arguments as well as offers. "
            "<bookmark mark='d'/>In argument mining, which finds claims and attacks in text; IBM's Project Debater "
            "argued against human champions in 2019. <bookmark mark='e'/>And in proposals to check large language "
            "models by having them debate. <bookmark mark='f'/>Each time the question is Dung's: which arguments "
            "survive their attackers?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()


def graphs_label(g: ArgGraph, lab: dict) -> list:
    return g.label_anims(lab)
