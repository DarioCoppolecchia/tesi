from PacketController import PacketController

def main():
    # test
    input_path = '../logs/conn.log'
    config_path = 'config.ini'
    pc = PacketController(input_path)
    pc.load_paths_and_filters_from_config_file(config_path)
    preprocessed_lines = pc.normalize_lines()
    pw = pc.conv_lines_to_PacketWrapper_list(preprocessed_lines)
    
    list_ = list(pw.items())
    for l in list_:
        print(l[1])
        print('\n')

if __name__ == "__main__":
    main()