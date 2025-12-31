import sys
import os
import json
import traceback
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                              QTextEdit, QTabWidget, QFrame, QScrollArea, 
                              QGraphicsDropShadowEffect, QSizePolicy, QMessageBox,
                              QSplitter, QGridLayout, QComboBox, QSpinBox,
                              QProgressBar, QCheckBox, QSlider, QFileDialog)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QPoint, QSize, QThread, Signal
from PySide6.QtGui import (QFont, QIcon, QPixmap, QPainter, QColor, QBrush, QPen, 
                          QLinearGradient, QRadialGradient, QConicalGradient,
                          QPainterPath, QFontDatabase, QPalette, QCursor, QAction)
import random
import time
from datetime import datetime
import logging

# Set up logging for better error handling
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandler:
    """Centralized error handling for the application"""
    @staticmethod
    def handle_error(error, title="Error", parent=None):
        """Handle and display errors with proper logging"""
        error_msg = f"{str(error)}\n\n{traceback.format_exc()}"
        logger.error(error_msg)
        
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(str(error))
        msg_box.setDetailedText(traceback.format_exc())
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

class ResponsiveFrostedGlassWidget(QWidget):
    """Enhanced frosted glass widget with responsive behavior"""
    def __init__(self, parent=None, blur_radius=20, opacity=0.85):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.blur_radius = blur_radius
        self.opacity = opacity
        
        # Add shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        # Make widget responsive
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create advanced frosted glass effect with gradient
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)
        
        # Main glass effect
        glass_color = QColor(255, 255, 255, int(40 * self.opacity))
        painter.fillPath(path, glass_color)
        
        # Subtle border glow
        pen = QPen(QColor(255, 255, 255, int(80 * self.opacity)))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Add subtle inner highlights
        highlight_gradient = QLinearGradient(0, 0, 0, self.height())
        highlight_gradient.setColorAt(0, QColor(255, 255, 255, int(30 * self.opacity)))
        highlight_gradient.setColorAt(1, QColor(255, 255, 255, int(5 * self.opacity)))
        
        highlight_path = QPainterPath()
        highlight_rect = self.rect().adjusted(2, 2, -2, -2)
        highlight_path.addRoundedRect(highlight_rect, 18, 18)
        painter.fillPath(highlight_path, QBrush(highlight_gradient))

class ModernButton(QPushButton):
    """Modern button with hover effects and gradients"""
    def __init__(self, text="", parent=None, color="#3B82F6", icon=None):
        super().__init__(text, parent)
        self.color = color
        self.base_color = QColor(color)
        self.hover_color = self.base_color.darker(120)
        self.press_color = self.base_color.darker(150)
        
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(self.base_color.red(), self.base_color.green(), self.base_color.blue(), 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.update_style()
        
    def update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                border-radius: 10px;
                font-weight: 600;
                font-size: 14px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.5);
            }}
            QPushButton:pressed {{
                background-color: rgba(255, 255, 255, 0.35);
            }}
        """)

class AnimatedWaveformWidget(QWidget):
    """Advanced waveform animation with multiple bars and smooth transitions"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(80, 40)
        self.bars = [random.uniform(0.1, 1.0) for _ in range(8)]
        self.target_bars = self.bars.copy()
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_bars)
        self.is_animating = False
        
    def start_animation(self):
        self.is_animating = True
        self.animation_timer.start(50)
        
    def stop_animation(self):
        self.is_animating = False
        self.animation_timer.stop()
        # Smoothly lower all bars
        self.target_bars = [0.1] * len(self.bars)
        QTimer.singleShot(500, self.update)
        
    def animate_bars(self):
        if self.is_animating:
            # Update target heights randomly
            for i in range(len(self.target_bars)):
                if random.random() < 0.3:  # 30% chance to change each frame
                    self.target_bars[i] = random.uniform(0.2, 1.0)
            
            # Smoothly interpolate towards target heights
            for i in range(len(self.bars)):
                self.bars[i] += (self.target_bars[i] - self.bars[i]) * 0.3
            
            self.update()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        bar_count = len(self.bars)
        bar_width = 6
        spacing = 3
        total_width = bar_count * bar_width + (bar_count - 1) * spacing
        start_x = (self.width() - total_width) // 2
        
        # Create gradient with stealth colors
        gradient = QLinearGradient(0, self.height(), 0, 0)
        gradient.setColorAt(0, QColor(99, 102, 241))
        gradient.setColorAt(1, QColor(168, 85, 247))
        
        for i, height_ratio in enumerate(self.bars):
            x = start_x + i * (bar_width + spacing)
            bar_height = height_ratio * (self.height() - 10)
            y = self.height() - bar_height - 5
            
            # Draw bar with rounded top
            path = QPainterPath()
            path.addRoundedRect(int(x), int(y), bar_width, bar_height, 3, 3)
            painter.fillPath(path, QBrush(gradient))
            
            # Add subtle highlight
            highlight = QLinearGradient(x, y, x + bar_width, y)
            highlight.setColorAt(0, QColor(255, 255, 255, 80))
            highlight.setColorAt(1, QColor(255, 255, 255, 20))
            painter.fillRect(int(x) + 1, int(y) + 1, bar_width - 2, 4, highlight)

