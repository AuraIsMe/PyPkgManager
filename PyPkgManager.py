import tkinter as tk
from tkinter import messagebox
import subprocess
import pkg_resources

class PackageManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Package Manager")
        self.geometry("600x400")
        self.installed_packages_list = []
        self.create_widgets()
        self.list_installed_packages()

    def create_widgets(self):
        self.search_bar = tk.Entry(self, width=50)
        self.search_bar.pack(pady=10)
        self.search_bar.bind("<KeyRelease>", self.filter_packages)

        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def list_installed_packages(self):
        installed_packages = pkg_resources.working_set
        self.installed_packages_list = sorted([i.key for i in installed_packages])
        self.display_packages()

    def display_packages(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for package in self.installed_packages_list:
            package_frame = tk.Frame(self.scrollable_frame)
            package_label = tk.Label(package_frame, text=package, width=40, anchor='w')
            package_label.pack(side=tk.LEFT)

            uninstall_button = tk.Button(package_frame, text="Uninstall", command=lambda p=package: self.uninstall_package(p))
            uninstall_button.pack(side=tk.LEFT)

            reinstall_button = tk.Button(package_frame, text="Reinstall", command=lambda p=package: self.reinstall_package(p))
            reinstall_button.pack(side=tk.LEFT)

            if not self.is_package_installed(package):
                uninstall_button.config(state=tk.DISABLED)
            else:
                reinstall_button.config(state=tk.DISABLED)

            package_frame.pack(fill=tk.X, padx=5, pady=2)

    def filter_packages(self, event):
        search_term = self.search_bar.get().lower()
        filtered_packages_list = [pkg for pkg in self.installed_packages_list if search_term in pkg.lower()]
        self.display_packages(filtered_packages_list)

    def display_packages(self, packages=None):
        if packages is None:
            packages = self.installed_packages_list
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for package in packages:
            package_frame = tk.Frame(self.scrollable_frame)
            package_label = tk.Label(package_frame, text=package, width=40, anchor='w')
            package_label.pack(side=tk.LEFT)

            uninstall_button = tk.Button(package_frame, text="Uninstall", command=lambda p=package: self.uninstall_package(p))
            uninstall_button.pack(side=tk.LEFT)

            reinstall_button = tk.Button(package_frame, text="Reinstall", command=lambda p=package: self.reinstall_package(p))
            reinstall_button.pack(side=tk.LEFT)

            if not self.is_package_installed(package):
                uninstall_button.config(state=tk.DISABLED)
            else:
                reinstall_button.config(state=tk.DISABLED)

            package_frame.pack(fill=tk.X, padx=5, pady=2)

    def is_package_installed(self, package_name):
        installed_packages = [pkg.key for pkg in pkg_resources.working_set]
        return package_name in installed_packages

    def uninstall_package(self, package):
        package_name = package
        response = messagebox.askyesno("Uninstall Package", f"Are you sure you want to uninstall {package_name}?")
        if response:
            subprocess.run(['pip', 'uninstall', '-y', package_name])
            self.update_package_buttons(package_name, uninstall=True)

    def reinstall_package(self, package):
        package_name = package
        response = messagebox.askyesno("Reinstall Package", f"Are you sure you want to reinstall {package_name}?")
        if response:
            subprocess.run(['pip', 'install', package_name])
            self.update_package_buttons(package_name, uninstall=False)

    def update_package_buttons(self, package_name, uninstall):
        for child in self.scrollable_frame.winfo_children():
            label = child.winfo_children()[0]
            if label.cget("text").startswith(package_name):
                uninstall_button = child.winfo_children()[1]
                reinstall_button = child.winfo_children()[2]
                if uninstall:
                    uninstall_button.config(state=tk.DISABLED)
                    reinstall_button.config(state=tk.NORMAL)
                else:
                    uninstall_button.config(state=tk.NORMAL)
                    reinstall_button.config(state=tk.DISABLED)
                break

if __name__ == "__main__":
    app = PackageManager()
    app.mainloop()
