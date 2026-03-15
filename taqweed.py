import os
from datetime import date, datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape
from flask import Flask, abort, make_response, render_template, request, Response, url_for

app = Flask(__name__, static_folder='static', template_folder='templates')


def get_template_last_modified(template_name: str) -> str:
    templates_dir = app.jinja_loader.searchpath[0]
    template_path = os.path.join(templates_dir, template_name)
    if os.path.isfile(template_path):
        dt = datetime.fromtimestamp(os.path.getmtime(template_path), tz=timezone.utc)
        # HTTP header expects GMT time
        return format_datetime(dt, usegmt=True)
    return format_datetime(datetime.now(tz=timezone.utc), usegmt=True)


def render_template_with_headers(template_name: str, **context):
    content = render_template(template_name, **context)
    response = make_response(content)
    response.headers['Cache-Control'] = 'public, max-age=3600'
    response.headers['Last-Modified'] = get_template_last_modified(template_name)
    # يؤكد لمحركات البحث أنه يمكن فهرسة هذه الصفحة
    response.headers['X-Robots-Tag'] = 'index, follow'
    return response
port = int(os.environ.get("PORT", 10000))

ARTICLE_CATEGORIES = {
    "noon-rules": [
        "izhar",
        "idgham",
        "iqlab",
        "ikhfa",
        "idgham-with-ghunnah",
        "idgham-without-ghunnah",
        "huruf-izhar",
        "huruf-idgham",
        "huruf-ikhfa",
    ],
    "meem-rules": [
        "izhar-shafawi",
        "idgham-shafawi",
        "ikhfa-shafawi",
        "huruf-meem-rules",
        "meem-sakinah-overview",
    ],
    "raa-rules": ["tafkheem", "tarqeeq", "raa-openings", "raa-waqf"],
    "makharej": ["halq", "lisan", "jawf", "khayshoom", "shafatan"],
    "sifat": ["hams-jahr", "shidda-rikhwa", "qalqala", "istila", "istifal"],
}


@app.route('/')
def index():
    return render_template_with_headers('index.html')


@app.route('/articles')
def articles_index():
    return render_template_with_headers('articles/index.html')


@app.route('/articles/<category>')
def articles_category(category):
    if category not in ARTICLE_CATEGORIES:
        abort(404)

    template_name = f'articles/{category}.html'
    template_path = os.path.join(app.jinja_loader.searchpath[0], template_name)
    if not os.path.isfile(template_path):
        abort(404)

    return render_template_with_headers(template_name)


@app.route('/articles/<category>/<article>')
def article_page(category, article):
    if category not in ARTICLE_CATEGORIES:
        abort(404)
    if article not in ARTICLE_CATEGORIES[category]:
        abort(404)

    template_name = f'articles/{category}/{article}.html'
    template_path = os.path.join(app.jinja_loader.searchpath[0], template_name)
    if not os.path.isfile(template_path):
        abort(404)

    # build list of other articles in the same category for internal linking
    related = []
    for a in ARTICLE_CATEGORIES.get(category, []):
        if a == article:
            continue
        related.append({
            "slug": a,
            "url": url_for("article_page", category=category, article=a),
        })

    return render_template_with_headers(template_name, related_articles=related)


@app.route('/<page>')
def render_page(page):
    templates_dir = app.jinja_loader.searchpath[0]
    page_path = os.path.join(templates_dir, f"{page}.html")

    if not os.path.isfile(page_path):
        abort(404)

    return render_template_with_headers(f"{page}.html")


@app.route('/sitemap.xml')
def sitemap():
    today = date.today().isoformat()

    def template_lastmod(template_name: str) -> str:
        template_path = os.path.join(app.jinja_loader.searchpath[0], template_name)
        if os.path.isfile(template_path):
            return date.fromtimestamp(os.path.getmtime(template_path)).isoformat()
        return today

    urls = []

    # Core pages
    urls.append({
        "loc": url_for("index", _external=True),
        "lastmod": template_lastmod("index.html"),
        "changefreq": "weekly",
        "priority": "1.0",
    })
    urls.append({
        "loc": url_for("articles_index", _external=True),
        "lastmod": template_lastmod("articles/index.html"),
        "changefreq": "weekly",
        "priority": "0.9",
    })

    # Category and article pages derived from ARTICLE_CATEGORIES
    for category, articles in ARTICLE_CATEGORIES.items():
        urls.append({
            "loc": url_for("articles_category", category=category, _external=True),
            "lastmod": template_lastmod(f"articles/{category}.html"),
            "changefreq": "monthly",
            "priority": "0.8",
        })

        for article in articles:
            urls.append({
                "loc": url_for("article_page", category=category, article=article, _external=True),
                "lastmod": template_lastmod(f"articles/{category}/{article}.html"),
                "changefreq": "monthly",
                "priority": "0.7",
            })

    # include any other top-level template pages automatically (e.g. contact, community, etc.)
    templates_dir = app.jinja_loader.searchpath[0]
    for dirpath, dirnames, filenames in os.walk(templates_dir):
        for filename in filenames:
            if not filename.endswith(".html"):
                continue
            rel_path = os.path.relpath(os.path.join(dirpath, filename), templates_dir)
            # skip files we've already added or that are part of articles
            if rel_path == "index.html" or rel_path.startswith("articles"):
                continue
            # compute URL. If file is at top level (e.g. "contact.html"), use render_page route
            parts = rel_path.replace("\\", "/").split("/")
            if len(parts) == 1:
                page = parts[0].rsplit(".", 1)[0]
                urls.append({
                    "loc": url_for("render_page", page=page, _external=True),
                    "lastmod": template_lastmod(rel_path),
                    "changefreq": "monthly",
                    "priority": "0.6",
                })
            else:
                # deeper path not handled by existing routes; skip
                pass

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for item in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{escape(item['loc'])}</loc>")
        xml_lines.append(f"    <lastmod>{item['lastmod']}</lastmod>")
        xml_lines.append(f"    <changefreq>{item['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{item['priority']}</priority>")
        xml_lines.append("  </url>")

    xml_lines.append("</urlset>")
    xml_content = "\n".join(xml_lines)
    return Response(xml_content, mimetype="application/xml")


@app.route('/robots.txt')
def robots_txt():
    sitemap_url = url_for("sitemap", _external=True)
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {sitemap_url}",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
