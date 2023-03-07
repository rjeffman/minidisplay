# This file is part of minidisplay
#
# Copyright (C) 2023 Rafael Guterres Jeffman
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <https://www.gnu.org/licenses/>.

"""The minidisplay application."""

import sched
import importlib

from minidisplay import StageConfiguration, Applet
from minidisplay.errors import StageException


class Application:
    """Define the application framework."""

    def __init__(self, rendercontext, configuration):
        """Initialize application's render context and configuration."""
        self.rendercontext = rendercontext
        self.configuration = configuration

    def __init_applet(self, config):
        module = importlib.import_module(config.get("module"))
        if hasattr(module, "configure"):
            module.configure(self.rendercontext)
        stage_config = {
            "module": module,
            "time": 2000,
            "update": 1000 / 60,  # 1/60s
            "trigger": None,
        }
        stage_config.update(self.configuration.get("stage_configuration", {}))
        del config["module"]
        stage_config.update(config)
        # TODO: setup GPIO trigger event.
        return Applet(**stage_config)

    def __validate_stage(self, config):
        """Ensure stage is valide."""
        valid_items = ["module", "time", "update", "trigger"]
        if any(param for param in config.keys() if param not in valid_items):
            raise StageException("Stage with invalid parameter.")
        if not config.get("module"):
            raise StageException("Module not defined for parameter.")
        if config.get("time", 0) < config.get("update", 0):
            raise StageException(
                "Stage time must be at least equal to update."
            )
        return True

    def __render_applet(self, applet):
        self.rendercontext.display.clear()
        applet.module.render(self.rendercontext)
        self.rendercontext.display.update()

    def __update_applet(self, applet, scheduler):
        self.__render_applet(applet)
        scheduler.enter(  # miliseconds
            applet.update / 1000,
            1,
            self.__update_applet,
            (applet, scheduler),
        )

    def __schedule_applet(self, applet, scheduler):
        if applet is not None:
            # Clear all pending update events as we want only the
            # current applet to update.
            for event in scheduler.queue:
                if event.action is self.__update_applet:
                    scheduler.cancel(event)
            # Render applet.
            self.__render_applet(applet)
            # Schedule applet update
            if applet.update:
                scheduler.enter(
                    applet.update / 1000,  # miliseconds
                    1,
                    self.__update_applet,
                    (applet, scheduler),
                )

    def __clear_events(self, scheduler):
        """Clear all scheduled events."""
        for event in scheduler.queue:
            scheduler.cancel(event)

    def __schedule_stages(self, scheduler, stages, next_stage=0):
        """Schedule stages to be executed."""
        for stage in stages:
            scheduler.enter(
                next_stage, 1, self.__schedule_applet, (stage, scheduler)
            )
            next_stage += stage.time / 1000
        # Reschedule stages once all stages are done.
        scheduler.enter(
            next_stage, 10, self.__schedule_stages, (scheduler, stages)
        )

    def __screen_saver(self, screen_saver, scheduler):
        def blank_screen():
            self.rendercontext.display.clear()
            self.rendercontext.display.update()

        self.__clear_events(scheduler)
        scheduler.enter(0, 10, blank_screen)
        scheduler.enter(
            screen_saver.get("timeout", 10) * 60,  # minutes
            10,
            lambda: None,
        )
        scheduler.run(blocking=False)

    def setup(self):
        """Prepare for execution."""
        # setup applets
        intro = self.configuration.get("intro")
        if intro is not None:
            intro = self.__init_applet(intro)
        shutdown = self.configuration.get("shutdown")
        if shutdown is not None:
            shutdown = self.__init_applet(shutdown)
        applets = [
            self.__init_applet(cfg)
            for cfg in self.configuration.get("stages", [])
            if self.__validate_stage(cfg)
        ]
        # create stage list
        return StageConfiguration(intro, shutdown, applets)

    def teardown(self, stages):
        """Tear down applets and application."""
        intro, shutdown, stages = stages
        # call shutdown on all applets: stages, shutdown, intro
        stages.extend([shutdown, intro])
        for stage in stages:
            if stage is not None and hasattr(stage.module, "shutdown"):
                stage.module.shutdown(self.rendercontext)

    def loop(self, stages):
        """Entry point for application main loop."""
        # Extract applets
        intro, shutdown, stages = stages
        # create scheduler
        scheduler = sched.scheduler()
        # Prepare environment
        next_stage = 0
        screen_saver = self.configuration.get("screensaver")
        # Schedule intro.
        if intro is not None:
            scheduler.enter(
                next_stage, 1, self.__schedule_applet, (intro, scheduler)
            )
            next_stage += intro.time / 1000
        # Main Loop
        try:
            while True:
                scheduler.run(blocking=True)
                # Schedule stages
                self.__schedule_stages(scheduler, stages, next_stage)
                # Schedule screen saver
                if screen_saver:
                    scheduler.enter(
                        screen_saver["after"] * 60,  # minutes
                        1,
                        self.__screen_saver,
                        (
                            screen_saver,
                            scheduler,
                        ),
                    )
        except KeyboardInterrupt:
            self.__clear_events(scheduler)
        # Call shutdown
        if shutdown is not None:
            # render shutdown
            self.__clear_events(scheduler)
            scheduler.enter(
                0, 1, self.__schedule_applet, (shutdown, scheduler)
            )
            # Allow shutdown applet to display.
            scheduler.enter(shutdown.time / 1000, 1, lambda: None)
            # run shudown applet
            scheduler.run()

    def run(self):
        """Start the application."""
        stages = self.setup()
        self.loop(stages)
        self.teardown(stages)
