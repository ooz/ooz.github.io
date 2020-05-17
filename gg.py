#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
from html import escape
import os
import sys
import time
import markdown

import ggconfig as gg

MD = markdown.Markdown(
        extensions = [
            'extra',
            'meta',
            'sane_lists',
            'toc',
            'pymdownx.magiclink',
            'pymdownx.betterem',
            'pymdownx.tilde',
            'pymdownx.emoji',
            'pymdownx.tasklist',
            'pymdownx.superfences'
        ]
    )

def render_template(canonical_url, body, MD, root):
    title = convert_meta(MD, 'title')
    date = convert_meta(MD, 'date')
    tags = convert_meta(MD, 'tags')
    description = convert_meta(MD, 'description', default=title)
    raw_title = ''.join(MD.Meta.get('title', ''))
    raw_description = ''.join(MD.Meta.get('description', raw_title))
    base_url = gg.config.get('site', {}).get('base_url', '')
    logo_url = base_url + '/' + gg.config.get('site', {}).get('logo', '')
    author_name = gg.config.get('author', {}).get('name', '')
    author_url = gg.config.get('author', {}).get('url', '')
    return \
f'''<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>{convert_title2pagetitle(title)}</title>
<link rel="canonical" href="{canonical_url}">
<link rel="shortcut icon" href="{logo_url}">

{style()}
{meta(author_name, description, tags)}
{twitter(gg.config.get('social', {}).get('twitter_username', ''))}
{opengraph(title, canonical_url, description, date)}
{json_ld(raw_title, canonical_url, raw_description)}
</head>

<body onload="initTheme()">
<header>
<a href="{author_url}"><img src="{logo_url}" class="avatar" /></a>
{post_header(title, date)}
</header>
<section>
{body}
</section>
<footer>
{render_footer_navigation(base_url, root)}
{render_about_and_social_icons()}
</footer>
</body>
</html>
'''

def style():
    return \
f'''<style>
body {{
    font-size: 18px;
    font-family: sans-serif;
    line-height: 1.6;
    color: #363636;
    background: #FFF;
    margin: 1rem auto;
    padding: 0 10px;
    max-width: 700px;
    scroll-behavior: smooth;
}}
a {{ color: #07A; text-decoration: none; }}
blockquote {{
    background: #EAEAEA;
    border-left: .3rem solid #07A;
    border-radius: .3rem;
    margin: 0 .2rem;
    padding: 0 .5rem;
}}
code {{
    font-size: 80%;
    background: #EAEAEA;
    padding: .2rem .5rem;
    white-space: nowrap;
}}
h1 {{ text-align: center; margin: 0 auto; }}
h1, h2, h3, h4, h5, h6 {{ font-family: serif; font-weight: bold; }}
header {{ text-align:center; }}
img {{ max-width: 100%; }}
ul.task-list, ul.task-list li.task-list-item {{
    list-style-type: none;
    list-style-image: none;
}}
pre {{ border-left: 0.3rem solid #07A; }}
pre > code {{
    font-size: 14px;
    background: #EAEAEA;
    box-sizing: inherit;
    display: block;
    overflow-x: auto;
    margin: 0 .2rem;
    white-space: pre;
}}
table {{
    border-spacing: 0;
    width: 100%;
}}
td, th {{
    border-bottom: .1rem solid;
    padding: .8rem 1rem;
    text-align: left;
}}
.avatar {{ border-radius: 50%; box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.2); max-width: 3rem; }}
.nav {{ float: left; margin-right: 1rem; }}
.social {{ float: right; margin-left: 1rem; }}

.dark-mode {{ color: #FFF; background: #363636; }}
.dark-mode a {{ color: #0A7; }}
.dark-mode blockquote {{ background: #222; border-left: 0.3rem solid #0A7; }}
.dark-mode code {{ background: #222; }}
.dark-mode pre {{ border-left: 0.3rem solid #0A7; }}
</style>
<script>
function toggleTheme() {{ document.body.classList.toggle("dark-mode") }}
function initTheme() {{ let h=new Date().getHours(); if (h <= 8 || h >= 20) {{ toggleTheme() }} }}
</script>
'''

