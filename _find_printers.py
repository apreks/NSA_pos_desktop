"""Find USB printers on Windows using WMI + registry."""
import subprocess, re

print("=" * 60)
print("  USB PRINTER / POS DEVICE SCANNER")
print("=" * 60)

# Method 1: Windows printers (winspool)
print("\n[1] Windows Installed Printers:")
try:
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "Get-Printer | Select-Object Name, DriverName, PortName | Format-List"],
        capture_output=True, text=True, timeout=10
    )
    print(r.stdout.strip() if r.stdout.strip() else "  (none found)")
except Exception as e:
    print(f"  Error: {e}")

# Method 2: USB devices with VID/PID
print("\n[2] USB Devices with VID & PID (from PnP):")
try:
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         r"Get-PnpDevice -Class Printer,USB -Status OK -ErrorAction SilentlyContinue "
         r"| Select-Object InstanceId, FriendlyName, Class "
         r"| Format-List"],
        capture_output=True, text=True, timeout=10
    )
    output = r.stdout.strip()
    if output:
        print(output)
        # Extract VID/PID pairs
        vids = re.findall(r'VID_([0-9A-Fa-f]{4})&PID_([0-9A-Fa-f]{4})', output)
        if vids:
            print("\n  Detected VID/PID pairs:")
            for vid, pid in set(vids):
                print(f"    VID=0x{vid}  PID=0x{pid}")
    else:
        print("  (none found)")
except Exception as e:
    print(f"  Error: {e}")

# Method 3: All USB devices (broader scan)
print("\n[3] All USB Devices (broader PnP scan):")
try:
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         r"Get-PnpDevice -Status OK | Where-Object { $_.InstanceId -match 'USB\\VID' } "
         r"| Select-Object InstanceId, FriendlyName | Format-Table -AutoSize"],
        capture_output=True, text=True, timeout=10
    )
    output = r.stdout.strip()
    print(output if output else "  (none found)")
    vids = re.findall(r'VID_([0-9A-Fa-f]{4})&PID_([0-9A-Fa-f]{4})', output)
    if vids:
        KNOWN = {"04B8": "Epson", "0519": "Star Micronics", "0DD4": "Bixolon"}
        print("\n  Receipt-Printer candidates:")
        for vid, pid in set(vids):
            brand = KNOWN.get(vid.upper(), "")
            if brand:
                print(f"    >>> {brand}: VID=0x{vid} PID=0x{pid}  <<<")
except Exception as e:
    print(f"  Error: {e}")
