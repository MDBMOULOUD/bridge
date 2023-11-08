from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
import os
import csv
from kivy import platform


class FolderSearchApp(MDApp):
    selected_path = None  # Add a class variable to store the selected folder path

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.screen = MDScreen()
        self.result_label = MDLabel(
            text="Searching for 'LTE-Signal-Logger' folder...",
            halign="center",
            theme_text_color="Secondary"
        )
        self.btn_open_file_manager = MDRaisedButton(
            text="Open File Manager",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.open_file_manager
        )
        self.screen.add_widget(self.result_label)
        self.screen.add_widget(self.btn_open_file_manager)
        self.file_manager = MDFileManager()
        self.file_manager.exit_manager = self.exit_file_manager
        self.file_manager.select_path = self.select_path
        return self.screen

    def open_file_manager(self, *args):
        self.file_manager.show('/')  # Start the file manager in the root directory

    def select_path(self, path):
        self.file_manager.close()
        self.selected_path = path  # Store the selected folder path
        self.result_label.text = f"Folder selected: {path}. Converting .txt files to .csv..."
        self.convert_txt_to_csv(path)

    def exit_file_manager(self, *args):
        self.file_manager.close()

    def convert_txt_to_csv(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".txt"):
                    txt_file_path = os.path.join(root, file)
                    csv_file_path = os.path.join(root, os.path.splitext(file)[0] + ".csv")

                    with open(txt_file_path, 'r') as txt_file, open(csv_file_path, 'w', newline='') as csv_file:
                        # Read the content from the .txt file and write it to the .csv file
                        reader = csv.reader(txt_file, delimiter=' ')
                        writer = csv.writer(csv_file, delimiter=',')
                        for row in reader:
                            writer.writerow(row)

                    # Delete the .txt file after conversion
                    os.remove(txt_file_path)
                    self.result_label.text = f"Conversion to Csv files have been completed. .txt files deleted."

if __name__ == '__main__':
    FolderSearchApp().run()
