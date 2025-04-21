import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class Disk:
    def __init__(self, size):
        self.size = size
        self.blocks = [None] * size  # None means the block is free

    def allocate_blocks(self, num_blocks):
        free_blocks = [i for i, block in enumerate(self.blocks) if block is None]
        if len(free_blocks) < num_blocks + 1:  # +1 for the index block
            return None  # Not enough free blocks

        allocated_blocks = random.sample(free_blocks, num_blocks + 1)
        index_block = allocated_blocks[0]
        data_blocks = allocated_blocks[1:]
        
        self.blocks[index_block] = data_blocks  # The index block stores the data blocks
        for block in data_blocks:
            self.blocks[block] = "data"

        return index_block, data_blocks

    def free_blocks(self, index_block):
        if self.blocks[index_block] is None:
            return  # No blocks to free

        data_blocks = self.blocks[index_block]
        self.blocks[index_block] = None
        for block in data_blocks:
            self.blocks[block] = None

    def display(self):
        return self.blocks

class DiskGUI:
    def __init__(self, master, disk):
        self.master = master
        self.disk = disk

        self.master.title("Indexed Allocation Simulation")
        self.master.state('zoomed')  # Start the application in fullscreen mode

        self.control_frame = tk.Frame(master)
        self.control_frame.grid(row=0, column=0, sticky='nsew')

        self.canvas = tk.Canvas(master)
        self.canvas.grid(row=1, column=0, sticky='nsew')

        self.allocate_button = tk.Button(self.control_frame, text="Allocate File", command=self.allocate_file)
        self.allocate_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.free_button = tk.Button(self.control_frame, text="Free File", command=self.free_file)
        self.free_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.view_index_button = tk.Button(self.control_frame, text="View Index Table", command=self.view_index_table)
        self.view_index_button.grid(row=0, column=2, padx=5, pady=5)

        self.block_size = 20
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        self.draw_disk()
        
        master.bind('<Configure>', self.resize_canvas)

    def draw_disk(self):
        self.canvas.delete("all")
        for i, block in enumerate(self.disk.display()):
            x = (i % 25) * self.block_size
            y = (i // 25) * self.block_size
            color = "white" if block is None else "green" if isinstance(block, list) else "blue"
            self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill=color)
            self.canvas.create_text(x + self.block_size // 2, y + self.block_size // 2, text=str(i))

    def resize_canvas(self, event):
        width = self.master.winfo_width()
        height = self.master.winfo_height() - self.control_frame.winfo_height()
        self.canvas.config(width=width, height=height)
        self.draw_disk_scaled(width, height)

    def draw_disk_scaled(self, width, height):
        self.block_size = min(width // 25, height // (self.disk.size // 25)) - 5
        self.draw_disk()

    def allocate_file(self):
        try:
            num_blocks = int(simpledialog.askstring("Input", "Enter number of blocks:", parent=self.master))
            if num_blocks <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return
        result = self.disk.allocate_blocks(num_blocks)
        if result is None:
            messagebox.showerror("Error", "Not enough free blocks")
        else:
            self.draw_disk()

    def free_file(self):
        try:
            index_block = int(simpledialog.askstring("Input", "Enter index block to free:", parent=self.master))
            if index_block < 0 or index_block >= self.disk.size or not isinstance(self.disk.blocks[index_block], list):
                raise ValueError
        except (TypeError, ValueError):
            return
        self.disk.free_blocks(index_block)
        self.draw_disk()

    def view_index_table(self):
        try:
            index_block = int(simpledialog.askstring("Input", "Enter index block of the file to view index table:", parent=self.master))
            if index_block < 0 or index_block >= self.disk.size or not isinstance(self.disk.blocks[index_block], list):
                raise ValueError
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Invalid index block")
            return
        index_table = self.disk.blocks[index_block]
        messagebox.showinfo("Index Table", f"Index Table for Index Block {index_block}: {index_table}")

if __name__ == "__main__":
    root = tk.Tk()
    disk = Disk(size=100)
    gui = DiskGUI(root, disk)
    root.mainloop()
