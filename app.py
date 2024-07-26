from api import API

# TODO: technically this module is not part of the framework -> it's just an example
app = API()


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
