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
        self.QuestionPointer = 0
    def __parseSection__(self, text, qType ):
        #print("{} {}:{}:{}".format(qType, self.lineCount, self.currentSectionLine, text))
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
            #print("{},{}".format(self.currentSectionLine, endSection+1))
            self.currentSectionLine = 1
            self.questions.append(self.questionText)
            self.questionText = ""
    def Parse(self):
        file = open(self.filePath, 'r')
        # with open(self.filePath) as file:
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
    def getNextQuestion(self):

        if (len(self.questions) == 0):
            return ""
        else:
            currentQuestion = self.questions[self.QuestionPointer]
            self.QuestionPointer += 1
            return currentQuestion
            # return re.sub('MC:|SA:', '', currentQuestion, re.M)
    def IsAtEnd(self):
        if (self.QuestionPointer == len(self.questions)):
            return True
        else:
            return False

def main():
    subjectList = ["Biology", "Chemistry", "EarthScience", "Energy", "Math", "Physics", "SpaceScience"]
    subjectQuestionList = []
    subjectDict = {}
    AllSubjects = []
    subjects = {
        "Biology":"Life Science",
        "Chemistry":"Physical Science",
        "EarthScience":"Earth & Space Science",
        "Energy":"Energy",
        "Math":"Math",
        "Physics":"Physical Science",
        "SpaceScience":"Earth & Space Science"
    }
    currentPath = os.getcwd()
    print(currentPath)
    for subject in subjects:
        filePath = os.path.join(currentPath, subject + '.txt')
        subjectType = subjects[subject]
        if not os.path.isfile(filePath):
            print("File not found: {}".format(filePath))
        else:
            print("Processing file {}".format(filePath))
            subjectQuestions = QuestionParser(filePath, subjectType)
            subjectQuestions.Parse()
            print("Line Count: {} ; Question Count: {}; MA: {} ; SA: {}".format(subjectQuestions.lineCount, len(subjectQuestions.questions), subjectQuestions.MultipleChoiceCount, subjectQuestions.SingleAnswer))
            subjectQuestionList.append(subjectQuestions.questions)
            subjectDict[subject] = subjectQuestions
    questionCounter = 1
    outputFile = open("NsBQuestions.txt","w")

    while True:
        QuestionsPending = False
        for subject in subjectList:
            currentSubject = subjectDict[subject]
            subjectType = subjects[subject]
            questionType = ""
            currentTossUp = currentSubject.getNextQuestion()
            if (currentSubject.IsAtEnd()):
                break
            if re.match('MC:\s*', currentTossUp.strip(), re.M):
                questionType = "Multiple Choice"
            if re.match('SA:\s*', currentTossUp.strip(), re.M):
                questionType = "Single Answer"
            currentTossUp = re.sub('MC:|SA:', '', currentTossUp.strip(), re.M)
            currentQuestion = "{}): Toss Up : {} : {} : {} {}".format(questionCounter, subjectType, questionType, currentTossUp, os.linesep)
            questionCounter += 1
            #print(currentQuestion)
            outputFile.write(currentQuestion)

            questionType = ""
            currentBonus = currentSubject.getNextQuestion()
            if (currentSubject.IsAtEnd()):
                break
            if re.match('MC:\s*', currentBonus.strip()):
                questionType = "Multiple Choice"
            if re.match('SA:\s*', currentBonus.strip()):
                questionType = "Single Answer"
            currentBonus = re.sub('MC:|SA:', '', currentBonus.strip(), re.M)
            currentQuestion = "{}): Bonus : {} : {} : {} {}".format(questionCounter, subjectType, questionType, currentBonus, os.linesep)
            questionCounter += 1
            #print(currentQuestion)
            QuestionsPending = True
            outputFile.write(currentQuestion)
        if (not QuestionsPending):
            break
    outputFile.close()
if __name__ == '__main__':
    main()
