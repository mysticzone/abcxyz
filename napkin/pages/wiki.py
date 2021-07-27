#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Napkin wiki.
"""

import datetime

import flask
import json

import markdown

from napkin.pages import utils as index_utils
from napkin.db import api as db_api


URL_PREFIX_WIKI_WEB = '/wiki'


def app_load_web_wiki(app, opts=None):


    def wiki_util_page_check_lock(pg):
        if not pg:
            return False

        if pg.state != 'lock':
            return False

        locked_at = pg.locked_at
        if not locked_at:
            return False

        time_now = datetime.datetime.now()
        tm_delta = time_now - locked_at
        d_sec = tm_delta.total_seconds()
        #if d_sec > 60 * 60:  # 1 hour
        if d_sec > 60 * 10:  # 10 minutes
            return False
        else:
            return True


    # Wiki Help Page
    @app.route(URL_PREFIX_WIKI_WEB + '/help/')
    ##@index_utils.login_required
    def wiki_help():
        txt = index_utils.file_read_local_md('napkin/templates/wiki/example.md')

        txthtml = wk_markdown_to_html(txt)
        #return flask.Response(nodes.to_json(),
        #                      mimetype='application/json')
        return flask.render_template('wiki/help.html', txthtml=txthtml)


    # Wiki Result Page
    @app.route(URL_PREFIX_WIKI_WEB + '/result/', methods=['GET', 'POST'])
    ##@index_utils.login_required
    def wiki_result():
        if flask.request.method == 'GET':
            args = index_utils.flask_req_get_querystr(flask.request)
        else:
            args = index_utils.flask_req_get_post_data(flask.request)

        result_txt = args.get('result', '')

        return flask.render_template('wiki/result.html', result_txt=result_txt)


    # Wiki List Page
    @app.route(URL_PREFIX_WIKI_WEB + '/list/')
    ##@index_utils.login_required
    def wiki_list_all():
        #pgs = db_api.wiki_page_get_all()
        #pgs = db_api.wiki_page_filter(level=1)
        pgs = db_api.wiki_page_filter(level=0).order_by('-created_at')
        return flask.render_template('wiki/list.html', pgs=pgs)

    # Wiki Index Page
    @app.route(URL_PREFIX_WIKI_WEB + '/')
    ##@index_utils.login_required
    def wiki_index():
        #pgs = db_api.wiki_page_get_all()
        pgs = db_api.wiki_page_filter(level=1).order_by('created_at')
        return flask.render_template('wiki/index.html', pgs=pgs)


    # Wiki Single Page
    @app.route(URL_PREFIX_WIKI_WEB + '/page/<pgid>')
    ##@index_utils.login_required
    def wiki_page(pgid=None):
        if not pgid:
            return flask.redirect(flask.url_for('wiki_index'))

        try:
            pg = db_api.wiki_page_get(pgid)
        except:
            return flask.redirect(flask.url_for('wiki_index'))
        content = pg.content  # TODO(likun):
        txthtml = wk_markdown_to_html(content)
        title = pg.title
        updated_at = pg.updated_at
        state = pg.state

        locked = wiki_util_page_check_lock(pg)
        return flask.render_template('wiki/page.html', title=title,
                                     txthtml=txthtml, pgid=pgid,
                                     updated_at=updated_at, state=state,
                                     locked=locked)


    # Wiki Post Page
    @app.route(URL_PREFIX_WIKI_WEB + '/post/')
    ##@index_utils.login_required
    def wiki_post():
        return flask.render_template('wiki/post.html')


    # Wiki Edit Page
    @app.route(URL_PREFIX_WIKI_WEB + '/edit/<pgid>')
    ##@index_utils.login_required
    def wiki_edit(pgid=None):
        if not pgid:
            return flask.redirect(flask.url_for('/'))

        try:
            pg = db_api.wiki_page_get(pgid)
        except:
            return flask.redirect(flask.url_for('wiki_index'))

        pgid = str(pg.id)

        locked = wiki_util_page_check_lock(pg)
        if locked:
            return flask.redirect('/wiki/page/' + pgid)

        content = pg.content  # TODO(likun):
        title = pg.title
        keywords = pg.keywords
        #if keywords:
        #    keywords = ' '.join(keywords)
        #else:
        #    keywords = ''
        if isinstance(keywords, (list, tuple, set)):
            keywords = ' '.join(keywords)
        level = pg.level
        updated_at = pg.updated_at

        # lock the page
        pg.state = 'lock'
        pg.locked_at = datetime.datetime.now()
        pg.save()

        return flask.render_template('wiki/edit.html', pgid=pgid,
                                     content=content, title=title,
                                     keywords=keywords, level=level,
                                     updated_at=updated_at)


    # Wiki Post API
    @app.route(URL_PREFIX_WIKI_WEB + '/api/post', methods=['POST'])
    ##@index_utils.login_required
    def wiki_api_post():
        if flask.request.method == 'GET':
            args = index_utils.flask_req_get_querystr(flask.request)
        else:
            args = index_utils.flask_req_get_post_data(flask.request)

        pgid = args.get('pageid')

        page_title = args.get('page_title', '')
        page_content = args.get('page_content', '')
        page_keywords = args.get('page_keywords', '')  # []
        page_level = args.get('page_level', 0)

        #if isinstance(page_keywords, (str, unicode)):
        #    page_keywords = index_utils.str_to_list_by(page_keywords)

        try:

            if pgid:  # edit
                pg = db_api.wiki_page_get(pgid)

                # TODO(likun):
                #locked = wiki_util_page_check_lock(pg)
                #if locked:
                #    return flask.redirect('/wiki/page/' + pgid)

                #pg.version += 1

                #pg.title = page_title
                #pg.content = page_content
                #pg.keywords = page_keywords

                pg_d = {}
                pg_d['version'] = pg.version + 1
                pg_d['title'] = page_title
                pg_d['content'] = page_content
                pg_d['keywords'] = page_keywords
                pg_d['level'] = page_level
                pg_d['updated_at'] = datetime.datetime.now()
                pg_d['state'] = 'open'
                #pg_d['locked_at'] = datetime.datetime.now()

                db_api.wiki_page_update(pgid, pg_d)
            else:
                pg_d = {}
                pg_d['title'] = page_title
                pg_d['content'] = page_content
                pg_d['keywords'] = page_keywords
                pg_d['level'] = page_level
                pg_d['state'] = 'open'
                #pg_d['locked_at'] = datetime.datetime.now()

                username = flask.session.get('username', 'author_name')
                pg_d['author_name'] = username  # TODO:
            
                pg_o = db_api.wiki_page_create(pg_d)

                pgid = str(pg_o.id)

            #return flask.Response(json.dumps(pg_d),
            #    mimetype='application/json')
            #return flask.Response(pgid)
            return flask.redirect('/wiki/page/' + pgid)
        except Exception as ex:
            flask.abort(400, repr(ex))


    # Wiki Delete Page
    @app.route(URL_PREFIX_WIKI_WEB + '/api/del/<pgid>')
    ##@index_utils.login_required
    def wiki_api_del(pgid=None):
        if not pgid:
            return flask.redirect(flask.url_for('/'))

        try:
            pg = db_api.wiki_page_get(pgid)
            pg.delete()
            return flask.redirect(flask.url_for('wiki_index'))
        except:
            return flask.redirect(flask.url_for('wiki_index'))




    # return the application at the end
    return app


# markdown functions #

# http://pythonhosted.org/Markdown/reference.html

# http://pythonhosted.org/Markdown/extensions/index.html
# Officially Supported Extensions

'''
Extension   Name
Extra   markdown.extensions.extra
    Abbreviations   markdown.extensions.abbr
    Attribute Lists   markdown.extensions.attr_list
    Definition Lists  markdown.extensions.def_list
    Fenced Code Blocks  markdown.extensions.fenced_code
    Footnotes   markdown.extensions.footnotes
    Tables  markdown.extensions.tables
    Smart Strong  markdown.extensions.smart_strong
Admonition  markdown.extensions.admonition
CodeHilite  markdown.extensions.codehilite
HeaderId  markdown.extensions.headerid
Meta-Data   markdown.extensions.meta
New Line to Break   markdown.extensions.nl2br
Sane Lists  markdown.extensions.sane_lists
SmartyPants   markdown.extensions.smarty
Table of Contents   markdown.extensions.toc
WikiLinks   markdown.extensions.wikilinks
'''

WK_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.abbr',
    'markdown.extensions.attr_list',
    'markdown.extensions.def_list',
    'markdown.extensions.fenced_code',
    'markdown.extensions.footnotes',
    'markdown.extensions.tables',
    'markdown.extensions.smart_strong',
    'markdown.extensions.admonition',
    'markdown.extensions.codehilite',
    'markdown.extensions.headerid',
    'markdown.extensions.meta',
    'markdown.extensions.nl2br',
    'markdown.extensions.sane_lists',
    'markdown.extensions.smarty',
    'markdown.extensions.toc',
    'markdown.extensions.wikilinks',
]


def wk_markdown_to_html(txt, *args, **kwargs):
    html = markdown.markdown(txt, extensions=WK_MARKDOWN_EXTENSIONS)
    html = wk_markdown_security_check(html)
    return html


WK_MARKDOWN_SEC_CHECKS = {
    '<script': '&lt;script',
    '</script':'&lt;/script',
}


def wk_markdown_security_check(html, *args, **kwargs):
    if not html:
        return html

    for k, v in WK_MARKDOWN_SEC_CHECKS.items():
        html = html.replace(k, v)

    return html
