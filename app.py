import os
from dotenv import load_dotenv
import flet
from flet import *
import requests
import datetime

load_dotenv()

API_KEY = os.environ.get("API_KEY")
PART = os.environ.get("PART")
UNITS = os.environ.get("UNITS")
LANG = os.environ.get("LANG")
CITY_NAME = os.environ.get("CITY_NAME")
COUNTRY_CODE = os.environ.get("COUNTRY_CODE")
LIMIT = os.environ.get("LIMIT")

_current_city = requests.get(
    f"http://api.openweathermap.org/geo/1.0/direct?q={CITY_NAME},{COUNTRY_CODE}&limit={LIMIT}&appid={API_KEY}"
)

LAT = _current_city.json()[0]["lat"]
LON = _current_city.json()[0]["lon"]

_current = requests.get(
    f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&exclude={PART}&units={UNITS}&appid={API_KEY}&lang={LANG}"
)


days = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun",
]


def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def _expand(e):
        if e.data == "true":
            _c.content.controls[1].height = 560
            _c.content.controls[1].update()
        else:
            _c.content.controls[1].height = 660 * 0.4
            _c.content.controls[1].update()

    def _current_temp():
        _current_temp = int(_current.json()["current"]["temp"])
        _current_weather = _current.json()["current"]["weather"][0]["main"]
        _current_description = _current.json()["current"]["weather"][0]["description"]
        _current_wind = int(_current.json()["current"]["wind_speed"])
        _current_humidity = int(_current.json()["current"]["humidity"])
        _current_feels = int(_current.json()["current"]["feels_like"])

        return [
            _current_temp,
            _current_weather,
            _current_description,
            _current_wind,
            _current_humidity,
            _current_feels,
        ]

    def _current_extra():
        _extra_info = []

        _extra = [
            [
                int(_current.json()["current"]["visibility"] / 1000),
                "Km",
                "Visibility",
                "./assets/visibility.png",  # 視界
            ],
            [
                int(_current.json()["current"]["pressure"]),
                "hPa",
                "Pressure",
                "./assets/barometer.png",  # 気圧計
            ],
            [
                datetime.datetime.fromtimestamp(
                    _current.json()["current"]["sunset"]
                ).strftime("%H:%M"),
                "",
                "Sunset",
                "./assets/sunset.png",  # 日の入
            ],
            [
                datetime.datetime.fromtimestamp(
                    _current.json()["current"]["sunrise"]
                ).strftime("%H:%M"),
                "",
                "Sunrise",
                "./assets/sunrise.png",  # 日の出
            ],
        ]

        for data in _extra:
            _extra_info.append(
                Container(
                    bgcolor="white10",
                    border_radius=12,
                    alignment=alignment.center,
                    content=Column(
                        alignment="center",
                        horizontal_alignment="center",
                        spacing=25,
                        controls=[
                            Container(
                                alignment=alignment.center,
                                content=Image(
                                    src=data[3],
                                    color="white",
                                ),
                                width=32,
                                height=32,
                            ),
                            Container(
                                content=Column(
                                    alignment=alignment.center,
                                    horizontal_alignment="center",
                                    spacing=0,
                                    controls=[
                                        Text(
                                            str(
                                                data[0],
                                            ) + " " + data[1],
                                            size=14,
                                        ),
                                        Text(
                                            data[2],
                                            size=11,
                                            color="white54",
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
            )

        return _extra_info

    def _top():
        _today = _current_temp()

        _today_extra = GridView(
            max_extent=150,
            expand=1,
            run_spacing=5,
            spacing=5,
        )

        for info in _current_extra():
            _today_extra.controls.append(info)

        top = Container(
            width=310,
            height=660 * 0.40,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=["lightblue600", "lightblue900"],
            ),
            border_radius=35,
            animate=animation.Animation(
                duration=450,
                curve="decelerate",
            ),
            on_hover=lambda e: _expand(e),
            content=Column(
                alignment="start",
                spacing=10,
                controls=[
                    Row(
                        alignment="center",
                        controls=[
                            Text(
                                f'{_current_city.json()[0]["name"]} , {_current_city.json()[0]["country"]}',
                                size=16,
                                weight="w500",
                            ),
                        ],
                    ),
                    Container(
                        padding=padding.only(bottom=5),
                    ),
                    Row(
                        alignment="center",
                        spacing=30,
                        controls=[
                            Column(
                                controls=[
                                    Container(
                                        width=90,
                                        height=90,
                                        content=Image(
                                            src=f'./assets/forecast/{_current.json()["current"]["weather"][0]["main"].lower()}.png',
                                            color="white",
                                        ),
                                    ),
                                ]
                            ),
                            Column(
                                spacing=5,
                                horizontal_alignment="center",
                                controls=[
                                    Text(
                                        "Today",
                                        size=12,
                                        text_align="center",
                                    ),
                                    Row(
                                        vertical_alignment="start",
                                        spacing=0,
                                        controls=[
                                            Container(
                                                content=Text(
                                                    _today[0],  # 気温
                                                    size=52,
                                                ),
                                            ),
                                            Container(
                                                content=Text(
                                                    "°",
                                                    size=28,
                                                    text_align="center",
                                                ),
                                            ),
                                        ],
                                    ),
                                    Text(
                                        f"{_today[1]} - Overcast",  # 天候
                                        size=10,
                                        color="white54",
                                        text_align="center",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Divider(
                        height=8,
                        thickness=1,
                        color="white10",
                    ),
                    Row(
                        alignment="spaceAround",
                        controls=[
                            Container(
                                content=Column(
                                    horizontal_alignment="center",
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image(
                                                src="./assets/wind.png",  # 風速計
                                                color="white",
                                            ),
                                            width=20,
                                            height=20,
                                        ),
                                        Text(
                                            f"{_today[3]} km/h",  # 風速
                                            size=11,
                                        ),
                                        Text(
                                            "Wind",
                                            size=9,
                                            color="white54",
                                        ),
                                    ],
                                ),
                            ),
                            Container(
                                content=Column(
                                    horizontal_alignment="center",
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image(
                                                src="./assets/humidity.png",  # 湿度計
                                                color="white",
                                            ),
                                            width=20,
                                            height=20,
                                        ),
                                        Text(
                                            f"{_today[4]} %",  # 湿度
                                            size=11,
                                        ),
                                        Text(
                                            "Humidity",
                                            size=9,
                                            color="white54",
                                        ),
                                    ],
                                ),
                            ),
                            Container(
                                content=Column(
                                    horizontal_alignment="center",
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image(
                                                src="./assets/thermometer.png",  # 気温計
                                                color="white",
                                            ),
                                            width=20,
                                            height=20,
                                        ),
                                        Text(
                                            f"{_today[5]} °",  # 気温
                                            size=11,
                                        ),
                                        Text(
                                            "Feel like",
                                            size=9,
                                            color="white54",
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                    _today_extra,
                ],
            ),
        )

        return top

    def _bot_data():
        _bot_data = []

        for index in range(1, 8):
            _bot_data.append(
                Row(
                    spacing=5,
                    alignment="spaceBetween",
                    controls=[
                        Row(
                            expand=1,
                            alignment="start",
                            controls=[
                                Container(
                                    alignment=alignment.center,
                                    content=Text(
                                        days[
                                            datetime.datetime.weekday(
                                                datetime.datetime.fromtimestamp(
                                                    _current.json()["daily"][index]["dt"],
                                                ),
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                        Row(
                            expand=1,
                            controls=[
                                Container(
                                    content=Row(
                                        alignment="start",
                                        controls=[
                                            Container(
                                                width=20,
                                                height=20,
                                                alignment=alignment.center_left,
                                                content=Image(
                                                    src=f'./assets/forecast/{_current.json()["daily"][index]["weather"][0]["main"].lower()}.png',
                                                    color="white",
                                                ),
                                            ),
                                            Text(
                                                _current.json()["daily"][index]["weather"][0]["main"],
                                                size=11,
                                                color="white54",
                                                text_align="center",
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                        Row(
                            expand=1,
                            alignment="end",
                            controls=[
                                Container(
                                    alignment=alignment.center,
                                    content=Row(
                                        alignment="center",
                                        spacing=5,
                                        controls=[
                                            Container(
                                                width=20,
                                                content=Text(
                                                    int(
                                                        _current.json()["daily"][index]["temp"]["max"],
                                                    ),
                                                    text_align="start",
                                                ),
                                            ),
                                            Container(
                                                width=20,
                                                content=Text(
                                                    int(
                                                        _current.json()["daily"][index]["temp"]["min"],
                                                    ),
                                                    text_align="end",
                                                ),
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            )

        return _bot_data

    def _bottom():
        _bot_column = Column(
            alignment="center",
            horizontal_alignment="center",
            spacing=25,
        )

        for data in _bot_data():
            _bot_column.controls.append(data)

        bottom = Container(
            padding=padding.only(
                top=280,
                left=20,
                right=20,
                bottom=20,
            ),
            content=_bot_column,
        )

        return bottom

    _c = Container(
        width=310,
        height=660,
        border_radius=35,
        bgcolor="black",
        padding=10,
        content=Stack(
            width=300,
            height=550,
            controls=[
                _bottom(),
                _top(),
            ],
        ),
    )

    page.add(_c)


if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")
