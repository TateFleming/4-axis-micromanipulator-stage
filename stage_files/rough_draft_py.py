from tkinter import *
from pyfirmata import ArduinoMega, util
from time import sleep


b = ArduinoMega('COM7')

it = util.Iterator(b)
it.start()

stp_1 = b.digital[22]
dir_1 = b.digital[23]
MS1_1 = b.digital[24]
MS2_1 = b.digital[25]
MS3_1 = b.digital[26]
EN_1 = b.digital[27]
stp_2 = b.digital[30]
dir_2 = b.digital[31]
MS1_2 = b.digital[32]
MS2_2 = b.digital[33]
MS3_2 = b.digital[34]
EN_2 = b.digital[35]
stp_3 = b.digital[38]
dir_3 = b.digital[39]
MS1_3 = b.digital[40]
MS2_3 = b.digital[41]
MS3_3 = b.digital[42]
EN_3 = b.digital[43]
stp_4 = b.digital[46]
dir_4 = b.digital[47]
MS1_4 = b.digital[48]
MS2_4 = b.digital[49]
MS3_4 = b.digital[50]
EN_4 = b.digital[51]

thing = None
root = Tk()
root.title("Motor Control")
root.geometry("600x500")
root.resizable(0, 0)
vert_pos = 5000
hor_pos = 5000
foc_pos = 5000
stage_pos = 5000
rate = 100
limit = 10000


def main():
    resetPins(5)
    stp_1.write(0)
    dir_1.write(0)
    MS1_1.write(0)
    MS2_1.write(0)
    MS3_1.write(0)
    EN_1.write(1)
    sleep(2)


def start_motorfwd(event):
    global rate
    dir_1.write(0)  # Pull direction pin low to move "forward"
    EN_1.write(0)
    rate = 101 - speed.get() #rate = 1001 - speed.get()
    sleep(0.1)
    direction = "forward"
    print("starting motor %s..." % direction)
    move(direction)


def stop_motorfwd(event):
    resetPins(1)
    direction = "forward"
    global thing
    root.after_cancel(thing)
    print("Stopping motor %s..." % direction)


def start_motorrev(event):
    global rate
    dir_1.write(1)  # Pull direction pin low to move "forward"
    EN_1.write(0)
    rate = 101 - speed.get() #rate = 1001 - speed.get()
    sleep(0.1)
    direction = "reverse"
    print("starting motor %s..." % direction)
    move(direction)


def stop_motorrev(event):
    resetPins(1)
    direction = "reverse"
    global thing
    root.after_cancel(thing)
    print("Stopping motor %s..." % direction)


def start_motorup(event):
    global rate
    dir_2.write(0)  # Pull direction pin low to move "forward"
    EN_2.write(0)
    rate = 101 - speed.get() #rate = 1001 - speed.get()
    sleep(0.1)
    direction = "up"
    print("starting motor %s..." % direction)
    move(direction)


def stop_motorup(event):
    resetPins(2)
    direction = "up"
    global thing
    root.after_cancel(thing)
    print("Stopping motor %s..." % direction)


def start_motordown(event):
    global rate
    dir_2.write(1)  # Pull direction pin low to move "forward"
    EN_2.write(0)
    rate = 101 - speed.get() #rate = 1001 - speed.get()
    sleep(0.1)
    direction = "down"
    print("starting motor %s..." % direction)
    move(direction)


def stop_motordown(event):
    resetPins(2)
    direction = "down"
    global thing
    root.after_cancel(thing)
    print("Stopping motor %s..." % direction)


def start_stage_motorup(event):
    global rate
    dir_3.write(0)  # Pull direction pin low to move "forward"
    EN_3.write(0)
    rate = 101 - speed.get() #rate = 1001 - speed.get()
    sleep(0.1)
    direction = "stage up"
    print("starting motor %s..." % direction)
    move(direction)


def stop_stage_motorup(event):
    resetPins(3)
    direction = "stage up"
    global thing
    root.after_cancel(thing)
    print("Stopping motor %s..." % direction)


def start_stage_motordown(event):
    global rate
    dir_3.write(1)  # Pull direction pin low to move "forward"
    EN_3.write(0)
    rate = 101 - speed.get() #rate = 1001 - speed.get()
    sleep(0.1)
    direction = "stage down"
    print("starting motor %s..." % direction)
    move(direction)


def stop_stage_motordown(event):
    resetPins(3)
    direction = "stage down"
    global thing
    root.after_cancel(thing)
    print("Stopping motor %s..." % direction)


