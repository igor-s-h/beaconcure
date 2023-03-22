from pathlib import Path
import imageio
import numpy as np


def convert_string_to_binary(message, end_of_message_string):
    message += end_of_message_string
    binary_message = ''.join([format(ord(i), "08b") for i in message])

    return binary_message


def decode_message(image_path, end_of_message_string="\0"):
    frames = imageio.v3.imread(image_path, index=...)
    message = decode_message_data(frames, end_of_message_string)
    return message


def decode_message_data(image_data, end_of_message_string="\0"):
    data = image_data.tobytes()

    data = list(data)
    message = ""
    for i in range(0, len(data), 8):
        byte = ''.join([str(c & 1) for c in data[i:i+8]])
        message += chr(int(byte, 2))
        if message[-1] == end_of_message_string:
            return message[:-1]

    return None


def encode_message(input_image_path, message, output_image_path, end_of_message_string="\0"):
    frames = imageio.v3.imread(input_image_path, index=...)
    encode_message_data(frames, message, output_image_path, end_of_message_string)


def encode_message_data(image_data, message, output_image_path, end_of_message_string="\0"):
    data = image_data.tobytes()
    binary_message = convert_string_to_binary(message, end_of_message_string)

    data = list(data)
    assert len(data) > len(binary_message), "The picture you are trying to use to encode the message is not big enough."

    for i in range(len(binary_message)):
        data[i] = (data[i] & 254) | int(binary_message[i])

    new_frames = np.asarray(data, dtype=np.uint8, order='C')
    new_frames = new_frames.reshape(image_data.shape)
    imageio.v3.imwrite(output_image_path, new_frames)



