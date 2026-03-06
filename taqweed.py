import os
from datetime import date
from xml.sax.saxutils import escape
from flask import Flask, abort, render_template, request, Response, url_for

app = Flask(__name__, static_folder='static', template_folder='templates')
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
    return render_template('index.html')


@app.route('/articles')
def articles_index():
    return render_template('articles/index.html')


@app.route('/articles/<category>')
def articles_category(category):
    if category not in ARTICLE_CATEGORIES:
        abort(404)

    template_name = f'articles/{category}.html'
    template_path = os.path.join(app.jinja_loader.searchpath[0], template_name)
    if not os.path.isfile(template_path):
        abort(404)

    return render_template(template_name)


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

    return render_template(template_name)


@app.route('/<page>')
def render_page(page):
    templates_dir = app.jinja_loader.searchpath[0]
    page_path = os.path.join(templates_dir, f"{page}.html")

    if not os.path.isfile(page_path):
        abort(404)

    return render_template(f"{page}.html")


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
