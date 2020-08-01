> July 20, 2020

# Mock Coding Interview Tool
[github](repo://mock-interview) [demo](demo://interview)
---

I have been practicing coding interviews with my computer science friends recently.  We have been sharing Leetcode over zoom.  Though this works, it is a very different environment than enterprise coding interview tools like [Code Pair](`https://www.hackerrank.com/products/codepair/?campaignid=1693960202&adgroupid=68741430191&adid=437658713184&gclid=CjwKCAjwgdX4BRB_EiwAg8O8Hf3MVY9G8Xdl-04nMZeergkaGS-9kdh-JR7Ecvk1xrRPyCEOV__FzRoCeyAQAvD_BwE`) or [CoderPad](https://coderpad.io/).  Unlike Leetcode, these tools do not have a "Submit" button that checks the solution.  Because it is so tempting to spam the Submit button, it would probably be more productive to practice with a real coding interview tool.  I couldn't find any free tools available, so I decided to implement my own.

## Specification

The mock coding interview tool must be a website capable of the following:
* Allow both users to be able to view and edit the code simultaneously; similar to google docs.
* Run the code whenever the interviewer or interviewee desires and display the output to both parties.  
* The language of the code will be assumed to be python because my friends and I almost exclusively use it for interviewers.  A possible extension to the project might be to add additional supported languages.

## Implementation

I used [Socket.IO](https://socket.io/) to sync code between all the users.  Because `node.js` has a clean Socket.IO library, [express](https://expressjs.com) was a natural choice for the backend.  Since I want to host this app in a place my friends can access, it seemed like a good idea to containerize the server using docker.  Using docker had the additional benefit of providing a filesystem where the interview session's code could be temporarily saved.   Additionally, running inside a container would allow for the installation of additional languages besides node, which could be used during the interview.  

### User Interface

![UI](/img/interview_tool.png)

The screen is divided into three sections using a table.  The leftmost contains the line numbers.  The column second from the left contains a `textarea`.  When the `textarea` is edited, the line numbers are updated to reflect the new interview session code.  The textarea's contents are synced between users using `socket.io`, which will be described in detail in the next section.  The rightmost column consists of a language selector, run button, and `div`s for holding program output and errors.  Though this user interface is barebones and ugly, it should be sufficient for the purpose of practice mock interviews with friends.    

### Socket.IO Logic

When a new client connects to the server for the first time, it needs to get the full contents of the code.  On connecting to the server, the frontend immediately sends a `get` command over socket.io:

```javascript
var socket = io.connect();
socket.on('connect', function(data) {
  socket.emit('get', '')
});
```

The backend receives this message and replies with a `file` command containing the code of the interview session.

```javascript
io.on("connection", function(client) {
  client.on("get", function(data) {
    client.emit("file", file)
  })

  ...

})
```

Upon receiving the `file` command from the server, the frontend updates a textarea with the interview session code.

```javascript
socket.on('file', function(data) {
  document.getElementById("code").value = data
  number()
});
```

> The number function updates the line numbering for the textfield.  See the full code for its implementation.

When the code is edited by a user, the frontend sends an `edit` command containing the modified code via socket.io to the server.  

```javascript
function onTyped() {
  var code = document.getElementById("code")
  number();
  socket.emit('edit', code.value)
}
```

This is recieved by the server, which broadcasts a `file` command with the updated code to the other clients.  When they recieve the file command, they will update their respective textareas with the latest code.

```javascript
client.on("edit", function(data) {
  file = data
  client.broadcast.emit("file", data)
})
```

The run button in the user interface sends a `run` command to the server.

```javascript
function onRun() {
    socket.emit('run', '')
}
```

The server responds by saving the code to file, running it using the python interpreter, and broadcasting a `results` command to all clients containing the `stdout` and `stderr` outputs from the program.

```javascript
client.on("run", function(data) {
    fs.writeFile("prog.py", file, function(err) {
      exec("python prog.py", function(error, stdout, stderr){
        client.emit("results", {
          output: stdout,
          error: stderr
        })
        client.broadcast.emit("results", {
          output: stdout,
          error: stderr
        })
      })
    })
  })
```

When the clients receive this message, they display this information to the user.

```javascript
socket.on('results', function(data) {
    var results = document.getElementById('results')
    var errors = document.getElementById('errors')
    results.innerHTML = data.output.replace("\n","<br>")
    errors.innerHTML = data.error.replace("\n", "<br>")
})
```

## Conclusion and Extensions

Though my homebrew mock interview tool satisfies my use case, it's quite different from most environments I've seen in actual interviews.  For example:

* It's only designed to host one interview at a time.
* It has no syntax highlighting and no code completion.
* It only supports python.

Of course, one could spin up many instances of this app and write another server to redirect new users to an available server.  This would provide support for multiple simultaneous interviews, and I might take on this project later.  Code highlighting can be implemented using a library like [highlight.js](https://highlightjs.org/).  Other languages can be supported by installing them in the container and trivially modifying the server code.  But unless my needs change, I'm probably going to leave the app as it is.
