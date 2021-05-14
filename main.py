import Getters
import QTGui
if __name__ == "__main__":
    try:
        gui = QTGui.QTGui()
        gui.start()
    except BaseException as e:
        print(e)