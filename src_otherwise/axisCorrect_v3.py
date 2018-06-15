# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QColor
from PyQt5.QtCore import Qt,QSize, QBasicTimer
import matplotlib.pyplot as plt
import subprocess
import glob
import shutil
import numpy as np

class MyWidget(QMainWindow):
	def __init__(self):
		super().__init__()

		self.init_ui()
		self.show()

	def init_ui(self):

		self.toolBar()

		self.la = QLabel("<b>Carbon File</b>",self)
		self.la.move(70,125)

		self.cfile = QLabel("",self)
		self.cfile.move(30,150)
		self.cfile.resize(150, 200)
		self.cfile.setObjectName('c')
		self.cfile.setAlignment((Qt.AlignTop | Qt.AlignCenter))

		self.cc = 404
		self.fpath = ""
		'''
		self.top_dock = QDockWidget("Ref para")
		self.textEdit = QTextEdit()
		self.textEdit.setReadOnly(True)
		self.top_dock.setWidget(self.textEdit)
		self.addDockWidget(Qt.TopDockWidgetArea, self.top_dock)
		'''

		self.statusBar().showMessage('default ref')
		self.flagRef = 0

		self.CheckBox()

		#self.plotSpace()

		label = QLabel("Standard [eV]",self)
		label.move(260,125)
		self.edit = QLineEdit("284.6", self)
		self.edit.move(250,150)


		
		self.setWindowTitle('[CE] For correcting the energy axis')
		self.setWindowIcon(QIcon('icon/myicon.jpg'))

		self.setGeometry(240, 150, 550, 400)

	def CheckBox(self):
		self.cb1 = QCheckBox('C-C', self)
		self.cb1.move(40, 70)
		self.cb1.toggle()

		self.cb2 = QCheckBox('C=C', self)
		self.cb2.move(40, 90)

		self.cb3 = QCheckBox('C-N', self)
		self.cb3.move(120, 70)

		self.cb4 = QCheckBox('C-O', self)
		self.cb4.move(120, 90)
		self.cb4.toggle()

		self.cb5 = QCheckBox('C-Cl', self)
		self.cb5.move(200, 70)

		self.cb6 = QCheckBox('C=O', self)
		self.cb6.move(200, 90)
		self.cb6.toggle()

		self.cb7 = QCheckBox('CF2', self)
		self.cb7.move(280, 70)
		self.cb7.toggle()

		self.cb8 = QCheckBox('N-C=O', self)
		self.cb8.move(280, 90)

		self.cb9 = QCheckBox('CF3', self)
		self.cb9.move(360, 70)
		self.cb9.toggle()

		self.cb10 = QCheckBox('CO3', self)
		self.cb10.move(360, 90)

		self.cb11 = QCheckBox('C-O-C', self)
		self.cb11.move(440, 70)

		self.cb12 = QCheckBox('CHF', self)
		self.cb12.move(440, 90)


	def prepare(self):
		ref = []
		if(self.cb1.isChecked()):
			ref.append("./ref/C1C.csv")
			self.cc = 0

		if(self.cb2.isChecked()):
			ref.append("./ref/C2C.csv")

		if(self.cb3.isChecked()):
			ref.append("./ref/C1N.csv")

		if(self.cb4.isChecked()):
			ref.append("./ref/C1O.csv")

		if(self.cb5.isChecked()):
			ref.append("./ref/C1Cl.csv")

		if(self.cb6.isChecked()):
			ref.append("./ref/C2O.csv")

		if(self.cb7.isChecked()):
			ref.append("./ref/CF2.csv")

		if(self.cb8.isChecked()):
			ref.append("./ref/N1C2O.csv")

		if(self.cb9.isChecked()):
			ref.append("./ref/CF3.csv")

		if(self.cb10.isChecked()):
			ref.append("./ref/CO3.csv")

		if(self.cb11.isChecked()):
			ref.append("./ref/C1O1C.csv")

		if(self.cb12.isChecked()):
			ref.append("./ref/CHF.csv")


		
		print(ref)
		'''
		try:
			self.run(ref)
		except:
			print("error!! number of ref")
			self.msg()
		'''
		
		self.run(ref)

	def run(self, ref):
		self.count = 0
		#self.figure.clear()
		for fc in self.cpath:
			if(self.flagRef == 0):
				num = len(ref)
				print(num)

			if(self.flagRef == 1):
				ref = self.myRef
				
				num = len(ref)
				print(ref,num)

				dis = []
				for i in ref:
					para_ref = np.loadtxt(i, delimiter = ",")
					print(para_ref[1])
					dis.append( abs( float( self.edit.text() ) - para_ref[1] ) )
				print(dis) 
				dis = np.array(dis)
				self.cc = dis.argmin()

				print("[fc]" + fc)

			if(num == 0):
				sys.exit()

			elif(num == 1):
				print(ref)
				subprocess.run(["ActiveShirley_ref.exe", fc,ref[0]])
			elif(num == 2):
				print(ref)
				subprocess.run([ "ActiveShirley_ref.exe", fc,ref[0], ref[1]])
			elif(num == 3):
				print(ref)
				subprocess.run(["ActiveShirley_ref.exe", fc,ref[0], ref[1], ref[2]])
			elif(num == 4):
				print(ref)
				subprocess.run(["ActiveShirley_ref.exe", fc,ref[0], ref[1], ref[2], ref[3]])
			elif(num == 5):
				print(ref)
				subprocess.run(["ActiveShirley_ref.exe", fc,ref[0], ref[1], ref[2], ref[3], ref[4]])
			elif(num == 6):
				print(ref)
				subprocess.run(["ActiveShirley_ref.exe", fc,ref[0], ref[1], ref[2], ref[3], ref[4], ref[5]])
			elif(num == 7):
				print(ref)
				subprocess.run(["ActiveShirley_ref.exe", fc,ref[0], ref[1], ref[2], ref[3], ref[4], ref[5], ref[6]])
			else:
				sys.exit()

			print("run end")

			#name = fc.rsplit("/",1)[1]
			c_name = os.path.basename(fc)

			self.difference(c_name)
			
			c_root, c_ext = os.path.splitext(c_name)
			if not(os.path.exists("result_"+c_root)):
				os.mkdir("result_"+c_root)

			for f in glob.glob("./*.csv"):
				shutil.copy(f, "result_"+c_root)


		mk = str(self.fpath) + "/correct"
		if not( os.path.exists(mk) ):
			os.mkdir(mk)


		print("-----------------")
		for i in glob.glob(self.fpath + "/" + "*cor.csv"):
			print(i)
			t = i.rsplit("/",1)[1]
			#print(i.rsplit('\\',1)[1])
			#print(mk + "/" + t.rsplit('\\',1)[1])
			'''u = t.rsplit("\\",1)
			if(len(u) == 2):
				v = u[1]
			else:
				v = [0]'''
			v = os.path.basename(i)

			shutil.move(i, mk + "/" + v)

		as_path = mk + "/*.csv"

		print(as_path)

		self.ActiveShirley(as_path)

	'''
	def plotRes(self, index, i ,name):
		#self.figure.clear()
		num = np.sqrt( len(self.clabel) + 1 )

		self.ax = self.figure.add_subplot(np.ceil(num),np.floor(num),i+1) 

		self.ax.set_xlabel('Binding Energy [eV]')
		self.ax.set_ylabel('Intensity [a.u.]')
		self.ax.set_title(str(name))

		fn = "result_No" + str(index) + "_last_optimization.csv"
		f = np.loadtxt(fn, delimiter = ",", skiprows = 1)
		num = f.shape[1]

		for k in range(5, num, 1):
			self.ax.plot(f[:,0], f[:,k])

		self.ax.plot(f[:,0], f[:,2])
		self.ax.plot(f[:,0], f[:,2])
		self.ax.plot(f[:,0], f[:,4])
		self.ax.scatter(f[:,0], f[:,1], s=50, c="#FFFFFF", linewidths=1, alpha=0.7, edgecolors="red", label="spectrum")
		
		self.ax.set_xlim(self.ax.get_xlim()[::-1])

		self.canvas.draw()

		self.figure.savefig("result.png")
	'''
	'''
	def saveFig(self):
		saveDir = QFileDialog.getExistingDirectory(self, 'Open File')
		print(saveDir)
		if(saveDir == ""):
			pass
		else:
			shutil.copy("result.png", saveDir + "/result.png")
	'''

	def toolBar(self):
		# 画像付き　吹き出しをExitにするアクションオブジェクト作成
		exitAction = QAction(QIcon('icon/exit.png'), 'Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(qApp.quit)

		# ツールバー作成
		self.toolbar = self.addToolBar('Exit')
		self.toolbar.addAction(exitAction)


		fileAction = QAction(QIcon('icon/file.jpg'),'File', self)
		fileAction.setShortcut('Ctrl+O')
		fileAction.triggered.connect(self.open_Files)

		# ツールバー作成
		self.toolbar = self.addToolBar('File')
		self.toolbar.addAction(fileAction)


		exeAction = QAction(QIcon('icon/exe.jpg'),'exe', self)
		exeAction.setShortcut('Ctrl+E')
		exeAction.triggered.connect(self.prepare)

		# ツールバー作成
		self.toolbar = self.addToolBar('Execute')
		self.toolbar.addAction(exeAction)


		refAction = QAction(QIcon('icon/ref.png'),'Ref', self)
		refAction.setShortcut('Ctrl+R')
		refAction.triggered.connect(self.getRef)

		# ツールバー作成
		self.toolbar = self.addToolBar('Ref')
		self.toolbar.addAction(refAction)


		paraAction = QAction(QIcon('icon/para.png'),'para', self)
		paraAction.setShortcut('Ctrl+T')
		paraAction.triggered.connect(self.viewPara)

		# ツールバー作成
		self.toolbar = self.addToolBar('para')
		self.toolbar.addAction(paraAction)


		'''
		plotAction = QAction(QIcon('icon/plot.png'),'plot', self)
		plotAction.setShortcut('Ctrl+P')
		plotAction.triggered.connect(self.plotSpace)

		# ツールバー作成
		self.toolbar = self.addToolBar('plot')
		self.toolbar.addAction(plotAction)
		'''



		saveAction = QAction(QIcon('icon/save.jpg'),'save', self)
		saveAction.setShortcut('Ctrl+S')
		saveAction.triggered.connect(self.open_dir)

		# ツールバー作成
		self.toolbar = self.addToolBar('save')
		self.toolbar.addAction(saveAction)


		'''
		figureAction = QAction(QIcon('icon/figure.png'),'figure', self)
		figureAction.setShortcut('Ctrl+F')
		figureAction.triggered.connect(self.saveFig)

		# ツールバー作成
		self.toolbar = self.addToolBar('figure')
		self.toolbar.addAction(figureAction)
		'''


		changeAction = QAction(QIcon('icon/change.png'),'change', self)
		changeAction.setShortcut('Ctrl+C')
		changeAction.triggered.connect(self.modeChange)

		# ツールバー作成
		self.toolbar = self.addToolBar('change')
		self.toolbar.addAction(changeAction)


		removeAction = QAction(QIcon('icon/remove.png'),'remove', self)
		removeAction.setShortcut('Ctrl+Z')
		removeAction.triggered.connect(self.remove)

		# ツールバー作成
		self.toolbar = self.addToolBar('remove')
		self.toolbar.addAction(removeAction)

		helpAction = QAction(QIcon('icon/help.jpg'),'help', self)
		#helpAction.setShortcut('Ctrl+F')
		helpAction.triggered.connect(self.msgHelp)

		# ツールバー作成
		self.toolbar = self.addToolBar('help')
		self.toolbar.addAction(helpAction)


	def msg(self):
		reply = QMessageBox.question(self, 'Message',
			"Error!!", QMessageBox.Yes | 
			QMessageBox.No, QMessageBox.No)

		if(reply == QMessageBox.Yes):
			pass
		else:
			sys.exit()

	def msgHelp(self):
		ss = "-----------------------\n"
		s = "Exit : Ctrl + Q\nFile : Ctrl + O\nRun : Ctrl + E\nRef : Ctrl + R\nPara : Ctrl + T\nPlot : Ctrl + P\nSave : Ctrl + S\nfigure : Ctrl + F\nChange : Ctrl + C\nRemove : Ctrl + Z\n"
		msg = QMessageBox.information(self, 'help [ShortCut]',ss+s+ss)

	def open_Files(self):
		self.filename = QFileDialog.getOpenFileNames(self, 'Open File', "","*.csv")
		if(len(self.filename[0]) == 0):
			pass
		else:
			self.cpath = self.searchCarbon()
			print(self.cpath[0])
			self.fpath = self.cpath[0].rsplit("/",1)[0]

			print(self.clabel)

			s = ""
			for i in self.cpath:
				j = i.rsplit("/",1)[1]
				s = s + str(j) + "\n"

			self.cfile.setText(s)


	def remove(self):
		if(self.fpath == ""):
			pass
		else:
			'''
			print(self.fpath)
			for p in glob.glob(self.fpath + "/*cor.csv"):
				print(p)
				os.remove(p)
			'''

			path = self.fpath + "/correct"
			if(os.path.exists(path)):
				print()
				shutil.rmtree(path)

	def open_dir(self):
		sdir = QFileDialog.getExistingDirectory(self, 'Open File')
		print(dir)

		if(sdir == ""):
			pass
		else:
			for i in glob.glob("*.csv"):
				shutil.copy(i, sdir)


	def getRef(self):
		self.statusBar().showMessage('My ref')
		self.flagRef = 1
		self.myRef = []
		self.refname = QFileDialog.getOpenFileNames(self, 'Open File', "","*.csv")
		for i in self.refname[0]:
			self.myRef.append(i)

		print(self.myRef)

	'''
	def plot(self, i, name):
		#print(self.f_x, self.f_y)
		#self.figure.clear()
		num = np.sqrt( len(self.clabel) + 1 )


		self.ax = self.figure.add_subplot(np.ceil(num),np.floor(num),i) 
		self.f_x = np.array(self.f_x)
		self.f_x = np.array(self.f_x)
		x = self.f_x[::-1]
		y = self.f_y[::-1]
		
		self.ax.plot(x, y, '*-')

		self.ax.set_xlabel('Binding Energy [eV]')
		self.ax.set_ylabel('Intensity [a.u.]')
		self.ax.set_title(str(name))
		self.ax.set_xlim(self.ax.get_xlim()[::-1])
		
		self.canvas.draw()
	'''

	def modeChange(self):
		self.statusBar().showMessage('default ref')
		self.flagRef = 0

	def searchCarbon(self):
		path = []
		self.clabel = []
		c = 1
		for n in self.filename[0]:
			root, ext = os.path.splitext(n)
			f = np.loadtxt(n, delimiter = ",")
			energy = f[:,0]
			middle = (energy[0] + energy[-1]) / 2.0
			print( type(middle), middle)
			if(300 > middle and middle > 270):
				self.f_x = f[:,0]
				self.f_y = f[:,1]
				
				path.append(n)
				self.clabel.append(n.rsplit("_",1)[1])
		'''
		if(len(path) == 0):
			pass
		else:
			for i in path:
				print(c,i)
				ff = np.loadtxt(i, delimiter = ",")
				self.f_x = ff[:,0]
				self.f_y = ff[:,1]
				name = i.rsplit("/",1)[1]
				self.plot(c,name)
				c = c + 1

			self.figure.tight_layout()
		'''

		return path

	def viewPara(self):
		self.top_dock = QDockWidget("Ref para")
		self.textEdit = QTextEdit()
		self.top_dock.setWidget(self.textEdit)
		self.addDockWidget(Qt.TopDockWidgetArea, self.top_dock)
		# 第二引数はダイアログのタイトル、第三引数は表示するパス
		fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

		# fname[0]は選択したファイルのパス（ファイル名を含む）
		if fname[0]:
			# ファイル読み込み
			f = open(fname[0], 'r')

			# テキストエディタにファイル内容書き込み
			with f:
				data = f.read()
				self.textEdit.setText(data)
	'''
	def plotSpace(self):
		self.plotDock = QDockWidget ("WORK")
		self.addDockWidget (Qt.BottomDockWidgetArea, self.plotDock)


		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		#self.setCentralWidget(self.canvas)
		self.plotDock.setWidget(self.canvas)
	'''

	def difference(self, name):
		std = float( self.edit.text() )
		print(type(std), std)

		res = np.loadtxt("chi.csv", delimiter = ",")
		chi = np.array(res[:,1])
		chi_min = 1e300
		for i,x in enumerate(chi):
			if(0.0<x):
				if(chi_min>x):
					minIndex = i
					chi_min = x

		#minIndex = chi.argmin()
		fname = "parameters_No" + str(minIndex) + "_last_optimization.csv"

		#self.plotRes(minIndex, self.count, name)

		cPara = np.loadtxt(fname, delimiter = ",", skiprows = 1)
		cp = cPara[:,2]

		position = cp[self.cc]

		dis = ( position - float(self.edit.text()) )

		print(position)
		print(dis)

		self.correct(dis)

		self.count = self.count + 1
	
	def correct(self, d):

		for fp in glob.glob(self.fpath + "/*" + self.clabel[self.count]):
			print(fp)
			data = np.loadtxt(fp, delimiter = ",")
			x = np.array(data[:,0])
			x_std = []
			for i in x:
				x_std.append( i - d )
			x_std = np.array(x_std)
			y = np.array(data[:,1])

			data_cor = np.array((x_std, y))
			data_cor = data_cor.transpose()

			root, ext = os.path.splitext(fp)

			np.savetxt(root + "_cor" + ext,data_cor ,fmt="%5f",delimiter=",")

	def ActiveShirley(self, as_path):

		for i in glob.glob(as_path):
			#subprocess.run(["ActiveShirley.exe", i])
			subprocess.run(["ActiveShirley_ref.exe", i])
			
			name = os.path.basename(i)
			root, ext = os.path.splitext(name)

			md = str(self.fpath) + "/result_" + str(root)

			if(os.path.exists(md)):
				shutil.rmtree(md)

			#if not( os.path.exists(md) ):
			os.mkdir(md)

			for file in glob.glob("*.csv"):
				shutil.move(file, md)
			

if __name__=='__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet('QCheckBox:checked { color: Red }')
	app.setStyleSheet('QLabel#c {font-size: 10pt;background-color: rgba(156,167,226,0.2)}')
	#app.setStyleSheet('QLabel#filetitle {font-size: 15pt}')

	window = MyWidget()
	sys.exit(app.exec_())
	