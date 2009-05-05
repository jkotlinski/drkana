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

import random
import wx

class Test:
	def __init__(self, window, dictionary, correct_guesses=None, guesses=0):
		if correct_guesses is None:
			correct_guesses = {}
		self.__window = window
		self.dictionary = dictionary
		self.guesses = guesses
		self.correct_guesses = correct_guesses
		self.has_shown_answer = False

		self.last_index = None

		random.seed()

		self.ResetAnswerWindow()
		self.ShowNewQuestion()

	def __getstate__(self):
		return (self.correct_guesses, self.dictionary, self.guesses)

	def __setstate__(self,state):
		self.correct_guesses, self.dictionary, self.guesses = state

	def IsFinished(self):
		return len(self.correct_guesses) == self.dictionary.GetWordCount()

	def PickRandomUnguessedWordIndex(self):
		while True:
			index = int(random.random() * self.dictionary.GetWordCount() )
			if not self.correct_guesses.has_key(index):
				return index

	def IsOnlyOneQuestionLeft(self):
		return len(self.correct_guesses) == self.dictionary.GetWordCount() - 1

	def PickUnguessedWordIndex(self):
		while True: 
			new_index = self.PickRandomUnguessedWordIndex()
			if self.IsOnlyOneQuestionLeft() or self.last_index != new_index: 
				self.last_index = new_index
				self.current_index = new_index
				return new_index

	def ShowNewQuestion(self):
		self.ShowGuessData()
		word = self.dictionary.GetWord ( self.PickUnguessedWordIndex() )
		self.__window.SetQuestionWord(word)
		return word

	def ResetAnswerWindow(self):
		self.__window.SetAnswerWord("")

	def ShowAnswer(self):
		self.__window.SetAnswerWord(self.dictionary.GetKana(self.current_index))
		self.has_shown_answer = True

	def Check(self):
		self.ShowAnswer()

	def CheckWithWord(self, entered_word):
		self.ShowAnswer()
		correct_word = self.dictionary.GetKana(self.current_index)

		#print correct_word.encode('ascii')
		#print entered_word.encode('ascii')
		guessed_right = correct_word == entered_word

		if guessed_right:
			self.AddCorrectGuess()
			self.__window.PrintGuessedRight()
		else:
			self.AddGuess()
			self.__window.PrintGuessedWrong()
		self.InitNewGuess()

	def ShowGuessData(self):
		guesses = "Correct guesses: " + `len(self.correct_guesses)` + "/" + `self.guesses`
		if self.IsFinished():
			guesses = guesses + " Finished!"
		else:
			guesses = guesses + " (Total: " + `self.dictionary.GetWordCount()` + ")"
		self.__window.ShowGuessData(guesses)

	def InitNewGuess(self):
		if self.IsFinished():
			self.ShowGuessData()
			return
		self.ShowNewQuestion()

	def WasWrong(self):
		if self.has_shown_answer:
			self.ResetAnswerWindow()
			self.AddGuess()
			self.InitNewGuess()
			self.has_shown_answer = False

	def WasRight(self):
		if self.has_shown_answer:
			self.ResetAnswerWindow()
			self.AddCorrectGuess()
			self.InitNewGuess()
			self.has_shown_answer = False

	def AddGuess(self):
		self.guesses = self.guesses + 1

	def AddCorrectGuess(self):
		self.AddGuess()
		self.correct_guesses[self.current_index] = True

