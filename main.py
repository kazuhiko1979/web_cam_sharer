from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

import wikipedia
import requests

Builder.load_file('frontend.kv')

# ヘッダーにユーザーエージェントを設定
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

class FirstScreen(Screen):

	def get_image_link(self):
		# Get user query from TextInput
		query = self.manager.current_screen.ids.user_query.text
		# Get wikipedia page and the first image link
		page = wikipedia.page(query)
		image_link = page.images[0]
		return image_link

	def download_image(self):
		try:
			req = requests.get(self.get_image_link(), headers=headers)
			if req.status_code == 200:
				imagepath = 'files/image.jpg'
				with open(imagepath, "wb") as f:
					f.write(req.content)
				return imagepath
			else:
				print(f"HTTP- Error Code: {req.status_code}")
		except Exception as e:
			print(f"Error: {str(e)}")

	def set_image(self):
		self.manager.current_screen.ids.img.source = self.download_image()

class RootWidget(ScreenManager):
	pass


class MainApp(App):

	def build(self):
		return RootWidget()


MainApp().run()
