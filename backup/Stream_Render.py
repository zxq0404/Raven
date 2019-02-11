
app = Flask(__name__)

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.disable_buffering()
    return rv

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
def generate():
    for item in data:
        yield str(item)
        time.sleep(.1)

@app.route('/stream')
def stream_view():
    rows = generate()
    return Response(stream_template('template.html', rows=rows))

app.run()
