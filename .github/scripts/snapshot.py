#!/usr/bin/env python3
"""Snapshot pipeline for the six-monitors repo.

Runs in GitHub Actions (see .github/workflows/snapshot.yml) every 6 hours.
Fetches public sources server-side with curl-equivalent HTTP (no CORS in a
runner), writes monitors/data/*.json, and on any source failure KEEPS the
last successful content for that source, marking it ok:false with a fresh
fetched_at. Never writes secrets to any file.

Sources (all curl-verified 2026-11-09, see audit doc):
  hot.json    Weibo intl weibointl.api.weibo.cn + Douyin iesdouyin hotsearch
              (+ Bilibili ranking, Zhihu recorded as 401/unavailable)
  ph.json     Product Hunt Atom feed producthunt.com/feed (no votes in RSS)
  trends.json Google Trends NEW rss https://trends.google.com/trending/rss
              geo=US/HK/TW only — geo=CN returns 400, NEVER use it
  prices.json OpenRouter /api/v1/models + models.dev api.json
              (models.dev /api/v1/models is dead, 302; api.json is live;
               Anthropic id is hyphenated: claude-opus-5-5)
  oss.json    GitHub Core API /repos/{full} for the 24-repo whitelist
              (GITHUB_TOKEN via Authorization header for rate limits)
"""
import json
import os
import re
import html
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
DATA = os.path.join(BASE, "monitors", "data")
UA = {"User-Agent": "Mozilla/5.0 (six-monitors snapshot; +https://github.com/xumao5393/six-monitors-)"}
GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")

NOW_UTC = datetime.now(timezone.utc)
CST = timezone(timedelta(hours=8))
FETCHED_AT = NOW_UTC.strftime("%Y-%m-%dT%H:%M:%SZ")
FETCHED_CST = NOW_UTC.astimezone(CST).strftime("%Y-%m-%d %H:%M:%S CST")
TODAY = NOW_UTC.astimezone(CST).strftime("%Y-%m-%d")  # Beijing date key
DAY = 86400


def fetch(url, timeout=25, headers=None):
    """Return (http_status, bytes) or (None, b'') on network failure."""
    h = dict(UA)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read() if hasattr(e, "read") else b""
    except Exception:
        return None, b""


def load_old(name):
    try:
        with open(os.path.join(DATA, name)) as f:
            return json.load(f)
    except Exception:
        return None


def save(name, obj):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, name), "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"wrote {name} ok={obj.get('ok')}")


def prune_history(hist, days=30):
    """hist: {YYYY-MM-DD: {...}} — keep last `days` entries."""
    if not isinstance(hist, dict):
        return {}
    cutoff = (NOW_UTC.astimezone(CST) - timedelta(days=days)).strftime("%Y-%m-%d")
    return {k: v for k, v in sorted(hist.items()) if k >= cutoff}


def delta_7d(hist, name, current):
    """Unified 7-day delta from snapshot history: earliest entry >=6 days
    before today; None until such a baseline exists (first week)."""
    if not isinstance(hist, dict):
        return None
    today = NOW_UTC.astimezone(CST).date()
    for date_str in sorted(hist):
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            continue
        if (today - d).days >= 6:
            base = hist[date_str]
            if isinstance(base, dict) and name in base:
                return current - base[name]
            return None
    return None


