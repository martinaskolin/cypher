detailed = False

def char_to_index(char):
    return ord(char.upper()) - ord('A')

def index_to_char(index):
    return chr(index + ord('A'))

class rotor:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, wiring, notch):
        self.wiring = list(wiring.upper())
        self.notch = notch
        self.position = 0

    def tick(self):
        self.position = (self.position + 1) % 26
        return self.position == self.notch # Turnover
    
    def encode_forward(self, index):
        index = (index + self.position) % 26
        output = (self.wiring.index(index_to_char(index)) - self.position) % 26
        if detailed:
            print(f"{(self.alphabet*3)[len(self.alphabet) + self.position:2 * len(self.alphabet)  + self.position]}")
            print(f"{("".join(self.wiring)*3)[len(self.wiring) + self.position:2 * len(self.wiring)  + self.position]}")
            print(f"{index_to_char(index)} -> {output}")
        return output
    
    def encode_backward(self, index):
        char = self.wiring[(index + self.position) % 26]
        output = (char_to_index(char) - self.position) % 26
        if detailed:
            print(f"{("".join(self.wiring)*3)[len(self.wiring) + self.position:2 * len(self.wiring)  + self.position]}")
            print(f"{(self.alphabet*3)[len(self.alphabet) + self.position:2 * len(self.alphabet)  + self.position]}")
            print(f"{char} -> {output}")
        return output
    
class plugboard:

    def __init__(self):
        self.connections = {}

    def add_connection(self, a, b):
        self.connections[a] = b
        self.connections[b] = a
    
class reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, index):
        if detailed:
            print(f"REFLECTION: {index} -> {self.wiring.index(index_to_char(index))}")
        return self.wiring.index(index_to_char(index))
    
class enigma:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

        print("ENIGMA SETTINGS")
        print([index_to_char(rotor.position) for rotor in self.rotors])
        for key in self.plugboard.connections:
            print(f"{key} -> {self.plugboard.connections[key]}")

        print()

    def reset(self):
        for rotor in self.rotors:
            rotor.position = 0

    def press(self, char):
        if detailed:
            print(f"{char.upper()} was pressed on the keyboard with index of {char_to_index(char)}")
            print(self.rotors[0].alphabet)

        for i in range(len(self.rotors)): # Tick rotors
            turnover = self.rotors[i].tick()
            if detailed:
                print(f"rotor {i} ticked to position: {self.rotors[i].position}")
            if (not turnover):
                break

        if char in self.plugboard.connections:
            if detailed:
                print(f"PLUGBOARD: {char} -> {self.plugboard.connections[char]}")
            char = self.plugboard.connections[char]
        
        index = char_to_index(char)
        for rotor in self.rotors: # Encode forward
            index = rotor.encode_forward(index)

        index = self.reflector.reflect(index) # Reflect index

        for rotor in self.rotors[::-1]:
            index = rotor.encode_backward(index)

        char = index_to_char(index)

        if detailed:
            print(self.rotors[0].alphabet)

        if char in self.plugboard.connections:
            if detailed:
                print(f"PLUGBOARD: {char} -> {self.plugboard.connections[char]}")
            char = self.plugboard.connections[char]
            
        if detailed:
            print(char)
        return char



s1 = rotor("UWYGADFPVZBECKMTHXSLRINQOJ", 0)
s2 = rotor("AJPCZWRLFBDKOTYUQGENHXMIVS", 0)
s3 = rotor("TAGBPCSDQEUFVNZHYIXJWLRKOM", 0)

s2.position = 0
s1.position = 4
s3.position = 1

ref = reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

plug = plugboard()
plug.add_connection('A', 'B')
plug.add_connection('S', 'Z')
plug.add_connection('U', 'Y')
plug.add_connection('G', 'H')
plug.add_connection('L', 'Q')
plug.add_connection('E', 'N')

e = enigma([s2,s1,s3], ref, plug)

plain = "GYHRVFLRXY"
#plain = "QHSGUWIG"
cipher = ""

for letter in plain:
        cipher += e.press(letter)

print(f"\nCIPHER   : {plain}")
print(f"PLAINTEXT: {cipher}")