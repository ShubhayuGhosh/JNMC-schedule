import base64
import os

BASE_DIR = "/Users/shubhayu/Documents/antigravity/splendid-raman"
gen_zip_path = os.path.join(BASE_DIR, "downloads", "MBBS_Phase_III_Part_I_General_Schedule.zip")
batch_b_zip_path = os.path.join(BASE_DIR, "downloads", "MBBS_Phase_III_Part_I_Batch_B_Schedule.zip")

with open(gen_zip_path, "rb") as f:
    gen_b64 = base64.b64encode(f.read()).decode("utf-8")

with open(batch_b_zip_path, "rb") as f:
    batch_b_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JNMC MBBS Phase III Schedule</title>
  <style>
    :root {{
      --bg: #F8F9FA;
      --card-bg: #FFFFFF;
      --text-main: #1F2937;
      --text-muted: #6B7280;
      --border: #E5E7EB;
      --btn-gray: #4B5563;
      --btn-gray-hover: #374151;
      --btn-gray-active: #1F2937;
      --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }}

    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #111827;
        --card-bg: #1F2937;
        --text-main: #F9FAFB;
        --text-muted: #9CA3AF;
        --border: #374151;
        --btn-gray: #4B5563;
        --btn-gray-hover: #6B7280;
        --btn-gray-active: #9CA3AF;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
      }}
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem 1rem;
      line-height: 1.5;
    }}

    .container {{
      width: 100%;
      max-width: 520px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 2.5rem 2rem;
      box-shadow: var(--shadow);
      text-align: center;
    }}

    .header-badge {{
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      background: rgba(107, 114, 128, 0.12);
      color: var(--text-muted);
      margin-bottom: 1rem;
    }}

    h1 {{
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
      color: var(--text-main);
      letter-spacing: -0.02em;
    }}

    p.subtitle {{
      font-size: 0.925rem;
      color: var(--text-muted);
      margin-bottom: 2.25rem;
    }}

    .button-group {{
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}

    .gray-button {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background-color: var(--btn-gray);
      color: #FFFFFF;
      border: none;
      border-radius: 12px;
      padding: 1.1rem 1.5rem;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.18s ease;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
      user-select: none;
    }}

    .gray-button:hover {{
      background-color: var(--btn-gray-hover);
      transform: translateY(-1px);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
    }}

    .gray-button:active {{
      background-color: var(--btn-gray-active);
      transform: translateY(0);
    }}

    .gray-button span.btn-sub {{
      font-size: 0.8rem;
      font-weight: 400;
      opacity: 0.85;
      margin-top: 0.25rem;
    }}

    .details {{
      margin-top: 2.25rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
      text-align: left;
    }}

    details summary {{
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      user-select: none;
      outline: none;
    }}

    details summary:hover {{
      color: var(--text-main);
    }}

    .palette-list {{
      margin-top: 0.85rem;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.5rem;
      font-size: 0.8rem;
    }}

    .palette-item {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: var(--text-muted);
    }}

    .color-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
    }}

    .instructions {{
      margin-top: 1rem;
      font-size: 0.775rem;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    .footer {{
      margin-top: 1.5rem;
      font-size: 0.75rem;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>

  <div class="container">
    <div class="header-badge">JNMC Belagavi • CBME</div>
    <h1>MBBS Phase III (Part I) Schedule</h1>
    <p class="subtitle">Complete semester class schedules formatted with 15-minute reminders and distinct subject color coding.</p>

    <div class="button-group">
      <!-- Button 1: General Schedule for Roll 1-202 -->
      <button class="gray-button" onclick="downloadZip('general')">
        <span>Download General Schedule</span>
        <span class="btn-sub">Meant for Roll 1–202 (7 Individual Subjects .zip)</span>
      </button>

      <!-- Button 2: Batch B Schedule -->
      <button class="gray-button" onclick="downloadZip('batch_b')">
        <span>Download Batch B Schedule</span>
        <span class="btn-sub">Meant for Roll 101–202 (Ophthalmology SDL & FMT .zip)</span>
      </button>
    </div>

    <div class="details">
      <details>
        <summary>View Included Subjects & Nordic Soft Palette</summary>
        <div class="palette-list">
          <div class="palette-item">
            <span class="color-dot" style="background-color: #3D5A80;"></span>
            <span>Medicine (Soft Navy)</span>
          </div>
          <div class="palette-item">
            <span class="color-dot" style="background-color: #9C5248;"></span>
            <span>Surgery (Muted Brick)</span>
          </div>
          <div class="palette-item">
            <span class="color-dot" style="background-color: #52796F;"></span>
            <span>ENT (Juniper Green)</span>
          </div>
          <div class="palette-item">
            <span class="color-dot" style="background-color: #7B5E7B;"></span>
            <span>OBG (Vintage Plum)</span>
          </div>
          <div class="palette-item">
            <span class="color-dot" style="background-color: #DDA15E;"></span>
            <span>Pediatrics (Warm Honey)</span>
          </div>
          <div class="palette-item">
            <span class="color-dot" style="background-color: #4682B4;"></span>
            <span>Ophthal Theory (Cerulean)</span>
          </div>
          <div class="palette-item">
            <span class="color-dot" style="background-color: #4A5568;"></span>
            <span>Community Med (Charcoal)</span>
          </div>
          <div class="palette-item">
            <span class="color-dot" style="background-color: #4A6B82;"></span>
            <span>Ophthal SDL (Steel)</span>
          </div>
          <div class="palette-item">
            <span class="color-dot" style="background-color: #5C677D;"></span>
            <span>FMT Batch B (Ash Slate)</span>
          </div>
        </div>
        <div class="instructions">
          <strong>How to Import:</strong><br>
          • <strong>Apple Calendar (Mac/iPhone):</strong> Unzip and double-click each <code>.ics</code> file to import into its dedicated colored calendar layer.<br>
          • <strong>Google Calendar:</strong> Go to Settings → <em>Add calendar</em> → <em>Create new calendar</em> (e.g. "Surgery"), then click <em>Import</em> and select the corresponding <code>.ics</code> file.
        </div>
      </details>
    </div>

    <div class="footer">
      Jawaharlal Nehru Medical College, Belagavi
    </div>
  </div>

  <script>
    const files = {{
      general: {{
        name: "MBBS_Phase_III_Part_I_General_Schedule.zip",
        b64: "{gen_b64}",
        path: "downloads/MBBS_Phase_III_Part_I_General_Schedule.zip"
      }},
      batch_b: {{
        name: "MBBS_Phase_III_Part_I_Batch_B_Schedule.zip",
        b64: "{batch_b_b64}",
        path: "downloads/MBBS_Phase_III_Part_I_Batch_B_Schedule.zip"
      }}
    }};

    function downloadZip(key) {{
      const item = files[key];
      // Convert base64 to Blob to ensure instant download across all browsers/offline
      try {{
        const byteCharacters = atob(item.b64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {{
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }}
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], {{ type: "application/zip" }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = item.name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(url), 1000);
      }} catch (e) {{
        // Fallback to relative path if atob fails
        window.location.href = item.path;
      }}
    }}
  </script>
</body>
</html>
'''

output_html_path = os.path.join(BASE_DIR, "index.html")
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated index.html at {output_html_path} ({len(html_content)} bytes)")
