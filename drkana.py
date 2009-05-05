"""
Copyright (c) 2009 Johan Kotlinski

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import wx
import pickle

from wx import *
from Dictionary import *
from Test import *

ID_LOAD_LESSON = 10001
ID_QUESTION_BOX = 10002
ID_ANSWER_BOX = 10003
ID_TEXTFIELD = 10004
ID_CHECK_BUTTON = 10005
ID_CORRECT_BUTTON = 10006
ID_ERROR_BUTTON = 10007
ID_CORRECT_COUNTER = 10008
ID_START_TEST = 10009
ID_SAVE_STATE = 10010
ID_LOAD_STATE = 10011

class MainWindow(wx.Frame):
	def __init__(self,parent,id,title):
		wx.Frame.__init__(self,parent,wx.ID_ANY,title,style=wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		self.Move( (200, 100) )
		self.SetClientSize( (400, 400) )
		self.CreateControls()
		self.Show(True)

		self.dictionary = None
		self.test = None
		
	def SetQuestionWord(self, word):
		self.question_box.SetLabel(word or "")

	def SetAnswerWord(self, word):
		self.answer_box.SetValue(word or "")
		self.answer_box.SetFont( self.GetVeryBigFont() )

	def CreateMenuBar(self):
		menu_bar = wx.MenuBar()
		file_menu = wx.Menu()
		file_menu.Append(ID_LOAD_LESSON, "&Load Lesson...", "")
		menu_bar.Append(file_menu, "&File")

		test_menu = wx.Menu()
		test_menu.Append(ID_START_TEST, "Start &Test", "")
		test_menu.AppendSeparator()
		test_menu.Append(ID_LOAD_STATE, "&Load State", "")
		test_menu.Append(ID_SAVE_STATE, "&Save State", "")
		menu_bar.Append(test_menu, "&Test")

		self.SetMenuBar(menu_bar)

		EVT_MENU(self, ID_LOAD_LESSON, self.OnLoadLesson)
		EVT_MENU(self, ID_START_TEST, self.OnStartTest)
		EVT_MENU(self, ID_LOAD_STATE, self.OnLoadState)
		EVT_MENU(self, ID_SAVE_STATE, self.OnSaveState)

	def GetBigFont(self):
		return wx.Font( 18, wx.SWISS, wx.NORMAL, wx.NORMAL) 

	def GetVeryBigFont(self):
		return wx.Font( 36, wx.DEFAULT, wx.NORMAL, wx.NORMAL) 

	def ShowGuessData(self, string):
		self.correct_counter.SetLabel(string)

	def AddQuestionBox(self):
		self.question_box = wx.StaticText(self, ID_QUESTION_BOX, " ", style=wx.BORDER|wx.ST_NO_AUTORESIZE)
		self.question_box.SetBackgroundColour(wx.Colour(255,255,255))
		self.question_box.SetFont( self.GetBigFont() )
		self.GetSizer().Add(self.question_box, 0, wx.GROW|wx.ALL, 5)

	def AddAnswerBox(self):
		self.answer_box = wx.TextCtrl(self, ID_ANSWER_BOX, "", style=wx.SUNKEN_BORDER|wx.TE_MULTILINE|wx.TE_RICH|wx.TE_READONLY)
		self.answer_box.SetFont( self.GetVeryBigFont() )
		self.answer_box.SetBackgroundColour(wx.Colour(255,255,255))
		self.GetSizer().Add(self.answer_box, 1, wx.GROW|wx.ALL|wx.ADJUST_MINSIZE, 5)

	def AddEntryControls(self):
		textfield_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.GetSizer().Add(textfield_sizer, 0, wx.GROW|wx.ALL, 5)
		self.textfield = wx.TextCtrl(self, ID_TEXTFIELD, style=wx.TE_PROCESS_ENTER)
		self.textfield.SetFont( self.GetBigFont() )
		EVT_TEXT_ENTER(self, ID_TEXTFIELD, self.OnTextfieldEnter)
		textfield_sizer.Add(self.textfield, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		self.check_button = wx.Button(self, ID_CHECK_BUTTON, "&Check")
		self.check_button.SetDefault()
		textfield_sizer.Add(self.check_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		EVT_BUTTON(self, ID_CHECK_BUTTON, self.OnCheckButton)

	def AddCorrectAndErrorButtons(self):
		horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.GetSizer().Add(horizontal_sizer, 0, wx.GROW|wx.ALL, 5)

		self.correct_counter = wx.StaticText(self, ID_CORRECT_COUNTER, "", style=wx.SUNKEN_BORDER|wx.ST_NO_AUTORESIZE)
		self.correct_counter.SetBackgroundColour(wx.Colour(255,255,255))
		
		horizontal_sizer.Add(self.correct_counter, 1, wx.GROW|wx.ALL|wx.ADJUST_MINSIZE, 7)
		self.correct_button = wx.Button(self, ID_CORRECT_BUTTON, unichr(0x2714))
		self.correct_button.SetBackgroundColour(wx.GREEN)
		horizontal_sizer.Add(self.correct_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		error_button = wx.Button(self, ID_ERROR_BUTTON, unichr(0x2718))
		error_button.SetBackgroundColour(wx.RED)
		horizontal_sizer.Add(error_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		EVT_BUTTON(self, ID_CORRECT_BUTTON, self.OnRightButton)
		EVT_BUTTON(self, ID_ERROR_BUTTON, self.OnWrongButton)

	def CreateControls(self):
		self.CreateMenuBar()

		vert_sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(vert_sizer)

		self.AddQuestionBox()
		self.AddAnswerBox()
		self.AddEntryControls()
		self.AddCorrectAndErrorButtons()

	def OnLoadLesson(self, event):
		file_dialog = wx.FileDialog(self, "Open Lesson", wildcard="*.txt", style=wx.OPEN|wx.CHANGE_DIR|wx.HIDE_READONLY)
		if file_dialog.ShowModal() == wx.ID_OK:
			filename = file_dialog.GetPath()
			self.dictionary = Dictionary()
			self.dictionary.PopulateFromFile(filename)
			self.OnStartTest(None)

	def ResetCheckButton(self):
		self.check_button.Enable()
		self.check_button.SetFocus()

	def OnStartTest(self, event):
		assert ( self.dictionary )
		self.ResetCheckButton()
		self.test = Test(self,self.dictionary)

	def OnRightButton(self, event):
		self.test.WasRight()
		self.ResetCheckButton()

	def OnWrongButton(self, event):
		self.test.WasWrong()
		self.ResetCheckButton()

	def OnCheckButton(self, event):
		self.test.Check()
		self.ResetCheckButton()
		self.check_button.Disable()
		self.correct_button.SetFocus()

	def OnTextfieldEnter(self, event):
		entered_word = self.textfield.GetValue()
		self.test.CheckWithWord(entered_word)

	def ClearTextField(self):
		self.textfield.SetValue("")

	def PrintGuessedRight(self):
		textctrl = self.answer_box
		textctrl.SetDefaultStyle(wx.TextAttr(wx.GREEN))
		textctrl.AppendText("\nOK!")
		self.ClearTextField()

	def PrintGuessedWrong(self):
		textctrl = self.answer_box
		textctrl.SetDefaultStyle(wx.TextAttr(wx.RED))
		textctrl.AppendText("\nWrong:(")
		self.ClearTextField()

	def OnSaveState(self, event):
		file = open ( "state", "w" )
		pickle.dump(self.test, file)
		file.close()

	def OnLoadState(self, event):
		file = open ( "state" )
		test = pickle.load(file)
		self.test = Test(self, test.dictionary, test.correct_guesses, test.guesses)
		file.close()

app = wx.PySimpleApp()
title_name = "Dr. Kana"
frame = MainWindow(None, -1, title_name)
app.MainLoop()

