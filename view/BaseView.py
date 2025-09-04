from abc import abstractmethod
from jinja2 import Environment

class BaseView:
	def __init__(self):
		self.__result: dict = {}

	def set_param(self, params: dict):
		self.params = params

	def tpl_assign(self, key: str, param):
		self.__result[key] = param
	
	@abstractmethod
	def execute(self)-> None:
		pass

	def render(self, env: Environment)-> str:
		self.execute()
		tpl = env.get_template(self.__class__.__name__ + ".html")
		return tpl.render(self.__result)