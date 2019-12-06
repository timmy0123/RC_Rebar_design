import sys,os,time
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog,QMessageBox,QWidget
import numpy.core._methods
import math
import numpy as np

Ui_Form_in,MyQtBaseclass_in = uic.loadUiType("RC_input.ui")
Ui_Form_out,MyQtBaseclass_out = uic.loadUiType("RC_output.ui")

class  MainWindow_in(QMainWindow, Ui_Form_in):
    def __init__(self):
            #QMainWindow.__init__(self)
            #Ui_Form_in.__init__(self)
            super(MainWindow_in,self).__init__()
            self.setupUi(self)
            self.fc_2.setValue(280)
            self.fy_2.setValue(4200)
            self.es_2.setValue(2.04E6)
            self.esu.setValue(0.003)
            self.b_2.setValue(30)
            self.d_2.setValue(50)
            self.d1_2.setValue(8)
            self.mu_2.setValue(50)
            self.pushactive()
            
    
    def pushactive(self):
        self.pushButton.clicked.connect(self.pushButton_ok)
        self.pushButton_3.clicked.connect(self.pushButtom_reset)
        self.pushButton_2.clicked.connect(self.close)
        
    def pushButtom_reset(self):
        self.fc_2.setValue(0)
        self.fy_2.setValue(0)
        #規定
        #self.es_2.setValue(0)
        #self.esu.setValue(0)
        self.b_2.setValue(0)
        self.d_2.setValue(0)
        self.d1_2.setValue(0)
        self.mu_2.setValue(0)


    def pushButton_ok(self):
        if self.fc_2.value() and self.fy_2.value() and self.es_2.value() and self.esu.value() \
            and self.b_2.value() and self.d_2.value() and self.d1_2.value() and self.mu_2.value():
            global fc,fy,es,eu,b,d,d1,mu
            fc,fy,es,eu,b,d,d1,mu = float(self.fc_2.value()),float(self.fy_2.value()),float(self.es_2.value()),float(self.esu.value())\
                ,float(self.b_2.value()),float(self.d_2.value()),float(self.d1_2.value()),float(self.mu_2.value())
            self.dialog=MainWindow_out(fc,fy,es,eu,b,d,d1,mu)
            self.dialog.show()
    
        else:
             QMessageBox.warning(self, 'Oops!', '有東西尚未輸入')

class  MainWindow_out(QMainWindow, Ui_Form_out):
    def __init__(self,fc,fy,es,eu,b,d,d1,mu):
            QMainWindow.__init__(self)
            Ui_Form_in.__init__(self)
            self.es=[0.004,0.005]
            self.phi=[0.815,0.9]
            self.setupUi(self)
            self.fc=fc
            self.fy=fy
            self.Es=es
            self.eu=eu
            self.b=b
            self.d=d
            self.d1=d1
            self.mu=mu
            self.beta=0.85-0.05*(fc-280)
            if self.beta<0.65:self.beta=0.65
            self.rho_min1=[14/self.fy,0.8*math.sqrt(self.fc)/self.fy]
            np.asarray(self.rho_min1)
            self.rho_max1=(100+self.fc)/(4*self.fy)
            self.pushactive()
            self.active()
    
    def pushactive(self):
        self.pushButton.clicked.connect(self.close)
    
    def active(self):
        x=3/7*self.d
        asm=(0.85*self.beta*self.b*x*self.fc)/self.fy
        mn=self.fy*asm*(self.d-self.beta*x/2)*1E-5
        self.Mn.setText(str(round(self.phi[0]*mn,5)))
        if self.mu<self.phi[0]*mn:
            self.Design_way.setText(str('single reinforced'))
            rn=self.mu*1E5/(0.9*self.b*self.d*self.d)
            m=self.fy/(0.85*self.fc)
            rho=1/m*(1-math.sqrt(1-2*rn*m/float(self.fy)))
            self.rho.setText(str(round(rho,5)))
            Asb=self.b*self.d*rho
            self.As.setText(str(round(Asb,5)))
            rho_minvalue=np.max(self.rho_min1)
            self.rho_max.setText(str(round(self.rho_max1,5)))
            self.rho_min.setText(str(round(rho_minvalue,5)))
            if rho>rho_minvalue:
                self.ok_2.setText(str('OK'))
            else:
                self.ok_2.setText(str('NG'))
            if rho<self.rho_max1:
                self.ok_1.setText(str('OK'))
            else:
                self.ok_1.setText(str('NG'))

        else:
            self.Design_way.setText(str('double reinforced'))
            x=self.eu*self.d/(self.eu+self.es[1])
            es1=self.eu*(x-self.d1)/x
            fs=self.Es*es1
            Asb1=(self.mu*1E5/self.phi[1]-0.85*self.fc*self.beta*x*self.b*(self.d-x*self.beta/2))/((fs-0.85*self.fc)*(self.d-self.d1))
            self.As1.setText(str(round(Asb1,5)))
            Asb=(0.85*self.fc*self.beta*x*self.b+(fs-0.85*self.fc)*Asb1)/self.fy
            self.As.setText(str(round(Asb,5)))
            self.As_As1.setText(str(round(Asb1+Asb,5)))
            rho=Asb/(self.b*self.d)
            self.rho.setText(str(round(rho,5)))
            rho_minvalue=np.max(self.rho_min1)
            self.rho_max.setText(str(round(self.rho_max1,5)))
            self.rho_min.setText(str(round(rho_minvalue,5)))
            if rho>rho_minvalue:
                self.ok_2.setText(str('OK'))
            else:
                self.ok_2.setText(str('NG'))
            if rho<self.rho_max1:
                self.ok_1.setText(str('OK'))
            else:
                self.ok_1.setText(str('NG'))





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow_in()
    window.show()

    sys.exit(app.exec_())
    