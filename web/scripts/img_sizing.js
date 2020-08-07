function scale_images() {
  imgs = document.getElementsByTagName("img")
  for (img of imgs) {
    var max_width = 0.7 * window.innerWidth
    console.log(max_width)
    if (img.naturalWidth > max_width) {
      console.log("in")
      img.width = max_width.toString()
    } else {
      img.width = img.naturalWidth.toString()
    }
  }
}
