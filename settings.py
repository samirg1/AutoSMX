# Use like this: dmgbuild -s settings.py "Test Volume" test.dmg
filename = "AutoSMX.dmg"
volume_name = "AutoSMX"
format = "UDBZ"
size = None
files = ["build/AutoSMX.app"]
symlinks = {"Applications": "/Applications"}
icon = "autosmx.ico"

icon_locations = {"AutoSMX": (140, 120), "Applications": (500, 100)}
background = "builtin-arrow"
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
sidebar_width = 180
window_rect = ((100, 100), (640, 280))
default_view = "icon-view"

show_icon_preview = False
include_icon_view_settings = "auto"
include_list_view_settings = "auto"

# .. Icon view configuration ...................................................
arrange_by = None
grid_offset = (0, 0)
grid_spacing = 100
scroll_position = (0, 0)
label_pos = "bottom"  # or 'right'
text_size = 16
icon_size = 128

# .. List view configuration ...................................................
list_icon_size = 16
list_text_size = 12
list_scroll_position = (0, 0)
list_sort_by = "name"
list_use_relative_dates = True
list_calculate_all_sizes = (False,)
list_columns = ("name", "date-modified", "size", "kind", "date-added")
list_column_widths = {
    "name": 300,
    "date-modified": 181,
    "date-created": 181,
    "date-added": 181,
    "date-last-opened": 181,
    "size": 97,
    "kind": 115,
    "label": 100,
    "version": 75,
    "comments": 300,
}
list_column_sort_directions = {
    "name": "ascending",
    "date-modified": "descending",
    "date-created": "descending",
    "date-added": "descending",
    "date-last-opened": "descending",
    "size": "descending",
    "kind": "ascending",
    "label": "ascending",
    "version": "ascending",
    "comments": "ascending",
}

# .. License configuration .....................................................
license = {
    "default-language": "en_US",
    "licenses": {
        "en_GB": b"""{\\rtf1\\ansi\\ansicpg1252\\cocoartf1504\\cocoasubrtf820
 {\\fonttbl\\f0\\fnil\\fcharset0 Helvetica-Bold;\\f1\\fnil\\fcharset0 Helvetica;}
 {\\colortbl;\\red255\\green255\\blue255;\\red0\\green0\\blue0;}
 {\\*\\expandedcolortbl;;\\cssrgb\\c0\\c0\\c0;}
 \\paperw11905\\paperh16837\\margl1133\\margr1133\\margb1133\\margt1133
 \\deftab720
 \\pard\\pardeftab720\\sa160\\partightenfactor0

 \\f0\\b\\fs60 \\cf2 \\expnd0\\expndtw0\\kerning0
 \\up0\\nosupersub\\ulnone\\outl0\\strokewidth0\\strokec2License\\
 \\pard\\pardeftab720\\sa160\\partightenfactor0

 \\f1\\b0\\fs22\\cf2\\strokec2
This project is licensed under the Creative Commons Attribution - NonCommercial 4.0 International License.\\
 You are free to:\\
 - Share copy and redistribute the material in any medium or format \\
 - Adapt remix, transform, and build upon the material \\
 Under the following terms:\\
 - Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use. \\
 - Non-Commercial: You may not use the material for commercial purposes without obtaining prior written permission from the copyright holder. \\
 No additional restrictions. \\
 - You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits. For more details, please see the full license terms.
 }""",
    },
    "buttons": {
        "en_US": (
            b"English",
            b"Agree!",
            b"Disagree!",
            b"Print!",
            b"Save!",
            b'Do you agree or not? Press "Agree" or "Disagree".',
        ),
    },
}
