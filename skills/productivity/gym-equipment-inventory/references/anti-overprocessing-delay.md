# Anti Over-Processing Delay & Media Thumbnail Best Practices

## 1. Randomized Human-like Jitter (Anti Over-Processing)
When batch uploading photos to Google Drive and immediately inserting rows into Google Sheets, automated burst requests can trigger Google API rate limits (HTTP 429) or suspicious automated activity flags.

### Best Practice:
- Apply randomized sleep intervals between consecutive item processing:
  - For small batches (< 5 items): 5 to 15 seconds random jitter.
  - For larger batches or sustained ingestion: 45 to 110 seconds random jitter (`random.randint(45, 110)`).
- Process sequentially (item-by-item queue) rather than concurrently hammering the API with multi-threaded bursts.

## 2. In-Cell Thumbnail Formula (`=IMAGE`)
To render image previews directly inside Google Sheets cells on desktop and mobile:

```excel
=IMAGE("https://drive.google.com/thumbnail?id=FILE_ID&sz=w200", 1)
```

### Critical Prerequisite:
Google Sheets backend servers fetch the image URL independently. If the file is strictly private to the authenticated user, `=IMAGE` will display a broken blank image icon.
Always grant `anyone` reader permission on the uploaded photo:
```python
drive.permissions().create(
    fileId=file_id,
    body={"role": "reader", "type": "anyone"}
).execute()
```

## 3. Formatting for Mobile Readability
- Set data row height to ~75px (`dimension: ROWS, pixelSize: 75`).
- Set vertical alignment to `MIDDLE`.
- Set wrap strategy to `WRAP` on descriptive columns (Nama Alat, Target Otot, Variasi, Catatan).
- Keep header row frozen (`frozenRowCount: 1`) with dark contrast background.
