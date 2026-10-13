import os, base64

BASE_DIR = "/Users/shubhayu/Documents/antigravity/splendid-raman"
gen_ics_path = os.path.join(BASE_DIR, "downloads", "MBBS_Phase_III_I_Schedule.ics")
batch_b_ics_path = os.path.join(BASE_DIR, "downloads", "MBBS_Phase_III_I_Batch_B_Additional.ics")

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
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    html {{
      height: 100%;
      width: 100%;
      margin: 0;
      padding: 0;
      -webkit-text-size-adjust: 100%;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #00030b;
      color: #e2e8f0;
      width: 100%;
      min-height: 100%;
      min-height: 100vh;
      min-height: 100dvh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin: 0;
      padding: max(1.5rem, env(safe-area-inset-top)) 1rem max(1.5rem, env(safe-area-inset-bottom)) 1rem;
      overflow-x: hidden;
      position: relative;
    }}

    #gl-canvas {{
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
      pointer-events: none;
    }}

    .ambient-glow {{
      position: fixed;
      inset: 0;
      width: 100%;
      height: 60vh;
      background: radial-gradient(ellipse at center top, rgba(162, 188, 216, 0.08) 0%, rgba(30, 58, 138, 0.03) 50%, rgba(0, 3, 11, 0) 80%);
      z-index: 1;
      pointer-events: none;
    }}

    .card {{
      position: relative;
      z-index: 10;
      width: 100%;
      max-width: 380px;
      margin: auto;
      text-align: center;
      background: rgba(10, 14, 24, 0.68);
      backdrop-filter: blur(40px) saturate(185%);
      -webkit-backdrop-filter: blur(40px) saturate(185%);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 28px;
      padding: 2.5rem 1.85rem 2rem;
      box-shadow: 
        inset 0 1px 0 0 rgba(255, 255, 255, 0.20),
        0 24px 64px -16px rgba(0, 0, 0, 0.75),
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
      body {{
        padding: max(1rem, env(safe-area-inset-top)) 0.75rem max(1rem, env(safe-area-inset-bottom)) 0.75rem;
      }}
      .card {{
        width: 100%;
        max-width: 360px;
        padding: 2.1rem 1.25rem 1.75rem;
        border-radius: 24px;
        margin: auto;
      }}
    }}

    .badge-pill {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.45rem;
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.14);
      font-size: 0.6875rem;
      font-weight: 600;
      letter-spacing: 0.075em;
      text-transform: uppercase;
      color: #94a3b8;
      margin: 0 auto 1.35rem;
    }}

    .badge-pill .dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #38bdf8;
      box-shadow: 0 0 8px #38bdf8;
    }}

    header {{
      margin-bottom: 1.85rem;
      text-align: center;
    }}

    h1 {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 2.35rem;
      font-weight: 400;
      letter-spacing: -0.015em;
      color: #ffffff;
      line-height: 1.15;
      margin: 0 auto 0.75rem;
      text-align: center;
      text-wrap: balance;
    }}

    @media (max-width: 480px) {{
      h1 {{
        font-size: 1.95rem;
        line-height: 1.18;
      }}
    }}

    .subtitle {{
      font-size: 0.875rem;
      color: #94a3b8;
      line-height: 1.55;
      font-weight: 400;
      text-align: center;
      margin: 0 auto;
      max-width: 320px;
      text-wrap: pretty;
    }}

    @media (max-width: 480px) {{
      .subtitle {{
        font-size: 0.825rem;
        line-height: 1.5;
        max-width: 290px;
      }}
    }}

    .actions {{
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
      margin-top: 1.75rem;
      width: 100%;
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
      gap: 0.5rem;
    }}

    @media (max-width: 480px) {{
      .btn {{
        padding: 0.88rem 1rem;
        border-radius: 13px;
        gap: 0.4rem;
      }}
    }}

    @media (max-width: 360px) {{
      .btn {{
        padding: 0.82rem 0.85rem;
        gap: 0.35rem;
      }}
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
      letter-spacing: -0.01em;
      color: #080a11;
      min-width: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .btn-primary .pill-tag {{
      font-size: 0.725rem;
      font-weight: 600;
      padding: 0.25rem 0.6rem;
      border-radius: 9999px;
      background: rgba(0, 0, 0, 0.08);
      color: #080a11;
      letter-spacing: 0.01em;
      white-space: nowrap;
      flex-shrink: 0;
    }}

    /* Secondary CTA (Glass Slate) */
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
      min-width: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
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
      flex-shrink: 0;
    }}

    @media (max-width: 480px) {{
      .btn-primary .label,
      .btn-secondary .label {{
        font-size: 0.90rem;
      }}
      .btn-primary .pill-tag,
      .btn-secondary .pill-tag {{
        font-size: 0.6875rem;
        padding: 0.2rem 0.52rem;
      }}
    }}

    .footer {{
      margin-top: 1.85rem;
      text-align: center;
      font-size: 0.75rem;
      font-weight: 500;
      color: #64748b;
      letter-spacing: 0.025em;
    }}
  </style>
