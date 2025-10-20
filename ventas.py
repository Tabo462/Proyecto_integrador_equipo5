import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Ventas(tk.Frame):
    db_name = "database.db"

    def __init__(self, parent):
        super().__init__(parent)  # Se crea el frame principal
        self.numero_factura_actual = self.obtener_numero_factura_actual()  # Saca el número siguiente de factura
        self.widgets()  # Arma la interfaz
        self.mostrar_numero_factura()  # Muestra el número en el campo correspondiente

    # Arma todos los widgets de la pantalla de ventas
    def widgets(self):
        frame1 = tk.Frame(self, bg="#DE2924", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="VENTAS", bg="#DE2924", font="sans 30 bold", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        frame2 = tk.Frame(self, bg="#FDC32F", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        lblframe = LabelFrame(frame2, text="Informacíon de la venta", bg="#FDC32F", font="sans 16 bold")
        lblframe.place(x=10, y=10, width=1060, height=80)

        label_numero_factura = tk.Label(lblframe, text="Número de \nfactura", bg="#FDC32F", font="sans 12 bold")
        label_numero_factura.place(x=10, y=5)
        self.numero_factura = tk.StringVar()

        self.entry_numero_factura = ttk.Entry(lblframe, textvariable=self.numero_factura, state="readonly", font="sans 12 bold")
        self.entry_numero_factura.place(x=100, y=5, width=80)

        label_nombre = tk.Label(lblframe, text="Productos: ", bg="#FDC32F", font="sans 12 bold")
        label_nombre.place(x=200, y=12)
        self.entry_nombre = ttk.Combobox(lblframe, font='sans 12 bold', state="readonly")
        self.entry_nombre.place(x=280, y=10, width=180)

        self.cargar_productos()

        label_valor = tk.Label(lblframe, text="Precio:", bg="#FDC32F", font="sans 12 bold")
        label_valor.place(x=470, y=12)
        self.entry_valor = ttk.Entry(lblframe, font="sans 12 bold", state="readonly")
        self.entry_valor.place(x=540, y=10, width=180)

        self.entry_nombre.bind("<<ComboboxSelected>>", self.actualizar_precio)

        label_cantidad = tk.Label(lblframe, text="Cantidad:", bg="#FDC32F", font="sans 12 bold")
        label_cantidad.place(x=730, y=12)

        self.entry_cantidad = ttk.Entry(lblframe, font="sans 12 bold")
        self.entry_cantidad.place(x=820, y=10)

        treFrame = tk.Frame(frame2, bg="#FDC32F")
        treFrame.place(x=150, y=120, width=800, height=200)

        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tree = ttk.Treeview(treFrame, columns=("Productos", "Precio", "Cantidad", "Subtotal"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)

        self.tree.heading("Productos", text="Producto")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Subtotal", text="Subtotal")

        self.tree.column("Productos", anchor="center")
        self.tree.column("Precio", anchor="center")
        self.tree.column("Cantidad", anchor="center")
        self.tree.column("Subtotal", anchor="center")

        self.tree.pack(expand=True, fill=BOTH)

        self.label_suma_total = tk.Label(frame2, text="Total a pagar: MXN 0", bg="#FDC32F", font="sans 25 bold")
        self.label_suma_total.place(x=360, y=420)

        lblframe1 = LabelFrame(frame2, text="Opciones", bg="#DE2924", font="sans 12 bold")
        lblframe1.place(x=10, y=340, width=1060, height=70)

        boton_agregar = tk.Button(lblframe1, text="Agregar Artículo", bg="#DE2924", font="sans 12 bold", command=self.registrar)
        boton_agregar.place(x=50, y=1, width=240, height=40)

        boton_pagar = tk.Button(lblframe1, text="Realizar Pago", bg="#DE2924", font="sans 12 bold", command=self.abrir_ventana_pago)
        boton_pagar.place(x=400, y=1, width=240, height=40)

        boton_ver_facturas = tk.Button(lblframe1, text="Ver Facturas", bg="#DE2924", font="sans 12", command=self.abrir_ventana_factura)
        boton_ver_facturas.place(x=750, y=1, width=240, height=40)

    # Carga los nombres de los productos para el combobox
    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM inventario")
            productos = c.fetchall()
            self.entry_nombre["values"] = [producto[0] for producto in productos]
            if not productos:
                print("No se encontraron productos en la base de datos.")
            conn.close()
        except sqlite3.Error as e:
            print("Error al cargar procutso desde la base de datos:", e)

    # Cuando eliges un producto, pone su precio en el campo de precio
    def actualizar_precio(self, event):
        nombre_producto = self.entry_nombre.get()
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio FROM inventario WHERE nombre = ?", (nombre_producto,))
            precio = c.fetchone()
            if (precio):
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, precio[0])
                self.entry_valor.config(state="readonly")
            else:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, "Precio no disponible")
                self.entry_valor.config(state="readonly")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el precio: {e}")
        finally:
            conn.close()

    # Recalcula el total sumando los subtotales de la tabla
    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        self.label_suma_total.config(text=f"Total a pagar : MXN {total:.2f}")

    # Agrega el artículo seleccionado a la lista de venta
    def registrar(self):
        producto = self.entry_nombre.get()
        precio_str = self.entry_valor.get()
        cantidad_str = self.entry_cantidad.get()

        if not producto:
            messagebox.showerror("Error", "Debe seleccionar un producto")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida mayor a 0")
            return

        try:
            precio = float(str(precio_str).replace(",", ""))
        except ValueError:
            messagebox.showerror("Error", "Precio inválido")
            return

        subtotal = round(precio * cantidad, 2)
        # Inserta una nueva fila en la tabla de la venta
        self.tree.insert("", tk.END, values=(producto, f"{precio:.2f}", cantidad, f"{subtotal:.2f}"))
        # Limpia la cantidad para que sea más cómodo ingresar otro artículo
        self.entry_cantidad.delete(0, tk.END)
        # Actualiza el total mostrado
        self.actualizar_total()

    # Saca el último número de factura y suma 1, si no hay devuelve 1
    def obtener_numero_factura_actual(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT MAX(factura) FROM ventas")
            result = c.fetchone()
            conn.close()
            if result and result[0]:
                return result[0] + 1
            else:
                return 1
        except sqlite3.Error:
            return 1

    # Muestra el número de factura en el campo correspondiente
    def mostrar_numero_factura(self):
        self.numero_factura.set(str(self.numero_factura_actual))

    # Abre una ventana simple para procesar el pago y guardar la venta
    def abrir_ventana_pago(self):
        if not self.tree.get_children():
            messagebox.showwarning("Pago", "No hay artículos en la venta")
            return

        ventana_pago = Toplevel(self)
        ventana_pago.title("Procesar Pago")
        ventana_pago.geometry("300x200")
        ventana_pago.config(bg="#FDC32F")

        lbl_total = Label(ventana_pago, text=self.label_suma_total.cget("text"), bg="#FDC32F", font="sans 12 bold")
        lbl_total.pack(pady=10)

        lbl_pago = Label(ventana_pago, text="Pago recibido:", bg="#FDC32F", font="sans 12 bold")
        lbl_pago.pack(pady=5)
        entry_pago = Entry(ventana_pago, font="sans 12 bold")
        entry_pago.pack(pady=5)

        def procesar_pago():
            try:
                pago = float(entry_pago.get().replace(",", ""))
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido")
                return

            # Calcula total nuevamente por seguridad
            total = 0.0
            items = []
            for child in self.tree.get_children():
                producto, precio_str, cantidad, subtotal_str = self.tree.item(child, "values")
                precio = float(str(precio_str).replace(",", ""))
                cantidad = int(cantidad)
                subtotal = float(str(subtotal_str).replace(",", ""))
                total += subtotal
                items.append((producto, precio, cantidad, subtotal))

            if pago < total:
                messagebox.showwarning("Pago", "El pago es insuficiente")
                return

            cambio = round(pago - total, 2)
            # Guarda cada artículo en la tabla ventas con el número de factura actual
            try:
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                for prod, precio, cantidad, subtotal in items:
                    consulta = "INSERT INTO ventas VALUES (?,?,?,?,?,?)"
                    parametros = (None, self.numero_factura_actual, prod, precio, cantidad, subtotal)
                    c.execute(consulta, parametros)
                    # Reduce el stock en inventario
                    c.execute("UPDATE inventario SET stock = stock - ? WHERE nombre = ?", (cantidad, prod))
                conn.commit()
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo guardar la venta: {e}")
                return

            messagebox.showinfo("Pago", f"Pago aceptado. Cambio: MXN {cambio:.2f}")
            # Limpia la venta actual y prepara la siguiente factura
            for child in self.tree.get_children():
                self.tree.delete(child)
            self.actualizar_total()
            self.numero_factura_actual += 1
            self.mostrar_numero_factura()
            ventana_pago.destroy()

        btn_procesar = Button(ventana_pago, text="Procesar", command=procesar_pago, font="sans 12 bold")
        btn_procesar.pack(pady=10)

    # Abre una ventana que muestra facturas guardadas (lista básica)
    def abrir_ventana_factura(self):
        ventana_facturas = Toplevel(self)
        ventana_facturas.title("Facturas")
        ventana_facturas.geometry("600x400")
        ventana_facturas.config(bg="#FDC32F")

        treFrame = tk.Frame(ventana_facturas, bg="#FDC32F")
        treFrame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        treef = ttk.Treeview(treFrame, columns=("Factura", "Producto", "Precio", "Cantidad", "Subtotal"), show="headings", yscrollcommand=scrol_y.set)
        scrol_y.config(command=treef.yview)

        treef.heading("Factura", text="Factura")
        treef.heading("Producto", text="Producto")
        treef.heading("Precio", text="Precio")
        treef.heading("Cantidad", text="Cantidad")
        treef.heading("Subtotal", text="Subtotal")

        treef.column("Factura", anchor="center")
        treef.column("Producto", anchor="center")
        treef.column("Precio", anchor="center")
        treef.column("Cantidad", anchor="center")
        treef.column("Subtotal", anchor="center")

        treef.pack(expand=True, fill=BOTH)

        # Carga facturas desde la base y las muestra
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT factura, nombre_articulo, valor_articulo, cantidad, subtotal FROM ventas ORDER BY factura DESC")
            rows = c.fetchall()
            conn.close()
            for row in rows:
                treef.insert("", tk.END, values=(row[0], row[1], f"{float(row[2]):.2f}", row[3], f"{float(row[4]):.2f}"))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudieron cargar las facturas: {e}")
