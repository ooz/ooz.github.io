#!/usr/bin/env python
# -*- coding: utf-8 -*-

config = {
    'site': {
        'base_url': 'https://oliz.io',
        'render_root_readme': True,
        'generate_sitemap': True,
        'additional_sitemap_entries': ['https://oliz.io/blog/'],
        'title': 'out of zeit',
        'logo': 'static/owl.png',
        'about_url': 'https://oliz.io/about.html',
        'csp': '''<meta http-equiv="Content-Security-Policy" content="script-src 'self'">''',
        'referrer': '''<meta name="referrer" content="no-referrer">'''
    },
    'author': {
        'name': 'oz',
        'url': 'https://oliz.io'
    },
    'social': {
        'github_url': 'https://github.com/ooz',
        'twitter_url': 'https://twitter.com/oozgo',
        'twitter_username': '@oozgo'
    }
}
