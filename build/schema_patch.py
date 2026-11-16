# Schema (JSON-LD) + share-card fixes from the 2026-11-16 audit of all 4 CaseAuthority sites.
# Runs on the FINAL built output (after split / sister_split), so it sees exactly what goes live.
#   python3 schema_patch.py public <pi|criminal|divorce|estate> <main|blog>
# Sister MAIN builds must put og-image.png and favicon-512.png into public/ before running this.
# Idempotent. Fails the build (exit 1) if any page ends up without valid, expected markup.
import html, json, pathlib, re, sys

ROOT, BRAND, MODE = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
DOMAINS = {"pi": "seopersonalinjurylawyer.com", "criminal": "seocriminaldefenselawyer.com",
           "divorce": "seodivorcelawyer.com", "estate": "seoestatelawyer.com"}
NICHE = {"criminal": "criminal defense lawyers", "divorce": "divorce lawyers", "estate": "estate planning lawyers"}
DOM = DOMAINS[BRAND]
BASE = "https://%s/" % DOM
ORG_ID = BASE + "#org"
LOGO = BASE + "favicon-512.png"
LINKEDIN = "https://www.linkedin.com/company/caseauthority/"
PHONE = "+1-838-205-8892"
OG_IMG = BASE + "og-image.png"
SISTER = BRAND != "pi"
OG_ALT = "CaseAuthority: SEO for %s. Rank #1. Sign more clients." % NICHE.get(BRAND, "")

# PI pages that are not services: page type to use instead of Service.
PI_PAGE_TYPES = {"contact": "ContactPage", "privacy-policy": "WebPage", "sales": "WebPage",
                 "case-studies": "CollectionPage", "why-choose-caseauthority": "AboutPage"}

LD_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def meta(s, pat):
    m = re.search(pat, s)
    return html.unescape(m.group(1)) if m else None


def nodes_of(data):
    if isinstance(data, dict) and "@graph" in data:
        return data["@graph"]
    return data if isinstance(data, list) else [data]


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for i in o:
            yield from walk(i)


def fix_org(o):
    """Normalise a CaseAuthority LLC organisation object in place."""
    if o.get("description"):
        o["description"] = o["description"].replace("CaseAuthority (Case Authority LLC) is", "CaseAuthority LLC is")
    if o.get("telephone"):
        o["telephone"] = PHONE
    o.setdefault("logo", LOGO)
    o.setdefault("image", LOGO)
    if not o.get("sameAs"):
        o["sameAs"] = [LINKEDIN]


def is_ca_org(o):
    return (o.get("@type") in ("ProfessionalService", "Organization")
            and o.get("name") == "CaseAuthority LLC")


def patch_ld(data, page_url, slug, s):
    nodes = nodes_of(data)
    for o in walk(nodes):
        if is_ca_org(o):
            if SISTER and o.get("@id") not in (None, ORG_ID):
                continue
            if not SISTER and "@id" not in o:
                # PI inline copies of the business: tie them to the home page entity.
                o["@id"] = ORG_ID
                if o.get("@type") == "Organization":
                    o["@type"] = "ProfessionalService"
            fix_org(o)
    out = []
    for n in nodes:
        t = n.get("@type")
        if t == "BlogPosting" and "url" not in n:
            n["url"] = page_url
        if t == "Blog" and "publisher" not in n:
            n["publisher"] = ({"@id": ORG_ID} if SISTER else
                              {"@type": "ProfessionalService", "@id": ORG_ID, "name": "CaseAuthority LLC",
                               "url": BASE, "logo": LOGO, "image": LOGO, "sameAs": [LINKEDIN]})
        if t == "Service" and not SISTER and slug in PI_PAGE_TYPES:
            prov = n.get("provider") or {}
            fix_org(prov)
            prov["@id"] = ORG_ID
            title = meta(s, r'(?s)<title[^>]*>(.*?)</title>') or n.get("name")
            desc = meta(s, r'<meta name="description" content="([^"]*)"') or n.get("description")
            n = {"@type": PI_PAGE_TYPES[slug], "@id": page_url + "#webpage", "url": page_url,
                 "name": title.strip(), "description": desc, "inLanguage": "en-US",
                 "isPartOf": {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "CaseAuthority LLC"},
                 "publisher": prov}
            if slug in ("why-choose-caseauthority",):
                n["about"] = {"@id": ORG_ID}
        if t == "OfferCatalog" and SISTER:
            # Orphan node on sister home pages: attach it to the business instead.
            org = next((x for x in nodes if x.get("@id") == ORG_ID), None)
            if org is not None:
                org["hasOfferCatalog"] = n
                continue
        out.append(n)
    if isinstance(data, dict) and "@graph" in data:
        data["@graph"] = out
        return data
    return out if isinstance(data, list) else out[0]


