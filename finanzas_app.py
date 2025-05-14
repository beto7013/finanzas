import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Financiera")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        # Establecer conexión con la base de datos
        self.conn = sqlite3.connect('finanzas.db')
        self.create_tables()
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), background='#f0f0f0')
        self.style.configure('Option.TButton', font=('Arial', 11), width=20, padding=10)
        
        # Crear widgets
        self.create_widgets()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                monto REAL NOT NULL,
                fecha TEXT NOT NULL,
                descripcion TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                tipo TEXT NOT NULL
            )
        ''')
        
        # Insertar categorías predeterminadas si no existen
        default_categories = [
            ('Alimentos', 'Gasto'),
            ('Transporte', 'Gasto'),
            ('Vivienda', 'Gasto'),
            ('Entretenimiento', 'Gasto'),
            ('Salario', 'Ingreso'),
            ('Freelance', 'Ingreso'),
            ('Inversiones', 'Ingreso')
        ]
        
        for category in default_categories:
            try:
                cursor.execute('INSERT INTO categorias (nombre, tipo) VALUES (?, ?)', category)
            except sqlite3.IntegrityError:
                pass
        
        self.conn.commit()
    
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame para el título
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título
        self.title_label = ttk.Label(
            self.header_frame, 
            text="Sistema de Gestión Financiera", 
            style='Header.TLabel'
        )
        self.title_label.pack()
        
        # Frame para el contenido (opciones y área de trabajo)
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para las opciones (vertical)
        self.options_frame = ttk.Frame(self.content_frame, width=200)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Botones de opciones
        self.option_buttons = []
        options = [
            ("Registrar Transacción", self.show_transaction_form),
            ("Ver Historial", self.show_transaction_history),
            ("Resumen Financiero", self.show_financial_summary),
            ("Gestión de Categorías", self.show_category_management),
            ("Configuración", self.show_settings)
        ]
        
        for text, command in options:
            btn = ttk.Button(
                self.options_frame, 
                text=text, 
                command=command,
                style='Option.TButton'
            )
            btn.pack(fill=tk.X, pady=5)
            self.option_buttons.append(btn)
        
        # Frame para el área de trabajo
        self.work_area = ttk.Frame(self.content_frame)
        self.work_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Mostrar el formulario de transacción por defecto
        self.show_transaction_form()
    
    def clear_work_area(self):
        for widget in self.work_area.winfo_children():
            widget.destroy()
    
    def show_transaction_form(self):
        self.clear_work_area()
        
        # Frame para el formulario
        form_frame = ttk.Frame(self.work_area)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(form_frame, text="Registrar Nueva Transacción", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Tipo de transacción
        ttk.Label(form_frame, text="Tipo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.transaction_type = tk.StringVar(value="Gasto")
        ttk.Radiobutton(form_frame, text="Gasto", variable=self.transaction_type, value="Gasto").grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(form_frame, text="Ingreso", variable=self.transaction_type, value="Ingreso").grid(row=1, column=1, sticky=tk.E)
        
        # Categoría
        ttk.Label(form_frame, text="Categoría:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(form_frame, textvariable=self.category_var)
        self.category_combobox.grid(row=2, column=1, sticky=tk.EW, pady=5)
        self.update_category_combobox()
        
        # Monto
        ttk.Label(form_frame, text="Monto:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
        
        # Fecha
        ttk.Label(form_frame, text="Fecha:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.description_entry = tk.Text(form_frame, height=4, width=30)
        self.description_entry.grid(row=5, column=1, sticky=tk.EW, pady=5)
        
        # Botón de guardar
        save_button = ttk.Button(form_frame, text="Guardar Transacción", command=self.save_transaction)
        save_button.grid(row=6, column=1, sticky=tk.E, pady=20)
        
        # Configurar el peso de las columnas
        form_frame.columnconfigure(1, weight=1)
    
    def update_category_combobox(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT nombre FROM categorias WHERE tipo = ? ORDER BY nombre', (self.transaction_type.get(),))
        categories = [row[0] for row in cursor.fetchall()]
        self.category_combobox['values'] = categories
        if categories:
            self.category_var.set(categories[0])
    
    def save_transaction(self):
        tipo = self.transaction_type.get()
        categoria = self.category_var.get()
        monto = self.amount_entry.get()
        fecha = self.date_entry.get()
        descripcion = self.description_entry.get("1.0", tk.END).strip()
        
        # Validaciones
        if not categoria:
            messagebox.showerror("Error", "Por favor seleccione una categoría")
            return
        
        try:
            monto = float(monto)
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un monto válido (número positivo)")
            return
        
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese una fecha válida en formato YYYY-MM-DD")
            return
        
        # Guardar en la base de datos
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO transacciones (tipo, categoria, monto, fecha, descripcion)
            VALUES (?, ?, ?, ?, ?)
        ''', (tipo, categoria, monto, fecha, descripcion))
        
        self.conn.commit()
        messagebox.showinfo("Éxito", "Transacción registrada correctamente")
        
        # Limpiar campos (excepto fecha y tipo)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete("1.0", tk.END)
    
    def show_transaction_history(self):
        self.clear_work_area()
        
        # Frame principal para el historial
        history_frame = ttk.Frame(self.work_area)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(history_frame, text="Historial de Transacciones", style='Header.TLabel').pack(pady=(0, 20))
        
        # Filtros
        filter_frame = ttk.Frame(history_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filtrar por:").pack(side=tk.LEFT, padx=5)
        
        self.filter_type = tk.StringVar(value="Todos")
        ttk.Radiobutton(filter_frame, text="Todos", variable=self.filter_type, value="Todos", 
                       command=self.update_transaction_table).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Gastos", variable=self.filter_type, value="Gasto", 
                       command=self.update_transaction_table).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Ingresos", variable=self.filter_type, value="Ingreso", 
                       command=self.update_transaction_table).pack(side=tk.LEFT, padx=5)
        
        # Tabla de transacciones
        columns = ("#", "Fecha", "Tipo", "Categoría", "Monto", "Descripción")
        self.transaction_tree = ttk.Treeview(
            history_frame, 
            columns=columns, 
            show="headings",
            selectmode="extended"
        )
        
        for col in columns:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.transaction_tree.column("#", width=50)
        self.transaction_tree.column("Descripción", width=200)
        self.transaction_tree.column("Monto", anchor=tk.E)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        button_frame = ttk.Frame(history_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Eliminar Seleccionados", command=self.delete_selected_transactions).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Exportar a CSV", command=self.export_to_csv).pack(side=tk.RIGHT, padx=5)
        
        # Actualizar la tabla
        self.update_transaction_table()
    
    def update_transaction_table(self):
        # Limpiar tabla
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        # Obtener transacciones según filtro
        cursor = self.conn.cursor()
        filter_value = self.filter_type.get()
        
        if filter_value == "Todos":
            cursor.execute('''
                SELECT id, fecha, tipo, categoria, monto, descripcion 
                FROM transacciones 
                ORDER BY fecha DESC
            ''')
        else:
            cursor.execute('''
                SELECT id, fecha, tipo, categoria, monto, descripcion 
                FROM transacciones 
                WHERE tipo = ?
                ORDER BY fecha DESC
            ''', (filter_value,))
        
        transactions = cursor.fetchall()
        
        # Insertar datos en la tabla
        for i, transaction in enumerate(transactions, 1):
            trans_id, fecha, tipo, categoria, monto, descripcion = transaction
            monto_str = f"${monto:,.2f}"
            
            # Cambiar color según el tipo
            tags = ('ingreso',) if tipo == "Ingreso" else ('gasto',)
            
            self.transaction_tree.insert(
                "", tk.END, 
                values=(i, fecha, tipo, categoria, monto_str, descripcion),
                tags=tags
            )
        
        # Configurar estilos para las filas
        self.transaction_tree.tag_configure('ingreso', foreground='green')
        self.transaction_tree.tag_configure('gasto', foreground='red')
    
    def delete_selected_transactions(self):
        selected_items = self.transaction_tree.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "Por favor seleccione al menos una transacción")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar", 
            f"¿Está seguro que desea eliminar las {len(selected_items)} transacciones seleccionadas?"
        )
        
        if not confirm:
            return
        
        cursor = self.conn.cursor()
        deleted_count = 0
        
        for item in selected_items:
            item_id = self.transaction_tree.item(item)['values'][0]
            cursor.execute('DELETE FROM transacciones WHERE id = ?', (item_id,))
            deleted_count += cursor.rowcount
        
        self.conn.commit()
        
        if deleted_count > 0:
            messagebox.showinfo("Éxito", f"Se eliminaron {deleted_count} transacciones")
            self.update_transaction_table()
        else:
            messagebox.showerror("Error", "No se pudo eliminar ninguna transacción")
    
    def export_to_csv(self):
        # Implementación básica - en una aplicación real, esto generaría un archivo CSV
        messagebox.showinfo("Información", "Esta función exportaría los datos a CSV en una implementación completa")
    
    def show_financial_summary(self):
        self.clear_work_area()
        
        # Frame principal para el resumen
        summary_frame = ttk.Frame(self.work_area)
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(summary_frame, text="Resumen Financiero", style='Header.TLabel').pack(pady=(0, 20))
        
        # Obtener datos de resumen
        cursor = self.conn.cursor()
        
        # Ingresos totales
        cursor.execute('SELECT SUM(monto) FROM transacciones WHERE tipo = "Ingreso"')
        total_income = cursor.fetchone()[0] or 0
        
        # Gastos totales
        cursor.execute('SELECT SUM(monto) FROM transacciones WHERE tipo = "Gasto"')
        total_expenses = cursor.fetchone()[0] or 0
        
        # Balance
        balance = total_income - total_expenses
        
        # Mostrar métricas principales
        metrics_frame = ttk.Frame(summary_frame)
        metrics_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(metrics_frame, text=f"Ingresos Totales: ${total_income:,.2f}", 
                 font=('Arial', 12), foreground='green').pack(side=tk.LEFT, padx=10)
        ttk.Label(metrics_frame, text=f"Gastos Totales: ${total_expenses:,.2f}", 
                 font=('Arial', 12), foreground='red').pack(side=tk.LEFT, padx=10)
        ttk.Label(metrics_frame, text=f"Balance: ${balance:,.2f}", 
                 font=('Arial', 12, 'bold'), 
                 foreground='blue' if balance >= 0 else 'red').pack(side=tk.LEFT, padx=10)
        
        # Gráfico de gastos por categoría (simulado con texto)
        chart_frame = ttk.Frame(summary_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(chart_frame, text="Distribución de Gastos por Categoría", 
                 font=('Arial', 11, 'bold')).pack(pady=(0, 10))
        
        cursor.execute('''
            SELECT categoria, SUM(monto) 
            FROM transacciones 
            WHERE tipo = "Gasto" 
            GROUP BY categoria 
            ORDER BY SUM(monto) DESC
        ''')
        expenses_by_category = cursor.fetchall()
        
        for category, amount in expenses_by_category:
            category_frame = ttk.Frame(chart_frame)
            category_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(category_frame, text=category, width=20).pack(side=tk.LEFT)
            
            # Barra de progreso simulada
            max_amount = max(row[1] for row in expenses_by_category)
            bar_length = int(300 * (amount / max_amount))
            
            canvas = tk.Canvas(category_frame, height=20, width=300, bg='white', highlightthickness=0)
            canvas.pack(side=tk.LEFT, padx=5)
            canvas.create_rectangle(0, 0, bar_length, 20, fill='#FF6B6B', outline='')
            
            ttk.Label(category_frame, text=f"${amount:,.2f}").pack(side=tk.LEFT)
    
    def show_category_management(self):
        self.clear_work_area()
        
        # Frame principal para gestión de categorías
        category_frame = ttk.Frame(self.work_area)
        category_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(category_frame, text="Gestión de Categorías", style='Header.TLabel').pack(pady=(0, 20))
        
        # Frame para formulario de nueva categoría
        new_cat_frame = ttk.Frame(category_frame)
        new_cat_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(new_cat_frame, text="Nueva Categoría:").pack(side=tk.LEFT, padx=5)
        
        self.new_category_name = ttk.Entry(new_cat_frame, width=20)
        self.new_category_name.pack(side=tk.LEFT, padx=5)
        
        self.new_category_type = tk.StringVar(value="Gasto")
        ttk.Radiobutton(new_cat_frame, text="Gasto", variable=self.new_category_type, value="Gasto").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(new_cat_frame, text="Ingreso", variable=self.new_category_type, value="Ingreso").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(new_cat_frame, text="Agregar", command=self.add_new_category).pack(side=tk.LEFT, padx=10)
        
        # Tabla de categorías existentes
        columns = ("#", "Nombre", "Tipo", "Acciones")
        self.category_tree = ttk.Treeview(
            category_frame, 
            columns=columns, 
            show="headings",
            selectmode="browse"
        )
        
        for col in columns:
            self.category_tree.heading(col, text=col)
            self.category_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.category_tree.column("#", width=50)
        self.category_tree.column("Acciones", width=100)
        
        scrollbar = ttk.Scrollbar(category_frame, orient=tk.VERTICAL, command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=scrollbar.set)
        
        self.category_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Actualizar tabla de categorías
        self.update_category_table()
    
    def update_category_table(self):
        # Limpiar tabla
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
        
        # Obtener categorías
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, nombre, tipo FROM categorias ORDER BY tipo, nombre')
        categories = cursor.fetchall()
        
        # Insertar datos en la tabla
        for i, (cat_id, nombre, tipo) in enumerate(categories, 1):
            self.category_tree.insert(
                "", tk.END, 
                values=(i, nombre, tipo, "Eliminar"),
                iid=cat_id
            )
    
    def add_new_category(self):
        name = self.new_category_name.get().strip()
        cat_type = self.new_category_type.get()
        
        if not name:
            messagebox.showerror("Error", "Por favor ingrese un nombre para la categoría")
            return
        
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO categorias (nombre, tipo) VALUES (?, ?)', (name, cat_type))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Categoría agregada correctamente")
            self.new_category_name.delete(0, tk.END)
            self.update_category_table()
            self.update_category_combobox()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe una categoría con ese nombre")
    
    def delete_category(self, category_id):
        # Primero verificar si hay transacciones asociadas
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM transacciones WHERE categoria = (SELECT nombre FROM categorias WHERE id = ?)', (category_id,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            messagebox.showerror("Error", "No se puede eliminar esta categoría porque tiene transacciones asociadas")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar", 
            "¿Está seguro que desea eliminar esta categoría?"
        )
        
        if confirm:
            cursor.execute('DELETE FROM categorias WHERE id = ?', (category_id,))
            self.conn.commit()
            self.update_category_table()
            self.update_category_combobox()
            messagebox.showinfo("Éxito", "Categoría eliminada correctamente")
    
    def show_settings(self):
        self.clear_work_area()
        
        # Frame para configuración
        settings_frame = ttk.Frame(self.work_area)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(settings_frame, text="Configuración", style='Header.TLabel').pack(pady=(0, 20))
        
        # Opciones de configuración (simuladas)
        ttk.Label(settings_frame, text="Esta es la sección de configuración").pack()
        ttk.Label(settings_frame, text="En una implementación completa aquí habría opciones como:").pack(pady=10)
        ttk.Label(settings_frame, text="- Moneda predeterminada").pack()
        ttk.Label(settings_frame, text="- Formato de fecha").pack()
        ttk.Label(settings_frame, text="- Copias de seguridad automáticas").pack()
        ttk.Label(settings_frame, text="- Tema de la interfaz").pack()
        
        ttk.Button(settings_frame, text="Exportar Base de Datos", command=self.export_database).pack(pady=20)
        ttk.Button(settings_frame, text="Importar Base de Datos", command=self.import_database).pack()
    
    def export_database(self):
        messagebox.showinfo("Información", "Esta función exportaría la base de datos en una implementación completa")
    
    def import_database(self):
        messagebox.showinfo("Información", "Esta función importaría una base de datos en una implementación completa")
    
    def on_closing(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
