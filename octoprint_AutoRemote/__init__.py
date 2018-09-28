# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import requests
from octoprint.events import Events

import os

#TODO LIST
#Add progress for % or Layer and textbox for value
#Add URL field for each trigger to make it a general webhook plugin instead of just AutoRemote

class OctoAutoremotePlugin(octoprint.plugin.StartupPlugin,
                        octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.EventHandlerPlugin):

#    def __init__(self):
#        self._logger = logging.getLogger("octoprint.plugins.OctoAutoremote")
#        self._OctoAutoremote_logger = logging.getLogger("octoprint.plugins.OctoAutoremote.debug")

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        if (hasattr, self._settings, 'autoremotekey'):
#            self.autoremotekey = self._settings.get(["autoremotekey"])
            self._logger.info("Saving AutoRemote personal Key: %s" % self._settings.get(["autoremotekey"]))
        else:
#            self.autoremotekey=''
            self._logger.info("No Autoremote Personal key set while trying to save!")
                    
    def on_after_startup(self):
        self._logger.info("OctoAutoremote Plugin Active")
#        self.autoremotekey = self._settings.get(["autoremotekey"])
#        self._logger.debug("AutoRemote personal Key: %s" % self.autoremotekey)

    def get_settings_defaults(self):
        return dict(
            autoremotekey = "",
            events = dict(
                PrintStarted=[dict(
                    enabled = False,
                    url = ""
                    )],
                PrintFailed=[dict(
                    enabled = False,
                    url = ""
                    )],
                PrintCancelling=[dict(
                    enabled = False,
                    url = ""
                    )],
                PrintCancelled=[dict(
                    enabled = False,
                    url = ""
                    )],
                PrintPaused=[dict(
                    enabled = False,
                    url = ""
                    )],
                PrintResumed=[dict(
                    enabled = False,
                    url = ""
                    )],
                PrintDone=[dict(
                    enabled = False,
                    url = ""
                    )],
                MovieRendering=[dict(
                    enabled = False,
                    url = ""
                    )],
                MovieDone=[dict(
                    enabled = False,
                    url = ""
                    )],
                MovieFailed=[dict(
                    enabled = False,
                    url = ""
                    )],
                Error=[dict(
                    enabled = False,
                    url = ""
                    )],
                Startup=[dict(
                    enabled = False,
                    url = ""
                    )],
                Shutdown=[dict(
                    enabled = False,
                    url = ""
                    )],
                Connecting=[dict(
                    enabled = False,
                    url = ""
                    )],
                Connected=[dict(
                    enabled = False,
                    url = ""
                    )],
                Disconnecting=[dict(
                    enabled = False,
                    url = ""
                    )],
                Disconnected=[dict(
                    enabled = False,
                    url = ""
                    )],
                ClientOpened=[dict(
                    enabled = False,
                    url = ""
                    )],
                ClientClosed=[dict(
                    enabled = False,
                    url = ""
                    )]
                )
            )
            
    def get_template_configs(self):
        return [ dict(type="settings", name="OctoAutoremote", custom_bindings=False) ]

    def get_assets(self):
        return dict(
            css=["css/octoautoremote.css"]
        )

    def get_settings_restricted_paths(self):
        # only used in OctoPrint versions > 1.2.16
        return dict(admin=[["autoremotekey"]])

######

    def on_event(self, event, payload):
        autoremotekey = self._settings.get(['autoremotekey'])
        self._logger.debug("on_event: autoremotekey: %s" % autoremotekey)
		
        events = self._settings.get(['events'], merged=True)
	if events == None or not event in events:
            return
	
	event_settings = events[event];
	if event_settings == None:
            return

	event_enabled = event_settings['enabled']
	if not event_enabled or event_enabled == False:
            self._logger.info("Event skipped: %s" % event)
            return

        message = ""

	if payload == None:
            payload = {}
            message += ",No_Message"

        if 'remoteAddress' in payload:
            message += ",RemoteAddress:" + payload["remoteAddress"]
            self._logger.debug("forming_Message: remoteAddress: %s" % payload["remoteAddress"])
        if 'port' in payload:
            message += ",port:" + str(payload["port"])
            self._logger.debug("forming_Message: port: %s" % str(payload["port"]))
        if 'baudrate' in payload:
            message += ",baudrate:" + str(payload["baudrate"])
            self._logger.debug("forming_Message: baudrate: %s" % str(payload["baudrate"]))
        if 'error' in payload:
            message += ",error:" + payload["error"]
            self._logger.debug("forming_Message: error: %s" % payload["error"])
        if 'name' in payload:
            message += ",name:" + payload["name"]
            self._logger.debug("forming_Message: name: %s" % payload["name"])
        if 'path' in payload:
            message += ",path:" + payload["path"]
            self._logger.debug("forming_Message: path: %s" % payload["path"])
        if 'origin' in payload:
            message += ",origin:" + payload["origin"]
            self._logger.debug("forming_Message: origin: %s" % payload["origin"])
        if 'time' in payload:
            message += ",time:" +  str(payload["time"])
            self._logger.debug("forming_Message: time: %s" % str(payload["time"]))
        if 'firmwareError' in payload:
            message += ",firmwareError:" +  str(payload["firmwareError"])
            self._logger.debug("forming_Message: firmwareError: %s" % payload["firmwareError"])
        if 'position' in payload:
            message += ",position:" +  payload["position"]
            self._logger.debug("forming_Message: position: %s" % payload["position"])
        if 'gcode' in payload:
            message += ",gcode:" +  payload["gcode"]
            self._logger.debug("forming_Message: gcode: %s" % payload["gcode"])
        if 'movie' in payload:
            message += ",movie:" +  payload["movie"]
            self._logger.debug("forming_Message: movie: %s" % payload["movie"])
        if 'movie_basename' in payload:
            message += ",movie_basename:" +  payload["movie_basename"]
            self._logger.debug("forming_Message: movie_basename: %s" % payload["movie_basename"])
        if 'returncode' in payload:
            message += ",returncode:" +  payload["returncode"]
            self._logger.debug("forming_Message: returncode: %s" % payload["returncode"])
        if 'reason' in payload:
            message += ",reason:" +  payload["reason"]
            self._logger.debug("forming_Message: reason: %s" % payload["reason"])

        message = message[1:]
        self._logger.info("Calling Send: Event: %s Key: %s Message: %s" % (event, autoremotekey, message))
        self._send_AutoRemote(event, autoremotekey, message)
        self._logger.info("Called Send: Event: %s Key: %s Message: %s" % (event, autoremotekey, message))
        
    def _send_AutoRemote(self, trigger, autoremotekey, message="No_Message"):
        import requests
        url = "https://autoremotejoaomgcd.appspot.com/sendmessage?key=" + autoremotekey + "&message=OctoAutoremote=:=" + trigger + "," + message
        res = requests.post(url)
        self._logger.info("URL: %s" % url)
        self._logger.info("Trigger: %s Response: %s" % (trigger, res.text))
        

    def get_update_information(self):
        return dict(
            OctoAutoremote=dict(
                displayName=self._plugin_name,
                displayVersion=self._plugin_version,

                type="github_release",
                current=self._plugin_version,
                user="sedgett",
                repo="octoprint_AutoRemote",
                stable_branch=dict(branch="master", name="Stable"),
                pip="https://github.com/trunzoc/octoprint_Autoremote/archive/{target_version}.zip"
                )
            )

                                                                                            
######
                        
__plugin_name__ = "OctoAutoremote"
__plugin_implementation__ = OctoAutoremotePlugin()


global __plugin_hooks__
__plugin_hooks__ = {
                "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
                    }
