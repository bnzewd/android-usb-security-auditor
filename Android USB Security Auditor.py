import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

DEVELOPER = "مقتدى الكعبي"

BG = "#16110a"
SIDEBAR = "#24180d"
CARD = "#2b1f12"
ACCENT = "#f59e0b"
ACCENT2 = "#fb7185"
TEXT = "#fff7ed"
MUTED = "#d6b48a"
OUTPUT_BG = "#120d07"

class AndroidUSBAuditor:
    def __init__(self, root):
        self.root = root
        self.root.title("📱 Android USB Security Auditor")
        self.root.geometry("1020x700")
        self.root.configure(bg=BG)

        self.setup_style()
        self.build_ui()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Main.TFrame", background=BG)
        style.configure("Side.TFrame", background=SIDEBAR)
        style.configure("Card.TFrame", background=CARD)

        style.configure("SideTitle.TLabel", background=SIDEBAR, foreground=TEXT, font=("Segoe UI", 18, "bold"))
        style.configure("SideSub.TLabel", background=SIDEBAR, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("CardLabel.TLabel", background=CARD, foreground=TEXT, font=("Segoe UI", 10, "bold"))

        style.configure("Primary.TButton", background=ACCENT, foreground="black", padding=10, font=("Segoe UI", 10, "bold"))
        style.map("Primary.TButton", background=[("active", "#fbbf24")])

        style.configure("Danger.TButton", background=ACCENT2, foreground="black", padding=10, font=("Segoe UI", 10, "bold"))
        style.map("Danger.TButton", background=[("active", "#fda4af")])

    def build_ui(self):
        container = ttk.Frame(self.root, style="Main.TFrame")
        container.pack(fill="both", expand=True)

        sidebar = ttk.Frame(container, style="Side.TFrame", width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="📱 USB Auditor", style="SideTitle.TLabel").pack(anchor="w", padx=20, pady=(25, 6))
        ttk.Label(sidebar, text=f"Developed by\n{DEVELOPER}", style="SideSub.TLabel").pack(anchor="w", padx=20)

        info_box = tk.Frame(sidebar, bg="#311f0c")
        info_box.pack(fill="x", padx=16, pady=20)

        tk.Label(info_box, text="وظيفة الأداة", bg="#311f0c", fg=TEXT, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(10, 4))
        tk.Label(info_box,
                 text="فحص حالة أمان هاتف Android\nالموصل عبر USB باستخدام ADB\nبشكل معلوماتي وآمن.",
                 bg="#311f0c", fg=MUTED, justify="left", font=("Segoe UI", 10)).pack(anchor="w", padx=12, pady=(0, 10))

        main = ttk.Frame(container, style="Main.TFrame")
        main.pack(side="left", fill="both", expand=True, padx=18, pady=18)

        card = ttk.Frame(main, style="Card.TFrame")
        card.pack(fill="x")

        controls = ttk.Frame(card, style="Card.TFrame")
        controls.pack(fill="x", padx=16, pady=16)

        ttk.Label(controls, text="فحص الجهاز المتصل عبر USB", style="CardLabel.TLabel").grid(row=0, column=0, padx=(0, 12), sticky="w")
        ttk.Button(controls, text="بدء الفحص", command=self.run_audit, style="Primary.TButton").grid(row=0, column=1, padx=6)
        ttk.Button(controls, text="حفظ التقرير", command=self.save_result, style="Danger.TButton").grid(row=0, column=2, padx=6)

        self.output = tk.Text(main, bg=OUTPUT_BG, fg=TEXT, insertbackground="white",
                              relief="flat", font=("Consolas", 11), wrap="word",
                              padx=14, pady=14)
        self.output.pack(fill="both", expand=True, pady=(14, 0))

        self.status_var = tk.StringVar(value="جاهز")
        tk.Label(main, textvariable=self.status_var, bg="#26180b", fg="#f5d0a9",
                 anchor="w", padx=12, pady=9, font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(12, 0))

    def run_cmd(self, cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return "", str(e)

    def adb_shell(self, command):
        return self.run_cmd(f'adb shell {command}')

    def write_output(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def run_audit(self):
        self.status_var.set("جاري فحص الجهاز...")
        self.root.update_idletasks()

        out, err = self.run_cmd("adb devices")
        if "List of devices attached" not in out:
            self.write_output("لم يتم العثور على ADB. تأكد من تثبيته وإضافته إلى PATH.")
            self.status_var.set("ADB غير متوفر.")
            return

        lines = [line for line in out.splitlines()[1:] if line.strip()]
        if not lines:
            self.write_output("لا يوجد هاتف متصل عبر USB أو لم يتم السماح بتصحيح USB.")
            self.status_var.set("لا يوجد جهاز.")
            return

        device_id = lines[0].split()[0]

        model, _ = self.adb_shell("getprop ro.product.model")
        brand, _ = self.adb_shell("getprop ro.product.brand")
        android_ver, _ = self.adb_shell("getprop ro.build.version.release")
        security_patch, _ = self.adb_shell("getprop ro.build.version.security_patch")
        encryption, _ = self.adb_shell("getprop ro.crypto.state")
        debuggable, _ = self.adb_shell("getprop ro.debuggable")
        usb_config, _ = self.adb_shell("getprop sys.usb.config")

        report = []
        report.append("=" * 72)
        report.append("ANDROID USB SECURITY AUDIT")
        report.append("=" * 72)
        report.append(f"Device ID        : {device_id}")
        report.append(f"Brand            : {brand or 'Unknown'}")
        report.append(f"Model            : {model or 'Unknown'}")
        report.append(f"Android Version  : {android_ver or 'Unknown'}")
        report.append(f"Security Patch   : {security_patch or 'Unknown'}")
        report.append(f"Encryption State : {encryption or 'Unknown'}")
        report.append(f"Debuggable       : {debuggable or 'Unknown'}")
        report.append(f"USB Config       : {usb_config or 'Unknown'}")
        report.append("")
        report.append("Assessment")
        report.append("-" * 72)

        if encryption == "encrypted":
            report.append("[OK] الهاتف يبدو مشفرًا.")
        elif encryption:
            report.append(f"[INFO] حالة التشفير: {encryption}")
        else:
            report.append("[INFO] لم يتم تحديد حالة التشفير.")

        if security_patch:
            report.append(f"[INFO] مستوى تحديث الأمان: {security_patch}")
        else:
            report.append("[INFO] لم يتم العثور على مستوى تحديث الأمان.")

        if debuggable == "1":
            report.append("[NOTICE] وضع debuggable مفعّل على النظام.")
        else:
            report.append("[OK] لا يظهر أن النظام debuggable.")

        if "adb" in usb_config:
            report.append("[INFO] ADB مفعل عبر USB.")
        else:
            report.append("[INFO] لم يتم رصد ADB ضمن sys.usb.config.")

        report.append("")
        report.append("General Notes")
        report.append("-" * 72)
        report.append("هذه الأداة تقدم فحصًا معلوماتيًا لحالة الجهاز عبر ADB.")
        report.append("لا تقوم باستغلال أو اختبار هجومي أو تجاوزات أمنية.")
        report.append("")
        report.append(f"Developed by     : {DEVELOPER}")

        self.write_output("\n".join(report))
        self.status_var.set("اكتمل فحص الجهاز.")

    def save_result(self):
        content = self.output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("تنبيه", "لا توجد نتيجة لحفظها.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="android_usb_audit_report.txt"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("تم", "تم حفظ التقرير بنجاح.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AndroidUSBAuditor(root)
    root.mainloop()