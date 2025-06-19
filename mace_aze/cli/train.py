import argparse
from mace_aze.pipe import trainer

def arg_parse():
    parser = argparse.ArgumentParser("Runs MACE training")
    parser.add_argument('--config', type=str, required=True, help="Location to configuration file")
    return parser.parse_args()

def main():
    args = arg_parse()
    trainer.train_mace(args.config)


if __name__ == "__main__":
    main()