import sys
import subprocess
import os
from PySide2 import QtCore, QtWidgets

class Window_converter(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()

		self.setWindowTitle("usd converter")
		self.setFixedSize(640, 380)
		self.build_layout()

	def build_layout(self):

		lyt = QtWidgets.QVBoxLayout()
		lyt.setAlignment(QtCore.Qt.AlignTop)
		lyt.setSpacing(8)
		self.setLayout(lyt)

		# Comments guides.
		folder_info = QtWidgets.QLabel(
		"Select your houdini bin folder.\n"
		"For example: "
		"C:Program Files/Side Effects Software/Houdini20.0.506/bin"
			)
		lyt.addWidget(folder_info)

		lyt_h = QtWidgets.QHBoxLayout()
		lyt.addLayout(lyt_h)
		lyt_h.setAlignment(QtCore.Qt.AlignLeft)

		# Houdini bin folder.
		self.folder = QtWidgets.QLineEdit(
			"C:/Program Files/Side Effects Software/"
			)
		self.folder.setReadOnly(True)
		self.folder.setStyleSheet("border: 2px solid grey;")
		lyt_h.addWidget(self.folder)

		# Button to select bin folder.
		b_find_folder = QtWidgets.QPushButton("Browse")
		b_find_folder.clicked.connect(self.select_folder)
		lyt_h.addWidget(b_find_folder)

		# Comments guides.
		usd_info = QtWidgets.QLabel(
			"Select your usd file.\n"
			"Supported formats: .usd .usda"
			)
		lyt.addWidget(usd_info)

		# New Horizontal layout.
		lyt_v = QtWidgets.QHBoxLayout()
		lyt.addLayout(lyt_v)
		lyt_v.setAlignment(QtCore.Qt.AlignLeft)
		
		# Field to select the usd file.
		self.usd_file = QtWidgets.QLineEdit()
		self.usd_file.setReadOnly(True)
		self.usd_file.setStyleSheet("border: 2px solid grey;")
		lyt_v.addWidget(self.usd_file)

		# Button to select usd file.
		b_find_usd = QtWidgets.QPushButton("Browse")
		b_find_usd.clicked.connect(self.select_usd)
		lyt_v.addWidget(b_find_usd)

		# Checkbox with extra settings.
		self.check_notification = QtWidgets.QCheckBox(
			"Notification when the process ends."
			)
		self.check_notification.setChecked(1)
		self.check_open_folder = QtWidgets.QCheckBox(
			"Open directory when process finishes."
			)
		lyt.addWidget(self.check_notification)
		lyt.addWidget(self.check_open_folder)

		# New Horizontal layout to add buttons.
		lyt_h = QtWidgets.QHBoxLayout()
		lyt_h.setAlignment(QtCore.Qt.AlignCenter)
		lyt.addLayout(lyt_h)

		# Export buttons.
		b_conv_to_usda = QtWidgets.QPushButton("Convert to .usda")
		b_conv_to_usd = QtWidgets.QPushButton("Convert to .usd")

		b_conv_to_usda.setFixedSize(115, 45)
		b_conv_to_usd.setFixedSize(115, 45)

		b_conv_to_usda.clicked.connect(lambda: self.export("usda"))
		b_conv_to_usd.clicked.connect(lambda: self.export("usd"))

		lyt_h.addWidget(b_conv_to_usda)
		lyt_h.addWidget(b_conv_to_usd)

	def select_folder(self):
		"""Open a new window to select the houdini bin folder."""

		info = "Select bin folder"
		prev_dir = self.folder.text()
		new_dir = QtWidgets.QFileDialog.getExistingDirectory(
			self, info, prev_dir
			)
		
		# Check if it is the correct bin folder.
		if new_dir != "":
			self.folder.setText(new_dir)
			self.check_bin_folder(new_dir)
		else:
			self.check_bin_folder(self.folder.text())

	def check_bin_folder(self, dir_folder):
		"""Check if it is the expected folder."""
		
		usdcat_path = os.path.join(dir_folder, "usdcat.exe")
		if os.path.exists(usdcat_path):
			self.folder.setStyleSheet("border: 2px solid green;")
			return True
		else:
			self.folder.setStyleSheet("border: 2px solid red;")
			return False

	def select_usd(self):
		"""New window for selecting usd file."""

		info = "Select usd file to convert"
		prev_file = self.usd_file.text()
		prev_dir = os.path.dirname(prev_file)
		file = QtWidgets.QFileDialog.getOpenFileName(
			self, 
			info, 
			prev_dir, 
			"USD Files (*.usd*)"
			)

		usd_selected = file[0]
		
		# Verify that the file is a valid usd file.
		if usd_selected != "":
			self.usd_file.setText(usd_selected)
			self.check_usd_file(usd_selected)
		else:
			self.check_usd_file(self.usd_file.text())

	def check_usd_file(self, file):
		"""Check that it is a valid usd file."""

		extension = os.path.splitext(file)[1].lower()

		if extension == ".usd":
			self.usd_file.setStyleSheet("border: 2px solid green;")
			return True
		elif extension == ".usda":
			self.usd_file.setStyleSheet("border: 2px solid green;")
			return True
		else:
			self.usd_file.setStyleSheet("border: 2px solid red;")
			return False

	def export(self, extension):
		"""Export the new usd file."""

		# Check that everything is configured correctly.
		can_export = self.check_to_export()

		# Convert and save new file.
		if can_export:

			usdcat_exe = self.folder.text() + "/usdcat"
			file = self.usd_file.text()

			usd_dir = os.path.dirname(file)

			init_usd = os.path.basename(file)
			usd_name = os.path.splitext(init_usd)[0]

			out_usd = f"{usd_dir}/{usd_name}.{extension}"

			subprocess.run([
				usdcat_exe,
				file,
				"--out",
				out_usd
				])

			# Open directory with new file.
			if self.check_open_folder.isChecked():
				os.startfile(os.path.dirname(file))

			if self.check_notification.isChecked():
				notification = QtWidgets.QMessageBox(self)
				notification.setText("Your file has been converted")
				notification.setWindowTitle("Process finished")
				notification.show()


	def check_to_export(self):
		"""Check valid folder and usd file."""

		correct_folder = self.check_bin_folder(self.folder.text())
		correct_usd = self.check_usd_file(self.usd_file.text())

		if correct_folder and correct_usd:
			return True
		else:
			return False


app = QtWidgets.QApplication(sys.argv)
ui = Window_converter()
ui.show()
app.exec_()
