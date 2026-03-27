import os
import glob
import html
import shutil

# Configuration
SOURCE_DIR = "/Users/ijaegwang/wordncode/Work/K/KRDS/node_modules/krds-uiux/html/code"
OUTPUT_FILE = "/Users/ijaegwang/wordncode/Work/K/KRDS/index.html"
PREVIEWS_DIR = "/Users/ijaegwang/wordncode/Work/K/KRDS/previews"

HTML_TEMPLATE_START = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KRDS Component Showcase</title>
    <link href="https://cdn.jsdelivr.net/npm/krds-uiux@1.0.3/resources/cdn/krds.min.css" type="text/css" rel="stylesheet" />
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-gov-dynamic-subset.min.css" />
    
    <style>
        :root {
            --bg-mesh: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            --glass-bg: rgba(255, 255, 255, 0.5);
            --glass-border: rgba(255, 255, 255, 0.6);
            --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
            
            --text-main: #1e293b;
            --text-sub: #64748b;
            --header-bg: rgba(255, 255, 255, 0.2);
            
            --modal-bg: rgba(255, 255, 255, 0.7);
            --modal-header-bg: rgba(255, 255, 255, 0.3);
            
            --pill-bg: #1a1a1a;
            --pill-active: #ffffff;
            --pill-text-active: #1a1a1a;
            --pill-text-inactive: #a3a3a3;
            
            --iframe-bg: #ffffff;
            --view-btn: #2563eb;
            --view-btn-hover: #1e40af;
            --badge-bg: rgba(3, 105, 161, 0.1);
            --badge-text: #0284c7;
        }

        [data-theme="dark"] {
            --bg-mesh: linear-gradient(135deg, #020617 0%, #0f172a 100%);
            --glass-bg: rgba(15, 23, 42, 0.6);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --header-bg: rgba(0, 0, 0, 0.3);
            
            --modal-bg: rgba(15, 23, 42, 0.8);
            --modal-header-bg: rgba(0, 0, 0, 0.4);
            
            --pill-bg: #000000;
            --pill-active: #334155;
            --pill-text-active: #ffffff;
            --pill-text-inactive: #64748b;
            
            --iframe-bg: #ffffff;
            --view-btn: #60a5fa;
            --view-btn-hover: #93c5fd;
            --badge-bg: rgba(56, 189, 248, 0.2);
            --badge-text: #38bdf8;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Pretendard', sans-serif;
            background: var(--bg-mesh);
            color: var(--text-main);
            line-height: 1.6;
            margin: 0;
            min-height: 100vh;
            overflow-x: hidden;
            transition: background 0.3s, color 0.3s;
        }

        .bg-shapes {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; overflow: hidden; pointer-events: none;
        }
        .shape {
            position: absolute; filter: blur(100px); border-radius: 50%; opacity: 0.6; animation: float 15s infinite ease-in-out alternate;
        }
        .shape-1 { top: -10%; left: -10%; width: 60vw; height: 60vw; background: rgba(59, 130, 246, 0.3); } 
        .shape-2 { bottom: -10%; right: -10%; width: 50vw; height: 50vw; background: rgba(139, 92, 246, 0.3); } 
        .shape-3 { top: 40%; left: 40%; width: 40vw; height: 40vw; background: rgba(16, 185, 129, 0.15); } 
        [data-theme="dark"] .shape { opacity: 0.3; }

        @keyframes float {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(5%, 10%) scale(1.1); }
        }

        header {
            background: var(--header-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--glass-border);
            padding: 60px 20px;
            text-align: center;
            margin-bottom: 40px;
        }
        header h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 10px; color: var(--text-main); }
        header p { font-size: 1.1rem; color: var(--text-sub); max-width: 600px; margin: 0 auto; }

        .container { max-width: 100%; margin: 0 auto; padding: 0 40px 60px; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 30px; }
        @media (max-width: 1024px) {
            .grid { grid-template-columns: 1fr; }
            .container { padding: 0 20px 40px; }
        }

        .card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            box-shadow: var(--glass-shadow);
            border: 1px solid var(--glass-border);
            display: flex; flex-direction: column; overflow: hidden;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15); border-color: rgba(255, 255, 255, 0.8); }
        [data-theme="dark"] .card:hover { border-color: rgba(255, 255, 255, 0.3); }

        .card-header {
            padding: 24px 24px 10px 24px;
            font-weight: 700; font-size: 18px;
            color: var(--text-main);
            display: flex; justify-content: space-between; align-items: center;
        }
        .card-header .badge {
            background: var(--badge-bg); color: var(--badge-text);
            font-size: 0.75rem; padding: 4px 10px; border-radius: 20px; font-weight: 700; text-transform: uppercase;
        }

        .card-body { padding: 0 24px 24px 24px; display: flex; flex-direction: column; flex-grow: 1; cursor: pointer; }

        .summary-preview {
            background: var(--iframe-bg);
            border-radius: 12px; overflow: hidden; height: 250px;
            margin-top: 15px; margin-bottom: 15px; position: relative;
            border: 1px solid rgba(0,0,0,0.05);
        }
        .card-iframe { width: 100%; height: 100%; border: none; pointer-events: none; }
        
        .view-btn { text-align: right; color: var(--view-btn); font-weight: 600; font-size: 0.95rem; transition: color 0.2s; }
        .card-body:hover .view-btn { color: var(--view-btn-hover); text-decoration: underline; }

        footer { text-align: center; padding: 40px; color: var(--text-sub); font-size: 0.9rem; border-top: 1px solid var(--glass-border); margin-top: 40px; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .card { animation: fadeIn 0.6s ease-out backwards; }

        .custom-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 9999; }
        .custom-modal.active { display: block; }
        .custom-modal-backdrop {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
        }
        .custom-modal-dialog {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 90%; max-width: 1400px; height: 90vh;
            background: var(--modal-bg);
            backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--glass-border); border-radius: 24px;
            display: flex; flex-direction: column;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
            animation: modalIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes modalIn { from { opacity: 0; transform: translate(-50%, -45%) scale(0.96); } to { opacity: 1; transform: translate(-50%, -50%) scale(1); } }
        
        .custom-modal-header {
            background: var(--modal-header-bg);
            padding: 24px 32px 0 32px; border-bottom: none;
            display: flex; justify-content: space-between; align-items: center; border-radius: 24px 24px 0 0; flex-shrink: 0;
        }
        .custom-modal-header h2 { font-size: 1.5rem; color: var(--text-main); margin: 0; }
        .custom-modal-close { background: none; border: none; font-size: 2rem; cursor: pointer; color: var(--text-sub); line-height: 1; transition: color 0.2s; }
        .custom-modal-close:hover { color: var(--text-main); }
        
        .modal-tabs {
            background: var(--modal-header-bg); display: flex; justify-content: center; padding: 20px 32px 24px 32px;
            border-bottom: 1px solid var(--glass-border); flex-shrink: 0;
        }
        .segmented-control { display: inline-flex; background-color: var(--pill-bg); border-radius: 50px; padding: 6px; }
        .tab-btn { background: transparent; border: none; padding: 10px 32px; font-size: 16px; font-weight: 600; color: var(--pill-text-inactive); cursor: pointer; border-radius: 40px; transition: all 0.3s ease; }
        .tab-btn.active { background-color: var(--pill-active); color: var(--pill-text-active); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        
        .custom-modal-body { flex-grow: 1; position: relative; background: transparent; border-radius: 0 0 24px 24px; overflow: hidden; padding: 0; }
        
        #modalPreview { display: flex; flex-direction: column; height: 100%; }
        #modalPreview iframe { width: 100%; height: 100%; border: none; background: var(--iframe-bg); border-radius: 0 0 24px 24px; }
        
        #modalCode { display: none; background: rgba(0,0,0,0.85); padding: 24px; overflow-y: auto; }
        
        .copy-btn { position: absolute; top: 16px; right: 16px; background: rgba(255,255,255,0.1); color: #ffffff; border: 1px solid rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 0.9rem; font-weight: 600; transition: all 0.2s; z-index: 10; }
        .copy-btn:hover { background: rgba(255,255,255,0.2); }
        
        .theme-toggle-btn {
            position: fixed; bottom: 40px; right: 40px; width: 56px; height: 56px; border-radius: 50%;
            background: var(--glass-bg); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border); box-shadow: var(--glass-shadow);
            color: var(--text-main); font-size: 24px; display: flex; align-items: center; justify-content: center;
            cursor: pointer; z-index: 1000; transition: all 0.3s;
        }
        .theme-toggle-btn:hover { transform: scale(1.1) rotate(15deg); }
    </style>
</head>
<body>
    <div class="bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
    </div>

    <header>
        <h1>KRDS Component Showcase</h1>
        <p>A beautifully curated collection of 74 UI components from the official 대한민국 디지털 정부 서비스 (KRDS) Design System.</p>
    </header>

    <div class="container">
        <div class="grid">
"""

HTML_TEMPLATE_END = """
        </div>
    </div>

    <footer>
        <p>&copy; 2026 KRDS Design System Integration. All rights reserved.</p>
    </footer>

    <!-- Theme Toggle -->
    <button id="themeToggle" class="theme-toggle-btn" onclick="toggleTheme()" title="Toggle Dark/Light Mode">🌙</button>

    <!-- Custom Modal -->
    <div id="componentModal" class="custom-modal">
        <div class="custom-modal-backdrop" onclick="closeModal()"></div>
        <div class="custom-modal-dialog">
            <div class="custom-modal-header">
                <h2 id="modalTitle">Component Name</h2>
                <button class="custom-modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-tabs">
                <div class="segmented-control">
                    <button id="tab-btn-preview" class="tab-btn active" onclick="switchTab('preview')">미리보기</button>
                    <button id="tab-btn-code" class="tab-btn" onclick="switchTab('code')">코드보기</button>
                </div>
            </div>
            <div class="custom-modal-body" id="modalPreview">
                <!-- Iframe injected via JS -->
            </div>
            <div class="custom-modal-body" id="modalCode">
                <button class="copy-btn" onclick="copyCode()">복사하기 📋</button>
                <pre><code id="codeBlock" style="color: #6ee7b7; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 14px; white-space: pre-wrap; word-break: break-all;"></code></pre>
            </div>
        </div>
    </div>

    <script>
        // Theme initialization
        function initTheme() {
            const savedTheme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', savedTheme);
            document.getElementById('themeToggle').innerText = savedTheme === 'dark' ? '☀️' : '🌙';
        }
        initTheme();

        function toggleTheme() {
            const root = document.documentElement;
            const isDark = root.getAttribute('data-theme') === 'dark';
            const newTheme = isDark ? 'light' : 'dark';
            root.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            document.getElementById('themeToggle').innerText = newTheme === 'dark' ? '☀️' : '🌙';
        }

        function openModal(idx, title) {
            document.getElementById('modalTitle').innerText = title;
            const iframeHTML = `<iframe src="previews/component_${idx}.html"></iframe>`;
            document.getElementById('modalPreview').innerHTML = iframeHTML;
            const codeHTML = document.getElementById('code-' + idx).innerHTML;
            document.getElementById('codeBlock').innerHTML = codeHTML;
            document.getElementById('componentModal').classList.add('active');
            document.body.style.overflow = 'hidden'; 
            switchTab('preview');
        }
        
        function switchTab(tabName) {
            if (tabName === 'preview') {
                document.getElementById('modalPreview').style.display = 'block';
                document.getElementById('modalCode').style.display = 'none';
                document.getElementById('tab-btn-preview').classList.add('active');
                document.getElementById('tab-btn-code').classList.remove('active');
            } else {
                document.getElementById('modalPreview').style.display = 'none';
                document.getElementById('modalCode').style.display = 'block';
                document.getElementById('tab-btn-preview').classList.remove('active');
                document.getElementById('tab-btn-code').classList.add('active');
            }
        }
        
        function copyCode() {
            const codeText = document.getElementById('codeBlock').innerText;
            navigator.clipboard.writeText(codeText).then(() => {
                const btn = document.querySelector('.copy-btn');
                btn.innerText = '복사완료! ✔️';
                setTimeout(() => { btn.innerText = '복사하기 📋'; }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                alert('복사에 실패했습니다.');
            });
        }
        
        function closeModal() {
            document.getElementById('componentModal').classList.remove('active');
            setTimeout(() => {
                document.getElementById('modalPreview').innerHTML = '';
            }, 200);
            document.body.style.overflow = '';
        }
    </script>
</body>
</html>
"""

PREVIEW_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KRDS Component Preview</title>
    <script defer src="https://cdn.jsdelivr.net/npm/krds-uiux@1.0.3/resources/cdn/krds.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/krds-uiux@1.0.3/resources/cdn/krds.min.css" type="text/css" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <link rel="stylesheet" href="../node_modules/krds-uiux/resources/css/common/common.css" />
    <style>
        body { margin: 0; padding: 24px; background-color: transparent; }
    </style>
</head>
<body>
{component_content}
</body>
</html>
"""

def generate_index():
    if os.path.exists(PREVIEWS_DIR):
        shutil.rmtree(PREVIEWS_DIR)
    os.makedirs(PREVIEWS_DIR)

    html_files = glob.glob(os.path.join(SOURCE_DIR, "*.html"))
    html_files.sort()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write(HTML_TEMPLATE_START)
        
        for idx, file_path in enumerate(html_files):
            filename = os.path.basename(file_path)
            title = filename.replace('.html', '').replace('_', ' ').title()
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            preview_filepath = os.path.join(PREVIEWS_DIR, f"component_{idx}.html")
            with open(preview_filepath, 'w', encoding='utf-8') as pf:
                pf.write(PREVIEW_TEMPLATE.replace("{component_content}", content))

            escaped_html = html.escape(content.strip())
            
            delay = (idx % 10) * 0.05
            outfile.write(f'            <div class="card" style="animation-delay: {delay}s;">\n')
            outfile.write(f'                <div class="card-header">\n')
            outfile.write(f'                    {title} <span class="badge">Component</span>\n')
            outfile.write(f'                </div>\n')
            outfile.write(f'                <div class="card-body" onclick=\'openModal({idx}, "{title}")\'>\n')
            outfile.write(f'                    <div class="summary-preview">\n')
            outfile.write(f'                        <iframe src="previews/component_{idx}.html" loading="lazy" class="card-iframe"></iframe>\n')
            outfile.write(f'                    </div>\n')
            outfile.write(f'                    <div class="view-btn">컴포넌트 보기 &rarr;</div>\n')
            outfile.write(f'                </div>\n')
            
            outfile.write(f'                <template id="code-{idx}">\n')
            outfile.write(f'{escaped_html}\n')
            outfile.write(f'                </template>\n')
            
            outfile.write(f'            </div>\n')
            
        outfile.write(HTML_TEMPLATE_END)
        
    print(f"Index generated successfully at {OUTPUT_FILE} with {len(html_files)} components.")

if __name__ == "__main__":
    generate_index()
