# reverse-color-blend

a small python script that unblends a color from an image, essentially reversing a normal blending operation with the selected color.

more info: [Alpha compositing](https://en.wikipedia.org/wiki/Alpha_compositing)

credit: [Legorol](https://forums.getpaint.net/topic/28014-unblend-reverse-normal-blend-with-a-chosen-color/)

### usage

```sh
$ python reverseblend.py input.png -c "#ffffff" -o output.png
```

- notes:
  - color should be specified in hex
  - requires `Pillow`, install using `pip install Pillow`

### example

- using `-c "#fd7c00"` ![#fd7c00](https://placehold.co/8/fd7c00/fd7c00)

![example](example.png)
