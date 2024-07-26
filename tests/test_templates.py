def test_template(api, client):
    @api.route("/html")
    def html_handler(req, resp):
        resp.body = api.template(
            "index.html", context={"title": "Some Title", "name": "Some Name"}
        ).encode()

    response = client.get("http://testserver/html")

    assert "text/html" in response.headers["Content-Type"]
    assert "Some Title" in response.text
    assert "Some Name" in response.text
