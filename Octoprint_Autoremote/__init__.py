	# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import requests
from octoprint.events import Events

import os


class OctoRemotePlugin(octoprint.plugin.StartupPlugin,
                        octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.SettingsPlugin,
                        octopfrint.plugin.EventHandlerPlugin):

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        if (hasattr, self._settings, 'autoremotekey'):
#            self.autoremotekey = self._settings.get(["autoremotekey"])
            self._logger.info("Saving AutoRemote personal Key: %s" % self._settings.get(["autoremotekey"]))
        else:
#            self.autoremotekey=''
            self._logger.info("No Autoremote Personal key set while trying to save!")
                    
    def on_after_startup(self):
        self._logger.info("OctoRemote Plugin Active")
#        self.autoremotekey = self._settings.get(["autoremotekey"])
#        self._logger.debug("AutoRemote personal Key: %s" % self.autoremotekey)

    def get_settings_defaults(self):
        return dict(autoremotekey="",
                    events=dict(PrintStarted=False
				,PrintFailed=False
				,PrintCancelling=False
				,PrintCancelled=False
				,PrintPaused=False
				,PrintResumed=False
				,PrintDone=False
				,Progress=False
				,MovieRendering=False
				,MovieDone=False
				,MovieFailed=False
				,Error=False
				,Startup=False
				,Shutdown=False
				,Connecting=False
				,Connected=False
				,Disconnecting=False
				,Disconnected=False
				,ClientOpened=False
				,ClientClosed=False
			       )
                    )
                
            
    def get_template_configs(self):
        return [ dict(type="settings", name="OctoRemote", custom_bindings=False) ]

    def get_settings_restricted_paths(self):
        # only used in OctoPrint versions > 1.2.16
        return dict(admin=[["autoremotekey"]])

######

    def on_event(self, event, payload):
        events = self._settings.get(['events'], merged=True)
        autoremotekey = self._settings.get(['autoremotekey'])
#        self._logger.debug("on_event: autoremotekey: %s" % autoremotekey)
        if event in events and events[event]:
            v1 = v2 = v3 = ""
            if 'file' in payload:
                v1 = payload["name"]
            if 'time' in payload:
                v2 = str(payload["time"])
            if 'remoteAddress' in payload:
                v3 = payload["remoteAddress"]
            elif 'position' in payload:
                v3 = payload["position"]
            elif 'movie_basename' in payload:
                v3 = payload["movie_basename"]
            self._send_AutoRemote(event, autoremotekey, v1, v2, v3)
        else:
            self._logger.info("Event skipped: %s" % event)
          
        
#         == Events.PRINT_DONE:
#            file = os.path.basename(payload["file"])
#            elapsed_time_in_seconds = payload["time"]
#            import datetime
#            import octoprint.util    
#            elapsed_time = octoprint.util.get_formatted_timedelta(datetime.timedelta(seconds=elapsed_time_in_seconds))
#            self._send_AutoRemote("PrintDone", file, elapsed_time)


MESSAGE_HERE
    def _send_AutoRemote(self, trigger, autoremotekey, value1=None, value2=None, value3=None):
        import requests
        payload = "value1:" + value1 + ",value2:" + value2 + ",value3:" + value3
         url = "https://autoremotejoaomgcd.appspot.com/sendmessage?key=" + autoremotekey + "&message=" + trigger + "=:=" + payload
        res = requests.post(url)
        self._logger.info("URL: %s" % url)
        self._logger.info("Trigger: %s Response: %s" % (trigger, res.text))
        

    def get_update_information(self):
        return dict(
            OctoRemote=dict(
                displayName=self._plugin_name,
                displayVersion=self._plugin_version,

                type="github_release",
                current=self._plugin_version,
                user="sedgett",
                repo="OctoPrint_AutoRemote",
                stable_branch=dict(branch="master", name="Stable"),
                pip="https://github.com/trunzoc/Octoprint_Autoremote/archive/{target_version}.zip"
                )
            )

                                                                                            
######
                        
__plugin_name__ = "OctoRemote"
__plugin_implementation__ = OctoRemotePlugin()


global __plugin_hooks__
__plugin_hooks__ = {
                "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
                    }
