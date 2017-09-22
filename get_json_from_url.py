import urllib, json

def get_json_from_url(url, parameters):
    """
    :rtype: string
    """
    query_string = urllib.urlencode(parameters)
    final_url = url+'?'+query_string
    response = urllib.urlopen(final_url)
    data = json.loads(response.read())
    return data
