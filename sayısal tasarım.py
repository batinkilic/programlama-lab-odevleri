import tkinter as tk
from tkinter import messagebox, simpledialog
import os

class LogicGate:
    def __init__(self, label, inputs, canvas, x, y, image):
        self.label = label
        self.inputs = inputs
        self.output = None
        self.connections = []
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = image
        self.id = self.canvas.create_image(x, y, image=self.image)
        self.text_id = self.canvas.create_text(x, y + 30, text=label)
        self.inputs_received = []

    def calculate_output(self, *inputs):
        pass

    def add_connection(self, connection):
        self.connections.append(connection)

    def propagate_output(self):
        for connection in self.connections:
            if isinstance(connection, LogicGate):
                connection.receive_input(self.output)
            elif isinstance(connection, OutputBox) or isinstance(connection, LED):
                connection.set_value(self.output)
                if isinstance(connection, LED):
                    connection.update_state()

    def receive_input(self, input_value):
        self.inputs_received.append(input_value)
        if len(self.inputs_received) == self.inputs:
            self.calculate_output(*self.inputs_received)
            self.inputs_received = []

    def __str__(self):
        return self.label

class ANDGate(LogicGate):
    def __init__(self, canvas, x, y, image):
        super().__init__("AND", 2, canvas, x, y, image)

    def calculate_output(self, a, b):
        self.output = a and b
        self.propagate_output()
        return self.output

class ORGate(LogicGate):
    def __init__(self, canvas, x, y, image):
        super().__init__("OR", 2, canvas, x, y, image)

    def calculate_output(self, a, b):
        self.output = a or b
        self.propagate_output()
        return self.output

class NOTGate(LogicGate):
    def __init__(self, canvas, x, y, image):
        super().__init__("NOT", 1, canvas, x, y, image)

    def calculate_output(self, a):
        self.output = not a
        self.propagate_output()
        return self.output

class BufferGate(LogicGate):
    def __init__(self, canvas, x, y, image):
        super().__init__("Buffer", 1, canvas, x, y, image)

    def calculate_output(self, a):
        self.output = a
        self.propagate_output()
        return self.output

class NANDGate(LogicGate):
    def __init__(self, canvas, x, y, image):
        super().__init__("NAND", 2, canvas, x, y, image)

    def calculate_output(self, a, b):
        self.output = not (a and b)
        self.propagate_output()
        return self.output

class NORGate(LogicGate):
    def __init__(self, canvas, x, y, image):
        super().__init__("NOR", 2, canvas, x, y, image)

    def calculate_output(self, a, b):
        self.output = not (a or b)
        self.propagate_output()
        return self.output

class XORGate(LogicGate):
    def __init__(self, canvas, x, y, image):
        super().__init__("XOR", 2, canvas, x, y, image)

    def calculate_output(self, a, b):
        self.output = a != b
        self.propagate_output()
        return self.output

class XNORGate(LogicGate):
    def __init__(self, canvas, x, y, image):
        super().__init__("XNOR", 2, canvas, x, y, image)

    def calculate_output(self, a, b):
        self.output = a == b
        self.propagate_output()
        return self.output

class InputBox:
    def __init__(self, label, canvas, x, y, value):
        self.label = label
        self.value = value
        self.canvas = canvas
        self.x = x
        self.y = y
        self.connections = []
        self.id = self.canvas.create_text(x, y, text=f"{label}: {self.value}", tags="input")

    def set_value(self, value):
        self.value = value
        self.canvas.itemconfig(self.id, text=f"{self.label}: {self.value}")

    def get_value(self):
        return self.value

    def add_connection(self, connection):
        self.connections.append(connection)

    def propagate_output(self):
        for connection in self.connections:
            if isinstance(connection, LogicGate):
                connection.receive_input(self.value)
            elif isinstance(connection, OutputBox) or isinstance(connection, LED):
                connection.set_value(self.value)
                if isinstance(connection, LED):
                    connection.update_state()

class OutputBox:
    def __init__(self, label, canvas, x, y):
        self.label = label
        self.value = None
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = self.canvas.create_text(x, y, text=label, tags="output")

    def set_value(self, value):
        self.value = value
        self.canvas.itemconfig(self.id, text=f"{self.label}: {self.value}")

    def get_value(self):
        return self.value

