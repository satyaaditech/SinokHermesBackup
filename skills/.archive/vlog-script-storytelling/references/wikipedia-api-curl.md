# Wikipedia Fact Verification via curl (fallback when web tools unconfigured)

Use when `web_search` / `web_extract` fail with "Web tools are not configured"
(Firecrawl missing). Wikipedia REST/MediaWiki APIs are reachable via plain curl —
this is the durable fallback for fact-checking Indonesian content.

## Plain-text extract (main workhorse)

```bash
curl -sL --max-time 30 \
  "https://id.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&titles=Stadion_Manahan" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); p=list(d['query']['pages'].values())[0]; print(p.get('extract','NO EXTRACT'))"
```

- `explaintext=1` strips wikitext → clean prose.
- Slice long extracts with python slicing: `e[2500:6500]`.
- Batch several titles in a shell loop (independent pages).

## Redirects (frequent gotcha)

`Kotagede` and `Panembahan_Senapati` returned EMPTY extracts — they are redirects.
Fix options:

1. Add the boolean redirects flag to the query:
   `...action=query&prop=extracts&explaintext=1&format=json&redirects&titles=Kotagede`
2. Or use the REST summary endpoint, which follows redirects and returns
   resolved title + extract:
   ```bash
   curl -sL -A "Mozilla/5.0" "https://id.wikipedia.org/api/rest_v1/page/summary/Kotagede"
   # returns "title": "Kotagede, Yogyakarta" + extract
   ```

## Reliability notes

- JSON parse errors (`JSONDecodeError: Expecting value`) = throttled/empty response.
  Retry after `sleep 2`; save to file first (`curl -o /tmp/x.json`) then parse.
- Non-existent pages return "NO EXTRACT" / empty — evidence of absence, do not fabricate.
- Always keep a source list at the end of delivered content; mark unverified claims (±).
- Cross-check critical claims against a second related article (e.g. Kotagede page
  confirms the Mentaok → Mataram link from the Ki Ageng Pamanahan page).
