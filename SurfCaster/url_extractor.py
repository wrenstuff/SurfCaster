from urllib.parse import urlparse
import re
import math
from tlds import tld_set
import torch

url_shortners = 'url-shortners.txt'

SUSPICIOUS_WORDS = [
    "login", "signin", "verify", "account", "secure", "update", "bank", "confirm", "password", "billing", "paypal", "wallet", "free", "bonus", "gift", "prize", "urgent"
]

SUSPICIOUS_TLDS = [
    "zip", "review", "country", "kim", "cricket", "science", "work", "party", "gq", "tk", "ml", "ga", "cf"
]

FEATURE_ORDER = [
    "length_url",
    "length_hostname",
    "ip",
    "nb_dots",
    "nb_hyphens",
    "nb_at",
    "nb_qm",
    "nb_and",
    "nb_or",
    "nb_eq",
    "nb_underscore",
    "nb_tilde",
    "nb_percent",
    "nb_slash",
    "nb_star",
    "nb_colon",
    "nb_comma",
    "nb_semicolumn",
    "nb_dollar",
    "nb_space",
    "nb_www",
    "nb_com",
    "nb_dslash",
    "http_in_path",
    "https_token",
    "ratio_digits_url",
    "ratio_digits_host",
    "punycode",
    "port",
    "tld_in_path",
    "tld_in_subdomain",
    "abnormal_subdomain",
    "nb_subdomains",
    "prefix_suffix",
    "random_domain",
    "shortening_service",
    "path_extension",
    "length_words_raw",
    "char_repeat",
    "shortest_words_raw",
    "shortest_word_host",
    "shortest_word_path",
    "longest_words_raw",
    "longest_word_host",
    "longest_word_path",
    "avg_words_raw",
    "avg_word_host",
    "avg_word_path",
    "phish_hints",
    "suspicious_tld"

]

def has_ip_address(hostname):
    if not hostname:
        return 0
    
    ipv4_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    return int(bool(re.match(ipv4_pattern, hostname)))

def count_char_repeats(text):
    return len(re.findall(r"(.)\1{2,}", text))

def get_words(text):
    return [word for word in re.split(r"[^A-Za-z0-9]+", text) if word]

def safe_min(values):
    return min(values) if values else 0

def safe_max(values):
    return max(values) if values else 0

def safe_avg(values):
    return sum(values) / len(values) if values else 0

def entropy(text):
    if not text:
        return 0

    probabilities = [text.count(char) / len(text) for char in set(text)]
    return -sum(p * math.log2(p) for p in probabilities)

def extract_url_features(url):
    parsed = urlparse(url)

    hostname = parsed.hostname or ""
    hostname = hostname.lower()

    path = parsed.path or ""
    query = parsed.query or ""
    full_url = url.lower()

    domain_parts = hostname.split(".") if hostname else []
    tld = domain_parts[-1] if len(domain_parts) > 1 else ""
    subdomain = ".".join(domain_parts[:-2]) if len(domain_parts) > 2 else ""

    raw_words = get_words(full_url)
    host_words = get_words(hostname)
    path_words = get_words(path)

    raw_word_lengths = [len(w) for w in raw_words]
    host_word_lengths = [len(w) for w in host_words]
    path_word_lengths = [len(w) for w in path_words]

    digits_url = sum(c.isdigit() for c in full_url)
    digits_host = sum(c.isdigit() for c in hostname)

    features = {
        "length_url": len(url),
        "length_hostname": len(hostname),

        "ip": has_ip_address(hostname),

        "nb_dots": full_url.count("."),
        "nb_hyphens": full_url.count("-"),
        "nb_at": full_url.count("@"),
        "nb_qm": full_url.count("?"),
        "nb_and": full_url.count("&"),
        "nb_or": full_url.count("|"),
        "nb_eq": full_url.count("="),
        "nb_underscore": full_url.count("_"),
        "nb_tilde": full_url.count("~"),
        "nb_percent": full_url.count("%"),
        "nb_slash": full_url.count("/"),
        "nb_star": full_url.count("*"),
        "nb_colon": full_url.count(":"),
        "nb_comma": full_url.count(","),
        "nb_semicolumn": full_url.count(";"),
        "nb_dollar": full_url.count("$"),
        "nb_space": full_url.count(" ") + full_url.count("%20"),

        "nb_www": full_url.count("www"),
        "nb_com": full_url.count(".com"),
        "nb_dslash": full_url.count("//"),

        "http_in_path": int("http" in path.lower()),
        "https_token": int("https" in hostname or "https" in path.lower()),

        "ratio_digits_url": digits_url / len(full_url) if full_url else 0,
        "ratio_digits_host": digits_host / len(hostname) if hostname else 0,

        "punycode": int("xn--" in hostname),
        "port": int(parsed.port is not None) if parsed.port else 0,

        "tld_in_path": int(any(f".{tld}" in path.lower() for tld in tld_set)),
        "tld_in_subdomain": int(any(t in subdomain for t in tld_set)),

        "abnormal_subdomain": int(subdomain.count(".") >= 3),
        "nb_subdomains": max(len(domain_parts) - 2, 0),

        "prefix_suffix": int("-" in hostname),

        "random_domain": int(entropy(hostname.split(".")[0]) > 3.5),

        "shortening_service": int(any(service in hostname for service in open(url_shortners).read().splitlines())),

        "path_extension": int(bool(re.search(r"\.[a-zA-Z0-9]{2,5}$", path))),

        "length_words_raw": len(raw_words),

        "char_repeat": count_char_repeats(full_url),

        "shortest_words_raw": safe_min(raw_word_lengths),
        "shortest_word_host": safe_min(host_word_lengths),
        "shortest_word_path": safe_min(path_word_lengths),

        "longest_words_raw": safe_max(raw_word_lengths),
        "longest_word_host": safe_max(host_word_lengths),
        "longest_word_path": safe_max(path_word_lengths),

        "avg_words_raw": safe_avg(raw_word_lengths),
        "avg_word_host": safe_avg(host_word_lengths),
        "avg_word_path": safe_avg(path_word_lengths),

        "phish_hints": sum(word in full_url for word in SUSPICIOUS_WORDS),

        "suspicious_tld": int(tld in SUSPICIOUS_TLDS)
    }

    feature_values = [features[name] for name in FEATURE_ORDER]
    input_tensor = torch.tensor([feature_values], dtype = torch.float32)

    return input_tensor
