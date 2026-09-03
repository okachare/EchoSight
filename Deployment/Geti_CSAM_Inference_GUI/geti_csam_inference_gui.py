from __future__ import annotations

import csv
import importlib
import importlib.util
import json
import os
import queue
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tkinter import END, BOTH, DISABLED, NORMAL, HORIZONTAL, LEFT, RIGHT, VERTICAL, Y, X, filedialog, messagebox, ttk
import tkinter as tk

import cv2
import numpy as np
from PIL import Image, ImageTk, ImageSequence


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}
BACKGROUND = "#14181d"
PANEL = "#1d232b"
PANEL_LIGHT = "#252d36"
TEXT = "#edf2f7"
MUTED = "#9aa8b6"
ACCENT = "#29b6c7"
SUCCESS = "#39c27f"
WARNING = "#e7ad4b"
DANGER = "#dc6470"


@dataclass
class LoadedFrame:
    source: Path
    frame_number: int
    image_rgb: np.ndarray


@dataclass
class InferenceResult:
    frame: LoadedFrame
    prediction: object | None
    error: str | None = None


class ZoomPanCanvas(tk.Canvas):
    def __init__(self, parent: tk.Misc, **kwargs: object) -> None:
        super().__init__(parent, background="#101419", highlightthickness=0, **kwargs)
        self.source_image: Image.Image | None = None
        self.photo: ImageTk.PhotoImage | None = None
        self.zoom = 1.0
        self._pan_start: tuple[int, int] | None = None
        self.bind("<MouseWheel>", self._on_wheel)
        self.bind("<Button-4>", self._on_wheel)
        self.bind("<Button-5>", self._on_wheel)
        self.bind("<ButtonPress-1>", self._start_pan)
        self.bind("<B1-Motion>", self._pan)
        self.bind("<ButtonRelease-1>", self._stop_pan)
        self.bind("<Configure>", lambda _event: self._render())

    def set_image(self, image_rgb: np.ndarray | None) -> None:
        self.source_image = Image.fromarray(image_rgb) if image_rgb is not None else None
        self.zoom = 1.0
        self.delete("all")
        self._render()

    def _on_wheel(self, event: tk.Event) -> str:
        direction = getattr(event, "delta", 0) or (1 if getattr(event, "num", 0) == 4 else -1)
        self.zoom = min(8.0, max(0.25, self.zoom * (1.15 if direction > 0 else 1 / 1.15)))
        self._render()
        return "break"

    def _start_pan(self, event: tk.Event) -> None:
        self._pan_start = (event.x, event.y)
        self.scan_mark(event.x, event.y)

    def _pan(self, event: tk.Event) -> None:
        if self._pan_start is not None:
            self.scan_dragto(event.x, event.y, gain=1)

    def _stop_pan(self, _event: tk.Event) -> None:
        self._pan_start = None

    def _render(self) -> None:
        self.delete("all")
        if self.source_image is None or self.winfo_width() < 2 or self.winfo_height() < 2:
            return
        image = self.source_image.copy()
        fit = min(self.winfo_width() / image.width, self.winfo_height() / image.height)
        scale = max(0.01, fit * self.zoom)
        size = (max(1, int(image.width * scale)), max(1, int(image.height * scale)))
        image = image.resize(size, Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.create_image(self.winfo_width() // 2, self.winfo_height() // 2, image=self.photo, anchor="center")


class GetiDeployment:
    def __init__(self, deployment_root: Path, device: str = "CPU") -> None:
        self.deployment_root = deployment_root
        self.device = device
        self.model_dir = self._find_model_dir(deployment_root)
        python_dir = self.model_dir.parent / "python"
        if not (python_dir / "demo_package").is_dir():
            raise RuntimeError(f"Geti demo package not found beside model: {python_dir}")
        sys.path.insert(0, str(python_dir))
        package_name = f"_geti_demo_package_{abs(hash(python_dir))}"
        package_init = python_dir / "demo_package" / "__init__.py"
        spec = importlib.util.spec_from_file_location(package_name, package_init, submodule_search_locations=[str(package_init.parent)])
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load Geti demo package from {python_dir}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[package_name] = module
        spec.loader.exec_module(module)
        self.wrapper = module.ModelWrapper(self.model_dir, device=device)
        self.task_type = str(self.wrapper.task_type.value)
        self.labels = self._parse_labels(self.wrapper.labels)
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> dict[str, object]:
        metadata: dict[str, object] = {}
        model_metadata = self.model_dir.parent / "model.json"
        project_metadata = self.deployment_root / "project.json"
        for path in (model_metadata, project_metadata):
            if path.is_file():
                try:
                    loaded = json.loads(path.read_text(encoding="utf-8"))
                    if path.name == "model.json":
                        metadata.update(loaded)
                    else:
                        metadata["project"] = loaded
                except (OSError, json.JSONDecodeError):
                    continue
        metadata["model_size_bytes"] = sum(path.stat().st_size for path in self.model_dir.glob("model.*") if path.is_file())
        return metadata

    @staticmethod
    def _find_model_dir(root: Path) -> Path:
        candidates = [path.parent for path in root.rglob("model.xml") if (path.parent / "config.json").is_file()]
        if not candidates:
            raise RuntimeError("No model.xml and config.json pair was found in the selected folder.")
        return candidates[0]

    @staticmethod
    def _parse_labels(labels: object) -> list[str]:
        if isinstance(labels, str):
            return labels.split()
        if isinstance(labels, dict):
            return [str(value) for value in labels.values()]
        return [str(value) for value in labels] if labels else []

    def infer(self, image_rgb: np.ndarray) -> object:
        return self.wrapper(image_rgb)[0]


class GetiCSAMInferenceGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Geti CSAM Inference")
        self.geometry("1250x800")
        self.minsize(980, 650)
        self.configure(bg=BACKGROUND)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._configure_styles()
        self.deployment: GetiDeployment | None = None
        self.frames: list[LoadedFrame] = []
        self.results: list[InferenceResult] = []
        self.current_result_index = 0
        self.result_queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self.worker: threading.Thread | None = None
        self.cancel_event = threading.Event()
        self.spinner_index = 0
        self.operation_started_at: float | None = None
        self.operation_status = ""
        self.activity_running = False
        self.output_directory: Path | None = None
        self.details: tk.Text | None = None
        self.progress_animation_id: str | None = None
        self._build_ui()
        self.after(100, self._poll_worker)
        self.after(120, self._animate_activity)
        self.after(250, self._auto_load_default_model)

    def _configure_styles(self) -> None:
        self.style.configure("TFrame", background=BACKGROUND)
        self.style.configure("Panel.TFrame", background=PANEL)
        self.style.configure("TLabel", background=BACKGROUND, foreground=TEXT, font=("Segoe UI", 10))
        self.style.configure("Muted.TLabel", background=BACKGROUND, foreground=MUTED, font=("Segoe UI", 9))
        self.style.configure("PanelTitle.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI Semibold", 11))
        self.style.configure("Header.TLabel", background=BACKGROUND, foreground=TEXT, font=("Segoe UI Semibold", 18))
        button_options = {"borderwidth": 2, "relief": "solid", "padding": (12, 8), "font": ("Segoe UI Semibold", 10)}
        self.style.configure("TButton", background=PANEL_LIGHT, foreground=TEXT, **button_options)
        self.style.map("TButton", background=[("pressed", ACCENT), ("active", "#354452"), ("disabled", "#30353b")], foreground=[("pressed", "#081217")])
        self.style.configure("RunAll.TButton", background="#b8e3c2", foreground="#10251a", bordercolor="#6d9f7a", lightcolor="#d9f0de", darkcolor="#6d9f7a", **button_options)
        self.style.map("RunAll.TButton", background=[("active", "#ccebd2"), ("pressed", "#8fc99b"), ("disabled", "#68786d")])
        self.style.configure("RunCurrent.TButton", background="#f2d19b", foreground="#35250d", bordercolor="#b08b45", lightcolor="#fae8c4", darkcolor="#b08b45", **button_options)
        self.style.map("RunCurrent.TButton", background=[("active", "#f7dfb4"), ("pressed", "#dfb96f"), ("disabled", "#817664")])
        self.style.configure("Cancel.TButton", background="#efb0b8", foreground="#3b1017", bordercolor="#b96a75", lightcolor="#f8d3d8", darkcolor="#b96a75", **button_options)
        self.style.map("Cancel.TButton", background=[("active", "#f5c4ca"), ("pressed", "#df8994"), ("disabled", "#80696c")])
        self.style.configure("TNotebook", background=BACKGROUND, borderwidth=0, tabmargins=(0, 0, 0, 0), padding=0)
        self.style.configure("TNotebook.Tab", background=PANEL_LIGHT, foreground=MUTED, padding=(14, 8), font=("Segoe UI Semibold", 10), borderwidth=2, relief="solid")
        self.style.map("TNotebook.Tab", background=[("selected", ACCENT), ("active", "#354452")], foreground=[("selected", "#081217"), ("active", TEXT)], padding=[("selected", (22, 13)), ("!selected", (14, 8))])
        self.style.configure("Horizontal.TProgressbar", troughcolor="#0e1115", background=ACCENT, borderwidth=0, thickness=12)
        self.style.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=TEXT, rowheight=28, borderwidth=0)
        self.style.configure("Treeview.Heading", background=PANEL_LIGHT, foreground=MUTED, font=("Segoe UI Semibold", 9))
        self.style.map("Treeview", background=[("selected", "#2c6873")])

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=X, padx=22, pady=(18, 8))
        title_group = ttk.Frame(header)
        title_group.pack(side=LEFT)
        ttk.Label(title_group, text="Geti CSAM Inference", style="Header.TLabel").pack(anchor="w")
        self.style.configure("AccentLine.TFrame", background=ACCENT)
        ttk.Frame(self, height=2, style="AccentLine.TFrame").pack(fill=X, padx=22, pady=(0, 4))
        activity_group = ttk.Frame(header)
        activity_group.pack(side=RIGHT, pady=4)
        self.activity_label = ttk.Label(activity_group, text="", foreground=ACCENT, background=BACKGROUND, font=("Segoe UI Semibold", 10))
        self.activity_label.pack(side=LEFT, padx=(0, 10))
        self.status_label = ttk.Label(activity_group, text="Ready for a deployment model", style="Muted.TLabel")
        self.status_label.pack(side=LEFT)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=True, padx=16, pady=(0, 16))
        self.notebook.pack_propagate(False)
        self.analyze_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)
        for tab in (self.analyze_tab, self.results_tab):
            tab.configure(width=1200, height=690)
            tab.pack_propagate(False)
        self.notebook.add(self.analyze_tab, text="  Analyze  ")
        self.notebook.add(self.results_tab, text="  Results  ")
        self.notebook.configure(width=1200, height=690)
        self._build_analyze_tab()
        self._build_results_tab()

    def _build_analyze_tab(self) -> None:
        controls = ttk.Frame(self.analyze_tab, style="Panel.TFrame", padding=16)
        controls.pack(fill=X, padx=8, pady=8)
        for column in range(6):
            controls.columnconfigure(column, weight=1 if column == 2 else 0)
        self.load_model_button = ttk.Button(controls, text="Load Model", command=self.load_model)
        self.load_model_button.grid(row=0, column=0, padx=(0, 8), sticky="w")
        self.import_button = ttk.Button(controls, text="Import Images", command=self.import_images)
        self.import_button.grid(row=0, column=1, padx=8, sticky="w")
        self.run_button = ttk.Button(controls, text="Run All", style="RunAll.TButton", command=self.run_all)
        self.run_button.grid(row=0, column=3, padx=8, sticky="e")
        self.run_current_button = ttk.Button(controls, text="Run Current", style="RunCurrent.TButton", command=self.run_current)
        self.run_current_button.grid(row=0, column=4, padx=8, sticky="e")
        self.cancel_button = ttk.Button(controls, text="Cancel", style="Cancel.TButton", command=self.cancel_run, state=DISABLED)
        self.cancel_button.grid(row=0, column=5, padx=(8, 0), sticky="e")
        self.model_info = tk.Text(controls, height=7, bg=PANEL, fg=TEXT, relief="flat", wrap="char", font=("Segoe UI", 9), state=DISABLED)
        self.model_info.grid(row=1, column=0, columnspan=6, sticky="ew", pady=(14, 0))
        self._set_model_info("No model loaded")

        body = ttk.Frame(self.analyze_tab)
        body.pack(fill=BOTH, expand=True, padx=8, pady=(0, 8))
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=3)
        body.rowconfigure(0, weight=1)
        file_panel = ttk.Frame(body, style="Panel.TFrame", padding=12)
        file_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(file_panel, text="Loaded images", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 8))
        self.image_list = tk.Listbox(file_panel, bg=PANEL, fg=TEXT, selectbackground="#2c6873", selectforeground=TEXT, relief="flat", highlightthickness=0, font=("Segoe UI", 9))
        self.image_list.pack(side=LEFT, fill=BOTH, expand=True)
        image_scroll = ttk.Scrollbar(file_panel, orient=VERTICAL, command=self.image_list.yview)
        image_scroll.pack(side=RIGHT, fill=Y)
        self.image_list.configure(yscrollcommand=image_scroll.set)
        self.image_list.bind("<<ListboxSelect>>", self._on_image_selected)

        preview_panel = ttk.Frame(body, style="Panel.TFrame", padding=12)
        preview_panel.grid(row=0, column=1, sticky="nsew")
        ttk.Label(preview_panel, text="Preview", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 8))
        self.preview_canvas = ZoomPanCanvas(preview_panel)
        self.preview_canvas.pack(fill=BOTH, expand=True)
        self.preview_hint = ttk.Label(preview_panel, text="Import an image or TIFF to begin", style="Muted.TLabel")
        self.preview_hint.place(relx=0.5, rely=0.5, anchor="center")
        self.progress = ttk.Progressbar(preview_panel, mode="determinate", style="Horizontal.TProgressbar")
        self.progress.pack(fill=X, pady=(12, 4))
        self.progress_label = ttk.Label(preview_panel, text="0 / 0", style="Muted.TLabel")
        self.progress_label.pack(anchor="e")

    def _build_results_tab(self) -> None:
        toolbar = ttk.Frame(self.results_tab, style="Panel.TFrame", padding=12)
        toolbar.pack(fill=X, padx=8, pady=8)
        ttk.Label(toolbar, text="Confidence", style="PanelTitle.TLabel").pack(side=LEFT, padx=(0, 8))
        self.threshold = tk.DoubleVar(value=10.0)
        self.threshold_scale = ttk.Scale(toolbar, from_=1.0, to=100.0, variable=self.threshold, command=self._on_threshold_changed)
        self.threshold_scale.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        self.threshold_value = ttk.Label(toolbar, text="10%", style="Muted.TLabel")
        self.threshold_value.pack(side=LEFT, padx=(0, 18))
        self.hide_no_object = tk.BooleanVar(value=True)
        ttk.Checkbutton(toolbar, text="Hide No_object", variable=self.hide_no_object, command=self._refresh_result).pack(side=LEFT, padx=8)
        self.show_labels = tk.BooleanVar(value=True)
        ttk.Checkbutton(toolbar, text="Show labels", variable=self.show_labels, command=self._refresh_result).pack(side=LEFT, padx=8)
        ttk.Button(toolbar, text="Export Current", command=self.export_current).pack(side=LEFT, padx=8)
        ttk.Button(toolbar, text="Export Selected", command=self.export_selected).pack(side=LEFT, padx=8)
        ttk.Button(toolbar, text="Export All", command=self.export_all).pack(side=LEFT, padx=(8, 0))

        content = ttk.Frame(self.results_tab)
        content.pack(fill=BOTH, expand=True, padx=8, pady=(0, 8))
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=3)
        content.columnconfigure(2, weight=1)
        content.rowconfigure(0, weight=1)
        nav_panel = ttk.Frame(content, style="Panel.TFrame", padding=10)
        nav_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(nav_panel, text="Frame / highest score", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 8))
        self.result_list = tk.Listbox(nav_panel, selectmode="extended", bg=PANEL, fg=TEXT, selectbackground="#2c6873", selectforeground=TEXT, relief="flat", highlightthickness=0, font=("Consolas", 9))
        self.result_list.pack(fill=BOTH, expand=True)
        self.result_list.bind("<<ListboxSelect>>", self._on_result_selected)
        view_panel = ttk.Frame(content, style="Panel.TFrame", padding=12)
        view_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 8))
        self.result_canvas = ZoomPanCanvas(view_panel)
        self.result_canvas.pack(fill=BOTH, expand=True)
        self.result_hint = ttk.Label(view_panel, text="Run inference to see results", style="Muted.TLabel")
        self.result_hint.place(relx=0.5, rely=0.5, anchor="center")
        buttons = ttk.Frame(view_panel, style="Panel.TFrame")
        buttons.pack(fill=X, pady=(10, 0))
        ttk.Button(buttons, text="Previous", command=self.previous_result).pack(side=LEFT)
        ttk.Button(buttons, text="Next", command=self.next_result).pack(side=RIGHT)
        detail_panel = ttk.Frame(content, style="Panel.TFrame", padding=12)
        detail_panel.grid(row=0, column=2, sticky="nsew")
        ttk.Label(detail_panel, text="Detection details", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 8))
        self.details = tk.Text(detail_panel, bg=PANEL, fg=TEXT, insertbackground=TEXT, relief="flat", wrap="word", font=("Consolas", 9), state=DISABLED)
        self.details.pack(fill=BOTH, expand=True)

    def load_model(self) -> None:
        folder = filedialog.askdirectory(title="Select Geti deployment parent folder")
        if not folder:
            return
        self._set_busy(True)
        self.status_label.configure(text="Loading model...")
        self._start_activity("Loading model")
        threading.Thread(target=self._load_model_worker, args=(Path(folder),), daemon=True).start()

    def _auto_load_default_model(self) -> None:
        gui_root = Path(__file__).resolve().parent
        candidates = [
            Path(os.environ["GETI_DEFAULT_DEPLOYMENT"]) if os.environ.get("GETI_DEFAULT_DEPLOYMENT") else None,
            gui_root.parent / "Test_Run_Detect",
            gui_root / "portable" / "deployment",
        ]
        deployment_root = next((path for path in candidates if path and path.is_dir()), None)
        if deployment_root is None:
            self.status_label.configure(text="Ready - select a deployment model")
            return
        self._set_busy(True)
        self.status_label.configure(text="Loading default model...")
        self._start_activity("Loading model")
        threading.Thread(target=self._load_model_worker, args=(deployment_root,), daemon=True).start()

    def _load_model_worker(self, folder: Path) -> None:
        try:
            deployment = GetiDeployment(folder)
            self.result_queue.put(("model", deployment))
        except Exception as error:
            self.result_queue.put(("error", f"Model load failed: {error}"))

    def import_images(self) -> None:
        paths = filedialog.askopenfilenames(title="Select images or TIFF files", filetypes=[("Supported images", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp"), ("All files", "*.*")])
        if not paths:
            return
        self._set_busy(True)
        self.status_label.configure(text="Loading images...")
        self._start_activity("Loading images")
        threading.Thread(target=self._import_worker, args=(paths,), daemon=True).start()

    def _import_worker(self, paths: tuple[str, ...]) -> None:
        loaded_frames: list[LoadedFrame] = []
        errors: list[str] = []
        for path_text in paths:
            path = Path(path_text)
            try:
                loaded_frames.extend(
                    self._load_frames(
                        path,
                        on_frame=lambda index, total, source: self.result_queue.put(
                            ("import_progress", (index, total, source))
                        ),
                    )
                )
            except Exception as error:
                errors.append(f"{path.name}: {error}")
        self.result_queue.put(("frames", (loaded_frames, errors)))

    @staticmethod
    def _load_frames(path: Path, on_frame: object | None = None) -> list[LoadedFrame]:
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError("unsupported image format")
        with Image.open(path) as image:
            frames = []
            total = int(getattr(image, "n_frames", 1))
            for index, frame in enumerate(ImageSequence.Iterator(image), start=1):
                rgb = np.array(frame.convert("RGB"))
                frames.append(LoadedFrame(path, index, rgb))
                if on_frame is not None:
                    on_frame(index, total, path)
            return frames

    def run_current(self) -> None:
        selection = self.image_list.curselection()
        if self.worker and self.worker.is_alive():
            self.status_label.configure(text="An inference run is already active")
            return
        if not self.deployment or not selection:
            messagebox.showinfo("Ready check", "Load a model and import an image first.")
            return
        self._start_inference([self.frames[selection[0]]])

    def run_all(self) -> None:
        if self.worker and self.worker.is_alive():
            self.status_label.configure(text="Run All is already active")
            return
        if not self.deployment or not self.frames:
            messagebox.showinfo("Ready check", "Load a model and import images first.")
            return
        self._start_inference(self.frames)

    def _start_inference(self, frames: list[LoadedFrame]) -> None:
        if self.worker and self.worker.is_alive():
            return
        self.results.clear()
        self.result_list.delete(0, END)
        self.cancel_event.clear()
        self.progress.configure(value=0, maximum=len(frames))
        self.progress_label.configure(text=f"0 / {len(frames)}")
        self._set_busy(True)
        self.status_label.configure(text=f"Starting inference for {len(frames)} image(s)...")
        self.operation_started_at = time.monotonic()
        self.operation_status = f"Starting inference for {len(frames)} image(s)..."
        self._start_activity("Analyzing")
        self._stop_progress_animation()
        self.progress.configure(mode="determinate", value=0, maximum=max(1, len(frames)))
        self.worker = threading.Thread(target=self._inference_worker, args=(frames,), daemon=True)
        self.worker.start()

    def _inference_worker(self, frames: list[LoadedFrame]) -> None:
        for index, frame in enumerate(frames, start=1):
            if self.cancel_event.is_set():
                break
            self.result_queue.put(("progress", (index, len(frames), frame)))
            try:
                prediction = self.deployment.infer(frame.image_rgb)
                self.result_queue.put(("result", (InferenceResult(frame, prediction), index, len(frames))))
            except Exception as error:
                self.result_queue.put(("result", (InferenceResult(frame, None, str(error)), index, len(frames))))
        self.result_queue.put(("complete", len(frames)))

    def cancel_run(self) -> None:
        self.cancel_event.set()
        self.status_label.configure(text="Cancelled")
        self._stop_activity()
        self._set_busy(False)

    def _poll_worker(self) -> None:
        try:
            while True:
                event, value = self.result_queue.get_nowait()
                if event == "model":
                    self.deployment = value
                    self._set_model_info(self._format_model_info(value))
                    self.status_label.configure(text="Model loaded")
                    self.operation_started_at = None
                    self._stop_activity()
                    self._set_busy(False)
                elif event == "frames":
                    frames, errors = value
                    self.frames = frames
                    self.results.clear()
                    self.image_list.delete(0, END)
                    self.result_list.delete(0, END)
                    for frame in frames:
                        suffix = f" [frame {frame.frame_number}]" if frame.frame_number > 1 else ""
                        self.image_list.insert(END, f"{frame.source.name}{suffix}")
                    if errors:
                        messagebox.showwarning("Import warning", "\n".join(errors))
                    if frames:
                        self.image_list.selection_set(0)
                        self._show_image(frames[0].image_rgb, self.preview_canvas, self.preview_hint)
                    self._stop_progress_animation()
                    self.progress.configure(mode="determinate", value=0, maximum=max(1, len(frames)))
                    self.progress_label.configure(text=f"0 / {len(frames)}")
                    self.status_label.configure(text=f"Loaded {len(frames)} image(s)")
                    self.operation_started_at = None
                    self._stop_activity()
                    self._set_busy(False)
                elif event == "import_progress":
                    index, total, source = value
                    self.operation_status = f"Reading {source.name}, frame {index}/{total}"
                    self.status_label.configure(text=self.operation_status)
                    self._animate_progress(index, total)
                elif event == "progress":
                    index, total, frame = value
                    self.operation_status = f"Analyzing {frame.source.name}, frame {frame.frame_number} ({index}/{total})"
                    self.status_label.configure(text=self.operation_status)
                elif event == "result":
                    result, index, total = value
                    self._animate_progress(index, total)
                    self.results.append(result)
                    self.result_list.insert(END, self._result_list_entry(result))
                    self._highlight_best_result()
                    self.progress_label.configure(text=f"{index} / {total}")
                elif event == "complete":
                    total = value
                    self._animate_progress(len(self.results), max(1, total))
                    if self.results:
                        self.current_result_index = 0
                        self.result_list.selection_set(0)
                        self.notebook.select(self.results_tab)
                        self._refresh_result()
                    if self.cancel_event.is_set():
                        self.status_label.configure(text=f"Inference cancelled after {len(self.results)} image(s)")
                    else:
                        self.status_label.configure(text=f"Inference complete: {len(self.results)} image(s)")
                    self._stop_activity()
                    self._set_busy(False)
                    self.worker = None
                elif event == "error":
                    self.status_label.configure(text="Operation failed")
                    self._stop_activity()
                    self._set_busy(False)
                    messagebox.showerror("Geti CSAM Inference", value)
        except queue.Empty:
            pass
        except Exception as error:
            self._stop_progress_animation()
            self.progress.configure(mode="determinate")
            self.status_label.configure(text="GUI update failed")
            self._stop_activity()
            self._set_busy(False)
            messagebox.showerror("Geti CSAM Inference", f"The results panel could not update:\n{error}")
        self.after(100, self._poll_worker)

    def _set_busy(self, busy: bool) -> None:
        state = DISABLED if busy else NORMAL
        self.load_model_button.configure(state=state)
        self.import_button.configure(state=state)
        self.run_button.configure(state=DISABLED if busy else NORMAL)
        self.run_current_button.configure(state=DISABLED if busy else NORMAL)
        self.cancel_button.configure(state=NORMAL if busy else DISABLED)

    def _stop_progress_animation(self) -> None:
        if self.progress_animation_id is not None:
            try:
                self.after_cancel(self.progress_animation_id)
            except tk.TclError:
                pass
            self.progress_animation_id = None

    def _animate_progress(self, target: int, maximum: int) -> None:
        maximum = max(1, maximum)
        target = min(maximum, max(0, target))
        self.progress.configure(mode="determinate", maximum=maximum)
        current = float(self.progress.cget("value") or 0)
        if current >= target - 0.01:
            self.progress.configure(value=target)
            self.progress_animation_id = None
            return
        self.progress.configure(value=current + max(0.05, (target - current) * 0.25))
        self._stop_progress_animation()
        self.progress_animation_id = self.after(20, lambda: self._animate_progress(target, maximum))

    def _start_activity(self, label: str) -> None:
        self.activity_label.configure(text="|")
        self.activity_running = True
        self.operation_started_at = time.monotonic()
        self.operation_status = self.status_label.cget("text")

    def _stop_activity(self) -> None:
        self.activity_label.configure(text="")
        self.activity_running = False
        self.operation_started_at = None

    def _animate_activity(self) -> None:
        if self.activity_running:
            spinner = ("|", "/", "-", "\\")
            self.spinner_index = (self.spinner_index + 1) % len(spinner)
            self.activity_label.configure(text=spinner[self.spinner_index])
            if self.operation_started_at is not None and self.operation_status:
                elapsed = time.monotonic() - self.operation_started_at
                suffix = "  |  still working" if elapsed >= 15 else ""
                self.status_label.configure(text=f"{self.operation_status}  |  {elapsed:.1f}s{suffix}")
        self.after(120, self._animate_activity)

    @staticmethod
    def _format_model_info(deployment: GetiDeployment) -> str:
        metadata = deployment.metadata
        size_bytes = int(metadata.get("model_size_bytes", 0))
        size_mb = size_bytes / (1024 * 1024)
        model_name = metadata.get("name", deployment.model_dir.name)
        version = metadata.get("version", "unknown")
        created = str(metadata.get("creation_date", "unknown"))
        score = metadata.get("performance", {}).get("score", "unknown") if isinstance(metadata.get("performance"), dict) else "unknown"
        score_text = f"{float(score):.1%}" if isinstance(score, (int, float)) else str(score)
        precision = ", ".join(str(item) for item in metadata.get("precision", [])) or "unknown"
        training_images = metadata.get("training_images", metadata.get("num_images", "not included in deployment metadata"))
        xai_head = "yes" if metadata.get("has_xai_head") else "no"
        optimization = metadata.get("optimization_type", "unknown")
        return (
            f"{model_name}  |  Version {version}  |  {deployment.task_type}  |  Device: {deployment.device}\n"
            f"Labels: {', '.join(deployment.labels)}  |  Precision: {precision}  |  Model size: {size_mb:.2f} MB\n"
            f"Model record date: {created}  |  Geti score: {score_text}  |  Optimization: {optimization}\n"
            f"Training images: {training_images}  |  XAI head: {xai_head}  |  Status: {metadata.get('model_status', 'unknown')}\n"
            f"Source: {deployment.model_dir}"
        )

    def _set_model_info(self, text: str) -> None:
        self.model_info.configure(state=NORMAL)
        self.model_info.delete("1.0", END)
        self.model_info.insert("1.0", text)
        self.model_info.configure(state=DISABLED)

    @staticmethod
    def _result_title(result: InferenceResult) -> str:
        name = result.frame.source.name
        return f"{name} [frame {result.frame.frame_number}]" if result.frame.frame_number > 1 else name

    def _result_list_entry(self, result: InferenceResult) -> str:
        title = self._result_title(result)
        if len(title) > 34:
            title = f"{title[:31]}..."
        score = self._result_confidence(result)
        score_text = f"{score:.1%}" if result.prediction is not None and not result.error else "--"
        return f"{title:<34}  Max {score_text:>6}"

    def _on_image_selected(self, _event: object) -> None:
        selection = self.image_list.curselection()
        if selection:
            self._show_image(self.frames[selection[0]].image_rgb, self.preview_canvas, self.preview_hint)

    def _on_result_selected(self, _event: object) -> None:
        selection = self.result_list.curselection()
        if selection:
            self.current_result_index = selection[0]
            self._refresh_result()

    def previous_result(self) -> None:
        if self.results:
            self.current_result_index = (self.current_result_index - 1) % len(self.results)
            self.result_list.selection_clear(0, END)
            self.result_list.selection_set(self.current_result_index)
            self._refresh_result()

    def next_result(self) -> None:
        if self.results:
            self.current_result_index = (self.current_result_index + 1) % len(self.results)
            self.result_list.selection_clear(0, END)
            self.result_list.selection_set(self.current_result_index)
            self._refresh_result()

    def _refresh_result(self) -> None:
        if not self.results:
            return
        self.threshold_value.configure(text=f"{self.threshold.get():.0f}%")
        result = self.results[self.current_result_index]
        annotated, details = self._render_result(result)
        self._show_image(annotated, self.result_canvas, self.result_hint)
        if self.details is not None:
            self.details.configure(state=NORMAL)
            self.details.delete("1.0", END)
            self.details.insert("1.0", details)
            self.details.configure(state=DISABLED)

    def _highlight_best_result(self) -> None:
        if not self.results:
            return
        best_index = max(range(len(self.results)), key=lambda index: self._result_confidence(self.results[index]))
        for index in range(self.result_list.size()):
            self.result_list.itemconfigure(index, background="#b8e3c2" if index == best_index else PANEL, foreground="#10251a" if index == best_index else TEXT)

    @staticmethod
    def _result_confidence(result: InferenceResult) -> float:
        objects = getattr(result.prediction, "objects", []) if result.prediction is not None else []
        if objects:
            return max((float(item.score) for item in objects), default=0.0)
        anomaly_score = getattr(result.prediction, "pred_score", None) if result.prediction is not None else None
        if anomaly_score is not None:
            return float(anomaly_score)
        scores = np.asarray(getattr(result.prediction, "scores", [])) if result.prediction is not None else np.array([])
        return float(scores.max()) if scores.size else 0.0

    def _on_threshold_changed(self, _value: str) -> None:
        self.threshold_value.configure(text=f"{self.threshold.get():.0f}%")
        self._refresh_result()

    def _render_result(self, result: InferenceResult) -> tuple[np.ndarray, str]:
        image = cv2.cvtColor(result.frame.image_rgb.copy(), cv2.COLOR_RGB2BGR)
        if result.error:
            return result.frame.image_rgb, f"Error\n{result.error}"
        prediction = result.prediction
        anomaly_mask = getattr(prediction, "pred_mask", None)
        anomaly_score = getattr(prediction, "pred_score", None)
        anomaly_label = getattr(prediction, "pred_label", None)
        if anomaly_mask is not None and anomaly_score is not None:
            score = float(anomaly_score)
            mask = np.asarray(anomaly_mask > 0, dtype=np.uint8)
            if mask.shape == image.shape[:2] and score >= self.threshold.get() / 100.0:
                overlay = image.copy()
                overlay[mask.astype(bool)] = (80, 170, 220)
                image = cv2.addWeighted(image, 0.65, overlay, 0.35, 0)
            if self.show_labels.get():
                text = f"{anomaly_label or 'Anomaly'} {score:.1%}"
                cv2.putText(image, text, (8, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (220, 245, 248), 1, cv2.LINE_AA)
            details = [f"Source: {result.frame.source.name}", f"Frame: {result.frame.frame_number}", f"Classification: {anomaly_label or 'unknown'}", f"Score: {score:.1%}", f"Mask shown: {'yes' if score >= self.threshold.get() / 100.0 else 'no'}"]
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "\n".join(details)
        classifications = getattr(prediction, "top_labels", None)
        if classifications:
            lines = [f"Source: {result.frame.source.name}", f"Frame: {result.frame.frame_number}", "Classifications:", ""]
            for index, item in enumerate(classifications, start=1):
                if len(item) >= 3:
                    _, label, score = item[:3]
                else:
                    label, score = item[0], item[1]
                score = float(score)
                lines.append(f"{index}. {label}: {score:.1%}")
                if self.show_labels.get():
                    text = f"{label} {score:.1%}"
                    cv2.putText(image, text, (8, 28 + index * 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (220, 245, 248), 1, cv2.LINE_AA)
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "\n".join(lines)
        objects = getattr(prediction, "objects", None)
        masks = getattr(prediction, "masks", None)
        if masks is not None:
            mask_array = np.asarray(masks)
            if mask_array.ndim == 3:
                overlay = image.copy()
                for mask in mask_array:
                    binary_mask = np.asarray(mask > 0, dtype=np.uint8)
                    if binary_mask.shape == image.shape[:2]:
                        overlay[binary_mask.astype(bool)] = (80, 170, 220)
                image = cv2.addWeighted(image, 0.65, overlay, 0.35, 0)
        if objects is not None:
            detections = [
                (
                    (item.xmin, item.ymin, item.xmax, item.ymax),
                    item.score,
                    item.str_label,
                )
                for item in objects
            ]
        else:
            boxes = np.asarray(getattr(prediction, "bboxes", []))
            scores = np.asarray(getattr(prediction, "scores", []))
            labels = list(getattr(prediction, "label_names", []))
            if not labels:
                numeric = np.asarray(getattr(prediction, "labels", []))
                labels = [self.deployment.labels[int(item)] if self.deployment and int(item) < len(self.deployment.labels) else str(item) for item in numeric]
            detections = zip(boxes, scores, labels)
        detections = list(detections)
        lines = [f"Source: {result.frame.source.name}", f"Frame: {result.frame.frame_number}", f"Detections: {len(detections)}", ""]
        visible = 0
        for box, score, label in detections:
            score = float(score)
            if score < self.threshold.get() / 100.0 or (self.hide_no_object.get() and str(label).lower() == "no_object"):
                continue
            visible += 1
            x_min, y_min, x_max, y_max = [int(value) for value in box]
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (41, 182, 199), 2)
            text = f"{label} {score:.1%}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            thickness = 1
            (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
            image_height, image_width = image.shape[:2]
            label_width = text_width + 8
            label_height = text_height + baseline + 8
            label_x = min(max(0, x_min), max(0, image_width - label_width))
            label_y = y_min - label_height if y_min >= label_height else min(image_height - label_height, y_max)
            label_y = max(0, label_y)
            text_x = label_x + 4
            text_y = label_y + text_height + 4
            if getattr(self, "show_labels", None) is None or self.show_labels.get():
                cv2.rectangle(image, (label_x, label_y), (label_x + label_width, label_y + label_height), (20, 24, 29), -1)
                cv2.putText(image, text, (text_x, text_y), font, font_scale, (220, 245, 248), thickness, cv2.LINE_AA)
            lines.append(f"{visible}. {label}: {score:.1%}\n   box: ({x_min}, {y_min}) - ({x_max}, {y_max})")
        lines[2] = f"Detections shown: {visible}"
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "\n".join(lines)

    def _show_image(self, image_rgb: np.ndarray, target: ZoomPanCanvas, hint: ttk.Label) -> None:
        hint.place_forget()
        target.set_image(image_rgb)

    def export_current(self) -> None:
        if not self.results:
            return
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self._export_results(Path(folder), self.results[self.current_result_index:self.current_result_index + 1])

    def export_selected(self) -> None:
        selected = self.result_list.curselection()
        if not selected:
            messagebox.showinfo("Select results", "Select one or more result images first.")
            return
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self._export_results(Path(folder), [self.results[index] for index in selected])

    def export_all(self) -> None:
        if not self.results:
            return
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self._export_results(Path(folder), self.results)

    def _export_results(self, folder: Path, results: list[InferenceResult]) -> None:
        run_folder = folder / datetime.now().strftime("run_%Y%m%d_%H%M%S")
        image_folder = run_folder / "annotated"
        image_folder.mkdir(parents=True, exist_ok=True)
        rows = []
        for index, result in enumerate(results, start=1):
            annotated, details = self._render_result(result)
            output_path = image_folder / f"{result.frame.source.stem}_frame_{result.frame.frame_number:04d}.png"
            Image.fromarray(annotated).save(output_path)
            rows.append({"source_file": str(result.frame.source), "frame_number": result.frame.frame_number, "output_file": str(output_path), "details": details.replace("\n", " | ")})
        with (run_folder / "results.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        session = {"model": str(self.deployment.model_dir) if self.deployment else None, "device": self.deployment.device if self.deployment else None, "threshold_percent": self.threshold.get(), "show_labels": self.show_labels.get(), "results": len(results), "created": datetime.now().isoformat()}
        (run_folder / "session.json").write_text(json.dumps(session, indent=2), encoding="utf-8")
        messagebox.showinfo("Export complete", f"Saved results to:\n{run_folder}")


if __name__ == "__main__":
    app = GetiCSAMInferenceGUI()
    app.mainloop()
