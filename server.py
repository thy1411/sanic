# SANIC - BASIC TUTORIAL

import asyncio

from sanic import Sanic
from sanic import text, html, json, raw, redirect, empty


# 1. SANIC APPLICATION
app = Sanic("MyHelloWorldApp")

# Application context
app.ctx.message = "Shared application context"

@app.get("/app-context")
async def app_context(request):
    return text(request.app.ctx.message)

# 2. HANDLERS
@app.get("/")
async def hello_world(request):
    return text("Hello, world.")

@app.get("/foo")
async def foo_handler(request):
    return text("I said foo!")

# Handler có thể sử dụng def hoặc async def
@app.get("/sync")
def sync_handler(request):
    return text("Synchronous handler")

@app.get("/async")
async def async_handler(request):
    return text("Asynchronous handler")

# Handler có type annotation
@app.get("/typed")
async def typed_handler(request):
    return text("Done.")

# 3. REQUEST
# Request JSON
@app.post("/request/json")
async def request_json(request):
    return json({
        "received": request.json
    })

# Request body dạng bytes
@app.post("/request/body")
async def request_body(request):
    return text(str(request.body))

# Request form
@app.post("/request/form")
async def request_form(request):
    return json({
        "foo": request.form.get("foo")
    })

# Query parameters
@app.get("/search")
async def search(request):
    query = request.args.get("q")

    if not query:
        return text("No query string provided")

    return text(f"Searching for: {query}")

# Path parameters
@app.get("/tag/<tag>")
async def tag_handler(request, tag):
    return text("Tag - {}".format(tag))

# Request context
@app.on_request
async def run_before_handler(request):
    request.ctx.message = "Request context example"

@app.get("/request-context")
async def request_context(request):
    return text(request.ctx.message)

# 4. RESPONSE
# Text response
@app.get("/response/text")
async def response_text(request):
    return text("Hi!")

# HTML response
@app.get("/response/html")
async def response_html(request):
    return html(
        '<!DOCTYPE html>'
        '<html lang="en">'
        '<meta charset="UTF-8">'
        '<div>Hi!</div>'
        '</html>'
    )

# JSON response
@app.get("/response/json")
async def response_json(request):
    return json({
        "foo": "bar"
    })

# Raw response
@app.get("/response/raw")
async def response_raw(request):
    return raw(b"raw bytes")

# Redirect response
@app.get("/response/redirect")
async def response_redirect(request):
    return redirect("/")

# Empty response
@app.get("/response/empty")
async def response_empty(request):
    return empty()

# Response với HTTP status code
@app.post("/response/status")
async def response_status(request):
    return json(
        {
            "created": True,
            "id": 1
        },
        status=201
    )

# 5. ROUTING
# Đăng ký route bằng add_route
async def route_handler(request):
    return text("OK")

app.add_route(route_handler, "/add-route")

# GET
@app.get("/test")
async def get_handler(request):
    return text("GET request")

# POST
@app.post("/test")
async def post_handler(request):
    return text("POST request")

# PUT
@app.put("/test")
async def put_handler(request):
    return text("PUT request")

# PATCH
@app.patch("/test")
async def patch_handler(request):
    return text("PATCH request")

# DELETE
@app.delete("/test")
async def delete_handler(request):
    return text("DELETE request")

# HEAD
@app.head("/test")
async def head_handler(request):
    return empty()

# OPTIONS
@app.options("/test")
async def options_handler(request):
    return empty()

# Path parameter có kiểu dữ liệu
@app.get("/foo/<foo_id:int>")
async def int_handler(request, foo_id: int):
    return text("ID - {}".format(foo_id))

# 6. LISTENERS
@app.before_server_start
async def before_start(app):
    print("Before server start")

@app.after_server_start
async def after_start(app):
    print("After server start")

@app.before_server_stop
async def before_stop(app):
    print("Before server stop")

@app.after_server_stop
async def after_stop(app):
    print("After server stop")

# 7. MIDDLEWARE
@app.on_request
async def add_key(request):
    request.ctx.foo = "bar"

@app.on_response
async def custom_banner(request, response):
    response.headers["X-Fake-Server"] = "Sanic"

@app.on_response
async def prevent_xss(request, response):
    response.headers["x-xss-protection"] = "1; mode=block"

@app.get("/middleware")
async def middleware_handler(request):
    return text(request.ctx.foo)

# 8. HEADERS
# Request headers
@app.get("/headers")
async def headers_handler(request):
    return json({
        "user_agent": request.headers.get("user-agent"),
        "accept": request.headers.get("accept")
    })

# Authorization token
@app.get("/token")
async def token_handler(request):
    return text(request.token or "No token")

# Request ID
@app.get("/request-id")
async def request_id_handler(request):
    return text(request.id)


# Response headers
@app.get("/response-headers")
async def response_headers(request):
    return text(
        "Done.",
        headers={
            "content-language": "en-US"
        }
    )

# Thêm Request ID vào response
@app.on_response
async def add_request_id_header(request, response):
    response.headers["X-Request-ID"] = request.id

# 9. COOKIES
# Đọc cookie
@app.get("/cookie")
async def read_cookie(request):
    test_cookie = request.cookies.get("test")

    return text(f"Test cookie: {test_cookie}")

# Tạo cookie
@app.get("/cookie/set")
async def write_cookie(request):
    response = text("There's a cookie up in this response")

    response.add_cookie(
        "test",
        "It worked!",
        domain=".yummy-yummy-cookie.com",
        httponly=True
    )

    return response

# Xóa cookie
@app.get("/cookie/delete")
async def delete_cookie(request):
    response = text("Time to eat some cookies")

    response.delete_cookie("eat_me")

    response.add_cookie(
        "fast_bake",
        "Be quick!",
        max_age=5
    )

    return response

# 10. BACKGROUND TASKS
async def notify_server_started_after_five_seconds():
    await asyncio.sleep(5)

    print("Server successfully started!")


# Sanic tự động truyền app vào task

async def auto_inject(app):
    await asyncio.sleep(5)

    print(app.name)

async def explicit_inject(app):
    await asyncio.sleep(5)

    print(app.name)

@app.after_server_start
async def start_background_tasks(app):
    app.add_task(
        notify_server_started_after_five_seconds()
    )

    app.add_task(auto_inject)

    app.add_task(explicit_inject(app))
