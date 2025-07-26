"""
UI 관련 설정, 스타일, 컴포넌트 통합 파일
"""

# ========================================
# 🎨 UI 색상/레이아웃/설정 상수
# ========================================
class UIColors:
    # ... 기존 UIColors 코드 ...
    LOAD_BUTTON_BG = 0xFF0D4F1C
    LOAD_BUTTON_BORDER = 0xFF2ECC40
    LOAD_BUTTON_HOVER = 0xFF1A6B2A
    RED_BUTTON_BG = 0xFF0D0D4F
    RED_BUTTON_BORDER = 0xFF2E2ECC
    RED_BUTTON_HOVER = 0xFF1A1A6B
    STATE_BUTTON_BG = 0xFF0D4F1C
    STATE_BUTTON_BORDER = 0xFF2ECC40
    STATE_BUTTON_HOVER = 0xFF1A6B2A
    YELLOW_BUTTON_BG = 0xFF007ACC
    YELLOW_BUTTON_BORDER = 0xFF00CCFF
    YELLOW_BUTTON_HOVER = 0xFF0099E6
    OBJECT_VIZ_BUTTON_BG = 0xFFCC007A
    OBJECT_VIZ_BUTTON_BORDER = 0xFFE60099
    OBJECT_VIZ_BUTTON_HOVER = 0xFFB30066
    TRANSPARENCY_BUTTON_BG = 0xFF808080
    TRANSPARENCY_BUTTON_BORDER = 0xFF606060
    TRANSPARENCY_BUTTON_HOVER = 0xFF909090
    SIDEBAR_SUCCESS = 0xFF2ECC40
    SIDEBAR_RESET = 0xFF2E2ECC
    SIDEBAR_STATE = 0xFF2ECC40
    TEXT_PRIMARY = 0xFFFFFFFF
    TEXT_BLACK = 0xFF000000
    TEXT_DARK_GRAY = 0xFF333333
    BLUE_BUTTON_BG = 0xFF7E231E
    BLUE_BUTTON_BORDER = 0xFFD27619
    BLUE_BUTTON_HOVER = 0xFFC06515

class UILayout:
    BUTTON_HEIGHT = 30
    BUTTON_HEIGHT_LARGE = 35
    LABEL_HEIGHT = 25
    SEPARATOR_HEIGHT = 5
    SEPARATOR_HEIGHT_LARGE = 10
    SPACING_SMALL = 5
    SPACING_MEDIUM = 8
    SIDEBAR_WIDTH = 4
    LABEL_WIDTH_SMALL = 60
    LABEL_WIDTH_MEDIUM = 80
    LABEL_WIDTH_LARGE = 150
    LABEL_WIDTH_XLARGE = 200
    BUTTON_BORDER_WIDTH = 1
    BUTTON_BORDER_WIDTH_THICK = 2
    BUTTON_BORDER_RADIUS = 2
    BUTTON_BORDER_RADIUS_LARGE = 3
    BUTTON_BORDER_RADIUS_XLARGE = 4
    BUTTON_MARGIN = 0
    BUTTON_PADDING = 5

class UIConfig:
    WORLD_CONTROLS_COLLAPSED = True
    JOINT_CONTROL_COLLAPSED = True
    VISIBILITY_CONTROL_COLLAPSED = True
    TRAJECTORY_STUDIO_COLLAPSED = True
    PHYSICS_DT = 1 / 100.0
    RENDERING_DT = 1 / 60.0
    GRAVITY = [0, 0, 0]
    SPHERE_LIGHT_PATH = "/World/SphereLight"
    SPHERE_LIGHT_RADIUS = 2
    SPHERE_LIGHT_INTENSITY = 100000
    SPHERE_LIGHT_POSITION = [6.5, 0, 12]
    RTX_FRACTIONAL_CUTOUT_OPACITY_KEY = "/rtx/raytracing/fractionalCutoutOpacity"
    RTX_FRACTIONAL_CUTOUT_OPACITY_VALUE = True

# ========================================
# 🧩 UI 컴포넌트 팩토리
# ========================================
import omni.ui as ui

