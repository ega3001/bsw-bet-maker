from typing import List

import attrs
import environ


@environ.config(prefix="BETMAKER")
class Config:
    @environ.config(prefix="DB")
    class DB:
        url: str = environ.var(
            validator=attrs.validators.instance_of(str), converter=str
        )

    @environ.config(prefix="SERVER")
    class SERVER:
        origin: str = environ.var(
            validator=attrs.validators.instance_of(str), converter=str
        )

    db: DB = environ.group(DB)
    server: SERVER = environ.group(SERVER)

    debug: bool = environ.var(
        validator=attrs.validators.instance_of(bool), converter=bool
    )


AppConfig = environ.to_config(Config)
