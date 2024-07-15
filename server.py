from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus, urlparse, parse_qs
import os
import time
import glob
import stat

def get_body_params(body):
    if not body:
        return {}
    parameters = body.split("&")

    # split each parameter into a (key, value) pair, and escape both
    def split_parameter(parameter):
        k, v = parameter.split("=", 1)
        k_escaped = unquote_plus(k)
        v_escaped = unquote_plus(v)
        return k_escaped, v_escaped

    body_dict = dict(map(split_parameter, parameters))
    print(f"Parsed parameters as: {body_dict}")
    # return a dictionary of the parameters
    return body_dict


def submission_to_table(item):
    
    """TODO: Takes a dictionary of form parameters and returns an HTML table row

    An example input dictionary might look like: 
    {
     'event': 'Sleep',
     'day': 'Sun',
     'start': '01:00',
     'end': '11:00', 
     'phone': '1234567890', 
     'location': 'Home',
     'extra': 'Have a nice dream', 
     'url': 'https://example.com'
    }
    """
    # pass
    tablerow =  '''
        <tr>
            <td>'''+item['event']+'''</td>
            <td>'''+item['day']+'''</td>
            <td>'''+item['start']+'''</td>
            <td>'''+item['end']+'''</td>
            <td>'''+item['phone']+'''</td>
            <td>'''+item['location']+'''</td>
            <td>'''+item['extra']+'''</td>
            <td>'''+item['url']+'''</td>
        </tr>
    '''

    return tablerow
    
def check_perms(resource):
    stmode = os.stat(resource).st_mode
    return (getattr(stat, 'S_IROTH') & stmode) > 0

def checkIfExist(file_path, MIME_type):
    # Check if the file exists
    if os.path.exists(file_path):
        # Check if the file is accessible
        #if not os.access(file_path, os.R_OK):
        if not check_perms(file_path):
            # If file is not accessible, return a 403 Forbidden response
            return open("static/html/403.html").read(), "text/html; charset=utf-8", 403
        else:
            if MIME_type == "text/html" or MIME_type == "text/css" or MIME_type == "text/javascript" or MIME_type == "text/plain":
                return open(file_path, encoding='utf-8').read(), MIME_type, 200
            else:
                return open(file_path, "br").read(), MIME_type, 200
    else:
        return open("static/html/404.html").read(), "text/html; charset=utf-8", 404

