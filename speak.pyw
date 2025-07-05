import sys
import os
import subprocess
from PyQt5 import QtWidgets, QtCore
from espeakng import Speaker

class TTSApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

       
        self.esng = Speaker(path='./espeak')

        self.voices = [
            "af", "am", "ar", "az", "be", "bg", "bn", "bs", "ca", "cs",
            "cy", "da", "de", "el", "en", "en-sc", "en-gb", "en-n", "en-rp",
            "en-wmids", "en-westindies", "eo", "es", "es-la", "et", "eu", "fa",
            "fi", "fr", "fr-be", "fr-ca", "fr-ch", "gl", "he", "hi", "hr",
            "ht", "hu", "hy", "id", "is", "it", "ja", "ka", "km", "kn",
            "ko", "ku", "la", "lv", "mk", "ml", "mn", "mr", "ms", "my",
            "ne", "nl", "no", "oc", "pa", "pl", "pt", "pt-br", "ro", "ru",
            "si", "sk", "sl", "so", "sq", "sr", "sv", "sw", "ta", "te",
            "th", "tl", "tr", "uk", "ur", "uz", "vi", "zh", "zh-yue"
        ]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("espeak for fallout76boy")
        layout = QtWidgets.QVBoxLayout()

        self.text_input = QtWidgets.QTextEdit()
        self.text_input.setPlaceholderText("write something (dont be racist)")
        layout.addWidget(self.text_input)

        layout.addWidget(QtWidgets.QLabel(" (Voice):"))
        self.voice_combo = QtWidgets.QComboBox()
        self.voice_combo.addItems(self.voices)
        self.voice_combo.setCurrentText("en")
        layout.addWidget(self.voice_combo)

        
        self.speed_label = QtWidgets.QLabel("(Speed): 170")
        self.speed_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.speed_slider.setMinimum(80)
        self.speed_slider.setMaximum(450)
        self.speed_slider.setValue(170)
        self.speed_value_edit = QtWidgets.QLineEdit("170")
        self.speed_value_edit.setFixedWidth(50)

        speed_layout = QtWidgets.QHBoxLayout()
        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_value_edit)
        layout.addLayout(speed_layout)

        self.speed_slider.valueChanged.connect(self.speed_slider_changed)
        self.speed_value_edit.editingFinished.connect(self.speed_edit_changed)

        
        self.pitch_label = QtWidgets.QLabel("Pitch: 50")
        self.pitch_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.pitch_slider.setMinimum(0)
        self.pitch_slider.setMaximum(99)
        self.pitch_slider.setValue(50)
        self.pitch_value_edit = QtWidgets.QLineEdit("50")
        self.pitch_value_edit.setFixedWidth(50)

        pitch_layout = QtWidgets.QHBoxLayout()
        pitch_layout.addWidget(self.pitch_label)
        pitch_layout.addWidget(self.pitch_slider)
        pitch_layout.addWidget(self.pitch_value_edit)
        layout.addLayout(pitch_layout)

        self.pitch_slider.valueChanged.connect(self.pitch_slider_changed)
        self.pitch_value_edit.editingFinished.connect(self.pitch_edit_changed)

       
        self.volume_label = QtWidgets.QLabel("(Volume): 100")
        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(200)
        self.volume_slider.setValue(100)
        self.volume_value_edit = QtWidgets.QLineEdit("100")
        self.volume_value_edit.setFixedWidth(50)

        volume_layout = QtWidgets.QHBoxLayout()
        volume_layout.addWidget(self.volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_value_edit)
        layout.addLayout(volume_layout)

        self.volume_slider.valueChanged.connect(self.volume_slider_changed)
        self.volume_value_edit.editingFinished.connect(self.volume_edit_changed)

        
        btn_layout = QtWidgets.QHBoxLayout()
        self.speak_btn = QtWidgets.QPushButton("speak")
        self.speak_btn.clicked.connect(self.speak)
        btn_layout.addWidget(self.speak_btn)

        self.save_btn = QtWidgets.QPushButton("save")
        self.save_btn.clicked.connect(self.save_audio)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

        
        self.progress = QtWidgets.QProgressBar()
        self.progress.setValue(0)
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def speed_slider_changed(self, val):
        self.speed_label.setText(f"(Speed): {val}")
        self.speed_value_edit.setText(str(val))

    def speed_edit_changed(self):
        try:
            val = int(self.speed_value_edit.text())
        except ValueError:
            val = self.speed_slider.value()
        val = max(80, min(450, val))
        self.speed_slider.setValue(val)
        self.speed_label.setText(f"((ı show)Speed): {val}")
        self.speed_value_edit.setText(str(val))

    def pitch_slider_changed(self, val):
        self.pitch_label.setText(f"Pitch: {val}")
        self.pitch_value_edit.setText(str(val))

    def pitch_edit_changed(self):
        try:
            val = int(self.pitch_value_edit.text())
        except ValueError:
            val = self.pitch_slider.value()
        val = max(0, min(99, val))
        self.pitch_slider.setValue(val)
        self.pitch_label.setText(f"Pitch: {val}")
        self.pitch_value_edit.setText(str(val))

    def volume_slider_changed(self, val):
        self.volume_label.setText(f"(Volume): {val}")
        self.volume_value_edit.setText(str(val))

    def volume_edit_changed(self):
        try:
            val = int(self.volume_value_edit.text())
        except ValueError:
            val = self.volume_slider.value()
        val = max(0, min(200, val))
        self.volume_slider.setValue(val)
        self.volume_label.setText(f"(Volume): {val}")
        self.volume_value_edit.setText(str(val))

    def apply_settings(self):
        self.esng.voice = self.voice_combo.currentText()
        self.esng.speed = self.speed_slider.value()
        self.esng.pitch = self.pitch_slider.value()
        self.esng.volume = self.volume_slider.value()

    def speak(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            QtWidgets.QMessageBox.warning(self, "WRİTE", "write something but dont be racist :d.")
            return
        
        voice = self.voice_combo.currentText()
        speed = self.speed_slider.value()
        pitch = self.pitch_slider.value()
        volume = self.volume_slider.value()

        try:
            cmd = [
                "espeak-ng",
                "-v", voice,
                "-s", str(speed),
                "-p", str(pitch),
                "-a", str(volume),
                text
            ]
            subprocess.run(cmd, check=True)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", str(e))

    def save_audio(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            QtWidgets.QMessageBox.warning(self, "WRİTE", "write something but dont be racist :d.")
            return

        self.apply_settings()

        models_dir = os.path.join(os.getcwd(), "models")
        os.makedirs(models_dir, exist_ok=True)

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "savet", models_dir, "(*.wav)"
        )
        if not filename:
            return

        self.progress.setVisible(True)
        self.progress.setValue(0)
        QtWidgets.QApplication.processEvents()

        try:
            self.esng.save_wav(text, filename)
            self.progress.setValue(100)
            QtWidgets.QApplication.processEvents()
            QtWidgets.QMessageBox.information(self, "yay", f"its saved!:\n{filename}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", str(e))
        finally:
            self.progress.setVisible(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TTSApp()
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec_())
