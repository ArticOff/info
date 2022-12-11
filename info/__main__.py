# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2022-today Artic

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
from json import loads
from http.client import HTTPResponse

try:
    from .__Constants__ import (
        __author__,
        __description__,
        __version__
    )
    from .__Core__ import get
except ImportError:
    from info.__Constants__ import (
        __author__,
        __description__,
        __version__
    )
    from info.__Core__ import get

if path[0] in ("", getcwd()):
    path.pop(0)

def __v__() -> None:
    return print(__version__)

def __top__() -> None:
    a: HTTPResponse = get(
        host="pypistats.org",
        url="/top"
    )

    html: str = str(a.read(), "utf-8").replace("\n", "")

    _daily: list[tuple[int, str, str]]
    _weekly: list[tuple[int, str, str]]
    _monthly: list[tuple[int, str, str]]
    listed: list[str] = []
    _count: list[int] = []
    _names: list[str] = []
    _downloads: list[str] = []

    packages: list[tuple[int, str, int]]

    for item in html.split(r"           "):
        if any(letter in item for letter in [r"/packages/"]):
            if any(letter in item for letter in [r"__all__"]):
                continue
            listed.append(item)
        elif any(letter in item for letter in [r"<", r">"]):
            continue
        else:
            listed.append(item)

    for c, i in enumerate(listed):
        listed[c] = i.strip()

    while "" in listed:
        listed.remove("")

    listed: list[str] = listed[3:]

    for c, i in enumerate(listed):
        if c % 3 == 0:
            _count.append(int(i))
        elif c % 3 == 1:
            cache: list[str] = []
            _cache: str = i.split()[1]
            for item in _cache:
                if item == r"<":
                    break
                cache.append(item)
            _names.append(("".join(cache)).split(r">")[1])
        elif c % 3 == 2:
            _downloads.append(i.replace(r",", r""))

    packages: list[tuple[int, str, str]] = list(zip(_count, _names, _downloads))

    chunks: list[list[tuple[int, str, str]]] = [packages[x:x+20] for x in range(0, len(packages), 20)]
    _monthly: list[tuple[int, str, str]] = chunks[2]
    _weekly: list[tuple[int, str, str]] = chunks[1]
    _daily: list[tuple[int, str, str]] = chunks[0]

    day: str = "\n".join([f"{int(_daily[item][2]):,}\t{_daily[item][1]}" for item in range(len(_daily))])
    week: str = "\n".join([f"{int(_weekly[item][2]):,}\t{_weekly[item][1]}" for item in range(len(_weekly))])
    month: str = "\n".join([f"{int(_monthly[item][2]):,}\t{_monthly[item][1]}" for item in range(len(_monthly))])

    try:
        if argv[2] in ("-m", "Month"):
            print(f"Most downloaded past month:\n{month}")
        elif argv[2] in ("-w", "Week"):
            print(f"Most downloaded past week:\n{week}")
        elif argv[2] in ("-d", "Day"):
            print(f"Most downloaded past day:\n{day}")
        else:
            print(f"The argument {argv[2]} is not supported.")
            raise IndexError()
    except IndexError:
        print(f"\nMonthly (python -m info --top [-m | Month]):\n{month}\n")
        print(f"Weekly (python -m info --top [-w | Week]):\n{week}\n")
        print(f"Daily (python -m info --top [-d | Day]):\n{day}\n")
 
def __get__(name: str = None) -> None:
    try:
        if name is None:
            raise SyntaxError("Missing the \"name\" argument.")
        try:
            response: HTTPResponse = get(
                host="pypi.org",
                url=f"/pypi/{name}/json",
                timeout=10.0
            )
        except Exception:
            return print(f"The module cannot work without an Internet connection.")
        if response.status == 404:
            return print(f"This module doesn't exist.")
        try:
            downloads: str = "{:,}".format(loads(get(
                host="pypistats.org",
                url=f"/api/packages/{name.replace('.', '-').lower()}/recent",
                timeout=2.0
            ).read().decode("utf-8"))["data"]["last_month"])
        except Exception:
            downloads: str = "Unable to get downloads"
        json: dict = loads(response.read().decode("utf-8"))
        info: dict = json["info"]

        try:
            _requires: str = f"\n- ".join([i.split(" ")[0] for i in info["requires_dist"]])
        except TypeError:
            _requires: str = "No requires provided."
        try:
            _urls: str = f"\n- ".join([f"{i}: {info['project_urls'][i]}" for i in list(info["project_urls"])])
        except TypeError:
            _urls: str = "Unable to get the urls"
        _versions: str = f"Write \"python -m info {name} -v\" to see the versions"
        if len(json["releases"]) < 8:
            _versions: str = f"\n- ".join([i for i in list(json["releases"])])

        def _version() -> None:
            _versions: str = f"\n- ".join([i for i in list(json["releases"])])
            return print(f"- {_versions}")

        def _url() -> None:
            return print(f"- {_urls}")
        
        def _require() -> None:
            return print(f"- {_requires}")

        def _info() -> None:
            return print(f"""{info["name"]} {info["version"]} (https://pypi.org/project/{info["name"]}/)
by {info["author"] or (info["maintainer"] or "nobody")} ({info["author_email"] or (info["maintainer_email"] or "no email")})

maintained by {info["maintainer"] or (info["author"] or "nobody")} ({info["author_email"] or (info["maintainer_email"] or (info["author_email"] or "no email"))})

description: {info["summary"]}
downloads last month: {downloads}
license: {info["license"] or "no license"}""")
        try:
            if argv[2] in ("-v", "Versions"):
                return _version()
            
            if argv[2] in ("-u", "Urls"):
                return _url()

            if argv[2] in ("-r", "Requires"):
                return _require()
            
            if argv[2] in ("-i", "Info"):
                return _info()
            
            if argv[2] not in [*("-i", "Info"), *("-u", "Urls"), *("-r", "Requires"), *("-i", "Info")]:
                print(f"The argument \"{argv[2]}\" doesn't exist.\n-> python -m info\n")

        except IndexError:
            pass

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
    except Exception as e:
        return print(f"Error when searching this module: {e.__class__.__name__}: {e}")
    
try:
    if argv[1] == "--top":
        __top__()
    elif argv[1] == "--version":
        __v__()
    elif argv[1] == "--help":
        raise IndexError()
    else:
        __get__(argv[1])
except IndexError:
    print(f"""python -m info [<YOUR PACKAGE NAME> | <OPTIONS>] [SUBOPTIONS]

Infos:
    author: {__author__}
    version: {__version__}
    description: {__description__}

Options:
    --help             Shos the help message
    --top              Get the most downloaded PyPI package
    --version          Show the package version

Suboptions:
    -v / Version       Show the versions only
    -u / Urls          Show the URLs only
    -r / Requires      Show the requires only
    -i / Info          Show the package without the versions, URLs and requires
    (top) -d / Day     Show the most downloaded packages past day
    (top) -w / Week    Show the most downloaded packages past week
    (top) -m / Month   Show the most downloaded packages past month
""")