def start_focus_motorup(event):
    global rate
    dir_4.write(0)  # Pull direction pin low to move "forward"
    EN_4.write(0)
    rate = 101 - speed.get() #rate = 1001 - speed.get()
    sleep(0.1)
    direction = "focus up"
    print("starting motor %s..." % direction)
    move(direction)


def stop_focus_motorup(event):
    resetPins(4)
    direction = "focus up"
    global thing
    root.after_cancel(thing)
    print("Stopping motor %s..." % direction)


def start_focus_motordown(event):
    global rate
    dir_4.write(1)  # Pull direction pin low to move "forward"
    EN_4.write(0)
    rate = 101 - speed.get() #rate = 1001 - speed.get()
    sleep(0.1)
    direction = "focus down"
    print("starting motor %s..." % direction)
    move(direction)


def stop_focus_motordown(event):
    resetPins(4)
    direction = "focus down"
    global thing
    root.after_cancel(thing)
    print("Stopping motor %s..." % direction)


def move(direction):
    global thing, vert_pos, hor_pos, stage_pos, foc_pos, rate, limit
    if direction == "forward":
        if hor_pos >= limit:
            print("Horizontal edge reached at %d...Stopping." % hor_pos)
            safe_stop()
        else:
            stp_1.write(1)
            sleep(0.001) #sleep(rate/100000)
            stp_1.write(0)
            print("forward %d" % hor_pos)
            hor_pos += 1
    elif direction == "reverse":
        if hor_pos <= 0:
            print("Horizontal edge reached at %d...Stopping." % hor_pos)
            safe_stop()
        else:
            stp_1.write(1)
            sleep(rate/100000)
            stp_1.write(0)
            print("reverse %d" % hor_pos)
            hor_pos -= 1
    elif direction == "up":
        if vert_pos >= limit:
            print("Horizontal edge reached at %d...Stopping." % vert_pos)
            safe_stop()
        else:
            stp_2.write(1)
            sleep(rate/100000)
            stp_2.write(0)
            print("up")
            vert_pos += 1
    elif direction == "down":
        if vert_pos <= 0:
            print("Horizontal edge reached at %d...Stopping." % vert_pos)
            safe_stop()
        else:
            stp_2.write(1)
            sleep(rate/100000)
            stp_2.write(0)
            print("down")
            vert_pos -= 1
    elif direction == "stage up":
        if stage_pos >= limit:
            print("Horizontal edge reached at %d...Stopping." % stage_pos)
            safe_stop()
        else:
            stp_3.write(1)
            sleep(rate/100000)
            stp_3.write(0)
            print("stage up")
            stage_pos += 1
    elif direction == "stage down":
        if stage_pos <= 0:
            print("Horizontal edge reached at %d...Stopping." % stage_pos)
            safe_stop()
        else:
            stp_3.write(1)
            sleep(rate/100000)
            stp_3.write(0)
            print("stage down")
            stage_pos -= 1
    elif direction == "focus up":
        if foc_pos >= limit:
            print("Horizontal edge reached at %d...Stopping." % foc_pos)
            safe_stop()
        else:
            stp_4.write(1)
            sleep(rate/100000)
            stp_4.write(0)
            print("focus up")
            foc_pos += 1
    elif direction == "focus down":
        if foc_pos <= 0:
            print("Horizontal edge reached at %d...Stopping." % foc_pos)
            safe_stop()
        else:
            stp_4.write(1)
            sleep(rate/100000)
            stp_4.write(0)
            print("focus down")
            foc_pos -= 1
    else:
        print("error")
        safe_stop()
    #int(rate)
    thing = root.after(1, move, direction)


def safe_stop():
    global thing
    root.after_cancel(thing)
    print("Invalid direction...invoking safe stop.")


def resetPins(num):
    if num == 1 or num == 5:
        stp_1.write(0)
        dir_1.write(0)
        MS1_1.write(0)
        MS2_1.write(0)
        MS3_1.write(0)
        EN_1.write(1)

    if num == 2 or num == 5:
        stp_2.write(0)
        dir_2.write(0)
        MS1_2.write(0)
        MS2_2.write(0)
        MS3_2.write(0)
        EN_2.write(1)

    if num == 3 or num == 5:
        stp_3.write(0)
        dir_3.write(0)
        MS1_3.write(0)
        MS2_3.write(0)
        MS3_3.write(0)
        EN_3.write(1)

    if num == 4 or num == 5:
        stp_4.write(0)
        dir_4.write(0)
        MS1_4.write(0)
        MS2_4.write(0)
        MS3_4.write(0)
        EN_4.write(1)


