#!/usr/bin/python
import json
import os, subprocess, webbrowser
import requests
from PIL import Image
from io import BytesIO
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QLineEdit

from GrayScaleImageWindow import GrayscaleImageWindow
from RgbImageWindow import RgbImageWindow


class ClickHandler:
    def __init__(self, mw):
        # Container is the main window of the click handler
        self.container = mw

    def handle(self, func):
        if self.container.mdiArea.currentSubWindow():
            sub_window = func()
            if not sub_window:
                pass
                # QMessageBox.information(self.container, "Error", "Unable to add a sub window")
            elif sub_window != self.container.mdiArea.currentSubWindow():
                self.container.mdiArea.addSubWindow(sub_window)
                sub_window.show()

    def handle_open(self, relative_path: str = ""):
        if not relative_path:
            my_path = "./Photos_Library_photoslibrary/"
        else:
            my_path = "./Photos_Library_photoslibrary/" + relative_path
        file_name = QFileDialog.getOpenFileName(self.container, "Choose an image file", my_path)
        if os.path.isfile(file_name[0]):
            image = QImage(file_name[0])
            if not image.isNull():
                self.container.lwindow.add_list_item(file_name[0])
                self.container.bwindow.update_image_info(file_name[0])
                # Create a new image window with the option 0
                if image.format() == QImage.Format_Indexed8:
                    # Create a gray scale image
                    subwindow = GrayscaleImageWindow(file_name[0], 0, self.container)
                else:
                    # Create a rgb color image
                    subwindow = RgbImageWindow(file_name[0], 0, self.container)

                if not subwindow:
                    QMessageBox.information(self, "Error", "Fail to create a sub window")
                else:
                    self.container.mdiArea.addSubWindow(subwindow)
                    subwindow.show()

    def parse_json(self):
        settings = open("default/userDefault.json")
        settings_text = ''
        for line in settings:
            settings_text += line
        settings.close()
        return json.loads(settings_text)

    def handle_open_for_json(self):
        json_obj = self.parse_json()
        for file_name in list(set(json_obj['open-windows'])):
            if os.path.isfile(file_name):
                image = QImage(file_name)
                if not image.isNull():
                    self.container.lwindow.add_list_item(file_name)
                    self.container.bwindow.update_image_info(file_name)
                    # Create a new image window with the option 0
                    if image.format() == QImage.Format_Indexed8:
                        # Create a gray scale image
                        subwindow = GrayscaleImageWindow(file_name, 0, self.container)
                    else:
                        # Create a rgb color image
                        subwindow = RgbImageWindow(file_name, 0, self.container)

                    if not subwindow:
                        QMessageBox.information(self, "Error", "Fail to create a sub window")
                    else:
                        self.container.mdiArea.addSubWindow(subwindow)
                        subwindow.show()

    def open_url_image(self, url="https://upload.wikimedia.org/wikipedia/ru/f/fd/Everything_Has_Changed.png"):
        if len(url) == 0:
            response = requests.get("https://upload.wikimedia.org/wikipedia/ru/f/fd/Everything_Has_Changed.png")
        else:
            response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        # img.show()
        file_name = "URL image"
        # self.container.lwindow.add_list_item(file_name)
        # self.container.bwindow.update_image_info(file_name)
        # Create a new image window with the option 0
        subwindow = RgbImageWindow(file_name, 0, self.container, img)
        subwindow.update_pixmap(subwindow.image)
        if not subwindow:
            QMessageBox.information(self, "Error", "Fail to create a sub window")
        else:
            self.container.mdiArea.addSubWindow(subwindow)
            subwindow.show()

    def handle_url(self):
        text, okPressed = QInputDialog.getText(self.container, "Open Image from URL", "Image address:", QLineEdit.Normal, "")
        if okPressed:
            self.open_url_image(text)

    def openWithPath(self, path_name):
        self.handle_open(path_name)

    def handle_finder(self):
        my_path = "./Photos_Library_photoslibrary/"
        subprocess.check_call(['open', '--', my_path])

    def handle_camera(self):
        os.system('open -a FaceTime.app')

    def handle_open_with_app(self):
        if isinstance(self.container.mdiArea.activeSubWindow(), RgbImageWindow) or \
                isinstance(self.container.mdiArea.activeSubWindow(), GrayscaleImageWindow):
            my_path =  self.container.mdiArea.activeSubWindow().name
            print(my_path + " is file? " + str(os.path.isfile(my_path)))
            if os.path.isfile(my_path):
                subprocess.check_call(['open', '--', my_path])

    def handle_instagram(self):
        webbrowser.open('https://www.instagram.com', new=0, autoraise=True)

    def handle_twitter(self):
        webbrowser.open('https://twitter.com', new=0, autoraise=True)

    def handle_snapchat(self):
        webbrowser.open('https://www.snapchat.com', new=0, autoraise=True)

    def handle_close_all(self):
        window_list = []
        for subwindow in self.container.mdiArea.subWindowList():
            window_list.append(subwindow.name)
        json_obj = self.parse_json()
        json_obj["open-windows"] = window_list
        self.save_json(json_obj)
        self.container.mdiArea.closeAllSubWindows()

    def handle_close_event(self):
        window_list = []
        for subwindow in self.container.mdiArea.subWindowList():
            window_list.append(subwindow.name)
        json_obj = self.parse_json()
        json_obj["open-windows"] = window_list
        self.save_json(json_obj)

    def save_json(self, json_obj):
        # save to file
        with open("default/userDefault.json", "w") as file:
            json.dump(json_obj, file)

    def handle_save(self):
        pass

    def handle_info(self):
        self.handle(self.container.mdiArea.currentSubWindow().info)

    def handle_reverse(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().reverse)
        elif isinstance(self.container.mdiArea.currentSubWindow(), GrayscaleImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().reverse)

    def handle_saturate_red(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().saturate_red)

    def handle_saturate_green(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().saturate_green)

    def handle_saturate_blue(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().saturate_blue)

    def handle_to_grayscale(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().to_grayscale)

    def handle_original_color(self):
        self.handle(self.container.mdiArea.currentSubWindow().origin_color)

    def handle_threshold(self):
        self.handle(self.container.mdiArea.currentSubWindow().threshold)

    def handle_blur(self):
        self.handle(self.container.mdiArea.currentSubWindow().blur)

    def handle_sharpen(self):
        self.handle(self.container.mdiArea.currentSubWindow().sharpen)

    def handle_ccl(self):
        self.handle(self.container.mdiArea.currentSubWindow().ccl)

    def handle_hsl(self):
        self.handle(self.container.mdiArea.currentSubWindow().hsl)

    def handle_outline(self):
        self.handle(self.container.mdiArea.currentSubWindow().outline)

    def handle_floyd(self):
        pass

    def handle_clipboard(self):
        self.container.clipboardChanged()

    def handle_rgb(self):
        self.handle(self.container.mdiArea.currentSubWindow().set_rgb)

    def handle_filter(self):
        self.handle(self.container.mdiArea.currentSubWindow().filter)

    def handle_crop(self):
        self.handle(self.container.mdiArea.currentSubWindow().crop)

    def handle_timer(self):
        self.handle(self.container.mdiArea.currentSubWindow().timer)

    def handle_toggle_l(self):
        if  self.container.gridLayout.columnMinimumWidth(1) > 200:
            self.container.gridLayout.setColumnMinimumWidth(1, 1)
            self.container.lwindow.hide()
            self.container.gridLayout.removeWidget(self.container.lwindow)
        else:
            self.container.gridLayout.setColumnMinimumWidth(1, 220)
            self.container.lwindow.show()
            self.container.gridLayout.addWidget(self.container.lwindow, 1, 1)

    def handle_toggle_r(self):
        if self.container.gridLayout.columnMinimumWidth(3) > 200:
            self.container.gridLayout.setColumnMinimumWidth(3, 1)
            self.container.rwindow.hide()
            self.container.gridLayout.removeWidget(self.container.rwindow)
        else:
            self.container.gridLayout.setColumnMinimumWidth(3, 220)
            self.container.rwindow.show()
            self.container.gridLayout.addWidget(self.container.rwindow, 1, 3)

    def handle_toggle_b(self):
        if self.container.gridLayout.rowMinimumHeight(2) > 120:
            self.container.gridLayout.setRowMinimumHeight(2, 1)
            self.container.bwindow.hide()
            self.container.gridLayout.removeWidget(self.container.bwindow)
        else:
            self.container.gridLayout.setRowMinimumHeight(2, 140)
            self.container.bwindow.show()
            self.container.gridLayout.addWidget(self.container.bwindow, 2, 1, 1, 3)

