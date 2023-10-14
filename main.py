import os
import queue
import shutil
import signal
import docx
from PyQt5 import QtWidgets, uic
import sys
import threading
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import speech_recognition as sr
from pydub import AudioSegment
import moviepy.editor as mp
from sys import platform
from ui_gui import Ui_Lecture2Text
r = sr.Recognizer()


def split_sound(sound) -> list:
    """
    this function split the audio file to small chunk to be easier to convert audio to text
    :param sound: audio file
    :return: list of segments
    """
    segments = []
    start_time = 0
    segments_size = 40000  # 40 seconds chunks
    sound_length = len(sound)
    while start_time < sound_length:
        end_time = start_time + segments_size
        segment = sound[start_time:end_time]
        segments.append(segment)
        start_time = end_time

    return segments


def transcribe_audio(language, path) -> list:
    """
    this function translate the chunks of audio to text using google-speech-to-text
    :param path: the chunk file
    :return: the text
    """
    # use the audio file as the audio source
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        # try converting it to text
        try:
            text = r.recognize_google(audio_listened, language=language)
            return text
        except Exception as e:
            print(str(e))


def show_message(message, title) -> None:
    """
    the function show pop up message
    :param message:
    :return:None
    """
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec_()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        self.t = None
        self.output_filename = None
        # uic.loadUi('untitled.ui', self)  # Load the .ui file
        # self.show()  # Show the GUI
        self.ui = Ui_Lecture2Text()
        self.ui.setupUi(self)
        self.show()
        show_message(
            "The purpose of this application is to help student to get a text file from the lectures video,"
            "this app can take mp4/mp3 and convert it to text with an option to export to docx file.\n"
            "In case you want to convert it to different language you can use this app:\n"
            "https://github.com/Charlieissa/PDF2Voice\n"
            "Note: the conversion may have a faults and not convert 100%, check please to be sure.", "About the App")
        self.file_name = None
        self.ui.btn_browse.clicked.connect(self.browse_lecture)
        self.ui.btn_export.clicked.connect(self.export_doc)
        try:
            self.ui.btn_convert.clicked.connect(self.start_convert)
        except Exception as e:
            show_message(f"Error message : {e}\nPlease restart the app and try again!", "Error")
        self.ui.btn_show_text.clicked.connect(self.show_text)
        self.output_filename = "lecture_audio.mp3"
        self.output_txt_file = "Output.txt"
        self.delete_mp3 = QMessageBox

    def closeEvent(self, event) -> None:
        """
        This function is closing the app and stopping the sound of the speech with it.
        :param event: form event
        :return: None
        """
        reply = QMessageBox.question(self, 'Window Close',
                                     'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if platform == "linux" or platform == "linux2":
                os.kill(os.getpid(), signal.SIGTERM)
            elif platform == "win32":
                os.system("taskkill /im python.exe")
            event.accept()
        else:
            event.ignore()

    def show_text(self):
        """
        the function open the output txt that generated from the functions that convert video/audio to text
        :return:
        """
        try:
            with open("Output.txt", "r") as result:
                txt = str(result.read())
                self.ui.txt_output.setText(txt)
                self.ui.btn_export.setEnabled(True)
        except Exception:
            show_message("Text file not found, try to convert again!", "Error")

    def browse_lecture(self):
        """
        the function ask the user for lecture file (mp4/mp3)
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_filter = "Video Files (*.mp4 *.avi *.mkv *.mp3)"  # Filter for video files
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open Video/Audio File", "/home/", file_filter,
                                                        options=options)
        self.ui.txt_path.setText(self.file_name)
        if self.file_name:
            self.ui.btn_convert.setEnabled(True)

    def start_convert(self) -> None:
        """
        The function start all the operation with threading , in this way the program won't freeze
        :return: None
        """

        if not self.ui.language.currentText():
            show_message("Please select lecture language", "Error")
            return
        self.t = threading.Thread(target=self.convert_video_to_audio, name="convert_video_to_audio")
        self.t.start()
        self.ui.btn_convert.setEnabled(False)

    def convert_video_to_audio(self) -> None:
        """
        The function convert video to audio before converting audio to txt
        :return: None
        """
        if self.file_name.endswith(".mp3"):
            try:
                self.get_large_audio_transcription_on_silence()
            except Exception as e:
                raise e

        else:
            try:
                self.ui.txt_progress.setText("Converting Video To Audio...")
                video = mp.VideoFileClip(self.file_name)
                audio = video.audio
                audio.write_audiofile(self.output_filename, bitrate="128k")
                self.get_large_audio_transcription_on_silence()

            except Exception as e:
                raise e

    def get_large_audio_transcription_on_silence(self) -> None:
        """
        Splitting the large audio file into chunks
        and apply speech recognition on each of these chunks.
        and output the speech in txt file
        :return: None
        """
        self.ui.txt_progress.setText("Splitting Audio to Chunks...")
        sound = AudioSegment.from_file(self.output_filename)
        result_queue1 = queue.Queue()
        result_queue1.put(split_sound(sound))
        chunks = result_queue1.get()
        folder_name = "audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        length = len(chunks)
        # export each chunk then convert it to text and delete it
        if self.ui.language.currentText() == "English":
            lang = "en-US"
        if self.ui.language.currentText() == "Hebrew":
            lang = "iw-IL"
        else:
            lang = "ar-IL"
        self.ui.txt_progress.setText("Converting Audio to Text")
        for i, audio_chunk in enumerate(chunks, start=1):
            self.ui.txt_progress.setText(f"Converted {i} Audio of {length} Chunks")
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            try:
                text = transcribe_audio(lang, chunk_filename)
                if text:
                    whole_text += text
                os.remove(chunk_filename)
            except Exception as e:
                raise e

        # remove the folder that created for chunks
        self.ui.txt_progress.setText(f"Saved text file as {self.output_filename} in the same directory.")
        with open(self.output_txt_file, "w") as text_file:
            text_file.write(whole_text)
        shutil.rmtree(folder_name, ignore_errors=True)
        self.ui.btn_show_text.setEnabled(True)
        show_message("Done, Enjoy!", "Info")

    def export_doc(self) -> None:
        """
        the function save the generated text from pdf file to doc file
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_filter = "Word Documents (*.docx);;All Files (*)"  # Filter for Word documents
        file_name, _ = QFileDialog.getSaveFileName(self, "Save as Word Document", "converted_doc", file_filter,
                                                   options=options)
        if file_name:
            doc = docx.Document()
            doc.add_paragraph(self.txt_output.toPlainText())
            doc.save(file_name + ".docx")
            QMessageBox.information(self, "File Saved", f"Text has been saved to {file_name}", QMessageBox.Ok)


app = QtWidgets.QApplication(sys.argv)
main_window = Ui()
main_window.show()
sys.exit(app.exec_())
