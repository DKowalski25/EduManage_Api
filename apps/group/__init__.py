from .container import Container

container = Container()
container.wire(packages=[__name__])
