import urllib, json

def get_json_from_url(url, parameters):
    """Get JSON from given URL and query parameters.
	
	:param url: google API url on which GET request is made
	:type url: str
	:param parameters: URL query parameters
	:type parameters: dict
    :return data: response JSON from google search API
    :rtype data: str
    """
    query_string = urllib.urlencode(parameters)
    final_url = url+'?'+query_string
    response = urllib.urlopen(final_url)
    data = json.loads(response.read())
    return data
