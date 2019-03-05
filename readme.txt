TeamsExt is a Python extension to WebEx Teams that allows users to easily send messages to multiple spaces, simultaneously. For ease of management, template messages can be created and edited, multiple spaces can be bundled as lists.


Required Libraries:
Pyqt5
AIOHTTP
REQUESTS


Please fill the following variables in the app_config.py:

client_id = "<<your_client_id>>"
client_secret = "<<your_client_secret>>"
app_integration_url_test = "<<your_api_integration_test>>"
redirect_url = "https://github.com/ziadkiwan/teamsext"



To Package app:
pyinstaller TeamsExt.py --hidden-import=aiohttp --windowed
