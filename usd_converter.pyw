import sys
import subprocess
import os
from PySide2 import QtCore, QtWidgets

class Window_converter(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()

		self.setWindowTitle("usd converter")
		self.setFixedSize(640, 460)
		self.build_layout()

	def build_layout(self):

		lyt = QtWidgets.QVBoxLayout()
		lyt.setAlignment(QtCore.Qt.AlignTop)
		lyt.setSpacing(8)
		self.setLayout(lyt)

		group_box1 = QtWidgets.QGroupBox()
		lyt_gb1 = QtWidgets.QVBoxLayout()
		group_box1.setLayout(lyt_gb1)
		lyt.addWidget(group_box1)

		group_box2 = QtWidgets.QGroupBox()
		lyt_gb2 = QtWidgets.QVBoxLayout()
		group_box2.setLayout(lyt_gb2)
		lyt.addWidget(group_box2)

		group_box3 = QtWidgets.QGroupBox()
		lyt_gb3 = QtWidgets.QVBoxLayout()
		group_box3.setLayout(lyt_gb3)
		lyt.addWidget(group_box3)

		# Comments guides.
		folder_info = QtWidgets.QLabel(
		"Select your houdini bin folder.\n"
		"For example: "
		"C:Program Files/Side Effects Software/Houdini20.0.506/bin"
			)
		lyt_gb1.addWidget(folder_info)

		lyt_h = QtWidgets.QHBoxLayout()
		lyt_gb1.addLayout(lyt_h)
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
		lyt_gb2.addWidget(usd_info)

		# New Horizontal layout.
		lyt_v = QtWidgets.QHBoxLayout()
		lyt_gb2.addLayout(lyt_v)
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

		# Export folder info.
		exp_folder_info = QtWidgets.QLabel(
			"Select export folder.\n"
			"If you do not choose a folder, It will use "
			"same folder."
			)
		lyt_gb3.addWidget(exp_folder_info)

		# New Layout.
		lyt_h = QtWidgets.QHBoxLayout()
		lyt_gb3.addLayout(lyt_h)
		lyt_h.setAlignment(QtCore.Qt.AlignLeft)

		# Export folder.
		self.exp_folder = QtWidgets.QLineEdit()
		self.exp_folder.setReadOnly(True)
		self.exp_folder.setEnabled(False)
		self.exp_folder.setStyleSheet("border: 2px solid grey;")
		lyt_h.addWidget(self.exp_folder)

		# Export folder button.
		self.b_exp_folder = QtWidgets.QPushButton("Browse")
		self.b_exp_folder.clicked.connect(self.choose_exp_folder)
		self.b_exp_folder.setEnabled(False)
		lyt_h.addWidget(self.b_exp_folder)

		# Check use original folder.
		self.check_exp_folder = QtWidgets.QCheckBox(
			"Same folder as the original file"
			)
		self.check_exp_folder.setChecked(1)
		self.check_exp_folder.toggled.connect(self.change_exp_path)
		lyt_gb3.addWidget(self.check_exp_folder)

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
			if self.check_exp_folder.isChecked():
				usd_dir = os.path.dirname(usd_selected)
				self.exp_folder.setText(usd_dir)
		else:
			self.check_usd_file(self.usd_file.text())

	def check_usd_file(self, file):
		"""Check that it is a valid usd file."""

		extension = os.path.splitext(file)[1].lower()

		if extension == ".usd" or extension == ".usda":
			self.usd_file.setStyleSheet("border: 2px solid green;")
			if self.check_exp_folder.isChecked():
				self.exp_folder.setStyleSheet(
					"border: 2px solid green;"
					)

			return True
		else:
			self.usd_file.setStyleSheet("border: 2px solid red;")
			return False

	def choose_exp_folder(self):
		"""Choose a custom export path."""

		if self.check_exp_folder.isChecked():
			return
			
		info = "Select your custom export folder"
		
		current_exp_f = self.exp_folder.text()
		
		if not os.path.exists(current_exp_f):
			init_dir = self.folder.text()
		else:
			init_dir = current_exp_f
		
		# Get Folder.
		fpath = QtWidgets.QFileDialog.getExistingDirectory(
				self, info, current_exp_f
				)
		
		if fpath != "" and os.path.exists(fpath):
			self.exp_folder.setText(fpath)
			self.exp_folder.setStyleSheet("border: 2px solid green")
		else:
			self.exp_folder.setText(self.exp_folder.text())

	def change_exp_path(self, status):
		"""Uses the original path as save path."""

		if status:
			self.exp_folder.setEnabled(False)
			self.b_exp_folder.setEnabled(False)

			# Get folder path.
			usd = self.usd_file.text()
			usd_dir = os.path.dirname(usd)

			# Copy that folder path.
			self.exp_folder.setText(usd_dir)

			correct_usd = self.check_usd_file(usd)
			if correct_usd:
				self.exp_folder.setStyleSheet(
					"border: 2px solid green"
					)
		else:
			self.exp_folder.setEnabled(True)
			self.b_exp_folder.setEnabled(True)

	def export(self, extension):
		"""Export the new usd file."""

		# Check that everything is configured correctly.
		can_export = self.check_to_export()

		# Convert and save new file.
		if can_export:

			usdcat_exe = self.folder.text() + "/usdcat"

			file = self.usd_file.text()

			init_usd = os.path.basename(file)
			usd_name = os.path.splitext(init_usd)[0]

			if self.exp_folder == "":
				usd_dir = os.path.dirname(file)
			else:
				usd_dir = self.exp_folder.text()		

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
