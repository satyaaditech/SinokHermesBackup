# Google Slides API Disabled Workaround: pptx to Google Slides Conversion & Update

## Problem
When calling the Google Slides API directly, you may encounter a `403 Forbidden` error indicating the Slides API is disabled in the developer console:
`HttpError 403 when requesting https://slides.googleapis.com/v1/... returned "Google Slides API has not been used in project ... or it is disabled."`

Typically, you cannot enable the API because you lack access to the user's Google Cloud Console.

## Solution
Rather than failing or requesting console access, use Google Drive API's native conversion capabilities:
1. Generate the presentation locally as a PowerPoint (`.pptx`) file using the `python-pptx` library.
2. Upload the `.pptx` file via the Google Drive API, setting the target MIME type to `'application/vnd.google-apps.presentation'`. Drive will automatically convert it into a native Google Slide.
3. For subsequent updates, rewrite the local `.pptx` file and execute an in-place update using `drive_service.files().update()` to overwrite the file contents **while retaining the same document ID and URL**.

## Step-by-Step Implementation

### 1. Install standard PPTX engine
```bash
pip install python-pptx
```

### 2. Generate PPTX Locally (Python script)
Set the aspect ratio to widescreen (16:9) and define reusable styles (background fills, font sizes, margins). Keep in-line elements positioned properly to prevent overlapping:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# Widescreen PPTX Dimensions: 13.33 x 7.5 inches
prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

# Formatting constants
bg_color = RGBColor(250, 250, 250)      # Clean Off-white
title_color = RGBColor(13, 40, 71)      # Dark Blue
body_color = RGBColor(40, 40, 40)       # Charcoal
accent_color = RGBColor(46, 125, 50)    # Green Accent

slide_layout = prs.slide_layouts[6]     # Use a blank layout for custom absolute placement
slide = prs.slides.add_slide(slide_layout)

# Apply Background color
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = bg_color

# Add logo/picture shape
logo_path = "/path/to/logo.png"
slide.shapes.add_picture(logo_path, Inches(1.0), Inches(1.0), Inches(1.5), Inches(1.5))

# Add main textbox
text_box = slide.shapes.add_textbox(Inches(3.0), Inches(1.0), Inches(9.33), Inches(5.5))
tf = text_box.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0)

# Add Paragraph
p = tf.paragraphs[0]
p.text = "Inovasi Slide Produk"
p.font.name = "Arial"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = title_color
p.space_after = Pt(14)

p2 = tf.add_paragraph()
p2.text = "• Detail poin utama 1"
p2.font.name = "Arial"
p2.font.size = Pt(18)
p2.font.color.rgb = body_color

# Save PowerPoint file
prs.save("output_deck.pptx")
```

### 3. Convert while Uploading to Drive (Drive API v3)
Create the file on Google Drive, specifying the Google Slides MIME type. Google Drive automatically performs the translation:

```python
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

# Build Drive client
drive_service = build('drive', 'v3', credentials=creds)

file_metadata = {
    'name': 'Title of the Presentation',
    'mimeType': 'application/vnd.google-apps.presentation'
}
media = MediaFileUpload(
    'output_deck.pptx', 
    mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
    resumable=True
)

file_obj = drive_service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id'
).execute()

slide_id = file_obj.get('id')
slide_url = f"https://docs.google.com/presentation/d/{slide_id}/edit"
```

### 4. Share Document
Provide public read access to ensure the user can view it on mobile devices without friction:

```python
drive_service.permissions().create(
    fileId=slide_id,
    body={'role': 'reader', 'type': 'anyone'}
).execute()
```

### 5. In-Place Updates
To apply layout fixes, content changes, or updates requested by the user, modify the local PPTX file and issue a Drive `update` request. This updates the underlying Slides presentation without creating a new file or breaking the sharing URL:

```python
media = MediaFileUpload(
    'modified_deck.pptx', 
    mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
    resumable=True
)

drive_service.files().update(
    fileId=slide_id,
    body={'name': 'Title of the Presentation (Updates)'},
    media_body=media
).execute()
```
