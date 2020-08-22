from plugins.screenshotapi.includes import screenshotapi

from core.models import action
from core import auth, db, helpers

class _websiteScreenshot(action._action):
    apiToken = str()
    targetURL = str()

    def run(self,data,persistentData,actionResult):
        if not hasattr(self,"plain_apiToken"):
            self.plain_apiToken = auth.getPasswordFromENC(self.apiToken)
        targetURL = helpers.evalString(self.targetURL,{"data" : data})
        screenshotClass = screenshotapi._screenshotapi(self.plain_apiToken)
        response = screenshotClass.takeScreenshot(targetURL)
        if response:
            actionResult["filename"] = screenshotClass.downloadScreenshot(response["screenshot"])
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["msg"] = "Screenshot taken and saved"
            return actionResult 
        actionResult["result"] = False
        actionResult["rc"] = 1
        actionResult["msg"] = "Error taking screenshot"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_websiteScreenshot, self).setAttribute(attr,value,sessionData=sessionData)
