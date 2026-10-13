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
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>MBBS Phase III/I Schedule</title>
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
      background-color: #07090e;
      background-image: 
        radial-gradient(circle at 15% 25%, rgba(99, 102, 241, 0.22) 0%, transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(14, 165, 233, 0.18) 0%, transparent 45%),
        radial-gradient(circle at 80% 85%, rgba(244, 63, 94, 0.14) 0%, transparent 50%),
        radial-gradient(circle at 20% 85%, rgba(139, 92, 246, 0.18) 0%, transparent 50%);
      background-attachment: fixed;
      color: #e5e7eb;
      min-height: 100vh;
      min-height: -webkit-fill-available;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: max(1.5rem, env(safe-area-inset-top)) 1rem max(1.5rem, env(safe-area-inset-bottom)) 1rem;
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

    .ambient-glow {{
      position: fixed;
      top: -20vh;
      left: 50%;
      transform: translateX(-50%);
      width: 100vw;
      height: 70vh;
      background: radial-gradient(ellipse at center, rgba(99, 102, 241, 0.12) 0%, rgba(56, 189, 248, 0.06) 40%, rgba(7, 9, 14, 0) 75%);
      z-index: 1;
      pointer-events: none;
    }}

    .card {{
      position: relative;
      z-index: 10;
      width: 100%;
      max-width: 400px;
      min-width: 0;
      background: rgba(13, 16, 24, 0.76);
      backdrop-filter: blur(44px) saturate(210%);
      -webkit-backdrop-filter: blur(44px) saturate(210%);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 26px;
      padding: 2.5rem 2rem;
      box-shadow: 
        inset 0 1px 0 0 rgba(255, 255, 255, 0.2),
        0 24px 48px -12px rgba(0, 0, 0, 0.65),
        0 4px 16px rgba(0, 0, 0, 0.4);
    }}

    @media (max-width: 600px) {{
      .card {{
        padding: 2.15rem 1.35rem;
        border-radius: 22px;
      }}
    }}

    header {{
      margin-bottom: 1.75rem;
      text-align: left;
    }}

    h1 {{
      font-size: 1.625rem;
      font-weight: 700;
      letter-spacing: -0.035em;
      color: #f8fafc;
      line-height: 1.22;
      margin-bottom: 0.65rem;
    }}

    @media (max-width: 600px) {{
      h1 {{
        font-size: 1.45rem;
      }}
    }}

    .subtitle {{
      font-size: 0.875rem;
      color: #94a3b8;
      line-height: 1.55;
      font-weight: 400;
    }}

    @media (max-width: 600px) {{
      .subtitle {{
        font-size: 0.84rem;
        line-height: 1.5;
      }}
    }}

    .actions {{
      display: flex;
      flex-direction: column;
      gap: 0.875rem;
      margin-top: 1.5rem;
      min-width: 0;
    }}

    .btn {{
      display: block;
      width: 100%;
      min-width: 0;
      border-radius: 16px;
      padding: 1.125rem 1.15rem;
      text-align: center;
      cursor: pointer;
      text-decoration: none;
      transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.18s cubic-bezier(0.16, 1, 0.3, 1), background 0.18s ease;
      line-height: 1.35;
      user-select: none;
      -webkit-user-select: none;
    }}

    @media (max-width: 600px) {{
      .btn {{
        padding: 1rem 0.875rem;
        border-radius: 14px;
      }}
    }}

    /* Primary high-affordance button (Bright Pearl White) */
    .btn-primary {{
      background: linear-gradient(180deg, #FFFFFF 0%, #F1F4F9 100%);
      border: 1px solid rgba(255, 255, 255, 0.95);
      box-shadow: 
        inset 0 1px 0 rgba(255, 255, 255, 1),
        0 4px 8px -1px rgba(0, 0, 0, 0.2),
        0 12px 28px -4px rgba(0, 0, 0, 0.38);
    }}

    .btn-primary:hover {{
      background: linear-gradient(180deg, #FFFFFF 0%, #E5EBF4 100%);
      transform: translateY(-1px);
      box-shadow: 
        inset 0 1px 0 rgba(255, 255, 255, 1),
        0 8px 16px -2px rgba(0, 0, 0, 0.25),
        0 16px 36px -4px rgba(0, 0, 0, 0.45);
    }}

    .btn-primary:active {{
      background: linear-gradient(180deg, #EAEFF6 0%, #DCE3ED 100%);
      transform: scale(0.985);
      box-shadow: 
        inset 0 1px 2px rgba(0, 0, 0, 0.15),
        0 2px 6px rgba(0, 0, 0, 0.3);
    }}

    .btn-primary .label {{
      display: block;
      font-size: 1.025rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #090d16;
    }}

    .btn-primary .caption {{
      display: block;
      font-size: 0.8125rem;
      font-weight: 500;
      color: #475569;
      margin-top: 0.25rem;
    }}

    /* Secondary high-affordance button (Luminous Ice Platinum) */
    .btn-secondary {{
      background: linear-gradient(180deg, #E6EDF5 0%, #D5DFEB 100%);
      border: 1px solid rgba(255, 255, 255, 0.65);
      box-shadow: 
        inset 0 1px 0 rgba(255, 255, 255, 0.9),
        0 4px 8px -1px rgba(0, 0, 0, 0.18),
        0 10px 24px -4px rgba(0, 0, 0, 0.32);
    }}

    .btn-secondary:hover {{
      background: linear-gradient(180deg, #EDF3FA 0%, #CBD7E5 100%);
      transform: translateY(-1px);
      box-shadow: 
        inset 0 1px 0 rgba(255, 255, 255, 0.95),
        0 6px 14px -2px rgba(0, 0, 0, 0.22),
        0 14px 32px -4px rgba(0, 0, 0, 0.38);
    }}

    .btn-secondary:active {{
      background: linear-gradient(180deg, #CCD7E4 0%, #BFCFDF 100%);
      transform: scale(0.985);
      box-shadow: 
        inset 0 1px 2px rgba(0, 0, 0, 0.15),
        0 2px 6px rgba(0, 0, 0, 0.25);
    }}

    .btn-secondary .label {{
      display: block;
      font-size: 1.025rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #0b1120;
    }}

    .btn-secondary .caption {{
      display: block;
      font-size: 0.8125rem;
      font-weight: 500;
      color: #4b5563;
      margin-top: 0.25rem;
    }}

    .footer {{
      margin-top: 2rem;
      text-align: center;
      font-size: 0.75rem;
      font-weight: 500;
      color: #64748b;
      letter-spacing: 0.025em;
    }}
  </style>
</head>
<body>

  <canvas id="gl-canvas"></canvas>
  <div class="ambient-glow"></div>

  <main class="card">
    <header>
      <h1>MBBS Phase III/I Schedule</h1>
      <p class="subtitle">Download the schedule files below and open it with your calendar app of choice</p>
    </header>

    <div class="actions">
      <button class="btn btn-primary" onclick="download('general')" aria-label="Download General Schedule for Roll 1 to 202">
        <span class="label">Download Schedule</span>
        <span class="caption">For Roll 1 to 202 (Single .ics file)</span>
      </button>

      <button class="btn btn-secondary" onclick="download('batch_b')" aria-label="Download Additional Schedule for Batch B">
        <span class="label">Additional for B batch</span>
        <span class="caption">Ophthalmology SDL and FMT (Single .ics file)</span>
      </button>
    </div>

    <footer class="footer">Made by Shubhayu :)</footer>
  </main>

  <script>
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

        float height(vec2 p, float t, vec2 mouse) {{
          float mDist = length(p - mouse);
          float mFactor = exp(-mDist * 1.8) * 0.32;

          float h1 = sin(p.x * 1.35 + t * 0.45) * cos(p.y * 1.15 - t * 0.35);
          
          vec2 w1 = vec2(
            sin(p.y * 2.1 + t * 0.40 + mFactor),
            cos(p.x * 1.85 - t * 0.30 - mFactor)
          );
          float h2 = sin((p.x + w1.x * 0.82) * 2.2 - t * 0.50) * cos((p.y + w1.y * 0.82) * 1.95 + t * 0.38);
          
          vec2 w2 = vec2(
            cos((p.x + h2 * 0.75) * 3.1 + t * 0.30),
            sin((p.y + h1 * 0.75) * 3.3 - t * 0.35)
          );
          float h3 = sin((p.x + w2.x * 0.48) * 4.1 + t * 0.55) * cos((p.y + w2.y * 0.48) * 3.7 - t * 0.42);

          return h1 * 0.52 + h2 * 0.34 + h3 * 0.19 + mFactor;
        }}

        void main() {{
          vec2 st = (gl_FragCoord.xy - 0.5 * u_resolution.xy) / min(u_resolution.x, u_resolution.y);
          float t = u_time * 0.27;
          vec2 m = (u_mouse - 0.5 * u_resolution.xy) / min(u_resolution.x, u_resolution.y) * 2.8;

          vec2 p = st * 2.75;

          float eps = 0.007;
          float hC = height(p, t, m);
          float hR = height(p + vec2(eps, 0.0), t, m);
          float hU = height(p + vec2(0.0, eps), t, m);

          vec3 normal = normalize(vec3((hC - hR) / eps, (hC - hU) / eps, 0.30));

          // Multi-directional lighting with color-popping reflection highlights
          vec3 keyLight    = normalize(vec3(-0.45, 0.75, 0.70));
          vec3 fillLight   = normalize(vec3(0.60, -0.50, 0.55));
          vec3 rimLight    = normalize(vec3(0.0, 1.0, 0.25));
          vec3 accentLight = normalize(vec3(0.85, 0.30, 0.50));

          float diffKey    = max(dot(normal, keyLight), 0.0);
          float diffFill   = max(dot(normal, fillLight), 0.0);
          float diffAccent = max(dot(normal, accentLight), 0.0);

          vec3 viewDir     = vec3(0.0, 0.0, 1.0);
          
          // Fresnel iridescent rim reflection
          float fresnel    = pow(1.0 - max(dot(normal, viewDir), 0.0), 3.0);

          // Specular highlights
          vec3 halfKey     = normalize(keyLight + viewDir);
          float specKey    = pow(max(dot(normal, halfKey), 0.0), 30.0);

          vec3 halfAccent  = normalize(accentLight + viewDir);
          float specAccent = pow(max(dot(normal, halfAccent), 0.0), 18.0);

          // Color palette with deep velvet carbon and iridescent pop
          vec3 deepCarbon    = vec3(0.032, 0.035, 0.045);
          vec3 electricIndigo= vec3(0.38, 0.40, 0.98);
          vec3 vividCyan     = vec3(0.12, 0.82, 0.90);
          vec3 warmRose      = vec3(0.96, 0.42, 0.68);
          vec3 platinum      = vec3(0.88, 0.90, 0.96);

          // Base tone modulated by fluid depth
          vec3 color = deepCarbon;
          float waveMix = smoothstep(-0.45, 0.55, hC);
          color = mix(color, mix(deepCarbon, electricIndigo * 0.42, waveMix), 0.85);

          // Vivid reflection color pops
          color += vividCyan * (diffKey * 0.38);
          color += warmRose * (diffAccent * 0.28);
          color += electricIndigo * (diffFill * 0.22);

          // Iridescent edge sheen
          vec3 rimGradient = mix(vividCyan, warmRose, sin(hC * 3.1415 + t) * 0.5 + 0.5);
          color += rimGradient * (fresnel * 0.52);

          // Pure platinum specular glints
          color += platinum * (specKey * 0.72);
          color += vividCyan * (specAccent * 0.40);

          // Elegant vignette
          float dist = length(st);
          color *= smoothstep(1.9, 0.35, dist * 0.88);

          // Subtle dithering
          float noise = fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453);
          color += (noise - 0.5) * 0.015;

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
      const mouseLoc = gl.getUniformLocation(prog, "u_mouse");

      let currentMouse = [window.innerWidth * 0.5, window.innerHeight * 0.5];
      let targetMouse = [window.innerWidth * 0.5, window.innerHeight * 0.5];

      function updatePointer(x, y) {{
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        targetMouse[0] = x * dpr;
        targetMouse[1] = (window.innerHeight - y) * dpr;
      }}

      window.addEventListener('mousemove', (e) => {{
        updatePointer(e.clientX, e.clientY);
      }});

      window.addEventListener('touchstart', (e) => {{
        if (e.touches && e.touches.length > 0) {{
          updatePointer(e.touches[0].clientX, e.touches[0].clientY);
        }}
      }}, {{ passive: true }});

      window.addEventListener('touchmove', (e) => {{
        if (e.touches && e.touches.length > 0) {{
          updatePointer(e.touches[0].clientX, e.touches[0].clientY);
        }}
      }}, {{ passive: true }});

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
        
        currentMouse[0] += (targetMouse[0] - currentMouse[0]) * 0.05;
        currentMouse[1] += (targetMouse[1] - currentMouse[1]) * 0.05;

        gl.uniform2f(resLoc, canvas.width, canvas.height);
        gl.uniform1f(timeLoc, elapsed);
        gl.uniform2f(mouseLoc, currentMouse[0], currentMouse[1]);

        gl.drawArrays(gl.TRIANGLES, 0, 6);
        requestAnimationFrame(render);
      }}
      requestAnimationFrame(render);
    }}

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

    function download(type) {{
      const file = files[type];
      if (!file) return;

      try {{
        const byteCharacters = atob(file.b64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {{
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }}
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], {{ type: 'text/calendar;charset=utf-8' }});
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = file.name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(url), 2000);
      }} catch (err) {{
        const a = document.createElement('a');
        a.href = file.path;
        a.download = file.name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }}
    }}
  </script>
</body>
</html>"""

out_path = os.path.join(BASE_DIR, "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Generated index.html successfully, size:", len(html))
