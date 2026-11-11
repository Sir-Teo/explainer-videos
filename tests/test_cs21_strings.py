"""Part 21's instruments against brute force."""

from __future__ import annotations

import itertools
import random
import unittest
import zlib

import numpy as np

from explainer.cs.algo import strings as S


def brute(text, pat):
    return [i for i in range(len(text) - len(pat) + 1) if text[i:i + len(pat)] == pat]


class Strings(unittest.TestCase):
    def setUp(self):
        rng = random.Random(21)
        self.texts = [bytes(rng.choice(b"ab") for _ in range(300)), bytes(rng.choice(b"acgt") for _ in range(500)),
                      b"abracadabra" * 20, b"a" * 200 + b"b"]
        self.pats = [b"ab", b"aab", b"abab", b"acg", b"abra", b"cadabra", b"a" * 10 + b"b", b"a" * 5, b"tttt"]

    def test_matchers(self):
        for t in self.texts:
            for p in self.pats:
                want = brute(t, p)
                self.assertEqual(S.naive(t, p)[0], want)
                self.assertEqual(S.naive_fast(t, p), S.naive(t, p))
                self.assertEqual(S.rabin_karp(t, p)[0], want)
                self.assertEqual(S.rabin_karp(t, p, mod=97)[0], want)        # spurious hits are filtered
                self.assertEqual(S.kmp(t, p)[0], want)
                self.assertLessEqual(S.kmp(t, p)[1], 2 * len(t))
                self.assertEqual(S.horspool(t, p)[0], want)
                self.assertEqual(S.boyer_moore(t, p)[0], want)

    def test_automaton(self):
        pat = b"abab"
        d = S.kmp_automaton(pat, b"ab")
        q, hits = 0, []
        for i, c in enumerate(b"abababbabab"):
            q = d[q][c]
            if q == len(pat):
                hits.append(i - 3)
        self.assertEqual(hits, brute(b"abababbabab", pat))

    def test_aho_corasick(self):
        pats = [b"he", b"she", b"his", b"hers", b"a", b"abra"]
        ac = S.AhoCorasick(pats)
        for t in self.texts + [b"ushers and his abra"]:
            hits, _ = ac.search(t)
            for p in pats:
                self.assertEqual(hits[p], len(brute(t, p)))

    def test_suffix_array_lcp_search(self):
        for t in self.texts + [b"banana$", b"mississippi\x00"]:
            sa = S.suffix_array(t)
            self.assertEqual(sa.tolist(), S.suffix_array_naive(t))
            lcp = S.lcp_kasai(t, sa)
            for i in range(1, len(t)):
                a, b = t[sa[i - 1]:], t[sa[i]:]
                k = 0
                while k < min(len(a), len(b)) and a[k] == b[k]:
                    k += 1
                self.assertEqual(lcp[i], k)
            for p in self.pats:
                lo, hi, _ = S.sa_search(t, sa, p)
                self.assertEqual(sorted(sa[lo:hi].tolist()), brute(t, p))

    def test_bwt_fm(self):
        rng = random.Random(3)
        for t in [b"banana\x00", b"abracadabra\x00", bytes(rng.choice(b"acgt") for _ in range(2000)) + b"\x00"]:
            sa = S.suffix_array(t)
            L = S.bwt_from_sa(t, sa)
            self.assertEqual(S.inverse_bwt(L), t)
            fm = S.FMIndex(t, sa, step=16, sa_step=8)
            for p in (b"a", b"an", b"ana", b"abra", b"acg", b"gtac", b"zz"):
                cnt, (lo, hi) = fm.count(p)
                self.assertEqual(cnt, len(brute(t, p)))
                self.assertEqual(sorted(fm.locate(r) for r in range(lo, hi)), brute(t, p))
        self.assertEqual(S.bwt_from_sa(b"banana\x00", S.suffix_array(b"banana\x00")), b"annb\x00aa")

    def test_compression(self):
        data = (b"it was the best of times, it was the worst of times, " * 30) + bytes(range(256))
        tok = S.lz77(data)
        self.assertEqual(S.lz77_decode(tok), data)
        sz = S.deflate_size(tok)
        self.assertLess(sz["bytes"], len(zlib.compress(data, 9)) * 1.6)
        codes, nd = S.lzw(data)
        self.assertEqual(nd, 256 + len(codes) - 1)
        r = S.RANS(data)
        enc = r.encode(data)
        self.assertEqual(r.decode(enc, len(data)), data)
        self.assertLess(len(enc) * 8, S.rans_size(data) * 1.05 + 64)
        mtf = S.move_to_front(b"aaabbbaaa")
        self.assertEqual(mtf.tolist(), [97, 0, 0, 98, 0, 0, 1, 0, 0])

    def test_alignment_and_diff(self):
        S_ = S.needleman_wunsch("GATTACA", "GCATGCU")
        self.assertEqual(S_[-1, -1], 0)
        best, end, start, _ = S.smith_waterman("xxxACGTACGTyyy", "zzACGTACGTzz")
        self.assertEqual(best, 16)
        rng = random.Random(9)
        for _ in range(40):
            a = [rng.choice("abc") for _ in range(rng.randint(0, 25))]
            b = [rng.choice("abc") for _ in range(rng.randint(0, 25))]
            D, ops, _, _ = S.myers(a, b)
            self.assertEqual(D, len(a) + len(b) - 2 * S.lcs_len(a, b))
            self.assertEqual([x for o, x in ops if o != "+"], a)
            self.assertEqual([x for o, x in ops if o != "-"], b)
            self.assertEqual(sum(o != "=" for o, _ in ops), D)
        anchors = S.patience_anchors(list("abcdxe"), list("xabcde"))
        self.assertTrue(all(a < b for (a, _), (b, _) in zip(anchors, anchors[1:])))

    def test_rolling_and_chunks(self):
        rng = np.random.default_rng(1)
        data = rng.integers(0, 256, 5000, dtype=np.uint8).tobytes()
        w = S.adler32_rolling(data, 64)
        for k in (0, 17, 4000):
            blk = data[k:k + 64]
            a = sum(blk) % 65536
            b = sum((64 - i) * x for i, x in enumerate(blk)) % 65536
            self.assertEqual(int(w[k]), (b << 16) | a)
        big = rng.integers(0, 256, 400_000, dtype=np.uint8).tobytes()
        cuts = S.cdc_chunks(big)
        edited = big[:200_000] + b"INSERTED" + big[200_000:]
        cuts2 = S.cdc_chunks(edited)
        h1, h2 = set(S.chunk_hashes(big, cuts)), set(S.chunk_hashes(edited, cuts2))
        self.assertGreaterEqual(len(h1 & h2), len(h1) - 3)

    def test_periodicity(self):
        self.assertEqual(S.manacher(b"xabacabay"), (1, 7))
        self.assertEqual(S.periods(b"abaababaab")[:3], [5, 8, 10])
        self.assertEqual(S.duval("banana"), ["b", "an", "an", "a"])
        f = S.duval("abracadabra")
        self.assertEqual("".join(f), "abracadabra")
        self.assertTrue(all(f[i] >= f[i + 1] for i in range(len(f) - 1)))




