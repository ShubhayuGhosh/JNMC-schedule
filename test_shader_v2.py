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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #07080a;
      color: #e5e7eb;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem 1rem;
      overflow-x: hidden;
      position: relative;
    }}

    #gl-canvas {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 0;
      pointer-events: none;
    }}

    /* Subtle top glow overlay */
    .ambient-glow {{
      position: fixed;
      top: -20vh;
      left: 50%;
      transform: translateX(-50%);
      width: 80vw;
      height: 50vh;
      background: radial-gradient(ellipse at center, rgba(148, 163, 184, 0.08) 0%, rgba(15, 23, 42, 0) 70%);
      z-index: 1;
      pointer-events: none;
    }}

    .card {{
      position: relative;
      z-index: 10;
      width: 100%;
      max-width: 440px;
      background: rgba(14, 16, 22, 0.76);
      backdrop-filter: blur(36px) saturate(190%);
      -webkit-backdrop-filter: blur(36px) saturate(190%);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 24px;
      padding: 2.75rem 2.25rem;
      box-shadow: 
        inset 0 1px 0 0 rgba(255, 255, 255, 0.12),
        inset 0 0 0 1px rgba(255, 255, 255, 0.03);
    }}

    header {{
      margin-bottom: 2rem;
    }}

    h1 {{
      font-size: 1.65rem;
      font-weight: 700;
      letter-spacing: -0.035em;
      color: #f8fafc;
      line-height: 1.2;
      margin-bottom: 0.85rem;
    }}

    .import-guide {{
      font-size: 0.875rem;
      color: #94a3b8;
      line-height: 1.55;
    }}

    .import-guide p {{
      margin-bottom: 0.4rem;
      font-weight: 400;
      color: #cbd5e1;
    }}

    .import-steps {{
      margin-top: 0.6rem;
      list-style-type: none;
      font-size: 0.8125rem;
      color: #94a3b8;
      line-height: 1.5;
    }}

    .import-steps li {{
      margin-bottom: 0.35rem;
      position: relative;
      padding-left: 1rem;
    }}

    .import-steps li::before {{
      content: "•";
      position: absolute;
      left: 0;
      color: #64748b;
    }}

    .import-steps strong {{
      color: #f1f5f9;
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
      background: linear-gradient(180deg, #252831 0%, #1c1e26 100%);
      color: #f8fafc;
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 14px;
      padding: 1.1rem 1.25rem;
      text-align: center;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      line-height: 1.3;
      box-shadow: 
        inset 0 1px 0 0 rgba(255, 255, 255, 0.1),
        0 1px 2px rgba(0, 0, 0, 0.2);
    }}

    .btn:hover {{
      background: linear-gradient(180deg, #2e323e 0%, #232630 100%);
      border-color: rgba(255, 255, 255, 0.16);
      transform: translateY(-1px);
      box-shadow: 
        inset 0 1px 0 0 rgba(255, 255, 255, 0.15),
        0 4px 12px rgba(0, 0, 0, 0.25);
    }}

    .btn:active {{
      background: linear-gradient(180deg, #1c1e25 0%, #16181e 100%);
      transform: translateY(0);
      box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.4);
    }}

    .btn .label {{
      display: block;
      font-size: 0.975rem;
      font-weight: 600;
      letter-spacing: -0.015em;
      color: #ffffff;
    }}

    .btn .caption {{
      display: block;
      font-size: 0.8125rem;
      font-weight: 400;
      color: #94a3b8;
      margin-top: 0.2rem;
    }}
  </style>
</head>
<body>

  <canvas id="gl-canvas"></canvas>
  <div class="ambient-glow"></div>

  <main class="card">
    <header>
      <h1>MBBS Phase III Schedule</h1>
      <div class="import-guide">
        <p>Tap below to download your calendar file.</p>
        <ul class="import-steps">
          <li><strong>Apple Calendar:</strong> Tap the file to add all classes directly.</li>
          <li><strong>Google Calendar:</strong> Open Settings, click Import, and select the file.</li>
        </ul>
      </div>
    </header>

    <div class="actions">
      <button class="btn" onclick="download('general')">
        <span class="label">Download Schedule</span>
        <span class="caption">For Roll 1 to 202 (Single .ics file)</span>
      </button>

      <button class="btn" onclick="download('batch_b')">
        <span class="label">Additional for B batch</span>
        <span class="caption">Ophthalmology SDL and FMT (Single .ics file)</span>
      </button>
    </div>
  </main>

  <script>
    // High-End Liquid Titanium / Silk Mesh Shader
    const canvas = document.getElementById('gl-canvas');
    const gl = canvas.getContext('webgl');

    if (gl) {{
      const vsSource = `
        attribute vec2 position;
        void main() {{
          gl_Position = vec4(position, 0.0, 1.0);
        }}
      `;

      const fsSource = `
        precision highp float;
        uniform vec2 u_resolution;
        uniform float u_time;

        // Smooth wave height function
        float height(vec2 p, float t) {{
          // Large undulating liquid waves
          float h1 = sin(p.x * 1.4 + t * 0.45) * cos(p.y * 1.2 - t * 0.35);
          
          // Domain warp 1
          vec2 w1 = vec2(
            sin(p.y * 2.1 + t * 0.4),
            cos(p.x * 1.9 - t * 0.3)
          );
          float h2 = sin((p.x + w1.x * 0.8) * 2.2 - t * 0.5) * cos((p.y + w1.y * 0.8) * 2.0 + t * 0.4);
          
          // Domain warp 2 (silky folds)
          vec2 w2 = vec2(
            cos((p.x + h2) * 3.1 + t * 0.3),
            sin((p.y + h1) * 3.3 - t * 0.35)
          );
          float h3 = sin((p.x + w2.x * 0.5) * 4.2 + t * 0.6) * cos((p.y + w2.y * 0.5) * 3.8 - t * 0.5);

          return h1 * 0.55 + h2 * 0.35 + h3 * 0.18;
        }}

        void main() {{
          vec2 st = (gl_FragCoord.xy - 0.5 * u_resolution.xy) / min(u_resolution.x, u_resolution.y);
          float t = u_time * 0.28;

          // Scale and coordinates
          vec2 p = st * 2.8;

          // Compute surface height and pseudo normals
          float eps = 0.006;
          float hC = height(p, t);
          float hR = height(p + vec2(eps, 0.0), t);
          float hU = height(p + vec2(0.0, eps), t);

          vec3 normal = normalize(vec3((hC - hR) / eps, (hC - hU) / eps, 0.32));

          // Multi-directional lighting setup (SaaS studio lighting)
          vec3 keyLight = normalize(vec3(-0.4, 0.7, 0.8));
          vec3 fillLight = normalize(vec3(0.5, -0.6, 0.5));
          vec3 rimLight = normalize(vec3(0.0, 1.0, 0.2));

          float diffKey = max(dot(normal, keyLight), 0.0);
          float diffFill = max(dot(normal, fillLight), 0.0);
          
          vec3 viewDir = vec3(0.0, 0.0, 1.0);
          vec3 halfKey = normalize(keyLight + viewDir);
          float specKey = pow(max(dot(normal, halfKey), 0.0), 24.0);

          vec3 halfRim = normalize(rimLight + viewDir);
          float specRim = pow(max(dot(normal, halfRim), 0.0), 12.0);

          // Luxurious slate titanium color palette
          vec3 deepBase    = vec3(0.032, 0.035, 0.042); // Obsidian carbon
          vec3 midSlate    = vec3(0.125, 0.135, 0.155); // Titanium slate
          vec3 silverSheen = vec3(0.280, 0.295, 0.325); // Liquid pewter
          vec3 highlight   = vec3(0.680, 0.710, 0.760); // Specular platinum

          // Composite shading
          vec3 color = deepBase;
          color = mix(color, midSlate, smoothstep(-0.8, 0.4, hC));
          color += silverSheen * (diffKey * 0.45 + diffFill * 0.15);
          color += highlight * (specKey * 0.65 + specRim * 0.25);

          // Subtle radial dark falloff
          float dist = length(st);
          color *= smoothstep(1.8, 0.2, dist * 0.9);

          // Micro film grain to eliminate 8-bit banding
          float noise = fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453);
          color += (noise - 0.5) * 0.018;

          gl_FragColor = vec4(color, 1.0);
        }}
      `;

      function createShader(gl, type, source) {{
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        return shader;
      }}

      const vs = createShader(gl, gl.VERTEX_SHADER, vsSource);
      const fs = createShader(gl, gl.FRAGMENT_SHADER, fsSource);
      const prog = gl.createProgram();
      gl.attachShader(prog, vs);
      gl.attachShader(prog, fs);
      gl.linkProgram(prog);
      gl.useProgram(prog);

      const posBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
        -1, -1,
         1, -1,
        -1,  1,
        -1,  1,
         1, -1,
         1,  1
      ]), gl.STATIC_DRAW);

      const posLoc = gl.getAttribLocation(prog, "position");
      gl.enableVertexAttribArray(posLoc);
      gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

      const resLoc = gl.getUniformLocation(prog, "u_resolution");
      const timeLoc = gl.getUniformLocation(prog, "u_time");

      function resize() {{
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width = window.innerWidth * dpr;
        canvas.height = window.innerHeight * dpr;
        gl.viewport(0, 0, canvas.width, canvas.height);
      }}
      window.addEventListener('resize', resize);
      resize();

      let startTime = performance.now();
      function render() {{
        const elapsed = (performance.now() - startTime) * 0.001;
        gl.uniform2f(resLoc, canvas.width, canvas.height);
        gl.uniform1f(timeLoc, elapsed);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
        requestAnimationFrame(render);
      }}
      requestAnimationFrame(render);
    }}

    // Download handlers
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
print("Updated index.html with liquid titanium shader.")
