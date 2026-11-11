import hashlib
import hmac
import random
import unittest

from explainer.cs.algo import crypto as K


class TestVectors(unittest.TestCase):
    def test_block_and_nonce_contracts(self):
        aes = K.AES(bytes(16))
        for n in (0, 15, 17, 24, 32):
            with self.assertRaises(ValueError):
                K.AES(bytes(n))
        for n in (0, 15, 17):
            with self.assertRaises(ValueError):
                aes.enc(bytes(n))
            with self.assertRaises(ValueError):
                aes.dec(bytes(n))
        for operation in (K.cbc_encrypt, K.cbc_decrypt):
            with self.assertRaises(ValueError):
                operation(aes, bytes(15), bytes(16))
            with self.assertRaises(ValueError):
                operation(aes, bytes(16), bytes(17))
        with self.assertRaises(ValueError):
            K.aes_gcm_encrypt(bytes(16), bytes(16), b"message")
        with self.assertRaises(ValueError):
            K.ctr_encrypt(aes, bytes(7), b"message")

    def test_chacha_counter_boundary(self):
        key, nonce = bytes(32), bytes(12)
        self.assertEqual(K.chacha20_encrypt(key, 2 ** 32 - 1, nonce, bytes(64)),
                         K.chacha20_block(key, 2 ** 32 - 1, nonce))
        with self.assertRaises(ValueError):
            K.chacha20_encrypt(key, 2 ** 32 - 1, nonce, bytes(65))
        with self.assertRaises(ValueError):
            K.chacha20_block(key, -1, nonce)

    def test_padding_roundtrips_and_rejects_malformed_lengths(self):
        for block_size in (8, 16):
            for length in (0, 1, 7, 8, 15, 16, 17, 32):
                data = bytes(length)
                self.assertEqual(K.pkcs7_unpad(K.pkcs7_pad(data, block_size), block_size), data)
        for data in (b"", b"\x01", b"x" * 15 + b"\x00", b"x" * 15 + b"\x02"):
            with self.assertRaises(ValueError):
                K.pkcs7_unpad(data)

    def test_aes_fips197(self):
        k = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
        aes = K.AES(k)
        self.assertEqual(aes.enc(bytes.fromhex("00112233445566778899aabbccddeeff")).hex(),
                         "69c4e0d86a7b0430d8cdb78070b4c55a")
        self.assertEqual(K.AES(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))
                         .enc(bytes.fromhex("3243f6a8885a308d313198a2e0370734")).hex(),
                         "3925841d02dc09fbdc118597196a0b32")
        self.assertEqual(aes.dec(aes.enc(b"0123456789abcdef")), b"0123456789abcdef")
        self.assertEqual(K.SBOX[0x53], 0xED)          # FIPS-197 section 5.1.1

    def test_chacha20_rfc8439(self):
        self.assertEqual(K.quarter_round(0x11111111, 0x01020304, 0x9B8D6F43, 0x01234567),
                         (0xEA2A92F4, 0xCB1CF8CE, 0x4581472E, 0x5881C4BB))
        blk = K.chacha20_block(bytes(range(32)), 1, bytes.fromhex("000000090000004a00000000"))
        self.assertEqual(blk[:16].hex(), "10f1e7e4d13b5915500fdd1fa32071c4")

    def test_gcm_nist(self):
        self.assertEqual(K.aes_gcm_encrypt(bytes(16), bytes(12), b"")[1].hex(), "58e2fccefa7e3061367f1d57a4e7455a")
        ct, tag = K.aes_gcm_encrypt(bytes(16), bytes(12), bytes(16))
        self.assertEqual(ct.hex(), "0388dace60b6a392f328c2b971b2fe78")
        self.assertEqual(tag.hex(), "ab6e47d42cec13bdf53a67b21257bddf")

    def test_hashes_against_hashlib(self):
        for m in (b"", b"abc", b"x" * 64, b"y" * 200):
            self.assertEqual(K.sha256(m), hashlib.sha256(m).digest())
            self.assertEqual(K.sha3_256(m), hashlib.sha3_256(m).digest())
            self.assertEqual(K.hmac_sha256(b"key", m), hmac.new(b"key", m, hashlib.sha256).digest())

    def test_enigma(self):
        self.assertEqual(K.Enigma().encrypt("AAAAA"), "BDZGO")
        e1, e2 = K.Enigma(positions="QEV"), K.Enigma(positions="QEV")
        self.assertEqual(e2.encrypt(e1.encrypt("ENIGMAREVEALED")), "ENIGMAREVEALED")   # an involution
        a, _ = K.rejewski_characteristic(("I", "II", "III"), "ABC", "")
        b, _ = K.rejewski_characteristic(("I", "II", "III"), "ABC", "AZ BY CX DW")
        self.assertEqual(a, b)                          # the plugboard cannot change the cycle structure


class TestAttacks(unittest.TestCase):
    def test_length_extension(self):
        secret, msg = b"supersecretkey!", b"user=alice&role=user"
        mac = hashlib.sha256(secret + msg).digest()
        new, forged = K.length_extension(mac, len(secret), msg, b"&role=admin")
        self.assertEqual(forged, hashlib.sha256(secret + new).digest())

    def test_padding_oracle(self):
        aes = K.AES(bytes(range(16)))
        iv = bytes(16)
        pt = K.pkcs7_pad(b"Attack at dawn!")
        c = K.cbc_encrypt(aes, iv, pt)

        def oracle(ivx, blk):
            try:
                K.pkcs7_unpad(K.cbc_decrypt(aes, ivx, blk))
                return True
            except ValueError:
                return False
        self.assertEqual(K.padding_oracle_attack(iv, c, oracle)[0], pt)

    def test_lfsr_and_bm(self):
        s = K.lfsr([2, 5], [1, 0, 1, 1, 0], 60)
        L, C = K.berlekamp_massey_gf2(s[:10])
        self.assertEqual(L, 5)
        self.assertEqual(K.lfsr_from_connection(C, s, 60), s)

    def test_spn(self):
        rng = random.Random(3)
        keys = [rng.randrange(1 << 16) for _ in range(5)]
        counts = K.spn_differential_attack(keys, 4000, rng)
        self.assertEqual(max(counts, key=counts.get), keys[4] & 0x0F0F)
        self.assertEqual(K.toy_decrypt(K.toy_cipher(4321, 999), 999), 4321)

    def test_classical(self):
        text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG " * 3
        self.assertEqual(K.vigenere(K.vigenere(text, "KEY"), "KEY", decrypt=True), K.letters(text))
        self.assertEqual(K.caesar(K.caesar("HELLO", 3), 23), "HELLO")
        root, levels = K.merkle_root([b"a", b"b", b"c", b"d", b"e"])
        self.assertTrue(K.merkle_verify(root, b"c", K.merkle_proof(levels, 2)))
        self.assertTrue(K.constant_time_equal(b"abc", b"abc"))
        self.assertFalse(K.early_exit_equal(b"abc", b"abd"))


if __name__ == "__main__":
    unittest.main()
