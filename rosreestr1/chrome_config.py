import os
import zipfile
from selenium import webdriver


def proxy(HOST, PORT, USER, PASS):
    PROXY_HOST = HOST
    PROXY_PORT = PORT
    PROXY_USER = USER
    PROXY_PASS = PASS


    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    
    return manifest_json, background_js


def get_chromedriver(use_proxy=False, user_agent=None, PROXY_HOST=None, PROXY_PORT=None, PROXY_USER=None, PROXY_PASS=None):

    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    
    prefs = {'download.default_directory' : os.getcwd() + '\\pdfs', 'plugins.always_open_pdf_externally': True}
    chrome_options.add_experimental_option('prefs', prefs)
    # chrome_options.add_argument("--incognito")
    
    if use_proxy:
        manifest_json, background_js = proxy(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    current_path = os.getcwd()
    try:
    	driver = webdriver.Chrome(current_path + '/chromedriver', chrome_options=chrome_options)
    except:
    	driver = webdriver.Chrome(current_path + '/chromedriver.exe', chrome_options=chrome_options)
    return driver
  
