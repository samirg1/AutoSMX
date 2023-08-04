from pynput import mouse

def get_click_position() -> tuple[int, int]:
    position: tuple[int, int] = -1, -1 
    def on_click(x: float, y: float, button: mouse.Button, pressed: bool):
        if button == mouse.Button.left and pressed:
            nonlocal position
            position = int(x), int(y)
            return False

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()

    return position