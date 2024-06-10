#!/usr/bin/env python3
""" Define an asynchronous coroutine function """
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """ Wait for a random delay between o and max_delay seconds """
    rand_number = random.uniform(0, max_delay)
    await asyncio.sleep(rand_number)
    return rand_number