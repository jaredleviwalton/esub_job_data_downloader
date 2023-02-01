"""
MIT License

Copyright (c) 2022 Jared Walton <jared.levi.walton@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os

import _secrets

BASE_FOLDER = None
FULL_SCREEN_CHROME = False
NUM_CONCURRENT_SESSIONS = None

USER_NAME = _secrets.USER_NAME
USER_PASS = _secrets.USER_PASS

LOGIN_URL = "https://app.esub.com/login"
PROJECTS_URL = "https://app.esub.com/project"

if BASE_FOLDER is None:
    BASE_FOLDER = os.path.abspath(os.getcwd())

CHROME_DOWNLOAD_FOLDER_PATH = os.path.join(BASE_FOLDER, "downloads")
DOWNLOAD_BASE_FOLDER = os.path.join(BASE_FOLDER, "payload")
DEBUG_PATH = os.path.join(BASE_FOLDER, "debug")
REMAINING_PATH = os.path.join(BASE_FOLDER, "remaining")
