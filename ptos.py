
from burp import IBurpExtender
from burp import IProxyListener
from burp import ITab

import java.util.ArrayList

from javax.swing import BoxLayout
from javax.swing import JLabel
from javax.swing import JPanel
from javax.swing import JTable
from javax.swing import JTextField
from javax.swing import JTextArea
from javax.swing import JScrollPane

from java.awt import Component, GridLayout

import random
import sys

EXTNAME = "PTOS"
DEFAULT_COOKIE = "<insert your Datadog cookie here>"
class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
    # your extension code here
        print("registering %s" % EXTNAME)
        print(sys.version)
        apm_pl = APMProxyListener()
        apm_pl._helpers = callbacks.getHelpers()
        callbacks.registerProxyListener(apm_pl)
        callbacks.setExtensionName(EXTNAME);


        self.cookie_text = JTextField(DEFAULT_COOKIE,
                                      actionPerformed=self.change_cookie)

        self.cookie_value = None

        # Cookie form
        self._pane = JPanel(GridLayout(0,2))
        self._pane.add(JLabel("Cookie value"))
        self._pane.add(self.cookie_text)
        # Result data
        scrollpane = JScrollPane(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
                                 JScrollPane.HORIZONTAL_SCROLLBAR_NEVER)
        self.result_panel = JPanel()
        self.result_panel.layout = BoxLayout(self.result_panel, BoxLayout.Y_AXIS)
        scrollpane.viewport.view = self.result_panel

        self._pane.add(scrollpane)

        self.add_apm_info("yoyo")
        self.add_apm_info("blah")

        callbacks.addSuiteTab(self)

        return

    def add_apm_info(self, apm_info):

        p = JPanel()

        # image grabbing seems very expensive, good place for a callback?
        p.add(JLabel("path xx"))

        p.add(JTextArea(text = str(apm_info),
                        editable = False,
                        wrapStyleWord = True,
                        lineWrap = True,
                        alignmentX = Component.LEFT_ALIGNMENT,
                        size = (300, 1)
        ))

        self.result_panel.add(p)

    def change_cookie(self, _event):
        self.cookie_value = self.cookie_text.text

    def getTabCaption(self):
        return EXTNAME

    def getUiComponent(self):
        return self._pane

class APMProxyListener(IProxyListener):

    def processProxyMessage(self, messageIsRequest, message):
        # messageIsRequest bool
        # message IHttpRequestResponse
        reference = message.getMessageReference()
        if messageIsRequest:
            request = message.getMessageInfo().getRequest()
            request = self.inject_apm_header(reference, request)
            message.getMessageInfo().setRequest(request)

    def inject_apm_header(self, reference, request):
        # reference integer
        # request str

        request_info = self._helpers.analyzeRequest(request)
        # request_info IRequestInfo
        headers = request_info.getHeaders()
        url = get_url(headers)
        # headers [str]

        body_offset = request_info.getBodyOffset() # int
        str_body = self._helpers.bytesToString(request[body_offset:])

        trace_id = get_trace_id()
        parent_id = get_trace_id()
        headers2 = headers + [u"x-datadog-origin: rum",
                              u"x-datadog-parent-id: %s" % parent_id,
                              u"x-datadog-sampling-priority: 1",
                              u"x-datadog-trace-id: %s" % trace_id]
                              
        print("[%s] %s" % (trace_id, url))

        bytes_body = self._helpers.stringToBytes(str_body)

        return self._helpers.buildHttpMessage(java.util.ArrayList(headers2),
                                              bytes_body)


def get_trace_id():
    trace_id = [str(random.randint(0, 9)) for x in range(len("000000000000000000"))]
    return "".join(trace_id)


def get_url(headers):
    verb = headers[0]
    for h in headers[1:]:
        if ":" in h:
            k, v = h.split(":")
            if k.lower() == "host":
                return "%s %s" % (verb, v)
    return verb


"""
https://app.datadoghq.com/apm/trace/586946425901060058?spanID=1097379696551280573

x-datadog-origin: rum
x-datadog-parent-id: 1097379696551280573
x-datadog-sampling-priority: 1
x-datadog-trace-id: 586946425901060058

"""
