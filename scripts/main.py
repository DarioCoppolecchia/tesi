from PacketController import PacketController

def main():
    # test
    input_path = '../logs/conn.log'
    config_path = 'config.ini'
    pw = PacketController(input_path)
    pw.load_paths_and_filters_from_config_file(config_path)
    preprocessed_lines = pw.normalize_lines()
    pw.conv_lines_to_PacketWrapper_list(preprocessed_lines)

if __name__ == "__main__":
    main()