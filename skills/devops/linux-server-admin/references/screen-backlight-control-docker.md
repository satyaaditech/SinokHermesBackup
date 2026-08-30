# Console Screen and Backlight Poweroff via Privileged Docker

When managing a Linux server console screen (e.g. an AMDGPU-based server) without having full sudo privileges, a privileged Docker container can be used to bypass the root password requirement and write directly to `/sys` files.

## Turning Screen OFF

Run the following command or place it in a script (e.g., `~/screen_off.sh`):

```bash
docker run --rm --privileged -v /sys:/sys alpine sh -c "echo 0 > /sys/class/backlight/amdgpu_bl0/brightness; echo 4 > /sys/class/graphics/fb0/blank"
```

## Explanation
- `--privileged` and `-v /sys:/sys`: Grants the container access to the host's sysfs file system.
- `/sys/class/backlight/amdgpu_bl0/brightness`: Controls the screen backlight (setting to `0` turns it off). Note that the path might vary depending on the GPU (e.g. `intel_backlight` vs `amdgpu_bl0`).
- `/sys/class/graphics/fb0/blank`: Controls the framebuffer blanking (setting to `4` powers down/blanks the display).
