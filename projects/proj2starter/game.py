# MCS 275 Spring 2024
# David Dumas

# NOTE: This _experimental_ labyrinth game/simulation is
# experimental and is not held to the same standard of
# quality as the normative project 2 materials.  It may
# also be updated to make improvements or fix bugs.

from plane import Point2, Vector2
import random
from tkinter import *
from tkinter import font
from tkinter import scrolledtext
from PIL import ImageTk, Image
from labyrinth import *
from functools import partial
import argparse

__version__ = "1.1"


class Pref:
    pressed_bg = "#bcbcf5"
    pressed_active_bg = "#c9c9f7"


class HelpWindow(Toplevel):
    """
    ESCAPE OF THE MINOTAUR v1.1 (Feb 2024)
    David Dumas

    Labyrinth editor/simulator created for MCS 275 Spring 2024 project 2 at UIC.

    Interface:

    EDIT button toggles between edit mode and play mode.

    ARROW KEYS move around while in play mode.  Try to solve the labyrinth.

    RESET button restarts the labyrinth in play mode.

    CLICK cell type buttons at bottom and/or inside labyrinth to make changes when in edit mode.

    Keyboard shortcuts:
     * up/down/left/right - move (in play mode)
     * Q/q - exit
     * Escape - toggle edit mode on/off
     * F1/H/h - open this help screen
    """

    def __init__(self, parent, close_cb=None):
        super().__init__(parent)
        self.content = (
            "\n".join(
                [(x[4:] if len(x) >= 4 else "") for x in self.__doc__.splitlines()]
            )
        ).format(__version__)
        self.close_cb = close_cb
        self.title("EotM Help")
        text_area = scrolledtext.ScrolledText(
            self, wrap=WORD, width=60, height=25, font=("sans-serif", 12)
        )
        text_area.insert(INSERT, self.content)
        text_area.configure(state=DISABLED)
        text_area.pack()
        btn = Button(self, text="Close", height=2, width=7, command=self.on_close)
        btn.pack(padx=20, pady=20)

    def destroy(self):
        if self.close_cb:
            self.close_cb()
        super().destroy()

    def on_close(self, *args):
        self.destroy()
        self.update()


class DoubleBufferCanvas(Canvas):
    def __init__(self, parent, img):
        w, h = img.size
        super().__init__(parent, width=w, height=h)
        self.itk_current = ImageTk.PhotoImage(image=img)
        self.itk_other = ImageTk.PhotoImage(image=img)
        self.id_current = self.create_image(0, 0, anchor=NW, image=self.itk_current)
        self.id_other = self.create_image(0, 0, anchor=NW, image=self.itk_other)
        self.fix_displaystates()

    def fix_displaystates(self):
        self.itemconfig(self.id_current, state="normal")
        self.itemconfig(self.id_other, state="hidden")

    def update_img(self, img):
        self.itk_other.paste(img)
        self.itk_current, self.itk_other = self.itk_other, self.itk_current
        self.id_current, self.id_other = self.id_other, self.id_current
        self.fix_displaystates()


class SustainedButton(Button):
    def __init__(self, *args, **kwargs):
        self.state = False
        self.offable = True
        if "state" in kwargs:
            self.state = kwargs.pop("state")
        if "offable" in kwargs:
            self.offable = kwargs.pop("offable")
        self.orig_cmd = None
        if "command" in kwargs:
            self.orig_cmd = kwargs.pop("command")
        super().__init__(*args, **kwargs, command=self.go)
        self.orig_bg = self.cget("background")
        self.orig_active_bg = self.cget("activebackground")
        self.update_disp()

    def toggle(self):
        self.set_state(not self.state)

    def set_state(self, state):
        self.state = state
        self.update_disp()

    def go(self):
        if self.offable or not self.state:
            self.toggle()
            if self.orig_cmd is not None:
                self.orig_cmd()

    def update_disp(self):
        if self.state:
            self.config(
                relief=SUNKEN,
                background=Pref.pressed_bg,
                activebackground=Pref.pressed_active_bg,
            )
        else:
            self.config(
                relief=RAISED,
                background=self.orig_bg,
                activebackground=self.orig_active_bg,
            )