def all_words(alphabet,length):
 for n in range(length+1):
  for t in itertools.product(alphabet,repeat=n):yield bytes(t)

def positions(t,p):return [i for i in range(len(t)-len(p)+1) if t[i:i+len(p)]==p]

class Regressions(unittest.TestCase):
 def test_exhaustive_matchers_and_counts(self):
  pats=list(all_words(b'ab',4))
  for text in all_words(b'ab',6):
   for pat in pats:
    expected=positions(text,pat);self.assertEqual(S.naive_fast(text,pat),S.naive(text,pat))
    for fn in [S.naive,S.rabin_karp,S.kmp,S.horspool,S.boyer_moore]:self.assertEqual(fn(text,pat)[0],expected,(fn.__name__,text,pat))
    self.assertLessEqual(S.kmp(text,pat)[1],2*len(text))
 def test_suffixes_and_lcp_exhaustive(self):
  for text in all_words(b'ab',7):
   sa=S.suffix_array(text);self.assertEqual(sa.tolist(),sorted(range(len(text)),key=lambda i:text[i:]))
   lcp=S.lcp_kasai(text,sa)
   for k in range(1,len(text)):
    a,b=text[sa[k-1]:],text[sa[k]:];n=0
    while n<min(len(a),len(b)) and a[n]==b[n]:n+=1
    self.assertEqual(lcp[k],n)
 def test_suffix_validation_all_permutations(self):
  text=b'aaba\0';correct=S.suffix_array(text).tolist()
  for perm in itertools.permutations(range(len(text))):
   if list(perm)==correct:S.bwt_from_sa(text,perm)
   else:
    with self.assertRaises(ValueError):S.bwt_from_sa(text,perm)
  for sa in [[0]*5,[-1,0,1,2,3],[0,1,2,3,8],[0.,1.,2.,3.,4.]]:
   with self.assertRaises(ValueError):S.lcp_kasai(text,sa)
 def test_fm_full_rank_and_locate(self):
  for body in all_words(b'ab',6):
   text=body+b'\0';sa=S.suffix_array(text);fm=S.FMIndex(text,sa,step=3,sa_step=4);L=S.bwt_from_sa(text,sa)
   self.assertEqual(S.inverse_bwt(L),text)
   for c in [0,97,98,255]:
    for k in range(len(text)+1):self.assertEqual(fm.rank(c,k),L[:k].count(c))
   self.assertEqual([fm.locate(i) for i in range(len(text))],sa.tolist())
   for pat in all_words(b'ab',3):
    n,(a,b)=fm.count(pat);expected=positions(body,pat);self.assertEqual(n,len(expected));self.assertEqual(sorted(fm.locate(i) for i in range(a,b)),expected)
   for pat in [b'\0',b'\0a',b'a\0']:
    with self.assertRaises(ValueError):fm.count(pat)
 def test_sentinel_and_domains(self):
  for text in [b'',b'aba',b'a\0a\0',b'\0a']:
   with self.assertRaises(ValueError):S.bwt_from_sa(text,list(range(len(text))))
  for L in [b'',b'aba',b'a\0a\0']:
   with self.assertRaises(ValueError):S.inverse_bwt(L)
  fm=S.FMIndex(b'ab\0',S.suffix_array(b'ab\0'))
  for row in [-1,3,1.2,True]:
   with self.assertRaises(ValueError):fm.locate(row)
  with self.assertRaises(ValueError):fm.rank(97,4)
  with self.assertRaises(ValueError):S.FMIndex(b'a\0',[1,0],0)
  with self.assertRaises(ValueError):S.AhoCorasick([b''])
 def test_manacher_all_sentinel_bytes(self):
  for text in all_words(b'$^#a',6):
   start,length=S.manacher(text);best=max((j-i for i in range(len(text)+1) for j in range(i,len(text)+1) if text[i:j]==text[i:j][::-1]),default=0)
   self.assertEqual(length,best,text);self.assertEqual(text[start:start+length],text[start:start+length][::-1])
 def test_rans_roundtrips_and_invalid_inputs(self):
  rng=random.Random(21)
  for data in [b'a',b'a'*100,bytes(range(256)),bytes(range(256))*4,bytes(rng.randrange(8) for _ in range(10000))]:
   model=S.RANS(data)
   self.assertEqual(sum(model.f),model.M);self.assertTrue(all(model.f[c]>0 for c in data))
   for payload in [data,data[:3],data[::-1],b'']:
    enc=model.encode(payload);self.assertEqual(model.decode(enc,len(payload)),payload)
    # A unary model emits no per-symbol information; output length is external metadata.
    if len(set(data)) > 1:
     with self.assertRaises(ValueError):model.decode(enc,len(payload)+1)
    with self.assertRaises(ValueError):model.decode(enc+b'X',len(payload))
   with self.assertRaises(ValueError):model.decode(b'',1)
  with self.assertRaises(ValueError):S.RANS(b'')
  with self.assertRaises(ValueError):S.RANS(b'abc',1)
  with self.assertRaises(ValueError):S.RANS(b'a').encode(b'b')
  for bits in [0,17,1.2,True]:
   with self.assertRaises(ValueError):S.RANS(b'a',bits)
 def test_compression_and_chunk_domains(self):
  for text in all_words(b'ab',7):self.assertEqual(S.lz77_decode(S.lz77(text)),text)
  for tokens in [[(2,1)],[97,(3,2)],[97,(0,1)]]:
   with self.assertRaises(ValueError):S.lz77_decode(tokens)
  for tokens in [[(2,1)],[(259,1)],[(3,0)],[(3,32769)]]:
   with self.assertRaises(ValueError):S.deflate_size(tokens)
  for block in [0,-1,1.2]:
   with self.assertRaises(ValueError):S.adler32_rolling(b'ab',block)
  self.assertEqual(len(S.adler32_rolling(b'ab',3)),0)
  for kw in [dict(mask_bits=0),dict(mask_bits=33),dict(min_size=0),dict(min_size=10,max_size=2)]:
   with self.assertRaises(ValueError):S.cdc_chunks(b'ab',**kw)
  for cuts in [[0,2],[2,1],[1],[3]]:
   with self.assertRaises(ValueError):S.chunk_hashes(b'ab',cuts)
  self.assertEqual(S.periods(b''),[]);self.assertEqual(S.entropy([]),0)
  with self.assertRaises(ValueError):S.entropy([-1])
 def test_unicode_suffix_tree(self):
  edges,_=S.suffix_tree_edges('éé$');self.assertEqual(len([e for e in edges if e[3] is not None]),3)

