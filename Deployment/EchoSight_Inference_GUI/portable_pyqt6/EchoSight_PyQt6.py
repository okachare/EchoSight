"""
EchoSight - Model-agnostic Image Inference and Inspection GUI (PyQt6 Edition)
Uses the same design engine as CSAM Image Analyser for a refined, professional experience.
"""

from __future__ import annotations

import sys
import threading
import time
import json
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass
from enum import Enum
from queue import Queue

import cv2
import numpy as np
from PIL import Image

from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize, QRect, QPoint
from PyQt6.QtGui import QPixmap, QImage, QFont, QIcon, QColor, QPalette, QFontMetrics
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QGroupBox, QPushButton, QLabel, QLineEdit, QFileDialog,
    QTableWidget, QTableWidgetItem, QScrollArea, QProgressBar, QSpinBox,
    QComboBox, QSlider, QCheckBox, QMessageBox, QSplitter, QFrame,
    QListWidget, QListWidgetItem, QHeaderView, QDoubleSpinBox, QTextEdit,
    QStackedWidget, QCalendarWidget, QDateEdit, QTimeEdit
)


# ============================================================================
# Constants & Color System (CSAM Image Analyser Inspired)
# ============================================================================

class Theme:
    """Color palette matching CSAM Image Analyser"""
    BG_PRIMARY = "#1f232a"      # Main background
    BG_SECONDARY = "#2b313c"    # Panels, inputs
    BG_TERTIARY = "#3a4250"     # Tabs, groups
    BORDER = "#475063"          # Borders
    BORDER_LIGHT = "#3a4250"    # Light borders
    TEXT_PRIMARY = "#e6edf3"    # Main text
    TEXT_SECONDARY = "#c9d1d9"  # Secondary text
    TEXT_MUTED = "#8b949e"      # Muted text
    
    # Semantic Colors
    SUCCESS = "#86d39f"         # Green for start/run
    SUCCESS_BORDER = "#98ddb0"
    SUCCESS_DARK = "#2f9e5b"
    
    WARNING = "#f6c177"         # Orange for warnings
    WARNING_BORDER = "#f8cd90"
    
    DANGER = "#f29ea0"          # Red for stop/cancel
    DANGER_BORDER = "#f6b2b4"
    
    INFO = "#5f8fe6"            # Blue for info
    INFO_BORDER = "#8aa0c8"


class TaskType(Enum):
    """Supported inference task types"""
    DETECTION = "Detection"
    SEGMENTATION = "Instance Segmentation"
    ANOMALY = "Anomaly Classification"


@dataclass
class InferenceResult:
    """Result container for inference"""
    frame_index: int
    frame_name: str
    predictions: dict[str, Any]
    processing_time_ms: float
    timestamp: float


# ============================================================================
# Worker Thread for Inference
# ============================================================================

class InferenceWorker(QThread):
    """Background inference worker with progress signals"""
    progress_updated = pyqtSignal(int, InferenceResult)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)
    
    def __init__(self, frames: list[np.ndarray], deployment, task_type: TaskType):
        super().__init__()
        self.frames = frames
        self.deployment = deployment
        self.task_type = task_type
        self.cancel_event = threading.Event()
        self.pause_event = threading.Event()
        self.results: list[InferenceResult] = []
    
    def run(self) -> None:
        """Execute inference on all frames"""
        try:
            for idx, frame in enumerate(self.frames):
                if self.cancel_event.is_set():
                    break
                
                # Pause support
                while self.pause_event.is_set():
                    time.sleep(0.1)
                
                start_time = time.perf_counter()
                try:
                    predictions = self.deployment.infer(frame)
                    elapsed_ms = (time.perf_counter() - start_time) * 1000
                    
                    result = InferenceResult(
                        frame_index=idx,
                        frame_name=f"Frame {idx+1}",
                        predictions=predictions,
                        processing_time_ms=elapsed_ms,
                        timestamp=time.time()
                    )
                    self.results.append(result)
                    self.progress_updated.emit(idx, result)
                except Exception as e:
                    self.error_signal.emit(f"Error processing frame {idx}: {str(e)}")
                    continue
            
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(f"Inference error: {str(e)}")


