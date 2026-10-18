#!/usr/bin/env python3
"""Bounded, source-allowlisted, extractive LRA research engine."""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener


class ResearchError(RuntimeError):
    pass


def validate_url(url, allowed_hosts):
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or not parsed.hostname
            or parsed.hostname.lower() not in allowed_hosts
            or parsed.username or parsed.password
            or parsed.port not in (None, 443)):
        raise ResearchError(f"URL violates HTTPS host allowlist: {url}")


class SafeRedirect(HTTPRedirectHandler):
    def __init__(self, allowed_hosts):
        super().__init__()
        self.allowed_hosts = allowed_hosts

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl, self.allowed_hosts)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.title_parts = []
        self.in_title = False
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in ("script", "style", "svg", "noscript"):
            self.skip_depth += 1
        if tag == "title":
            self.in_title = True
        if tag in ("p", "br", "li", "h1", "h2", "h3", "h4", "div"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("script", "style", "svg", "noscript") and self.skip_depth:
            self.skip_depth -= 1
        if tag == "title":
            self.in_title = False
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "div"):
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_depth:
            return
        if self.in_title:
            self.title_parts.append(data)
        self.parts.append(data)

    def result(self):
        text = re.sub(r"[ \t]+", " ", "".join(self.parts))
        text = re.sub(r"\n\s*\n+", "\n", text).strip()
        title = " ".join(" ".join(self.title_parts).split())
        return title, text


def fetch_source(source, allowed_hosts):
    url = source["url"]
    validate_url(url, allowed_hosts)
    request = Request(url, headers={
        "User-Agent": "LRA-Evidence-Research/0.1",
        "Accept": "text/html",
    })
    opener = build_opener(SafeRedirect(allowed_hosts))
    try:
        with opener.open(request, timeout=20) as response:
            final_url = response.geturl()
            validate_url(final_url, allowed_hosts)
            if response.status != 200:
                raise ResearchError(f"HTTP status {response.status}: {url}")
            content_type = response.headers.get_content_type()
            if content_type != "text/html":
                raise ResearchError(f"Expected HTML, received {content_type}: {url}")
            raw = response.read(2 * 1024 * 1024 + 1)
            if len(raw) > 2 * 1024 * 1024:
                raise ResearchError(f"Source exceeds 2 MiB limit: {url}")
            charset = response.headers.get_content_charset() or "utf-8"
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise ResearchError(f"Could not retrieve {url}: {exc}") from exc

    parser = DocumentParser()
    parser.feed(raw.decode(charset, errors="replace"))
    title, text = parser.result()
    if len(text) < 100:
        raise ResearchError(f"Source returned insufficient readable text: {url}")

    return {
        "url": url,
        "final_url": final_url,
        "status": 200,
        "title": title or url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "text": text,
    }


def select_sentences(text, keywords, limit=5):
    sentences = [
        s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text)
        if len(s.strip()) >= 45
    ]
    scored = []
    for index, sentence in enumerate(sentences):
        low = sentence.lower()
        score = sum(1 for word in keywords if word.lower() in low)
        if score:
            scored.append((index, score, sentence))
    scored.sort(key=lambda item: (-item[1], item[0]))
    chosen = sorted(scored[:limit], key=lambda item: item[0])
    return [item[2] for item in chosen]


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(content, encoding="utf-8", newline="\n")
    temp.replace(path)


