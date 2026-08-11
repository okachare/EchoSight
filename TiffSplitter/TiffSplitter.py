import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageSequence, UnidentifiedImageError


OUTPUT_FORMATS = {
    "PNG": "png",
    "JPEG": "jpg",
    "BMP": "bmp",
    "TIFF": "tif",
    "WEBP": "webp",
}


class TiffSplitterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("TIFF Splitter - Offline Tool")
        self.root.geometry("680x420")
        self.root.minsize(640, 390)

        self.input_path_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.format_var = tk.StringVar(value="PNG")
        self.jpeg_quality_var = tk.IntVar(value=95)
        self.status_var = tk.StringVar(value="Ready")

        self._build_ui()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=14)
        main.pack(fill=tk.BOTH, expand=True)

        input_label = ttk.Label(main, text="Input TIFF file")
        input_label.grid(row=0, column=0, sticky="w")

        input_entry = ttk.Entry(main, textvariable=self.input_path_var)
        input_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(4, 10))

        input_btn = ttk.Button(main, text="Browse", command=self.choose_input)
        input_btn.grid(row=1, column=1, sticky="ew", pady=(4, 10))

        output_label = ttk.Label(main, text="Output folder")
        output_label.grid(row=2, column=0, sticky="w")

        output_entry = ttk.Entry(main, textvariable=self.output_dir_var)
        output_entry.grid(row=3, column=0, sticky="ew", padx=(0, 8), pady=(4, 10))

        output_btn = ttk.Button(main, text="Browse", command=self.choose_output)
        output_btn.grid(row=3, column=1, sticky="ew", pady=(4, 10))

        format_label = ttk.Label(main, text="Output image format")
        format_label.grid(row=4, column=0, sticky="w")

        format_box = ttk.Combobox(
            main,
            textvariable=self.format_var,
            values=list(OUTPUT_FORMATS.keys()),
            state="readonly",
        )
        format_box.grid(row=5, column=0, sticky="w", pady=(4, 10))
        format_box.bind("<<ComboboxSelected>>", lambda _: self._update_jpeg_quality_visibility())

        self.quality_frame = ttk.Frame(main)
        self.quality_frame.grid(row=6, column=0, sticky="ew", pady=(0, 12))

        quality_label = ttk.Label(self.quality_frame, text="JPEG quality")
        quality_label.grid(row=0, column=0, sticky="w", padx=(0, 8))

        quality_spin = ttk.Spinbox(
            self.quality_frame,
            from_=1,
            to=100,
            textvariable=self.jpeg_quality_var,
            width=8,
        )
        quality_spin.grid(row=0, column=1, sticky="w")

        self.split_button = ttk.Button(main, text="Split TIFF", command=self.on_split_clicked)
        self.split_button.grid(row=7, column=0, sticky="w")

        self.progress = ttk.Progressbar(main, orient="horizontal", mode="determinate")
        self.progress.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(14, 8))

        self.status_label = ttk.Label(main, textvariable=self.status_var)
        self.status_label.grid(row=9, column=0, columnspan=2, sticky="w")

        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=0)

        self._update_jpeg_quality_visibility()

    def _update_jpeg_quality_visibility(self) -> None:
        if self.format_var.get() == "JPEG":
            self.quality_frame.grid()
        else:
            self.quality_frame.grid_remove()

    def choose_input(self) -> None:
        selected = filedialog.askopenfilename(
            title="Select TIFF image",
            filetypes=[("TIFF files", "*.tif *.tiff"), ("All files", "*.*")],
        )
        if selected:
            self.input_path_var.set(selected)
            if not self.output_dir_var.get():
                self.output_dir_var.set(str(Path(selected).parent))

    def choose_output(self) -> None:
        selected = filedialog.askdirectory(title="Select output folder")
        if selected:
            self.output_dir_var.set(selected)

    def on_split_clicked(self) -> None:
        input_path = self.input_path_var.get().strip().strip('"')
        output_dir = self.output_dir_var.get().strip().strip('"')

        if not input_path:
            messagebox.showerror("Missing input", "Please select an input TIFF file.")
            return

        if not output_dir:
            messagebox.showerror("Missing output", "Please select an output folder.")
            return

        input_file = Path(input_path)
        if not input_file.exists() or not input_file.is_file():
            messagebox.showerror("Invalid input", "Selected input file does not exist.")
            return

        if input_file.suffix.lower() not in {".tif", ".tiff"}:
            messagebox.showerror("Invalid input", "Input must be a .tif or .tiff file.")
            return

        output_folder = Path(output_dir)
        try:
            output_folder.mkdir(parents=True, exist_ok=True)
        except OSError as ex:
            messagebox.showerror("Output error", f"Unable to create output folder.\n\n{ex}")
            return

        quality = self.jpeg_quality_var.get()
        if self.format_var.get() == "JPEG" and not (1 <= quality <= 100):
            messagebox.showerror("Invalid quality", "JPEG quality must be between 1 and 100.")
            return

        self.set_busy(True)
        worker = threading.Thread(
            target=self._split_images_worker,
            args=(input_file, output_folder, self.format_var.get(), quality),
            daemon=True,
        )
        worker.start()

    def set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self.split_button.configure(state=state)
        self.status_var.set("Processing..." if busy else "Ready")

    def _split_images_worker(self, input_file: Path, output_folder: Path, output_format_key: str, jpeg_quality: int) -> None:
        try:
            count = self._split_tiff(input_file, output_folder, output_format_key, jpeg_quality)
            self.root.after(0, lambda: self._on_split_success(count, output_folder))
        except Exception as ex:
            detail = f"{ex}\n\n{traceback.format_exc()}"
            self.root.after(0, lambda: self._on_split_failure(detail))

    def _split_tiff(self, input_file: Path, output_folder: Path, output_format_key: str, jpeg_quality: int) -> int:
        extension = OUTPUT_FORMATS[output_format_key]
        with Image.open(input_file) as source:
            total = getattr(source, "n_frames", 1)
            if total <= 0:
                raise ValueError("No images found in the TIFF file.")

            self.root.after(0, lambda: self._set_progress(0, total))

            base_name = input_file.stem
            for index, frame in enumerate(ImageSequence.Iterator(source), start=1):
                frame_copy = frame.copy()
                save_kwargs = {}

                if output_format_key == "JPEG":
                    if frame_copy.mode not in ("RGB", "L"):
                        frame_copy = frame_copy.convert("RGB")
                    save_kwargs["quality"] = jpeg_quality
                    save_kwargs["optimize"] = True

                out_name = f"{base_name}_{index:03d}.{extension}"
                out_path = output_folder / out_name
                frame_copy.save(out_path, format=output_format_key, **save_kwargs)

                self.root.after(0, lambda i=index, t=total: self._set_progress(i, t))

            return total

    def _set_progress(self, current: int, total: int) -> None:
        self.progress.configure(maximum=total, value=current)
        if total > 0:
            self.status_var.set(f"Processing {current}/{total}...")

    def _on_split_success(self, count: int, output_folder: Path) -> None:
        self.set_busy(False)
        self.progress.configure(value=self.progress.cget("maximum"))
        self.status_var.set(f"Done. Exported {count} images.")
        messagebox.showinfo(
            "Complete",
            f"Successfully exported {count} images.\n\nOutput folder:\n{output_folder}",
        )

    def _on_split_failure(self, detail: str) -> None:
        self.set_busy(False)
        self.progress.configure(value=0)
        self.status_var.set("Failed")
        messagebox.showerror("Split failed", detail)


def main() -> None:
    root = tk.Tk()
    TiffSplitterApp(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except UnidentifiedImageError:
        messagebox.showerror("Invalid image", "The selected file is not a valid TIFF image.")
    except Exception as ex:
        messagebox.showerror("Fatal error", str(ex))
