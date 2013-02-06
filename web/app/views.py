from libs.render import render_to

@render_to('fuck.html')
def fuck(rctx):
    return {}

@render_to('index.html')
def index(rctx):
    return {}
