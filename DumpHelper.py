import requests

class BoardSettings:
	def __init__(self, board):
		retry_attempts = 10
		for attempt in range(retry_attempts):
			settings_url = "https://8ch.net/settings.php?board={0}".format(board)
			try:
				r = requests.get(settings_url)
				j = r.json()
			except requests.exceptions.Timeout:
				print("Could not connect to {0}, retrying (retry {1}/{2})", settings_url, attempt, retry_attempts)
				continue
			except requests.exceptions.RequestException as e:
				print(e)
				exit()
			except ValueError as e:
				print("Failed to get json response from {0}\nError: {1}, retrying (retry {2}/{3})".format(settings_url, e, attempt, retry_attempts))
				continue
			break
		self.allowed_extensions = [".{0}".format(ext) for ext in j["allowed_ext"] + j["allowed_ext_files"]]
		self.max_files = j["max_images"]
		self.captcha_enabled = j["captcha"]["enabled"]
		self.new_thread_captcha = j["new_thread_capt"]