import faulthandler

from view.view import SimulationView

faulthandler.enable()

if __name__ == "__main__":
    SimulationView().run()
