class EnigmaMachine():
    def __init__(self, rotor1, rotor2, rotor3, reflector, plugboard):
        self.rotor1 = rotor1
        self.rotor2 = rotor2
        self.rotor3 = rotor3
        self.reflector = reflector
        self.plugboard = plugboard

    def decode(self, message):
        returnMessage = ""
        for letter in message:
            returnMessage += self.getLetter(letter)

        return returnMessage

    def getLetter(self, inputLetter):
        # Performs the logic of the machine and then rotates the rotors
        self.rotateRotors()
        letter = self.plugboard.getOutputLetter(inputLetter)

        letter = self.rotor3.getForwardOutput(letter)
        letter = self.rotor2.getForwardOutput(letter)
        letter = self.rotor1.getForwardOutput(letter)

        letter = self.reflector.getForwardOutput(letter)

        letter = self.rotor1.getBackwardOutput(letter)
        letter = self.rotor2.getBackwardOutput(letter)
        letter = self.rotor3.getBackwardOutput(letter)

        letter = self.plugboard.getOutputLetter(letter)

        return letter

    def rotateRotors(self):
        '''Rotates rotor 1, then rotates rotar 2 if determined by rotar 1, 
        and then rotates rotar 3 if determined by rotar 2'''
        if self.rotor1.rotate():
            if self.rotor2.rotate():
                self.rotor3.rotate()

class Rotor():
    def __init__(self, rotorInfo, ringPos = 1, letterPos = "A"):
        # Rotor info of form [outputSequence, turnoverNotch]
        self.outputSequence = rotorInfo[0]
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.turnoverNotch = rotorInfo[1]

        # Set ring position
        for i in range(0,ringPos - 1):
            self.rotate()

        # Set alphabet
        for i in range(0,self.alphabet.index(letterPos)):
            self.rotateAlphabet()

    def rotateAlphabet(self):
        lastLetter = self.alphabet[-1]
        self.alphabet = lastLetter + self.alphabet[:len(self.alphabet) - 1]

    def rotate(self):
        # rotates rotor and returns True if next rotor should turn and False if it should not
        firstLetter = self.outputSequence[0]
        self.outputSequence = self.outputSequence[1:] + firstLetter

        return firstLetter == self.turnoverNotch

    def getForwardOutput(self,inputLetter):
        return self.outputSequence[self.alphabet.index(inputLetter)]

    def getBackwardOutput(self, inputLetter):
        return self.alphabet[self.outputSequence.index(inputLetter)]

class Plugboard():
    def __init__(self, plugPairs):
        # plugpairs is of form "letter1letter2 letter3letter4"
        # self.plugPairs is of form {"letter1":"letter2", "letter3":"letter4"}
        self.plugPairs = {}

        currentLetter1 = None
        for letter in plugPairs:
            if currentLetter1 and letter != " ":
                self.plugPairs[currentLetter1] = letter
                currentLetter1 = None
            elif letter != " ":
                currentLetter1 = letter

    def getOutputLetter(self,inputLetter):
        if inputLetter in self.plugPairs:
            return self.plugPairs[inputLetter]
        elif inputLetter in self.plugPairs.values():
            return list(self.plugPairs.keys())[list(self.plugPairs.values()).index(inputLetter)]
        else:
            return inputLetter

# Rotor info (Do Not Change)
I = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"]
II = ["AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"]
III = ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"]
IV = ["ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"]
V = ["VZBRGITYUPSDNHLXAWMJQOFECK", "Z"]

# Reflector info (Do Not Change)
A = ["EJMZALYXVBWFCRQUONTSPIKHGD","A"]
B = ["YRUHQSLDPXNGOKMIEBFZCWVJAT","A"]
C = ["FVPJIAOYEDRZXWGCTKUQSBNMHL","A"]




'''This is where you change the starting settings of the machine'''

# Define plugboard. These are the letters that are connected
# example: "AV BS CG" would connect A and V, B and S, and C an G
plugboard = Plugboard("AV BS CG DL FU HZ IN KM OW RX")

# Define rotors ([outputSequence, turnoverNotch], ringPos, letterPos)
rotor1 = Rotor(II, 2,"B")
rotor2 = Rotor(IV, 21,"L")
rotor3 = Rotor(V, 12,"A")

# Define reflector (just a rotor, but letters map to eachother, turnoverNotch does not matter, and startPos = 1)
reflector = Rotor(B)




# Create the machine
machine = EnigmaMachine(rotor1, rotor2, rotor3, reflector, plugboard)
print(machine.decode("GKJQJ"))
print(machine.getLetter("G"))
print(machine.getLetter("K"))
print(machine.getLetter("J"))
print(machine.getLetter("Q"))
print(machine.getLetter("J"))