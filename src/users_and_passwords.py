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

USER_NAME = _secrets.USER_NAME
USER_PASS = _secrets.USER_PASS

LOGIN_URL = "https://app.esub.com/login"
PROJECTS_URL = "https://app.esub.com/project"

BASE_FOLDER = None

FULL_SCREEN_CHROME = False

if BASE_FOLDER is None:
    BASE_FOLDER = os.path.abspath(os.getcwd())

CHROME_DOWNLOAD_FOLDER_PATH = os.path.join(BASE_FOLDER, "downloads")
DOWNLOAD_BASE_FOLDER = os.path.join(BASE_FOLDER, "payload")
DEBUG_PATH = os.path.join(BASE_FOLDER, "debug")
REMAINING_PATH = os.path.join(BASE_FOLDER, "remaining")

PROJECT_URLS = [
    "https://app.esub.com/project/1",
    "https://app.esub.com/project/3",
    "https://app.esub.com/project/3",
    # "https://app.esub.com/project/4",  # <--------------------------
    "https://app.esub.com/project/5",
    "https://app.esub.com/project/6",
    "https://app.esub.com/project/7",
    "https://app.esub.com/project/8",
    "https://app.esub.com/project/9",
    "https://app.esub.com/project/10",
    "https://app.esub.com/project/11",
    "https://app.esub.com/project/12",
    "https://app.esub.com/project/13",
    "https://app.esub.com/project/14",
    "https://app.esub.com/project/15",
    "https://app.esub.com/project/16",
    "https://app.esub.com/project/17",
    "https://app.esub.com/project/18",
    "https://app.esub.com/project/19",
    "https://app.esub.com/project/20",
    "https://app.esub.com/project/21",
    "https://app.esub.com/project/22",
    "https://app.esub.com/project/23",
    "https://app.esub.com/project/24",
    "https://app.esub.com/project/25",
    "https://app.esub.com/project/26",
    "https://app.esub.com/project/27",
    "https://app.esub.com/project/28",
    "https://app.esub.com/project/29",
    "https://app.esub.com/project/29",
    "https://app.esub.com/project/30",
    "https://app.esub.com/project/31",
    "https://app.esub.com/project/32",
    "https://app.esub.com/project/33",
    "https://app.esub.com/project/34",
    "https://app.esub.com/project/35",
    "https://app.esub.com/project/36",
    "https://app.esub.com/project/37",
    "https://app.esub.com/project/38",
    "https://app.esub.com/project/39",
    "https://app.esub.com/project/40",
    "https://app.esub.com/project/41",
    "https://app.esub.com/project/42",
    "https://app.esub.com/project/43",
    "https://app.esub.com/project/44",
    "https://app.esub.com/project/45",
    "https://app.esub.com/project/46",
    "https://app.esub.com/project/47",
    "https://app.esub.com/project/48",
    "https://app.esub.com/project/49",
    "https://app.esub.com/project/50",
    "https://app.esub.com/project/51",
    "https://app.esub.com/project/52",
    "https://app.esub.com/project/53",
    "https://app.esub.com/project/53",
    "https://app.esub.com/project/54",
    "https://app.esub.com/project/55",
    "https://app.esub.com/project/56",
    "https://app.esub.com/project/10056",
    "https://app.esub.com/project/10057",
    "https://app.esub.com/project/10058",
    "https://app.esub.com/project/10059",
    "https://app.esub.com/project/10060",
    "https://app.esub.com/project/10061",
    "https://app.esub.com/project/10062",
    "https://app.esub.com/project/10063",
    "https://app.esub.com/project/10064",
    "https://app.esub.com/project/10065",
    "https://app.esub.com/project/10066",
    "https://app.esub.com/project/10067",
    "https://app.esub.com/project/10068",
    "https://app.esub.com/project/10069",
    "https://app.esub.com/project/10070",
    "https://app.esub.com/project/10071",
    "https://app.esub.com/project/10072",
    "https://app.esub.com/project/10073",
    "https://app.esub.com/project/10073",
    "https://app.esub.com/project/10074",
    "https://app.esub.com/project/10075",
    "https://app.esub.com/project/10076",
    "https://app.esub.com/project/10077",
    "https://app.esub.com/project/10078",
    "https://app.esub.com/project/10079",
    "https://app.esub.com/project/10080",
    "https://app.esub.com/project/10081",
    "https://app.esub.com/project/10082",
    "https://app.esub.com/project/10083",
    "https://app.esub.com/project/10084",
    "https://app.esub.com/project/10085",  # <----------------------------------
    "https://app.esub.com/project/10086",
    "https://app.esub.com/project/10087",
    "https://app.esub.com/project/10088",
    "https://app.esub.com/project/10089",
    "https://app.esub.com/project/10090",
    "https://app.esub.com/project/10091",
    "https://app.esub.com/project/10092",
    "https://app.esub.com/project/10093",
    "https://app.esub.com/project/10094",
    "https://app.esub.com/project/10095",
    "https://app.esub.com/project/10096",
    "https://app.esub.com/project/10097",
    "https://app.esub.com/project/10098",
    "https://app.esub.com/project/10099",
    "https://app.esub.com/project/10100",
    "https://app.esub.com/project/10101",
    "https://app.esub.com/project/10102",
    "https://app.esub.com/project/10103",
    "https://app.esub.com/project/10104",
    "https://app.esub.com/project/10105",
    "https://app.esub.com/project/10106",
    "https://app.esub.com/project/10107",
    "https://app.esub.com/project/10108",
    "https://app.esub.com/project/10109",
    "https://app.esub.com/project/10110",
    "https://app.esub.com/project/10111",
    "https://app.esub.com/project/10112",
    "https://app.esub.com/project/10113",
    "https://app.esub.com/project/10114",
    "https://app.esub.com/project/10115",
    "https://app.esub.com/project/10116",
    "https://app.esub.com/project/10117",
    "https://app.esub.com/project/10118",
    "https://app.esub.com/project/10119",
    "https://app.esub.com/project/10120",
    "https://app.esub.com/project/10121",
    "https://app.esub.com/project/10122",
    "https://app.esub.com/project/10123",
    "https://app.esub.com/project/10124",
    "https://app.esub.com/project/10125",
    "https://app.esub.com/project/10126",
    "https://app.esub.com/project/10127",
    "https://app.esub.com/project/10128",
    "https://app.esub.com/project/10129",
    "https://app.esub.com/project/10130",
    "https://app.esub.com/project/10131",
    "https://app.esub.com/project/10132",
    "https://app.esub.com/project/10133",
    "https://app.esub.com/project/10134",
    "https://app.esub.com/project/10136",
    "https://app.esub.com/project/10137",
    "https://app.esub.com/project/10138",
    "https://app.esub.com/project/10139",
    "https://app.esub.com/project/10141",
    "https://app.esub.com/project/10141",
    "https://app.esub.com/project/10142",
    "https://app.esub.com/project/10143",
    "https://app.esub.com/project/10144",
    "https://app.esub.com/project/10145",
    "https://app.esub.com/project/10146",
    "https://app.esub.com/project/10147",
    "https://app.esub.com/project/10148",
    "https://app.esub.com/project/10148",
    "https://app.esub.com/project/10149",
    "https://app.esub.com/project/10150",
    "https://app.esub.com/project/10151",
    "https://app.esub.com/project/10152",
    "https://app.esub.com/project/10153",
    "https://app.esub.com/project/10154",
    "https://app.esub.com/project/10155",
    "https://app.esub.com/project/10156",
    "https://app.esub.com/project/10157",
    "https://app.esub.com/project/10158",
    "https://app.esub.com/project/10159",
    "https://app.esub.com/project/10160",
    "https://app.esub.com/project/10161",
    "https://app.esub.com/project/10162",
    "https://app.esub.com/project/10163",
    "https://app.esub.com/project/10164",
    "https://app.esub.com/project/10165",
    "https://app.esub.com/project/10166",
    "https://app.esub.com/project/10167",
    "https://app.esub.com/project/10168",
    "https://app.esub.com/project/10169",
    "https://app.esub.com/project/10170",
    "https://app.esub.com/project/10171",
    "https://app.esub.com/project/10172",
    "https://app.esub.com/project/10173",
    "https://app.esub.com/project/10174",
    "https://app.esub.com/project/10175",
    "https://app.esub.com/project/10176",
    "https://app.esub.com/project/10177",
    "https://app.esub.com/project/10178",
    "https://app.esub.com/project/10179",
    "https://app.esub.com/project/10180",
    "https://app.esub.com/project/10181",
    "https://app.esub.com/project/10182",
    "https://app.esub.com/project/10183",
    "https://app.esub.com/project/10184",
    "https://app.esub.com/project/10185",
    "https://app.esub.com/project/10186",
    "https://app.esub.com/project/10187",
    "https://app.esub.com/project/10188",
    "https://app.esub.com/project/10189",
    "https://app.esub.com/project/10190",
    "https://app.esub.com/project/10191",
    "https://app.esub.com/project/10192",
    "https://app.esub.com/project/10193",
    "https://app.esub.com/project/10194",
    "https://app.esub.com/project/10195",
    "https://app.esub.com/project/10196",
    "https://app.esub.com/project/10197",
    "https://app.esub.com/project/10198",
    "https://app.esub.com/project/10199",
    "https://app.esub.com/project/10200",
    "https://app.esub.com/project/10201",
    "https://app.esub.com/project/10202",
    "https://app.esub.com/project/10203",
    "https://app.esub.com/project/10204",
    "https://app.esub.com/project/10205",
    "https://app.esub.com/project/10206",
    "https://app.esub.com/project/10207",
    "https://app.esub.com/project/10208",
    "https://app.esub.com/project/10209",
    "https://app.esub.com/project/10210",
    "https://app.esub.com/project/10211",
    "https://app.esub.com/project/10212",
    "https://app.esub.com/project/10213",
    "https://app.esub.com/project/10214",
    "https://app.esub.com/project/10215",
    "https://app.esub.com/project/10216",
    "https://app.esub.com/project/10217",
    "https://app.esub.com/project/10218",
    "https://app.esub.com/project/10219",
    "https://app.esub.com/project/10220",
    "https://app.esub.com/project/10221",
    "https://app.esub.com/project/10222",
    "https://app.esub.com/project/10223",
    "https://app.esub.com/project/10224",
    "https://app.esub.com/project/10225",
    "https://app.esub.com/project/10225",
    "https://app.esub.com/project/10226",
    "https://app.esub.com/project/10227",
    "https://app.esub.com/project/10228",
    "https://app.esub.com/project/10229",
    "https://app.esub.com/project/10230",
    "https://app.esub.com/project/10231",
    "https://app.esub.com/project/10232",
    "https://app.esub.com/project/10233",
    "https://app.esub.com/project/10234",
    "https://app.esub.com/project/10235",
    "https://app.esub.com/project/10236",
    "https://app.esub.com/project/10237",
    "https://app.esub.com/project/10238",
    "https://app.esub.com/project/10239",
    "https://app.esub.com/project/10239",
    "https://app.esub.com/project/10240",
    "https://app.esub.com/project/10240",
    "https://app.esub.com/project/10241",
    "https://app.esub.com/project/10242",
    "https://app.esub.com/project/10242",
    "https://app.esub.com/project/10243",
    "https://app.esub.com/project/10243",
    "https://app.esub.com/project/10244",
    "https://app.esub.com/project/10245",
    "https://app.esub.com/project/10246",
    "https://app.esub.com/project/10247",
    "https://app.esub.com/project/10248",
    "https://app.esub.com/project/10249",
    "https://app.esub.com/project/10250",
    "https://app.esub.com/project/10251",
    "https://app.esub.com/project/10252",
    "https://app.esub.com/project/10253",
    "https://app.esub.com/project/10254",
    "https://app.esub.com/project/10255",
    "https://app.esub.com/project/10256",
    "https://app.esub.com/project/10257",
    "https://app.esub.com/project/10258",
    "https://app.esub.com/project/10259",
    "https://app.esub.com/project/10260",
    "https://app.esub.com/project/10261",
    "https://app.esub.com/project/10262",
    "https://app.esub.com/project/10263",
    "https://app.esub.com/project/10264",
    "https://app.esub.com/project/10265",
    "https://app.esub.com/project/10266",
    "https://app.esub.com/project/10267",
    "https://app.esub.com/project/10268",
    "https://app.esub.com/project/10269",
    "https://app.esub.com/project/10270",
    "https://app.esub.com/project/10271",
    "https://app.esub.com/project/10272",
    "https://app.esub.com/project/10273",
    "https://app.esub.com/project/10274",
    "https://app.esub.com/project/10275",
    "https://app.esub.com/project/10276",
    "https://app.esub.com/project/10277",
    "https://app.esub.com/project/10278",
    "https://app.esub.com/project/10279",
    "https://app.esub.com/project/10280",
    "https://app.esub.com/project/10281",
    "https://app.esub.com/project/10282",
    "https://app.esub.com/project/10283",
    "https://app.esub.com/project/10284",
    "https://app.esub.com/project/10285",
    "https://app.esub.com/project/10286",
    "https://app.esub.com/project/10287",
    "https://app.esub.com/project/10288",
    "https://app.esub.com/project/10289",
    "https://app.esub.com/project/10290",
    "https://app.esub.com/project/10291",
]
