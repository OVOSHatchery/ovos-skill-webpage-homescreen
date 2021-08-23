from mycroft import MycroftSkill, intent_file_handler


class WebpageHomescreen(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('homescreen.webpage.intent')
    def handle_homescreen_webpage(self, message):
        self.speak_dialog('homescreen.webpage')


def create_skill():
    return WebpageHomescreen()