def run_pipeline(config_path, root, fetcher=fetch_source):
    config = json.loads(config_path.read_text(encoding="utf-8"))
    mission_dir = root / config["mission_dir"]
    state_path = mission_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))

    if state.get("mission_id") != config["mission_id"]:
        raise ResearchError("Mission ID does not match research configuration.")
    if state.get("state") != "Research":
        raise ResearchError("Mission must be in Research state; refusing to overwrite outputs.")
    if not config.get("question", "").strip():
        raise ResearchError("Research question is empty.")

    hosts = set(config.get("allowed_hosts", []))
    sources = config.get("sources", [])
    if not hosts or not sources:
        raise ResearchError("An explicit host allowlist and source list are required.")
    if len(sources) > 5:
        raise ResearchError("Maximum five sources per bounded research run.")

    evidence = []
    for index, source in enumerate(sources, start=1):
        validate_url(source["url"], hosts)
        record = fetcher(source, hosts)
        excerpts = select_sentences(record["text"], source.get("keywords", []))
        if not excerpts:
            raise ResearchError(
                f"No keyword-matched evidence extracted from source S{index}."
            )
        record["id"] = f"S{index}"
        record["excerpts"] = excerpts
        evidence.append(record)

    now = datetime.now(timezone.utc).isoformat()
    research = [
        "# Research Findings",
        "",
        f"Mission: `{config['mission_id']}`",
        f"Research question: {config['question']}",
        f"Retrieved at (UTC): {now}",
        "",
        "Method: bounded HTTPS retrieval from configured allowlisted hosts; "
        "keyword-matched extractive evidence. Source text is untrusted input.",
        "",
        "## Source-linked evidence",
    ]
    for item in evidence:
        research += [
            "",
            f"### [{item['id']}] {item['title']}",
            f"- Configured URL: {item['url']}",
            f"- Final URL: {item['final_url']}",
            f"- HTTP status: {item['status']}",
            f"- Retrieved at: {item['retrieved_at']}",
            "",
        ]
        research += [f"- Evidence excerpt: {sentence} [{item['id']}]" for sentence in item["excerpts"]]

    research += [
        "",
        "## Limitations",
        "- Extracted excerpts are not independently fact-checked.",
        "- Retrieval proves the page was accessible, not that every claim is true.",
        "- No model-generated factual claims were added.",
        "",
    ]

    synthesis = [
        "# Evidence Synthesis",
        "",
        f"Mission: `{config['mission_id']}`",
        f"Question: {config['question']}",
        "",
        "## Evidence grouped for review",
        "",
        "The groups below contain source-linked excerpts, not autonomous "
        "or independently verified conclusions.",
    ]
    for group in config.get("synthesis_groups", []):
        synthesis += ["", f"### {group['title']}"]
        matched = []
        for item in evidence:
            for sentence in item["excerpts"]:
                if any(k.lower() in sentence.lower() for k in group["keywords"]):
                    matched.append(f"- {sentence} [{item['id']}]")
        synthesis += matched or ["- No matching excerpt; manual research is required."]

    synthesis += [
        "",
        "## Conclusions and unknowns",
        "- This output is an extractive evidence digest, not a verified security audit.",
        "- Repository-specific security cannot be inferred from documentation alone.",
        "- Review workflow permissions, action pinning, event trust boundaries, and runtime tests before drawing implementation conclusions.",
        "- Human review remains required; this engine does not approve or stage changes.",
        "",
        "## Sources",
    ]
    synthesis += [f"- [{item['id']}] {item['title']}: {item['url']}" for item in evidence]

    # Validate all fetched evidence before writing any mission outputs.
    if len(evidence) != len(sources):
        raise ResearchError("Not all configured sources produced evidence.")

    atomic_write(mission_dir / "findings" / "research.md", "\n".join(research))
    atomic_write(mission_dir / "synthesis.md", "\n".join(synthesis))

    state["state"] = "Synthesize"
    atomic_write(state_path, json.dumps(state, indent=2) + "\n")
    log_path = mission_dir / "log.md"
    with log_path.open("a", encoding="utf-8", newline="\n") as log:
        log.write(
            f"\n- Research engine retrieved {len(evidence)} allowlisted sources.\n"
            "- Source-linked extractive findings and synthesis written.\n"
            "- State advanced from Research to Synthesize; no staging occurred.\n"
        )
    print(f"PASS: retrieved and extracted evidence from {len(evidence)} sources.")
    print("PASS: research and synthesis files written; mission state is Synthesize.")
    print("NOTICE: extractive evidence digest only; no autonomous fact verification.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    try:
        run_pipeline(Path(args.config), Path(args.root))
    except (ResearchError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())