# Madiolahb
# Copyright 2011 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.

def main():
    from core import fill_character
    import acting
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', type=argparse.FileType('w'),
        default=sys.stdout)
    parser.add_argument('--output-format', '--ofmt',
        choices=('JSON', 'YAML'),
        default='JSON')
    parser.add_argument('--lifewheel-format', '--lfmt',
        choices=('JSON', 'YAML'),
        default='JSON')
    parser.add_argument('--lifewheel', '-l', type=argparse.FileType('r'),
        default=sys.stdin)

    subp = parser.add_subparsers()
    acting.register_commands(subp)

    args = parser.parse_args()

    lw = None
    if args.lifewheel_format == 'JSON':
        import json
        lw = json.load(args.lifewheel)
    elif args.lifewheel_format == 'YAML':
        import yaml
        lw = yaml.load(args.lifewheel)
    fill_character(lw)

    args.func(lw, **args.__dict__)
    if args.output_format == 'JSON':
        import json
        json.dump(lw, args.output)
    elif args.output_format == 'YAML':
        import yaml
        yaml.dump(lw, args.output)

if __name__ == "__main__":
    main()

# vim: ai et ts=4 sts=4 sw=4
