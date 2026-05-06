from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

_TOPO_CSS = """
#geosym-credit {
    position: fixed;
    bottom: 16px;
    right: 20px;
    font-family: system-ui, sans-serif;
    font-size: 12px;
    color: #c4a882;
    opacity: 0.55;
    text-decoration: none;
    pointer-events: auto;
    z-index: 100;
    letter-spacing: 0.3px;
}
#geosym-credit:hover {
    opacity: 0.9;
}

body::after {
    content: '';
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 220px;
    pointer-events: none;
    z-index: 0;
    opacity: 0.3;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 220' preserveAspectRatio='none'%3E%3Cpolyline points='0,220 80,180 180,195 300,130 420,160 520,90 620,115 720,55 820,80 920,35 1020,60 1120,20 1240,50 1360,30 1440,45 1440,220' fill='none' stroke='%23c4a882' stroke-width='2'/%3E%3Cpolyline points='0,220 100,190 220,205 340,150 460,175 560,115 660,138 760,82 860,105 960,62 1060,88 1160,48 1280,72 1400,55 1440,68 1440,220' fill='none' stroke='%23c4a882' stroke-width='1.5'/%3E%3Cpolyline points='0,220 120,200 260,210 380,168 500,188 600,138 700,158 800,108 900,128 1000,90 1100,112 1200,75 1320,95 1420,80 1440,88 1440,220' fill='none' stroke='%23c4a882' stroke-width='1'/%3E%3Cpolyline points='0,220 140,208 280,215 400,182 520,198 640,158 740,175 840,130 940,148 1040,115 1140,135 1240,100 1360,118 1440,105 1440,220' fill='none' stroke='%23c4a882' stroke-width='0.75'/%3E%3C/svg%3E") no-repeat bottom center;
    background-size: 100% 100%;
}
"""

_CREDIT_HTML = (
    '<a id="geosym-credit" href="https://zackoverend.com"'
    ' target="_blank" rel="noopener">GeoSym &mdash; by Zackary Overend</a>'
)


def scalar_docs() -> HTMLResponse:
    response = get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="GeoSym API",
        custom_css=_TOPO_CSS,
    )
    html = response.body.decode()
    html = html.replace("</body>", f"{_CREDIT_HTML}</body>")
    return HTMLResponse(content=html)
