import os
import re

root_dir = r"H:\portfolio_website\hemalshah"
script_js_path = os.path.join(root_dir, "script.js")

# 1. Remove p5.js script tags from all HTML files
for dirpath, dirnames, filenames in os.walk(root_dir):
    if 'node_modules' in dirnames:
        dirnames.remove('node_modules')
    if '.git' in dirnames:
        dirnames.remove('.git')
        
    for file in filenames:
        if file.endswith('.html'):
            filepath = os.path.join(dirpath, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove any p5.js script tags (1.4.0 or 1.9.0 or with defer)
            content = re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/p5\.js/[0-9\.]+/p5\.min\.js"[^>]*></script>\s*', '', content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

# 2. Rewrite script.js to use HTML5 Canvas instead of p5.js
if os.path.exists(script_js_path):
    with open(script_js_path, 'r', encoding='utf-8') as f:
        script = f.read()
        
    # Replace the invocation
    script = re.sub(
        r'if\s*\(\s*typeof\s+p5\s*!==\s*[\'"]undefined[\'"]\s*\)\s*\{[\s\S]*?initP5Particles\(container\);[\s\S]*?\}\s*else\s*\{[\s\S]*?initCSSParticles\(container\);[\s\S]*?\}',
        'initCanvasParticles(container);',
        script
    )
    
    # Define new Canvas function
    canvas_impl = """function initCanvasParticles(container) {
  const canvas = document.createElement('canvas');
  canvas.style.position = 'absolute';
  canvas.style.top = '0';
  canvas.style.left = '0';
  canvas.style.pointerEvents = 'none';
  container.appendChild(canvas);
  
  const ctx = canvas.getContext('2d');
  
  let width, height;
  const isMobile = window.innerWidth < 600;
  const numParticles = isMobile ? 30 : 60;
  const connectDist  = isMobile ? 70 : 110;
  
  let particles = [];
  
  function resize() {
    width = container.offsetWidth;
    height = container.offsetHeight;
    canvas.width = width;
    canvas.height = height;
  }
  
  window.addEventListener('resize', resize);
  resize();
  
  for (let i = 0; i < numParticles; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.8,
      vy: (Math.random() - 0.5) * 0.8,
      size: Math.random() * 3.5 + 2,
      opacity: Math.random() * 0.4 + 0.2
    });
  }
  
  function draw() {
    ctx.clearRect(0, 0, width, height);
    
    for (let i = 0; i < particles.length; i++) {
      const pt = particles[i];
      pt.x += pt.vx;
      pt.y += pt.vy;
      
      if (pt.x < 0) pt.x = width;
      if (pt.x > width) pt.x = 0;
      if (pt.y < 0) pt.y = height;
      if (pt.y > height) pt.y = 0;
      
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, pt.size / 2, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${pt.opacity})`;
      ctx.fill();
      
      for (let j = i + 1; j < particles.length; j++) {
        const other = particles[j];
        const dx = pt.x - other.x;
        const dy = pt.y - other.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist < connectDist) {
          const alpha = (1 - dist / connectDist) * 0.35;
          ctx.beginPath();
          ctx.moveTo(pt.x, pt.y);
          ctx.lineTo(other.x, other.y);
          ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`;
          ctx.lineWidth = 0.6;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  
  draw();
}"""

    # Replace the old initP5Particles implementation
    script = re.sub(
        r'function initP5Particles\(container\)\s*\{[\s\S]*?p\.windowResized\s*=\s*function\s*\(\)\s*\{[\s\S]*?p\.resizeCanvas\(container\.offsetWidth,\s*container\.offsetHeight\);[\s\S]*?\};\s*\}\);\s*\}',
        canvas_impl,
        script
    )
    
    # We must also bump the cache version of script.js from ?v=1.1 to ?v=1.2 globally
    # but since this script runs immediately, maybe no need, or we can just bump it.
    
    with open(script_js_path, 'w', encoding='utf-8') as f:
        f.write(script)

# 3. Bump cache version to v=1.2 for script.js
for dirpath, dirnames, filenames in os.walk(root_dir):
    if 'node_modules' in dirnames:
        dirnames.remove('node_modules')
    if '.git' in dirnames:
        dirnames.remove('.git')
        
    for file in filenames:
        if file.endswith('.html'):
            filepath = os.path.join(dirpath, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace("script.js?v=1.1", "script.js?v=1.2")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

print("Replaced p5.js with native HTML5 Canvas API globally and bumped cache version.")
