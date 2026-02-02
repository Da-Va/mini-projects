import sys

import rosbag2_py

def main(args):
    bag_file = args[1]

    reader = rosbag2_py.SequentialReader()
    reader.open(
        rosbag2_py.StorageOptions(uri=bag_file, storage_id="mcap"),
        rosbag2_py.ConverterOptions(
            input_serialization_format="cdr", output_serialization_format="cdr"
        )
    )


if __name__=='__main__':
    main(sys.argv)