class UIComponentFactory:
    @staticmethod
    def _create_ui_button(text, callback=None, height=UILayout.BUTTON_HEIGHT, style=None):
        if style is not None:
            return ui.Button(text, clicked_fn=callback, height=height, style=style)
        else:
            return ui.Button(text, clicked_fn=callback, height=height)
    @staticmethod
    def create_section_header(text, height=UILayout.LABEL_HEIGHT):
        return ui.Label(text, height=height)
    @staticmethod
    def create_separator(height=UILayout.SEPARATOR_HEIGHT):
        return ui.Separator(height=height)
    @staticmethod
    def create_spacer(width=UILayout.SPACING_SMALL):
        return ui.Spacer(width=width)
    @staticmethod
    def create_status_label(text, width=UILayout.LABEL_WIDTH_LARGE):
        return ui.Label(text, width=width)
    @staticmethod
    def create_colored_sidebar(color, width=UILayout.SIDEBAR_WIDTH, height=UILayout.BUTTON_HEIGHT):
        return ui.Rectangle(
            width=width, 
            height=height, 
            style={
                "background_color": color, 
                "border_radius": UILayout.BUTTON_BORDER_RADIUS
            }
        )
    @staticmethod
    def create_button(text, callback=None, height=UILayout.BUTTON_HEIGHT, style=None):
        return UIComponentFactory._create_ui_button(text, callback, height, style)
    @staticmethod
    def create_styled_button(text, callback=None, color_scheme='default', height=UILayout.BUTTON_HEIGHT):
        style_map = {
            'red': {
                "Button": {
                    "background_color": UIColors.RED_BUTTON_BG,
                    "border_width": UILayout.BUTTON_BORDER_WIDTH,
                    "border_color": UIColors.RED_BUTTON_BORDER,
                    "border_radius": UILayout.BUTTON_BORDER_RADIUS_LARGE
                },
                "Button:hovered": {"background_color": UIColors.RED_BUTTON_HOVER}
            },
            'yellow': {
                "Button": {
                    "background_color": UIColors.YELLOW_BUTTON_BG,
                    "border_width": UILayout.BUTTON_BORDER_WIDTH,
                    "border_color": UIColors.YELLOW_BUTTON_BORDER,
                    "border_radius": UILayout.BUTTON_BORDER_RADIUS_LARGE
                },
                "Button:hovered": {
                    "background_color": UIColors.YELLOW_BUTTON_HOVER
                }
            },
            'object_viz': {
                "Button": {
                    "background_color": UIColors.OBJECT_VIZ_BUTTON_BG,
                    "border_width": UILayout.BUTTON_BORDER_WIDTH,
                    "border_color": UIColors.OBJECT_VIZ_BUTTON_BORDER,
                    "border_radius": UILayout.BUTTON_BORDER_RADIUS_LARGE
                },
                "Button:hovered": {"background_color": UIColors.OBJECT_VIZ_BUTTON_HOVER}
            },
            'transparency': {
                "Button": {
                    "background_color": UIColors.TRANSPARENCY_BUTTON_BG,
                    "border_width": UILayout.BUTTON_BORDER_WIDTH,
                    "border_color": UIColors.TRANSPARENCY_BUTTON_BORDER,
                    "border_radius": UILayout.BUTTON_BORDER_RADIUS_LARGE,
                },
                "Button:hovered": {
                    "background_color": UIColors.TRANSPARENCY_BUTTON_HOVER,
                }
            },
            'green': {
                "Button": {
                    "background_color": UIColors.STATE_BUTTON_BG,
                    "border_width": UILayout.BUTTON_BORDER_WIDTH,
                    "border_color": UIColors.STATE_BUTTON_BORDER,
                    "border_radius": UILayout.BUTTON_BORDER_RADIUS_LARGE
                },
                "Button:hovered": {
                    "background_color": UIColors.STATE_BUTTON_HOVER
                }
            },
            'blue': {
                "Button": {
                    "background_color": UIColors.BLUE_BUTTON_BG,
                    "border_width": UILayout.BUTTON_BORDER_WIDTH,
                    "border_color": UIColors.BLUE_BUTTON_BORDER,
                    "border_radius": UILayout.BUTTON_BORDER_RADIUS_LARGE
                },
                "Button:hovered": {
                    "background_color": UIColors.BLUE_BUTTON_HOVER
                }
            },
            'default': None
        }
        style = style_map.get(color_scheme, None)
        return UIComponentFactory._create_ui_button(text, callback, height, style)


    @staticmethod
    def create_status_row(labels_and_widths):
        with ui.HStack(height=UILayout.LABEL_HEIGHT):
            status_labels = []
            for label_text, width in labels_and_widths:
                label = ui.Label(label_text, width=width)
                status_labels.append(label)
            return status_labels

    @staticmethod
    def create_button_row(buttons_config, height=UILayout.BUTTON_HEIGHT_LARGE):
        with ui.HStack(height=height):
            buttons = []
            for button_text, callback, style in buttons_config:
                button = UIComponentFactory._create_ui_button(
                    button_text, callback, UILayout.BUTTON_HEIGHT, style
                )
                buttons.append(button)
            return buttons
