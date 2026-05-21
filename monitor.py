import psutil
import time
import os

def bar(percent):
    blocks = int(percent / 10)
    return "█" * blocks + "-" * (10 - blocks)

def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    return f"{hours}h {minutes}m"

print("Booting System Monitor...")
time.sleep(1)
print("Loading metrics...")
time.sleep(1)
print("System Online\n")

while True:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    uptime = get_uptime()

    os.system("cls" if os.name == "nt" else "clear")

    print("====================================")
    print("     SYSTEM HEALTH MONITOR")
    print("====================================\n")

    print(f"CPU Usage   : {cpu}%  | {bar(cpu)}")
    print(f"RAM Usage   : {ram}%  | {bar(ram)}")
    print(f"Disk Usage  : {disk}% | {bar(disk)}")
    print(f"Uptime      : {uptime}")

    print("\n------------------------------------")

    if cpu > 80:
        print("⚠ WARNING: High CPU usage")
    if ram > 85:
        print("⚠ WARNING: High memory usage")
    if disk > 90:
        print("⚠ WARNING: Low disk space")

    print("------------------------------------")

    time.sleep(1)