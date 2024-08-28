from db.containers import DatabaseContainer as Container

container = Container()
container.wire(packages=[__name__])