def render_about_and_social_icons():
    github = gg.config.get('social', {}).get('github_url', '')
    twitter = gg.config.get('social', {}).get('twitter_url', '')
    email = gg.config.get('author', {}).get('email', '')
    about = gg.config.get('site', {}).get('about_url', '')
    icons = []

    if len(email):
        icons.append('<a href="mailto:%s" class="social">email</a>' % email)
    if len(twitter):
        icons.append('<a href="%s" class="social">twitter</a>' % twitter)
    if len(github):
        icons.append('<a href="%s" class="social">github</a>' % github)
    if len(about):
        icons.append('<a href="%s" class="social">about</a>' % about)
    return '\n'.join(icons)

def render_footer_navigation(root_url, is_root):
    nav = []
    if not is_root:
        nav.append(f'''<a href="{root_url}" class="nav">back</a>''')
    nav.append('''<a href="#" class="nav">top</a>''')
    nav.append('''<a href="javascript:toggleTheme()" class="nav">🌚🌞</a>''')
    return '\n'.join(nav)


def meta(author, description, tags):
    return \
f'''<meta name="author" content="{author}" />
<meta name="description" content="{description}" />
<meta name="keywords" content="{tags}" />'''

def twitter(twitter_username):
    return \
f'''<meta name="twitter:author" content="{twitter_username}" />
<meta name="twitter:card" content="summary" />
<meta name="twitter:creator" content="{twitter_username}" />'''

# URL should end with "/" for a directory!
def opengraph(title, url, description, date,
              image=gg.config.get('site', {}).get('base_url', '') + '/' + gg.config.get('site', {}).get('logo', '')):
    return \
f'''<meta property="og:title" content="{title}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<meta property="og:description" content="{description}" />
<meta property="og:image" content="{image}" />
<meta property="og:locale" content="en-US" />
<meta property="article:published_time" content="{date}" />'''

def json_ld(title, url, description):
    root_title = gg.config.get('site', {}).get('title', '')
    json_escaped_root_title = root_title.replace('"', '\\"')
    json_escaped_title = title.replace('"', '\\"')
    json_escaped_description = description.replace('"', '\\"')
    name_block = f',"name":"{json_escaped_root_title}"' if len(root_title) else ''
    return \
f'''<script type="application/ld+json">
{{"@context":"http://schema.org","@type":"WebSite","headline":"{json_escaped_title}","url":"{url}"{name_block},"description":"{json_escaped_description}"}}</script>'''

def post_header(title, date):
    name = gg.config.get('author', {}).get('name', '')
    author_url = gg.config.get('author', {}).get('url', '')
    name_and_date = date[:10]
    if len(name) and len(name_and_date):
        maybe_linked_author = name
        if len(author_url):
            maybe_linked_author = f'<a href="{author_url}">{name}</a>'
        name_and_date = f'{maybe_linked_author}, {name_and_date}'
    if len(name_and_date):
        name_and_date = f'''<small>{name_and_date}</small>'''
    title_html = ''
    if len(title):
        title_html = MD.reset().convert('# ' + title)
    header = ''
    if len(title_html) or len(name_and_date):
        header = f'''<div style="text-align:right;">
{title_html}
{name_and_date}
</div>'''
    return header


def convert(directory, filepath, root=False):
    with open(filepath, 'r') as infile:
        markdown_post = infile.read()
        html_post = MD.reset().convert(markdown_post)
        targetpath = convert_path(filepath)
        with open(targetpath, 'w') as outfile:
            canonical_url = convert_canonical(directory, targetpath)
            date = convert_meta(MD, 'date')
            tags = convert_meta(MD, 'tags')
            title = convert_meta(MD, 'title')
            html = render_template(canonical_url,
                html_post,
                MD,
                root
            )
            outfile.write(html)
            return {
                'date': date,
                'url': canonical_url,
                'title': title,
                'tags': tags,
                'last_modified': last_modified(filepath)
            }

