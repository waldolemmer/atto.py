import asyncio
import json
import httpx

class StreamClient:
    def __init__(self, url, headers = None):
        self.url = url
        self.headers = headers or {}
        self._latest = None                  # stores the most recent object
        self._queue = asyncio.Queue(maxsize=1)
        self._task = None
        self._client = httpx.AsyncClient()

    async def start(self, on_update = None):
        """
        Kick off the background streaming task.
        on_update(obj) will be called for every new object (push mode).
        """
        if self._task and not self._task.done():
            raise RuntimeError("Stream already running")
        self._task = asyncio.create_task(self._run(on_update))

    async def _run(self, on_update):
        async with self._client.stream("GET", self.url, headers=self.headers) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)
                obj = self._parse(data)
                # update cache
                self._latest = obj
                # replace any waiting item in the queue so pull-mode always sees the newest
                try:
                    self._queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
                await self._queue.put(obj)
                # push-mode callback
                if on_update:
                    # if callback is sync, wrap it so it doesn’t block
                    if asyncio.iscoroutinefunction(on_update):
                        asyncio.create_task(on_update(obj))
                    else:
                        on_update(obj)

    def _parse(self, data: dict):
        """
        Override this (or monkey‑patch) to turn raw JSON into your domain object.
        """
        return data

    def get_latest(self):
        """
        Returns the most recent object (or None if none yet).
        """
        return self._latest

    async def get_next(self, timeout: float | None = None):
        """
        Wait for the next object—and give it to the caller.
        If timeout is set and no new object arrives in time, raises asyncio.TimeoutError.
        """
        if timeout is None:
            return await self._queue.get()
        return await asyncio.wait_for(self._queue.get(), timeout)

    async def stop(self):
        """
        Cancel the background task and close the HTTP client.
        """
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
        await self._client.aclose()
