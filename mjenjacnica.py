# -*- coding: cp1250 -*-

#povlacenje libraryja

import wx
import wx.xrc
from time import gmtime
import urllib2
from Moj_modul import *
import subprocess
import os
from datetime import datetime
import shutil


#provjeravanje da li postoji lokalni file u koji sprema svaki rezultat, ako ga nema kreira ga

PATH='./povijest.txt'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    pass
else:
    Dato = 'povijest.txt'
    fh = open (Dato, 'a')
    fh.write('%-15s %-15s %-15s %-15s %1s %30s\n' % ('Unos:','Valuta:','Izlaz:','Valuta:','Datum i vrijeme računa:','Datum tečajne liste:'))
    fh.close()

class GlavniFrame ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'Mjenjačnica v1.7', pos = wx.DefaultPosition, size = wx.Size( 650,550 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        Dat = 'TL.txt'
        G, M, D = gmtime()[:3];  G %= 100
        dat     = "%2d%02d%02d" % (D, M, G)
        TL = urllib2.urlopen('https://www.hnb.hr/hnb-tecajna-lista-portlet/rest/tecajn/getformatedrecords.dat');tl = TL.read()
        dat = open (Dat, 'w')
        tl = tl.replace ('\r', '')
        dat.write(tl +'\n')
        dat.close()
        dat = open (Dat, 'r')
        datum = dat.readline()[11:19]
        tl = dat.read()
        tl = tl.replace (',', '.')
        TL0 =  ['000HRK001       1.000000       1.000000       1.000000']
        TL0 += tl.split ('\n')
        TL0.pop()
        self.TL = []
        for x in TL0 : x = x[3:6] +' ' +x[:3] +' ' +x[6:]; self.TL.append (x.split())

        image_file = 'pozadina.jpg'
        bmp1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap1 = wx.StaticBitmap(self, -1, bmp1, (0, 0))
        
        self.m_staticText1 = wx.StaticText( self.bitmap1, wx.ID_ANY, u"Dan:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.m_textCtrl4 = wx.TextCtrl( self.bitmap1, wx.ID_ANY, '08', wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_textCtrl4, 0, wx.ALL, 5 )

        self.m_staticText1 = wx.StaticText( self.bitmap1, wx.ID_ANY, u"Mjesec:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.m_textCtrl5 = wx.TextCtrl( self.bitmap1, wx.ID_ANY, '06', wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_textCtrl5, 0, wx.ALL, 5 )

        self.m_staticText1 = wx.StaticText( self.bitmap1, wx.ID_ANY, u"Godina:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.m_textCtrl6 = wx.TextCtrl( self.bitmap1, wx.ID_ANY, '16', wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_textCtrl6, 0, wx.ALL, 5 )

        self.dan = str(self.m_textCtrl4.GetValue())
        self.mjesec = str(self.m_textCtrl5.GetValue())
        self.godina = str(self.m_textCtrl6.GetValue())

        self.m_staticText1 = wx.StaticText( self.bitmap1, wx.ID_ANY, u"Iznos:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_textCtrl1 = wx.TextCtrl( self.bitmap1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_textCtrl1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        m_choice1Choices = [ u"HRK", u"AUD", u"CAD", u"CZK", u"DKK", u"HUF", u"JPY", u"NOK", u"SEK", u"CHF", u"GBP", u"USD", u"EUR", u"PLN" ]
        self.m_choice1 = wx.Choice( self.bitmap1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
        self.m_choice1.SetSelection( 0 )
        bSizer1.Add( self.m_choice1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticText2 = wx.StaticText( self.bitmap1, wx.ID_ANY, u"Promjena u valutu:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        m_choice11Choices = [ u"HRK", u"AUD", u"CAD", u"CZK", u"DKK", u"HUF", u"JPY", u"NOK", u"SEK", u"CHF", u"GBP", u"USD", u"EUR", u"PLN" ]
        self.m_choice11 = wx.Choice( self.bitmap1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice11Choices, 0 )
        self.m_choice11.SetSelection( 0 )
        bSizer1.Add( self.m_choice11, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_button1 = wx.Button( self.bitmap1, wx.ID_ANY, u"Učitaj novu listu", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_button1, 0, wx.ALL, 5 )

        self.m_button2 = wx.Button( self.bitmap1, wx.ID_ANY, u"Izračunaj", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_button2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.svi_racuni = wx.Button( self.bitmap1, wx.ID_ANY, u"Svi računi (tekst)", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.svi_racuni, 0, wx.ALL, 5 )

        self.svi_racuni_xls = wx.Button( self.bitmap1, wx.ID_ANY, u"Svi računi (excel)", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.svi_racuni_xls, 0, wx.ALL, 5 )

        self.SetSizer( bSizer1 )
        self.Layout()
        self.Centre( wx.BOTH )
        # eventi
        self.m_button1.Bind( wx.EVT_BUTTON, self.f_nova_lista )
        self.m_button2.Bind( wx.EVT_BUTTON, self.f_izracunaj )
        self.svi_racuni.Bind( wx.EVT_BUTTON, self.f_svi_racuni )
        self.svi_racuni_xls.Bind( wx.EVT_BUTTON, self.f_svi_racuni_xls )
    def __del__( self ):
        pass
    # FUNGCIJE EVENATA
    def f_nova_lista( self, event ):
        Dat = 'TL.txt'
        G, M, D = gmtime()[:3];  G %= 100
        dat     = "%2d%02d%02d" % (D, M, G)

        self.dan = str(self.m_textCtrl4.GetValue())
        self.mjesec = str(self.m_textCtrl5.GetValue())
        self.godina = str(self.m_textCtrl6.GetValue())

        TL = urllib2.urlopen('http://www.hnb.hr/tecajn/f' +str(self.dan) +str(self.mjesec) +str(self.godina) +'.dat');tl = TL.read()
        dat = open (Dat, 'w')
        tl = tl.replace ('\r', '')
        dat.write(tl +'\n')
        dat.close()
        dat = open (Dat, 'r')
        datum = dat.readline()[11:19]
        tl = dat.read()
        tl = tl.replace (',', '.')
        TL0 =  ['000HRK001       1.000000       1.000000       1.000000']
        TL0 += tl.split ('\n')
        TL0.pop()
        self.TL = []
        for x in TL0 : x = x[3:6] +' ' +x[:3] +' ' +x[6:]; self.TL.append (x.split())

        dlg = wx.MessageDialog(None, 'Nova lista preuzeta.', 'info', wx.OK)
        dlg.ShowModal()
        dat.close()
        #TRAZI NEZELJENE VALUTE I BRISE IH IZ LISTE
        lose_rijeci = ['960XDR001', '703SKK001', '705SIT100']
        with open('TL.txt') as starifile, open('novifile.txt', 'w') as novifile:
            for line in starifile:
                if not any(bad_word in line for bad_word in lose_rijeci):
                    novifile.write(line)
        open('TL.txt', 'w').close()
        f = open('novifile.txt')
        f1 = open('TL.txt', 'a')
        for line in f.readlines():
            f1.write(line)
        f1.close()
        f.close()
        dat = open (Dat, 'r')
        tl = dat.read()
        tl = tl.replace (',', '.')
        TL0 =  ['000HRK001       1.000000       1.000000       1.000000']
        TL0 += tl.split ('\n')
        TL0.pop()

        self.TL = []
        for x in TL0 : x = x[3:6] +' ' +x[:3] +' ' +x[6:]; self.TL.append (x.split())
        del self.TL[1]
                
    def f_izracunaj( self, event ):
        self.iz = self.m_choice1.GetSelection()
        self.u = self.m_choice11.GetSelection()
        self.izn = int(self.m_textCtrl1.GetValue())
        I = self.TL[self.iz]
        J = self.TL[self.u]
        self.rjesenje = self.izn, I[0], "=", round(self.izn *1.0/int (I[2]) *eval (I[3] +'/'+J[5]), 2), J[0]
        rjesenje2 = ' '.join((str(self.izn), str(I[0]), "=", str(round(self.izn *1.0/int (I[2]) *eval (I[3] +'/'+J[5]), 2)), str(J[0])))

        dlg = wx.MessageDialog(None, str(rjesenje2), 'info', wx.OK)

        Dato = 'povijest.txt'
        fh = open (Dato, 'a')
        a1,a2,a3,a4,b1,b2,b3,b4=str(datetime.now()),str(self.dan+'.'),str(self.mjesec+'.'),str(self.godina+'.'),str(self.izn),str(I[0]),str(round(self.izn *1.0/int (I[2]) *eval (I[3] +'/'+J[5]), 2)),str(J[0])
        fh.write('%-15s %-15s %-15s %-15s %1s %10s %s %s\n' % (b1,b2,b3,b4,a1,a2,a3,a4))
        fh.close()

        dlg.ShowModal()
    def f_svi_racuni( self, event ):
        os.startfile("povijest.txt")
    def f_svi_racuni_xls( self, event):
        PUT='./povijest-tablica.txt'
        PUT2='./povijest-tablica.csv'
        if os.path.isfile(PUT) and os.access(PUT, os.R_OK):
            os.remove('povijest-tablica.txt')
        else:
            pass
        if os.path.isfile(PUT2) and os.access(PUT2, os.R_OK):
            os.remove('povijest-tablica.csv')
        else:
            pass
        shutil.copy2('povijest.txt', 'povijest-tablica.txt')
        os.rename("povijest-tablica.txt", "povijest-tablica.csv")
        os.startfile("povijest-tablica.csv")
                    
app = wx.App()
frame = GlavniFrame(None).Show()
app.MainLoop()
        

