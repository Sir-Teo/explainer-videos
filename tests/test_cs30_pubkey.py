import random
import unittest

from explainer.cs.algo import pubkey as P


class TestVectors(unittest.TestCase):
    def test_input_lengths_and_scalar_domains(self):
        for n in (0, 31, 33):
            with self.assertRaises(ValueError):
                P.x25519(bytes(n), bytes(32))
            with self.assertRaises(ValueError):
                P.x25519(bytes(32), bytes(n))
        for length in (-1, 8161):
            with self.assertRaises(ValueError):
                P.hkdf_expand(bytes(32), b"", length)
        self.assertEqual(P.P256.mul(-1, P.P256.G), P.P256.neg(P.P256.G))
        self.assertFalse(P.ecdsa_verify(None, b"sample", (1, 1)))
        self.assertFalse(P.ecdsa_verify((0, 0), b"sample", (1, 1)))
        with self.assertRaises(ValueError):
            P.ecdsa_sign(1, b"sample", k=0)

    def test_x25519_rfc7748(self):
        k = bytes.fromhex("a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4")
        u = bytes.fromhex("e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c")
        self.assertEqual(P.x25519(k, u).hex(), "c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552")

    def test_hkdf_rfc5869(self):
        prk = P.hkdf_extract(bytes(range(13)), b"\x0b" * 22)
        self.assertEqual(prk.hex(), "077709362c2e32df0ddc3f0dc47bba6390b6c73bb50f9c3122ec844ad7c2b3e5")
        self.assertEqual(P.hkdf_expand(prk, bytes(range(0xf0, 0xfa)), 42).hex(),
                         "3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf34007208d5b887185865")

    def test_ecdsa_rfc6979(self):
        x = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
        Q = P.P256.mul(x, P.P256.G)
        self.assertEqual(Q[0], 0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6)
        r, s = P.ecdsa_sign(x, b"sample")
        self.assertEqual(r, 0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716)
        self.assertEqual(s, 0xF7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8)
        self.assertTrue(P.ecdsa_verify(Q, b"sample", (r, s)))
        self.assertFalse(P.ecdsa_verify(Q, b"samplf", (r, s)))
        self.assertIsNone(P.P256.mul(P.P256.n, P.P256.G))


class TestNumberTheory(unittest.TestCase):
    def test_euclid_crt_primes(self):
        g, x, y = P.egcd(240, 46)
        self.assertEqual((g, 240 * x + 46 * y), (2, 2))
        self.assertEqual(P.inv_mod(17, 3120), 2753)
        self.assertEqual(P.crt([2, 3, 2], [3, 5, 7]), 23)
        self.assertEqual(P.pow_trace(3, 13, 1000)[-1][1], pow(3, 13, 1000))
        self.assertTrue(P.is_probable_prime(2 ** 127 - 1))
        self.assertFalse(P.is_probable_prime(561))          # a Carmichael number
        p = 1019
        g = P.find_generator(p)
        self.assertEqual(P.mult_order(g, p), p - 1)

    def test_dlogs(self):
        rng = random.Random(4)
        p = P.random_prime(36, rng)
        g = P.find_generator(p)
        x = rng.randrange(p - 1)
        h = pow(g, x, p)
        self.assertEqual(P.bsgs(g, h, p)[0], x)
        self.assertEqual(P.pohlig_hellman(g, h, p)[0], x)
        p2 = P.random_prime(24, rng)
        g2 = P.find_generator(p2)
        x2 = rng.randrange(p2 - 1)
        self.assertEqual(P.index_calculus(g2, pow(g2, x2, p2), p2, 50, rng)[0], x2)

    def test_factoring(self):
        rng = random.Random(5)
        a, b = P.random_prime(34, rng), P.random_prime(34, rng)
        self.assertIn(P.pollard_rho(a * b, rng)[0], (a, b))
        self.assertIn(P.quadratic_sieve(a * b)[0], (a, b))


