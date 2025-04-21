import tkinter as tk
from tkinter import messagebox

# Constants
TOTAL_BLOCKS = 100

# Initialize FAT table with all blocks free (-1)
FAT = [-1] * TOTAL_BLOCKS

# Initialize block allocation status
blocks = ["free"] * TOTAL_BLOCKS

def create_file(file_size):
    free_blocks = [i for i, x in enumerate(FAT) if x == -1]
    if len(free_blocks) < file_size:
        messagebox.showerror("Error", "Not enough free blocks")
        return

    start_block = free_blocks.pop(0)
    current_block = start_block

    for _ in range(file_size - 1):
        next_block = free_blocks.pop(0)
        FAT[current_block] = next_block
        current_block = next_block

    FAT[current_block] = -2  # End of file marker
    update_blocks()
    return start_block

def delete_file(start_block):
    current_block = start_block
    while current_block != -2:
        next_block = FAT[current_block]
        FAT[current_block] = -1
        current_block = next_block
    update_blocks()

def update_blocks():
    for i in range(TOTAL_BLOCKS):
        if FAT[i] == -1:
            blocks[i] = "free"
        else:
            blocks[i] = "allocated"
    draw_blocks()

def draw_blocks():
    for i in range(TOTAL_BLOCKS):
        color = "green" if blocks[i] == "free" else "red"
        canvas.itemconfig(block_rects[i], fill=color)

def create_file_callback():
    try:
        size = int(entry_file_size.get())
        if size <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid file size")
        return

    start_block = create_file(size)
    if start_block is not None:
        messagebox.showinfo("Success", f"File created starting at block {start_block}")

def delete_file_callback():
    try:
        start_block = int(entry_start_block.get())
        if start_block < 0 or start_block >= TOTAL_BLOCKS or FAT[start_block] == -1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid start block")
        return

    delete_file(start_block)
    messagebox.showinfo("Success", f"File starting at block {start_block} deleted")

def view_fat_callback():
    fat_window = tk.Toplevel(root)
    fat_window.title("FAT Table")

    fat_text = tk.Text(fat_window, width=50, height=10)
    fat_text.pack()

    for i, entry in enumerate(FAT):
        fat_text.insert(tk.END, f"Block {i}: {entry}\n")

def resize_canvas(event):
    width = event.width
    height = event.height - frame_controls.winfo_height()  # Adjust for control frame height
    canvas.config(width=width, height=height)
    draw_blocks_scaled(width, height)

def draw_blocks_scaled(width, height):
    block_size = min(width // 20, height // 5) - 5
    for i in range(TOTAL_BLOCKS):
        x0 = (i % 20) * (block_size + 5)
        y0 = (i // 20) * (block_size + 5)
        x1 = x0 + block_size
        y1 = y0 + block_size
        canvas.coords(block_rects[i], x0, y0, x1, y1)

# GUI Setup
root = tk.Tk()
root.title("FAT File Allocation Simulation")
root.state('zoomed')  # Start the application in fullscreen mode

frame_controls = tk.Frame(root)
frame_controls.pack(fill=tk.X)

label_file_size = tk.Label(frame_controls, text="File Size:")
label_file_size.grid(row=0, column=0)
entry_file_size = tk.Entry(frame_controls)
entry_file_size.grid(row=0, column=1)
button_create = tk.Button(frame_controls, text="Create File", command=create_file_callback)
button_create.grid(row=0, column=2)

label_start_block = tk.Label(frame_controls, text="Start Block:")
label_start_block.grid(row=1, column=0)
entry_start_block = tk.Entry(frame_controls)
entry_start_block.grid(row=1, column=1)
button_delete = tk.Button(frame_controls, text="Delete File", command=delete_file_callback)
button_delete.grid(row=1, column=2)

button_view_fat = tk.Button(frame_controls, text="View FAT", command=view_fat_callback)
button_view_fat.grid(row=2, columnspan=3)

canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

block_rects = []
for i in range(TOTAL_BLOCKS):
    rect = canvas.create_rectangle(0, 0, 20, 20, fill="green", outline="black")
    block_rects.append(rect)

root.bind('<Configure>', resize_canvas)

root.mainloop()
