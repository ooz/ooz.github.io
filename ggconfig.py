#!/usr/bin/env python
# -*- coding: utf-8 -*-

config = {
    'site': {
        'base_url': 'https://oliz.io',
        'generate_sitemap': True,
        'additional_sitemap_entries': [
            'https://oliz.io/blog/',
            'https://oliz.io/mocs/'
        ],
        'title': 'Oliver Z.',
        'logo': 'static/owl.png',
        'head': [
            '''<meta http-equiv="Content-Security-Policy" content="script-src 'unsafe-inline'">''',
            '''<meta name="referrer" content="no-referrer">'''
        ]
    },
    'author': {
        'name': 'oz',
        'url': 'https://oliz.io'
    },
    'social': {
        'about': 'https://oliz.io/about.html',
        'blog': 'https://oliz.io/blog/',
        'github': 'https://github.com/ooz',
        'twitter': 'https://twitter.com/oozgo'
    }
}