class MeasurementReferences(unittest.TestCase):
    def test_exact_finite_prefix_comparisons(self):
        from videos.cs.cs21.measurement_references import naive_comparisons_reference
        for text in all_words(b"ab", 5):
            for pat in all_words(b"ab", 3):
                self.assertEqual(naive_comparisons_reference(text,pat),S.naive(text,pat)[1])
        self.assertEqual(naive_comparisons_reference(b"aaaa",b"aa"),6)

    def test_repeat_residual_and_complete_order(self):
        from videos.cs.cs21.measurement_references import check_suffix_order,longest_repeat_reference
        for text in [b"aaaaabaaaaac",b"banana",b"abcabca",b"abababa"]:
            indexed=text+b"\0";sa=S.suffix_array(indexed);check_suffix_order(indexed,sa)
            length,at=longest_repeat_reference(indexed,sa)
            best=max((k for i in range(len(text)) for j in range(i+1,len(text)) for k in range(1,len(text)-j+1) if text[i:i+k]==text[j:j+k]),default=0)
            self.assertEqual(length,best)
            self.assertEqual(indexed[at[0]:at[0]+length],indexed[at[1]:at[1]+length])
        with self.assertRaises(AssertionError):check_suffix_order(b"ba\0",[0,1,2])

    def test_decoders_and_exact_reuse(self):
        from videos.cs.cs21.measurement_references import exact_chunk_reuse,lzw_decode_reference,huffman_cost_reference
        from collections import Counter
        for text in all_words(b"ab",6):
            codes,_=S.lzw(text);self.assertEqual(lzw_decode_reference(codes),text)
            frequencies=Counter(text)
            self.assertEqual(huffman_cost_reference(frequencies),sum(n*S.huffman_lengths(frequencies)[c] for c,n in frequencies.items()))
        self.assertEqual(exact_chunk_reuse(b"abcd",[2,4],b"abXYcd",[2,4,6]),[1])

    def test_alignment_and_border_references(self):
        from videos.cs.cs21.measurement_references import alignment_reference,border_reference
        for a in ["", "a", "aba", "aaa", "INTENTION"]:
            self.assertEqual(border_reference(a.encode()),S.kmp_failure(a.encode()))
            for b in ["", "b", "aab", "EXECUTION"]:
                self.assertEqual(alignment_reference(a,b),S.needleman_wunsch(a,b).tolist())
                self.assertEqual(alignment_reference(a,b,local=True),S.smith_waterman(a,b)[3].tolist())


class StreamingHorspool(unittest.TestCase):
    def test_stream_chunks_and_overlapping_matches(self):
        from videos.cs.cs21.stream_horspool import search
        for text in all_words(b"ab", 6):
            for pat in all_words(b"ab", 3):
                expected = brute(text, pat)
                for width in [1, 2, 5]:
                    chunks = [text[i:i+width] for i in range(0, len(text), width)]
                    positions, reads, comparisons = search(iter(chunks), pat)
                    self.assertEqual(positions, expected)
                    self.assertEqual(reads, len(text))
                    self.assertEqual(comparisons, S.horspool(text, pat)[1])


if __name__ == "__main__":
    unittest.main()
