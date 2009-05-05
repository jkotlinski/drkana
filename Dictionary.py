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
import codecs
import re

class Dictionary:
	def __init__(self):
		self.word = []
		self.kana = []

	def PopulateFromFile(self, filename):
		file = codecs.open ( filename, 'r', 'utf-8' )

		reading_word = True
		string = ""

		i = 0

		for line in file:
			line = re.sub("#.*","",line) #remove comments
			line = line.rstrip()
			if line == "%%":
				if reading_word:
					self.word.append(string)
				else:
					self.kana.append(string)
				reading_word = not reading_word
				string = ""
			else:
				string = string + line
				
		if not reading_word:
			self.kana.append(string)

		file.close()

	def GetWordCount(self):
		return len(self.word)

	def GetWord(self, index):
		return self.word[index]

	def GetKana(self, index):
		return self.kana[index]
