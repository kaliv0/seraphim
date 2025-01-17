from seraphim import API
from seraphim import Middleware

# TODO: technically this module is not part of the framework -> it's just an example
app = API(templates_dir="example/templates", static_dir="example/static")


# TODO: move to routers module?
@app.route("/")
@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


# @app.route("/hello/{name}")
# def greeting(request, response, name):
#     response.text = f"Ciao, {name}"


@app.route("/pow/{num_1:d}")
def pow_num(request, response, num_1):
    result = int(num_1) ** 2
    response.text = f"{num_1} ** 2 = {result}"


##############################################
# class based handlers -> Django style
# TODO: should methods be static?
@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"


#############################
def handler(req, resp):
    resp.text = "sample"


app.add_route("/sample", handler)


###################################
# @app.route("/template")
# def template_handler(req, resp):
#     resp.body = app.template(
#         "index.html",
#         context={"title": "Hello world", "name": "Blue Baloo", "foo": "Foo", "bar": "Bar!!!"},
#     ).encode()


@app.route("/template")
def template_handler(req, resp):
    resp.html = app.template(
        "index.html",
        context={"title": "Hello world", "name": "Blue Baloo", "foo": "Foo", "bar": "Bar!!!"},
    )


@app.route("/json")
def json_handler(req, resp):
    resp.json = {"name": "data", "type": "JSON"}


@app.route("/text")
def text_handler(req, resp):
    resp.text = "This is a simple text"


##################################
def custom_exception_handler(request, response, exception_cls):
    response.text = str(exception_cls)


app.add_exception_handler(custom_exception_handler)


@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be used.")


###################################
class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, res):
        print("Processing response", req.url)


app.add_middleware(SimpleCustomMiddleware)
