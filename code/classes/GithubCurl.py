import urllib.request

class GithubCurl:

	__token = None

	def setToken(token):
		GithubCurl.__token = token

	def __init__(self) -> None:
		return
	

	def get(self, url):
		if not GithubCurl.__token:
			raise TokenNotExistsError()
		
		req = urllib.request.Request(url)
		# req.add_header("User-Agent", "")
		req.add_header("Authorization", f'token {self.__token}')
		res = urllib.request.urlopen(req)
		return res


class TokenNotExistsError(Exception):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
		
	def __str__(self):
		return "トークンが存在していません。"