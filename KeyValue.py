import argparse


class KeyValue(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())

        for value in values:
            key, value = value.split('=')
            if key in getattr(namespace, self.dest):
                getattr(namespace, self.dest)[key].append(value)
            else:
                getattr(namespace, self.dest)[key] = [value]