class ResponsiveTextEdit(QTextEdit):
    """Text edit widget that properly handles resizing"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Ensure proper text wrapping on resize
        self.setLineWrapMode(QTextEdit.WidgetWidth)

class ResponsiveTabWidget(QTabWidget):
    """Tab widget that properly handles resizing and maintains consistent layout"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Enhanced styling
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
                margin-top: 5px;
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.7);
                padding: 10px 20px;
                margin-right: 3px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 500;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background: rgba(59, 130, 246, 0.3);
                color: white;
                border-bottom: 2px solid rgb(59, 130, 246);
            }
            QTabBar::tab:hover:!selected {
                background: rgba(255, 255, 255, 0.15);
            }
        """)

    def addTab(self, widget, title):
        """Override addTab to ensure proper widget sizing"""
        super().addTab(widget, title)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class WorkerThread(QThread):
    """Worker thread for processing AI requests without blocking UI"""
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, action, user_input):
        super().__init__()
        self.action = action
        self.user_input = user_input
        
    def run(self):
        try:
            # Simulate processing time
            time.sleep(1)
            
            # Generate response based on action
            responses = {
                'answer': f"**Comprehensive Answer**\n\nBased on your query about '{self.user_input}', here's a detailed response:\n\nI understand you're looking for information. Let me break this down into key points and provide you with a thorough explanation that covers the main concepts and practical applications.\n\nThis comprehensive answer addresses all aspects of your question with detailed explanations, examples, and practical recommendations that you can implement immediately.",
                'code': f"// Solution for: {self.user_input}\n\nfunction optimizedSolution() {{\n  // Implement efficient algorithm\n  const result = processData(user_input);\n  \n  // Add error handling\n  try {{\n    return validateResult(result);\n  }} catch (error) {{\n    console.error('Processing error:', error);\n    return null;\n  }}\n}}\n\n// Additional helper functions\nfunction processData(input) {{\n  // Process input data\n  return input.map(item => transform(item));\n}}\n\nfunction validateResult(result) {{\n  // Validate processing results\n  if (!result || result.length === 0) {{\n    throw new Error('Invalid result');\n  }}\n  return result;\n}}",
                'analyze': f"**Deep Analysis Report**\n\n**Subject:** {self.user_input}\n\n**Key Findings:**\n• Pattern recognition: Multiple correlated elements detected\n• Optimization potential: 40-60% improvement possible\n• Risk assessment: Low to moderate complexity\n• Performance metrics: Above average benchmarks\n• Scalability factors: Suitable for enterprise deployment\n\n**Recommendations:**\n1. Implement scalable architecture\n2. Add comprehensive testing\n3. Monitor performance metrics\n4. Consider security implications\n5. Plan for future expansion\n\n**Implementation Strategy:**\nPhase 1: Core functionality\nPhase 2: Advanced features\nPhase 3: Optimization and scaling",
                'summarize': f"**Executive Summary**\n\n**Topic:** {self.user_input}\n\n**Main Points:**\n• Core concept explained in simple terms\n• Key benefits and applications highlighted\n• Implementation considerations outlined\n• Potential challenges and solutions identified\n\n**Takeaways:**\nThis provides a solid foundation for understanding the fundamental principles and practical applications. The summary captures the essential information while maintaining clarity and conciseness.\n\n**Next Steps:**\n1. Review detailed documentation\n2. Conduct proof of concept\n3. Develop implementation roadmap\n4. Allocate resources and timeline",
                'create': f"**Creative Solution** 🎨\n\nFor '{self.user_input}', here's an innovative approach:\n\n**Concept:** Next-generation interactive experience\n**Features:** AI-powered adaptive interface, real-time collaboration, seamless integration\n**Technical Stack:** Modern framework with cloud-native architecture\n\n**Design Elements:**\n• User-centric interface with intuitive navigation\n• Responsive design for all device types\n• Accessibility features for inclusive experience\n• Performance optimization for smooth interactions\n\n**Implementation Plan:**\n1. Discovery and research phase\n2. Design and prototyping\n3. Development and testing\n4. Deployment and maintenance\n\nLet's bring this vision to life with cutting-edge technology!"
            }
            
            response = responses.get(self.action, "Action not recognized.")
            self.finished.emit(response)
        except Exception as e:
            self.error.emit(str(e))

class AdvancedAIInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ AI Assistant")
        self.resize(1200, 900)  # Increased default size
        
        # Set window properties for transparency
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Store original geometry for restore
        self.normal_geometry = QRect(50, 50, 1200, 900)
        self.is_minimized_to_icon = False
        
        # Initialize variables
        self.is_recording = False
        self.recording_type = None
        self.transcription_text = ""
        
        # Resize tracking variables
        self.dragging = False
        self.resizing = False
        self.resize_mode = None
        self.drag_position = None
        self.resize_margin = 10
        
        # Worker thread for AI processing
        self.worker_thread = None
        
        # Setup UI
        self.setup_ui()
        
        # Setup animations
        self.setup_animations()
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
        
    def setup_ui(self):
        """Setup the advanced UI components"""
        # Main container with advanced frosted glass
        self.main_container = ResponsiveFrostedGlassWidget(self, blur_radius=25, opacity=0.9)
        self.main_container.setGeometry(50, 50, 1100, 800)
        
        # Main layout
        main_layout = QVBoxLayout(self.main_container)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(10)
        
        # Create a splitter for better layout control
        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)
        
        # Top section (20% of space)
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header section
        self.setup_header(top_layout)
        
        # Input section
        self.setup_input_section(top_layout)
        
        # Action buttons
        self.setup_action_buttons(top_layout)
        
        # Output section (80% of space)
        output_widget = self.setup_output_section_widget()
        
        # Add widgets to splitter with appropriate sizes
        splitter.addWidget(top_widget)
        splitter.addWidget(output_widget)
        splitter.setSizes([200, 800])  # 20% and 80% ratio
        
        main_layout.addWidget(splitter)
        
        # Add window controls
        self.add_advanced_window_controls()
        
        # Add floating elements
        self.add_floating_elements()
        
    def setup_header(self, parent_layout):
        """Setup the header section"""
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        # Main title with gradient text effect
        self.title_label = QLabel("⚡ AI Assistant")
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: 800;
                background: transparent;
            }
        """)
        self.title_label.setFixedHeight(40)
        
        # Subtitle
        self.subtitle_label = QLabel("AI-powered conversation and code generation")
        self.subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px; font-weight: 400;")
        
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)
        parent_layout.addLayout(header_layout)
        
    def setup_input_section(self, parent_layout):
        """Setup the input section with advanced styling"""
        input_container = QWidget()
        input_container.setStyleSheet("background: rgba(255, 255, 255, 0.05); border-radius: 15px;")
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(20, 20, 20, 20)
        input_layout.setSpacing(15)
        
        # Input label
        input_label = QLabel("Voice & Text Input")
        input_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 16px; font-weight: 600;")
        input_layout.addWidget(input_label)
        
        # Recording controls
        self.setup_recording_controls(input_layout)
        
        # Text input
        self.setup_text_input(input_layout)
        
        parent_layout.addWidget(input_container)
        
    def setup_recording_controls(self, parent_layout):
        """Setup recording controls with waveform"""
        controls_layout = QHBoxLayout()
        
        # Recording buttons
        button_layout = QHBoxLayout()
        
        self.internal_mic_btn = ModernButton("🎤 Internal Mic", color="#16213e")
        self.internal_mic_btn.clicked.connect(lambda: self.toggle_recording('internal'))
        
        self.external_mic_btn = ModernButton("🎧 External Mic", color="#533483")
        self.external_mic_btn.clicked.connect(lambda: self.toggle_recording('external'))
        
        button_layout.addWidget(self.internal_mic_btn)
        button_layout.addWidget(self.external_mic_btn)
        button_layout.addStretch()
        
        # Waveform display
        self.waveform = AnimatedWaveformWidget()
        self.recording_label = QLabel("Ready")
        self.recording_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        
        waveform_layout = QHBoxLayout()
        waveform_layout.addWidget(self.waveform)
        waveform_layout.addWidget(self.recording_label)
        waveform_layout.addStretch()
        
        controls_layout.addLayout(button_layout)
        controls_layout.addLayout(waveform_layout)
        parent_layout.addLayout(controls_layout)
        
    def setup_text_input(self, parent_layout):
        """Setup text input area"""
        input_group = QVBoxLayout()
        
        # Text input field
        input_field_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your question or command...")
        self.user_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.08);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 12px 16px;
                color: white;
                font-size: 14px;
                selection-background-color: rgba(59, 130, 246, 0.3);
            }
            QLineEdit:focus {
                border: 2px solid rgba(59, 130, 246, 0.5);
                background: rgba(255, 255, 255, 0.12);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.4);
            }
        """)
        self.user_input.setFixedHeight(45)
        
        self.clear_input_btn = QPushButton("✕")
        self.clear_input_btn.setFixedSize(35, 35)
        self.clear_input_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.6);
                font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
                color: white;
            }
        """)
        self.clear_input_btn.clicked.connect(self.clear_input)
        
        input_field_layout.addWidget(self.user_input)
        input_field_layout.addWidget(self.clear_input_btn)
        input_group.addLayout(input_field_layout)
        
        # Live transcription
        self.transcription = QTextEdit()
        self.transcription.setPlaceholderText("Live transcription will appear here...")
        self.transcription.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 12px;
                color: rgba(255, 255, 255, 0.8);
                font-size: 13px;
                selection-background-color: rgba(59, 130, 246, 0.3);
            }
        """)
        self.transcription.setFixedHeight(70)
        input_group.addWidget(self.transcription)
        
        parent_layout.addLayout(input_group)
        
    def setup_action_buttons(self, parent_layout):
        """Setup the action buttons with modern styling"""
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        actions_data = [
            ("💬 Answer", "#1a1a2e", 'answer'),
            ("⚡ Code", "#16213e", 'code'),
            ("🔍 Analyze", "#0f3460", 'analyze'),
            ("📋 Summarize", "#533483", 'summarize'),
            ("✨ Create", "#e94560", 'create')
        ]
        
        self.action_buttons = []
        for text, color, action in actions_data:
            btn = ModernButton(text, color=color)
            btn.clicked.connect(lambda checked, a=action: self.process_action(a))
            btn.setFixedHeight(45)
            actions_layout.addWidget(btn)
            self.action_buttons.append(btn)
            
        parent_layout.addLayout(actions_layout)
        
    def setup_output_section_widget(self):
        """Setup the output section widget and return it"""
        output_container = QWidget()
        output_container.setStyleSheet("background: rgba(255, 255, 255, 0.05); border-radius: 15px;")
        output_layout = QVBoxLayout(output_container)
        output_layout.setContentsMargins(20, 20, 20, 20)
        
        # Output header
        output_header = QHBoxLayout()
        output_label = QLabel("AI Responses")
        output_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 16px; font-weight: 600;")
        
        output_header.addWidget(output_label)
        output_header.addStretch()
        
        # Output actions
        self.setup_output_actions(output_header)
        output_layout.addLayout(output_header)
        
        # Advanced tabs
        self.setup_advanced_tabs(output_layout)
        
        return output_container
        
    def setup_output_actions(self, parent_layout):
        """Setup output action buttons"""
        actions = [
            ("📋 Copy", self.copy_output),
            ("💾 Export", self.export_output),
            ("✨ Highlight", self.highlight_output),
            ("🔄 Refresh", self.refresh_output)
        ]
        
        for text, slot in actions:
            btn = QPushButton(text)
            btn.setFixedSize(80, 30)
            btn.setStyleSheet("""
            QPushButton {
                    background: rgba(255, 255, 255, 0.1);
                    border: none;
                    border-radius: 6px;
                    color: rgba(255, 255, 255, 0.8);
                    font-size: 11px;
                    padding: 4px;
            }
            QPushButton:hover {
                    background: rgba(255, 255, 255, 0.15);
                color: white;
            }
        """)
            btn.clicked.connect(slot)
            parent_layout.addWidget(btn)
            
    def setup_advanced_tabs(self, parent_layout):
        """Setup advanced tab widget with custom styling"""
        self.tabs = ResponsiveTabWidget()
        
        # Create and setup tabs
        self.setup_tab_content()
        parent_layout.addWidget(self.tabs)
        
    def setup_tab_content(self):
        """Setup content for each tab"""
        tabs_data = [
            ("💬 Chat", "text_answer", "Chat conversations will appear here..."),
            ("⚡ Code", "code", "// Generated code will appear here\nfunction example() {\n  return 'Hello World';\n}"),
            ("🔍 Analysis", "analysis", "Analysis results will be displayed here..."),
            ("📋 Summary", "summary", "Content summaries will appear here..."),
            ("✨ Creative", "creative", "Creative content and ideas will appear here...")
        ]
        
        for icon_name, tab_type, placeholder in tabs_data:
            tab = QWidget()
            layout = QVBoxLayout(tab)
            
            # Create responsive text edit
            text_edit = ResponsiveTextEdit()
            text_edit.setPlainText(placeholder)
            text_edit.setStyleSheet("""
            QTextEdit {
                    background: rgba(255, 255, 255, 0.15);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 12px;
                    color: #000000;
                    font-size: 15px;
                    font-weight: bold;
                    padding: 15px;
                    selection-background-color: rgba(59, 130, 246, 0.3);
            }
        """)
            
            # Store reference to output widget
            setattr(self, f"{tab_type}_output", text_edit)
            
            layout.addWidget(text_edit)
            self.tabs.addTab(tab, icon_name)
            
    def add_advanced_window_controls(self):
        """Add advanced window control buttons"""
        controls = [
            ("—", self.showMinimized, "#16213e"),
            ("□", self.toggle_maximize, "#0f3460"), 
            ("×", self.close, "#e94560")
        ]
        
        x_pos = 1060  # Adjusted for larger window
        for text, slot, color in controls:
            btn = QPushButton(text, self)
            btn.setGeometry(x_pos, 20, 30, 30)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                color: white;
                border: none;
                    border-radius: 15px;
                    font-weight: bold;
                font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {QColor(color).darker(120).name()};
                }}
            """)
            btn.clicked.connect(slot)
            x_pos += 40
            
    def add_floating_elements(self):
        """Add floating decorative elements"""
        # Floating AI suggestion button
        self.floating_ai_btn = ModernButton("AI", color="#4285F4")
        self.floating_ai_btn.setFixedSize(50, 50)
        self.floating_ai_btn.move(1000, 100)
        self.floating_ai_btn.clicked.connect(self.show_ai_suggestions)
        
        # Decorative floating particles (simulated)
        self.floating_particles = []
        for _ in range(5):
            particle = QLabel("✦", self)
            particle.setStyleSheet("color: rgba(255, 255, 255, 0.3); font-size: 16px;")
            x = random.randint(50, 1050)
            y = random.randint(50, 750)
            particle.move(x, y)
            self.floating_particles.append(particle)
            
    def setup_animations(self):
        """Setup various animations"""
        self.animations = []
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Create actions for shortcuts
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        self.addAction(quit_action)
        
        # Focus input shortcut
        focus_action = QAction("Focus Input", self)
        focus_action.setShortcut("Ctrl+K")
        focus_action.triggered.connect(self.user_input.setFocus)
        self.addAction(focus_action)
        
    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        if self.isMaximized() or self.width() > 1400:
            self.showNormal()
            self.resize(1200, 900)
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.show()
        else:
            # Store position before maximizing
            self.normal_pos = self.pos()
            screen = QApplication.primaryScreen().geometry()
            self.resize(screen.width(), screen.height())
            self.move(0, 0)
            
    def showMinimized(self):
        """Override to minimize to icon instead of taskbar"""
        self.normal_geometry = self.geometry()
        self.is_minimized_to_icon = True
        
        # Create minimized icon widget
        if not hasattr(self, 'minimized_icon'):
            self.minimized_icon = MinimizedIcon(self)
        
        # Position icon near current window position
        icon_pos = self.pos() + QPoint(50, 50)
        self.minimized_icon.move(icon_pos)
        self.minimized_icon.show()
        
        # Hide main window
        self.hide()
        
    def restore_from_minimize(self):
        """Restore from minimized icon"""
        self.show()
        if hasattr(self, 'minimized_icon'):
            self.minimized_icon.hide()
        self.is_minimized_to_icon = False
        
    def toggle_recording(self, mic_type):
        """Toggle recording state with enhanced feedback"""
        if self.is_recording and self.recording_type == mic_type:
            self.stop_recording()
        else:
            self.start_recording(mic_type)
            
    def start_recording(self, mic_type):
        """Start recording with visual feedback"""
        self.is_recording = True
        self.recording_type = mic_type
        self.waveform.start_animation()
        self.recording_label.setText("🎤 Recording...")
        self.recording_label.setStyleSheet("color: #e94560; font-weight: 600;")
            
        # Update button states
        if mic_type == 'internal':
            self.internal_mic_btn.setText("⏹️ Stop")
        else:
            self.external_mic_btn.setText("⏹️ Stop") 
        
            self.simulate_transcription()
    
    def stop_recording(self):
        """Stop recording with smooth transition"""
        self.is_recording = False
        self.waveform.stop_animation()
        self.recording_label.setText("✅ Ready")
        self.recording_label.setStyleSheet("color: #10B981; font-weight: 600;")
        
        # Reset buttons
        self.internal_mic_btn.setText("🎤 Internal Mic")
        self.external_mic_btn.setText("🎧 External Mic")
        
        # Finalize transcription
        self.transcription.setPlainText("✓ Transcription complete and ready for processing.")
    
    def simulate_transcription(self):
        """Simulate live transcription with random content"""
        if not self.is_recording:
            return
        
        samples = [
            "I'm looking for help with programming a new feature...",
            "Can you explain how machine learning algorithms work?",
            "I need to create a responsive web design for my project...",
            "What's the best way to optimize database queries?",
            "Could you help me debug this Python code I'm working on?"
        ]
        
        sample = random.choice(samples)
        self.transcription_text = ""
        self.transcription_timer = QTimer()
        self.transcription_timer.timeout.connect(lambda: self.type_text(sample))
        self.transcription_timer.start(80)
        
    def type_text(self, full_text):
        """Type text character by character"""
        if not self.is_recording or len(self.transcription_text) >= len(full_text):
            self.transcription_timer.stop()
            return
        
        self.transcription_text += full_text[len(self.transcription_text)]
        self.transcription.setPlainText(self.transcription_text)
    
    def clear_input(self):
        """Clear all input fields"""
        self.user_input.clear()
        self.transcription.clear()
        self.transcription_text = ""
    
    def process_action(self, action):
        """Process AI actions with enhanced responses using worker thread"""
        user_input = self.user_input.text() or self.transcription.toPlainText()
        if not user_input:
            user_input = "Hello, how can you help me today?"
            
        # Disable action buttons during processing
        for btn in self.action_buttons:
            btn.setEnabled(False)
        
        # Show processing indicator
        self.recording_label.setText("⏳ Processing...")
        
        # Start worker thread
        self.worker_thread = WorkerThread(action, user_input)
        self.worker_thread.finished.connect(self.on_processing_finished)
        self.worker_thread.error.connect(self.on_processing_error)
        self.worker_thread.start()
    
    def on_processing_finished(self, response):
        """Handle processing completion"""
        # Re-enable action buttons
        for btn in self.action_buttons:
            btn.setEnabled(True)
        
        # Reset recording label
        self.recording_label.setText("✅ Ready")
        
        # Get action type from worker thread
        action = self.worker_thread.action
        
        # Update appropriate output widget
        output_widget = getattr(self, f"{action}_output")
        output_widget.setPlainText(response)
        
        # Switch to appropriate tab
        tab_index = ['text_answer', 'code', 'analysis', 'summary', 'creative'].index(action)
        self.tabs.setCurrentIndex(tab_index)
    
    def on_processing_error(self, error_msg):
        """Handle processing errors"""
        # Re-enable action buttons
        for btn in self.action_buttons:
            btn.setEnabled(True)
        
        # Reset recording label
        self.recording_label.setText("❌ Error")
        
        # Show error message
        ErrorHandler.handle_error(error_msg, "Processing Error", self)
    
    def copy_output(self):
        """Copy current output to clipboard"""
        current_index = self.tabs.currentIndex()
        tab_names = ['text_answer', 'code', 'analysis', 'summary', 'creative']
        output_widget = getattr(self, f"{tab_names[current_index]}_output")
        
        QApplication.clipboard().setText(output_widget.toPlainText())
        self.show_notification("✓ Copied to clipboard")
    
    def export_output(self):
        """Export output to file"""
        current_index = self.tabs.currentIndex()
        tab_names = ['text_answer', 'code', 'analysis', 'summary', 'creative']
        output_widget = getattr(self, f"{tab_names[current_index]}_output")
        
        # Get file path from user
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Export Output", 
            f"ai_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(output_widget.toPlainText())
                    self.show_notification(f"✓ Exported to {os.path.basename(file_path)}")
            except Exception as e:
                ErrorHandler.handle_error(e, "Export Error", self)
    
    def highlight_output(self):
        """Toggle highlight on current output"""
        current_index = self.tabs.currentIndex()
        tab_names = ['text_answer', 'code', 'analysis', 'summary', 'creative']
        output_widget = getattr(self, f"{tab_names[current_index]}_output")
        
        current_style = output_widget.styleSheet()
        if "rgba(59, 130, 246, 0.1)" in current_style:
            output_widget.setStyleSheet(output_widget.styleSheet().replace("background: rgba(59, 130, 246, 0.1);", ""))
            self.show_notification("✓ Highlight removed")
        else:
            output_widget.setStyleSheet(output_widget.styleSheet() + "background: rgba(59, 130, 246, 0.1);")
            self.show_notification("✓ Content highlighted")
            
    def refresh_output(self):
        """Refresh the current output tab"""
        current_index = self.tabs.currentIndex()
        self.show_notification("✓ Output refreshed")
        
    def show_ai_suggestions(self):
        """Show AI suggestions"""
        suggestions = [
            "How can I optimize my code for better performance?",
            "Explain neural networks in simple terms",
            "Help me design a database schema",
            "Create a responsive web layout",
            "Debug this Python function"
        ]
        
        self.user_input.setText(random.choice(suggestions))
        self.show_notification("💡 AI suggestion added")
        
    def show_notification(self, message):
        """Show temporary notification"""
        # Simple notification implementation
        self.recording_label.setText(message)
        QTimer.singleShot(2000, lambda: self.recording_label.setText("Ready" if not self.is_recording else "🎤 Recording..."))
    
    def mousePressEvent(self, event):
        """Handle window dragging and start of resizing"""
        if event.button() == Qt.LeftButton:
            pos = event.position().toPoint()
            
            # Check for resize areas
            if self.check_resize_edge(pos):
                self.resizing = True
            else:
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def check_resize_edge(self, pos):
        """Check if position is on a resize edge and return mode"""
        rect = self.rect()
        width = self.width()
        height = self.height()
        margin = self.resize_margin
        
        # Corners (takes priority)
        if pos.x() <= margin and pos.y() <= margin:
            self.resize_mode = 'top_left'
            return True
        elif pos.x() >= width - margin and pos.y() <= margin:
            self.resize_mode = 'top_right'
            return True
        elif pos.x() <= margin and pos.y() >= height - margin:
            self.resize_mode = 'bottom_left'
            return True
        elif pos.x() >= width - margin and pos.y() >= height - margin:
            self.resize_mode = 'bottom_right'
            return True
        # Edges
        elif pos.x() <= margin:
            self.resize_mode = 'left'
            return True
        elif pos.x() >= width - margin:
            self.resize_mode = 'right'
            return True
        elif pos.y() <= margin:
            self.resize_mode = 'top'
            return True
        elif pos.y() >= height - margin:
            self.resize_mode = 'bottom'
            return True
        else:
            self.resize_mode = None
            return False
    
    def get_resize_mode(self, pos, width, height, margin):
        """Determine the resize mode for cursor display"""
        # Corners (takes priority over edges)
        if pos.x() <= margin and pos.y() <= margin:
            return 'top_left'
        elif pos.x() >= width - margin and pos.y() <= margin:
            return 'top_right'
        elif pos.x() <= margin and pos.y() >= height - margin:
            return 'bottom_left'
        elif pos.x() >= width - margin and pos.y() >= height - margin:
            return 'bottom_right'
        # Edges
        elif pos.x() <= margin:
            return 'left'
        elif pos.x() >= width - margin:
            return 'right'
        elif pos.y() <= margin:
            return 'top'
        elif pos.y() >= height - margin:
            return 'bottom'
        else:
            return None
    
    def mouseMoveEvent(self, event):
        """Handle window dragging and resizing"""
        pos = event.position().toPoint()
        width = self.width()
        height = self.height()
        margin = self.resize_margin
        
        # Cursor feedback when not dragging/resizing
        if not self.resizing and not self.dragging:
            mode = self.get_resize_mode(pos, width, height, margin)
            self.update_cursor_for_resize_mode(mode)
        
        # Handle resizing
        if self.resizing and event.buttons() == Qt.LeftButton:
            self.handle_resize(event)
        
        # Handle dragging
        elif self.dragging and event.buttons() == Qt.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            self.move(new_pos)
        
        event.accept()
    
    def handle_resize(self, event):
        """Handle the actual resizing based on resize mode"""
        pos = event.pos()
        
        # Minimum and maximum constraints
        min_width, max_width = 1000, 1920
        min_height, max_height = 800, 1080
        
        if self.resize_mode == 'right':
            # Resize from right edge
            new_width = max(min_width, min(pos.x(), max_width))
            self.resize(new_width, self.height())
        elif self.resize_mode == 'left':
            # Resize from left edge (adjust position too)
            delta_x = pos.x()
            new_width = max(min_width, min(self.width() - delta_x, max_width))
            new_x = self.frameGeometry().right() - new_width
            self.setGeometry(new_x, self.y(), new_width, self.height())
        elif self.resize_mode == 'bottom':
            # Resize from bottom edge
            new_height = max(min_height, min(pos.y(), max_height))
            self.resize(self.width(), new_height)
        elif self.resize_mode == 'top':
            # Resize from top edge (adjust position too)
            delta_y = pos.y()
            new_height = max(min_height, min(self.height() - delta_y, max_height))
            new_y = self.frameGeometry().bottom() - new_height
            self.setGeometry(self.x(), new_y, self.width(), new_height)
        elif self.resize_mode == 'bottom_right':
            # Resize from bottom-right corner
            new_width = max(min_width, min(pos.x(), max_width))
            new_height = max(min_height, min(pos.y(), max_height))
            self.resize(new_width, new_height)
        elif self.resize_mode == 'bottom_left':
            # Resize from bottom-left corner
            delta_x = pos.x()
            new_width = max(min_width, min(self.width() - delta_x, max_width))
            new_height = max(min_height, min(pos.y(), max_height))
            new_x = self.frameGeometry().right() - new_width
            self.setGeometry(new_x, self.y(), new_width, new_height)
        elif self.resize_mode == 'top_right':
            # Resize from top-right corner
            new_width = max(min_width, min(pos.x(), max_width))
            delta_y = pos.y()
            new_height = max(min_height, min(self.height() - delta_y, max_height))
            new_y = self.frameGeometry().bottom() - new_height
            self.setGeometry(self.x(), new_y, new_width, new_height)
        elif self.resize_mode == 'top_left':
            # Resize from top-left corner
            delta_x = pos.x()
            delta_y = pos.y()
            new_width = max(min_width, min(self.width() - delta_x, max_width))
            new_height = max(min_height, min(self.height() - delta_y, max_height))
            new_x = self.frameGeometry().right() - new_width
            new_y = self.frameGeometry().bottom() - new_height
            self.setGeometry(new_x, new_y, new_width, new_height)
    
    def update_cursor_for_resize_mode(self, mode):
        """Update cursor based on resize mode"""
        cursors = {
            'right': Qt.SizeHorCursor,
            'left': Qt.SizeHorCursor,
            'bottom': Qt.SizeVerCursor,
            'top': Qt.SizeVerCursor,
            'bottom_right': Qt.SizeFDiagCursor,
            'bottom_left': Qt.SizeBDiagCursor,
            'top_right': Qt.SizeBDiagCursor,
            'top_left': Qt.SizeFDiagCursor,
            None: Qt.ArrowCursor
        }
        self.setCursor(cursors.get(mode, Qt.ArrowCursor))
    
    def mouseReleaseEvent(self, event):
        """Reset resize mode when mouse is released"""
        self.resizing = False
        self.dragging = False
        self.resize_mode = None
        self.setCursor(Qt.ArrowCursor)
        event.accept()
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Clean up worker thread
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.worker_thread.wait()
        
        # Accept the close event
        event.accept()

class MinimizedIcon(QWidget):
    """Small minimized icon window that stays on screen"""
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(80, 80)
        
        # Make it draggable
        self.drag_pos = QPoint()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create frosted glass icon with rounded rect
        brush = QBrush(QColor(22, 33, 62, 200))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)
        
        # Draw icon/text
        painter.setPen(QPen(Qt.white, 2))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, "⚡")
        
    def mousePressEvent(self, event):
        self.drag_pos = event.globalPosition().toPoint()
        
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
                self.drag_pos = event.globalPosition().toPoint()
            
    def mouseDoubleClickEvent(self, event):
        """Double click to restore"""
        self.main_window.restore_from_minimize()
        
    def enterEvent(self, event):
        """Show hint on hover"""
        self.setStyleSheet("background: rgba(22, 33, 62, 0.9);")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set dark theme
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(15, 23, 42))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(dark_palette)
    
    # Create and show window
    window = AdvancedAIInterface()
    window.show()
    
    sys.exit(app.exec())