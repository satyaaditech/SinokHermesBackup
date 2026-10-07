# Google Doc from Markdown Upgrade (online-access version)

Established 2026-08-09 (Bussines_plan_coaching session). After building the UPGRADE .md
(foto + ekstrak ID + penjelasan), user asked: "bikin di google doc dengan judul yang sama
dan isi yang sama, untuk mempermudah aku mengakses secara online."

Working recipe: upload the slide photos to Drive (public), build an HTML rendering of the
markdown content, then import that HTML into a Google Doc via the Drive API
(`mimeType: application/vnd.google-apps.document`). Token scope `documents` + `drive`
must both be present (they are for this user). Result: a normal editable Google Doc whose
images are embedded, shareable via link.

## Steps

1. **Reuse the SLIDES data** from the upgrade generator instead of re-transcribing:
   `exec(open('/tmp/gen_upgrade.py').read().replace('build()\n',''), ns)` → `SLIDES` list of
   `(slide_num, title, img_filename, extract_id_text, explanation_text)`.
2. **Upload each image** to the Drive root with `googleapiclient` (NOT raw requests — see
   pitfalls), `permissions().create(role='reader', type='anyone')`, then reference it as:
   `https://drive.google.com/thumbnail?id=<FILE_ID>&sz=w1400` (thumbnail endpoint renders
   reliably inside imported HTML).
3. **Convert markdown → HTML** with a small inline converter. Must handle at least:
   headings (`###`/`####`), `**bold**`, `*italic*`, tables (`| a | b |` + separator row),
   `- ` bullets, `1. ` numbered lists, `> ` blockquotes. See the working converter shape in
   the session script `/tmp/create_gdoc.py` (md_to_html + inline_md functions).
4. **Import** with a multipart Drive upload:
   ```python
   media = MediaFileUpload('/tmp/upgrade_doc.html', mimetype='text/html', resumable=False)
   doc = drive.files().create(
       body={'name': DOC_TITLE, 'mimeType': 'application/vnd.google-apps.document',
             'parents': [FOLDER_ID]},
       media_body=media, fields='id').execute()
   ```
5. **Share**: `drive.permissions().create(fileId=doc_id, body={'role':'reader','type':'anyone'})`
   → link `https://docs.google.com/document/d/<DOC_ID>/edit`.
6. Tell the user: doc is a **snapshot** — if the .md grows more slides later, regenerate.
   Owner (user's account) can edit; anyone-with-link can view.

## Pitfalls (all hit in-session)
- **requests multipart upload fails** with `400 Unsupported content with type:
  application/octet-stream` — the `files=`/`data=` combo sends wrong part headers. ALWAYS use
  `googleapiclient.http.MediaFileUpload` for Drive uploads.
- **f-string expression cannot include a backslash** (SyntaxError) — putting a regex literal
  like `r"^\s*[-•]\s+"` directly inside an f-string expression breaks. Assign the regex to a
  variable first (`BULLET_RE = r'...'`) then use `re.sub(BULLET_RE, ...)` in the f-string.
- Emoji in headings is fine, but keep the HTML `<!DOCTYPE html>` + `<meta charset="utf-8">`
  or the import can mangle special chars.
- Don't embed base64 data-URIs in the HTML — the import won't fetch them. Use Drive URLs.
- The 23-image version lands ~2.5 MB md / ~41 KB HTML; import is quick, no pagination needed.