def og_block(s):
    title = meta(s, r'<meta property="og:title" content="([^"]*)"') or meta(s, r'(?s)<title[^>]*>(.*?)</title>') or "CaseAuthority LLC"
    desc = meta(s, r'<meta property="og:description" content="([^"]*)"') or meta(s, r'<meta name="description" content="([^"]*)"')
    e = lambda x: html.escape(x.strip(), quote=True)
    tags = ['<meta property="og:image" content="%s">' % OG_IMG,
            '<meta property="og:image:secure_url" content="%s">' % OG_IMG,
            '<meta property="og:image:type" content="image/png">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            '<meta property="og:image:alt" content="%s">' % e(OG_ALT),
            '<meta name="twitter:card" content="summary_large_image">',
            '<meta name="twitter:title" content="%s">' % e(title)]
    if desc:
        tags.append('<meta name="twitter:description" content="%s">' % e(desc))
    tags += ['<meta name="twitter:image" content="%s">' % OG_IMG,
             '<meta name="twitter:image:alt" content="%s">' % e(OG_ALT)]
    return "\n".join(tags)


bad, changed, pages = [], 0, 0
for p in sorted(ROOT.rglob("*.html")):
    s0 = s = p.read_text(encoding="utf-8")
    canon = meta(s, r'<link rel="canonical" href="([^"]*)"')
    page_url = canon or BASE  # 404 and similar still get the org markup normalised
    slug = page_url[len(BASE):].strip("/") if page_url.startswith(BASE) else ""

    def repl(m):
        data = json.loads(m.group(2))
        data = patch_ld(data, page_url, slug, s)
        txt = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        return m.group(1) + txt + m.group(3)

    try:
        s = LD_RE.sub(repl, s)
    except Exception as ex:  # unparsable JSON-LD must never ship
        bad.append("%s: JSON-LD error %s" % (p, ex)); continue

    if SISTER and 'property="og:image"' not in s:
        s = re.sub(r'<meta name="twitter:card" content="summary">\n?', "", s)
        ms = list(re.finditer(r'<meta property="og:[^"]*" content="[^"]*">\n?', s))
        head_end = s.find("</head>")
        if not ms or ms[-1].end() > head_end:
            bad.append("%s: no og: tags in head" % p); continue
        i = ms[-1].end()
        s = s[:i] + ("" if s[i - 1] == "\n" else "\n") + og_block(s) + "\n" + s[i:]

    if s != s0:
        p.write_text(s, encoding="utf-8")
        changed += 1
    pages += 1

# ---- verification: every page must now pass ----
if SISTER and MODE == "main":
    for f in ("og-image.png", "favicon-512.png"):
        q = ROOT / f
        if not q.is_file() or q.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            bad.append("missing or invalid public/%s" % f)
for p in sorted(ROOT.rglob("*.html")):
    s = p.read_text(encoding="utf-8")
    blocks = LD_RE.findall(s)
    objs = []
    for b in blocks:
        try:
            objs += list(walk(nodes_of(json.loads(b[1]))))
        except Exception as ex:
            bad.append("%s: JSON-LD does not parse (%s)" % (p, ex))
    types = [o.get("@type") for o in objs]
    if "VideoObject" in types:
        bad.append("%s: VideoObject present" % p)
    for o in objs:
        if o.get("@type") == "AudioObject" and "transcript" in o:
            bad.append("%s: AudioObject has transcript" % p)
        if is_ca_org(o) and o.get("@id") == ORG_ID:
            if not o.get("logo") or LINKEDIN not in (o.get("sameAs") or []):
                bad.append("%s: org missing logo/sameAs" % p)
        if o.get("@type") == "BlogPosting" and "headline" in o and "author" in o and "url" not in o:
            bad.append("%s: BlogPosting without url" % p)
        if isinstance(o.get("description"), str) and "Case Authority LLC" in o["description"]:
            bad.append("%s: old spelling 'Case Authority LLC' in schema" % p)
    if not SISTER:
        canon = meta(s, r'<link rel="canonical" href="([^"]*)"') or ""
        slug = canon[len(BASE):].strip("/")
        if slug in PI_PAGE_TYPES and "Service" in types:
            bad.append("%s: Service markup on a non-service page" % p)
    if SISTER and blocks:
        if s.count('property="og:image"') != 1 or s.count('name="twitter:card"') != 1 or 'content="summary_large_image"' not in s:
            bad.append("%s: share card tags wrong" % p)

if bad:
    print("schema_patch FAILED:\n  " + "\n  ".join(bad[:40]))
    sys.exit(1)
print("schema_patch ok: %s %s, %d pages checked, %d changed" % (BRAND, MODE, pages, changed))