class MinotaurStatusFrame(Frame):
    def __init__(self, parent, scale, *args, **kwargs):
        self.scale = scale
        self.status = {
            "plank": True,
            "keys": 3,
            "flight_range": 5,
        }
        if "status" in kwargs:
            self.status = {k: status[k] for k in kwargs.pop("status")}
        self.on_change = None
        if "on_change" in kwargs:
            self.on_change = kwargs.pop("on_change")
        super().__init__(parent, *args, **kwargs)
        default_font = font.nametofont("TkDefaultFont")
        Label(self, text="Plank").grid(row=1, column=1, sticky=E)
        Label(self, text="Keys").grid(row=2, column=1, sticky=E)
        Label(self, text="Flight range").grid(row=3, column=1, sticky=E)
        self.winlabel = Label(
            self,
            text="",
            width=17,
            fg="red",
            font=("sans-serif", self._d(0.4), font.BOLD),
        )
        self.winlabel.grid(
            row=4, column=1, columnspan=2, sticky=E + W + S, padx=10, pady=10
        )
        self.plank_v = IntVar(value=int(self.status["plank"]))
        self.plank_v.trace_add("write", self.on_plank_write)
        self.plank_w = SustainedButton(
            self,
            width=5,
            text=str(self.status["plank"]),
            state=self.status["plank"],
            command=self.on_plank_write,
        )
        self.plank_w.grid(row=1, column=2, sticky=W, padx=15, pady=5)
        self.keys_v = StringVar(value=str(self.status["keys"]))
        self.keys_v.trace_add("write", self.on_keys_write)
        self.keys_w = Entry(self, textvariable=self.keys_v, width=5, font=default_font)
        self.number_vcmd = (self.register(self.validate_number), "%P")
        self.keys_w.config(validate="all", validatecommand=self.number_vcmd)
        self.keys_w.grid(row=2, column=2, sticky=W, padx=15, pady=5)
        self.range_v = StringVar(value=("{:.1f}".format(self.status["flight_range"])))
        self.range_v.trace_add("write", self.on_range_write)
        self.float_vcmd = (self.register(self.validate_float), "%P")
        self.range_w = Entry(
            self, textvariable=self.range_v, width=5, font=default_font
        )
        self.range_w.config(validate="all", validatecommand=self.float_vcmd)
        self.range_w.grid(column=2, row=3, sticky=W, padx=15, pady=5)

    def _d(self, x):
        return int(x * self.scale)

    def validate_number(self, value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            self.bell()
            return False

    def validate_float(self, value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            self.bell()
            return False

    def on_plank_write(self, *args):
        self.status["plank"] = self.plank_w.state
        self.plank_w.config(text=str(self.plank_w.state))

    def on_range_write(self, *args):
        try:
            self.status["flight_range"] = float(self.range_v.get())
        except:
            pass

    def on_keys_write(self, *args):
        try:
            self.status["keys"] = int(self.keys_v.get())
        except:
            pass

    def keys_sync(self):
        self.keys_v.set(self.status["keys"])


class CellSelectFrame(Frame):
    def __init__(self, parent, scale, *args, **kwargs):
        self.scale = scale
        self.selected = CT_EMPTY
        if "selected" in kwargs:
            self.selected = kwargs.pop("selected")
        self.on_change = None
        if "on_change" in kwargs:
            self.on_change = kwargs.pop("on_change")
        super().__init__(parent, *args, **kwargs)
        self.ct_btn = {}
        self.ct_btn_image = {}
        for c in CELL_TYPES:
            itk = ImageTk.PhotoImage(image=CellRenderer.img(c, scale=self.scale))
            self.ct_btn_image[c] = itk
            b = SustainedButton(
                self,
                offable=False,
                image=itk,
                width=3 * self.scale // 2,
                height=3 * self.scale // 2,
                command=partial(self.pressed, c),
                state=(c == self.selected),
            )
            self.ct_btn[c] = b
            b.pack(side=LEFT, padx=self._d(0.1), pady=self._d(0.1))

    def _d(self, x):
        return int(x * self.scale)

    def pressed(self, c):
        self.selected = c
        for c in self.ct_btn:
            if c != self.selected:
                self.ct_btn[c].set_state(False)

    def set_active(self, s):
        for b in self.ct_btn.values():
            b.configure(state="normal" if s else "disable")
        for c in self.ct_btn:
            self.ct_btn[c].set_state((c == self.selected) and s)


class LabyrinthInteractorApp(Tk):
    KEY_DISPS = {
        "left": Vector2(-1, 0),
        "right": Vector2(1, 0),
        "down": Vector2(0, 1),
        "up": Vector2(0, -1),
    }

    def __init__(self, lab, scale=40):
        super().__init__()
        self.helpwindow = None
        self.deleted_locks = []
        self.lab = lab
        self.minotaur_pos = self.lab.start
        self.scale = scale
        default_font = font.nametofont("TkDefaultFont")
        fontsize = default_font.cget("size")
        default_font.configure(size=max(self.scale // 4, 12, fontsize))
        self.title("Escape of the Minotaur")
        self.canvas = DoubleBufferCanvas(self, self.lab.as_image(scale=self.scale))
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.canvas_btn1)
        self.canvas.bind("<B1-Motion>", self.canvas_btn1)
        self.bind("<Up>", lambda ev: self.keypress("up"))
        self.bind("<Down>", lambda ev: self.keypress("down"))
        self.bind("<Left>", lambda ev: self.keypress("left"))
        self.bind("<Right>", lambda ev: self.keypress("right"))
        self.bind("q", lambda ev: self.destroy())
        self.bind("Q", lambda ev: self.destroy())
        self.bind("h", lambda ev: self.help_click())
        self.bind("H", lambda ev: self.help_click())
        self.bind("<F1>", lambda ev: self.help_click())
        self.lower_frame = Frame(self)
        self.editing = Frame(self.lower_frame)
        self.buttons = Frame(self.editing)
        self.editbtn = SustainedButton(
            self.buttons, text="Edit", command=self.edit_click, width=10, height=2
        )
        self.editbtn.pack(side=LEFT, padx=20)
        self.resetbtn = Button(
            self.buttons, text="Reset", command=self.reset_click, width=10, height=2
        )
        self.resetbtn.pack(side=LEFT, padx=20)
        self.helpbtn = Button(
            self.buttons, text="Help", command=self.help_click, width=10, height=2
        )
        self.helpbtn.pack(side=LEFT, padx=20)
        self.buttons.pack(side=TOP, pady=20)
        self.bind("<Escape>", lambda ev: self.editbtn.go())
        self.ct_sel = CellSelectFrame(self.editing, self.scale)
        self.ct_sel.pack(side=TOP, pady=20)
        self.ct_sel.set_active(False)
        self.editing.pack(side=LEFT, padx=50, pady=0)

        self.stframe = MinotaurStatusFrame(self.lower_frame, self.scale)
        self.stframe.pack(side=LEFT)

        self.lower_frame.pack(side=TOP)
        x, y = self.point_to_coords(self.lab.start)
        r = self.scale * (10 + self.stframe.status["flight_range"])
        self.range_circle_id = self.canvas.create_oval(
            x - r, y - r, x + r, y + r, outline="red", width=3
        )
        self.canvas.itemconfig(self.range_circle_id, state="hidden")
        self.circle_show = False
        self.lab_redraw()

    def point_to_coords(self, p):
        return int(self.scale * (p.x + 0.5)), int(self.scale * (p.y + 0.5))

    def show_range_circle(self, p, d):
        r = self.scale * d
        x, y = self.point_to_coords(p)
        self.canvas.coords(self.range_circle_id, x - r, y - r, x + r, y + r)
        self.canvas.itemconfig(self.range_circle_id, state="normal")
        self.circle_show = True

    def keypress(self, k):
        if self.editbtn.state:
            # edit mode, do nothing
            return
        if not self.minotaur_pos:
            return
        if self.minotaur_pos == self.lab.goal:
            return
        new_pos = self.minotaur_pos + self.KEY_DISPS[k]
        if not self.lab.is_valid(new_pos):
            return
        ct = self.lab.get_cell(new_pos)
        dirty = False
        if ct == CT_WALL:
            return
        if ct in [CT_EMPTY, CT_GOAL, CT_START]:
            self.minotaur_pos = new_pos
            if ct == CT_GOAL:
                self.win_show()
            dirty = True
        elif ct == CT_PIT:
            if self.stframe.status["plank"]:
                self.minotaur_pos = new_pos
                dirty = True
        elif ct == CT_LOCK:
            if self.stframe.status["keys"]:
                self.lab.set_empty(new_pos)
                self.deleted_locks.append(new_pos)
                self.minotaur_pos = new_pos
                dirty = True
                self.stframe.status["keys"] -= 1
                self.stframe.keys_sync()
        elif ct == CT_SPRING:
            if self.stframe.status["flight_range"] >= abs(new_pos - self.lab.goal):
                # can fly
                self.minotaur_pos = self.lab.goal
                self.win_show()
                dirty = True
            else:
                if self.stframe.status["flight_range"] > 0:
                    self.show_range_circle(new_pos, self.stframe.status["flight_range"])
                pass
        if dirty:
            self.lab_redraw()

    def win_clear(self):
        self.stframe.winlabel.configure(text="")

    def win_show(self):
        self.stframe.winlabel.configure(text="Minotaur escaped!")

    def reset_click(self):
        if self.editbtn.state:
            return
        self.win_clear()
        for p in self.deleted_locks:
            self.lab.set_lock(p)
        self.deleted_locks.clear()
        self.minotaur_pos = self.lab.start
        self.lab_redraw()

    def help_click(self):
        if self.helpwindow is None:
            self.helpwindow = HelpWindow(self, self.on_help_close)

    def on_help_close(self):
        self.helpwindow = None

    def edit_click(self):
        self.ct_sel.set_active(self.editbtn.state)
        self.win_clear()
        if self.editbtn.state:
            # entering edit mode
            for p in self.deleted_locks:
                self.lab.set_lock(p)
            self.deleted_locks.clear()
            self.resetbtn.configure(state="disabled")
        else:
            # exiting edit mode
            self.minotaur_pos = self.lab.start
            self.resetbtn.configure(state="normal")
        self.lab_redraw()

    def canvas_btn1(self, ev):
        if not self.editbtn.state:
            return
        c = self.ct_sel.selected
        p = Point2(ev.x // self.scale, ev.y // self.scale)
        if self.lab.get_cell(p) == c:
            return
        if c == CT_START:
            self.lab.start = p
        elif c == CT_GOAL:
            self.lab.goal = p
        else:
            self.lab.set_cell(p, c)
        self.lab_redraw()

    def _d(self, x):
        return int(x * self.scale)

    def lab_redraw(self):
        if self.circle_show:
            self.canvas.itemconfig(self.range_circle_id, state="hidden")
        h = []
        if self.minotaur_pos and not self.editbtn.state:
            h.append(self.minotaur_pos)
        self.canvas.update_img(self.lab.as_image(scale=self.scale, highlight=h))

    def on_click(self):
        x = random.randrange(self.lab.xsize)
        y = random.randrange(self.lab.ysize)
        self.minotaur_pos = Point2(x, y)
        self.lab_redraw()


parser = argparse.ArgumentParser()
parser.add_argument(
    "-l",
    "--labyrinth",
    default="blank20x20",
    help="Labyrinth to start with; options are sample0,sample1,...,sample8 or blankNxM where N and M are integers (e.g. blank25x14) or a named labyrinth used by the autograder.",
)
parser.add_argument(
    "-s",
    "--scale",
    default=30,
    type=int,
    help="Pixels per grid square, increase to make labyrinth view larger.  Minimum 5.",
)
args = parser.parse_args()

if args.labyrinth.startswith("blank"):
    xsize, ysize = [int(t) for t in args.labyrinth.removeprefix("blank").split("x")]
    assert xsize > 2
    assert ysize > 2
    lab = Labyrinth(
        xsize=xsize,
        ysize=ysize,
        start=Point2(xsize // 2, ysize // 2),
        goal=Point2(xsize - 1, ysize // 2),
    )
    lab.apply_empty_interior()
elif args.labyrinth.startswith("sample"):
    n = int(args.labyrinth.removeprefix("sample"))
    lab = sample_labyrinth(n)
else:
    lab = sample_labyrinth(args.labyrinth)

assert args.scale >= 5
app = LabyrinthInteractorApp(lab, scale=args.scale)
app.mainloop()
