# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2022-present Artic

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from http.client import (
    HTTPSConnection,
    HTTPResponse
)

class Response:
    def __init__(self, response: HTTPResponse) -> None:
        assert isinstance(response, HTTPResponse), f"The argument \"response\" takes a {type(HTTPResponse)} value, not a {type(response)}"

        self.response = response

        return
    
def get(host: str, url: str, timeout: float = None) -> Response:
    connection: HTTPSConnection = HTTPSConnection(
        host=host,
        timeout=timeout
    )
    connection.request(
        method="GET",
        url=url
    )
    response: HTTPResponse = connection.getresponse()
    return Response(response).response