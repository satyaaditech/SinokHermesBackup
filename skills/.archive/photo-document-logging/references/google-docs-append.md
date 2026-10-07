# Logging & Appending Photo Transcriptions to Google Docs

This document outlines the workflow and API styling requirements when the user requests a photo log or slide transcription to be built progressively inside a Google Document instead of a plain text/markdown file.

## 1. User Style & Format Preferences

* **No Raw Markdown Characters**: Under no circumstances should raw markdown characters (such as `**`, `*`, `###`, or divider lines like `----`) be written directly into the body of the Google Doc.
* **Native Styling**: Use the Google Docs API to format the text blocks natively:
  - **Headings**: Use `updateParagraphStyle` to set paragraph styles like `HEADING_1` or `HEADING_2`.
  - **Bolding & Font Sizes**: Use `updateTextStyle` to apply bolding and adjust font size/color for key titles, metrics, or totals.
  - **Layout & Structure**: Use capitalization, clean indentation, and well-designed bullet points for readability.

## 2. API Implementation & Index-Shifting Workaround

When inserting text and applying styles using `documents.batchUpdate`, multiple sequential requests inside a single batch run into the **index-shifting problem** (inserting text changes the indices of subsequent edits).

### Index-Tracking Solution

To safely insert and style multiple paragraphs in a single API call, calculate and track the cumulative `current_index` offsets sequentially:

```python
# retrieve current end index of the document
doc = docs_service.documents().get(documentId=DOC_ID).execute()
content_list = doc.get('body', {}).get('content', [])
current_index = content_list[-1]['endIndex'] - 1 if content_list else 1

requests = []
blocks = [
    {"text": "SLIDE NAME\n", "style": "HEADING_1"},
    {"text": "Key info 1: value 1\n", "style": "BULLET"},
    {"text": "Key info 2: value 2\n", "style": "NORMAL"},
]

for b in blocks:
    text_len = len(b['text'])
    start = current_index
    end = current_index + text_len
    
    # 1. Insert Text Block
    requests.append({
        'insertText': {
            'location': {'index': current_index},
            'text': b['text']
        }
    })
    
    # 2. Style Paragraph (Heading vs Normal)
    p_style = {'namedStyleType': 'HEADING_1' if b['style'] == 'HEADING_1' else 'NORMAL_TEXT'}
    requests.append({
        'updateParagraphStyle': {
            'range': {'startIndex': start, 'endIndex': end},
            'paragraphStyle': p_style,
            'fields': 'namedStyleType'
        }
    })
    
    # 3. Apply Custom Styles (Bolding)
    if b['style'] == 'HEADING_1':
        t_style = {
            'bold': True,
            'fontSize': {'magnitude': 13, 'unit': 'PT'},
            'foregroundColor': {'color': {'rgbColor': {'blue': 0.6, 'green': 0.1, 'red': 0.2}}}
        }
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end},
                'textStyle': t_style,
                'fields': '*'
            }
        })
        
    # Advance the index pointer to the end of the newly inserted block
    current_index = end

# Execute batch
docs_service.documents().batchUpdate(documentId=DOC_ID, body={'requests': requests}).execute()
```

## 3. Pitfalls & Anti-Patterns

* **Avoid double-newline offset bugs**: Always ensure the character count of each block (`len(b['text'])`) matches the exact string length being inserted, including all newlines (`\n`).
* **Clear Document Command**: If the document gets corrupted with raw markdown syntax, it is best to clear the document completely using a `deleteContentRange` request from index 1 to `endIndex - 1` and write the structured text clean.
