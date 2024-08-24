class Timer:
    def __init__(self, config, root, alarm_sound, display_view):
        self.root = root
        self.display_view = display_view
        self.alarm_sound = alarm_sound
        self.config = config

        self.iMin = int(config.read("TIMER", "minutes"))
        self.iSec = int(config.read("TIMER", "seconds"))
        self.iTotal = f"{self.iMin:02}:{self.iSec:02}"
        self.wMin = self.iMin
        self.wSec = self.iSec
        self.working = False

    def run_timer(self):
        if not self.working:
            return
        self.display_view.update_display(f"{self.wMin:02}:{self.wSec:02}")
        if self.wMin == 0 and self.wSec == 0:
            self.alarm()
        else:
            if self.wSec == 0:
                self.wMin -= 1
                self.wSec = 59
            else:
                self.wSec -= 1
            self.root.after(1000, self.run_timer)

    def alarm(self):
        self.alarm_sound.play()

    def go_stop(self):
        if self.working:
            self.working = False
        else:
            self.working = True
            self.root.after(200, self.run_timer)

    def quit_all(self):
        self.root.destroy()

    def reset(self):            
        self.wMin = self.iMin
        self.wSec = self.iSec
        self.display_view.update_display(f"{self.iMin:02}:{self.iSec:02}")
        if not self.working:
            self.working = True
            
    