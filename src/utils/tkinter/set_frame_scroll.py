import customtkinter as ctk

def set_frame_scroll(scrollable_frame: ctk.CTkScrollableFrame, to_pos: float) -> None:
    scrollable_frame._parent_canvas.yview_moveto(to_pos / scrollable_frame.winfo_height())
