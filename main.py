import kociemba
import tkinter as tk

moves = [
    [0, 2, 8, 6, 1, 5, 7, 3, 9, 18, 36, 45, 10, 19, 37, 46, 11, 20, 38, 47],  # U
    [9, 11, 17, 15, 10, 14, 16, 12, 2, 51, 29,20, 5, 48, 32, 23, 8, 45, 35, 26],  # R
    [18, 20, 26, 24, 19, 23, 25, 21, 6, 9, 29, 44, 7, 12, 28, 41, 8, 15, 27, 38],  # F
    [27, 29, 35, 33, 28, 32, 34, 30, 24, 15, 51, 42, 25, 16, 52, 43, 26, 17, 53, 44],  # D
    [36, 38, 44, 42, 37, 41, 43, 39, 0, 18, 27, 53, 3, 21, 30, 50, 6, 24, 33, 47],  # L
    [45, 47, 53, 51, 46, 50, 52, 48, 2, 36, 33, 17, 1, 39, 34, 14, 0, 42, 35, 11]  # B
]

ColorScheme = [
    "#EEEEEE",  # white
    "#DD0000",  # red
    "#00DD00",  # green
    "#EEEE00",  # yellow
    "#FF6014",  # orange
    "#0032FF"  # blue
]


Stickers = [  # sticker size: 50x50
    [3, 0], [4, 0], [5, 0],  # U face
    [3, 1], [4, 1], [5, 1],
    [3, 2], [4, 2], [5, 2],

    [6, 3], [7, 3], [8, 3],  # R face
    [6, 4], [7, 4], [8, 4],
    [6, 5], [7, 5], [8, 5],

    [3, 3], [4, 3], [5, 3],  # F face
    [3, 4], [4, 4], [5, 4],
    [3, 5], [4, 5], [5, 5],

    [3, 6], [4, 6], [5, 6],  # D face
    [3, 7], [4, 7], [5, 7],
    [3, 8], [4, 8], [5, 8],

    [0, 3], [1, 3], [2, 3],  # L face
    [0, 4], [1, 4], [2, 4],
    [0, 5], [1, 5], [2, 5],

    [9, 3], [10, 3], [11, 3],  # B face
    [9, 4], [10, 4], [11, 4],
    [9, 5], [10, 5], [11, 5]
]

Widgets = {
    "RESET": [55, 500],
    "MANEUVER": [100, 500],
    "APPLY": [410, 500],
    "FIND": [55, 528],
    "SOLUTION": [100, 530],
    "PREVIOUS": [480, 500],
    "CURRENT": [515, 490],
    "NEXT": [580, 500],
    "EMPTY": [4, 500],
    "HINT": [4, 528]
}

FacesIndex = "URFDLB"

SolvedString = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

State = [0] * 54

Core = [4, 13, 22, 31, 40, 49]

Root = Canvas = None

SelectedColor = 0

PatternSize = 50

PatternOffsetX = PatternOffsetY = 0

ShowFaceHints = False

Hints = []


def StringToIndex(face):
    return FacesIndex.find(face)


def IndexToString(index):
    return FacesIndex[index]


def StringToState(string):
    state = [0] * 54
    i = 0
    while i < 54:
        face = StringToIndex(string[i])
        # handle errors
        if face < 0:
            print(
                f"Error parsing string at index {i}: Incorrect color {string[i]}\n{string}\n{' ' * i}^")
            return False
        state[i] = face
        i += 1

    return state


def StateToString(state):
    string = ""
    for i in state:
        string += IndexToString(i)

    return string


def ResetState(empty=False):
    global State
    State = StringToState(SolvedString)
    if empty:
        i = 0
        while i < 54:
            if not i in Core:
                State[i] = -1
            i += 1
    draw_stickers()


