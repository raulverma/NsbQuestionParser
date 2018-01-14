import sys
import os
import re
import enum

class QuestionType(enum.Enum):
    Undeinfed = 0
    singleAnswer = 1
    MultipleChoice = 2

class QuestionParser():

    def __init__(self, filePath, subject):
        self.filePath = filePath
        self.subject = subject
        self.questions = []
        self.currentSectionLine = 0
        self.questionText = ""
        self.lineCount = 0
        self.MultipleChoiceCount = 0
        self.SingleAnswer = 0
    def __parseMultipleChoice__(self, text):
        #print("multipe choice {}:{}:{}".format(self.lineCount, self.currentSectionLine, text))
        if self.currentSectionLine >= 3 and self.currentSectionLine <= 10:
            self.questionText += (text + os.linesep)
        if self.currentSectionLine == 10 and (not (re.match('^Answer', text))):
            #print("text:{}".format(line))
            print("Error {}:{} : {}".format(self.lineCount, self.currentSectionLine, text))
        if self.currentSectionLine == 11:
            self.currentSectionLine = 1
            self.questions.append(self.questionText)
            self.questionText = ""
    def __parseSingleAnswer__(self, text):
        #print("single answer {}:{}:{}".format(self.lineCount, self.currentSectionLine, text))
        if self.currentSectionLine >= 3 and self.currentSectionLine <= 6:
            self.questionText += (text + os.linesep)
        if self.currentSectionLine == 6 and (not (re.match('^Answer', text))):
            #print("text:{}".format(text))
            print("Error {}:{} : {}".format(self.lineCount, self.currentSectionLine, text))
        if self.currentSectionLine == 7:
            self.currentSectionLine = 1
            self.questions.append(self.questionText)
            self.questionText = ""
    def __parseSection__(self, text, qType ):
        # print("{} {}:{}:{}".format(qType, self.lineCount, self.currentSectionLine, text))
        if (qType == QuestionType.MultipleChoice):
            startSection = 3
            endSection = 10
        if (qType == QuestionType.singleAnswer):
            startSection = 3
            endSection = 6
        if self.currentSectionLine >= startSection and self.currentSectionLine <= endSection:
            self.questionText += (text + os.linesep)
        if self.currentSectionLine == endSection and (not (re.match('^Answer', text, re.IGNORECASE))):
            print("text:{}".format(text))
            print("Error {}:{} : {}".format(self.lineCount, self.currentSectionLine, text))
        if self.currentSectionLine == (endSection + 1):
            # print("{},{}".format(self.currentSectionLine, endSection+1))
            self.currentSectionLine = 1
            self.questions.append(self.questionText)
            self.questionText = ""

    def Parse(self):
        with open(self.filePath) as file:
            self.lineCount = 0
            self.currentSectionLine = 0
            qType = QuestionType.MultipleChoice # Assuming first question is a multiple choice question instead of undefined
            for line in file:
                self.lineCount += 1
                self.currentSectionLine += 1
                if re.match('MC:\s*', line):
                    qType = QuestionType.MultipleChoice
                    self.MultipleChoiceCount += 1
                if re.match('SA:\s*', line):
                    qType = QuestionType.singleAnswer
                    self.SingleAnswer += 1
                self.__parseSection__(line, qType)

def main():
    subjects = {
        "Biology":"Life Science",
        "Chemistry":"Physical Science",
        "EarthScience":"Earth & Space Science",
        "Energy":"Energy",
        "Math":"Math",
        "Physics":"Physical Science",
        "SpaceScience":"Earth & Space Science"
    }
    print(subjects)
    #print(len(sys.argv))
    #print(sys.argv[0])
    currentPath = os.getcwd()
    filePath = os.path.join(currentPath, 'Biology.txt')
    print(filePath)
    #filePath = r"C:\Users\raulv\OneDrive\SundayPractice\12312017\Biology.txt"
    if len(sys.argv) >= 2:
        filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found: {} using default".format(filePath))

    Biology = QuestionParser(filePath, "Life Science")
    Biology.Parse()

    filePath = os.path.join(currentPath, 'Chemistry.txt')
    print(filePath)

    Chemistry = QuestionParser(filePath, "Physical Science")
    Chemistry.Parse()

    filePath = os.path.join(currentPath, 'Energy.txt')
    print(filePath)

    Energy = QuestionParser(filePath, "Energy")
    Energy.Parse()

if __name__ == '__main__':
    main()