# ---------------------------------------------------------------- hot.json
def build_hot():
    old = load_old("hot.json") or {}
    old_plats = old.get("platforms", {}) if isinstance(old, dict) else {}
    plats = {}
    # Weibo intl
    st, body = fetch("https://weibointl.api.weibo.cn/portal.php?ct=feed&a=search_topic")
    if st == 200:
        try:
            data = json.loads(body).get("data", [])
            if not data:
                raise ValueError("empty list")
            plats["weibo"] = {"ok": True, "http": 200,
                "source": "https://weibointl.api.weibo.cn/portal.php?ct=feed&a=search_topic",
                "items": [{"title": x["title"], "heat": x.get("number")} for x in data[:10]]}
        except Exception as e:
            plats["weibo"] = dict(old_plats.get("weibo", {"ok": False, "items": []}), ok=False, http=st or 0, error="空响应（列表为空）" if "empty" in str(e) else "parse failed")
    else:
        plats["weibo"] = dict(old_plats.get("weibo", {"ok": False, "items": []}), ok=False, http=st or 0,
                              error=f"HTTP {st}" if st else "network failure")
    # Douyin
    st, body = fetch("https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/")
    if st == 200:
        try:
            data = json.loads(body).get("word_list", [])
            if not data:
                raise ValueError("empty list")
            plats["douyin"] = {"ok": True, "http": 200,
                "source": "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/",
                "items": [{"title": x["word"], "heat": x.get("hot_value")} for x in data[:10]]}
        except Exception as e:
            plats["douyin"] = dict(old_plats.get("douyin", {"ok": False, "items": []}), ok=False, http=st or 0, error="空响应（列表为空）" if "empty" in str(e) else "parse failed")
    else:
        plats["douyin"] = dict(old_plats.get("douyin", {"ok": False, "items": []}), ok=False, http=st or 0,
                               error=f"HTTP {st}" if st else "network failure")
    # Zhihu — expected 401; record it, never invent items
    st, _ = fetch("https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10")
    plats["zhihu"] = {"ok": False, "http": st or 0,
        "source": "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10",
        "error": "401 身份未验证" if st == 401 else (f"HTTP {st}" if st else "network failure"), "items": []}
    # Bilibili ranking (no heat values published)
    st, body = fetch("https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all", headers={"Referer": "https://www.bilibili.com"})
    if st == 200:
        try:
            data = json.loads(body).get("data", {}).get("list", [])
            if not data:
                raise ValueError("empty list")
            plats["bili"] = {"ok": True, "http": 200,
                "source": "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all",
                "items": [{"title": x["title"], "category": x.get("tname")} for x in data[:10]]}
        except Exception as e:
            plats["bili"] = dict(old_plats.get("bili", {"ok": False, "items": []}), ok=False, http=st or 0, error="空响应（列表为空）" if "empty" in str(e) else "parse failed")
    else:
        plats["bili"] = dict(old_plats.get("bili", {"ok": False, "items": []}), ok=False, http=st or 0,
                             error=f"HTTP {st}" if st else "network failure")
    save("hot.json", {
        "fetched_at": FETCHED_AT, "fetched_at_cst": FETCHED_CST,
        "ok": bool(plats["weibo"]["ok"] and plats["douyin"]["ok"]),
        "source": "GitHub Actions snapshot (curl, server-side) — see .github/workflows/snapshot.yml; browser direct fetch is CORS-blocked",
        "platforms": plats,
        "browser": {"note": "浏览器直连：微博/抖音/B站均无 CORS 头，直连失败是预期；本文件为服务端 curl 快照，页面只读同域 JSON。知乎 curl 亦 401。"},
    })


# ---------------------------------------------------------------- ph.json
def build_ph():
    old = load_old("ph.json") or {}
    st, body = fetch("https://www.producthunt.com/feed")
    if st == 200:
        try:
            ns = {"a": "http://www.w3.org/2005/Atom"}
            root = ET.fromstring(body)
            items = []
            for e in root.findall("a:entry", ns)[:15]:
                link = [l.get("href") for l in e.findall("a:link", ns) if l.get("rel") == "alternate"]
                content = e.find("a:content", ns)
                txt = re.sub(r"<[^>]+>", " ", html.unescape(content.text or "")) if content is not None else ""
                items.append({"title": (e.findtext("a:title", namespaces=ns) or "").strip(),
                              "link": link[0] if link else "",
                              "published": e.findtext("a:published", namespaces=ns),
                              "votes": None, "votes_note": "票数未获取（Product Hunt RSS 不含票数）",
                              "summary": re.sub(r"\s+", " ", txt).strip()[:200]})
            if not items:
                raise ValueError("empty feed")
            save("ph.json", {"fetched_at": FETCHED_AT, "fetched_at_cst": FETCHED_CST, "ok": True,
                             "source": "https://www.producthunt.com/feed",
                             "note": "RSS 无 CORS，浏览器必失败；本文件为服务端 curl 快照。票数 RSS 不提供，一律未获取，不编造。",
                             "items": items})
            return
        except Exception:
            pass
    # failure: keep last successful items, mark ok:false
    save("ph.json", {"fetched_at": FETCHED_AT, "fetched_at_cst": FETCHED_CST, "ok": False,
                     "source": "https://www.producthunt.com/feed",
                     "note": "本次抓取失败，保留上次成功内容；票数 RSS 不提供，一律未获取。",
                     "error": f"HTTP {st}" if st else "network failure",
                     "items": old.get("items", [])})


