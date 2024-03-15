from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler
from ovos_workshop.decorators import resting_screen_handler

MARK_II = "mycroft_mark_2"


class WebpageHomescreen(OVOSSkill):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_active = False

    def initialize(self):
        """Perform final setup of Skill."""
        # Disable manual refresh until this Homepage is made active.
        self.disable_intent("refresh-homepage.intent")
        self.settings_change_callback = self.refresh_homescreen

    def get_intro_message(self):
        """Provide instructions on first install."""
        self.speak_dialog("setting-url")

    @resting_screen_handler("Webpage Homescreen")
    def handle_request_to_use_homescreen(self, _):
        """Handler for requests from GUI to use this Homescreen."""
        self.is_active = True
        self.display_homescreen()
        self.refresh_homescreen()
        self.enable_intent("refresh-homepage.intent")

    def display_homescreen(self):
        """Display the selected webpage as the Homescreen."""
        default_url = "https://mycroft.ai"
        url = self.settings.get("homepage_url", default_url)
        self.gui.show_url(url)

    @intent_handler("refresh-homepage.intent")
    def refresh_homescreen(self):
        """Update refresh rate of homescreen and refresh screen.

        Defaults to 600 seconds / 10 minutes.
        """
        self.cancel_scheduled_event("refresh-webpage-homescreen")
        if self.is_active:
            self.schedule_repeating_event(
                self.display_homescreen,
                0,
                self.settings.get("refresh_frequency", 600),
                name="refresh-webpage-homescreen",
            )

    def shutdown(self):
        """Actions to perform when Skill is shutting down."""
        self.cancel_all_repeating_events()
