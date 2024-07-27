import asyncio
from typing import Literal


def test(a: str) -> str:
    return "asdas" + a


async def main() -> Literal[0]:
    print("asdasds")
    print(test(122))
    return 0


if __name__ == "__main__":
    asyncio.run(main())
