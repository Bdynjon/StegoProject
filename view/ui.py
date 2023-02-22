from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QMainWindow
from stego.stegosystem import StegoSystem
from view.stego_ui import Ui_MainWindow
import os


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButtonFileImport.clicked.connect(self.push_button_import_click)
        self.ui.pushButtonFileExport.clicked.connect(self.push_button_file_export_click)

        self.ui.pushButtonMainFileImport.triggered.connect(self.push_button_file_import_main_im_click)
        self.ui.pushButtonMainFileExport.triggered.connect(self.push_button_file_export_main_im_click)

        self.ui.pushButtonKeyImport.triggered.connect(self.push_button_import_key_click)
        self.ui.pushButtonKeyExport.triggered.connect(self.push_button_export_key_click)

        self.ui.pushButtonSettingsImport.triggered.connect(self.push_button_import_settings_click)
        self.ui.pushButtonSettingsExport.triggered.connect(self.push_button_export_settings_click)

        self.ui.spinBoxSizeUnit.valueChanged.connect(self.on_block_size_unit_text_changed)
        self.ui.spinBoxSizeBlockEmbeddingStripsTo.valueChanged.connect(self.on_size_block_embedding_changed)

        self.ui.plainTextEdit_Embedded.textChanged.connect(self.on_text_changed)

        self.ui.checkBoxRedChannel.stateChanged.connect(self.on_max_bit_change)
        self.ui.checkBoxBlueChannel.stateChanged.connect(self.on_max_bit_change)
        self.ui.checkBoxGreenChannel.stateChanged.connect(self.on_max_bit_change)

        self.ui.pushButtonEncrypt.clicked.connect(self.push_button_encrypt_click)
        self.ui.pushButtonDecrypt.clicked.connect(self.push_button_decrypt_click)

        self.ui.pushButtonDoc.triggered.connect(self.on_open_doc)

        self.stego_sys = StegoSystem()
        self.__set_params()
        self.doc_path = "data/doc/CoxJao.pdf"
        self.show()

    def on_text_changed(self):
        if len(self.ui.plainTextEdit_Embedded.toPlainText()) != 0:
            self.ui.labelCountBitText.setText(str(len(self.ui.plainTextEdit_Embedded.toPlainText()) * 8 + 15))
        else:
            self.ui.labelCountBitText.setText(str(0))

    def on_open_doc(self):
        os.system(self.doc_path)

    def on_size_block_embedding_changed(self):
        self.ui.spinBoxSizeBlockEmbeddingStripsFrom.setMaximum(self.ui.spinBoxSizeBlockEmbeddingStripsTo.value())

    def on_block_size_unit_text_changed(self):
        self.__set_params()
        self.ui.labelMaxBit.setText(str(self.stego_sys.get_count_bits()))
        max_row = self.ui.spinBoxSizeUnit.value() * 2 - 1
        self.ui.spinBoxSizeBlockEmbeddingStripsFrom.setMaximum(max_row)
        self.ui.spinBoxSizeBlockEmbeddingStripsTo.setMaximum(max_row)

    def on_max_bit_change(self):
        self.__set_params()
        self.ui.labelMaxBit.setText(str(self.stego_sys.get_count_bits()))

    def push_button_import_settings_click(self):
        path = QFileDialog.getOpenFileName(self, 'Открыть файл', '.', 'JSON files (*.json)')

        try:
            if path[0] != '':
                params = self.stego_sys.load_preset(path[0])
                self.ui.spinBoxSizeBlockLimitDifferentiation.setValue(params[0])
                self.ui.spinBoxSizeBlockEmbeddingStripsFrom.setValue(params[1][0])
                self.ui.spinBoxSizeBlockEmbeddingStripsTo.setValue(params[1][1])
                self.ui.spinBoxSizeUnit.setValue(params[2])
                self.ui.checkBoxBlueChannel.setChecked(params[3]["blue"])
                self.ui.checkBoxGreenChannel.setChecked(params[3]["green"])
                self.ui.checkBoxRedChannel.setChecked(params[3]["red"])

                max_row = params[0]*2 -1
                self.ui.spinBoxSizeBlockEmbeddingStripsFrom.setMaximum(max_row)
                self.ui.spinBoxSizeBlockEmbeddingStripsTo.setMaximum(max_row)

        except:
            self.error_box('Файл не содержит корректных данных')

    def __check_is_param_set(self):
        if not (self.ui.checkBoxBlueChannel.isChecked() or
                self.ui.checkBoxGreenChannel.isChecked() or
                self.ui.checkBoxRedChannel.isChecked()):

            self.error_box('Введите параметры')

    def __set_params(self):
        try:
            channel_dict = {
                "blue": self.ui.checkBoxBlueChannel.isChecked(),
                "green": self.ui.checkBoxGreenChannel.isChecked(),
                "red": self.ui.checkBoxRedChannel.isChecked()
            }
            self.stego_sys.set_params(self.ui.spinBoxSizeBlockLimitDifferentiation.value(),
                                      [self.ui.spinBoxSizeBlockEmbeddingStripsFrom.value(),
                                       self.ui.spinBoxSizeBlockEmbeddingStripsTo.value()],
                                      self.ui.spinBoxSizeUnit.value(),
                                      channel_dict)
        except:
            self.error_box('Введены некоректные параметры')

    def push_button_export_settings_click(self):
        self.__check_is_param_set()

        path = QFileDialog.getSaveFileName(self, 'Сохранить файл', '.', 'JSON files (*.json)')
        self.__set_params()
        if path[0] != '':
            self.stego_sys.save_preset(path[0])

    def push_button_import_key_click(self):
        path = QFileDialog.getOpenFileName(self, 'Открыть файл', '.', 'JSON files (*.json)')

        try:
            if path[0] != '':
                self.ui.lineEditKey.setText(str(self.stego_sys.load_key(path[0])))
        except:
            self.error_box('Файл не содержит корректных данных')

    def push_button_export_key_click(self):
        if self.ui.lineEditKey.text() == '':
            self.error_box('Введите ключ')
            return

        try:
            key_val = int(self.ui.lineEditKey.text())
            path = QFileDialog.getSaveFileName(self, 'Сохранить файл', '.', 'JSON files (*.json)')
            if path[0] != '':
                self.stego_sys.save_key(key_val, path[0])
        except:
            self.error_box('Ключ должен быть целым неотрицательным числом')

    def push_button_import_click(self):
        path = QFileDialog.getOpenFileName(self, 'Открыть изображение', '.', 'Image files (*.png *.jpg *.bmp)')
        if path[0] != '':
            self.stego_sys.load_im_message_insert(path[0])
            QPixmap(path[0])
            try:
                self.ui.labelEmbeddedPictureInput.setPixmap(self.convert_open_cv_image_to_q_pixmap(self.stego_sys.get_im_message_insert()))
            except Exception as ex:
                print(ex)
            self.ui.labelCountBitImage.setText(str(self.stego_sys.get_inserted_image_len()))

    def push_button_file_export_click(self):
        if self.stego_sys.get_im_message_extract() is None:
            self.error_box('Изображения для сохранения нет!')
            return

        path = QFileDialog.getSaveFileName(self, 'Сохранить файл', '.', 'Image files (*.png *.jpg *.bmp)')
        if path[0] != '':
            self.stego_sys.save_extracted_image(path[0])

    def push_button_file_import_main_im_click(self):
        path = QFileDialog.getOpenFileName(self, 'Открыть изображение', '.', 'Image files (*.png *.jpg *.bmp)')
        if path[0] != '':
            self.stego_sys.load_first_im(path[0])
            QPixmap(path[0])
            self.ui.labelMainPictureInput.setPixmap(self.convert_open_cv_image_to_q_pixmap(self.stego_sys.get_first_im()))
            self.ui.labelMaxBit.setText(str(self.stego_sys.get_count_bits()))

    def push_button_file_export_main_im_click(self):
        if self.stego_sys.get_second_im() is None:
            self.error_box('Изображения для сохранения нет!')
            return

        path = QFileDialog.getSaveFileName(self, 'Сохранить файл', '.', 'Image files (*.png *.jpg *.bmp)')
        if path[0] != '':
            self.stego_sys.save_second_im(path[0])

    def push_button_encrypt_click(self):

        if self.ui.tabText_2.isVisible():
            message = self.ui.plainTextEdit_Embedded.toPlainText()
            message_type = "string"
            if message == '':
                self.error_box('Введите сообщение')
                return
        else:
            message = None
            message_type = "image"

        try:
            self.stego_sys.set_key(int(self.ui.lineEditKey.text()))
        except:
            self.error_box('Ключ должен быть положительным целым числом')
            return

        self.__set_params()
        try:
            self.stego_sys.encode(message, message_type)
        except:
            self.error_box('Размер сообщения превышает объем контейнера')
            return

        self.ui.labelMainPictureOutput.setPixmap(self.convert_open_cv_image_to_q_pixmap(self.stego_sys.get_second_im()))
        self.success_box('Информация встроена')

    def push_button_decrypt_click(self):

        message_type = "string" if self.ui.tabText_2.isVisible() else "image"

        try:
            self.stego_sys.set_key(int(self.ui.lineEditKey.text()))
        except:
            self.error_box('Ключ должен быть положительным целым числом')
            return

        self.__check_is_param_set()
        self.__set_params()

        try:
            message = self.stego_sys.decode(message_type)
            if message:
                self.ui.plainTextEdit_Extracted.setPlainText(message)
            else:
                self.ui.labelExtractedPictureInput.setPixmap(self.convert_open_cv_image_to_q_pixmap(self.stego_sys.get_im_message_extract()))
        except:
            self.error_box('Информация не может быть извлечена ввиде изображения')
        else:
            self.success_box('Информация извлечена')

    def error_box(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Ошибка!")
        dlg.setText(message)
        dlg.exec()

    def success_box(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Успех!")
        dlg.setText(message)
        dlg.exec()

    @staticmethod
    def convert_open_cv_image_to_q_pixmap(opencv_image):
        height, width, channel = opencv_image.shape
        bytes_per_line = 3 * width
        qImg = QImage(opencv_image.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        return QPixmap(qImg)
