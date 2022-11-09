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

from sys import (
    path,
    argv
)
from os import getcwd

from requests import (
    get,
    Response
)

if path[0] in ("", getcwd()):
    path.pop(0)

def __get__(name: str = None) -> None:
    if name is None:
        raise SyntaxError("Missing the \"name\" argument.")
    response: Response = get(
        url=f"https://pypi.org/pypi/{name}/json"
    )
    downloads: int = get(
        url=f"https://pypistats.org/api/packages/{name.replace('.', '-')}/recent"
    ).json()["data"]["last_month"]

    json: dict = response.json()
    info: dict = json["info"]

    try:
        _requires: str = "\n- ".join([i.split(" ")[0] for i in info["requires_dist"]])
    except TypeError:
        _requires: str = "No requires provided."
    _urls: str = "\n- ".join([f"{i}: {info['project_urls'][i]}" for i in list(info["project_urls"])])
    _versions: str = "\n- ".join([i for i in list(json["releases"])])

    print(f"""{info["name"]} {info["version"]} (https://pypi.org/project/{info["name"]}/)
by {info["author"] or (info["maintainer"] or "nobody")} ({info["author_email"] or (info["maintainer_email"] or "no email")})

maintained by {info["maintainer"] or (info["author"] or "nobody")} ({info["author_email"] or (info["maintainer_email"] or (info["author_email"] or "no email"))})

description: {info["summary"]}
downloads last month: {downloads}
license: {info["license"] or "no license"}

Requires:
- {_requires}

URLs:
- {_urls}

Versions:
- {_versions}""")
    return

__get__(argv[1])