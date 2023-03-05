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
            "trigger": None
        }
        stage_config.update(self.configuration.get("stage_configuration", {}))
        del config["module"]
        stage_config.update(config)
        # TODO: setup GPIO trigger event.
        return Applet(**stage_config)

    def __render_applet(self, applet, scheduler):
        if applet is not None:
            self.rendercontext.display.clear()
            applet.module.render(self.rendercontext)
            self.rendercontext.display.update()
            if applet.update:
                scheduler.enter(
                    applet.update / 1000,
                    1,
                    self.__render_applet,
                    (applet, scheduler),
                )

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
        # Call intro.
        if intro is not None:
            scheduler.enter(
                next_stage, 1, self.__render_applet, (intro, scheduler)
            )
            next_stage += intro.time / 1000

        try:
            while True:
                for stage in stages:
                    scheduler.enter(
                        next_stage, 1, self.__render_applet, (stage, scheduler)
                    )
                    next_stage += stage.time / 1000
                scheduler.run()
                next_stage = stages[-1].time / 1000
        except KeyboardInterrupt:
            pass
        # Call shutdown
        if shutdown is not None:
            # render shutdown and exit function.
            scheduler = sched.scheduler()
            scheduler.enter(
                0, 1, self.__render_applet, (shutdown, scheduler)
            )
            scheduler.enter(
                shutdown.time / 1000,
                1,
                lambda: None,
            )
            scheduler.run()

    def run(self):
        """Start the application."""
        stages = self.setup()
        self.loop(stages)
        self.teardown(stages)
