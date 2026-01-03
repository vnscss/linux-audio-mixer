import webview
from audio import AudioAPI

audio = AudioAPI()

window = webview.create_window(
    title="Linux Audio Mixer",
    url="../UI/index.html",
    js_api=audio,
    width=500,
    height=400,
    confirm_close=False
)

webview.start(debug=True)
