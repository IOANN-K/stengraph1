from pathlib import Path

import numpy as np
import pytest
from cryptography.fernet import InvalidToken
from PIL import Image

from stengraph.embedding.adaptive import embed_adaptive, extract_adaptive
from stengraph.embedding.lsb import embed_random, embed_sequential, extract_random, extract_sequential
from stengraph.estimation.rs_rate import estimate_rate
from stengraph.io.payloads import bits_to_bytes, bytes_to_bits, max_payload_bytes
from stengraph.metrics.image_quality import analyze_images
from stengraph.preprocessing.compression import compress, decompress
from stengraph.preprocessing.crypto import decrypt, encrypt, generate_key
from stengraph.steganalysis.basic import binary_entropy, lsb_statistics, pov_chi_square, spatial_lsb_statistics
from stengraph.steganalysis.rs import classify_groups, prepare_groups
from stengraph.utils.hashing import sha256_bytes


@pytest.fixture
def cover(tmp_path: Path) -> Path:
    rng = np.random.default_rng(42)
    path = tmp_path / "cover.png"
    Image.fromarray(rng.integers(0, 256, (24, 24, 3), dtype=np.uint8), mode="RGB").save(path)
    return path


def test_bits_roundtrip_and_capacity():
    data = b"stengraph\x00\xff"
    assert bits_to_bytes(bytes_to_bits(data)) == data
    assert max_payload_bytes(10, 10, 1) == 33
    assert max_payload_bytes(10, 10, 4) == 146
    with pytest.raises(ValueError): max_payload_bytes(10, 10, 0)


@pytest.mark.parametrize("depth", [1, 2, 3, 4])
def test_sequential_roundtrip_all_depths(cover, tmp_path, depth):
    output = tmp_path / f"sequential-{depth}.png"; payload = b"depth roundtrip"
    embed_sequential(cover, output, payload, depth)
    assert extract_sequential(output, depth) == payload


def test_random_roundtrip_is_deterministic_and_wrong_key_fails(cover, tmp_path):
    first, second = tmp_path / "one.png", tmp_path / "two.png"
    embed_random(cover, first, b"payload", 1, "correct")
    embed_random(cover, second, b"payload", 1, "correct")
    assert first.read_bytes() == second.read_bytes()
    assert extract_random(first, 1, "correct") == b"payload"
    with pytest.raises(ValueError): extract_random(first, 1, "wrong")


def test_adaptive_roundtrip(cover, tmp_path):
    output = tmp_path / "adaptive.png"
    embed_adaptive(cover, output, b"adaptive", 2)
    assert extract_adaptive(output, 2) == b"adaptive"


def test_payload_too_large_and_rgb_conversion(tmp_path):
    cover = tmp_path / "gray.png"; output = tmp_path / "output.png"
    Image.new("L", (4, 4), 100).save(cover)
    with pytest.raises(ValueError): embed_sequential(cover, output, b"too large", 1)


def test_image_metrics_sanity(cover):
    metrics = analyze_images(cover, cover)
    assert metrics["mse"] == 0
    assert metrics["psnr"] == float("inf")
    assert metrics["ssim"] == pytest.approx(1.0)
    assert metrics["changed_pixels"] == 0


def test_hash_compression_and_crypto_roundtrips():
    data = b"repeat " * 20
    assert sha256_bytes(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert decompress(compress(data)) == data
    key = generate_key(); token = encrypt(data, key)
    assert decrypt(token, key) == data
    with pytest.raises(InvalidToken): decrypt(token, generate_key())


def test_basic_steganalysis_small_arrays():
    channel = np.arange(16, dtype=np.uint8).reshape(4, 4)
    assert binary_entropy(0.5) == pytest.approx(1.0)
    assert lsb_statistics(channel)["lsb_one_ratio"] == pytest.approx(0.5)
    assert pov_chi_square(channel)["chi_square_normalized"] == pytest.approx(0.0)
    spatial = spatial_lsb_statistics(channel)
    assert 0 <= spatial["horizontal_lsb_agreement"] <= 1


def test_rs_classification_partition_and_interpolation():
    groups = prepare_groups(np.arange(20, dtype=np.uint8))
    classes = classify_groups(groups, [1, 0, 1, 0])
    assert sum(classes.values()) == len(groups)
    points = [(0.0, 0.4), (50.0, 0.2), (100.0, 0.0)]
    assert estimate_rate(0.3, points) == pytest.approx(25.0)
    assert estimate_rate(1.0, points) == 0.0
