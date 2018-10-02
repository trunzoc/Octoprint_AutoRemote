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
        return dict(autoremotekey="",
		    autoremotesender="",
                    events=dict(Startup=False
					,Shutdown=False
					,ClientOpened=False
					,ClientClosed=False
					,ConnectivityChanged=False
					,Connecting=False
					,Connected=False
					,PrintStarted=False
					,Disconnecting=False
					,Disconnected=False
					,Error=False
					,PrinterStateChanged=False
                                        ,Upload=False
                                        ,FileAdded=False
                                        ,FileRemoved=False
                                        ,FolderAdded=False
                                        ,FolderRemoved=False
                                        ,UpdatedFiles=False
                                        ,MetadataAnalysisStarted=False
                                        ,MetadataAnalysisFinished=False
                                        ,FileSelected=False
                                        ,FileDeselected=False
                                        ,TransferStarted=False
                                        ,TransferDone=False
					,PrintFailed=False
					,PrintCancelling=False
					,PrintCancelled=False
					,PrintPaused=False
					,PrintResumed=False
					,PrintDone=False
					,MovieRendering=False
					,MovieDone=False
					,MovieFailed=False
					,CaptureStart=False
					,CaptureDone=False
					,CaptureFailed=False
                                        ,SettingsUpdated=False
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
        events = self._settings.get(['events'], merged=True)

	if event in events and events[event]:
            message = "OctoAutoremote=:={'Trigger':'" + event + "'"
	
            if not payload:
                payload = {}
                message = ",'NoData':'No_Data_For_This_Event'"
            else:
                for data in payload:
                    message += ",'%s':'%s'" % (data, str(payload[data]))
                    self._logger.debug("forming_Message: '%s':'%s'" % (data, str(payload[data])))

            message += "}"
            self._logger.info("Calling Send: Event: %s Message: %s" % (event, message))
            self._send_AutoRemote(message)
            self._logger.info("Called Send: Event: %s Message: %s" % (event, message))
        else:
            self._logger.info("Event skipped: %s" % event)

    def _send_AutoRemote(self, message=",'NoData':'No_Data_For_This_Event'"):
        import requests
	
        autoremotekey = self._settings.get(['autoremotekey'])
        autoremotesender = self._settings.get(['autoremotesender'])

	#url = "https://autoremotejoaomgcd.appspot.com/sendmessage"
        #url += "?key=" + autoremotekey
        #if autoremotesender:
        #    url += "&sender=" + autoremotesender
        #url += "&message=" + message
        
	#res = requests.post(url)
	
	url = "https://autoremotejoaomgcd.appspot.com/sendrequest"
        autoremote_header = {'content-type': 'application/x-www-form-urlencoded'}
        autoremote_json = {
            'key': autoremotekey,
            'request': {
                'message': message,
                'sender': autoremotesender,
                'communication_base_params': {
                     'type': 'Message'
                     }
                }
	}

	self._logger.info("Sending %s to URL: %s" % (autoremote_json, url))

	res = requests.post(url, data=autoremote_json, headers=autoremote_header)
		    
        self._logger.info("Response from %s: %s" % (url, res.text))
		    
		    
		    

    def get_update_information(self):
        return dict(
            OctoAutoremote=dict(
                displayName=self._plugin_name,
                displayVersion=self._plugin_version,

                type="github_release",
                current=self._plugin_version,
                user="trunzoc",
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
