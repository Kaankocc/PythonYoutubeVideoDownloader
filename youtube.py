import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from pytube import YouTube

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_folder = ""
        self.init_ui()

    def init_ui(self):
        # Set up the user interface
        self.setWindowTitle("YouTube Video Downloader")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()  # Create a vertical layout

        # Welcome label
        welcome_label = QLabel("Welcome to YouTube Downloader", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; color: #9195F6; font-weight: bold;")
        layout.addWidget(welcome_label)

        # URL label and entry field
        url_label = QLabel("Please enter a YouTube URL:", self)
        url_label.setStyleSheet("font-size: 16px; color: #9195F6;")
        layout.addWidget(url_label)
        self.url_entry = QLineEdit(self)
        self.url_entry.setStyleSheet("font-size: 16px; color: #31363F; border: 1px solid #CCCCCC; padding: 5px;")
        layout.addWidget(self.url_entry)

        # Button to select download folder
        select_folder_button = QPushButton("Select Folder", self)
        select_folder_button.setStyleSheet("font-size: 16px; background-color: #9195F6; color: #FFFFFF; border: none; border-radius: 15px; padding: 10px 20px;")
        select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(select_folder_button)

        # Button to start download
        download_button = QPushButton("Download", self)
        download_button.setStyleSheet("font-size: 16px; background-color: #9195F6; color: #FFFFFF; border: none; border-radius: 15px; padding: 10px 20px;")
        download_button.clicked.connect(self.download)
        layout.addWidget(download_button)

        self.setLayout(layout)

    def select_folder(self):
        # Open a dialog to select a folder
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_folder = folder
            QMessageBox.information(self, "Folder Selected", f"Selected folder: {self.selected_folder}")

    def download(self):
        # Get the URL and check if a folder is selected before downloading
        url = self.url_entry.text()
        if not self.selected_folder:
            QMessageBox.warning(self, "Warning", "Please select a folder first.")
            return

        try:
            # Download the video
            yt = YouTube(url)
            streams = yt.streams.filter(progressive=True, file_extension="mp4")
            highest_res_stream = streams.get_highest_resolution()
            highest_res_stream.download(output_path=self.selected_folder)
            QMessageBox.information(self, "Download Successful", "Video downloaded successfully!")
        except Exception as e:
            # Handle download errors
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())
