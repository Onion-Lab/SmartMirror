import subprocess

def streaming(isStreaming):
    if isStreaming:
        subprocess.run("sudo systemctl start smartmirror-streamer.service", shell=True)
    else:
        subprocess.run("sudo systemctl stop smartmirror-streamer.service", shell=True)
