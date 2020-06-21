> June 20th, 2020

# Web Browser Extension for Permalinking Pages

---
I've been applying to jobs recently.  When I apply to a job, I usually copy down the link to the job description in a spreadsheet so that I can refer back to it before interviewing.  However, job postings are not necessarily kept visible after they are closed to applications, which can be well before they interview candidates.  I recently found that many of the links I copied down are now broken.  I figure that I need a way of [permalinking](https://en.wikipedia.org/wiki/Permalink) job description pages, so that I can refer to them after they've been taken down.  Though there are probably many good tools available for saving pages, I wanted to try to make my own.
## The Specifics

I decided that what I really wanted was an in-browser button I could click that would copy a permalink to the clipboard.  [Web browser extensions](https://extensionworkshop.com/\#about) lend themselves nicely to this task, as they allow you to create a browser button that runs a script when clicked.  I opted to store the page on the local machine and run a web server in the background to process requests to the permalinks.  When the button in the web extension is pressed, it would send a request to the web server with the url of the active tab.  The HTTP server would download the source of the page, store it to disk, and send back a permalink to the web extension.  When the extension recieved the permalink it would copy it to the clipboard.

## Server Implementation

I wrote the backend web server using Python 3 + [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/).  The code for the add endpoint, which is responsible for permalink creation, is as follows:
```
@app.route("/add", methods=["POST"])
def add():
    url = request.form["url"].encode("utf8")
    hash = hashlib.sha256(url).hexdigest()
    resp = requests.get(url)
    file = open("pages/{0}".format(hash), "wb")
    file.write(resp.text.encode("utf8"))
    file.close()
    resp = make_response("http://localhost:8000/{0}".format(hash))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp
```
> Note the inclusion of the [Access-Control-Allow-Origin](https://web.dev/cross-origin-resource-sharing/) header.  This is necessary to ensure that the web extension script gets the response because the its origin will differ from that of the page being permalinked.

In a nutshell, the add endpoint stores the source of the page at the specified url in `pages/[hash]` where `hash` is the sha256 hash of the url. It responds with a permalink to the page which points back to the local web server.  Queries to the permalinks are handled by the get endpoint, which is implemented as follows:
```
app.route("/<hash>")
def get(hash):
    resp = send_file("pages/{0}".format(hash))
    resp.headers["Content-Type"] = "text/html"
    return resp
```  
> The Content-Type header is needed here because the files are not saved with the .html extension

To make it easier to run this server as a daemon, I wrapped it in a Docker container.

## Web Extension Implementation

To add a button to the toolbar, I added the following snippet to `manifest.json`:

```
"browser_action": {
    "browser_style": true,
    "default_icon": {
      "16": "icons/icon-16.png",
      "32": "icons/icon-32.png"
    }
  }
```
Getting this button to function required adding a backgound script which supplies an onclick listener using `browser.browserAction.onClicked.addListener`.  This was accomplished by first adding the following to `manifest.json`:
```
"background": {
   "scripts": ["background/bg.js"]
}
```
Then in `background/bg.js` I added the following onclick listener which queries the add endpoint with the url of the current tab:
```
browser.browserAction.onClicked.addListener((tab) => {
  var xhttp = new XMLHttpRequest()
  xhttp.onreadystatechange = function() {
    copyToClipboad(xhttp.responseText)
  }
  xhttp.open("POST", "http://localhost:8000/add", true)
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var url = encodeURIComponent(tab.url)
  xhttp.send("url="+url)
});
```
> Accessing `tab.url` requires the `tabs` permissions, which can be enabled in manifest.json

The listener also copies the permalink that is contained in the response to the clipboard by calling `copyToClipboad`.  The implementation is outlined below:
```
function copyToClipboad(text) {
  const el = document.createElement('textarea');
  el.value = text;
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);
}
```
> Using document.execCommand('copy') outside of a user generated event requires the `clipboardWrite` permission, which must be added to the manifest

## Conclusions and Extensions

Though the extension as written works pretty well for the purposes of saving job descriptions, it has some limitations:
* There is currently no user feedback when the web extension button is pressed.  Users might expect some kind of confirmation that the action completed successfully, e.g. a popup displaying `Copied to Clipboard`.  Because I am not planning on releasing this web extension, I am not too concerned about this.  However, it might be a nice addition to the project.
* When the backend fetches the page, it doesn't fetch any of the embedded objects (e.g. images, scripts, stylesheets) in that page.  This means that the page permalinked will almost always look different than the original page.  Because I'm only interested in the textual content of the page, this isn't too big of a deal.  But it wouldn't be that hard to have the server permalink all the urls embedded in the page.
* Some pages identify the backend server as a bot, and do not reply with the page requested.  I've been able to bypass bot detection on most pages by adding a realistic `Referer` and `User-Agent` header.  It is probably possible to get the source of any page using something like [Selenium](https://www.selenium.dev/documentation/en/), but that's probably beyond the scope of this project.
