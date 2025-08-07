import flet as ft
from flet import TextField
import datetime
import time
import requests

def main(page: ft.Page):
    page.title = "LogBook"
    page.theme_mode = "Dark"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def show_login():
        username: TextField = TextField("", text_align=ft.TextAlign.CENTER, label="Username")
        password: TextField = TextField("", text_align=ft.TextAlign.CENTER, label="Password", password=True)

        def login(e):
            login = username.value
            passwrd = password.value
            url = "https://api.fakhrulhakimy.tech/login"
            data = {
                "username": login,
                "password": passwrd
            }

            response = requests.post(url, json=data)

            if response.status_code == 200:
                msg = ft.Text("Login Success ✅", color="green")
                page.controls.append(ft.Row([msg], alignment=ft.MainAxisAlignment.CENTER))
                page.update()
                time.sleep(1)
                show_logbook()
            else:
                msg = ft.Text("❌ Login Failed", color="red")
                page.controls.append(ft.Row([msg], alignment=ft.MainAxisAlignment.CENTER))
                page.update()
                time.sleep(2)
                page.controls.pop()  # remove error message
                page.update()

        page.controls.clear()
        page.add(
            ft.Row([ft.Image(src="logo.png", width=230)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([username], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([password], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.TextButton(text="LOGIN", on_click=login)], alignment=ft.MainAxisAlignment.CENTER)
        )
        page.update()

    def show_logbook():
        page.controls.clear()

        comment: TextField = TextField("", text_align=ft.TextAlign.CENTER, width=1000, multiline=True, label="Comment", min_lines=1, max_lines=3)
        image_preview = ft.Image(width=200, height=200)

        file_picker = ft.FilePicker(on_result=lambda e: on_file_result(e, image_preview))
        page.overlay.append(file_picker)

        time_in = ft.TimePicker()
        time_out = ft.TimePicker()
        date_picker = ft.DatePicker(
            first_date=datetime.datetime(year=2000, month=10, day=1),
            last_date=datetime.datetime(year=2025, month=10, day=1),
        )

        def on_file_result(e: ft.FilePickerResultEvent, image_preview):
            if e.files:
                image_preview.src = e.files[0].path
                page.update()

        def submit(e):
            import os

            url = "https://api.fakhrulhakimy.tech/logs"

            # Collect data
            date = date_picker.value.strftime('%d/%m/%Y')
            Din = time_in.value
            Dout = time_out.value
            Dcomment = comment.value
            image_path = image_preview.src  # This must be a valid file path on disk

            # Validate image path exists
            if not os.path.isfile(image_path):
                print("❌ Invalid image path")
                return

            # Prepare form data and file
            with open(image_path, "rb") as img_file:
                files = {
                    "file": (os.path.basename(image_path), img_file, "image/png")  # or image/jpeg if needed
                }
                data = {
                    "date": date,
                    "time_in": Din,
                    "time_out": Dout,
                    "comment": Dcomment
                }

                # Send the request
                response = requests.post(url, data=data, files=files)

            if response.status_code == 200:
                msg = ft.Text("Log add to the system ✅", color="green")
                page.controls.append(ft.Row([msg], alignment=ft.MainAxisAlignment.CENTER))
                page.update()
                time.sleep(1)
                page.update()
                time.sleep(1)
                show_logbook()
            else:
                msg = ft.Text("Log failed to be add", color="red")
                page.controls.append(ft.Row([msg], alignment=ft.MainAxisAlignment.CENTER))
                page.update()
                time.sleep(1)
                page.controls.pop()  # remove error message
                page.update()





        page.add(
            image_preview,
            ft.ElevatedButton("Pick date", width=1000, icon=ft.Icons.CALENDAR_MONTH, on_click=lambda e: page.open(date_picker)),
            ft.ElevatedButton("Time-in", width=1000, icon=ft.Icons.TIME_TO_LEAVE, on_click=lambda _: page.open(time_in)),
            ft.ElevatedButton("Time-out", width=1000, icon=ft.Icons.TIME_TO_LEAVE, on_click=lambda _: page.open(time_out)),
            comment,
            ft.ElevatedButton("Choose image...", width=1000, on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"])),
            ft.Row([ft.TextButton(text="Submit", on_click=submit)], alignment=ft.MainAxisAlignment.CENTER),
        )
        page.update()

    # Show login screen first
    show_login()

ft.app(target=main)