class LED:
    def __init__(self, label, canvas, x, y):
        self.label = label
        self.state = False
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="red")
        self.text_id = self.canvas.create_text(x, y+20, text=label)

    def turn_on(self):
        self.state = True
        self.canvas.itemconfig(self.id, fill="green")

    def turn_off(self):
        self.state = False
        self.canvas.itemconfig(self.id, fill="red")

    def set_value(self, value):
        self.state = value
        self.update_state()

    def update_state(self):
        if self.state:
            self.turn_on()
        else:
            self.turn_off()

class ConnectionNode:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue")

class DigitalDesignPlatform:
    def __init__(self, root):
        self.root = root
        self.root.title("Sayısal Tasarım Projesi")
        self.gates = []
        self.input_boxes = []
        self.output_boxes = []
        self.leds = []
        self.lines = []
        self.nodes = []
        self.current_x = 100  # Başlangıç x pozisyonu
        self.current_y = 400  # Başlangıç y pozisyonu
        self.x_offset = 100  # Elemanlar arasındaki yatay mesafe
        self.load_images()
        self.create_widgets()
        self.selected_item = None

    def load_images(self):
        base_path = os.path.dirname(__file__)
        self.and_image = tk.PhotoImage(file=os.path.join(base_path, "and_gate.png")).subsample(4, 4)
        self.or_image = tk.PhotoImage(file=os.path.join(base_path, "or_gate.png")).subsample(4, 4)
        self.not_image = tk.PhotoImage(file=os.path.join(base_path, "not_gate.png")).subsample(4, 4)
        self.buffer_image = tk.PhotoImage(file=os.path.join(base_path, "buffer_gate.png")).subsample(4, 4)
        self.nand_image = tk.PhotoImage(file=os.path.join(base_path, "nand_gate.png")).subsample(4, 4)
        self.nor_image = tk.PhotoImage(file=os.path.join(base_path, "nor_gate.png")).subsample(4, 4)
        self.xor_image = tk.PhotoImage(file=os.path.join(base_path, "xor_gate.png")).subsample(4, 4)
        self.xnor_image = tk.PhotoImage(file=os.path.join(base_path, "xnor_gate.png")).subsample(4, 4)

    def create_widgets(self):
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        self.label = tk.Label(self.control_frame, text="Mantık Kapıları:")
        self.label.pack(side=tk.LEFT)

        self.gate_buttons = [
            ("AND", ANDGate, self.and_image),
            ("OR", ORGate, self.or_image),
            ("NOT", NOTGate, self.not_image),
            ("Buffer", BufferGate, self.buffer_image),
            ("NAND", NANDGate, self.nand_image),
            ("NOR", NORGate, self.nor_image),
            ("XOR", XORGate, self.xor_image),
            ("XNOR", XNORGate, self.xnor_image),
        ]

        for (text, gate, image) in self.gate_buttons:
            button = tk.Button(self.control_frame, text=text, image=image, compound=tk.TOP, command=lambda g=gate, img=image: self.add_gate(g, img))
            button.pack(side=tk.LEFT)

        self.add_input_button = tk.Button(self.control_frame, text="Giriş Kutusu Ekle", command=self.add_input_box)
        self.add_input_button.pack(side=tk.LEFT)

        self.add_output_button = tk.Button(self.control_frame, text="Çıkış Kutusu Ekle", command=self.add_output_box)
        self.add_output_button.pack(side=tk.LEFT)

        self.add_led_button = tk.Button(self.control_frame, text="LED Ekle", command=self.add_led)
        self.add_led_button.pack(side=tk.LEFT)

        self.add_node_button = tk.Button(self.control_frame, text="Bağlantı Düğümü Ekle", command=self.add_connection_node)
        self.add_node_button.pack(side=tk.LEFT)

        self.run_button = tk.Button(self.control_frame, text="Çalıştır", command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.control_frame, text="Durdur", command=self.stop_simulation)
        self.stop_button.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.select_item)
        self.canvas.bind("<Button-3>", self.connect_items)

    def add_gate(self, gate_class, image):
        x, y = self.get_position()
        gate = gate_class(self.canvas, x, y, image)
        self.gates.append(gate)
        messagebox.showinfo("Eklendi", f"{gate} eklendi.")
        self.update_position()

    def add_input_box(self):
        x, y = self.get_position()
        label = f"Giriş {len(self.input_boxes) + 1}"
        value = self.ask_for_value()
        input_box = InputBox(label, self.canvas, x, y, value)
        self.input_boxes.append(input_box)
        self.canvas.tag_bind(input_box.id, "<Double-1>", lambda event, box=input_box: self.set_input_value(box))
        self.update_position()

    def add_output_box(self):
        x, y = self.get_position()
        label = f"Çıkış {len(self.output_boxes) + 1}"
        output_box = OutputBox(label, self.canvas, x, y)
        self.output_boxes.append(output_box)
        self.canvas.create_text(x, y + 20, text="Sonuç bekleniyor...", tags="output")
        self.update_position()

    def add_led(self):
        x, y = self.get_position()
        label = f"LED {len(self.leds) + 1}"
        led = LED(label, self.canvas, x, y)
        self.leds.append(led)
        self.update_position()

    def add_connection_node(self):
        x, y = self.get_position()
        node = ConnectionNode(self.canvas, x, y)
        self.nodes.append(node)
        messagebox.showinfo("Eklendi", "Bağlantı düğümü eklendi.")
        self.update_position()

    def ask_for_value(self):
        while True:
            value = simpledialog.askstring("Giriş Değeri", "0 veya 1 giriniz:")
            if value in ["0", "1"]:
                return int(value)
            else:
                messagebox.showwarning("Hata", "Giriş değeri 0 veya 1 olmalıdır.")

    def get_position(self):
        return self.current_x, self.current_y

    def update_position(self):
        self.current_x += self.x_offset
        if self.current_x > self.canvas.winfo_width() - self.x_offset:
            self.current_x = 100
            self.current_y += 100

    def select_item(self, event):
        self.selected_item = self.canvas.find_closest(event.x, event.y)[0]

    def connect_items(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        if self.selected_item and self.selected_item != item:
            x1, y1 = self.canvas.coords(self.selected_item)[:2]
            x2, y2 = self.canvas.coords(item)[:2]
            line = self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
            self.lines.append(line)
            from_item = self.find_object_by_id(self.selected_item)
            to_item = self.find_object_by_id(item)
            if isinstance(from_item, LogicGate) and isinstance(to_item, LogicGate):
                from_item.add_connection(to_item)
            elif isinstance(from_item, InputBox) and isinstance(to_item, LogicGate):
                from_item.add_connection(to_item)
            elif isinstance(from_item, LogicGate) and isinstance(to_item, OutputBox):
                from_item.add_connection(to_item)
            elif isinstance(from_item, LogicGate) and isinstance(to_item, LED):
                from_item.add_connection(to_item)
            elif isinstance(from_item, InputBox) and isinstance(to_item, OutputBox):
                from_item.add_connection(to_item)
            elif isinstance(from_item, InputBox) and isinstance(to_item, LED):
                from_item.add_connection(to_item)
            messagebox.showinfo("Bağlantı", f"{from_item} ile {to_item} arasında bağlantı kuruldu.")
            self.selected_item = None

    def find_object_by_id(self, item_id):
        for gate in self.gates:
            if gate.id == item_id:
                return gate
        for input_box in self.input_boxes:
            if input_box.id == item_id:
                return input_box
        for output_box in self.output_boxes:
            if output_box.id == item_id:
                return output_box
        for led in self.leds:
            if led.id == item_id:
                return led
        for node in self.nodes:
            if node.id == item_id:
                return node
        return None

    def run_simulation(self):
        for input_box in self.input_boxes:
            input_box.propagate_output()

        for gate in self.gates:
            inputs = [box.get_value() for box in self.input_boxes[:gate.inputs]]
            result = gate.calculate_output(*inputs)
            gate.output = result
            self.canvas.itemconfig(gate.text_id, text=f"{gate.label}: {int(result)}")

        for output_box in self.output_boxes:
            if output_box.value is None:
                output_box.value = 0
            self.canvas.itemconfig(output_box.id, text=f"{output_box.label}: {int(output_box.value)}")

        for led in self.leds:
            led.update_state()

    def reset_simulation(self):
        self.gates.clear()
        self.input_boxes.clear()
        self.output_boxes.clear()
        self.leds.clear()
        self.nodes.clear()
        self.lines.clear()
        self.canvas.delete("all")
        self.current_x = 100
        self.current_y = 400
        messagebox.showinfo("Reset", "Simülasyon sıfırlandı.")

    def stop_simulation(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalDesignPlatform(root)
    root.mainloop()
