from src.PacketsModule.Packets import PacketController


def main():
    # test
    input_path = '../logs/conn.log'
    config_path = 'config.ini'
    pc = PacketController(input_path)
    pc.load_paths_and_filters_from_config_file(config_path)
    preprocessed_lines = pc.normalize_lines()
    pc.conv_lines_to_PacketWrapper_list(preprocessed_lines)
    pc.print_packetWrapper_list_to_json_file()

if __name__ == "__main__":
    main()