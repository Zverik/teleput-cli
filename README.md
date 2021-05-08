# Teleput CLI Tool

This is a command-line script to send messages and files
to yourself with the [Teleput Bot](https://t.me/teleput_bot).
Install it like this:

    pip3 install --user teleput

Then get a key from the bot (click the link above) and pass it to the tool:

    teleput -k YOUR_KEY

Now sending messages to yourself is simple:

    teleput "Message"
    pbpaste | teleput -

And even files:

    teleput review.docx
    teleput image.jpg

Note that it tries to detect the file format, so images and sounds will
be compressed. To send files without compression, use `--raw` switch:

    teleput -r image.jpg

Only one file can be sent. But you also can add a comment with a second argument:

    teleput image.jpg "Look at this image!"

## Author and License

Written by Ilya Zverev, published under the ISC license.
