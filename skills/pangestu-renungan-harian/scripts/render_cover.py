import sys
import os
from PIL import Image, ImageDraw, ImageFont

def draw_gradient_background(draw, width, height, color1, color2):
    for y in range(height):
        factor = y / height
        r = int(color1[0] + (color2[0] - color1[0]) * factor)
        g = int(color1[1] + (color2[1] - color1[1]) * factor)
        b = int(color1[2] + (color2[2] - color1[2]) * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_jawani_border(draw, width, height, margin, color):
    # 1. Gambar Motif Kawung Geometris Jawi ing 4 Pojok Bingkai (Mboten Rame)
    corners = [
        (margin + 24, margin + 24),           # Kiri Atas
        (width - margin - 24, margin + 24),   # Kanan Atas
        (margin + 24, height - margin - 24),  # Kiri Bawah
        (width - margin - 24, height - margin - 24) # Kanan Bawah
    ]
    
    r = 16 # Radius kelopak kawung
    for cx, cy in corners:
        # Elips 4 penjuru mbentuk kembang kawung
        draw.ellipse([cx - r, cy - 2*r, cx + r, cy], outline=color, width=2) # Atas
        draw.ellipse([cx - r, cy, cx + r, cy + 2*r], outline=color, width=2) # Bawah
        draw.ellipse([cx - 2*r, cy - r, cx, cy + r], outline=color, width=2) # Kiri
        draw.ellipse([cx, cy - r, cx + 2*r, cy + r], outline=color, width=2) # Kanan
        # Sentral kancing kembang
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)
        
    # 2. Bingkai Garis Ganda njawi & njero ingkang medhot sacara manis ing pojokan kawung
    gap = 85 # Jarak saking pojok supados mboten tabrakan kaliyan motif kawung
    
    # Bingkai Njawi (Outer Border) Tebal 3px
    draw.line([margin + gap, margin, width - margin - gap, margin], fill=color, width=3) # Atas
    draw.line([margin + gap, height - margin, width - margin - gap, height - margin], fill=color, width=3) # Bawah
    draw.line([margin, margin + gap, margin, height - margin - gap], fill=color, width=3) # Kiri
    draw.line([width - margin, margin + gap, width - margin, height - margin - gap], fill=color, width=3) # Kanan
    
    # Bingkai Njero (Inner Border) Tebal 1px, offset 12px
    offset = 12
    draw.line([margin + gap, margin + offset, width - margin - gap, margin + offset], fill=color, width=1) # Upper inner
    draw.line([margin + gap, height - margin - offset, width - margin - gap, height - margin - offset], fill=color, width=1) # Lower inner
    draw.line([margin + offset, margin + gap, margin + offset, height - margin - gap], fill=color, width=1) # Left inner
    draw.line([width - margin - offset, margin + gap, width - margin - offset, height - margin - gap], fill=color, width=1) # Right inner

def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_text = " ".join(current_line)
        bbox = font.getbbox(line_text)
        width = bbox[2] - bbox[0]
        
        if width > max_width:
            if len(current_line) == 1:
                lines.append(line_text)
                current_line = []
            else:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
                
    if current_line:
        lines.append(" ".join(current_line))
        
    return lines

def create_cover(title, quote, date_str, output_path):
    width, height = 1200, 1200
    img = Image.new("RGB", (width, height), color=(252, 251, 249))
    draw = ImageDraw.Draw(img)
    
    # 1. Latar Belakang Gradasi Terang (Krem Hangat ke Putih Gading)
    color_start = (253, 252, 250)
    color_end = (245, 242, 235)
    draw_gradient_background(draw, width, height, color_start, color_end)
    
    # 2. Bingkai Hitam Jawani (Polan Motif Kawung ing Pojokan)
    margin = 50
    black_color = (0, 0, 0)
    draw_jawani_border(draw, width, height, margin, black_color)
    
    # 3. Font Setup
    font_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_serif_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    font_serif_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    font_sans_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    
    header_font = ImageFont.truetype(font_bold_path, 36)
    title_font = ImageFont.truetype(font_serif_bold_path, 62) # Font Raksasa kagem Tamel
    quote_font = ImageFont.truetype(font_serif_path, 28)
    footer_font = ImageFont.truetype(font_sans_path, 28)
    
    # 4. Gambar Teks Header
    header_text = "RENUNGAN PENYISWAAN"
    h_bbox = header_font.getbbox(header_text)
    h_w = h_bbox[2] - h_bbox[0]
    draw.text(((width - h_w)/2, 160), header_text, fill=black_color, font=header_font)
    
    # Garis Penghias Hitam ing sangadhap Header
    line_w = 120
    draw.line([((width - line_w)/2, 215), ((width + line_w)/2, 215)], fill=black_color, width=2)
    
    # 5. Gambar Judul Renungan (Tengah)
    max_text_width = width - (margin * 4) # 1000px
    wrapped_title = wrap_text(title, title_font, max_text_width)
    
    title_y_start = 380
    line_height = 80
    for i, line in enumerate(wrapped_title):
        t_bbox = title_font.getbbox(line)
        t_w = t_bbox[2] - t_bbox[0]
        draw.text(((width - t_w)/2, title_y_start + (i * line_height)), line, fill=black_color, font=title_font)
        
    # Titik tengah pembatas hitam
    dot_y = title_y_start + (len(wrapped_title) * line_height) + 40
    draw.ellipse([(width/2 - 5, dot_y - 5), (width/2 + 5, dot_y + 5)], fill=black_color)
    
    # 6. Gambar Kutipan Kunci / Sabda
    quote_text = f'"{quote}"'
    wrapped_quote = wrap_text(quote_text, quote_font, max_text_width)
    
    quote_y_start = dot_y + 50
    q_line_height = 44
    for i, line in enumerate(wrapped_quote):
        q_bbox = quote_font.getbbox(line)
        q_w = q_bbox[2] - q_bbox[0]
        draw.text(((width - q_w)/2, quote_y_start + (i * q_line_height)), line, fill=black_color, font=quote_font)
        
    # 7. Gambar Teks Footer
    footer_text = f"{date_str}"
    f_bbox = footer_font.getbbox(footer_text)
    f_w = f_bbox[2] - f_bbox[0]
    draw.text(((width - f_w)/2, 1000), footer_text, fill=black_color, font=footer_font)
    
    footer_sub = "Menuju Katentreman Batin"
    fs_bbox = footer_font.getbbox(footer_sub)
    fs_w = fs_bbox[2] - fs_bbox[0]
    draw.text(((width - fs_w)/2, 1040), footer_sub, fill=black_color, font=footer_font)
    
    # Simpan Gambar
    img.save(output_path, "PNG")