# NOTE: Please read the updated function carefully, as it has changed from the
# version in the previous homework. It has important information in comments
# which will help you complete this assignment.
table = ''
def handle_req(url, body=None):
    """
    The url parameter is a *PARTIAL* URL of type string that contains the path
    name and query string.

    If you enter the following URL in your browser's address bar:
    `http://localhost:4131/MyForm.html?name=joe` then the `url` parameter will have
    the value "/MyForm.html?name=joe"

    This function should return two strings in a list or tuple. The first is the
    content to return, and the second is the content-type.
    """
    # global table

    # Get rid of any query string parameters
    url, *_ = url.split("?", 1)
    # Parse any form parameters submitted via POST
    parameters = get_body_params(body)
    
    if url.endswith("html"):
        index = url.rfind("/")
        file_path = "static/html" + url[index:]
        return checkIfExist(file_path, "text/html")
    elif url.endswith("css"):
        index = url.rfind("/")
        file_path = "static/css" + url[index:]
        return checkIfExist(file_path, "text/css")
    elif url.endswith("js"):
        index = url.rfind("/")
        file_path = "static/js" + url[index:]
        return checkIfExist(file_path, "text/javascript")
    elif url.endswith("png"):
        index = url.rfind("/")
        file_path = "static/img" + url[index:]
        return checkIfExist(file_path, "image/png")
    elif url.endswith("jpg") or url.endswith("jpeg"):
        index = url.rfind("/")
        file_path = "static/img" + url[index:]
        return checkIfExist(file_path, "image/jpeg")
    elif url.endswith("mp3"):
        index = url.rfind("/")
        file_path = "static/audio" + url[index:]
        return checkIfExist(file_path, "audio/mpeg")
    elif url.endswith("txt"):
        index = url.rfind("/")
        file_path = "static/txt" + url[index:]
        return checkIfExist(file_path, "text/plain")
    else:
        return open("static/html/404.html").read(), "text/html; charset=utf-8", 404
    '''
    if url.endswith("MySchedule.html"):
        return open("static/html/MySchedule.html").read(), "text/html"
    elif url == "/MyForm.html":
        return open("static/html/MyForm.html").read(), "text/html"
    elif url == "/AboutMe.html":
        return open("static/html/AboutMe.html", encoding='utf-8').read(), "text/html"
    elif url == "/stockQuotes.html":
        return open("static/html/stockQuotes.html").read(), "text/html"
    # NOTE: These files may be different for your server, but we include them to
    # show you examples of how yours may look. You may need to change the paths
    # to match the files you want to serve. Before you do that, make sure you
    # understand what the code is doing, specifically with the MIME types and
    # opening some files in binary mode, i.e. `open(..., "br")`.
    elif url == "/js/map.js":
        return open("static/js/map.js").read(), "text/javascript"
    elif url == "/js/formPOI.js":
        return open("static/js/formPOI.js").read(), "text/javascript"
    elif url == "/js/stock.js":
        return open("static/js/stockQuotes.js").read(), "text/javascript"
    elif url == "/js/formPOI.js":
        return open("static/js/formPOI.js").read(), "text/javascript"
    elif url == "/css/style.css":
        return open("static/css/style.css").read(), "text/css"
    elif url == "/css/form.css":
        return open("static/css/form.css").read(), "text/css"
    elif url == "/css/schedule.css":
        return open("static/css/schedule.css").read(), "text/css"
    elif url == "/css/stockQuotes.css":
        return open("static/css/stockQuotes.css").read(), "text/css"
    elif url == "/img/gophers-mascot.png":
        return open("static/img/gophers-mascot.png", "br").read(), "image/png"
    elif url == "/img/golden-gopher.png":
        return open("static/img/golden-gopher.png", "br").read(), "image/png"
    elif url == "/img/anderson.jpg":
        return open("static/img/anderson.jpg", "br").read(), "image/jpeg"
    elif url == "/img/healthscienceseducationcenter.jpg":
        return open("static/img/healthscienceseducationcenter.jpg", "br").read(), "image/jpeg"
    elif url == "/img/McNeal.jpg":
        return open("static/img/McNeal.jpg", "br").read(), "image/jpeg"
    elif url == "/img/FoodScience.jpg":
        return open("static/img/FoodScience.jpg", "br").read(), "image/jpeg"
    elif url == "/img/Ruttan.jpg":
        return open("static/img/Ruttan.jpg", "br").read(), "image/jpeg"
    elif url == "/img/Hyland.jpg":
        return open("static/img/Hyland.jpg", "br").read(), "image/jpeg"
    elif url == "/img/TraderJoe.jpg":
        return open("static/img/TraderJoe.jpg", "br").read(), "image/jpeg"
    elif url == "/img/radius.jpg":
        return open("static/img/radius.jpg", "br").read(), "image/jpeg"
    elif url == "/img/landmark.png":
        return open("static/img/landmark.png", "br").read(), "image/png"
    elif url == "/img/route.jpg":
        return open("static/img/route.jpg", "br").read(), "image/jpeg"
    # TODO: Add update the HTML below to match your other pages and
    # implement the `submission_to_table`.
    elif url == "/EventLog.html":
        print(parameters)
        if(parameters != {}):  
            table = table+submission_to_table(parameters)
        return (
            """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <title> Event Submission </title>
                <link rel="stylesheet" href="../css/style.css">
            </head>
            <body>
                <header>
                  <div id="bar">
                    <!-- TODO: Update to appear like the navigation in your other
                    pages if needed -->
                      <a href="/MySchedule.html">My Schedule</a>
                      <a href="/MyForm.html">Form Input</a>
                      <a href="/AboutMe.html">About Me</a>
                      <a href="/EventLog.html">Form Submissions</a>
                  </div>
                </header>
                <h1> My New Events </h1>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>Event</th>
                                <th>Day</th>
                                <th>Start</th>
                                <th>End</th>
                                <th>Phone</th>
                                <th>Location</th>
                                <th>Extra Info</th>
                                <th>URL</th>
                            </tr>
                        </thead>
                        <tbody>
                        """
            + table
            + """
                        </tbody>
                    </table>
                </div>
            </body>
            </html>""",
            "text/html; charset=utf-8",
        )
    else:
        return open("static/html/404.html").read(), "text/html; charset=utf-8"
    '''  

