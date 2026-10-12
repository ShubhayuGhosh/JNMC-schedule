import base64
import os
import subprocess

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
      background-color: #0b0c10;
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

    .card {{
      position: relative;
      z-index: 10;
      width: 100%;
      max-width: 440px;
      background: rgba(18, 20, 26, 0.72);
      backdrop-filter: blur(28px) saturate(180%);
      -webkit-backdrop-filter: blur(28px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 24px;
      padding: 2.75rem 2.25rem;
      box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.08);
    }}

    header {{
      margin-bottom: 2rem;
    }}

    h1 {{
      font-size: 1.65rem;
      font-weight: 700;
      letter-spacing: -0.035em;
      color: #f3f4f6;
      line-height: 1.2;
      margin-bottom: 0.85rem;
    }}

    .import-guide {{
      font-size: 0.875rem;
      color: #9ca3af;
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
      color: #e2e8f0;
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
      background: #272a33;
      color: #f1f5f9;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 1.1rem 1.25rem;
      text-align: center;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.18s ease;
      line-height: 1.3;
      box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.05);
    }}

    .btn:hover {{
      background: #323642;
      border-color: rgba(255, 255, 255, 0.14);
      transform: translateY(-1px);
    }}

    .btn:active {{
      background: #1f2229;
      transform: translateY(0);
    }}

    .btn .label {{
      display: block;
      font-size: 0.975rem;
      font-weight: 600;
      letter-spacing: -0.015em;
      color: #f8fafc;
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
    // WebGL Fluid Monochrome Shader
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
        uniform vec2 u_mouse;

        // Simplex-inspired organic noise
        vec3 mod289(vec3 x) {{ return x - floor(x * (1.0 / 289.0)) * 289.0; }}
        vec2 mod289(vec2 x) {{ return x - floor(x * (1.0 / 289.0)) * 289.0; }}
        vec3 permute(vec3 x) {{ return mod289(((x*34.0)+1.0)*x); }}

        float snoise(vec2 v) {{
          const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
          vec2 i  = floor(v + dot(v, C.yy) );
          vec2 x0 = v -   i + dot(i, C.xx);
          vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
          vec4 x12 = x0.xyxy + C.xxzz;
          x12.xy -= i1;
          i = mod289(i);
          vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 )) + i.x + vec3(0.0, i1.x, 1.0 ));
          vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
          m = m*m ;
          m = m*m ;
          vec3 x = 2.0 * fract(p * C.www) - 1.0;
          vec3 h = abs(x) - 0.5;
          vec3 ox = floor(x + 0.5);
          vec3 a0 = x - ox;
          m *= 1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h );
          vec3 g;
          g.x  = a0.x  * x0.x  + h.x  * x0.y;
          g.yz = a0.yz * x12.xz + h.yz * x12.yw;
          return 130.0 * dot(m, g);
        }}

        float fbm(vec2 p) {{
          float total = 0.0;
          float amp = 0.5;
          for(int i = 0; i < 4; i++) {{
            total += amp * snoise(p);
            p = p * 2.02 + vec2(1.7, 9.2);
            amp *= 0.5;
          }}
          return total;
        }}

        void main() {{
          vec2 st = gl_FragCoord.xy / u_resolution.xy;
          st.x *= u_resolution.x / u_resolution.y;

          float t = u_time * 0.12;

          // Domain warping (fluid smoke flow)
          vec2 q = vec2(
            fbm(st + vec2(0.0, t * 0.5)),
            fbm(st + vec2(5.2, 1.3 - t * 0.4))
          );

          vec2 r = vec2(
            fbm(st + 3.0 * q + vec2(1.7 - t * 0.3, 9.2 + t * 0.2)),
            fbm(st + 3.0 * q + vec2(8.3 + t * 0.4, 2.8 - t * 0.3))
          );

          float f = fbm(st + 4.0 * r);

          // Deep, luxurious slate and charcoal monochromatic gradient
          vec3 c1 = vec3(0.045, 0.048, 0.055); // Dark obsidian base
          vec3 c2 = vec3(0.110, 0.118, 0.130); // Cool carbon
          vec3 c3 = vec3(0.240, 0.255, 0.275); // Smoky slate
          vec3 c4 = vec3(0.480, 0.500, 0.530); // Silver highlight

          vec3 color = mix(c1, c2, clamp(f * f * 2.0, 0.0, 1.0));
          color = mix(color, c3, clamp(length(q), 0.0, 1.0));
          color = mix(color, c4, clamp(length(r.x), 0.0, 1.0) * 0.45);

          // Subtle vignette
          vec2 uv = gl_FragCoord.xy / u_resolution.xy;
          float vignette = 1.0 - 0.45 * length(uv - 0.5);
          color *= vignette;

          // Subtle film grain
          float grain = fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453) * 0.025;
          color += grain;

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
print("Updated index.html")