def StringToDisplay(s=State):
    if type(s) is list:
        s = StateToString(s)

    {s[0]}
    out = f"\
         |*********|\n\
         |*{s[0]}**{s[1]}**{s[2]}*|\n\
         |*********|\n\
         |*{s[3]}**{s[4]}**{s[5]}*|\n\
         |*********|\n\
         |*{s[6]}**{s[7]}**{s[8]}*|\n\
*********|*********|*********|*********\n\
*{s[36]}**{s[37]}**{s[38]}*|*{s[18]}**{s[19]}**{s[20]}*|*{s[9]}**{s[10]}**{s[11]}*|*{s[45]}**{s[46]}**{s[47]}*\n\
*********|*********|*********|*********\n\
*{s[39]}**{s[40]}**{s[41]}*|*{s[21]}**{s[22]}**{s[23]}*|*{s[12]}**{s[13]}**{s[14]}*|*{s[48]}**{s[49]}**{s[50]}*\n\
*********|*********|*********|*********\n\
*{s[42]}**{s[43]}**{s[44]}*|*{s[24]}**{s[25]}**{s[26]}*|*{s[15]}**{s[16]}**{s[17]}*|*{s[51]}**{s[52]}**{s[53]}*\n\
*********|*********|*********|*********\n\
         |*{s[27]}**{s[28]}**{s[29]}*|\n\
         |*********|\n\
         |*{s[30]}**{s[31]}**{s[32]}*|\n\
         |*********|\n\
         |*{s[33]}**{s[34]}**{s[35]}*|\n\
         |*********|\n\
    "
    return out


def Display(state):
    print(StringToDisplay(state))


def GetColorCenterFace(center):
    if type(center) is str:
        center = StringToIndex(center)

    i = 0
    while i < 6:
        if State[Core[i]] == center:
            return i
        i += 1


def draw_stickers(offx=5, offy=5, gray=False):
    global PatternSize, PatternOffsetX, PatternOffsetY, ShowFaceHints, Hints
    PatternOffsetX = offx
    PatternOffsetY = offy

    ps = PatternSize

    def draw_sticker(pos):
        
        x, y = Stickers[pos]
        x *= ps
        y *= ps
        x += offx
        y += offy
        if State[pos] == -1:
            color = "#888888"
        else:
            color = ColorScheme[State[pos]]
        Canvas.create_rectangle(x, y, x+ps, y+ps, fill=color, outline="#000000", width="3")
        Canvas.pack()

    i = 0
    while i < 54:
        draw_sticker(i)
        i += 1

    if ShowFaceHints:
        i = 0
        Hints = []
        while i < 6:
            hint = tk.Label(Root, text=FacesIndex[i], bg=ColorScheme[State[Core[i]]], font=("Roboto", 25))
            x, y = Stickers[Core[i]]
            x *= PatternSize
            y *= PatternSize
            hint.place(x=x+16, y=y+10)
            Hints.append(hint)
            i += 1
    else:
        for i in Hints:
            i.destroy()
        Hints = []


def ParseMove(move):
    if type(move) is not str or len(move) == 0:
        return

    finalMove = [0, 0, False]
    char = 0

    # find face
    finalMove[0] = StringToIndex(move[0].upper())

    # find wide move
    if move[0].islower():
        finalMove[2] = True
    elif len(move) > 1:
        if move[1] == "w":
            finalMove[2] = True
            char = 1

    char += 1
    # find turn count
    if len(move) > char:
        turns = move[char]
        if turns.isnumeric():
            turns = int(turns) % 4
        elif turns == "'":
            turns = -1
        else:
            turns = 1
    else:
        turns = 1

    finalMove[1] = turns
    return finalMove


def ApplyMove(move):
    global State
    if type(move) is not list:  # parsing move if not done yet
        move = ParseMove(move)

    if move[1] < 0:  # converting negative turn count to positive equivalent
        move[1] += 4

    def swapCubies():
        d = moves[move[0]]  # data
        i = j = 0
        global State
        fState = State
        while i < 5:
            j = i * 4
            buffer = fState[d[j]]
            fState[d[j]] = fState[d[j+3]]
            fState[d[j+3]] = fState[d[j+2]]
            fState[d[j+2]] = fState[d[j+1]]
            fState[d[j+1]] = buffer
            i += 1
        State = fState

    turns = 0
    while turns < move[1]:
        swapCubies()
        turns += 1

    draw_stickers()


def ParseManeuver(maneuver):
    fManeuver = []
    for i in maneuver.split(" "):
        if i == " ":
            continue
        fManeuver.append(ParseMove(i))

    return fManeuver


