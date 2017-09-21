import urllib, json

def get_json_from_url(url):
    """
    :rtype: string
    """
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data
