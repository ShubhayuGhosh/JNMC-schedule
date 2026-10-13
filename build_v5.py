import os, base64

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
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #03050a;
      color: #e2e8f0;
      min-height: 100vh;
      min-height: -webkit-fill-available;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: max(1.5rem, env(safe-area-inset-top)) 1.25rem max(1.5rem, env(safe-area-inset-bottom)) 1.25rem;
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
      top: 10vh;
      left: 50%;
      transform: translateX(-50%);
      width: 90vw;
      height: 60vh;
      background: radial-gradient(ellipse at center, rgba(56, 189, 248, 0.08) 0%, rgba(30, 58, 138, 0.04) 50%, rgba(3, 5, 10, 0) 80%);
      z-index: 1;
      pointer-events: none;
    }}

    .card {{
      position: relative;
      z-index: 10;
      width: 100%;
      max-width: 430px;
      min-width: 0;
      background: rgba(10, 13, 22, 0.78);
      backdrop-filter: blur(50px) saturate(200%);
      -webkit-backdrop-filter: blur(50px) saturate(200%);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 32px;
      padding: 2.75rem 2.25rem 2.25rem;
      box-shadow: 
        inset 0 1px 0 0 rgba(255, 255, 255, 0.16),
        0 24px 64px -16px rgba(0, 0, 0, 0.8),
        0 4px 16px rgba(0, 0, 0, 0.5);
      animation: cardAppear 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}

    @keyframes cardAppear {{
      from {{
        opacity: 0;
        transform: translateY(12px) scale(0.985);
      }}
      to {{
        opacity: 1;
        transform: translateY(0) scale(1);
      }}
    }}

    @media (max-width: 480px) {{
      .card {{
        padding: 2.15rem 1.45rem 1.85rem;
        border-radius: 26px;
      }}
    }}

    .badge-pill {{
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
      font-size: 0.6875rem;
      font-weight: 600;
      letter-spacing: 0.075em;
      text-transform: uppercase;
      color: #94a3b8;
      margin-bottom: 1.25rem;
    }}

    .badge-pill .dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #38bdf8;
      box-shadow: 0 0 8px #38bdf8;
    }}

    header {{
      margin-bottom: 2rem;
      text-align: left;
    }}

    h1 {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 2.35rem;
      font-weight: 400;
      letter-spacing: -0.015em;
      color: #ffffff;
      line-height: 1.15;
      margin-bottom: 0.75rem;
      text-wrap: balance;
    }}

    @media (max-width: 480px) {{
      h1 {{
        font-size: 2.05rem;
      }}
    }}

    .subtitle {{
      font-size: 0.875rem;
      color: #94a3b8;
      line-height: 1.55;
      font-weight: 400;
    }}

    @media (max-width: 480px) {{
      .subtitle {{
        font-size: 0.825rem;
        line-height: 1.5;
      }}
    }}

    .actions {{
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
      margin-top: 1.75rem;
      min-width: 0;
    }}

    .btn {{
      position: relative;
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      min-width: 0;
      border-radius: 14px;
      padding: 0.95rem 1.15rem;
      text-decoration: none;
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
      line-height: 1.25;
      text-align: left;
    }}

    /* Primary Hero CTA (Pure Porcelain White) */
    .btn-primary {{
      background: #ffffff;
      border: 1px solid rgba(255, 255, 255, 1);
      color: #080a11;
      box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.3),
        0 1px 2px rgba(0, 0, 0, 0.15);
    }}

    .btn-primary:hover {{
      background: #f8fafc;
      transform: translateY(-1.5px);
      box-shadow: 
        0 10px 24px -4px rgba(255, 255, 255, 0.2),
        0 4px 12px rgba(0, 0, 0, 0.35);
    }}

    .btn-primary:active {{
      transform: scale(0.985);
      background: #e2e8f0;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
    }}

    .btn-primary .label {{
      font-size: 0.95rem;
      font-weight: 600;
      letter-spacing: -0.015em;
      color: #080a11;
    }}

    .btn-primary .pill-tag {{
      font-size: 0.725rem;
      font-weight: 600;
      padding: 0.25rem 0.6rem;
      border-radius: 9999px;
      background: rgba(8, 10, 17, 0.08);
      color: #334155;
      letter-spacing: 0.01em;
      white-space: nowrap;
    }}

    /* Secondary CTA (Refined Frosted Charcoal Glass) */
    .btn-secondary {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.11);
      color: #e2e8f0;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06);
    }}

    .btn-secondary:hover {{
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-1px);
      color: #ffffff;
    }}

    .btn-secondary:active {{
      transform: scale(0.985);
      background: rgba(255, 255, 255, 0.02);
      border-color: rgba(255, 255, 255, 0.08);
    }}

    .btn-secondary .label {{
      font-size: 0.95rem;
      font-weight: 500;
      letter-spacing: -0.01em;
      color: #f1f5f9;
    }}

    .btn-secondary .pill-tag {{
      font-size: 0.725rem;
      font-weight: 500;
      padding: 0.25rem 0.6rem;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.06);
      color: #94a3b8;
      letter-spacing: 0.01em;
      white-space: nowrap;
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
    <div class="badge-pill">
      <span class="dot"></span>
      <span>JNMC • 2026 to 2027</span>
    </div>

    <header>
      <h1>MBBS Phase III/I Schedule</h1>
      <p class="subtitle">Download the schedule files below and open it with your calendar app of choice</p>
    </header>

    <div class="actions">
      <button class="btn btn-primary" onclick="download('general')" aria-label="Download Schedule for Roll 1 to 202">
        <span class="label">Download Schedule</span>
        <span class="pill-tag">Roll 1 to 202</span>
      </button>

      <button class="btn btn-secondary" onclick="download('batch_b')" aria-label="Download Additional Schedule for Batch B">
        <span class="label">Additional for B batch</span>
        <span class="pill-tag">Ophth SDL & FMT</span>
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

      // Adapted Framer Rings Concentric Dispersion Lens Shader
      const fsSource = `
        precision highp float;
        uniform vec2 u_resolution;
        uniform float u_time;
        uniform vec2 u_mouse;

        const int SAMPLES = 7;
        const float EPHEMERAL_DRIP = 1.0;

        vec3 hash3(vec3 p) {{
            p = vec3(dot(p, vec3(127.1, 311.7, 74.7)),
                     dot(p, vec3(269.5, 183.3, 246.1)),
                     dot(p, vec3(113.5, 271.9, 124.6)));
            return fract(sin(p) * 43758.5453123);
        }}

        vec3 seedRandom(float s) {{
            return hash3(vec3(s, s * 1.5 + 7.31, s * 2.7 + 13.37));
        }}

        // Luxury Ethereal Palette: Midnight Obsidian, Deep Electric Sapphire, Luminous Ice Cyan, Champagne Caustic
        vec3 palette(float t) {{
            vec3 c0 = vec3(0.012, 0.020, 0.045); // Velvet Obsidian
            vec3 c1 = vec3(0.060, 0.220, 0.650); // Deep Electric Sapphire
            vec3 c2 = vec3(0.180, 0.720, 0.880); // Luminous Ice Cyan
            vec3 c3 = vec3(0.960, 0.930, 0.860); // Champagne Platinum Highlight
            
            t = clamp(t, 0.0, 1.0);
            if (t < 0.35) {{
                float f = t / 0.35;
                f = f * f * (3.0 - 2.0 * f);
                return mix(c0, c1, f);
            }} else if (t < 0.70) {{
                float f = (t - 0.35) / 0.35;
                f = f * f * (3.0 - 2.0 * f);
                return mix(c1, c2, f);
            }} else {{
                float f = (t - 0.70) / 0.30;
                f = f * f * (3.0 - 2.0 * f);
                return mix(c2, c3, f);
            }}
        }}

        float getGradientT(vec2 uv, float t, vec2 dir1, vec2 dir2, vec3 freqs, vec2 dir3) {{
            vec2 suv = uv * 1.0;
            float flow = dot(suv, dir1) + sin(dot(suv, dir2) * freqs.x + t) * 0.32 + t * 0.18;
            float flow2 = dot(suv, dir2.yx) + cos(dot(suv, dir1.yx) * freqs.y - t * 0.75) * 0.22;
            
            float gradT = sin(flow * 1.4) * 0.5 + 0.5;
            gradT += cos(flow2 * 1.15) * 1.25;
            gradT += sin(dot(suv, dir3) * freqs.z + t * 3.2) * 1.15;
            
            return smoothstep(0.0, 4.0, gradT);
        }}

        void applyRingLens(vec2 pp, vec2 fragCoord, vec2 r, float iorOffset, vec2 mouseOffset, out vec2 warpedUV, out float edgeFactor) {{
            float u_ringRadius = 1.0;
            float u_ringSpacing = 1.45;
            float u_ringWarpStrength = 3.8;
            float u_lensScale = 10.0;
            
            float radiusSq = u_ringRadius * u_ringRadius;
            vec2 centerPos = vec2(r.x * 0.5, r.y * 0.82) + mouseOffset;
            vec2 lensUV = (fragCoord - centerPos) / r.y * u_lensScale;
            float dist = length(lensUV);
            
            float fw = 0.007 * u_ringSpacing;
            float ringDist = mod(dist, u_ringSpacing) / u_ringSpacing;
            float ringShifted = ringDist - 0.5;
            float localR = ringShifted * 2.0;
            
            float sp = radiusSq - localR * localR;
            float edgeSdf = abs(localR) - u_ringRadius;
            float edgeAA = smoothstep(fw, -fw, edgeSdf);
            
            float lensAmount = smoothstep(0.0, 0.3, sp);
            edgeFactor = (1.0 - smoothstep(0.0, radiusSq, sp)) * lensAmount * edgeAA;
            
            vec2 dir = lensUV / max(dist, 0.001);
            warpedUV = pp;
            if (sp > 0.0) {{
                float lens = sqrt(sp) / max(u_ringRadius, 0.001);
                float baseWarp = mix(1.0, u_ringWarpStrength, lens);
                float warpAmount = baseWarp * (1.0 + iorOffset);
                float ringCenter = (floor(dist / u_ringSpacing) + 0.5) * u_ringSpacing;
                vec2 offset = pp - dir * ringCenter;
                warpedUV = dir * ringCenter + offset * warpAmount;
            }}
        }}

        void main() {{
            vec2 fragCoord = gl_FragCoord.xy;
            vec2 r = u_resolution;
            vec2 p = (fragCoord * 2.0 - r) / r.y;
            
            float u_speed = 0.42;
            float t = u_time * u_speed;
            
            float u_seed = 47.0;
            vec3 seedOff1 = seedRandom(u_seed);
            vec3 seedOff2 = seedRandom(u_seed + 100.0);
            
            float angle1 = seedOff1.x * 6.28318;
            float angle2 = seedOff1.y * 6.28318;
            vec2 dir1 = vec2(cos(angle1), sin(angle1));
            vec2 dir2 = vec2(cos(angle2), sin(angle2));
            vec2 dir3 = dir1 + dir2;
            vec3 freqs = vec3(
                1.0 + seedOff1.z * 2.0,
                1.0 + seedOff2.x * 1.5,
                1.5 + seedOff2.y * 2.0
            );
            
            float u_ringDispersion = 0.38;
            vec3 ringIorOffsets = vec3(-1.0, 0.0, 1.0) * u_ringDispersion;
            
            float u_lensScale = 10.0;
            float u_ephemeralAmp = 0.12;
            float u_edgeDisp = 1.25;
            
            vec2 mouseOffset = (u_mouse - 0.5 * r) * 0.15;
            
            vec3 col = vec3(0.0);
            
            for (int i = 0; i < SAMPLES; i++) {{
                float ephemeral = float(i) / float(SAMPLES);
                float sqEph = ephemeral * ephemeral;
                
                vec2 pt = p;
                pt.x += u_ephemeralAmp * sqEph * sin(p.y * 2.0 + t);
                pt.y += u_ephemeralAmp * sqEph * cos(p.x * 1.5 - t) * 0.5;
                pt.y -= (1.0 - exp(-EPHEMERAL_DRIP * sqEph)) * abs(pt.y) * sign(pt.y) * 0.28;
                
                vec3 tint = smoothstep(1.0, 0.0, abs(3.0 * ephemeral - vec3(1.0, 1.5, 2.0)));
                
                vec3 gradTs = vec3(0.0);
                vec3 edgeFactors = vec3(0.0);
                
                for (int c = 0; c < 3; c++) {{
                    float ior = (c == 0) ? ringIorOffsets.r : ((c == 1) ? ringIorOffsets.g : ringIorOffsets.b);
                    vec2 pp = pt * u_lensScale;
                    vec2 warpedUV;
                    float edgeFactor;
                    applyRingLens(pp, fragCoord, r, ior, mouseOffset, warpedUV, edgeFactor);
                    
                    vec2 gradUV = warpedUV / u_lensScale;
                    float gT = getGradientT(gradUV, t * 0.8, dir1, dir2, freqs, dir3);
                    if (c == 0) {{ gradTs.r = gT; edgeFactors.r = edgeFactor; }}
                    else if (c == 1) {{ gradTs.g = gT; edgeFactors.g = edgeFactor; }}
                    else {{ gradTs.b = gT; edgeFactors.b = edgeFactor; }}
                }}
                
                vec3 convergentColor = palette(gradTs.g);
                float edgeMix = max(max(edgeFactors.r, edgeFactors.g), edgeFactors.b);
                
                vec3 dispersedColor = vec3(
                    palette(gradTs.r).r,
                    convergentColor.g,
                    palette(gradTs.b).b
                );
                
                vec3 finalColor = mix(convergentColor, dispersedColor, edgeMix * 2.0);
                vec3 rainbow = (gradTs - gradTs.g) * 3.0;
                finalColor += rainbow * edgeMix * u_edgeDisp;
                
                col += tint * finalColor * (3.0 / float(SAMPLES));
            }}
            
            // Vignette
            vec2 st = (fragCoord - 0.5 * r) / min(r.x, r.y);
            col *= smoothstep(1.8, 0.35, length(st) * 0.85);
            
            // Film Grain
            float noise = fract(sin(dot(fragCoord, vec2(12.9898, 78.233))) * 43758.5453);
            col += (noise - 0.5) * 0.014;
            
            gl_FragColor = vec4(col, 1.0);
        }}
      `;

      function createShader(gl, type, source) {{
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {{
          console.error(gl.getShaderInfoLog(shader));
        }}
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
        targetMouse[0] = x;
        targetMouse[1] = window.innerHeight - y;
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
        
        currentMouse[0] += (targetMouse[0] - currentMouse[0]) * 0.04;
        currentMouse[1] += (targetMouse[1] - currentMouse[1]) * 0.04;

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

print("Generated index.html with Framer Rings shader and 10/10 design!")
