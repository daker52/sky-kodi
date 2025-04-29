import re
import urllib.request
import urllib.parse
import http.cookiejar

def login(username, password):
    login_url = "https://www.sdilej.cz/prihlaseni"
    post_data = urllib.parse.urlencode({
        "username": username,
        "password": password
    }).encode("utf-8")

    # Správa cookies
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(login_url, data=post_data, headers=headers)
    opener.open(req)  # provede login

    return opener  # vracíme otevřený session opener

def get_stream_url(page_url, username, password):
    opener = login(username, password)

    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(page_url, headers=headers)
    response = opener.open(req)
    html = response.read().decode('utf-8')

    match = re.search(
        r'https://s\d+\.sdilej\.cz/sdilej_profi\.php\?id=\d+&stream=1&session=[a-f0-9]+',
        html
    )
    if match:
        return match.group(0)

    raise Exception("Stream link nebyl nalezen.")
