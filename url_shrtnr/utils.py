def check_trailing_slash(url):
    """Checks if the given url has a slash at end"""
    last_char = url[-1]
    if last_char == "/":
        return url
    url += "/"
    return url