# You shouldn't change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    FILES_DIR = "files"
    # global table

    def list_supported_files(self):
        supported_files = []
        for ext in ["html", "css", "js", "png", "jpg", "jpeg", "mp3", "txt"]:
            supported_files.extend(glob.glob(os.path.join(self.FILES_DIR, f"*.{ext}")))
        return supported_files

    def list_files_html(self):
        files_list = self.list_supported_files()
        files_html = "<ul>"
        for file_path in files_list:
            file_name = os.path.basename(file_path)
            files_html += f'<li><a href="/files/{file_name}">{file_name}</a></li>'
        files_html += "</ul>"
        return files_html

    def get_content_type(self, file_name):
        _, file_extension = os.path.splitext(file_name)
        if file_extension.startswith(".html"):
            return "text/html"
        elif file_extension.startswith(".css"):
            return "text/css"
        elif file_extension.startswith(".js"):
            return "text/javascript"
        elif file_extension.startswith(".png"):
            return "image/png"
        elif file_extension.startswith(".jpg") or file_extension.startswith(".jpeg"):
            return "image/jpeg"
        elif file_extension.startswith(".mp3"):
            return "audio/mpeg"
        elif file_extension.startswith(".txt"):
            return "text/plain"
        else:
            return "application/octet-stream"
        
    def __c_read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        body = str(body, encoding="utf-8")
        return body

    def __c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)

        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Log the response information
        self.log_response(response_code, headers)

        # Send the file.
        self.wfile.write(message)

    def do_GET(self):
        parsed_path = urlparse(self.path)

        if self.path.startswith("/calculator"):
            query_components = parse_qs(urlparse(self.path).query)
            num1 = float(query_components.get('num1', [''])[0])
            num2 = float(query_components.get('num2', [''])[0])
            operator = query_components.get('operator', [''])[0]

            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    result = "Error: Division by zero"
                else:
                    result = num1 / num2
            else:
                result = "Error: Invalid operator"

            # Send the result back to the client
            self.send_response(200)  # HTTP status code 200 OK
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(str(result).encode('utf-8'))
        elif self.path.startswith("/redirect"):
            query_components = parse_qs(urlparse(self.path).query)
            search_query = unquote_plus(query_components.get('query', [''])[0])
            search_engine = query_components.get('source', [''])[0]

            if search_engine == 'youtube':
                youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
                self.send_response(307)
                self.send_header('Location', youtube_url)
                self.end_headers()
            elif search_engine == 'google':
                google_url = f"https://www.google.com/search?q={search_query}"
                self.send_response(307)
                self.send_header('Location', google_url)
                self.end_headers()
        elif parsed_path.path == "/explorer":
            # Handle file explorer page
            files_html = self.list_files_html()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body><h1>File Explorer</h1>{files_html}</body></html>".encode("utf-8"))
        elif parsed_path.path.startswith("/files"):
            content_type = self.get_content_type(parsed_path.path)

            message, content_type, response_code = checkIfExist(parsed_path.path[1:], content_type)
            if type(message) == str:
                message = bytes(message, "utf8")

            self.send_response(response_code)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(message)

        else:
            print(self.requestline)
            for header, value in self.headers.items():
                print(header + ": " + value)

            # Call the student-edited server code.
            message, content_type, response_code = handle_req(self.path)

            # Convert the return value into a byte string for network transmission
            if type(message) == str:
                message = bytes(message, "utf8")

            # print(message)
            self.__c_send_response(
                message,
                response_code,
                {
                    "Content-Type": content_type,
                    "Content-Length": len(message),
                    "X-Content-Type-Options": "nosniff",
                },
            )

    def do_POST(self):
        global table
        body = self.__c_read_body()
        message, content_type, response_code = handle_req(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        if self.path.startswith("/EventLog"):
            file_content = open("static/html/EventLog.html", encoding='utf-8').read()
            # Parse any form parameters submitted via POST
            parameters = get_body_params(body)
            if(parameters != {}):  
                table = table+submission_to_table(parameters)
            file_content = file_content.replace("<tbody></tbody>", "<tbody>"+table+"</tbody>")

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"{file_content}".encode("utf-8"))
            
        else:
            self.__c_send_response(
                message,
                response_code,
                {
                    "Content-Type": content_type,
                    "Content-Length": len(message),
                    "X-Content-Type-Options": "nosniff",
                },
            )
    def log_response(self, response_code, headers):
        log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} [{response_code}, {headers}]\n"
        with open("response.log", "a") as log_file:
            log_file.write(log_entry)


def run():
    PORT = 9016
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
