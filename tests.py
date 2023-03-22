from encoder import *


extension = "gif"
in_image_path = f"data/image.{extension}"
out_image_path = in_image_path.replace(f".{extension}", f"_encoded.{extension}")


def test_encode_message():
    in_message = "Hello Steganography!"
    encode_message(in_image_path, in_message, out_image_path, end_of_message_string="$")
    out_message = decode_message(out_image_path, end_of_message_string="$")

    assert in_message == out_message
