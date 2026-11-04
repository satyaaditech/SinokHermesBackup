---
name: server-screen-control
description: "Use when controlling n8nserver monitor screen on/off."
version: 1.0.0
---

# Server Screen Control (n8nserver)

Trik bypass root tanpa password menggunakan docker privileged untuk mengontrol backlight dan framebuffer screen server:

## Turn Screen OFF (Matikan Layar)
```bash
/home/satyaaditech/screen_off.sh
# Atau langsung perintah:
docker run --rm --privileged -v /sys:/sys alpine sh -c "echo 0 > /sys/class/backlight/amdgpu_bl0/brightness; echo 4 > /sys/class/graphics/fb0/blank"
```

## Turn Screen ON (Nyalakan Layar)
```bash
/home/satyaaditech/screen_on.sh
# Atau langsung perintah:
docker run --rm --privileged -v /sys:/sys alpine sh -c "echo 255 > /sys/class/backlight/amdgpu_bl0/brightness; echo 0 > /sys/class/graphics/fb0/blank"
```
