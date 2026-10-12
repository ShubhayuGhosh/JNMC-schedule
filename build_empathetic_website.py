import base64
import os

BASE_DIR = "/Users/shubhayu/Documents/antigravity/splendid-raman"
gen_ics_path = os.path.join(BASE_DIR, "downloads", "MBBS_Phase_III_Schedule.ics")
batch_b_ics_path = os.path.join(BASE_DIR, "downloads", "MBBS_Phase_III_Batch_B_Additional.ics")

with open(gen_ics_path, "rb") as f:
    gen_b64 = base64.b64encode(f.read()).decode("utf-8")

with open(batch_b_ics_path, "rb") as f:
    batch_b_b64 = base64.b64encode(f.read()).decode("utf-8")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MBBS Phase III Schedule</title>
  <style>
    :root {{
      --bg: #F9FAFB;
      --surface: #FFFFFF;
      --text: #111827;
      --muted: #6B7280;
      --subtle: #9CA3AF;
      --border: #E5E7EB;
      --btn-bg: #4B5563;
      --btn-hover: #374151;
      --btn-active: #1F2937;
    }}

    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #0F172A;
        --surface: #1E293B;
        --text: #F8FAFC;
        --muted: #94A3B8;
        --subtle: #64748B;
        --border: #334155;
        --btn-bg: #475569;
        --btn-hover: #334155;
        --btn-active: #1E293B;
      }}
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem 1rem;
      -webkit-font-smoothing: antialiased;
    }}

    .card {{
      width: 100%;
      max-width: 440px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 2.75rem 2.25rem;
      box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
    }}

    header {{
      margin-bottom: 2rem;
    }}

    h1 {{
      font-size: 1.625rem;
      font-weight: 600;
      letter-spacing: -0.025em;
      color: var(--text);
      line-height: 1.25;
      margin-bottom: 0.75rem;
    }}

    .import-guide {{
      font-size: 0.875rem;
      color: var(--muted);
      line-height: 1.55;
    }}

    .import-guide p {{
      margin-bottom: 0.35rem;
    }}

    .import-steps {{
      margin-top: 0.6rem;
      padding-left: 1.1rem;
      font-size: 0.8125rem;
      color: var(--muted);
      line-height: 1.5;
    }}

    .import-steps li {{
      margin-bottom: 0.25rem;
    }}

    .import-steps strong {{
      color: var(--text);
      font-weight: 500;
    }}

    .actions {{
      display: flex;
      flex-direction: column;
      gap: 0.875rem;
      margin-top: 2rem;
    }}

    .btn {{
      display: block;
      width: 100%;
      background: var(--btn-bg);
      color: #FFFFFF;
      border: none;
      border-radius: 14px;
      padding: 1.1rem 1.25rem;
      font-size: 0.9375rem;
      font-weight: 500;
      text-align: center;
      cursor: pointer;
      text-decoration: none;
      transition: background 0.15s ease, transform 0.1s ease;
      line-height: 1.3;
    }}

    .btn:hover {{
      background: var(--btn-hover);
      transform: translateY(-1px);
    }}

    .btn:active {{
      background: var(--btn-active);
      transform: translateY(0);
    }}

    .btn .label {{
      display: block;
      font-size: 1rem;
      font-weight: 600;
      letter-spacing: -0.01em;
    }}

    .btn .caption {{
      display: block;
      font-size: 0.8125rem;
      font-weight: 400;
      opacity: 0.85;
      margin-top: 0.2rem;
    }}

    footer {{
      margin-top: 2.25rem;
      padding-top: 1.25rem;
      border-top: 1px solid var(--border);
      text-align: center;
      font-size: 0.75rem;
      color: var(--subtle);
      letter-spacing: 0.01em;
    }}
  </style>
</head>
<body>

  <main class="card">
    <header>
      <h1>MBBS Phase III Schedule</h1>
      <div class="import-guide">
        <p>Tap below to download your calendar file.</p>
        <ul class="import-steps">
          <li><strong>Apple Calendar:</strong> Tap the file to add all classes directly.</li>
          <li><strong>Google Calendar:</strong> Open Settings → Import & select the file.</li>
        </ul>
      </div>
    </header>

    <div class="actions">
      <!-- Button 1: Complete General Schedule (Roll 1-202) -->
      <button class="btn" onclick="download('general')">
        <span class="label">Download Schedule</span>
        <span class="caption">For Roll 1–202 (Single .ics file)</span>
      </button>

      <!-- Button 2: Batch B Additional -->
      <button class="btn" onclick="download('batch_b')">
        <span class="label">Additional for B batch</span>
        <span class="caption">Ophthalmology SDL & FMT (Single .ics file)</span>
      </button>
    </div>

    <footer>
      15-minute notification included before every class
    </footer>
  </main>

  <script>
    const files = {{
      general: {{
        name: "MBBS_Phase_III_Schedule.ics",
        b64: "{gen_b64}",
        path: "downloads/MBBS_Phase_III_Schedule.ics"
      }},
      batch_b: {{
        name: "MBBS_Phase_III_Batch_B_Additional.ics",
        b64: "{batch_b_b64}",
        path: "downloads/MBBS_Phase_III_Batch_B_Additional.ics"
      }}
    }};

    function download(key) {{
      const item = files[key];
      try {{
        const bytes = atob(item.b64);
        const len = bytes.length;
        const u8 = new Uint8Array(len);
        for (let i = 0; i < len; i++) {{
          u8[i] = bytes.charCodeAt(i);
        }}
        const blob = new Blob([u8], {{ type: "text/calendar;charset=utf-8" }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = item.name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(url), 1000);
      }} catch (err) {{
        window.location.href = item.path;
      }}
    }}
  </script>
</body>
</html>
"""

output_path = os.path.join(BASE_DIR, "index.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Empathetic website written to {output_path} ({len(html)} bytes)")
