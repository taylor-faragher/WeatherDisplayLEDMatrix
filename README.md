# 🌤️ Weather Display LED Matrix Setup Guide
**Platform:** Raspberry Pi OS (Debian Bookworm Lite 64-bit)

This guide provides step‑by‑step instructions for installing and configuring the RGB LED matrix display with the Weather Display Python service.

---

## 🧰 Hardware Requirements
- Raspberry Pi (any model with GPIO support)
- Adafruit RGB Matrix HAT + RTC or compatible
- RGB LED Matrix Panel (32×32 or 64×32)
- Internet connection (Ethernet or Wi‑Fi)

---

## 🧑💻 1. Prepare Your Raspberry Pi
SSH into your Pi, then update and upgrade the system:
```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🔧 2. Install Adafruit RGB Matrix Driver
Download and run the Adafruit installer:
```bash
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh > rgb-matrix.sh
sudo bash rgb-matrix.sh
```

Follow the prompts:

1. Press **Y** and **Enter** to install the RGB matrix software.  
2. Choose **2. Adafruit RGB Matrix HAT + RTC**  
3. Choose **N** for Real‑Time Clock support.  
4. Select a convenient option for matrix quality.  
5. Select **Y** to continue and install.  
6. When prompted, select **Y** to reboot.

After the reboot, SSH back into your Pi.

---

## 🧪 3. Test the Matrix
Confirm the hardware works by running a demo:
```bash
cd ~/rpi-rgb-led-matrix/examples-api-use/
sudo ./demo --led-rows=32 --led-cols=32 --led-gpio-mapping=adafruit-hat -D 0
```
You should see patterns or color animations on the matrix.

---

## 📦 4. Install Dependencies and Weather Display Code
Install Git:
```bash
sudo apt install git -y
git --version
```

Clone the project repository:
```bash
git clone https://github.com/taylor-faragher/WeatherDisplayLEDMatrix.git
```

---

## 🧱 5. Create and Activate a Virtual Environment
```bash
cd
python3 -m venv rgbmatrix
source rgbmatrix/bin/activate
```

---

## ⚙️ 6. Build and Install Python Bindings for the Matrix
Compile and install the Python bindings:
```bash
cd rpi-rgb-led-matrix/
make install-python
```

---

## 🧩 7. Install Python Dependencies
Inside the virtual environment:
```bash
cd
pip install "Pillow<10.0.0" requests
```

> 🧠 We pin Pillow below version 10.0 because the RGB matrix bindings expect an older `unsafe_ptrs` API that was removed in Pillow ≥ 10.

---

## ⚡ 8. Run the Script Manually (First Test)
While still in the venv:
```bash
python /home/ledWeatherMatrix/WeatherDisplayLEDMatrix/code.py
```

If you see weather data appear on your LED panel, everything is working!  
If it warns about “not running as root” or shows flicker, that’s okay for now — we’ll fix that next.

---

## 🔁 9. Run Automatically at Boot (systemd Service)
Create a service file:
```bash
sudo nano /etc/systemd/system/ledweathermatrix.service
```

Paste the following (adjust paths if needed):
```ini
[Unit]
Description=Weather Display LED Matrix
After=network.target

[Service]
User=ledWeatherMatrix
WorkingDirectory=/home/ledWeatherMatrix/WeatherDisplayLEDMatrix
ExecStart=/home/ledWeatherMatrix/rgbmatrix/bin/python3 /home/ledWeatherMatrix/WeatherDisplayLEDMatrix/code.py >> /home/ledWeatherMatrix/WeatherDisplayLEDMatrix/ledmatrix.log 2>&1
Restart=on-failure
Environment=PYTHONUNBUFFERED=1
AmbientCapabilities=CAP_SYS_NICE
ExecStartPre=/bin/sleep 10

[Install]
WantedBy=multi-user.target
```

Reload and enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ledweathermatrix.service
sudo systemctl start ledweathermatrix.service
```

Check status:
```bash
sudo systemctl status ledweathermatrix.service
```

> The `ExecStartPre=/bin/sleep 10` ensures the service waits briefly for Wi‑Fi or networking before fetching weather data.

---

## 🧾 10. Troubleshooting

### View recent logs
```bash
journalctl -u ledweathermatrix.service -n 30 --no-pager
```

### Common Issues

| Symptom | Cause | Fix |
|----------|--------|-----|
| `ModuleNotFoundError: No module named 'rgbmatrix'` | Script not using virtual environment | Ensure service points to `/home/ledWeatherMatrix/rgbmatrix/bin/python3` |
| `AttributeError: 'ImagingCore' object has no attribute 'unsafe_ptrs'` | Pillow version too new | Run `pip install "Pillow<10.0.0"` |
| Color flicker or timing warnings | Process lacks real‑time priority | Add `AmbientCapabilities=CAP_SYS_NICE` |
| Weather fetch fails on boot | Service starts before network | Keep `ExecStartPre=/bin/sleep 10` |

---

## ✅ 11. Verify Persistent Startup
Reboot the Pi:
```bash
sudo reboot
```

After reboot:
```bash
sudo systemctl status ledweathermatrix.service
```
You should see **“active (running)”**, and the LED matrix will automatically display the weather.

---

## 🧩 Optional Optimization
To improve refresh timing, edit `/boot/cmdline.txt` and append: