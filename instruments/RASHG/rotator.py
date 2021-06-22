from K10CR1.k10cr1 import K10CR1
import elliptec


def find_ports(type):
    if type == "K10CR1":
        return ["55001000", "55114554", "55114654"]
    elif type == "elliptec":
        return [port.device for port in elliptec.find_ports()]
    # more or less documentation on finding the rotators


class rotator():
    def __init__(self, i, type="K10CR1"):
        self.type = type
        if type == "K10CR1":
            self.rotator = K10CR1(i)
            self.home()

        elif type == "elliptec":
            self.rotator = elliptec.Motor(i)
            rotator.do_("forward")
        '''
        elif type == "thorlabs_apt":
            rotator = apt.Motor(i[1])
            rotator.set_move_home_parameters(2, 1, 10, 0)
            rotator.set_velocity_parameters(0, 10, 10)
            rotator.move_home()
            return rotator
        '''

    def home(self):
        if self.type == "K10CR1":
            self.rotator.home()
        elif self.type == "elliptec":
            self.rotator.do_("home")
    def move_abs(self,value):
        if self.type == "K10CR1":
            self.rotator.move_abs(value)
        elif self.type == "elliptec":
            val = self.rotator.deg_to_hex(value)
            self.rotator.set_('stepsize',val)

