#!/usr/bin/env python3
import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any

import aiohttp

URLS_DEFAULT = [
    "https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band1",
    "https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band2",
    "https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band3",
    "https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band4",
    "https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band5",
    "https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band6",
    "https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band7",
    "https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band8",
    "https://emono.unibas.ch/stadtgeschichtebasel/catalog/book/band9",
]

# DOI regex (Crossref-compatible, case-insensitive). We normalize to lowercase.
DOI_RE = re.compile(r"10\.\d{4,9}/[A-Za-z0-9][A-Za-z0-9().;_/:~-]*", re.IGNORECASE)
DOI_HREF_RE = re.compile(r'href=["\']https?://doi\.org/([^"\'<> ]+)["\']', re.IGNORECASE)
TRAILING_PUNCT_RE = re.compile(r'[">)\].,;]+$')

USER_AGENT = "doi-harvester/2.0 (+https://example.org; mailto:contact@example.org)"


def clean_doi(raw: str) -> str:
    """Lowercase and strip common trailing punctuation."""
    d = raw.strip()
    d = TRAILING_PUNCT_RE.sub("", d)
    return d.lower()


def extract_from_html(html: str, url: str) -> list[tuple[str, str, str, str]]:
    """
    Returns list of (doi, page, origin, detail)
    origin ∈ {"href","text"}
    detail includes line number and snippet or full href.
    """
    out: list[tuple[str, str, str, str]] = []
    lines = html.splitlines()

    # A) href-based extraction with line numbers
    for i, line in enumerate(lines, start=1):
        for m in DOI_HREF_RE.finditer(line):
            doi = clean_doi(m.group(1))
            if doi:
                href = f"https://doi.org/{doi}"
                out.append((doi, url, "href", f"line {i}: {href}"))

    # B) raw text DOI with line context
    for i, line in enumerate(lines, start=1):
        for m in DOI_RE.finditer(line):
            doi = clean_doi(m.group(0))
            if doi:
                ctx = line.strip()
                if len(ctx) > 200:
                    ctx = ctx[:200] + "…"
                out.append((doi, url, "text", f"line {i}: {ctx}"))

    return out


async def fetch_text(session: aiohttp.ClientSession, url: str, *, retries: int = 3) -> str:
    backoff = 1.0
    for attempt in range(1, retries + 1):
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.text()
        except Exception:
            if attempt == retries:
                raise
            await asyncio.sleep(backoff)
            backoff *= 2
    raise RuntimeError("unreachable")


async def fetch_json(session: aiohttp.ClientSession, url: str, *, retries: int = 3) -> Any:
    backoff = 1.0
    for attempt in range(1, retries + 1):
        try:
            async with session.get(
                url,
                headers={
                    "Accept": "application/vnd.citationstyles.csl+json, application/json;q=0.9"
                },
            ) as resp:
                if resp.status != 200:
                    raise aiohttp.ClientResponseError(
                        resp.request_info,
                        resp.history,
                        status=resp.status,
                        message=f"HTTP {resp.status}",
                    )
                text = await resp.text()
                return json.loads(text)
        except Exception:
            if attempt == retries:
                raise
            await asyncio.sleep(backoff)
            backoff *= 2
    raise RuntimeError("unreachable")


async def gather_pages(urls: list[str]) -> dict[str, str]:
    timeout = aiohttp.ClientTimeout(total=45)
    async with aiohttp.ClientSession(
        timeout=timeout, headers={"User-Agent": USER_AGENT}
    ) as session:
        # maintain URL association while still benefiting from concurrency
        results = await asyncio.gather(
            *[fetch_text(session, u) for u in urls], return_exceptions=True
        )
        htmls: dict[str, str] = {}
        for u, res in zip(urls, results, strict=True):
            if isinstance(res, Exception):
                print(f"WARN: could not fetch page: {u}", file=sys.stderr)
            else:
                htmls[u] = res
        return htmls


async def gather_csl(
    dois: list[str], provenance: dict[str, list[tuple[str, str, str]]], concurrency: int = 10
):
    timeout = aiohttp.ClientTimeout(total=45)
    sem = asyncio.Semaphore(concurrency)
    ok: list[Any] = []
    failures: dict[str, str] = {}

    async with aiohttp.ClientSession(
        timeout=timeout, headers={"User-Agent": USER_AGENT}
    ) as session:

        async def worker(doi: str):
            url = f"https://doi.org/{doi}"
            async with sem:
                try:
                    data = await fetch_json(session, url)
                    ok.append(data)
                except Exception as e:
                    failures[doi] = f"{type(e).__name__}: {e}"

        await asyncio.gather(*[worker(d) for d in dois])
    return ok, failures


def write_failed_report(
    failures: dict[str, str], provenance: dict[str, list[tuple[str, str, str]]], out_path: Path
):
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Failed DOI fetches: {len(failures)}\n\n")
        for doi in sorted(failures):
            f.write(f"DOI: {doi}\n")
            f.write(f"  error: {failures[doi]}\n")
            for page, origin, detail in provenance.get(doi, []):
                f.write(f"  page: {page}\n  origin: {origin}\n  detail: {detail}\n\n")


def main():
    ap = argparse.ArgumentParser(
        description="Extract DOIs from pages, fetch CSL JSON, and compile outputs."
    )
    ap.add_argument(
        "--url", action="append", help="Add a URL to scan (can be used multiple times)."
    )
    ap.add_argument("--urls-file", type=Path, help="Path to a text file with one URL per line.")
    ap.add_argument(
        "--concurrency", type=int, default=10, help="Concurrent DOI fetches. Default 10."
    )
    ap.add_argument("--out-dois", type=Path, default=Path("dois.txt"))
    ap.add_argument("--out-json", type=Path, default=Path("metadata.json"))
    ap.add_argument("--out-fail", type=Path, default=Path("failed_dois_report.txt"))
    args = ap.parse_args()

    urls: list[str] = []
    if args.urls_file and args.urls_file.exists():
        urls.extend(
            [
                line.strip()
                for line in args.urls_file.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        )
    if args.url:
        urls.extend(args.url)
    if not urls:
        urls = URLS_DEFAULT

    # 1) Fetch pages
    html_map = asyncio.run(gather_pages(urls))

    # 2) Extract DOIs with provenance
    prov: dict[str, list[tuple[str, str, str]]] = {}
    for url, html in html_map.items():
        for doi, page, origin, detail in extract_from_html(html, url):
            prov.setdefault(doi, []).append((page, origin, detail))

    # 3) Unique sorted DOI list
    dois_sorted = sorted(prov.keys())
    if not dois_sorted:
        print("No DOIs found.", file=sys.stderr)
        sys.exit(1)

    args.out_dois.write_text("\n".join(dois_sorted) + "\n", encoding="utf-8")
    print(f"Wrote {len(dois_sorted)} unique DOIs -> {args.out_dois}")

    # 4) Fetch CSL JSON concurrently
    ok, failures = asyncio.run(gather_csl(dois_sorted, prov, concurrency=args.concurrency))

    # 5) Write JSON array
    args.out_json.write_text(json.dumps(ok, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(ok)} records -> {args.out_json}")

    # 6) Failure report
    if failures:
        write_failed_report(failures, prov, args.out_fail)
        print(f"Wrote provenance report -> {args.out_fail}")


if __name__ == "__main__":
    main()