# ---------------------------------------------------------------- trends.json
def parse_trends_rss(body):
    root = ET.fromstring(body)
    out = []
    for it in root.findall(".//item")[:10]:
        traffic = None
        for ch in it:
            if ch.tag.endswith("approx_traffic"):
                traffic = ch.text
        out.append({"title": it.findtext("title"), "traffic": traffic, "link": it.findtext("link")})
    return out


def build_trends():
    old = load_old("trends.json") or {}
    old_geos = old.get("geos", {}) if isinstance(old, dict) else {}
    geos = {}
    all_ok = True
    for geo in ("US", "HK", "TW"):  # NEVER geo=CN (400)
        st, body = fetch(f"https://trends.google.com/trending/rss?geo={geo}")
        if st == 200:
            try:
                _items = parse_trends_rss(body)
                if not _items:
                    raise ValueError("empty feed")
                geos[geo] = {"ok": True, "http": 200, "items": _items}
                continue
            except Exception:
                pass
        all_ok = False
        geos[geo] = dict(old_geos.get(geo, {"ok": False, "items": []}), ok=False, http=st or 0,
                         error=f"HTTP {st}" if st else "network failure")
    geos["CN"] = {"ok": False, "http": 400, "error": "geo=CN 返回 400 Bad Request，永不使用", "items": []}
    save("trends.json", {"fetched_at": FETCHED_AT, "fetched_at_cst": FETCHED_CST, "ok": all_ok,
                         "source": "https://trends.google.com/trending/rss (new endpoint; old daily RSS 404)",
                         "note": "geo=CN 返回 400，永不使用。RSS 无 CORS，浏览器拉不到；本文件为服务端 curl 快照。",
                         "geos": geos})


# ---------------------------------------------------------------- prices.json
FLAGSHIPS = ['openai/gpt-6.1-terra', 'openai/gpt-6.1-sol', 'anthropic/claude-opus-5.5',
             'google/gemini-4-argon', 'x-ai/grok-4.7', 'deepseek/deepseek-v4-pro',
             'qwen/qwen3.8-max-prime', 'moonshotai/kimi-k3.1-pro', 'z-ai/glm-5.3-prime',
             'bytedance-seed/seed-2-1-turbo']
EXTRA_PREFIXES = ('openai/gpt-', 'anthropic/claude-', 'google/gemini-', 'x-ai/grok-',
                  'deepseek/', 'qwen/', 'moonshotai/kimi-', 'z-ai/glm-', 'meta-llama/llama-')
MD_KEEP = ("opus-5", "opus-4-5", "gpt-6.1", "gemini-4", "grok-4.7", "deepseek-v4",
           "kimi-k3", "glm-5.3", "seed-2-1", "claude-opus-5-5")
MD_PROVIDERS = {"anthropic", "openai", "google", "x-ai", "deepseek", "qwen",
                "moonshotai", "z-ai", "bytedance-seed"}


def build_prices():
    old = load_old("prices.json") or {}
    or_ok, md_ok = False, False
    models, md_models = old.get("openrouter_models", []), old.get("models_dev_models", {})
    st, body = fetch("https://openrouter.ai/api/v1/models")
    if st == 200:
        try:
            data = json.loads(body)["data"]

            def price(m):
                p = m.get("pricing") or {}

                def conv(k):
                    try:
                        return round(float(p[k]) * 1e6, 4) if p.get(k) is not None else None
                    except Exception:
                        return None
                return {"id": m["id"], "name": m.get("name"),
                        "prompt_per_m": conv("prompt"), "completion_per_m": conv("completion"),
                        "context_length": m.get("context_length")}
            seen, uniq = set(), []
            for m in data:
                if m["id"] in FLAGSHIPS or m["id"].startswith(EXTRA_PREFIXES):
                    if m["id"] not in seen:
                        seen.add(m["id"])
                        uniq.append(price(m))
            models, or_ok = uniq, True
            total = len(data)
        except Exception:
            total = old.get("sources", {}).get("openrouter", {}).get("total_models")
    else:
        total = old.get("sources", {}).get("openrouter", {}).get("total_models")
    st2, body2 = fetch("https://models.dev/api.json")
    if st2 == 200:
        try:
            md = json.loads(body2)
            md_models = {}
            for prov, pdata in md.items():
                for mid, m in (pdata.get("models") or {}).items():
                    c = m.get("cost") or {}
                    if (c.get("input") is not None or c.get("output") is not None) \
                            and prov in MD_PROVIDERS and any(s in mid for s in MD_KEEP):
                        md_models[f"{prov}/{mid}"] = {"provider": prov, "id": mid, "name": m.get("name"),
                                                      "input_per_m": c.get("input"), "output_per_m": c.get("output")}
            md_ok = True
        except Exception:
            pass
    hist = prune_history(old.get("history", {}))
    hist[TODAY] = {m["id"]: {"prompt_per_m": m["prompt_per_m"], "completion_per_m": m["completion_per_m"]} for m in models}
    save("prices.json", {"fetched_at": FETCHED_AT, "fetched_at_cst": FETCHED_CST, "ok": bool(or_ok and md_ok),
                         "sources": {
                             "openrouter": {"ok": or_ok, "http": st or 0, "source": "https://openrouter.ai/api/v1/models",
                                            "total_models": total, "flagship_ids": FLAGSHIPS},
                             "models_dev": {"ok": md_ok, "http": st2 or 0, "source": "https://models.dev/api.json",
                                            "note": "models.dev api.json 活；/api/v1/models 已死（302）。Anthropic id 用连字符 claude-opus-5-5。"},
                         },
                         "openrouter_models": models, "models_dev_models": md_models, "history": hist})


