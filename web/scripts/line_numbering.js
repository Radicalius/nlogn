function number_lines() {
  pres = document.getElementsByTagName("pre")
  for (elem in pres) {
    console.log(pres[elem])
    var code = pres[elem].childNodes[0]
    var newHTML = ""
    var i = 1
    lines = code.innerHTML.split("\n")
    lines = lines
    for (line in lines) {
      if (line > 0 && line < lines.length-1) {
        if (i < 10) {
          newHTML += " "
        }
        newHTML += (i)+". "+lines[line]+"\n"
        i++
      }
    }
    code.innerHTML = newHTML
  }
}