def ApplyManeuver(maneuver):
    if type(maneuver) is str:
        maneuver = ParseManeuver(maneuver)
    for i in maneuver:
        if type(i) is list:
            ApplyMove(i)


WidgetFunctions = {}


def draw_widgets():
    reset = tk.Button(Root, text="RESET", command=ResetState)
    reset.place(x=Widgets["RESET"][0], y=Widgets["RESET"][1])

    maneuver = tk.Entry(Root, width=50)
    maneuver.place(x=Widgets["MANEUVER"][0], y=Widgets["MANEUVER"][1])

    def ApplyClipboard():
        ApplyManeuver(maneuver.get())
    WidgetFunctions["ApplyClipboard"] = ApplyClipboard

    apply = tk.Button(Root, text="APPLY", command=ApplyClipboard)
    apply.place(x=Widgets["APPLY"][0], y=Widgets["APPLY"][1])

    def Solve():
        try:
            sol = kociemba.solve(StateToString(State))
        except ValueError:
            sol = "INCORRECT CUBESTRING"
        solution = tk.Label(Root, text=sol, width=50)
        solution.place(x=Widgets["SOLUTION"][0], y=Widgets["SOLUTION"][1])

    WidgetFunctions["Solve"] = Solve

    find = tk.Button(Root, text="FIND", command=Solve)
    find.place(x=Widgets["FIND"][0], y=Widgets["FIND"][1])

    def ShowColor():
        x, y = Widgets["CURRENT"]
        Canvas.create_rectangle(
            x, y, x+50, y+50, fill=ColorScheme[SelectedColor], outline="#000000", width="3")
    WidgetFunctions["ShowColor"] = ShowColor

    ShowColor()

    def PrevColor():
        global SelectedColor
        SelectedColor -= 1
        if SelectedColor < 0:
            SelectedColor = 5
        ShowColor()
    WidgetFunctions["PrevColor"] = PrevColor

    def NextColor():
        global SelectedColor
        SelectedColor += 1
        if SelectedColor > 5:
            SelectedColor = 0
        ShowColor()
    WidgetFunctions["NextColor"] = NextColor

    previous = tk.Button(Root, text="<", command=PrevColor)
    previous.place(x=Widgets["PREVIOUS"][0], y=Widgets["PREVIOUS"][1])

    next = tk.Button(Root, text=">", command=NextColor)
    next.place(x=Widgets["NEXT"][0], y=Widgets["NEXT"][1])

    def Empty():
        ResetState(empty=True)

    empty = tk.Button(Root, text="EMPTY", command=Empty)
    empty.place(x=Widgets["EMPTY"][0], y=Widgets["EMPTY"][1])

    def ShowFaceHint():
        global ShowFaceHints
        ShowFaceHints = not ShowFaceHints
        draw_stickers()
    WidgetFunctions["ShowFaceHint"] = ShowFaceHint

    hint = tk.Button(Root, text="HINT", command=ShowFaceHint)
    hint.place(x=Widgets["HINT"][0], y=Widgets["HINT"][1])

def OnMouseClick(event):
    global PatternSize, PatternOffsetX, PatternOffsetY, WidgetFunctions, SelectedColor
    ps = PatternSize
    offx = PatternOffsetX
    offy = PatternOffsetY
    x = event.x
    y = event.y

    i = 0
    while i < 54:
        sx, sy = Stickers[i]
        sx = sx * ps + offx
        sy = sy * ps + offy

        if (sy < y < sy + ps) and (sx < x < sx + ps):
            if i in Core:
                SelectedColor = State[i]
                WidgetFunctions["ShowColor"]()
            else:
                State[i] = SelectedColor
            draw_stickers()

        i += 1


def main():
    global Root, Canvas, PatternSize
    print("Welcome to the Rubik's Cube python app !")

    # init window
    Root = tk.Tk()
    Root.geometry("610x600")
    Canvas = tk.Canvas(width=610, height=600)
    Canvas['bg'] = "#DADADA"
    Canvas.pack()

    # show widgets
    draw_widgets()

    # bind mouse click
    Canvas.bind("<Button-1>", OnMouseClick)

    # init cube
    ResetState()

    draw_stickers()
    return


if __name__ == "__main__":
    main()
    Root.mainloop()
