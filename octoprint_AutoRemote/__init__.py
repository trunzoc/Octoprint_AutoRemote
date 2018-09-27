# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import requests
from octoprint.events import Events

import os

#TODO LIST
#Add progress for % or Layer and textbox for value
#Add URL field for each trigger to make it a general webhook plugin instead of just AutoRemote

class OctoRemotePlugin(octoprint.plugin.StartupPlugin,
                        octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.EventHandlerPlugin):

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
            message = ""
	
            if 'remoteAddress' in payload:
                message += ",RemoteAddress:" + payload["remoteAddress"]
            if 'port' in payload:
                message += ",Port:" + payload["Port"]
            if 'baudrate' in payload:
                message += ",baudrate:" + payload["baudrate"]
            if 'error' in payload:
                message += ",error:" + payload["error"]
            if 'file' in payload:
                message += ",file:" + payload["file"]
            if 'filename' in payload:
                message += ",filename:" + payload["filename"]
            if 'name' in payload:
                message += ",name:" + payload["name"]
            if 'path' in payload:
                message += ",path:" + payload["path"]
            if 'origin' in payload:
                message += ",origin:" + payload["origin"]
            if 'time' in payload:
                message += ",time:" +  str(payload["time"])
            if 'firmwareError' in payload:
                message += ",firmwareError:" +  str(payload["firmwareError"])
            if 'position' in payload:
                message += ",position:" +  payload["position"]
            if 'gcode' in payload:
                message += ",gcode:" +  payload["gcode"]
            if 'movie' in payload:
                message += ",movie:" +  payload["movie"]
            if 'movie_basename' in payload:
                message += ",movie_basename:" +  payload["movie_basename"]
            if 'returncode' in payload:
                message += ",returncode:" +  payload["returncode"]
            if 'reason' in payload:
                message += ",reason:" +  payload["reason"]
            self._send_AutoRemote(event, autoremotekey, message)
        else:
            self._logger.info("Event skipped: %s" % event)
          
        
#         == Events.PRINT_DONE:
#            file = os.path.basename(payload["file"])
#            elapsed_time_in_seconds = payload["time"]
#            import datetime
#            import octoprint.util    
#            elapsed_time = octoprint.util.get_formatted_timedelta(datetime.timedelta(seconds=elapsed_time_in_seconds))
#            self._send_AutoRemote("PrintDone", file, elapsed_time)

    def _send_AutoRemote(self, trigger, autoremotekey, message=None):
        import requests
        url = "https://autoremotejoaomgcd.appspot.com/sendmessage?key=" + autoremotekey + "&message=" + trigger + "=:=" + message
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