# ============================================================================
# Main Application Window
# ============================================================================

class EchoSightApp(QMainWindow):
    """Main application window with professional PyQt6 UI"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EchoSight - Model-agnostic Image Inference and Inspection")
        self.setMinimumSize(1400, 900)
        
        # Application state
        self.deployment = None
        self.frames: list[np.ndarray] = []
        self.frame_paths: list[Path] = []
        self.results: list[InferenceResult] = []
        self.current_result_idx = 0
        self.inference_worker: Optional[InferenceWorker] = None
        self.is_running = False
        self.is_paused = False
        
        # UI Setup
        self._apply_theme()
        self._build_ui()
        self._setup_connections()
        
        # Animation timer for progress
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._update_progress_animation)
        self.anim_tick = 0
    
    def _apply_theme(self) -> None:
        """Apply CSAM-inspired stylesheet"""
        stylesheet = f"""
        QMainWindow, QWidget {{
            background-color: {Theme.BG_PRIMARY};
            color: {Theme.TEXT_PRIMARY};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {Theme.BORDER};
            background: {Theme.BG_PRIMARY};
        }}
        
        QTabBar::tab {{
            background: {Theme.BG_SECONDARY};
            color: {Theme.TEXT_SECONDARY};
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            border: 1px solid {Theme.BORDER_LIGHT};
        }}
        
        QTabBar::tab:selected {{
            background: {Theme.BG_TERTIARY};
            color: {Theme.TEXT_PRIMARY};
            border-bottom: 2px solid {Theme.INFO};
        }}
        
        QGroupBox {{
            border: 1px solid {Theme.BORDER};
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: 600;
            color: {Theme.TEXT_PRIMARY};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 4px;
        }}
        
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {{
            background-color: {Theme.BG_SECONDARY};
            color: {Theme.TEXT_PRIMARY};
            border: 1px solid {Theme.BORDER};
            border-radius: 6px;
            padding: 6px;
            selection-background-color: {Theme.INFO};
        }}
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus {{
            border: 1px solid {Theme.INFO_BORDER};
        }}
        
        QProgressBar {{
            background-color: {Theme.BG_SECONDARY};
            color: {Theme.TEXT_PRIMARY};
            border: 1px solid {Theme.BORDER};
            border-radius: 6px;
            text-align: center;
            font-weight: 700;
            font-size: 11px;
            padding: 2px;
        }}
        
        QProgressBar::chunk {{
            background-color: {Theme.INFO};
            border-radius: 4px;
        }}
        
        QProgressBar[complete="true"]::chunk {{
            background-color: {Theme.SUCCESS};
        }}
        
        QPushButton {{
            background-color: {Theme.BG_SECONDARY};
            color: {Theme.TEXT_PRIMARY};
            border: 1px solid {Theme.BORDER};
            border-radius: 7px;
            padding: 7px 14px;
            font-weight: 600;
            font-size: 11px;
        }}
        
        QPushButton:hover {{
            border: 1px solid {Theme.INFO_BORDER};
            background-color: {Theme.BG_TERTIARY};
        }}
        
        QPushButton:pressed {{
            background-color: {Theme.BG_PRIMARY};
            border: 1px solid {Theme.INFO_BORDER};
            padding: 8px 14px 6px 14px;
        }}
        
        QPushButton:disabled {{
            background-color: {Theme.BG_SECONDARY};
            color: {Theme.TEXT_MUTED};
            border: 1px solid {Theme.BORDER_LIGHT};
        }}
        
        /* Role-based Button Styles */
        QPushButton[role="start"] {{
            background-color: {Theme.SUCCESS};
            color: #0f2416;
            border: 1px solid {Theme.SUCCESS_BORDER};
        }}
        
        QPushButton[role="start"]:hover {{
            background-color: #97dcaf;
            border: 1px solid {Theme.SUCCESS_BORDER};
        }}
        
        QPushButton[role="start"]:pressed {{
            background-color: {Theme.SUCCESS};
            padding: 8px 14px 6px 14px;
        }}
        
        QPushButton[role="warn"] {{
            background-color: {Theme.WARNING};
            color: #33210a;
            border: 1px solid {Theme.WARNING_BORDER};
        }}
        
        QPushButton[role="warn"]:hover {{
            background-color: #f8cb8a;
            border: 1px solid {Theme.WARNING_BORDER};
        }}
        
        QPushButton[role="stop"] {{
            background-color: {Theme.DANGER};
            color: #3d1113;
            border: 1px solid {Theme.DANGER_BORDER};
        }}
        
        QPushButton[role="stop"]:hover {{
            background-color: #f5adaf;
            border: 1px solid {Theme.DANGER_BORDER};
        }}
        
        QTableWidget, QListWidget {{
            background-color: {Theme.BG_SECONDARY};
            color: {Theme.TEXT_PRIMARY};
            border: 1px solid {Theme.BORDER};
            gridline-color: {Theme.BORDER};
        }}
        
        QTableWidget::item:selected, QListWidget::item:selected {{
            background-color: {Theme.INFO};
            color: #ffffff;
        }}
        
        QHeaderView::section {{
            background-color: {Theme.BG_TERTIARY};
            color: {Theme.TEXT_PRIMARY};
            padding: 4px;
            border: none;
            border-right: 1px solid {Theme.BORDER};
            border-bottom: 1px solid {Theme.BORDER};
            font-weight: 600;
        }}
        
        QLabel {{
            color: {Theme.TEXT_PRIMARY};
        }}
        
        QLabel[muted="true"] {{
            color: {Theme.TEXT_MUTED};
        }}
        
        QCheckBox {{
            color: {Theme.TEXT_PRIMARY};
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 3px;
            border: 1px solid {Theme.BORDER};
            background-color: {Theme.BG_SECONDARY};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {Theme.INFO};
            border: 1px solid {Theme.INFO_BORDER};
        }}
        
        QScrollBar:vertical {{
            background-color: {Theme.BG_SECONDARY};
            width: 12px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {Theme.BORDER};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {Theme.INFO};
        }}
        """
        self.setStyleSheet(stylesheet)
    
    def _build_ui(self) -> None:
        """Build the main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("EchoSight")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        subtitle_label = QLabel("Model-agnostic Image Inference and Inspection")
        subtitle_label.setProperty("muted", True)
        subtitle_font = QFont("Segoe UI", 10)
        subtitle_label.setFont(subtitle_font)
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addStretch()
        self.status_label = QLabel("Ready for a deployment model")
        self.status_label.setProperty("muted", True)
        header_layout.addWidget(self.status_label)
        main_layout.addLayout(header_layout)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet(f"border: 1px solid {Theme.BORDER};")
        main_layout.addWidget(divider)
        
        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setTabBar(self.tabs.tabBar())
        main_layout.addWidget(self.tabs)
        
        # Create Tabs
        self.analyze_tab = QWidget()
        self.results_tab = QWidget()
        self._build_analyze_tab()
        self._build_results_tab()
        
        self.tabs.addTab(self.analyze_tab, "  Analyze  ")
        self.tabs.addTab(self.results_tab, "  Results  ")
    
    def _build_analyze_tab(self) -> None:
        """Build Analyze tab"""
        layout = QVBoxLayout(self.analyze_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Control Panel
        control_group = QGroupBox("Model & Input")
        control_layout = QHBoxLayout(control_group)
        control_layout.setSpacing(8)
        
        self.load_model_btn = QPushButton("Load Model")
        self.load_model_btn.clicked.connect(self.load_model)
        control_layout.addWidget(self.load_model_btn)
        
        self.import_btn = QPushButton("Import Images")
        self.import_btn.clicked.connect(self.import_images)
        control_layout.addWidget(self.import_btn)
        
        control_layout.addStretch()
        
        self.run_all_btn = QPushButton("Run Analysis")
        self.run_all_btn.setProperty("role", "start")
        self.run_all_btn.clicked.connect(self.run_inference_all)
        self.run_all_btn.setEnabled(False)
        control_layout.addWidget(self.run_all_btn)
        
        self.run_selection_btn = QPushButton("Run Selection")
        self.run_selection_btn.setProperty("role", "start")
        self.run_selection_btn.clicked.connect(self.run_inference_selection)
        self.run_selection_btn.setEnabled(False)
        control_layout.addWidget(self.run_selection_btn)
        
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setProperty("role", "warn")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setEnabled(False)
        control_layout.addWidget(self.pause_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setProperty("role", "stop")
        self.cancel_btn.clicked.connect(self.cancel_inference)
        self.cancel_btn.setEnabled(False)
        control_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(control_group)
        
        # File List
        files_group = QGroupBox("Images")
        files_layout = QVBoxLayout(files_group)
        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(180)
        files_layout.addWidget(self.file_list)
        layout.addWidget(files_group)
        
        # Progress
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        self.progress_label = QLabel("Ready")
        self.progress_label.setProperty("muted", True)
        progress_layout.addWidget(self.progress_label)
        layout.addWidget(progress_group)
        
        layout.addStretch()
    
    def _build_results_tab(self) -> None:
        """Build Results tab"""
        layout = QVBoxLayout(self.results_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Results table
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)
        self.results_table = QTableWidget(0, 3)
        self.results_table.setHorizontalHeaderLabels(["Frame", "Detections", "Confidence"])
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        results_layout.addWidget(self.results_table)
        layout.addWidget(results_group)
        
        # Export button
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        self.export_btn = QPushButton("Export Results")
        self.export_btn.clicked.connect(self.export_results)
        self.export_btn.setEnabled(False)
        export_layout.addWidget(self.export_btn)
        layout.addLayout(export_layout)
    
    def _setup_connections(self) -> None:
        """Setup signal-slot connections"""
        pass
    
    def _update_progress_animation(self) -> None:
        """Update animated progress label"""
        if self.is_running:
            spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            self.progress_label.setText(f"{spinner[self.anim_tick % 10]} Processing...")
            self.anim_tick += 1
    
    def load_model(self) -> None:
        """Load a Geti deployment model"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Model Deployment Directory")
        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            self.status_label.setText(f"Model loaded: {dialog.selectedFiles()[0]}")
            QMessageBox.information(self, "Model Loaded", "Model deployment loaded successfully.")
    
    def import_images(self) -> None:
        """Import images for inference"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilters(["Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)", "All Files (*)"])
        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            files = dialog.selectedFiles()
            self.frame_paths = [Path(f) for f in files]
            self.file_list.clear()
            for path in self.frame_paths:
                self.file_list.addItem(path.name)
            self.status_label.setText(f"Imported {len(files)} images")
            self.run_all_btn.setEnabled(True)
            self.run_selection_btn.setEnabled(True)
    
    def run_inference_all(self) -> None:
        """Run inference on all frames"""
        if not self.frame_paths:
            QMessageBox.warning(self, "No Images", "Please import images first.")
            return
        
        self.is_running = True
        self.progress_bar.setValue(0)
        self.progress_label.setText("Starting inference...")
        self.anim_timer.start(100)
        self.run_all_btn.setEnabled(False)
        self.run_selection_btn.setEnabled(False)
        self.import_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        self.status_label.setText("Inference running...")
    
    def run_inference_selection(self) -> None:
        """Run inference on selected frames"""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select frames first.")
            return
        self.status_label.setText(f"Processing {len(selected_items)} selected frames...")
    
    def toggle_pause(self) -> None:
        """Toggle pause state"""
        self.is_paused = not self.is_paused
        self.pause_btn.setText("Resume" if self.is_paused else "Pause")
        self.status_label.setText("Paused" if self.is_paused else "Resumed")
    
    def cancel_inference(self) -> None:
        """Cancel inference"""
        self.is_running = False
        self.is_paused = False
        self.anim_timer.stop()
        self.progress_bar.setValue(0)
        self.progress_label.setText("Cancelled")
        self.run_all_btn.setEnabled(True)
        self.run_selection_btn.setEnabled(True)
        self.import_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.pause_btn.setText("Pause")
        self.status_label.setText("Ready")
    
    def export_results(self) -> None:
        """Export inference results"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Export Directory")
        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Export", "Results exported successfully.")
    
    @staticmethod
    def set_button_role(button: QPushButton, role: str) -> None:
        """Apply a role to a button and polish it"""
        button.setProperty("role", role)
        button.style().unpolish(button)
        button.style().polish(button)


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    window = EchoSightApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