def last_modified(filepath):
    return time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(filepath)))

def convert_meta(md, field, default=''):
    field_value = MD.Meta.get(field, '')
    if len(field_value) > 0:
        return escape(', '.join(field_value)) if field == 'tags' else escape(''.join(field_value))
    return default

def convert_path(filepath):
    targetpath = filepath[:-3]
    if targetpath.endswith('README'):
        targetpath = targetpath[:-6] + 'index'
    targetpath += '.html'
    return targetpath

def convert_canonical(directory, targetpath):
    base_url = gg.config.get('site', {}).get('base_url', '')
    targetpath = os.path.relpath(targetpath, directory)
    if targetpath.endswith('index.html'):
        return f'{base_url}/{targetpath[:-10]}'
    return f'{base_url}/{targetpath}'

def convert_title2pagetitle(title):
    root_title = gg.config.get('site', {}).get('title', '')
    if len(title) and title != root_title:
        return f'{title} | {root_title}'
    return root_title

def make_index(posts):
    base_url = gg.config.get('site', {}).get('base_url', '')
    root_title = gg.config.get('site', {}).get('title', '')
    logo_url = base_url + '/' + gg.config.get('site', {}).get('logo', '')
    author_url = gg.config.get('author', {}).get('url', '')
    posts_html = []
    for post in reversed(sorted(posts, key=lambda post: post['date'])):
        day = post['date'][:10]
        title = post['title']
        url = post['url']
        if (day != '' and title != ''):
            posts_html.append('<tr><td>%s</td><td><a href="%s">%s</a></td></tr>' % (day, url, title))
    posts_html = "\n".join(posts_html)

    index_html = \
f'''<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>Index | {root_title}</title>
<link rel="canonical" href="{base_url}">
<link rel="shortcut icon" href="{logo_url}">

{style()}
</head>

<body onload="initTheme()">
<header>
<a href="{author_url}"><img src="{logo_url}" class="avatar" /></a>
<h1>Index</h1>
</header>
<section>
<table><tbody>
{posts_html}
</tbody></table>
</section>
<footer>
{render_footer_navigation(None, True)}
{render_about_and_social_icons()}
</footer>
</body>
</html>
'''
    with open('index.html', 'w') as index_file:
        index_file.write(index_html)

def is_root_readme(path):
    return os.path.relpath(path) == 'README.md'

def make_sitemap(posts):
    sitemap_xml = []
    sitemap_xml.append('<?xml version="1.0" encoding="utf-8" standalone="yes" ?>')
    sitemap_xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    additional_entries = gg.config.get('site', {}).get('additional_sitemap_entries', [])
    all_entries = [(post['url'], post['last_modified']) for post in posts]
    all_entries = all_entries + [(entry, '') for entry in additional_entries]
    all_entries = sorted(all_entries, key=lambda entry: entry[0])
    for entry in all_entries:
        sitemap_xml.append('  <url>')
        sitemap_xml.append('    <loc>%s</loc>' % escape(entry[0]))
        if len(entry[1]):
            sitemap_xml.append('    <lastmod>%s</lastmod>' % entry[1])
        sitemap_xml.append('  </url>')
    sitemap_xml.append('</urlset>\n')
    sitemap_xml = '\n'.join(sitemap_xml)
    with open('sitemap.xml', 'w') as sitemap_file:
        sitemap_file.write(sitemap_xml)

def main(directories):
    render_root_readme = gg.config.get('site', {}).get('render_root_readme', True)
    posts = []
    for directory in directories:
        paths = glob.glob(directory + '/**/*.md', recursive=True)
        for path in paths:
            root_readme = is_root_readme(path)
            if not root_readme or render_root_readme:
                posts.append(convert(directory, path, root=root_readme))

    posts = [post for post in posts if 'draft' not in post['tags']]
    if not render_root_readme:
        make_index(posts)

    generate_sitemap = gg.config.get('site', {}).get('generate_sitemap', False)
    if generate_sitemap:
        make_sitemap(posts)

if __name__ == '__main__':
    main(sys.argv[1:])
