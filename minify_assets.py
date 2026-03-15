import os

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')


def minify_css(content: str) -> str:
    lines = content.splitlines()
    out = []
    for line in lines:
        s = line.strip()
        if not s or s.startswith('/*') and s.endswith('*/'):
            continue
        out.append(s)
    result = ' '.join(out)
    result = result.replace('; }', '}')
    return result


def minify_js(content: str) -> str:
    lines = content.splitlines()
    out = []
    skip = False
    for line in lines:
        s = line.strip()
        if s.startswith('//'):
            continue
        if '/*' in s and '*/' in s:
            s = s[:s.index('/*')] + s[s.index('*/') + 2:]
            s = s.strip()
            if not s:
                continue
        if '/*' in s:
            skip = True
            s = s[: s.index('/*')].strip()
            if not s:
                continue
        if '*/' in s:
            skip = False
            s = s[s.index('*/') + 2 :].strip()
            if not s:
                continue
        if skip:
            continue
        if not s:
            continue
        out.append(s)
    return ' '.join(out)


def minify_file(src_name: str, dst_name: str, minify_fn):
    src_path = os.path.join(STATIC_DIR, src_name)
    dst_path = os.path.join(STATIC_DIR, dst_name)
    if not os.path.exists(src_path):
        print(f'Source file not found: {src_path}')
        return
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    minified = minify_fn(content)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(minified)
    print(f'Wrote {dst_path} ({len(minified)} bytes)')


def main():
    minify_file('style.css', 'style.min.css', minify_css)
    minify_file('java.js', 'java.min.js', minify_js)


if __name__ == '__main__':
    main()
