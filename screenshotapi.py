from core import plugin, model

class _screenshotapi(plugin._plugin):
    version = 1.0

    def install(self):
        # Register models
        model.registerModel("websiteScreenshot","_websiteScreenshot","_action","plugins.screenshotapi.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("websiteScreenshot","_websiteScreenshot","_action","plugins.screenshotapi.models.action")
        return True

    def upgrade(self,LatestPluginVersion):
        pass
