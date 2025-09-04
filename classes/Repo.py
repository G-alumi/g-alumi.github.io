from datetime import date, datetime

class Repo:
	def __init__(self, d) -> None:
		self.repo: str					= d["repo"]
		self.name: str					= d["name"]
		self.description: str			= d["description"]
		self.thumbnails: list[str]		= d["thumbnails"]
		self.updates: list[Repo.Update] = Repo.Update.generate(d["updates"])

	@classmethod
	def generate(cls, l:list[dict]) -> list["Repo"]:
		res: list["Repo"] = []
		for item in l:
			res.append(cls(item))
		return res
	
	def getRelease(self):
		return f'https://github.com/{self.repo}/releases/latest'
	
	def getUrl(self):
		return f'https://github.com/{self.repo}'

	def getThumbnailsUrl(self):
		return f'https://raw.githubusercontent.com/{self.repo}/refs/tags/{self.updates[0].tag}/{self.thumbnails[0]}'

	def getDict(self):
		res = self.__dict__.copy()
		res["updates"] = [update.getDict() for update in self.updates]
		return res

	class Update:
		def __init__(self, d):
			self.tag: str			= d["tag"]
			self.date: date			= datetime.strptime(d["date"], "%Y-%m-%d").date()
			self.description: str	= d["description"]

		@classmethod
		def generate(cls, l:list[dict]) -> list["Repo.Update"]:
			res: list["Repo.Update"] = []
			for item in l:
				res.append(cls(item))
			return res
		
		def getDict(self):
			res = self.__dict__.copy()
			res["date"] = self.date.strftime("%Y-%m-%d")
			return res
