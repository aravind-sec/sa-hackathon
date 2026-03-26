import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import threading
import time
from datetime import datetime
import os

BASE_URL = "http://127.0.0.1:5000"

class ModernButton(tk.Canvas):
    """Custom animated button with gradient and hover effects"""
    def __init__(self, parent, text, command, bg_color, hover_color, width=140, height=80):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, relief=tk.FLAT)
        
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.width = width
        self.height = height
        self.current_color = bg_color
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
        self.config(cursor="hand2")
        self.draw()
    
    def draw(self):
        self.delete("all")
        self.create_rounded_rect(0, 0, self.width, self.height, radius=8, fill=self.current_color)
        self.create_text(self.width // 2, self.height // 2, text=self.text, fill="white", font=("Segoe UI", 9, "bold"), justify=tk.CENTER)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        kwargs.pop('outline', None)
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def on_enter(self, event):
        self.current_color = self.hover_color
        self.draw()
    
    def on_leave(self, event):
        self.current_color = self.bg_color
        self.draw()
    
    def on_click(self, event):
        if self.command:
            self.command()

class AttackSimulatorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ API Shield - Attack Simulator Pro")
        self.root.state('zoomed')  # Full screen on Windows
        
        # Premium color palette
        self.colors = {
            'bg_primary': '#0d1117',
            'bg_secondary': '#161b22',
            'bg_tertiary': '#1c2128',
            'accent_blue': '#58a6ff',
            'accent_red': '#f85149',
            'accent_yellow': '#ffd500',
            'accent_green': '#3fb950',
            'accent_orange': '#fb8500',
            'text_primary': '#e6edf3',
            'text_secondary': '#8b949e',
            'border': '#30363d',
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        self.attacking = False
        self.total_attacks = 0
        self.successful_attacks = 0
        
        self.setup_ui()
        self.add_styles()
    
    def add_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TCombobox',
            fieldbackground=self.colors['bg_tertiary'],
            background=self.colors['bg_secondary'],
            foreground=self.colors['text_primary'],
            borderwidth=1
        )
    
    def setup_ui(self):
        # ===== MAIN CONTAINER =====
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # ===== TOP SECTION (Header + Stats) =====
        top_section = tk.Frame(main_container, bg=self.colors['bg_primary'])
        top_section.pack(fill=tk.X, padx=0, pady=0)
        
        self.create_header(top_section)
        self.create_stats(top_section)
        
        # ===== MIDDLE SECTION (Controls + Buttons) =====
        middle_section = tk.Frame(main_container, bg=self.colors['bg_primary'])
        middle_section.pack(fill=tk.X, padx=20, pady=20)
        
        self.create_controls(middle_section)
        self.create_attack_buttons(middle_section)
        
        # ===== BOTTOM SECTION (Log) =====
        bottom_section = tk.Frame(main_container, bg=self.colors['bg_primary'])
        bottom_section.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.create_log_section(bottom_section)
        
        # ===== FOOTER =====
        self.create_footer(main_container)
    
    def create_header(self, parent):
        header = tk.Frame(parent, bg=self.colors['bg_secondary'], height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Left side
        left = tk.Frame(header, bg=self.colors['bg_secondary'])
        left.pack(side=tk.LEFT, padx=30, pady=16, fill=tk.BOTH, expand=True)
        
        title = tk.Label(
            left,
            text="🛡️ Attack Simulator Pro",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title.pack(anchor=tk.W)
        
        subtitle = tk.Label(
            left,
            text="Professional API Security Testing Tool",
            font=("Segoe UI", 11),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        subtitle.pack(anchor=tk.W, pady=(2, 0))
        
        # Right side - target info
        right = tk.Frame(header, bg=self.colors['bg_secondary'])
        right.pack(side=tk.RIGHT, padx=30, pady=16)
        
        target_label = tk.Label(
            right,
            text="Target API",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        target_label.pack()
        
        target_value = tk.Label(
            right,
            text="http://localhost:5000",
            font=("Courier New", 11, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_blue']
        )
        target_value.pack()
    
    def create_stats(self, parent):
        stats_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        stats_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        # Stats container
        stats_container = tk.Frame(stats_frame, bg=self.colors['bg_secondary'])
        stats_container.pack(fill=tk.X)
        
        stats_inner = tk.Frame(stats_container, bg=self.colors['bg_secondary'])
        stats_inner.pack(fill=tk.X, padx=20, pady=12)
        
        # Stat 1: Total Attacks
        stat1_frame = tk.Frame(stats_inner, bg=self.colors['bg_secondary'])
        stat1_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            stat1_frame,
            text="Total Attacks",
            font=("Segoe UI", 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        ).pack()
        
        self.total_attacks_label = tk.Label(
            stat1_frame,
            text="0",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_blue']
        )
        self.total_attacks_label.pack()
        
        # Stat 2: Successful
        stat2_frame = tk.Frame(stats_inner, bg=self.colors['bg_secondary'])
        stat2_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            stat2_frame,
            text="Successful",
            font=("Segoe UI", 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        ).pack()
        
        self.successful_label = tk.Label(
            stat2_frame,
            text="0",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_green']
        )
        self.successful_label.pack()
        
        # Stat 3: Success Rate
        stat3_frame = tk.Frame(stats_inner, bg=self.colors['bg_secondary'])
        stat3_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            stat3_frame,
            text="Success Rate",
            font=("Segoe UI", 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        ).pack()
        
        self.success_rate_label = tk.Label(
            stat3_frame,
            text="0%",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_yellow']
        )
        self.success_rate_label.pack()
        
        # Stat 4: Status
        stat4_frame = tk.Frame(stats_inner, bg=self.colors['bg_secondary'])
        stat4_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            stat4_frame,
            text="Status",
            font=("Segoe UI", 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        ).pack()
        
        self.status_indicator = tk.Label(
            stat4_frame,
            text="● Ready",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_green']
        )
        self.status_indicator.pack()
    
    def create_controls(self, parent):
        controls_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title = tk.Label(
            controls_frame,
            text="⚙️ Configuration",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Control box
        box = tk.Frame(controls_frame, bg=self.colors['bg_secondary'], relief=tk.FLAT)
        box.pack(fill=tk.X)
        
        inner = tk.Frame(box, bg=self.colors['bg_secondary'])
        inner.pack(fill=tk.X, padx=20, pady=12)
        
        # Intensity selector
        intensity_label = tk.Label(
            inner,
            text="Attack Intensity:",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        intensity_label.pack(side=tk.LEFT)
        
        self.intensity_var = tk.StringVar(value="Normal (20 req)")
        intensity_options = ttk.Combobox(
            inner,
            textvariable=self.intensity_var,
            values=["Light (5 req)", "Normal (20 req)", "Heavy (100 req)"],
            state="readonly",
            width=20
        )
        intensity_options.pack(side=tk.LEFT, padx=15)
        
        # Info label
        info = tk.Label(
            inner,
            text="Select attack intensity level",
            font=("Segoe UI", 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        info.pack(side=tk.LEFT, padx=15)
    
    def create_attack_buttons(self, parent):
        buttons_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        buttons_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title = tk.Label(
            buttons_frame,
            text="🎯 Attack Types",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Button grid
        buttons_container = tk.Frame(buttons_frame, bg=self.colors['bg_primary'])
        buttons_container.pack(fill=tk.X)
        
        # Row 1
        row1 = tk.Frame(buttons_container, bg=self.colors['bg_primary'])
        row1.pack(fill=tk.X, pady=8)
        
        btn1 = ModernButton(
            row1,
            "🔐 Credential\nStuffing",
            lambda: self.run_attack(self.credential_stuffing),
            self.colors['accent_red'],
            '#ff6b5b',
            width=180,
            height=90
        )
        btn1.pack(side=tk.LEFT, padx=10)
        
        btn2 = ModernButton(
            row1,
            "⚡ Rate\nAbuse",
            lambda: self.run_attack(self.rate_abuse),
            self.colors['accent_yellow'],
            '#ffe033',
            width=180,
            height=90
        )
        btn2.pack(side=tk.LEFT, padx=10)
        
        btn3 = ModernButton(
            row1,
            "🤖 Bot\nActivity",
            lambda: self.run_attack(self.bot_activity),
            self.colors['accent_blue'],
            '#79c0ff',
            width=180,
            height=90
        )
        btn3.pack(side=tk.LEFT, padx=10)
        
        btn4 = ModernButton(
            row1,
            "🚨 Suspicious\nAccess",
            lambda: self.run_attack(self.suspicious_access),
            self.colors['accent_orange'],
            '#ffa94d',
            width=180,
            height=90
        )
        btn4.pack(side=tk.LEFT, padx=10)
    
    def create_log_section(self, parent):
        log_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(
            log_frame,
            text="📊 Attack Log",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Log output
        self.output = scrolledtext.ScrolledText(
            log_frame,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_blue'],
            font=("Courier New", 10),
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightcolor=self.colors['border'],
            highlightbackground=self.colors['border']
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags
        self.output.tag_configure("success", foreground=self.colors['accent_green'])
        self.output.tag_configure("error", foreground=self.colors['accent_red'])
        self.output.tag_configure("warning", foreground=self.colors['accent_yellow'])
        self.output.tag_configure("info", foreground=self.colors['text_secondary'])
        self.output.tag_configure("header", foreground=self.colors['accent_blue'], font=("Courier New", 10, "bold"))
    
    def create_footer(self, parent):
        footer = tk.Frame(parent, bg=self.colors['bg_secondary'], height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        footer_text = tk.Label(
            footer,
            text="API Shield v1.0 • Enterprise Security Testing • " + datetime.now().strftime("%Y-%m-%d"),
            font=("Segoe UI", 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        footer_text.pack(pady=10)
    
    def log(self, message, tag="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.output.insert(tk.END, log_message, tag)
        self.output.see(tk.END)
        self.root.update()
    
    def update_stats(self):
        self.total_attacks_label.config(text=str(self.total_attacks))
        self.successful_label.config(text=str(self.successful_attacks))
        
        if self.total_attacks > 0:
            rate = int((self.successful_attacks / self.total_attacks) * 100)
        else:
            rate = 0
        self.success_rate_label.config(text=f"{rate}%")
    
    def get_attack_count(self):
        intensity = self.intensity_var.get()
        if "Light" in intensity:
            return 5
        elif "Heavy" in intensity:
            return 100
        else:
            return 20
    
    def credential_stuffing(self):
        count = self.get_attack_count()
        self.log(f"🔐 Credential Stuffing Attack ({count} attempts)", "header")
        self.log(f"Target: {BASE_URL}/login", "info")
        
        for i in range(count):
            try:
                response = requests.post(f"{BASE_URL}/login", json={
                    "username": "admin",
                    "password": f"wrong{i}"
                }, timeout=5)
                self.total_attacks += 1
                if response.status_code == 401:
                    self.successful_attacks += 1
                self.log(f"  ├─ Attempt {i+1}/{count} ✓", "success")
            except Exception as e:
                self.total_attacks += 1
                self.log(f"  ├─ Attempt {i+1}/{count} ✗ {str(e)}", "error")
            self.update_stats()
            time.sleep(0.08)
        
        self.log(f"✓ Attack complete\n", "success")
    
    def rate_abuse(self):
        count = self.get_attack_count()
        self.log(f"⚡ Rate Abuse Attack ({count} requests)", "header")
        self.log(f"Target: {BASE_URL}/api/data", "info")
        
        for i in range(count):
            try:
                response = requests.get(f"{BASE_URL}/api/data", timeout=5)
                self.total_attacks += 1
                if response.status_code == 200:
                    self.successful_attacks += 1
                self.log(f"  ├─ Request {i+1}/{count} ✓", "success")
            except Exception as e:
                self.total_attacks += 1
                self.log(f"  ├─ Request {i+1}/{count} ✗ {str(e)}", "error")
            self.update_stats()
            time.sleep(0.04)
        
        self.log(f"✓ Attack complete\n", "success")
    
    def bot_activity(self):
        count = self.get_attack_count()
        self.log(f"🤖 Bot Activity Attack ({count} rapid requests)", "header")
        self.log(f"Target: {BASE_URL}/api/data", "info")
        
        for i in range(count):
            try:
                response = requests.get(f"{BASE_URL}/api/data", timeout=5)
                self.total_attacks += 1
                if response.status_code == 200:
                    self.successful_attacks += 1
                self.log(f"  ├─ Bot request {i+1}/{count} ✓", "success")
            except Exception as e:
                self.total_attacks += 1
                self.log(f"  ├─ Bot request {i+1}/{count} ✗ {str(e)}", "error")
            self.update_stats()
            time.sleep(0.015)
        
        self.log(f"✓ Attack complete\n", "success")
    
    def suspicious_access(self):
        count = self.get_attack_count()
        self.log(f"🚨 Suspicious Endpoint Access ({count} attempts)", "header")
        self.log(f"Target: {BASE_URL}/admin", "info")
        
        for i in range(count):
            try:
                response = requests.get(f"{BASE_URL}/admin", timeout=5)
                self.total_attacks += 1
                if response.status_code == 200:
                    self.successful_attacks += 1
                self.log(f"  ├─ Access attempt {i+1}/{count} ✓", "success")
            except Exception as e:
                self.total_attacks += 1
                self.log(f"  ├─ Access attempt {i+1}/{count} ✗ {str(e)}", "error")
            self.update_stats()
            time.sleep(0.1)
        
        self.log(f"✓ Attack complete\n", "success")
    
    def run_attack(self, attack_func):
        if self.attacking:
            messagebox.showwarning("Attack Running", "Please wait for current attack to finish")
            return
        
        self.attacking = True
        self.status_indicator.config(text="● Running", fg=self.colors['accent_red'])
        
        def execute():
            try:
                attack_func()
            except Exception as e:
                self.log(f"❌ Attack failed: {str(e)}", "error")
            finally:
                self.attacking = False
                self.status_indicator.config(text="● Ready", fg=self.colors['accent_green'])
                self.log("─" * 100 + "\n", "info")
        
        thread = threading.Thread(target=execute, daemon=True)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttackSimulatorPro(root)
    root.mainloop()