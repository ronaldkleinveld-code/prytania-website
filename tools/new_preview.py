#!/usr/bin/env python3
"""Create a new unlisted project-preview page for prytaniapartners.com.

Usage:
    python3 tools/new_preview.py "Project title" "Client name"

Creates site/p/<random-slug>/index.html (plus an empty draft/ folder)
and prints the private URL to share with the client.
"""
import re
import secrets
import sys
from datetime import date
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent  # repo root = site root

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Private preview — {title}</title>
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="referrer" content="no-referrer">
<link rel="stylesheet" href="/styles.css">
</head>
<body>

<div class="preview-banner">Private client preview — please do not share this link</div>

<header class="site">
  <div class="wrap">
    <a class="brand" href="/"><svg width="19" height="23" viewBox="0 0 76 94" style="vertical-align:-4px;margin-right:9px" aria-hidden="true"><rect x="0" y="0" width="76" height="8" rx="2" fill="#12233d"/><rect x="6" y="12" width="64" height="6" rx="2" fill="#b08d3f"/><rect x="12" y="22" width="10" height="50" rx="2" fill="#12233d"/><rect x="33" y="22" width="10" height="50" rx="2" fill="#12233d"/><rect x="54" y="22" width="10" height="50" rx="2" fill="#12233d"/><rect x="6" y="76" width="64" height="6" rx="2" fill="#b08d3f"/><rect x="0" y="86" width="76" height="8" rx="2" fill="#12233d"/></svg>Prytania <span>Partners</span></a>
  </div>
</header>

<section>
  <div class="wrap">
    <div class="eyebrow">Project preview</div>
    <h2>{title}</h2>
    <div class="prose">
      <p>This is a private, work-in-progress preview shared with you by Prytania Partners. It reflects the current state of the project and will change as work continues.</p>
    </div>

    <ul class="meta-list">
      <li><strong>Client</strong> {client}</li>
      <li><strong>Status</strong> In progress — draft for review</li>
      <li><strong>Last updated</strong> {updated}</li>
      <li><strong>Feedback to</strong> <a href="mailto:info@prytaniapartners.com">info@prytaniapartners.com</a></li>
    </ul>

    <div class="frame-bar">
      <a class="fs-open" href="draft/index.html" target="_blank" rel="noopener">Open in new tab &#8599;</a>
      <button type="button" class="fs-btn" id="fsBtn">&#x26F6; Full screen</button>
    </div>
    <div class="preview-frame" id="pFrame">
      <button type="button" class="fs-exit" id="fsExit">&#10005; Exit full screen</button>
      <iframe src="draft/index.html" title="Project draft preview"></iframe>
    </div>
    <script>
      (function () {{
        var f = document.getElementById('pFrame');
        var b = document.getElementById('fsBtn');
        var x = document.getElementById('fsExit');
        function set(on) {{
          f.classList.toggle('fullscreen', on);
          document.body.classList.toggle('noscroll', on);
        }}
        b.addEventListener('click', function () {{ set(true); }});
        x.addEventListener('click', function () {{ set(false); }});
        document.addEventListener('keydown', function (e) {{ if (e.key === 'Escape') set(false); }});
      }})();
    </script>
  </div>
</section>

<footer class="site">
  <div class="wrap">
    <div>&copy; {year} Prytania Partners B.V. — Confidential preview</div>
  </div>
</footer>

</body>
</html>
"""


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('Usage: new_preview.py "Project title" ["Client name"]')
    title = sys.argv[1]
    client = sys.argv[2] if len(sys.argv) > 2 else "—"

    slug = secrets.token_urlsafe(9)  # ~72 bits, e.g. q6aN2EjKG4xT
    slug = re.sub(r"[^A-Za-z0-9_-]", "", slug)

    folder = SITE / "p" / slug
    (folder / "draft").mkdir(parents=True)
    (folder / "index.html").write_text(
        TEMPLATE.format(
            title=title,
            client=client,
            updated=date.today().strftime("%-d %B %Y"),
            year=date.today().year,
        ),
        encoding="utf-8",
    )
    (folder / "draft" / "index.html").write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<meta name='robots' content='noindex, nofollow'>"
        f"<title>Draft — {title}</title></head>"
        "<body><p>Put the work-in-progress draft here.</p></body></html>",
        encoding="utf-8",
    )

    print("Created:", folder)
    print("Private URL: https://www.prytaniapartners.com/p/%s/" % slug)


if __name__ == "__main__":
    main()