# ---------------------------------------------------------------- oss.json
WHITELIST = [
    ('ollama/ollama', 'LLM'), ('huggingface/transformers', 'LLM'), ('ggml-org/llama.cpp', 'LLM'),
    ('vllm-project/vllm', 'LLM'), ('mlc-ai/mlc-llm', 'LLM'), ('oobabooga/textgen', 'LLM'),
    ('langchain-ai/langchain', 'Agent'), ('langchain-ai/langgraph', 'Agent'), ('microsoft/autogen', 'Agent'),
    ('crewAIInc/crewAI', 'Agent'), ('Significant-Gravitas/AutoGPT', 'Agent'),
    ('modelcontextprotocol/servers', 'MCP'), ('modelcontextprotocol/typescript-sdk', 'MCP'),
    ('openai/codex', '编码'), ('continuedev/continue', '编码'), ('Aider-AI/aider', '编码'), ('opencode-ai/opencode', '编码'),
    ('Comfy-Org/ComfyUI', '视觉'), ('AUTOMATIC1111/stable-diffusion-webui', '视觉'), ('huggingface/diffusers', '视觉'),
    ('openai/whisper', '音频'), ('SYSTRAN/faster-whisper', '音频'), ('coqui-ai/TTS', '音频'), ('RVC-Boss/GPT-SoVITS', '音频'),
]


def build_oss():
    old = load_old("oss.json") or {}
    old_repos = {r["name"]: r for r in old.get("repos", []) if isinstance(r, dict)}
    headers = {"Accept": "application/vnd.github+json"}
    if GH_TOKEN:
        headers["Authorization"] = f"Bearer {GH_TOKEN}"  # rate limits only; never written to files
    repos, failed = [], []
    fetched_ok = 0
    for name, cat in WHITELIST:
        st, body = fetch(f"https://api.github.com/repos/{name}", headers=headers)
        if st == 200:
            try:
                d = json.loads(body)
                fetched_ok += 1
                repos.append({"name": d["full_name"], "cat": cat, "stars": d["stargazers_count"],
                              "forks": d["forks_count"], "language": d.get("language"),
                              "pushed_at": d.get("pushed_at"), "delta_7d": None})
                continue
            except Exception:
                pass
        failed.append(name)
        if name in old_repos:  # keep last successful repo row on failure
            repos.append(old_repos[name])
    hist = prune_history(old.get("history", {}))
    if repos:
        hist[TODAY] = {r["name"]: r["stars"] for r in repos}
    for r in repos:
        r["delta_7d"] = delta_7d(hist, r["name"], r["stars"])
    save("oss.json", {"fetched_at": FETCHED_AT, "fetched_at_cst": FETCHED_CST,
                      "ok": len(failed) == 0, "ok_count": fetched_ok,
                      "count": len(WHITELIST), "failed": failed,
                      "source": "GitHub Core API https://api.github.com/repos/{full} (24 whitelist repos, GITHUB_TOKEN in Actions)",
                      "note": "周增 Δ Star 需连续快照 ≥7 天：delta_7d 由 history 中 ≥6 天前的基线算出，第 1 周为 null，之后全站统一 Δ；页面同时保留本机 localStorage 差分作补充。",
                      "repos": repos, "history": hist})


if __name__ == "__main__":
    build_hot()
    build_ph()
    build_trends()
    build_prices()
    build_oss()
    print("snapshot done", FETCHED_AT, FETCHED_CST)