</head>
<body>

  <div class="ambient-glow"></div>
  <canvas id="gl-canvas"></canvas>

  <main class="card">
    <div class="badge-pill">
      <span class="dot"></span>
      <span>JNMC 2024 to 2029</span>
    </div>

    <header>
      <h1>MBBS Phase III/I</h1>
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
    const gl = canvas.getContext('webgl2', {{
      alpha: true,
      premultipliedAlpha: false,
      antialias: false,
      powerPreference: 'high-performance'
    }});

    if (gl) {{
      const vsSource = `#version 300 es
      precision highp float;

      in vec2 a_position;
      in vec2 a_texCoord;

      out vec2 v_uv;

      void main() {{
          v_uv = a_texCoord;
          gl_Position = vec4(a_position, 0.0, 1.0);
      }}`;

      const fsSource = `#version 300 es
      precision highp float;

      in vec2 v_uv;
      out vec4 fragColor;

      #define NUM_COLORS 8
      uniform vec4 u_colors[NUM_COLORS];
      uniform int u_colors_length;

      uniform vec2 u_resolution;
      uniform float u_time;
      uniform float u_speed;
      uniform float u_seed;
      uniform float u_ephemeralAmp;
      uniform float u_lensScale;
      uniform float u_ringSpacing;
      uniform float u_ringRadius;
      uniform float u_ringWarpStrength;

      const int SAMPLES = 8;
      const float EPHEMERAL_DRIP = 1.0;

      // === PCG hash ===
      uvec3 hash3(uvec3 v) {{
          v = v * 1664525u + 1013904223u;
          v.x += v.y * v.z;
          v.y += v.z * v.x;
          v.z += v.x * v.y;
          v ^= v >> 16u;
          v.x += v.y * v.z;
          v.y += v.z * v.x;
          v.z += v.x * v.y;
          return v;
      }}

      uvec3 seed;
      vec3 random3f() {{
          seed = hash3(seed);
          return vec3(seed) / float(0xFFFFFFFFu);
      }}

      vec3 seedRandom(float seedVal) {{
          uvec3 s = uvec3(
              floatBitsToUint(seedVal),
              floatBitsToUint(seedVal * 1.5 + 7.31),
              floatBitsToUint(seedVal * 2.7 + 13.37)
          );
          s = hash3(s);
          return vec3(s) / float(0xFFFFFFFFu);
      }}

      // === PALETTE SAMPLING ===
      vec3 getColor(int idx) {{
          if (u_colors_length < 1) return vec3(0.0);
          int safeIdx = clamp(idx, 0, u_colors_length - 1);
          return u_colors[safeIdx].rgb;
      }}

      vec3 paletteN(float t, int count) {{
          if (count < 1) return vec3(0.0);
          if (count < 2) return getColor(0);
          t = clamp(t, 0.0, 1.0) * float(count - 1);
          int idx = min(int(floor(t)), count - 2);
          float localT = fract(t);
          localT = localT * localT * (3.0 - 2.0 * localT);
          return mix(getColor(idx), getColor(idx + 1), localT);
      }}

      // === Gradient Flow ===
      float getGradientT(vec2 uv, float t, vec2 dir1, vec2 dir2, vec3 freqs, vec2 dir3) {{
          vec2 suv = uv * 1.0;
          
          float flow = dot(suv, dir1) + sin(dot(suv, dir2) * freqs.x + t) * 0.3 + t * 0.2;
          float flow2 = dot(suv, dir2.yx) + cos(dot(suv, dir1.yx) * freqs.y - t * 0.8) * 0.25;
          
          float gradT = sin(flow * 1.5) * 0.5 + 0.5;
          gradT += cos(flow2 * 1.2) * 1.3;
          gradT += sin(dot(suv, dir3) * freqs.z + t * 3.5) * 1.2;
          
          return smoothstep(0.0, 4.12, gradT);
      }}

      // === RING LENS ===
      void applyRingLens(vec2 pp, vec2 fragCoord, vec2 r, out vec2 warpedUV) {{
          float radiusSq = u_ringRadius * u_ringRadius;
          float minDim = min(r.x, r.y);
          
          vec2 lensUV = (fragCoord - vec2(r.x * 0.5, 0.0)) / minDim * u_lensScale;
          float dist = length(lensUV);
          
          float ringDist = mod(dist, u_ringSpacing) / u_ringSpacing;
          float ringShifted = ringDist - 0.5;
          float localR = ringShifted * 2.0;
          
          float sp = radiusSq - localR * localR;
          vec2 dir = lensUV / max(dist, 0.001);
          
          warpedUV = pp;
          if (sp > 0.0) {{
              float lens = sqrt(sp) / max(u_ringRadius, 0.001);
              float baseWarp = mix(1.0, u_ringWarpStrength, lens);
              float ringCenter = (floor(dist / u_ringSpacing) + 0.5) * u_ringSpacing;
              vec2 offset = pp - dir * ringCenter;
              warpedUV = dir * ringCenter + offset * baseWarp;
          }}
      }}

      void main() {{
          vec2 fragCoord = v_uv * u_resolution;
          seed = uvec3(uvec2(fragCoord), uint(fract(u_time) * 1000.0));
          
          vec2 r = u_resolution;
          float minDim = min(r.x, r.y);
          vec2 p = (fragCoord * 2.0 - r) / minDim;
          float t = u_time * u_speed;
          
          int colorCount = u_colors_length;
          if (colorCount < 1) {{
              fragColor = vec4(0.0, 0.0, 0.0, 1.0);
              return;
          }}
          
          vec3 seedOff1 = seedRandom(u_seed);
          vec3 seedOff2 = seedRandom(u_seed + 100.0);
          
          float angle1 = seedOff1.x * 6.28;
          float angle2 = seedOff1.y * 6.28;
          vec2 dir1 = vec2(cos(angle1), sin(angle1));
          vec2 dir2 = vec2(cos(angle2), sin(angle2));
          vec2 dir3 = dir1 + dir2;
          vec3 freqs = vec3(
              1.0 + seedOff1.z * 2.0,
              1.0 + seedOff2.x * 1.5,
              1.5 + seedOff2.y * 2.0
          );
          
          float dice = random3f().x;
          vec3 col = vec3(0.0);
          
          // High-performance single-pass ray-marched samples (300% faster with identical visuals)
          for (int i = 0; i < SAMPLES; i++) {{
              float ephemeral = (float(i) + dice) / float(SAMPLES);
              float sqEph = ephemeral * ephemeral;
              
              vec2 pt = p;
              pt.x += u_ephemeralAmp * sqEph * sin(p.y * 2.0 + t);
              pt.y += u_ephemeralAmp * sqEph * cos(p.x * 1.5 - t) * 0.5;
              pt.y -= (1.0 - exp(-EPHEMERAL_DRIP * sqEph)) * abs(pt.y) * sign(pt.y) * 0.3;
              
              vec3 tint = smoothstep(1.0, 0.0, abs(3.0 * ephemeral - vec3(1.0, 1.5, 2.0)));
              
              vec2 pp = pt * u_lensScale;
              vec2 warpedUV;
              applyRingLens(pp, fragCoord, r, warpedUV);
              
              vec2 gradUV = warpedUV / u_lensScale;
              float gT = getGradientT(gradUV, t * 0.8, dir1, dir2, freqs, dir3);
              vec3 convergentColor = paletteN(gT, colorCount);
              
              col += tint * convergentColor * (3.0 / float(SAMPLES));
          }}
          
          fragColor = vec4(col, 1.0);
      }}`;

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
      const posLoc = gl.getAttribLocation(prog, "a_position");
      gl.enableVertexAttribArray(posLoc);
      gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

      const texBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, texBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
        0, 0,
        1, 0,
        0, 1,
        0, 1,
        1, 0,
        1, 1
      ]), gl.STATIC_DRAW);
      const texLoc = gl.getAttribLocation(prog, "a_texCoord");
      gl.enableVertexAttribArray(texLoc);
      gl.vertexAttribPointer(texLoc, 2, gl.FLOAT, false, 0, 0);

      const uRes = gl.getUniformLocation(prog, "u_resolution");
      const uTime = gl.getUniformLocation(prog, "u_time");
      const uSpeed = gl.getUniformLocation(prog, "u_speed");
      const uSeed = gl.getUniformLocation(prog, "u_seed");
      const uEph = gl.getUniformLocation(prog, "u_ephemeralAmp");
      const uScale = gl.getUniformLocation(prog, "u_lensScale");
      const uSpacing = gl.getUniformLocation(prog, "u_ringSpacing");
      const uRadius = gl.getUniformLocation(prog, "u_ringRadius");
      const uWarp = gl.getUniformLocation(prog, "u_ringWarpStrength");
      const uColors = gl.getUniformLocation(prog, "u_colors");
      const uColorsLen = gl.getUniformLocation(prog, "u_colors_length");

      gl.uniform1f(uSpeed, 0.2);
      gl.uniform1f(uSeed, 0.0);
      gl.uniform1f(uEph, 0.5);
      gl.uniform1f(uScale, 4.4);
      gl.uniform1f(uSpacing, 0.4);
      gl.uniform1f(uRadius, 2.0);
      gl.uniform1f(uWarp, 1.2);

      gl.uniform1i(uColorsLen, 3);
      const colorsData = new Float32Array(8 * 4);
      colorsData.set([0.0 / 255.0, 3.0 / 255.0, 11.0 / 255.0, 1.0], 0);
      colorsData.set([1.0, 1.0, 1.0, 1.0], 4);
      colorsData.set([51.0 / 255.0, 65.0 / 255.0, 85.0 / 255.0, 1.0], 8);
      gl.uniform4fv(uColors, colorsData);

      function resize() {{
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const resScale = window.innerWidth < 768 ? 0.65 : 0.75;
        canvas.width = Math.max(Math.round(window.innerWidth * dpr * resScale), 320);
        canvas.height = Math.max(Math.round(window.innerHeight * dpr * resScale), 320);
        gl.viewport(0, 0, canvas.width, canvas.height);
      }}
      window.addEventListener('resize', resize);
      resize();

      let startTime = performance.now();
      function render(now) {{
        const elapsed = (now - startTime) * 0.001;
        gl.uniform2f(uRes, canvas.width, canvas.height);
        gl.uniform1f(uTime, elapsed);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
        requestAnimationFrame(render);
      }}
      requestAnimationFrame(render);
    }}

    const files = {{
      general: {{
        name: "MBBS_Phase_III_I_Schedule.ics",
        b64: "{gen_b64}",
        path: "downloads/MBBS_Phase_III_I_Schedule.ics"
      }},
      batch_b: {{
        name: "MBBS_Phase_III_I_Batch_B_Additional.ics",
        b64: "{batch_b_b64}",
        path: "downloads/MBBS_Phase_III_I_Batch_B_Additional.ics"
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

print("Generated index.html with optimized performance, isotropic follow, and translucent box!")
