from ..action import ReportAction
from ..config import buttoncombo

ReportAction.add_option("--emulate-xboxdrv", action="store_true",
                         help="Emulates the same joystick layout as a "
                              "Xbox 360 controller used via xboxdrv")
ReportAction.add_option("--emulate-xpad", action="store_true",
                        help="Emulates the same joystick layout as a wired "
                             "Xbox 360 controller used via the xpad module")
ReportAction.add_option("--emulate-xpad-wireless", action="store_true",
                        help="Emulates the same joystick layout as a wireless "
                             "Xbox 360 controller used via the xpad module")
ReportAction.add_option("--ignored-buttons", metavar="button(s)",
                        type=buttoncombo(","), default=[],
                        help="A comma-separated list of buttons to never send "
                             "as joystick events. For example specify 'PS' to "
                             "disable Steam's big picture mode shortcut when "
                             "using the --emulate-* options")
ReportAction.add_option("--mapping", metavar="mapping",
                        help="Use a custom button mapping specified in the "
                             "config file")
ReportAction.add_option("--trackpad-mouse", action="store_true",
                        help="Makes the trackpad control the mouse")
ReportAction.add_option("--udp-remap-buttons", action="store_true",
                        help="Swap A-B and X-Y in UDP reports")


class ReportActionInput(ReportAction):
    """Sends motion sensor data and battery level over UDP."""

    def __init__(self, *args, **kwargs):
        super(ReportActionInput, self).__init__(*args, **kwargs)

    def setup(self, device):
        if self.controller.server:
            self.controller.server.device_for_pad(self.controller.index - 1, device)

    def disable(self):
        pass

    def load_options(self, options):
        self.controller.remap = options.udp_remap_buttons

    def handle_report(self, report):
        if self.controller.server:
            self.controller.server.report_for_pad(self.controller.index - 1, report, remap=self.controller.remap)
