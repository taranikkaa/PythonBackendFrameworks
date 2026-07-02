from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Step 102: Dynamically proxy and route client patterns to distinct microservice target hosts
COURSE_SERVICE_URL = "http://localhost:5001"
STUDENT_SERVICE_URL = "http://localhost:5002"

@app.route('/api/courses', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/api/courses/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_course_service(path):
    target_url = f"{COURSE_SERVICE_URL}{request.full_path}"
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    return Response(resp.content, resp.status_code, resp.headers.items())

@app.route('/api/students', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/api/students/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_student_service(path):
    target_url = f"{STUDENT_SERVICE_URL}{request.full_path}"
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    return Response(resp.content, resp.status_code, resp.headers.items())

if __name__ == '__main__':
    # Step 102: Gateway runs on base entry port 5000
    app.run(port=5000, debug=True)