def return_home(event):
    global hor_pos, vert_pos, stage_pos, foc_pos
    if hor_pos - 5000 != 0:
        dist = abs(hor_pos - 5000)
        if hor_pos > 5000:
            dir_1.write(1)
        else:
            dir_1.write(0)
        EN_1.write(0)
        sleep(0.1)
        while dist > 0:
            stp_1.write(1)
            sleep(0.0001)
            stp_1.write(0)
            sleep(0.001)
            dist -= 1
            print(dist)
        resetPins(1)
        hor_pos = 5000
    if vert_pos - 5000 != 0:
        dist = abs(vert_pos - 5000)
        if vert_pos > 5000:
            dir_2.write(1)
        else:
            dir_2.write(0)
        EN_2.write(0)
        sleep(0.1)
        while dist > 0:
            stp_2.write(1)
            sleep(0.0001)
            stp_2.write(0)
            sleep(0.00001)
            dist -= 1
            print(dist)
        resetPins(2)
        vert_pos = 5000
    if stage_pos - 5000 != 0:
        dist = abs(stage_pos - 5000)
        if stage_pos > 5000:
            dir_3.write(1)
        else:
            dir_3.write(0)
        EN_3.write(0)
        sleep(0.1)
        while dist > 0:
            stp_3.write(1)
            sleep(0.0001)
            stp_3.write(0)
            sleep(0.00001)
            dist -= 1
            print(dist)
        resetPins(3)
        stage_pos = 5000
    if foc_pos - 5000 != 0:
        dist = abs(foc_pos - 5000)
        if foc_pos > 5000:
            dir_4.write(1)
        else:
            dir_4.write(0)
        EN_4.write(0)
        sleep(0.1)
        while dist > 0:
            stp_4.write(1)
            sleep(0.0001)
            stp_4.write(0)
            sleep(0.00001)
            dist -= 1
            print(dist)
        resetPins(1)
        foc_pos = 5000



button1 = Button(root, text="FORWARD", height=5, width=10, bg="white", fg="blue")
button1.grid(row=6, column=2)
button1.bind('<ButtonPress-1>', start_motorfwd)
button1.bind('<ButtonRelease-1>', stop_motorfwd)
button2 = Button(root, text="REVERSE", height=5, width=10, bg="white", fg="red")
button2.grid(row=6, column=0)
button2.bind('<ButtonPress-1>', start_motorrev)
button2.bind('<ButtonRelease-1>', stop_motorrev)
button3 = Button(root, text="UP", height=5, width=10, bg="white", fg="blue")
button3.grid(row=0, column=1)
button3.bind('<ButtonPress-1>', start_motorup)
button3.bind('<ButtonRelease-1>', stop_motorup)
button4 = Button(root, text="DOWN", height=5, width=10, bg="white", fg="red")
button4.grid(row=10, column=1)
button4.bind('<ButtonPress-1>', start_motordown)
button4.bind('<ButtonRelease-1>', stop_motordown)
button5 = Button(root, text="STAGE UP", height=5, width=10, bg="white", fg="blue")
button5.grid(row=12, column=0)
button5.bind('<ButtonPress-1>', start_stage_motorup)
button5.bind('<ButtonRelease-1>', stop_stage_motorup)
button6 = Button(root, text="STAGE DOWN", height=5, width=10, bg="white", fg="red")
button6.grid(row=13, column=0)
button6.bind('<ButtonPress-1>', start_stage_motordown)
button6.bind('<ButtonRelease-1>', stop_stage_motordown)
button7 = Button(root, text="FOCUS UP", height=5, width=10, bg="white", fg="blue")
button7.grid(row=12, column=2)
button7.bind('<ButtonPress-1>', start_focus_motorup)
button7.bind('<ButtonRelease-1>', stop_focus_motorup)
button8 = Button(root, text="FOCUS DOWN", height=5, width=10, bg="white", fg="red")
button8.grid(row=13, column=2)
button8.bind('<ButtonPress-1>', start_focus_motordown)
button8.bind('<ButtonRelease-1>', stop_focus_motordown)
button9 = Button(root, text="RETURN HOME", height=5, width=10, bg="white", fg="red")
button9.grid(row=6, column=1)
button9.bind('<ButtonPress-1>', return_home)

speed = Scale(root, from_=1, to=100, orient=HORIZONTAL, label="SPEED", length=435, width=20, bg="white")
speed.grid(row=24, column=1)


if __name__ == '__main__':
    main()
    root.mainloop()
    b.exit()
