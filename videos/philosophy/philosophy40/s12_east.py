from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class East(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Proofs, \ poems and Cook Ding", r"Can a proof, \ a poem or a skill be beautiful?", lit=(1940, 1908), part=PART)
        with self.voiceover("Chapter eleven. Proofs, poems and Cook Ding."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.maths()
        self.proofs()
        self.xiehe()
        self.music()
        self.dao()
        self.modern()

    def maths(self):
        head = history_card(1940, r"G. H. Hardy", r"\textit{A Mathematician's Apology}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"Hardy \ (1940)", r"\textit{A Mathematician's Apology}: \ `there is no permanent place in the world for ugly mathematics'", FORM),
                (r"what makes it beautiful", r"surprise, \ inevitability and economy: \ Euclid's infinitude of primes, \ $\sqrt2$ irrational", SYM),
                (r"Erdős's Book", r"God keeps a book of the perfect proofs \ (Aigner and Ziegler, \ \textit{Proofs from THE BOOK})", TASTE),
                (r"Zeki et al. \ (2014)", r"mathematicians rated Euler's identity most beautiful; \ the same brain region responded as to beauty in art", ART)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Mathematicians speak of beauty constantly. <bookmark mark='a'/>G. H. Hardy's A Mathematician's Apology, "
            "of 1940, said that there is no permanent place in the world for ugly mathematics. <bookmark mark='b'/>He "
            "found beauty in surprise, inevitability and economy, as in Euclid's proof that there are infinitely many "
            "primes, and the proof that the square root of two is irrational. <bookmark mark='c'/>Paul Erdős spoke of "
            "a Book in which God keeps the perfect proofs; Martin Aigner and Günter Ziegler collected candidates in "
            "Proofs from THE BOOK. <bookmark mark='d'/>And Semir Zeki and colleagues found in 2014 that when "
            "mathematicians viewed formulas they rated beautiful, with Euler's identity rated highest, the same "
            "region of the brain responded as when people experience beauty in art or music."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def xiehe(self):
        head = label(r"Chinese aesthetics: \ painting and poetry", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Xie He \ (6th c.)", r"six principles of painting; \ the first: \ \textit{qiyun shengdong}, \ spirit resonance and life-motion", EAST),
                (r"the others", r"bone method in the brush; \ fidelity to the object; \ colour; \ composition; \ copying the masters", TASTE),
                (r"\textit{yijing}", r"the realm of a poem or painting: \ scene and feeling fused, \ meaning beyond the words", FORM),
                (r"Wang Guowei \ (1908)", r"\textit{Renjian cihua}: \ the highest poetry has \textit{jingjie}, \ a world of its own", ART)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Chinese aesthetics developed its own vocabulary. <bookmark mark='a'/>Xie He, in the sixth century, set "
            "out six principles of painting. The first, spirit resonance and life-motion, asks that a painting carry "
            "the living energy of its subject. <bookmark mark='b'/>The others concern the bone method of the brush, "
            "fidelity to the object, colour, composition, and copying the masters. <bookmark mark='c'/>Later "
            "criticism prized the yijing of a poem or painting, its realm, in which scene and feeling fuse and "
            "meaning lies beyond the words. <bookmark mark='d'/>Wang Guowei's Remarks on Song Lyrics, of 1908, made "
            "jingjie, a world of its own, the mark of the highest poetry, bringing Kant and Schopenhauer into "
            "conversation with the Chinese tradition."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def dao(self):
        head = label(r"Cook Ding \ (\textit{Zhuangzi})", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the story", r"Cook Ding carves an ox for Lord Wenhui; \ every movement in rhythm, \ like a dance", EAST),
                (r"the method", r"`I follow the natural pattern': \ his blade, \ nineteen years old, \ is as sharp as new", SYM),
                (r"skill as beauty", r"beauty in effortless mastery, \ attuned to the way of things", TASTE),
                (r"today", r"Csíkszentmihályi's `flow' \ (1990); \ Li Zehou, \ \textit{The Path of Beauty} \ (1981)", FORM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The Zhuangzi offers a different picture of beauty, in action. <bookmark mark='a'/>Cook Ding carves an ox "
            "for Lord Wenhui, and every movement falls into rhythm, like a dance to ancient music. <bookmark "
            "mark='b'/>Asked how, he says he no longer sees the ox with his eyes; he follows its natural pattern, "
            "sliding his blade through the hollows, and after nineteen years it is as sharp as if new from the "
            "whetstone. <bookmark mark='c'/>Beauty here is effortless mastery, attuned to the way of things. "
            "<bookmark mark='d'/>Modern echoes include Mihály Csíkszentmihályi's flow, of 1990, and Li Zehou's The "
            "Path of Beauty, of 1981, a history of Chinese aesthetic sensibility."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def music(self):
        head = label(r"Music and ritual", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Confucius", r"heard the Shao music in Qi, \ and for three months did not notice the taste of meat", EAST),
                (r"Xunzi", r"`Discourse on Music': \ music shapes feeling, \ and binds people in harmony", TASTE),
                (r"Ji Kang \ (3rd c.)", r"`music has in it neither grief nor joy': \ the feelings are in the listener", FORM),
                (r"wabi-sabi", r"Japanese: \ beauty in the imperfect, \ impermanent and incomplete", ART)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "In the Chinese tradition, music was ethics. <bookmark mark='a'/>Confucius, the Analects say, heard the "
            "Shao music in the state of Qi, and for three months did not notice the taste of meat. <bookmark "
            "mark='b'/>Xunzi's Discourse on Music held that music shapes feeling and binds people in harmony, as "
            "ritual orders them. <bookmark mark='c'/>Against this, Ji Kang argued in the third century that music has "
            "in it neither grief nor joy: the feelings are the listener's, Hume's view fourteen centuries early. "
            "<bookmark mark='d'/>And the Japanese aesthetic of wabi-sabi finds beauty in the imperfect, impermanent "
            "and incomplete, a long way from the symmetry groups."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def proofs(self):
        head = label(r"Two proofs Hardy admired", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        e1 = VGroup(label(r"Euclid: \ there are infinitely many primes", font_size=22, color=FORM),
                    MathTex(r"\text{suppose } p_1, \dots, p_n \text{ are all the primes; \ let } N = p_1 p_2 \cdots p_n + 1",
                            font_size=28),
                    MathTex(r"\text{no } p_i \text{ divides } N, \text{ so } N \text{ has a prime factor not on the list}",
                            font_size=28)).arrange(DOWN, buff=0.2).move_to([0, 1.6, 0])
        e2 = VGroup(label(r"$\sqrt2$ is irrational", font_size=22, color=FORM),
                    MathTex(r"\sqrt2 = \tfrac{a}{b} \text{ in lowest terms} \;\Rightarrow\; a^2 = 2b^2 \;\Rightarrow\; "
                            r"a = 2c", font_size=28),
                    MathTex(r"\Rightarrow\; 4c^2 = 2b^2 \;\Rightarrow\; b^2 = 2c^2 \;\Rightarrow\; b \text{ even: "
                            r"not lowest terms}", font_size=28)).arrange(DOWN, buff=0.2).move_to([0, -1.0, 0])
        foot = label(r"`a mathematician, \ like a painter or a poet, \ is a maker of patterns' \ --- \ Hardy",
                     font_size=21, color=TASTE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Hardy's two favourite examples can be shown in full. <bookmark mark='a'/>Euclid's: suppose there were "
            "only finitely many primes. Multiply them all together and add one. That number leaves remainder one when "
            "divided by every prime on the list, so its prime factors are not on the list. The list was never "
            "complete. <bookmark mark='b'/>The Pythagoreans': if the square root of two were a fraction in lowest "
            "terms, a over b, then a squared would be twice b squared, so a is even, so b squared is twice a square, "
            "so b is even too, and the fraction was not in lowest terms after all. <bookmark mark='c'/>Each is short, "
            "surprising and inevitable, and neither has dated in more than two thousand years. A mathematician, Hardy "
            "wrote, like a painter or a poet, is a maker of patterns."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(e1[0]), Write(e1[1]))
            self.play(Write(e1[2]))
            vo.wait_until("b")
            self.play(FadeIn(e2[0]), Write(e2[1]))
            self.play(Write(e2[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def modern(self):
        head = label(r"Modern Chinese aesthetics", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Cai Yuanpei \ (1917)", r"`replace religion with aesthetic education': \ beauty as moral formation", EAST),
                (r"Zhu Guangqian", r"psychological aesthetics; \ translated Hegel's \textit{Aesthetics} into Chinese", TASTE),
                (r"Zong Baihua", r"the rhythm of space in Chinese painting: \ emptiness as part of the form", FORM),
                (r"Li Zehou", r"`sedimentation': \ the forms we find beautiful carry the history of human practice", SYM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Modern Chinese aesthetics joined these traditions. <bookmark mark='a'/>Cai Yuanpei, president of Peking "
            "University, argued in 1917 that aesthetic education should replace religion as a source of moral "
            "formation. <bookmark mark='b'/>Zhu Guangqian wrote a psychology of aesthetics and translated Hegel's "
            "lectures on aesthetics into Chinese. <bookmark mark='c'/>Zong Baihua wrote on the rhythm of space in "
            "Chinese painting, where empty paper is part of the form. <bookmark mark='d'/>And Li Zehou proposed that "
            "the forms we find beautiful carry, sedimented in them, the history of human practice."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
