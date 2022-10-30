#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import argparse
import json
import os.path
import pathlib2 as pathlib

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.event import Event
from google.assistant.library.event import RenderResponseEvent
from google.assistant.library.file_helpers import existing_file
from google.assistant.library.device_helpers import register_device

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

import json
import wave
import pyaudio
import time

import pygame

pygame.mixer.init()

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
# DETECT_DING = os.path.join(TOP_DIR, "resources/ding.wav")
# DETECT_DONG = os.path.join(TOP_DIR, "resources/dong.wav")
DETECT_DING = "resources/ding.wav"

WARNING_NOT_REGISTERED = """
    This device is not registered. This means you will not be able to use
    Device Actions or see your device in Assistant Settings. In order to
    register this device follow instructions at:

    https://developers.google.com/assistant/sdk/guides/library/python/embed/register-device
"""

"""
def play_audio_file(fname=DETECT_DING):
    ding_wav = wave.open(fname, 'rb')
    ding_data = ding_wav.readframes(ding_wav.getnframes())
    audio = pyaudio.PyAudio()
    stream_out = audio.open(
        format=audio.get_format_from_width(ding_wav.getsampwidth()),
        channels=ding_wav.getnchannels(),
        rate=ding_wav.getframerate(), input=False, output=True)
    stream_out.start_stream()
    stream_out.write(ding_data)
    # time.sleep(0.2)
    stream_out.stop_stream()
    stream_out.close()
    audio.terminate()
"""

def play_audio_file(fname=DETECT_DING):
    ding = pygame.mixer.Sound(fname)
    ding.play()
    time.sleep(0.2)


def process_event(event, callback):
    print(event)
    if event.type == EventType.ON_MUTED_CHANGED:
        print("뮤트 정보")
        callback({'type':'ON_MUTED_CHANGED', 'text':''})
    elif event.type == EventType.ON_MEDIA_STATE_IDLE:
        print("미디어 IDLE")
        callback({'type':'ON_MEDIA_STATE_IDLE', 'text':''})
    elif event.type == EventType.ON_START_FINISHED:
        print("모든 초기화 완료")
        callback({'type':'ON_START_FINISHED', 'text':''})
    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        play_audio_file(DETECT_DING)
        print("사용자의 말하기 시작(핫워드감지)")
        callback({'type':'ON_CONVERSATION_TURN_STARTED', 'text':''})
    elif event.type == EventType.ON_END_OF_UTTERANCE:
        print("사용자의 말하기 끝")
        callback({'type':'ON_END_OF_UTTERANCE', 'text':''})
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        print("사용자의 말하기", event.args['text'])
        callback({'type':'ON_RECOGNIZING_SPEECH_FINISHED', 'text':event.args['text']})
    elif event.type == EventType.ON_RESPONDING_STARTED:
        print(" GAS가 말하기 시작!")
        callback({'type':'ON_RESPONDING_STARTED', 'text':''})
    elif event.type == EventType.ON_RENDER_RESPONSE:
        print("GAS의 답변", event.args['text'])
        callback({'type':'ON_RENDER_RESPONSE', 'text':event.args['text']})
    elif event.type == EventType.ON_RESPONDING_FINISHED:
        print("GAS 말하기 종료")
        callback({'type':'ON_RESPONDING_FINISHED', 'text':''})
    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        print("음성인식 종료")
        callback({'type':'ON_CONVERSATION_TURN_FINISHED', 'text':''})
    else:
        print("ERROR", event)



class AssistantManager():
    def __init__(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--device-model-id', '--device_model_id', type=str,
                            metavar='DEVICE_MODEL_ID', required=False,
                            help='the device model ID registered with Google')
        parser.add_argument('--project-id', '--project_id', type=str,
                            metavar='PROJECT_ID', required=False,
                            help='the project ID used to register this device')
        parser.add_argument('--nickname', type=str,
                            metavar='NICKNAME', required=False,
                            help='the nickname used to register this device')
        parser.add_argument('--device-config', type=str,
                            metavar='DEVICE_CONFIG_FILE',
                            default=os.path.join(
                                os.path.expanduser('~/.config'),
                                'googlesamples-assistant',
                                'device_config_library.json'
                            ),
                            help='path to store and read device configuration')
        parser.add_argument('--credentials', type=existing_file,
                            metavar='OAUTH2_CREDENTIALS_FILE',
                            default=os.path.join(
                                os.path.expanduser('~/.config'),
                                'google-oauthlib-tool',
                                'credentials.json'
                            ),
                            help='path to store and read OAuth2 credentials')
        parser.add_argument('--query', type=str,
                            metavar='QUERY',
                            help='query to send as soon as the Assistant starts')
        parser.add_argument('-v', '--version', action='version',
                            version='%(prog)s ' + Assistant.__version_str__())

        args = parser.parse_args()
        with open(args.credentials, 'r') as f:
            self.credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))

        self.device_model_id = None
        self.last_device_id = None
        self.project_id = args.project_id
        self.nickname = args.nickname
        self.query = args.query
        self.isMuted = False

        try:
            with open(args.device_config) as f:
                self.device_config = json.load(f)
                self.device_model_id = self.device_config['model_id']
                self.last_device_id = self.device_config.get('last_device_id', None)
        except FileNotFoundError:
            pass

        if not args.device_model_id and not self.device_model_id:
            raise Exception('Missing --device-model-id option')

        # Re-register if "device_model_id" is given by the user and it differs
        # from what we previously registered with.
        self.should_register = (
            args.device_model_id and args.device_model_id != self.device_model_id)

        self.device_model_id = args.device_model_id or self.device_model_id
        self.assistant = Assistant(self.credentials, self.device_model_id)
        self.events = self.assistant.start()


    def runGoogleAssistance(self, callback=None):
        device_id = self.assistant.device_id
        print('device_model_id:', self.device_model_id)
        print('device_id:', device_id + '\n')

        # Re-register if "device_id" is different from the last "device_id":
        if self.should_register or (device_id != self.last_device_id):
            if self.project_id:
                register_device(self.project_id, self.credentials,
                                self.device_model_id, device_id, self.nickname)
                pathlib.Path(os.path.dirname(self.device_config)).mkdir(
                    exist_ok=True)
                with open(self.device_config, 'w') as f:
                    json.dump({
                        'last_device_id': device_id,
                        'model_id': self.device_model_id,
                    }, f)
            else:
                print(WARNING_NOT_REGISTERED)
        self.assistant.set_mic_mute(True)
        for event in self.events:
            if event.type == EventType.ON_START_FINISHED and self.query:
                self.assistant.send_text_query(self.query)
            process_event(event, callback)


    def setMuteEnable(self, isMuted):
        print('뮤트한다?', isMuted)
        self.assistant.set_mic_mute(isMuted)



if __name__ == '__main__':
    gas = AssistantManager()
    # gas.setMuteEnable(True)
    gas.runGoogleAssistance()


