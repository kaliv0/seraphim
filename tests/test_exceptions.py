def test_custom_exception_handler(api, client):
    def on_exception(req, resp, exc):
        resp.text = "AttributeErrorHappened"

    api.add_exception_handler(on_exception)

    @api.route("/")
    def index(req, resp):
        raise AttributeError()

    response = client.get("http://testserver/")

    assert response.text == "AttributeErrorHappened"


# TODO: move test
def test_404_is_returned_for_nonexistent_static_file(client):
    assert client.get(f"http://testserver/main.css)").status_code == 404
