def wsgi_application(environ, start_response):

    body = [bytes(param + '\n', 'ascii') for param in environ['QUERY_STRING'].split('&')]

    status = '200 OK'
    headers = [
        ('Content-Type', 'text/plain')
    ]
    start_response(status, headers)

    return body
