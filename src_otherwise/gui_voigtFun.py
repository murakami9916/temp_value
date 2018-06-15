import sys
import os
from PyQt5.QtWidgets import *
from tkinter import *
from PyQt5.QtCore import *
import sip
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.QtGui import QIcon
import csv
import random
import subprocess
import numpy as np
import shutil

class MainWindow(QWidget):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.count = 0
		self.flag = 1

		self.btnLayout = QGridLayout()

		self.add_btn = QPushButton('add')
		self.add_btn.clicked.connect(self.add)
		self.add_btn.setFocusPolicy(Qt.NoFocus)
		self.add_btn.setToolTip('This is a add parameter textBox Button')
		self.output_btn = QPushButton('output')
		self.output_btn.setFocusPolicy(Qt.NoFocus)
		try:
			self.output_btn.clicked.connect(self.output)
		except:
			pass
		self.output_btn.setToolTip('This is a write-csv Button')
		self.remove_btn = QPushButton('remove')
		self.remove_btn.setFocusPolicy(Qt.NoFocus)
		self.remove_btn.clicked.connect(self.remove)
		self.remove_btn.setToolTip('This is a remove parameter textBox Button')
		self.plot_btn = QPushButton('review')
		self.plot_btn.setFocusPolicy(Qt.NoFocus)
		try:
			self.plot_btn.clicked.connect(self.plot)
		except:
			pass
		self.plot_btn.setToolTip('This is a plot Button')
		self.clear_btn = QPushButton('clear')
		self.clear_btn.setFocusPolicy(Qt.NoFocus)
		self.clear_btn.clicked.connect(self.clear)
		self.clear_btn.setToolTip('This is a plot Button')
		self.btnLayout.addWidget(self.clear_btn,2,1)		

		self.readme_btn = QPushButton('readme')
		self.readme_btn.setFocusPolicy(Qt.NoFocus)
		self.readme_btn.clicked.connect(self.makeWindow)
		self.readme_btn.setToolTip('This is explan Button')
		self.btnLayout.addWidget(self.readme_btn,2,0)

		self.textLayout = QHBoxLayout()

		self.layout = QVBoxLayout()
		self.btnLayout.addWidget(self.output_btn,0,0)
		self.btnLayout.addWidget(self.plot_btn,0,1)
		self.btnLayout.addWidget(self.add_btn,1,0)
		self.btnLayout.addWidget(self.remove_btn,1,1)
		self.layout.addLayout(self.btnLayout)
		#self.layout.addWidget(self.add_btn)
		#self.layout.addWidget(self.remove_btn)
		#self.layout.addWidget(self.output_btn)

		self.statusLayout = QHBoxLayout()
		self.ndataLayout = QVBoxLayout()
		self.scaleLayout = QVBoxLayout()
		self.stepLayout = QVBoxLayout()
		self.fileLayout = QVBoxLayout()
		self.statusLayout.addLayout(self.ndataLayout)
		self.statusLayout.addLayout(self.scaleLayout)
		self.statusLayout.addLayout(self.stepLayout)
		self.statusLayout.addLayout(self.fileLayout)
		self.layout.addLayout(self.statusLayout)

		ndata_label = QLabel("number")
		self.ndataLayout.addWidget(ndata_label,alignment=(Qt.AlignTop | Qt.AlignCenter))
		self.ndata = QLineEdit()
		self.ndata.setText("")
		self.ndataLayout.addWidget(self.ndata,alignment=(Qt.AlignTop | Qt.AlignCenter))

		scale_label = QLabel("scale-Facter")
		self.scaleLayout.addWidget(scale_label,alignment=(Qt.AlignTop | Qt.AlignCenter))
		self.scale = QLineEdit()
		self.scale.setText("1")
		#self.scale.setFocusPolicy(Qt.NoFocus)
		self.scaleLayout.addWidget(self.scale,alignment=(Qt.AlignTop | Qt.AlignCenter))

		step_label = QLabel("step")
		self.stepLayout.addWidget(step_label,alignment=(Qt.AlignTop | Qt.AlignCenter))
		self.step = QLineEdit()
		self.step.setText("output-only : cal F2")
		self.step.setFocusPolicy(Qt.NoFocus)
		self.step.setReadOnly(True)
		self.stepLayout.addWidget(self.step,alignment=(Qt.AlignTop | Qt.AlignCenter))

		file_label = QLabel("output name")
		self.fileLayout.addWidget(file_label,alignment=(Qt.AlignTop | Qt.AlignCenter))
		self.file = QLineEdit()
		#self.file.setFocusPolicy(Qt.NoFocus)
		self.file.setText("samplespectrum")
		self.fileLayout.addWidget(self.file,alignment=(Qt.AlignTop | Qt.AlignCenter))

		self.rangeLayout = QHBoxLayout()
		self.startLayout = QVBoxLayout()
		self.endLayout = QVBoxLayout()
		self.bgHighLayout = QVBoxLayout()
		self.bgLowLayout = QVBoxLayout()

		self.rangeLayout.addLayout(self.startLayout)
		self.rangeLayout.addLayout(self.endLayout)
		self.rangeLayout.addLayout(self.bgHighLayout)
		self.rangeLayout.addLayout(self.bgLowLayout)
		self.layout.addLayout(self.rangeLayout)

		start_label = QLabel("Start")
		self.startLayout.addWidget(start_label,alignment=(Qt.AlignTop | Qt.AlignCenter))
		self.start = QLineEdit()
		self.start.setText("")
		self.startLayout.addWidget(self.start,alignment=(Qt.AlignTop | Qt.AlignCenter))

		end_label = QLabel("End")
		self.endLayout.addWidget(end_label,alignment=(Qt.AlignTop | Qt.AlignCenter))
		self.end = QLineEdit()
		self.end.setText("")
		self.endLayout.addWidget(self.end,alignment=(Qt.AlignTop | Qt.AlignCenter))

		high_label = QLabel("BG-High")
		self.bgHighLayout.addWidget(high_label,alignment=(Qt.AlignTop | Qt.AlignCenter))
		self.high = QLineEdit()
		self.high.setText("")
		self.bgHighLayout.addWidget(self.high,alignment=(Qt.AlignTop | Qt.AlignCenter))

		low_label = QLabel("BG-Low")
		self.bgLowLayout.addWidget(low_label,alignment=(Qt.AlignTop | Qt.AlignCenter))
		self.low = QLineEdit()
		self.low.setText("")
		self.bgLowLayout.addWidget(self.low,alignment=(Qt.AlignTop | Qt.AlignCenter))


		self.muLayout = QVBoxLayout()
		self.textLayout.addLayout(self.muLayout)
		self.hLayout = QVBoxLayout()
		self.textLayout.addLayout(self.hLayout)
		self.wLayout = QVBoxLayout()
		self.textLayout.addLayout(self.wLayout)
		self.lLayout = QVBoxLayout()
		self.textLayout.addLayout(self.lLayout)

		self.layout.addLayout(self.textLayout)

		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		self.layout.addWidget(self.canvas)

		self.setGeometry(200,150,600,600)
		self.setLayout(self.layout)
		self.setWindowTitle("create psudo-Voigt Function")
		self.setWindowIcon(QIcon('icon.png'))

	def add(self):
		self.count += 1
		print(self.count)

		if(self.count==1):
			self.mu_label = QLabel("mu")
			self.muLayout.addWidget(self.mu_label,alignment=Qt.AlignCenter)
			self.mu1 = QLineEdit()
			self.mu1.setText("")
			self.muLayout.addWidget(self.mu1)

			self.h_label = QLabel("hight")
			self.hLayout.addWidget(self.h_label,alignment=Qt.AlignCenter)
			self.h1 = QLineEdit()
			self.h1.setText("")
			self.hLayout.addWidget(self.h1)

			self.w_label = QLabel("width")
			self.wLayout.addWidget(self.w_label,alignment=Qt.AlignCenter)
			self.w1 = QLineEdit()
			self.w1.setText("")
			self.wLayout.addWidget(self.w1)

			self.l_label = QLabel("L/G ratio")
			self.lLayout.addWidget(self.l_label,alignment=Qt.AlignCenter)
			self.l1 = QLineEdit()
			self.l1.setText("")
			self.lLayout.addWidget(self.l1)

		if(self.count==2):
			self.mu2 = QLineEdit()
			self.mu2.setText("")
			self.muLayout.addWidget(self.mu2)

			self.h2 = QLineEdit()
			self.h2.setText("")
			self.hLayout.addWidget(self.h2)

			self.w2 = QLineEdit()
			self.w2.setText("")
			self.wLayout.addWidget(self.w2)

			self.l2 = QLineEdit()
			self.l2.setText("")
			self.lLayout.addWidget(self.l2)

		if(self.count==3):
			self.mu3 = QLineEdit()
			self.mu3.setText("")
			self.muLayout.addWidget(self.mu3)

			self.h3 = QLineEdit()
			self.h3.setText("")
			self.hLayout.addWidget(self.h3)

			self.w3 = QLineEdit()
			self.w3.setText("")
			self.wLayout.addWidget(self.w3)

			self.l3 = QLineEdit()
			self.l3.setText("")
			self.lLayout.addWidget(self.l3)

		if(self.count==4):
			self.mu4 = QLineEdit()
			self.mu4.setText("")
			self.muLayout.addWidget(self.mu4)

			self.h4 = QLineEdit()
			self.h4.setText("")
			self.hLayout.addWidget(self.h4)

			self.w4 = QLineEdit()
			self.w4.setText("")
			self.wLayout.addWidget(self.w4)

			self.l4 = QLineEdit()
			self.l4.setText("")
			self.lLayout.addWidget(self.l4)

		if(self.count==5):
			self.mu5 = QLineEdit()
			self.mu5.setText("")
			self.muLayout.addWidget(self.mu5)

			self.h5 = QLineEdit()
			self.h5.setText("")
			self.hLayout.addWidget(self.h5)

			self.w5 = QLineEdit()
			self.w5.setText("")
			self.wLayout.addWidget(self.w5)

			self.l5 = QLineEdit()
			self.l5.setText("")
			self.lLayout.addWidget(self.l5)

		if(self.count==6):
			self.mu6 = QLineEdit()
			self.mu6.setText("")
			self.muLayout.addWidget(self.mu6)

			self.h6 = QLineEdit()
			self.h6.setText("")
			self.hLayout.addWidget(self.h6)

			self.w6 = QLineEdit()
			self.w6.setText("")
			self.wLayout.addWidget(self.w6)

			self.l6 = QLineEdit()
			self.l6.setText("")
			self.lLayout.addWidget(self.l6)

		if(self.count > 6):
			self.count -= 1
			meg = "これ以上、ピークを生成できません。\n作業を続けますか？？"
			buttonReply = QMessageBox.question(self, 'message', meg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if buttonReply == QMessageBox.Yes:
				print('Yes clicked.')
			else:
				print('No clicked.')
				sys.exit()

	def remove(self):
		if(self.count==1):
			self.muLayout.removeWidget(self.mu1)
			sip.delete(self.mu1)
			self.mu1 = None
			self.muLayout.removeWidget(self.mu_label)
			sip.delete(self.mu_label)
			self.mu_label = None

			self.hLayout.removeWidget(self.h1)
			sip.delete(self.h1)
			self.h1 = None
			self.hLayout.removeWidget(self.h_label)
			sip.delete(self.h_label)
			self.h_label = None

			self.wLayout.removeWidget(self.w1)
			sip.delete(self.w1)
			self.w1 = None
			self.wLayout.removeWidget(self.w_label)
			sip.delete(self.w_label)
			self.w_label = None

			self.lLayout.removeWidget(self.l1)
			sip.delete(self.l1)
			self.l1 = None
			self.lLayout.removeWidget(self.l_label)
			sip.delete(self.l_label)
			self.l_label = None

		if(self.count==2):
			self.muLayout.removeWidget(self.mu2)
			sip.delete(self.mu2)
			self.mu2 = None

			self.hLayout.removeWidget(self.h2)
			sip.delete(self.h2)
			self.h2 = None

			self.wLayout.removeWidget(self.w2)
			sip.delete(self.w2)
			self.w2 = None

			self.lLayout.removeWidget(self.l2)
			sip.delete(self.l2)
			self.l2 = None

		if(self.count==3):
			self.muLayout.removeWidget(self.mu3)
			sip.delete(self.mu3)
			self.mu3 = None

			self.hLayout.removeWidget(self.h3)
			sip.delete(self.h3)
			self.h3 = None

			self.wLayout.removeWidget(self.w3)
			sip.delete(self.w3)
			self.w3 = None

			self.lLayout.removeWidget(self.l3)
			sip.delete(self.l3)
			self.l3 = None

		if(self.count==4):
			self.muLayout.removeWidget(self.mu4)
			sip.delete(self.mu4)
			self.mu4 = None

			self.hLayout.removeWidget(self.h4)
			sip.delete(self.h4)
			self.h4 = None

			self.wLayout.removeWidget(self.w4)
			sip.delete(self.w4)
			self.w4 = None

			self.lLayout.removeWidget(self.l4)
			sip.delete(self.l4)
			self.l4 = None

		if(self.count==5):
			self.muLayout.removeWidget(self.mu5)
			sip.delete(self.mu5)
			self.mu5 = None

			self.hLayout.removeWidget(self.h5)
			sip.delete(self.h5)
			self.h5 = None

			self.wLayout.removeWidget(self.w5)
			sip.delete(self.w5)
			self.w5 = None

			self.lLayout.removeWidget(self.l5)
			sip.delete(self.l5)
			self.l5 = None

		if(self.count==6):
			self.muLayout.removeWidget(self.mu6)
			sip.delete(self.mu6)
			self.mu6 = None

			self.hLayout.removeWidget(self.h6)
			sip.delete(self.h6)
			self.h6 = None

			self.wLayout.removeWidget(self.w6)
			sip.delete(self.w6)
			self.w6 = None

			self.lLayout.removeWidget(self.l6)
			sip.delete(self.l6)
			self.l6 = None

		self.count -= 1
		print(self.count)
		if(self.count < 0):
			self.count = 0

	def output(self):
		if(self.ndata.text() == ""):
			pass
		else:
			if(os.path.exists("samplespectrum.csv")):
				os.remove("samplespectrum.csv")

			mu = []
			h = []
			w = []
			l = []
			if(self.count >= 1):
				mu.append(self.mu1.text())
				h.append(self.h1.text())
				w.append(self.w1.text())
				l.append(self.l1.text())

			if(self.count >= 2):
					mu.append(self.mu2.text())
					h.append(self.h2.text())
					w.append(self.w2.text())
					l.append(self.l2.text())

			if(self.count >= 3):
					mu.append(self.mu3.text())
					h.append(self.h3.text())
					w.append(self.w3.text())
					l.append(self.l3.text())

			if(self.count >= 4):
					mu.append(self.mu4.text())
					h.append(self.h4.text())
					w.append(self.w4.text())
					l.append(self.l4.text())

			if(self.count >= 5):
					mu.append(self.mu5.text())
					h.append(self.h5.text())
					w.append(self.w5.text())
					l.append(self.l5.text())

			if(self.count >= 6):
				mu.append(self.mu6.text())
				h.append(self.h6.text())
				w.append(self.w6.text())
				l.append(self.l6.text())

			if( int(self.ndata.text()) == 0 ):
				meg = "データ数の入力が 0 です。作業を続けますか？？"
				zeroReply = QMessageBox.question(self, 'message', meg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				if zeroReply == QMessageBox.Yes:
					print('Yes clicked.')
				else:
					print('No clicked.')
					sys.exit()
			else:
				self.writeCSV(mu, h, w, l)
				#process = subprocess.run(["makeNoisedSpectrum.exe","input.csv","log.txt"])
				process = subprocess.run(["makeNoisedSpectrum.exe","input.csv"])
				if(process.returncode):
					print("erorr in [subprocess]")
					sys.exit()

				if(self.flag):
					self.fileMove()
					
					meg = "人工データの生成に成功しました。\n作業を続けますか？？"
					gendata = QMessageBox.question(self, 'message', meg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
					if gendata == QMessageBox.Yes:
						print('Yes clicked.')
					else:
						print('No clicked.')
						sys.exit()

	def writeCSV(self, mu, h, w, l):
		f = open('input.csv', 'w')
		writer = csv.writer(f, lineterminator='\n')
		writer.writerow(["ndata",int(self.ndata.text())])
		writer.writerow(["xHigh",self.end.text()])
		writer.writerow(["xLow",self.start.text()])
		writer.writerow(["peakHeightScaleFactor",self.scale.text()])
		writer.writerow(["bgHigh",self.high.text()])
		writer.writerow(["bgLow",self.low.text()])
		for mut,ht,wt,lt in zip(mu,h,w,l):
			writer.writerow(["peak",ht,mut,wt,lt])
		f.close()

	def plot(self):
		self.flag = 0

		try:
			self.output()

		except ValueError:
			pass

		except:
			e_meg = "予期せぬエラーが発生しました。\n作業を続けますか？？"
			error = QMessageBox.question(self, 'message', meg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if error == QMessageBox.Yes:
				print('Yes clicked.')
			else:
				print('No clicked.')
				sys.exit()
		else:
			if(os.path.exists("samplespectrum.csv")):
				f = np.loadtxt("samplespectrum.csv", delimiter=",",skiprows=1)
				f_x = np.array(f[:,0])
				f_x = f_x[::-1]
				f_noise = np.array(f[:,1])
				f_noise = f_noise[::-1]
				f_y = np.array(f[:,2])
				f_y = f_y[::-1]
				f_bg = np.array(f[:,3])
				f_bg = f_bg[::-1]

				self.figure.clear()

				ax = self.figure.add_subplot(111)
				
				ax.plot(f_x, f_bg, c="#00FF00")
				for i in range(self.count):
					peak = np.array(f[:,i+4])
					peak = peak[::-1]
					ax.plot(f_x, peak + f_bg)
				ax.scatter(f_x,f_noise, c="#FFFFFF", linewidths=1, alpha=0.7, edgecolors="red")
				ax.set_xlim(ax.get_xlim()[::-1])

				self.canvas.draw()

		finally:
			self.flag = 1

	def clear(self):
		self.start.setText("")
		self.end.setText("")
		self.high.setText("")
		self.low.setText("")
		self.ndata.setText("")
		self.scale.setText("1")
		self.step.setText("output-only : cal F2")
		self.file.setText("samplespectrum")

		if(self.count >= 1):
			self.mu1.setText("")
			self.h1.setText("")
			self.w1.setText("")
			self.l1.setText("")

		if(self.count >= 2):
			self.mu2.setText("")
			self.h2.setText("")
			self.w2.setText("")
			self.l2.setText("")

		if(self.count >= 3):
			self.mu3.setText("")
			self.h3.setText("")
			self.w3.setText("")
			self.l3.setText("")

		if(self.count >= 4):
			self.mu4.setText("")
			self.h4.setText("")
			self.w4.setText("")
			self.l4.setText("")

		if(self.count >= 5):
			self.mu5.setText("")
			self.h5.setText("")
			self.w5.setText("")
			self.l5.setText("")

		if(self.count >= 6):
			self.mu6.setText("")
			self.h6.setText("")
			self.w6.setText("")
			self.l6.setText("")

	def voigtFunc(x, c, a, w, l):
		gauss = pow(2.0, -pow((x - c) / w, 2))
		lorentz = 1.0 / (1.0 + pow((x - c) / w, 2))
		voigt = a * ( (1-l) * gauss + l * lorentz )
		return voigt

	def fileMove(self):
		f = open('path.txt')
		path = f.read()
		f.close()
		if(self.file.text() == ""):
			self.file.setText("samplespectrum.csv")

		if(os.path.exists("samplespectrum.csv")):
			f = np.loadtxt("samplespectrum.csv", delimiter=",",skiprows=1)
			xy = np.vstack((f[:,0], f[:,1]))
			xy = xy.transpose()
			np.savetxt(str(path) + "/" + self.file.text() + ".csv", xy, fmt="%6f", delimiter=",")
			shutil.move( "samplespectrum.csv", str(path) + "/" + self.file.text() + "_all.csv" )

		if(os.path.exists("input.csv")):
			shutil.move( "input.csv", str(path) + "/input.csv" )

	def keyPressEvent(self, e):
		if(e.key() == Qt.Key_Escape):
			self.close()

		if(e.key() == Qt.Key_Shift):
			pass

		if(e.key() == Qt.Key_Shift):
			self.add()

		if(e.key() == Qt.Key_Alt):
			self.remove()

		if(e.key() == Qt.Key_F5):
			self.output()

		if(e.key() == Qt.Key_F6):
			self.plot()

		if(e.key() == Qt.Key_F2):
			if(self.end.text()=="" or self.start.text() == "" or self.ndata.text() ==""):
				pass
			else:
				if(int(self.ndata.text()) == 0):
					meg = "データ数の入力が 0 です。作業を続けますか？？"
					zeroReply = QMessageBox.question(self, 'message', meg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
					if zeroReply == QMessageBox.Yes:
						print('Yes clicked.')
					else:
						print('No clicked.')
						sys.exit()
				else:
					dis = abs( float(self.end.text()) - float(self.start.text()) )
					self.step.setText(str( dis/int(self.ndata.text())))

	def makeWindow(self):
		subWindow = SubWindow()
		subWindow.show()

class SubWindow(QWidget):
	def __init__(self, parent=None):
		self.w = QDialog(parent)
		label1 = QLabel()
		label2 = QLabel()
		label3 = QLabel()
		label4 = QLabel()
		label5 = QLabel()
		label6 = QLabel()

		readme = "<b>psudo-Voigt関数を作成するプログラム</b>"
		readme_output = "output ＞＞　入力したパラメータで人口データを生成する（疑似Voigt関数） [F5]。"
		readme_add = "add　＞＞　パラメータ入力のためのテキストボックスが出現する。 [Shift]\n　　　　 現在のコードでは最大6本のピークまで対応している。"
		readme_remove = "remove ＞＞　addにより出現させたテキストボックスの削除する。 [Alt]"
		readme_review = "review ＞＞　現入力パラメータでどのようなグラフが生成されるか描画する。 [F6]\n[Esc]で終了。\n※dict/*/path.txtを生成ファイルを出力したいフォルダのパスに書き換える。"
		writer = "作成者：村上　諒"

		label1.setText(readme)
		label2.setText(readme_output)
		label3.setText(readme_add)
		label4.setText(readme_remove)
		label5.setText(readme_review)
		label6.setText(writer)

		rLayout = QVBoxLayout()
		rLayout.addWidget(label1)
		rLayout.addWidget(label2)
		rLayout.addWidget(label3)
		rLayout.addWidget(label4)
		rLayout.addWidget(label5)
		rLayout.addWidget(label6)
		self.w.setLayout(rLayout)

	def show(self):
		self.w.exec_()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	main_window = MainWindow()

	main_window.show()
	sys.exit(app.exec_())