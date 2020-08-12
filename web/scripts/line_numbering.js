var numbered = [];

function onClick(i) {
  return function() {
    numbered[i] = !numbered[i]
    number_lines()
  }
}

function initialize_headers() {
  var i = 0
  for (elem of document.getElementsByClassName("codeblock")) {
    numbered.push(true)
    div = document.createElement("div")
    div.className = "code-header"
    button = document.createElement("button")
    button.innerHTML = "#"
    button.style.backgroundColor = "transparent"
    button.style.color = "#ffffff"
    button.style.border = "2px"
    button.style.borderRadius = "4px";
    button.onclick = onClick(i)
    div.appendChild(button)
    elem.appendChild(div)
    i++
  }
}

function number_lines() {
  pres = document.getElementsByTagName("pre")
  var p = 0
  for (elem of pres) {
    if (numbered[p] && !elem.childNodes[0].innerHTML.includes("1. ")) {
      var code = elem.childNodes[0]
      var newHTML = ""
      var i = 0
      lines = code.innerHTML.split("\n")
      lines = lines
      for (line in lines) {
        if (i == 0) {
          newHTML += lines[line]+"\n"
          i++
          continue;
        }
        if (i < lines.length - 1) {
          if (i < 10) {
            newHTML += " "
          }
          newHTML += (i)+". "+lines[line]+"\n"
          i++
        }
      }
      code.innerHTML = newHTML
   } else if (!numbered[p]) {
     var code = elem.childNodes[0]
       code.innerHTML = code.innerHTML.replace(/[ ]?\d+\./g, "")
   }
   p++
 }
}