class TestSchemes(unittest.TestCase):
    def test_puzzles_do_not_share_weak_key_checks(self):
        class SameWeakKey(random.Random):
            def randrange(self, *args):
                return 0
        result = P.merkle_puzzles(4, SameWeakKey(4), include_puzzles=True)
        self.assertTrue(result["agreed"])
        self.assertEqual(result["bob_tries"], 1)
        # Even when every weak key is identical, each public puzzle has a
        # different check; the same precomputed tag cannot unlock all of them.
        puzzles = result["puzzles"]
        self.assertEqual(len({tag for _, tag, _ in puzzles}), 4)
        self.assertEqual(len({salt for salt, _, _ in puzzles}), 4)

    def test_oaep_and_rsa_reject_noncanonical_representatives(self):
        rng = random.Random(10)
        key = P.rsa_keygen(768, rng)
        ct = P.oaep_encrypt(b"message", key, rng)
        for bad in (ct[:-1], b"\0" + ct, P.i2b(key["n"], len(ct))):
            with self.assertRaises(ValueError):
                P.oaep_decrypt(bad, key)
        for bad in (b"", bytes(65), bytes(97)):
            with self.assertRaises(ValueError):
                P.oaep_decode(bad, 96)
        for x in (-1, key["n"]):
            with self.assertRaises(ValueError):
                P.rsa_enc(x, key)
            with self.assertRaises(ValueError):
                P.rsa_dec(x, key)
        sig = P.rsa_sign(b"message", key)
        self.assertFalse(P.rsa_verify(b"message", sig + key["n"], key))
        with self.assertRaises(ValueError):
            P.pkcs1_v15_pad(b"x" * 22, 32, rng)

    def test_rsa(self):
        rng = random.Random(1)
        key = P.rsa_keygen(768, rng)
        m = 31415926535
        self.assertEqual(P.rsa_dec(P.rsa_enc(m, key), key), m)
        self.assertEqual(P.rsa_dec(P.rsa_enc(m, key), key, use_crt=False), m)
        self.assertEqual(P.oaep_decrypt(P.oaep_encrypt(b"attack at dawn", key, rng), key), b"attack at dawn")
        sig = P.rsa_sign(b"hello", key)
        self.assertTrue(P.rsa_verify(b"hello", sig, key))
        self.assertFalse(P.rsa_verify(b"hellp", sig, key))

    def test_bleichenbacher(self):
        rng = random.Random(2)
        key = P.rsa_keygen(256, rng)
        k = P.klen(key)
        em = P.pkcs1_v15_pad(b"PIN 4921", k, rng)
        c = P.rsa_enc(P.b2i(em), key)
        m, _ = P.bleichenbacher(c, key, lambda cc: P.pkcs1_v15_conforming(P.i2b(P.rsa_dec(cc, key), k)))
        self.assertEqual(P.i2b(m, k), em)

    def test_ecdsa_nonce_reuse_and_tls(self):
        rng = random.Random(3)
        d, _ = P.ec_keypair(P.P256, rng)
        k = rng.randrange(1, P.P256.n)
        s1, s2 = P.ecdsa_sign(d, b"one", k=k), P.ecdsa_sign(d, b"two", k=k)
        self.assertEqual(P.ecdsa_nonce_reuse(b"one", s1, b"two", s2), (k, d))
        t = P.tls_handshake(rng)
        for key in ("shared_equal", "tags_equal", "cert_ok", "cv_ok", "finished_ok", "plaintext_ok"):
            self.assertTrue(t[key], key)

    def test_lattices(self):
        rng = random.Random(6)
        (b1, b2), _ = P.gauss_reduce((90, 123), (56, 76))
        self.assertEqual(abs(90 * 76 - 123 * 56), abs(b1[0] * b2[1] - b1[1] * b2[0]))    # same lattice volume
        kp = P.knapsack_keygen(12, rng)
        bits = [rng.getrandbits(1) for _ in range(12)]
        self.assertEqual(P.knapsack_attack(kp["pub"], sum(b * x for b, x in zip(bits, kp["pub"]))), bits)
        f = [rng.randrange(P.MLQ) for _ in range(256)]
        g = [rng.randrange(P.MLQ) for _ in range(256)]
        self.assertEqual(P.intt(P.ntt(f)), f)
        self.assertEqual(P.intt(P.ntt_mul(P.ntt(f), P.ntt(g))), P.poly_mul_schoolbook(f, g))
        sk = P.kpke_keygen(rng)
        m = [rng.getrandbits(1) for _ in range(256)]
        self.assertEqual(P.kpke_decrypt(sk, P.kpke_encrypt(sk, m, rng))[0], m)
        s, pub = P.lwe_keygen(16, 64, 3329, rng)
        for bit in (0, 1, 1, 0):
            self.assertEqual(P.lwe_decrypt(s, P.lwe_encrypt(pub, bit, 3329, rng), 3329)[0], bit)

    def test_signatures_and_sharing(self):
        rng = random.Random(7)
        sk, pk = P.lamport_keygen(rng)
        sig = P.lamport_sign(sk, b"hi")
        self.assertTrue(P.lamport_verify(pk, b"hi", sig))
        self.assertFalse(P.lamport_verify(pk, b"ho", sig))
        grp = P.schnorr_group(rng, qbits=64, pbits=192)
        x = rng.randrange(grp[1])
        y = pow(grp[2], x, grp[0])
        self.assertTrue(P.schnorr_verify(y, b"m", P.schnorr_sign(x, b"m", grp, rng), grp))
        p = 2 ** 127 - 1
        shares, _ = P.shamir_split(424242, 3, 5, p, rng)
        self.assertEqual(P.shamir_combine(shares[:3], p), 424242)
        self.assertEqual(P.shamir_combine([shares[0], shares[2], shares[4]], p), 424242)
        self.assertNotEqual(P.shamir_combine(shares[:2], p), 424242)


if __name__ == "__main__":
    unittest.main()
